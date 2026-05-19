# 15. Presentation Outline (English)

Speaker: Luigy Leonardo · Course: Artificial Intelligence (BEINSOF52) · USCO 2026
Duration target: 10–12 minutes · Language: English

This outline is a slide-by-slide script. Build the actual deck in Keynote,
Google Slides, or PowerPoint after the final ViT results are in.

---

## Slide 1 — Title (15 s)

**LeafLens 🌿🔍**
AI-powered houseplant identification and care assistant.

Luigy Leonardo · Universidad Surcolombiana
Artificial Intelligence final project, May 2026
Instructor: Juan Antonio Castro Silva

> Opener: "Half of all houseplants bought every year die within twelve months.
> Not because owners don't care — because they don't know what they have.
> LeafLens is a one-photo fix for that."

---

## Slide 2 — The problem (45 s)

- 50%+ of indoor plants die within a year of purchase.
- Three failure modes: identification, lookup, translation to action.
- Pet owners: dozens of common houseplants are toxic to cats and dogs and
  most owners learn it the hard way.

> Visual: photo of a wilted store-bought plant + screenshot of confusing
> care-forum advice.

---

## Slide 3 — What LeafLens does (45 s)

Demo screenshot: phone photo → result card.

Three deliverables in one product:
1. **Identification** — top-1 species with confidence + top-3 alternatives.
2. **Care card** — watering, light, temperature, humidity, fertilizer.
3. **Pet safety badge** — toxic / mild / safe for cats and dogs.

End-to-end latency under one second on the live deployment.

---

## Slide 4 — Live demo (90 s)

Open the deployed URL. Upload three pre-staged photos in sequence:

1. **Pothos** (clean confident match) — show the care card.
2. **Snake plant** — point out the "toxic to pets" badge.
3. **Out-of-distribution** photo (a flower or random object) — show the
   low-confidence banner and top-3 fallback.

> Speaking tip: keep narration tight; let the result cards speak.

---

## Slide 5 — Dataset (30 s)

- **Kaggle "House Plant Species"** by *kacpergregorowicz* (2024 release).
- 47 classes covering the most common indoor plants worldwide.
- 14,774 labelled images.
- Stratified 70 / 15 / 10 / 15 (train / val / test) with a fixed seed.
- Class distribution shown on a horizontal bar chart — the data is mildly
  imbalanced (Yucca ≈ 66 images, Anthurium ≈ 454).

---

## Slide 6 — Architectures compared (60 s)

Three transfer-learning baselines, all pretrained on ImageNet, with their
classification heads replaced by a 47-way linear layer.

| Architecture | Params | Why we picked it |
|---|---|---|
| EfficientNet-B0 | 4.1 M | Lightweight CNN, fastest inference. |
| ResNet-50 | 23.6 M | Strong classical baseline. |
| ViT-Base/16 | 85.8 M | Modern transformer reference. |

Training recipe: 3-epoch frozen-backbone warm-up, then differential learning
rates (1e-4 backbone, 1e-3 head), AdamW + weight decay, class-weighted
cross-entropy, early stopping on validation accuracy.

---

## Slide 7 — Results (60 s)

Headline metrics on the held-out test set:

| Model | Top-1 | Top-3 | Macro F1 | Weighted F1 | Latency (warm) |
|---|---|---|---|---|---|
| EfficientNet-B0 | 92.02% | 98.06% | 0.9147 | 0.9200 | ~100 ms |
| ResNet-50       | 92.38% | 98.02% | 0.9116 | 0.9241 | ~200 ms |
| ViT-Base/16     | _filled after training_ | _ | _ | _ | _ |

Both targets from section 3 met:
- ≥ 85% top-1 ✅
- ≥ 95% top-3 ✅

Selected for deployment: **{best model name}**.

---

## Slide 8 — Where the model still fails (45 s)

Confusion matrix highlights (insert image):
- Snake Plant vs Cast Iron Plant — similar dark strap-shaped leaves.
- Various trailing Araceae (Pothos vs Philodendron) — same family habit.
- Begonia subspecies — hard even for botanists from a single photo.

Mitigation: deliberately surface the top-3 alternatives and a clear
"low confidence" banner below 40 % top-1.

---

## Slide 9 — System architecture (60 s)

(Insert architecture diagram from docs/12-architecture.md.)

- React + Vite frontend on Vercel.
- Flask + gunicorn backend on Render free tier.
- PostgreSQL managed on Render — holds the curated 47-species catalog
  (47 care profiles + 94 toxicity records).
- PyTorch inference runs on the same backend process (no separate GPU node
  required for the academic scale).

---

## Slide 10 — Documentation and engineering practices (45 s)

- Repository: 79+ files, 14-section English documentation set.
- Tests: unit, functional, integration (pytest + pytest-flask).
- CI: GitHub Actions runs lint + tests on every push.
- Reproducibility: train/val/test splits stored as CSV manifests with a
  fixed seed (42). Anyone can re-run and get the same numbers.
- Cleanup script: `scripts/cleanup.sh --hard` removes the entire workspace
  after grading.

---

## Slide 11 — Future work (30 s)

- Expand catalog to 100+ species via curated PlantNet-300K subset.
- Export the model to CoreML for on-device inference (no server cost,
  no upload latency, full privacy).
- Plant disease overlay using PlantVillage.
- Push reminders for watering and fertilizing.

---

## Slide 12 — Thanks + Q&A (15 s)

- Live demo URL: https://leaflens.vercel.app (replace after deploy)
- Code: https://github.com/luigy23/leaflens
- Questions?

> Closing line: "If you've ever killed a plant by loving it too much,
> LeafLens is for you. Thank you."

---

## Speaker notes — common questions to prepare for

1. **Why three architectures and not one?**
   Rubric requirement, but also good practice: a CNN and a transformer make
   different mistakes; comparing them gives a defensible model selection.

2. **Why not train from scratch?**
   ImageNet-pretrained backbones converge to greater than 90% in a single
   training day on this dataset; from scratch would have wasted the
   one-week budget for no measurable accuracy gain.

3. **How do you handle class imbalance?**
   Class-weighted cross-entropy loss with weights inversely proportional
   to class frequency, plus data augmentation (rotation, flip, color
   jitter). Confirmed by per-class F1 staying close to overall F1.

4. **What about pets — is the toxicity data reliable?**
   Curated from ASPCA's toxic plant database (the standard reference for
   US-based vets) cross-checked with the RHS plant finder. The UI
   explicitly states that this is informational, not a vet substitute.

5. **Why no IoT layer?**
   The instructor confirmed IoT was a suggestion, not a hard requirement
   for this specific project track. The deliverable focuses on the
   computer vision + software engineering scope.

6. **Why English documentation if you're a Spanish speaker?**
   The rubric requires English documentation and presentation. The codebase
   itself follows international conventions to make collaboration with
   future maintainers easier.

7. **How are uploaded images handled?**
   Decoded into memory, run through the model, discarded. No server-side
   persistence. Only the prediction outcome (species id, confidence,
   latency) is stored — for analytics, not for retrieval.
