# 17. Presentation Cheat Sheet — Numbers, Paths, and Q&A Reference

Print this sheet (or keep it open on your phone) during the presentation.
Everything a professor or peer might ask, in one page.

---

## 🌱 The headline numbers

| Question | Answer |
|---|---|
| Best test top-1 accuracy | **92.38%** (ResNet-50) |
| Best test top-3 accuracy | **98.06%** (EfficientNet-B0) |
| Number of species | **47** |
| Number of training images | **10,341** |
| Number of validation images | **2,216** |
| Number of test images | **2,217** |
| Total dataset size | **14,774 images, 4.85 GB** |
| Number of architectures compared | **3** (EfficientNet-B0, ResNet-50, ViT-Base) |
| Inference latency (warm, MPS) | **~200 ms** (ResNet-50) |
| API end-to-end latency target | **< 3 s** (NFR-01) — actual ~1.2 s cold |

---

## 📂 Local paths (your laptop)

| Resource | Path |
|---|---|
| Repository root | `~/Documents/GitHub/leaflens` |
| GitHub remote | `https://github.com/luigy23/leaflens` |
| Python venv | `~/Documents/GitHub/leaflens/.venv` |
| Dataset (Kaggle cache) | `~/.cache/kagglehub/datasets/kacpergregorowicz/house-plant-species/versions/4/house_plant_species/` |
| Dataset symlink in repo | `data/raw/house_plant_species` → above |
| Train manifest | `data/processed/train.csv` (10,341 rows) |
| Validation manifest | `data/processed/val.csv` (2,216 rows) |
| Test manifest | `data/processed/test.csv` (2,217 rows) |
| Class distribution report | `data/processed/class_distribution.csv` |
| Curated species catalog | `backend/data/species.yaml` (47 entries) |
| Local SQLite database | `backend/leaflens.db` (gitignored) |
| Trained checkpoints | `models/checkpoints/{efficientnet,resnet50,vit}_best.pt` |
| Deployed checkpoint | `models/checkpoints/best.pt` (copy of resnet50_best.pt) |
| Evaluation reports | `models/checkpoints/*_best.eval.json` |
| Training histories | `models/checkpoints/*_history.json` |
| Backend log | `/tmp/leaflens_backend.log` |
| Frontend log | `/tmp/leaflens_frontend.log` |
| ViT training log | `/tmp/leaflens_train_vit.log` |

---

## 🌐 URLs

| Service | URL |
|---|---|
| Source code (public) | https://github.com/luigy23/leaflens |
| Backend (local dev) | http://localhost:5001/api/health |
| Frontend (local dev) | http://localhost:5173 |
| Backend (production) | _set after Render deploy_ |
| Frontend (production) | _set after Vercel deploy_ |
| Kaggle dataset | https://www.kaggle.com/datasets/kacpergregorowicz/house-plant-species |
| ASPCA toxicity reference | https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants |
| RHS plant finder | https://www.rhs.org.uk/plants/search-form |

---

## 🧠 Architecture details (in case they grill you)

### EfficientNet-B0
- **Source**: `timm.create_model('efficientnet_b0', pretrained=True)`
- **Params**: 4.1 M total, 60 K trainable in the frozen phase
- **ImageNet top-1**: 77.7%

### ResNet-50 (deployed)
- **Source**: `torchvision.models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)`
- **Params**: 23.6 M total, 96 K trainable in the frozen phase
- **ImageNet top-1**: 80.9% (V2 weights)

### ViT-Base/16
- **Source**: `timm.create_model('vit_base_patch16_224', pretrained=True)`
- **Params**: 85.8 M total, 36 K trainable in the frozen phase
- **ImageNet top-1**: 81.0%
- **Why it lost on our dataset**: 14k images / 47 classes is below ViT's data-hungry sweet spot. CNNs with strong inductive biases win in the small-data regime.

---

## ⚙️ Training recipe (identical for all 3 architectures)

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Weight decay | 1e-4 |
| Learning rate (backbone) | 1e-4 (after warm-up) |
| Learning rate (head) | 1e-3 |
| Backbone freeze epochs | 3 |
| Total epochs (cap) | 15 (12 for ViT) |
| Early stopping patience | 5 epochs |
| Loss function | Class-weighted cross-entropy |
| Image size | 224 × 224 |
| Batch size | 32 (16 for ViT, memory-bound on MPS) |
| Augmentation | RandomResizedCrop, HorizontalFlip, Rotation(±15°), ColorJitter(0.1) |
| Train/val/test split | 70 / 15 / 15, stratified |
| Random seed | 42 |
| Device | Apple MPS (M4 Air, 16 GB) |

---

## 🩺 Care card data sources

The catalog at `backend/data/species.yaml` was hand-curated from:

- **ASPCA Animal Poison Control Center** — toxicity data (the standard US veterinary reference)
- **Royal Horticultural Society (RHS) plant finder** — care requirements
- **Missouri Botanical Garden plant finder** — family, origin, descriptions
- **Pl@ntNet** — scientific name disambiguation

Each of the 47 species has:
- 1 care profile (watering, light, temp, humidity, fertilizer)
- 2 toxicity records (cat + dog)
- 34 species are pet-safe, 7 mildly toxic, 53 toxic out of 94 total records

---

## ❓ Likely questions and crisp answers

**Q: Why three models?**
Rubric requires ≥3 for the "best practices" section. Also: a CNN and a transformer make different mistakes; comparing them validates the model choice.

**Q: Why didn't ViT win? It's supposed to.**
ViT's advantage emerges with millions of images. With 14k images and 47 classes, ImageNet-pretrained CNNs have a stronger inductive bias and converge faster. Documented in Section 13.8.

**Q: Why did you stop ViT early at epoch 3?**
Its trajectory was 3 percentage points behind ResNet-50 with shrinking gap-closing room. Continuing 9 more epochs would have cost ~2 GPU-hours of laptop time with no expected ranking change. Disclosed transparently in Section 13.3.

**Q: How do you handle class imbalance?**
Two mechanisms: (1) class-weighted cross-entropy loss with weights inversely proportional to class frequency, and (2) data augmentation. Confirmed by per-class F1 staying close to weighted F1.

**Q: How big is the model in production?**
The ResNet-50 checkpoint is 90 MB. Fits comfortably in Render's free-tier container image.

**Q: What happens if I upload a photo of a dog or a car?**
The model still returns a top-1 prediction (it has no "unknown" class), but the confidence will be low (< 40%), which triggers the explicit "low confidence — try a better photo" UI banner instead of the result card.

**Q: Is the toxicity info trustworthy?**
Sourced from ASPCA, the standard veterinary reference. The UI explicitly says it's informational, not a vet substitute. Section 5.2 lists this in non-functional requirements.

**Q: Did you train from scratch?**
No — all three models use ImageNet pretrained weights and were fine-tuned with a frozen-backbone warm-up followed by differential learning rates. Standard transfer learning. Training from scratch would have cost weeks and lost accuracy.

**Q: How is the dataset split deterministic?**
`scripts/split_data.py` uses `sklearn.train_test_split` with `random_state=42` and `stratify=labels`. The resulting CSV manifests are gitignored only because they reference local file paths — the seed and the script are version-controlled.

**Q: Why no IoT?**
The course rubric lists IoT as worth 10% but the instructor confirmed it was a suggestion for the agriculture track. Our project track focuses on computer vision + software engineering scope.

**Q: What's the deployment pipeline?**
Push to `main` → GitHub Actions runs lint + tests → Render auto-deploys backend (Docker) → Vercel auto-deploys frontend. Zero manual steps after the initial setup.

**Q: Can the model handle multiple plants in one photo?**
No — it's a classifier, not a detector. Out of scope for this project; future-work item.

**Q: Are uploaded photos stored?**
No. Section 7.3 / NFR-07. Only the prediction outcome (species id, confidence, latency) is logged for analytics.

---

## 🎤 Demo flow (for the live demo slide)

1. Open http://localhost:5173 (or production URL)
2. Drop in **Pothos** photo → show 99% confidence, point at the toxic-to-pets badge
3. Drop in **Snake Plant** photo → show different care card (water every 14–28 days)
4. Drop in **out-of-distribution** photo (a flower, anything random) → show the low-confidence banner
5. Click **Catalog** → show the 47-species grid
6. Click a species → show the detail page
