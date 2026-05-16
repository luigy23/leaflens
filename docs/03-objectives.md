# 3. Objectives

## General objective

Design, train, and deploy an end-to-end web application that identifies common houseplants from photographs and returns species-specific care instructions and pet-safety information, using deep learning for classification and modern web technologies for delivery.

## Specific objectives

1. **Prepare a reproducible image classification dataset.**
   Acquire the Kaggle House Plant Species dataset (47 classes), perform a stratified 70/15/15 train/validation/test split with a fixed random seed, and persist the splits as CSV manifests so that any team member can recover the exact partitioning.

2. **Train and compare at least three classification architectures.**
   Apply transfer learning with EfficientNet-B0, ResNet-50, and ViT-Base to the prepared dataset. Track accuracy, F1-score (macro and weighted), confusion matrix, and inference latency for each. Select the best-performing model for deployment.

3. **Mitigate class imbalance.**
   Inspect the per-class distribution after splitting; apply class-weighted loss and image augmentation strategies (rotation, horizontal flip, color jitter) for minority classes.

4. **Build a care-information knowledge base.**
   Curate a structured database covering every species in the dataset, with normalized fields for watering interval, light level, temperature range, ideal humidity, fertilizer schedule, and toxicity to cats and dogs.

5. **Implement a Flask REST API.**
   Expose endpoints for image upload, prediction, and care-card lookup. Use PostgreSQL for the care knowledge base and SQLAlchemy as the ORM.

6. **Implement a React web frontend.**
   Provide a single-page experience: drag-and-drop or file picker upload, loading state, result card with species, confidence, top-three alternatives, and full care information.

7. **Deploy the application to the cloud.**
   Use a free-tier provider (Render, Railway, or HuggingFace Spaces) for the backend; Vercel or Netlify for the static frontend.

8. **Cover the system with automated tests.**
   Implement unit tests for data utilities, functional tests for the inference pipeline, and integration tests for the API endpoints.

9. **Document the project in English.**
   Produce the full set of sections required by the course rubric: introduction, problem, objectives, state of the art, requirements, use cases, ER model, class diagrams, GUI mockups, API catalog, testing, architecture, results, recommendations and future work.

## Success criteria

| Criterion | Target |
|---|---|
| Test set top-1 accuracy of the best model | ≥ 85% |
| Test set top-3 accuracy of the best model | ≥ 95% |
| API end-to-end latency (image upload → response) | < 3 seconds |
| Code coverage of automated tests | ≥ 70% |
| Documentation completeness | 14/14 sections produced |
| Working public deployment | One URL reachable from any browser |
