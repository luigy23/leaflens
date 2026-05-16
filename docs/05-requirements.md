# 5. Requirements

## 5.1 Functional requirements

| ID | Title | Description | Priority |
|---|---|---|---|
| FR-01 | Image upload | The user can upload an image of a plant from their device through a drag-and-drop area or a file picker. Accepted formats: JPEG, PNG, WebP. Maximum size: 10 MB. | High |
| FR-02 | Species prediction | The system returns the top-1 predicted species with a confidence score expressed as a percentage. | High |
| FR-03 | Top-k alternatives | The system additionally returns the second and third most likely species. | High |
| FR-04 | Care card | For the predicted species the system displays watering interval, light requirement, temperature range, ideal humidity, fertilization schedule. | High |
| FR-05 | Pet safety indicator | The system displays whether the species is toxic to cats, dogs, or both. | High |
| FR-06 | Low-confidence handling | If the top-1 confidence is below 40%, the system shows a "low confidence" warning and asks for a clearer photo. | Medium |
| FR-07 | Image validation | The system rejects images that are too small (below 224×224 pixels) or that fail a quick blur check. | Medium |
| FR-08 | History (local) | The browser stores the last ten predictions in local storage for quick re-access. | Low |
| FR-09 | Catalog browsing | The user can browse the full catalog of 47 species without uploading a photo, to learn about plants by name. | Low |
| FR-10 | About page | A static page explains how the model works and lists the dataset and model architectures. | Low |

## 5.2 Non-functional requirements

| ID | Title | Description | Priority |
|---|---|---|---|
| NFR-01 | End-to-end latency | Total time from image upload click to result displayed: < 3 seconds on a 10 Mbps connection. | High |
| NFR-02 | Model accuracy | Test-set top-1 accuracy of the deployed model: ≥ 85%. | High |
| NFR-03 | Availability | The public deployment is reachable at least 95% of the time during the academic evaluation period. | High |
| NFR-04 | Browser support | The frontend works on the last two stable versions of Chrome, Safari, Firefox, and Edge. | High |
| NFR-05 | Mobile responsiveness | The interface adapts to viewport widths from 320 pixels upward. | High |
| NFR-06 | Security | The image upload endpoint validates content type and size before invoking the model. No secrets are committed to the repository. | High |
| NFR-07 | Privacy | Uploaded images are not persisted server-side after inference completes. | High |
| NFR-08 | Language | All user-facing copy, API responses, and documentation are in English. | High |
| NFR-09 | Reproducibility | Train/validation/test splits, random seeds, and hyperparameters are versioned in the repository. | Medium |
| NFR-10 | Test coverage | Automated tests cover at least 70% of backend code. | Medium |
| NFR-11 | Code quality | Python code passes `ruff check` and is formatted with `black`. JS/TS code is formatted with `prettier`. | Medium |
| NFR-12 | Disk footprint | The full local development environment (deps + dataset + checkpoints) fits in < 25 GB. | Medium |

## 5.3 Constraints

- **Single developer**, one-week budget.
- **Apple Silicon laptop** with 16 GB unified memory and no NVIDIA GPU. PyTorch must use the MPS backend.
- **No paid cloud services**: free tiers only (Render, Railway, Vercel, Netlify, HuggingFace Spaces).
- **No proprietary datasets**: every data source is publicly available.

## 5.4 Assumptions

- Users provide one plant per photo, with the plant occupying most of the frame.
- Users have a modern browser and a stable internet connection.
- The Kaggle dataset's class boundaries are correct (we trust the original annotators).
