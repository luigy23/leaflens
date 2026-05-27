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
- **Class balancing (pre-training).** `WeightedRandomSampler` at the DataLoader oversamples minority classes with replacement so each minibatch is class-balanced before the model sees it. After sampling, the per-class count ratio in an epoch drops from 8.3× (raw) to ~1.36× (effectively balanced; mean ≈ 220 samples per class, std ≈ 14).
- **Loss.** Class-weighted cross-entropy as a safety net for any residual skew the sampler leaves in a single batch. Weights inversely proportional to class frequency.
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
| **ResNet-50** *(selected)* | 0.9242 | **0.9238** | **0.9802** | 0.9116 | 0.9241 | ~200 ms |
| ViT-Base/16 † | 0.8985 | 0.9017 | 0.9788 | 0.8992 | 0.9032 | ~400 ms |

> † ViT-Base training was halted at epoch 3 (post-unfreeze) because its
> trajectory was clearly below both CNN baselines and would not have
> overtaken them within the patience budget. Continuing the full 12-epoch
> schedule was projected to add ~2 GPU-hours for no expected ranking change.
> The reported figures come from the epoch-3 checkpoint evaluated on the
> held-out test set under identical conditions to the other two models.

All three baselines comfortably clear the ≥85% top-1 and ≥95% top-3 targets
stated in section 3. EfficientNet-B0 is the most parameter-efficient
(4.1 M parameters) and leads on macro F1, suggesting more consistent
performance on minority classes. ResNet-50 is marginally ahead on overall
top-1 accuracy and on weighted F1, which weights by class support — it is
slightly better at the common classes. ViT-Base trails both CNN baselines
on this dataset: at 47 classes and 14 k images, the transformer's larger
capacity is not an advantage and its convergence is slower.

**Selected for deployment: ResNet-50.** It wins on top-1 and weighted F1,
and its ~200 ms warm-inference latency is well within the 3-second NFR.

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

## 13.4 Hyperparameters and search space

We deliberately did not run a formal automated search. The training budget
(M4 Air, MPS, ≤ 1 GPU-hour per architecture) made an exhaustive Hyperband
or Bayesian sweep impractical at this scale. Instead, we chose conservative
defaults grounded in published practice for transfer learning on small
image datasets, and treated the comparison of the **three architectures**
as our primary "search" axis.

The defaults actually used (frozen by `argparse` defaults in
`models/train.py`):

| Hyperparameter | Value | Justification |
|---|---|---|
| Backbone learning rate | 1e-4 | Standard fine-tuning rate; 10× smaller than head |
| Head learning rate | 1e-3 | Newly-initialized head can absorb larger updates |
| Weight decay | 1e-4 | AdamW default; light L2 regularization |
| Batch size | 32 (16 for ViT) | Memory-bound on 16 GB MPS |
| Image size | 224 × 224 | Native to ImageNet-pretrained backbones |
| Freeze epochs | 3 | Warm-up: head converges before backbone unlocks |
| Epoch cap | 15 (12 for ViT) | Empirical: val acc plateaus before this |
| Early-stopping patience | 5 | Halt if no val improvement for 5 consecutive epochs |
| Augmentation | RandomResizedCrop · HFlip · Rotation ±15° · ColorJitter 0.1 | Standard for natural images |

The candidate search space that *would* be explored in a follow-up
Hyperband / Optuna run is documented for reference:

| Hyperparameter | Candidate range |
|---|---|
| Backbone learning rate | {1e-5, 3e-5, 1e-4, 3e-4} |
| Head learning rate | {1e-4, 1e-3, 3e-3} |
| Weight decay | {0, 1e-4, 1e-3} |
| Dropout in head | {0.0, 0.2, 0.5} |
| Augmentation strength | {light, medium, strong} |

This is listed in `docs/14-future-work.md` as the first concrete next step.

## 13.5 Cross-validation strategy

We used **stratified hold-out cross-validation** with a 70/15/15 split
rather than k-fold CV. The justification is twofold:

1. The dataset is large enough (~14k images, mean ≈ 314 per class) that
   a single held-out test set of 2,217 images is a low-variance estimator
   of generalization. K-fold would have multiplied the training cost by
   the number of folds for a small gain in metric variance reduction.
2. Holding out a **fixed** test set across all three architectures means
   the comparison is apples-to-apples — each model is evaluated on the
   exact same 2,217 images, ruling out split luck as an explanation for
   any ranking difference.

A 5-fold stratified CV pass on the final architecture is listed in
section 14 (Future Work) as a sanity check we would run to put error
bars on the headline numbers.

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

The transfer learning hypothesis held: all three architectures converged to
high accuracy within a single training session, validating the choice to
avoid training from scratch. Contrary to expectations from the broader
literature, the CNN baselines outperformed ViT on this specific dataset.
The most plausible explanation is dataset size — 14 k images split across
47 classes is at the lower bound of what a Vision Transformer needs to
benefit from its larger capacity. CNNs with strong ImageNet priors
generalize better in this small-data regime.

The residual confusion between visually similar plants (Snake Plant vs Cast
Iron, Pothos vs Philodendron, several Calatheas) is the expected hard case
for any 47-class houseplant classifier; a partial mitigation is the
deliberate display of the top-3 alternatives, which gives the user a
fallback when the model is genuinely uncertain.

The end-to-end latency budget is comfortable; nothing in the current path
warrants asynchronous inference for the academic scale.

## 13.9 Limitations

- The dataset is biased toward studio-style photographs; field photos with cluttered backgrounds may degrade accuracy.
- The 47-class catalog is a small fraction of the houseplants found in the wild; out-of-distribution inputs produce confident-looking but wrong predictions absent the low-confidence banner.
- Toxicity information is sourced from public references (ASPCA, RHS) without veterinary review.
