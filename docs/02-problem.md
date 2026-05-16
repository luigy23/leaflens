# 2. Problem Statement

## The pain point

Houseplant owners frequently kill their plants by giving them the wrong care. Surveys conducted by the Royal Horticultural Society and large retail chains (Home Depot, IKEA) consistently report that more than half of indoor plants purchased die within twelve months of leaving the store. The leading causes are overwatering, underwatering, and incorrect light exposure — three failure modes that depend entirely on species-specific tolerances.

The friction lies in three steps the average owner cannot complete reliably:

1. **Identification.** The plant arrived without a label, was inherited, or carries a generic store tag ("tropical plant"). The owner does not know its botanical name.
2. **Lookup.** Even when identified, gardening references are dense, fragmented across blogs and forums, and contradict each other.
3. **Translation to action.** Knowing that a plant "prefers bright indirect light" does not translate easily into "place it 50 cm from a north-facing window."

The result is wasted money, dead plants, and the recurring disappointment that pushes many casual owners out of the hobby.

## Secondary problem: pet safety

A subset of common houseplants is toxic to cats and dogs (e.g. *Dieffenbachia*, *Spathiphyllum*, *Philodendron*). Pet owners frequently discover this only after their animal has ingested foliage. A reliable identifier paired with a toxicity database closes this gap.

## What is needed

A tool that takes a single photograph as input and returns:

- A confident species identification (with calibrated confidence)
- Care instructions in plain, actionable language
- Pet-safety information

The tool must be:

- **Accessible**: available on a normal web browser, no app store install
- **Fast**: total response time under three seconds on a phone camera image
- **Trustworthy**: confidence shown explicitly; never silently guesses when uncertain

## Why this is a good fit for artificial intelligence

Image-based plant identification is a textbook supervised classification problem with mature techniques (convolutional networks, vision transformers) and large public datasets (Kaggle's House Plant Species, PlantNet-300K, iNaturalist). It is not a problem that yields well to handcrafted rules — leaf shape, color, vein pattern, and stem morphology interact in ways that defeat traditional feature engineering. Deep learning models with transfer learning consistently outperform classical approaches by wide margins on these datasets, and modern pretrained backbones converge to usable accuracy with modest fine-tuning effort.

## Out of scope

This project does **not** attempt to:

- Diagnose pests or diseases (this is its own classification problem with separate datasets, and would require many more classes)
- Replace a botanist for rare or edge species (the model is limited to the 47 most common houseplants present in the chosen dataset)
- Provide commercial-grade pet safety advice (the toxicity table is informative, not a substitute for veterinary consultation)
