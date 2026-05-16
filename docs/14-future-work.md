# 14. Recommendations and Future Work

## 14.1 Recommendations

### For users
- Capture the entire plant including the pot when possible. Closeups of a single leaf perform worse on fine-grained discrimination between visually similar species.
- Prefer natural daylight. Hard backlight and saturated artificial light shift colors enough to bias the model.
- When the application reports low confidence, take a second photo from a different angle before accepting the alternative candidates.

### For operators
- Monitor the `predictions` table for the share of low-confidence outcomes. A sustained increase usually points either to dataset drift (a new common houseplant entered the market) or to a regression in the preprocessing pipeline.
- Re-train every six months. New cultivars appear on the market continuously; six months is a sane refresh cadence at this scale.

### For maintainers
- Keep the 70/15/15 split frozen across model releases. A reshuffle invalidates direct comparison with prior reported metrics.
- Track inference latency in production. The free-tier instance can slip silently when CPU credits are exhausted.

## 14.2 Future work

### Short term (one to three months)

- **Expand the catalog.** Combine the Kaggle base with curated subsets of PlantNet-300K to cover the long tail of less common houseplants. Target 100 species.
- **On-device inference.** Export the best checkpoint to ONNX and CoreML so that the prediction can run locally in a mobile browser via WebNN or in a native iOS shell. This eliminates the upload latency and the privacy footprint entirely.
- **Plant disease overlay.** Train a second classifier on PlantVillage to flag visible disease symptoms (powdery mildew, leaf spot) on top of the species identification.
- **Multi-image input.** Allow the user to upload two or three photos of the same plant; combine predictions with a small ensembling rule to reduce confusion on visually similar species.

### Medium term (three to twelve months)

- **Care timeline.** Move beyond a static care card to a live schedule: push reminders to water, fertilize, and re-pot, with simple per-plant tracking.
- **Pest and disease diagnosis.** A dedicated CNN that takes a closeup of a damaged area and returns a likely cause and treatment.
- **Community-contributed photos.** A feedback loop where signed-in users can confirm or correct identifications, growing a high-quality labeled corpus over time.
- **Federated learning.** Train per-region models without centralizing user photos, using federated averaging across opt-in mobile clients.

### Long term (one year or more)

- **Multi-modal interface.** Accept text descriptions ("trailing vine with heart-shaped variegated leaves") alongside images, combining a CLIP-style image encoder with a text encoder.
- **Augmented reality care.** Detect the plant in the live camera feed and overlay care reminders contextually (point your phone at your pothos, see when it was last watered).
- **Voice assistant integration.** Expose the API to Alexa and Google Home so users can ask "Hey Google, what kind of plant is on my desk?" with a paired smart camera.

## 14.3 Lessons learned

- **Reproducibility is cheap if you start with it.** Saving the train/val/test split as CSV manifests on day one removed an entire class of "why does my number not match yours" debugging later.
- **Transfer learning is the right default.** Training from scratch on 14,000 images would have been a poor use of the one-week budget. Fine-tuning a pretrained backbone reached usable accuracy by day three.
- **Documentation as you go.** Writing the docs alongside the implementation, rather than in a frantic final two days, produced a much more coherent narrative — and surfaced design ambiguities while there was still time to fix them.
- **Free tiers are sufficient.** The full deployment lives within free-tier limits on Render and Vercel. Cloud cost is not a meaningful constraint for academic projects at this scale.
