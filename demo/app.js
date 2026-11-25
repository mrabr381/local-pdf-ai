/* Local PDF AI — in-browser demo (demo/app.js).
 *
 * Static only: no server, no API key, no upload. The PDF you pick never
 * leaves your machine — PDF.js (CDN) extracts the text in the browser,
 * and the TF-IDF index below is a line-for-line port of the Python
 * backend in localpdfai/chunking.py, localpdfai/embeddings.py and
 * localpdfai/index.py:
 *
 *   - chunking: ~600-char chunks, never crossing a page boundary,
 *     100-char overlap carried into the next chunk.
 *   - tokenize: lowercase [a-z0-9]+ tokens, same stopword list.
 *   - TF-IDF: idf = ln((n+1)/(df+1)) + 1, tf = 1 + ln(count),
 *     rows L2-normalised.
 *   - search: cosine similarity, ties broken by chunk order
 *     (deterministic — same question, same answer).
 *
 * The pure functions (tokenize / chunkPages / TfidfEmbedder / buildIndex /
 * search) have no DOM dependency, so they can also be run under node for
 * testing: `node -e "const d = require('./app.js'); ..."`.
 */

"use strict";

/* ------------------------------------------------------------------ */
/* Chunking — mirrors localpdfai/chunking.py                           */
/* ------------------------------------------------------------------ */

const MAX_CHUNK_CHARS = 600;
const OVERLAP_CHARS = 100;

// Split on whitespace that follows a sentence-ending mark, exactly as
// Python's re.compile(r"(?<=[.!?])\s+") does.
const SENTENCE_END = /(?<=[.!?])\s+/;

function splitSentences(text) {
  const parts = text.split(SENTENCE_END).map((s) => s.trim()).filter(Boolean);
  const out = [];
  for (let part of parts) {
    // A very long "sentence" (no punctuation) is hard-split so no chunk
    // ever grows unbounded — same cut rule as the Python version.
    while (part.length > MAX_CHUNK_CHARS) {
      let cut = part.lastIndexOf(" ", MAX_CHUNK_CHARS - 1);
      if (cut <= 100) cut = MAX_CHUNK_CHARS;
      out.push(part.slice(0, cut).trim());
      part = part.slice(cut).trim();
    }
    if (part) out.push(part);
  }
  return out;
}

function chunkPages(pages) {
  // pages: [{page: 1-based number, text: string}, ...]
  // Returns [{id, page, text}, ...]; chunks never cross a page boundary.
  const chunks = [];
  for (const page of pages) {
    const sentences = splitSentences(page.text.split(/\s+/).join(" "));
    let current = "";
    for (const sentence of sentences) {
      const candidate = current ? current + " " + sentence : sentence;
      if (candidate.length > MAX_CHUNK_CHARS && current) {
        chunks.push({ id: chunks.length, page: page.page, text: current });
        // Overlap: carry the tail of the finished chunk forward.
        current = (current.slice(-OVERLAP_CHARS) + " " + sentence).trim();
        if (current.length > MAX_CHUNK_CHARS) {
          chunks.push({ id: chunks.length, page: page.page, text: current });
          current = "";
        }
      } else {
        current = candidate;
      }
    }
    if (current) {
      chunks.push({ id: chunks.length, page: page.page, text: current });
    }
  }
  return chunks;
}

/* ------------------------------------------------------------------ */
/* TF-IDF — mirrors localpdfai/embeddings.py (TfidfEmbedder)           */
/* ------------------------------------------------------------------ */

// Same small English stopword list as the Python backend, verbatim.
const STOPWORDS = new Set(
  ("a an the and or but if then else for of to in on at by with from as is are " +
    "was were be been being it its this that these those there here what which " +
    "who whom how when where why can could should would will shall may might " +
    "do does did have has had not no yes you your he she we they them his her " +
    "our their i me my we us our do does did is am are was were be been being")
    .split(/\s+/)
    .filter(Boolean)
);

function tokenize(text) {
  const found = text.toLowerCase().match(/[a-z0-9]+/g) || [];
  return found.filter((t) => !STOPWORDS.has(t));
}

class TfidfEmbedder {
  constructor() {
    this.vocab = new Map(); // token -> column index
    this.idf = []; // per-column idf, aligned with vocab order
  }

  fit(texts) {
    const df = new Map();
    for (const text of texts) {
      for (const token of new Set(tokenize(text))) {
        df.set(token, (df.get(token) || 0) + 1);
      }
    }
    const sorted = [...df.keys()].sort();
    this.vocab = new Map(sorted.map((token, i) => [token, i]));
    const n = Math.max(texts.length, 1);
    this.idf = sorted.map(
      (token) => Math.log((n + 1) / (df.get(token) + 1)) + 1.0
    );
  }

  embed(texts) {
    const dim = this.vocab.size;
    return texts.map((text) => {
      const row = new Array(dim).fill(0);
      const counts = new Map();
      for (const token of tokenize(text)) {
        const idx = this.vocab.get(token);
        if (idx !== undefined) counts.set(idx, (counts.get(idx) || 0) + 1);
      }
      for (const [idx, count] of counts) {
        // log-scaled TF x IDF
        row[idx] = (1.0 + Math.log(count)) * this.idf[idx];
      }
      let norm = Math.sqrt(row.reduce((sum, v) => sum + v * v, 0));
      if (norm === 0) norm = 1.0;
      return row.map((v) => v / norm);
    });
  }
}

/* ------------------------------------------------------------------ */
/* Index + search — mirrors localpdfai/index.py (Index.build/search)   */
/* ------------------------------------------------------------------ */

function buildIndex(pages) {
  const chunks = chunkPages(pages);
  if (!chunks.length) {
    throw new Error("no chunks could be built from this document");
  }
  const embedder = new TfidfEmbedder();
  const texts = chunks.map((c) => c.text);
  embedder.fit(texts);
  const matrix = embedder.embed(texts);
  return { chunks, matrix, embedder };
}

function search(index, query, topK) {
  if (!query || !query.trim()) {
    throw new Error("question must not be empty");
  }
  const k = topK || 3;
  const queryVec = index.embedder.embed([query])[0];
  const scored = index.matrix.map((row, i) => ({
    chunk: index.chunks[i],
    // cosine: rows are L2-normalised, so the dot product is the cosine.
    score: row.reduce((sum, v, j) => sum + v * queryVec[j], 0),
    order: i,
  }));
  // Stable: ties keep chunk order, so the same question always returns
  // the same passages (Array.sort is stable, the tiebreak is explicit).
  scored.sort((a, b) => b.score - a.score || a.order - b.order);
  return scored.slice(0, k).map(({ chunk, score }) => ({ chunk, score }));
}

function extractiveAnswer(results) {
  const lines = ["Based on the document, here are the most relevant passages:", ""];
  results.forEach((result, i) => {
    lines.push(
      `${i + 1}. [p. ${result.chunk.page}] (relevance ${result.score.toFixed(2)})`
    );
    lines.push(`   ${result.chunk.text}`);
    lines.push("");
  });
  lines.push(
    "This is an extractive answer: it quotes the document directly " +
      "instead of rephrasing it, so nothing is invented."
  );
  return lines.join("\n").trim();
}

/* ------------------------------------------------------------------ */
/* Built-in sample — the tomato-growing guide from                    */
/* scripts/make_sample.py (the repo's offline test fixture).           */
/* Quoted verbatim, page by page, so the demo reproduces the fixture  */
/* exactly: 4 pages, 7 chunks, 6/6 questions top-1 correct.           */
/* ------------------------------------------------------------------ */

const SAMPLE_PAGES = [
  {
    page: 1,
    text:
      "Page 1 — Choosing varieties and spacing There are two main types of tomato plant. " +
      "Determinate varieties, such as Roma, grow to a fixed height of about 90 centimetres and " +
      "ripen most of their fruit within a few weeks. Indeterminate varieties, such as Sungold, " +
      "keep growing all season and need tall stakes or a trellis. Space plants 60 to 90 " +
      "centimetres apart (24 to 36 inches) so air can circulate between them. Crowded plants " +
      "stay damp and invite disease. Plant seedlings deep: bury the stem up to the first true " +
      "leaves and roots will form along the buried stem, giving a stronger plant.",
  },
  {
    page: 2,
    text:
      "Page 2 — Soil, feeding and watering Tomatoes grow best in soil with a pH between 6.0 and 6.8. " +
      "Test your soil before planting and add lime to raise the pH or sulphur to lower it. Mix in " +
      "two handfuls of compost per planting hole. Water deeply but infrequently: tomato plants need " +
      "2.5 to 5 centimetres (1 to 2 inches) of water per week, delivered at the base of the plant. " +
      "Wet leaves spread disease, so never use an overhead sprinkler in the evening. A layer of " +
      "straw mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the " +
      "lower leaves. Feed once a fortnight with a balanced liquid fertiliser after the first flowers appear.",
  },
  {
    page: 3,
    text:
      "Page 3 — Pests and diseases The most common pest is the tomato hornworm, a large green " +
      "caterpillar that can strip a plant overnight. Pick hornworms off by hand in the morning and " +
      "drop them into soapy water. Aphids cluster on young shoots; a strong jet of water knocks " +
      "most of them off, and ladybirds eat the rest. Early blight shows as dark rings on the lower " +
      "leaves — remove affected leaves at once and never compost them. Blossom-end rot is not a " +
      "disease: it is a calcium problem caused by uneven watering, and the fix is steady, regular " +
      "watering rather than any spray. A weekly neem oil spray in the evening helps against most " +
      "insects without harming bees.",
  },
  {
    page: 4,
    text:
      "Page 4 — Harvest and storage Most varieties take 60 to 80 days from transplanting to the " +
      "first ripe fruit. Pick tomatoes when they are fully coloured but still firm; a ripe tomato " +
      "comes away with a gentle twist. Harvest in the morning when the flavour is at its best. " +
      "Never store tomatoes in the fridge: cold temperatures destroy their flavour compounds and " +
      "turn the flesh mealy. Keep them at room temperature, stem-side down, and eat them within " +
      "five days. Green tomatoes left at the end of the season will ripen indoors in a paper bag " +
      "with a banana. One healthy plant yields roughly 4 to 7 kilograms of fruit over a season.",
  },
];

// The six fixture questions from tests/test_qa.py — all top-1 correct
// against this sample (see sample_output/qa_report.md).
const SAMPLE_QUESTIONS = [
  "What soil pH do tomatoes need?",
  "How much water do tomato plants need each week?",
  "How do I deal with tomato hornworms?",
  "How long until tomatoes are ready to harvest?",
  "Should I store tomatoes in the fridge?",
  "How far apart should I space tomato plants?",
];

const UPLOAD_QUESTIONS = [
  "What is this document about?",
  "What are the key numbers or dates in it?",
  "What should I do first?",
];

/* ------------------------------------------------------------------ */
/* Browser UI — only runs when loaded in a page (not under node).      */
/* PDF.js comes from the CDN (see index.html); everything else here    */
/* is plain JS. The uploaded file is read with FileReader and never    */
/* sent anywhere.                                                      */
/* ------------------------------------------------------------------ */

if (typeof document !== "undefined") {
  const PDFJS_CDN_VERSION = "3.11.174";
  const PDFJS_WORKER_URL =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/" +
    PDFJS_CDN_VERSION +
    "/pdf.worker.min.js";

  let currentIndex = null;
  let currentSource = "";

  const $ = (id) => document.getElementById(id);

  function escapeHtml(s) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function setStatus(msg, isError) {
    const el = $("status");
    el.textContent = msg;
    el.classList.toggle("error", !!isError);
  }

  function setExampleQuestions(questions) {
    const box = $("examples");
    box.innerHTML = "";
    for (const q of questions) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip";
      chip.textContent = q;
      chip.addEventListener("click", () => {
        $("question").value = q;
        ask();
      });
      box.appendChild(chip);
    }
  }

  function showIndex(sourceLabel, pages, index) {
    currentIndex = index;
    currentSource = sourceLabel;
    $("doc-stats").innerHTML =
      "<strong>" + escapeHtml(sourceLabel) + "</strong> — " +
      pages.length + " page" + (pages.length === 1 ? "" : "s") + ", " +
      index.chunks.length + " chunks, " +
      index.embedder.vocab.size + " indexed words (TF-IDF).";
    $("ask-btn").disabled = false;
    $("question").disabled = false;
    $("question").focus();
  }

  function loadSample() {
    try {
      const index = buildIndex(SAMPLE_PAGES);
      showIndex("Built-in sample: The Beginner's Guide to Growing Tomatoes", SAMPLE_PAGES, index);
      setExampleQuestions(SAMPLE_QUESTIONS);
      setStatus(
        "Sample guide loaded — 4 pages, " + index.chunks.length + " chunks. " +
        "Ask a question below, or upload your own PDF."
      );
      $("results").innerHTML =
        "<p class=\"muted\">Try a question — for example, " +
        "“What soil pH do tomatoes need?” (top passage: p. 2, relevance 0.33).</p>";
    } catch (err) {
      setStatus("Could not build the sample index: " + err.message, true);
    }
  }

  async function extractPagesFromPdf(arrayBuffer) {
    if (typeof window.pdfjsLib === "undefined") {
      throw new Error(
        "PDF.js did not load from the CDN — check your connection and reload the page. " +
        "The built-in sample below still works without it."
      );
    }
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER_URL;
    const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    const pages = [];
    for (let n = 1; n <= pdf.numPages; n++) {
      setStatus("Reading page " + n + " of " + pdf.numPages + "…");
      const page = await pdf.getPage(n);
      const content = await page.getTextContent();
      const text = content.items.map((item) => item.str || "").join(" ");
      pages.push({ page: n, text: text.trim() });
      // Let the status line repaint on long documents.
      await new Promise((resolve) => setTimeout(resolve, 0));
    }
    if (!pages.some((p) => p.text)) {
      throw new Error(
        "no extractable text in this PDF — it may be a scanned image-only PDF " +
        "(OCR is not supported yet)"
      );
    }
    return pages;
  }

  async function handleFile(file) {
    if (!file) return;
    if (!/\.pdf$/i.test(file.name) && file.type !== "application/pdf") {
      setStatus("That does not look like a PDF — please pick a .pdf file.", true);
      return;
    }
    $("ask-btn").disabled = true;
    $("question").disabled = true;
    $("results").innerHTML = "";
    setStatus("Reading " + file.name + "…");
    try {
      const arrayBuffer = await file.arrayBuffer();
      const pages = await extractPagesFromPdf(arrayBuffer);
      const index = buildIndex(pages);
      showIndex(file.name, pages, index);
      setExampleQuestions(UPLOAD_QUESTIONS);
      setStatus(
        "Indexed " + file.name + " — " + pages.length + " pages, " +
        index.chunks.length + " chunks. Ask a question below."
      );
      $("results").innerHTML =
        "<p class=\"muted\">Document ready. Ask in the document's own words for the best matches — " +
        "TF-IDF matches on words, not meaning.</p>";
    } catch (err) {
      setStatus("Could not read that PDF: " + err.message, true);
      $("ask-btn").disabled = false;
      $("question").disabled = false;
    }
  }

  function ask() {
    if (!currentIndex) {
      setStatus("Load the sample or upload a PDF first.", true);
      return;
    }
    const question = $("question").value;
    const topK = parseInt($("topk").value, 10) || 3;
    let results;
    try {
      results = search(currentIndex, question, topK);
    } catch (err) {
      setStatus(err.message, true);
      return;
    }
    const started = performance.now();
    const box = $("results");
    let html =
      "<p>Based on the document, here are the most relevant passages:</p><ol class=\"answers\">";
    for (const result of results) {
      html +=
        "<li><div class=\"cite\">[p. " + result.chunk.page + "] " +
        "<span class=\"score\">relevance " + result.score.toFixed(2) + "</span></div>" +
        "<div class=\"passage\">" + escapeHtml(result.chunk.text) + "</div></li>";
    }
    html += "</ol>";
    html +=
      "<p class=\"muted\">This is an extractive answer: it quotes the document directly " +
      "instead of rephrasing it, so nothing is invented. " +
      "Answered from “" + escapeHtml(currentSource) + "” in " +
      Math.max(1, Math.round(performance.now() - started)) + " ms.</p>";
    box.innerHTML = html;
    setStatus(
      "Top passage: p. " + results[0].chunk.page +
      " (relevance " + results[0].score.toFixed(2) + ")."
    );
  }

  document.addEventListener("DOMContentLoaded", () => {
    $("sample-btn").addEventListener("click", loadSample);
    $("file-input").addEventListener("change", (e) => handleFile(e.target.files[0]));
    $("ask-btn").addEventListener("click", ask);
    $("question").addEventListener("keydown", (e) => {
      if (e.key === "Enter") ask();
    });

    const dropzone = $("dropzone");
    ["dragenter", "dragover"].forEach((evt) =>
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragging");
      })
    );
    ["dragleave", "drop"].forEach((evt) =>
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragging");
      })
    );
    dropzone.addEventListener("drop", (e) => {
      const file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      handleFile(file);
    });

    // The demo works immediately: the sample is indexed on load, so Ask
    // works with zero clicks. Uploading a PDF replaces it.
    loadSample();
  });
}

/* Node export (for testing the QA logic without a browser). */
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    MAX_CHUNK_CHARS,
    OVERLAP_CHARS,
    STOPWORDS,
    tokenize,
    splitSentences,
    chunkPages,
    TfidfEmbedder,
    buildIndex,
    search,
    extractiveAnswer,
    SAMPLE_PAGES,
    SAMPLE_QUESTIONS,
  };
}
