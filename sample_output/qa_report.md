# Sample Q&A verification report

Sample document: `sample_data/sample.pdf` — *The Beginner's Guide to Growing Tomatoes*, 4 pages, regenerated with `python scripts/make_sample.py`. Index: 4 pages, 7 chunks, TF-IDF backend.

Each question was run with:

```
python -m localpdfai ask --pdf sample_data/sample.pdf --index sample_output/sample_index.json --q "..."
```

## Q: What soil pH do tomatoes need?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 2] (relevance 0.33)
   Page 2 — Soil, feeding and watering Tomatoes grow best in soil with a pH between 6.0 and 6.8. Test your soil before planting and add lime to raise the pH or sulphur to lower it. Mix in two handfuls of compost per planting hole. Water deeply but infrequently: tomato plants need 2.5 to 5 centimetres (1 to 2 inches) of water per week, delivered at the base of the plant. Wet leaves spread disease, so never use an overhead sprinkler in the evening. A layer of straw mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the lower leaves.

2. [p. 2] (relevance 0.16)
   mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the lower leaves. Feed once a fortnight with a balanced liquid fertiliser after the first flowers appear.

3. [p. 4] (relevance 0.08)
   Page 4 — Harvest and storage Most varieties take 60 to 80 days from transplanting to the first ripe fruit. Pick tomatoes when they are fully coloured but still firm; a ripe tomato comes away with a gentle twist. Harvest in the morning when the flavour is at its best. Never store tomatoes in the fridge: cold temperatures destroy their flavour compounds and turn the flesh mealy. Keep them at room temperature, stem-side down, and eat them within five days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

## Q: How much water do tomato plants need each week?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 2] (relevance 0.25)
   Page 2 — Soil, feeding and watering Tomatoes grow best in soil with a pH between 6.0 and 6.8. Test your soil before planting and add lime to raise the pH or sulphur to lower it. Mix in two handfuls of compost per planting hole. Water deeply but infrequently: tomato plants need 2.5 to 5 centimetres (1 to 2 inches) of water per week, delivered at the base of the plant. Wet leaves spread disease, so never use an overhead sprinkler in the evening. A layer of straw mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the lower leaves.

2. [p. 1] (relevance 0.15)
   Page 1 — Choosing varieties and spacing There are two main types of tomato plant. Determinate varieties, such as Roma, grow to a fixed height of about 90 centimetres and ripen most of their fruit within a few weeks. Indeterminate varieties, such as Sungold, keep growing all season and need tall stakes or a trellis. Space plants 60 to 90 centimetres apart (24 to 36 inches) so air can circulate between them. Crowded plants stay damp and invite disease. Plant seedlings deep: bury the stem up to the first true leaves and roots will form along the buried stem, giving a stronger plant.

3. [p. 3] (relevance 0.11)
   Page 3 — Pests and diseases The most common pest is the tomato hornworm, a large green caterpillar that can strip a plant overnight. Pick hornworms off by hand in the morning and drop them into soapy water. Aphids cluster on young shoots; a strong jet of water knocks most of them off, and ladybirds eat the rest. Early blight shows as dark rings on the lower leaves — remove affected leaves at once and never compost them. Blossom-end rot is not a disease: it is a calcium problem caused by uneven watering, and the fix is steady, regular watering rather than any spray.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

## Q: How do I deal with tomato hornworms?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 3] (relevance 0.16)
   Page 3 — Pests and diseases The most common pest is the tomato hornworm, a large green caterpillar that can strip a plant overnight. Pick hornworms off by hand in the morning and drop them into soapy water. Aphids cluster on young shoots; a strong jet of water knocks most of them off, and ladybirds eat the rest. Early blight shows as dark rings on the lower leaves — remove affected leaves at once and never compost them. Blossom-end rot is not a disease: it is a calcium problem caused by uneven watering, and the fix is steady, regular watering rather than any spray.

2. [p. 4] (relevance 0.04)
   Page 4 — Harvest and storage Most varieties take 60 to 80 days from transplanting to the first ripe fruit. Pick tomatoes when they are fully coloured but still firm; a ripe tomato comes away with a gentle twist. Harvest in the morning when the flavour is at its best. Never store tomatoes in the fridge: cold temperatures destroy their flavour compounds and turn the flesh mealy. Keep them at room temperature, stem-side down, and eat them within five days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana.

3. [p. 1] (relevance 0.04)
   Page 1 — Choosing varieties and spacing There are two main types of tomato plant. Determinate varieties, such as Roma, grow to a fixed height of about 90 centimetres and ripen most of their fruit within a few weeks. Indeterminate varieties, such as Sungold, keep growing all season and need tall stakes or a trellis. Space plants 60 to 90 centimetres apart (24 to 36 inches) so air can circulate between them. Crowded plants stay damp and invite disease. Plant seedlings deep: bury the stem up to the first true leaves and roots will form along the buried stem, giving a stronger plant.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

## Q: How long until tomatoes are ready to harvest?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 4] (relevance 0.31)
   Page 4 — Harvest and storage Most varieties take 60 to 80 days from transplanting to the first ripe fruit. Pick tomatoes when they are fully coloured but still firm; a ripe tomato comes away with a gentle twist. Harvest in the morning when the flavour is at its best. Never store tomatoes in the fridge: cold temperatures destroy their flavour compounds and turn the flesh mealy. Keep them at room temperature, stem-side down, and eat them within five days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana.

2. [p. 4] (relevance 0.10)
   days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana. One healthy plant yields roughly 4 to 7 kilograms of fruit over a season.

3. [p. 2] (relevance 0.05)
   Page 2 — Soil, feeding and watering Tomatoes grow best in soil with a pH between 6.0 and 6.8. Test your soil before planting and add lime to raise the pH or sulphur to lower it. Mix in two handfuls of compost per planting hole. Water deeply but infrequently: tomato plants need 2.5 to 5 centimetres (1 to 2 inches) of water per week, delivered at the base of the plant. Wet leaves spread disease, so never use an overhead sprinkler in the evening. A layer of straw mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the lower leaves.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

## Q: Should I store tomatoes in the fridge?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 4] (relevance 0.26)
   Page 4 — Harvest and storage Most varieties take 60 to 80 days from transplanting to the first ripe fruit. Pick tomatoes when they are fully coloured but still firm; a ripe tomato comes away with a gentle twist. Harvest in the morning when the flavour is at its best. Never store tomatoes in the fridge: cold temperatures destroy their flavour compounds and turn the flesh mealy. Keep them at room temperature, stem-side down, and eat them within five days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana.

2. [p. 4] (relevance 0.08)
   days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana. One healthy plant yields roughly 4 to 7 kilograms of fruit over a season.

3. [p. 2] (relevance 0.04)
   Page 2 — Soil, feeding and watering Tomatoes grow best in soil with a pH between 6.0 and 6.8. Test your soil before planting and add lime to raise the pH or sulphur to lower it. Mix in two handfuls of compost per planting hole. Water deeply but infrequently: tomato plants need 2.5 to 5 centimetres (1 to 2 inches) of water per week, delivered at the base of the plant. Wet leaves spread disease, so never use an overhead sprinkler in the evening. A layer of straw mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the lower leaves.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

## Q: How far apart should I space tomato plants?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 1] (relevance 0.25)
   Page 1 — Choosing varieties and spacing There are two main types of tomato plant. Determinate varieties, such as Roma, grow to a fixed height of about 90 centimetres and ripen most of their fruit within a few weeks. Indeterminate varieties, such as Sungold, keep growing all season and need tall stakes or a trellis. Space plants 60 to 90 centimetres apart (24 to 36 inches) so air can circulate between them. Crowded plants stay damp and invite disease. Plant seedlings deep: bury the stem up to the first true leaves and roots will form along the buried stem, giving a stronger plant.

2. [p. 2] (relevance 0.07)
   Page 2 — Soil, feeding and watering Tomatoes grow best in soil with a pH between 6.0 and 6.8. Test your soil before planting and add lime to raise the pH or sulphur to lower it. Mix in two handfuls of compost per planting hole. Water deeply but infrequently: tomato plants need 2.5 to 5 centimetres (1 to 2 inches) of water per week, delivered at the base of the plant. Wet leaves spread disease, so never use an overhead sprinkler in the evening. A layer of straw mulch 5 to 8 centimetres thick keeps the soil moist and stops soil splashing onto the lower leaves.

3. [p. 4] (relevance 0.03)
   Page 4 — Harvest and storage Most varieties take 60 to 80 days from transplanting to the first ripe fruit. Pick tomatoes when they are fully coloured but still firm; a ripe tomato comes away with a gentle twist. Harvest in the morning when the flavour is at its best. Never store tomatoes in the fridge: cold temperatures destroy their flavour compounds and turn the flesh mealy. Keep them at room temperature, stem-side down, and eat them within five days. Green tomatoes left at the end of the season will ripen indoors in a paper bag with a banana.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

## Determinism

Same question asked twice produces byte-identical output (verified with `diff`).
