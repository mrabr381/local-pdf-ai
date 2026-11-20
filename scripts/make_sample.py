"""Generate the sample PDF (4-page tomato-growing guide) with reportlab.

The PDF itself is binary and gitignored — it is regenerated locally by
this script, so a fresh clone can rebuild it with one command:

    python scripts/make_sample.py
"""

from __future__ import annotations

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "sample_data", "sample.pdf")

# (heading, body) per page. Facts are deliberately distinct per page so
# Q&A citations can be checked by hand.
PAGES = [
    (
        "Choosing varieties and spacing",
        "There are two main types of tomato plant. Determinate varieties, "
        "such as Roma, grow to a fixed height of about 90 centimetres and "
        "ripen most of their fruit within a few weeks. Indeterminate "
        "varieties, such as Sungold, keep growing all season and need tall "
        "stakes or a trellis. Space plants 60 to 90 centimetres apart "
        "(24 to 36 inches) so air can circulate between them. Crowded "
        "plants stay damp and invite disease. Plant seedlings deep: bury "
        "the stem up to the first true leaves and roots will form along "
        "the buried stem, giving a stronger plant.",
    ),
    (
        "Soil, feeding and watering",
        "Tomatoes grow best in soil with a pH between 6.0 and 6.8. Test "
        "your soil before planting and add lime to raise the pH or sulphur "
        "to lower it. Mix in two handfuls of compost per planting hole. "
        "Water deeply but infrequently: tomato plants need 2.5 to 5 "
        "centimetres (1 to 2 inches) of water per week, delivered at the "
        "base of the plant. Wet leaves spread disease, so never use an "
        "overhead sprinkler in the evening. A layer of straw mulch 5 to 8 "
        "centimetres thick keeps the soil moist and stops soil splashing "
        "onto the lower leaves. Feed once a fortnight with a balanced "
        "liquid fertiliser after the first flowers appear.",
    ),
    (
        "Pests and diseases",
        "The most common pest is the tomato hornworm, a large green "
        "caterpillar that can strip a plant overnight. Pick hornworms off "
        "by hand in the morning and drop them into soapy water. Aphids "
        "cluster on young shoots; a strong jet of water knocks most of "
        "them off, and ladybirds eat the rest. Early blight shows as dark "
        "rings on the lower leaves — remove affected leaves at once and "
        "never compost them. Blossom-end rot is not a disease: it is a "
        "calcium problem caused by uneven watering, and the fix is steady, "
        "regular watering rather than any spray. A weekly neem oil spray "
        "in the evening helps against most insects without harming bees.",
    ),
    (
        "Harvest and storage",
        "Most varieties take 60 to 80 days from transplanting to the "
        "first ripe fruit. Pick tomatoes when they are fully coloured but "
        "still firm; a ripe tomato comes away with a gentle twist. "
        "Harvest in the morning when the flavour is at its best. Never "
        "store tomatoes in the fridge: cold temperatures destroy their "
        "flavour compounds and turn the flesh mealy. Keep them at room "
        "temperature, stem-side down, and eat them within five days. "
        "Green tomatoes left at the end of the season will ripen indoors "
        "in a paper bag with a banana. One healthy plant yields roughly "
        "4 to 7 kilograms of fruit over a season.",
    ),
]


def main() -> str:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    styles = getSampleStyleSheet()
    story = []
    for i, (heading, body) in enumerate(PAGES):
        if i:
            story.append(PageBreak())
        story.append(Paragraph(f"Page {i + 1} — {heading}", styles["Heading1"]))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(body, styles["BodyText"]))
    doc = SimpleDocTemplate(OUT, pagesize=A4,
                            title="The Beginner's Guide to Growing Tomatoes")
    doc.build(story)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes, {len(PAGES)} pages)")
    return OUT


if __name__ == "__main__":
    main()
