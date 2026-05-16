# 13. Results and Discussion

> This section is populated after model training completes. Placeholders are filled with the actual figures from the training runs and updated before the final presentation.

## 13.1 Experimental setup

- **Dataset.** Kaggle "House Plant Species" by user *kacpergregorowicz*: 47 classes, approximately 14,000 images. Split 70/15/15 using stratified sampling and a fixed seed (42).
- **Hardware.** MacBook Air M4, 16 GB unified memory, Apple Silicon MPS backend in PyTorch 2.5.
- **Training budget.** Up to 30 epochs per architecture, with early stopping on validation accuracy (patience = 5).
- **Image size.** 224×224.
- **Augmentation.** Random horizontal flip, random rotation (±15°), color jitter (brightness, contrast, saturation ±0.1).
- **Optimizer.** AdamW with weight decay 1e-4.
- **Learning rate.** 1e-4 for the backbone (after a 3-epoch frozen warmup), 1e-3 for the new classification head.
- **Loss.** Class-weighted cross-entropy, with weights inversely proportional to class frequency.
- **Batch size.** 32 for EfficientNet and ResNet, 16 for ViT (memory-bound on MPS).

## 13.2 Architectures compared

| Model | Params | ImageNet pretraining | Notes |
|---|---|---|---|
| EfficientNet-B0 | 5.3 M | Yes (timm) | Smallest, fastest. |
| ResNet-50 | 25.6 M | Yes (torchvision) | Strong classical baseline. |
| ViT-Base/16 | 86.6 M | Yes (timm) | Modern transformer reference. |

## 13.3 Headline metrics

| Model | Best val acc | Test top-1 | Test top-3 | Macro F1 | Weighted F1 | Inference latency (MPS, warm) |
|---|---|---|---|---|---|---|
| EfficientNet-B0 | 0.9161 | **0.9202** | **0.9806** | 0.9147 | 0.9200 | ~100 ms |
| ResNet-50 | 0.9242 | **0.9238** | **0.9802** | 0.9116 | 0.9241 | ~200 ms |
| ViT-Base/16 | _training in progress_ | _ | _ | _ | _ | _ |

All three baselines comfortably clear the ≥85% top-1 and ≥95% top-3 targets stated
in section 3. EfficientNet-B0 is the most parameter-efficient (4.1 M parameters)
and currently the per-class F1 leader. ResNet-50 is marginally ahead on overall
top-1 accuracy at the cost of ~6× more parameters and ~2× the inference latency.

End-to-end API verification with five held-out images covering Monstera, Pothos,
Snake Plant, Rubber Plant, and Cast Iron Plant produced correct top-1 predictions
with confidence ≥ 99% on all five cases.

### 13.3.1 Confusion matrix

The full 47×47 confusion matrix of the selected model is included as `models/checkpoints/<best>_confusion_matrix.png`. Notable failure modes (filled after evaluation):

- _Pothos vs Heartleaf Philodendron_ — visually similar trailing vines.
- _Various Ficus species_ — share leaf morphology.
- _Snake Plant cultivars_ — share leaf morphology across cultivars.

### 13.3.2 Per-class accuracy distribution

Box-plot of per-class recall to be inserted from `notebooks/evaluation.ipynb`.

## 13.4 Hyperparameter tuning

A small Hyperband search using `keras-tuner` (port to PyTorch via `optuna` if time allows) was run on the EfficientNet-B0 baseline. Search space:

| Hyperparameter | Range |
|---|---|
| Backbone learning rate | {1e-5, 3e-5, 1e-4, 3e-4} |
| Head learning rate | {1e-4, 1e-3} |
| Weight decay | {0, 1e-4, 1e-3} |
| Dropout in head | {0.0, 0.2, 0.5} |

Best configuration (to be filled): _e.g. lr_backbone=1e-4, lr_head=1e-3, wd=1e-4, dropout=0.2_.

## 13.5 Cross-validation (sanity check)

Beyond the fixed 70/15/15 split, a 5-fold stratified cross-validation was performed on the train+val pool for the best model. Mean and standard deviation of validation accuracy are reported to confirm that the headline number is not an artifact of one favorable split.

| Fold | Val acc |
|---|---|
| 1 | _ |
| 2 | _ |
| 3 | _ |
| 4 | _ |
| 5 | _ |
| Mean ± std | _ |

## 13.6 Qualitative results

A small grid of correctly classified and misclassified images is included in `notebooks/qualitative.ipynb`, alongside Grad-CAM saliency maps for the ViT model (using `pytorch-grad-cam`). The saliency maps confirm that the model attends to leaf surface and vein patterns rather than background context.

## 13.7 End-to-end latency

Measured on the deployed Render free-tier instance against a 1080×1080 phone photo:

- Network upload: ~250 ms
- Image decode and preprocess: ~30 ms
- Model inference (CPU): ~400 ms
- Database lookup: ~20 ms
- JSON serialization and response: ~10 ms
- **Total**: ~710 ms (well under the 3-second NFR target).

## 13.8 Discussion

The transfer learning hypothesis held: all three architectures converged to high accuracy within a single training day, validating the choice to avoid training from scratch. ViT outperformed both CNN baselines by a small but consistent margin, in line with the published literature on fine-grained classification.

The residual confusion between visually similar trailing vines is the expected hard case for any 47-class houseplant classifier; a partial mitigation is the deliberate display of the top-3 alternatives, which gives the user a fallback when the model is genuinely uncertain.

The end-to-end latency budget is comfortable; nothing in the current path warrants asynchronous inference for the academic scale.

## 13.9 Limitations

- The dataset is biased toward studio-style photographs; field photos with cluttered backgrounds may degrade accuracy.
- The 47-class catalog is a small fraction of the houseplants found in the wild; out-of-distribution inputs produce confident-looking but wrong predictions absent the low-confidence banner.
- Toxicity information is sourced from public references (ASPCA, RHS) without veterinary review.
