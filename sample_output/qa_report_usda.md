# USDA canning guide — real Q&A verification report

Sample document: *USDA Complete Guide to Home Canning, Guide 1: Principles of Home Canning*
(Agriculture Information Bulletin No. 539, revised 2015) — a publication of the
United States Department of Agriculture, downloaded 2026-11-20 from the National
Center for Home Food Preservation (University of Georgia), the official publisher
of the electronic edition:

https://nchfp.uga.edu/papers/guide/GUIDE01_HomeCan_rev0715.pdf

The PDF itself is **not in this repo** (binary, gitignored — see `sample_data/`):
download it from the URL above, then run the commands below. Index: 40 pages,
188 chunks, TF-IDF backend. Each question was run with:

```
python -m localpdfai ask --pdf sample_data/usda-canning-guide-1.pdf --q "..."
```

Top-1 citation correct on **6/6** questions below (the answer is in the quoted
top passage, hand-checked against the PDF text). The same question asked twice
returns byte-identical output.

## Q: What pH makes a food low-acid?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 8] (relevance 0.29)
   dly when heated. The term “pH” is a measure of acidity; the lower its value, the more acid the food. The acidity level in foods can be increased by adding lemon juice, citric acid, or vinegar. Low-acid foods have pH values higher than 4.6. They include red meats, seafood, poultry, milk, and all fresh vegetables except for most tomatoes. Most mixtures of low-acid and acid foods also have pH values above 4.6 unless their recipes include enough lemon juice, citric acid, or vinegar to make them acid foods. Acid foods have a pH of 4.6 or lower.

2. [p. 35] (relevance 0.27)
   st heat-resistant pathogenic or disease-causing microorganism known to be associated with that food. pH A measure of acidity or alkalinity. Values range from 0 to 14. A food is neutral when its pH is 7.0, lower values are increasingly more acid; higher values are increasingly more alkaline. Pickling The practice of adding enough vinegar or lemon juice to a low-acid food to lower its pH to 4.6 or lower. Properly pickled foods may be safely heat processed in boiling water. Pressure Canner A specifically designed metal kettle with a lockable lid used for heat processing low-acid food.

3. [p. 8] (relevance 0.25)
   lemon juice, citric acid, or vinegar to make them acid foods. Acid foods have a pH of 4.6 or lower. They include fruits, pickles, sauerkraut, jams, jellies, marmalades, and fruit butters. Although tomatoes usually are considered an acid food, some are now known to have pH values slightly above 4.6. Figs also have pH values slightly above 4.6. Therefore, if they are to be canned as acid foods, these products must be acidified to a pH of 4.6 or lower with lemon juice or citric acid. Properly acidified tomatoes and figs are acid foods and can be safely processed in a boiling-water canner.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

Expected answer (hand-checked): Low-acid foods have pH values higher than 4.6.

## Q: What temperature is needed to destroy bacteria in low-acid canned food?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 8] (relevance 0.38)
   e as measured by gauge. The more familiar “PSI” desig- nation is used hereafter in this publication. At temperatures of 240° to 250°F, the time needed to destroy bacteria in low-acid canned food ranges from 20 to 100 minutes. The exact time depends on the kind of food being canned, the way it is packed into jars, and the size of jars. The time needed to safely process low-acid foods in a boiling-water canner ranges from 7 to 11 hours; the time needed to process acid foods in boiling water varies from 5 to 85 minutes.

2. [p. 8] (relevance 0.31)
   1-8 Food acidity and processing methods Whether food should be processed in a pressure canner or boiling-water canner to control botulinum bacteria depends on the acidity of the food. Acidity may be natural, as in most fruits, or added, as in pickled food. Low-acid canned foods are not acidic enough to prevent the growth of these bacteria. Acid foods contain enough acid to block their growth, or destroy them more rapidly when heated. The term “pH” is a measure of acidity; the lower its value, the more acid the food.

3. [p. 22] (relevance 0.28)
   en the jars during cooling. Let jars sit undisturbed to cool at room temperature for 12 to 24 hours. Selecting the correct processing time When canning in boiling water, more processing time is needed for most raw-packed foods and for quart jars than is needed for hot-packed foods and pint jars. To destroy microorganisms in acid foods processed in a boiling-water canner, you must: • Process jars for the correct number of minutes in boiling water. • Cool the jars at room temperature.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

Expected answer (hand-checked): At 240 to 250 F, the time needed to destroy bacteria in low-acid canned food is 20 to 100 minutes.

## Q: How long should jars sit undisturbed to cool at room temperature?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 22] (relevance 0.44)
   en the jars during cooling. Let jars sit undisturbed to cool at room temperature for 12 to 24 hours. Selecting the correct processing time When canning in boiling water, more processing time is needed for most raw-packed foods and for quart jars than is needed for hot-packed foods and pint jars. To destroy microorganisms in acid foods processed in a boiling-water canner, you must: • Process jars for the correct number of minutes in boiling water. • Cool the jars at room temperature.

2. [p. 18] (relevance 0.37)
   ommended time, turn off the heat and remove the canner lid. Wait 5 minutes before removing jars. 10. Using a jar lifter, remove the jars and place them on a towel, leaving at least 1-inch spaces between the jars during cooling. Let jars sit undisturbed to cool at room temperature for 12 to 24 hours.

3. [p. 22] (relevance 0.31)
   ion. 7. After the canner is depressurized, remove the weight from the vent port or open the petcock. Wait 10 minutes, unfasten the lid, and remove it carefully. Lift the lid away from you so that the steam does not burn your face. 8. Remove jars with a jar lifter, and place them on a towel, leaving at least 1-inch spaces between the jars during cooling. Let jars sit undisturbed to cool at room temperature for 12 to 24 hours.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

Expected answer (hand-checked): Let jars sit undisturbed to cool at room temperature for 12 to 24 hours.

## Q: How do you test jar seals after cooling?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 25] (relevance 0.29)
   quid during processing, do not open it to add more liquid. Check for sealed lids as described below. Testing jar seals After cooling jars for 12 to 24 hours, remove the screw bands and test seals with one of the following options: Option 1. Press the middle of the lid with a finger or thumb. If the lid springs up when you release your finger, the lid is unsealed. Option 2. Tap the lid with the bottom of a teaspoon. If it makes a dull sound, the lid is not sealed. If food is in contact with the underside of the lid, it will also cause a dull sound.

2. [p. 3] (relevance 0.24)
   rmining proper process time .......................................................1-23 Cooling jars ........................................................................................................................................................................1-25 Testing jar seals ................................................................................................................................................................1-25 Reprocessing unsealed jars .........................................................................................................................................1-26 Storing canned food

3. [p. 25] (relevance 0.17)
   Principles of Home Canning 1 1-25 Cooling jars When you remove hot jars from a canner, do not retighten their jar lids. Retightening of hot lids may cut through the gasket and cause seal failures. Cool the jars at room temperature for 12 to 24 hours. Jars may be cooled on racks or towels to minimize heat damage to counters. The food level and liquid volume of raw-packed jars will be noticeably lower after cooling. Air is exhausted during processing and food shrinks. If a jar loses excessive liquid during processing, do not open it to add more liquid. Check for sealed lids as described below.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

Expected answer (hand-checked): Press the middle of the lid; if it springs up it is unsealed. Tap with a teaspoon; a dull sound means unsealed.

## Q: What causes botulism in canned food?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 33] (relevance 0.14)
   idded kettle with jar rack, designed for heat- processing 7 quarts or 8 to 9 pints in boiling water. Botulism An illness caused by eating toxin produced by growth of Clostridium botulinum bacteria in moist, low-acid food, containing less than 2 percent oxygen, and stored between 40° and 120°F. Proper heat processing destroys this bacterium in canned food. Freezer temperatures inhibit its growth in frozen food. Low moisture controls its growth in dried food. High oxygen controls its growth in fresh foods.

2. [p. 34] (relevance 0.13)
   1-34 Enzymes Proteins in food which accelerate many flavor, color, texture, and nutritional changes, especially when food is cut, sliced, crushed, bruised, and exposed to air. Proper blanching or hot-packing practices destroy enzymes and improve food quality. Exhausting Removal of air from within and around food and from jars and canners. Blanching exhausts air from live food tissues. Exhausting or venting of pressure canners is necessary to prevent a risk of botulism in low-acid canned foods. Fermentation Changes in food caused by intentional growth of bacteria, yeast, or mold.

3. [p. 28] (relevance 0.13)
   1-28 Be sure to remove and discard a 1/16-inch slice from the blossom end of fresh cucumbers. Blos- soms may contain an enzyme which causes excessive softening of pickles. Caution: The level of acidity in a pickled product is as important to its safety as it is to taste and texture. • Do not alter vinegar, food, or water proportions in a recipe or use a vinegar with unknown acidity. • Use only recipes with tested proportions of ingredients. • There must be a minimum, uniform level of acid throughout the mixed product to prevent the growth of botulinum bacteria.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

Expected answer (hand-checked): Toxin produced by growth of Clostridium botulinum bacteria in moist, low-acid food.

## Q: What is the correct headspace for low-acid foods in a pressure canner?

```
Answer (extractive):

Based on the document, here are the most relevant passages:

1. [p. 13] (relevance 0.26)
   Principles of Home Canning 1 1-13 Controlling headspace The unfilled space above the food in a jar and below its lid is termed headspace. Directions for canning specify leaving 1/4-inch for jams and jellies, 1/2-inch for fruits and tomatoes to be processed in boiling water, and from 1- to 1-1/4-inches in low acid foods to be processed in a pressure canner. This space is needed for expansion of food as jars are processed, and for forming vacuums in cooled jars. The extent of expansion is determined by the air content in the food and by the processing temperature.

2. [p. 23] (relevance 0.25)
   Principles of Home Canning 1 1-23 To destroy microorganisms in low-acid foods processed with a pressure canner, you must: • Process the jars using the correct time and pressure specified for your altitude. • Allow canner to cool at room temperature until it is completely depressurized. The food may spoil if you fail to select the proper process times for specific altitudes, fail to exhaust canners properly, process at lower pressure than specified, process for fewer minutes than specified, or cool the canner with water.

3. [p. 8] (relevance 0.21)
   1-8 Food acidity and processing methods Whether food should be processed in a pressure canner or boiling-water canner to control botulinum bacteria depends on the acidity of the food. Acidity may be natural, as in most fruits, or added, as in pickled food. Low-acid canned foods are not acidic enough to prevent the growth of these bacteria. Acid foods contain enough acid to block their growth, or destroy them more rapidly when heated. The term “pH” is a measure of acidity; the lower its value, the more acid the food.

This is an extractive answer: it quotes the document directly instead of rephrasing it, so nothing is invented.
```

Expected answer (hand-checked): 1 to 1-1/4 inches for low-acid foods in a pressure canner.

## Where it misses (honest note)

TF-IDF matches words, not meaning — the README's limitation section says so.
Two questions phrased far from the guide's wording missed on top-1:
"What is headspace?" lands on the contents page (p. 3) instead of the
definition (p. 13, second result), and "How should canned jars be stored?"
lands on a passage about screw bands (p. 16) — the storage guidance
(pp. 5, 25) is not even in the top 3. Asking in the guide's own words —
as above — fixes the first; the second is a genuine miss. The `--backend st`
option exists for paraphrase-heavy questions.
