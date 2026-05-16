# 4. State of the Art

## 4.1 Plant identification as a computer vision problem

Plant identification from images sits at the intersection of fine-grained visual classification and large-scale species recognition. The challenge has been studied for more than a decade and has matured rapidly as deep learning replaced hand-engineered features.

### Early work (pre-2015)

Before convolutional neural networks dominated the field, plant classification relied on hand-crafted descriptors of leaf shape (Fourier descriptors, moment invariants), color histograms, and texture statistics fed into shallow classifiers — k-nearest neighbors, support vector machines, random forests. Representative works such as Mouine et al. (2013) and Kumar et al.'s *Leafsnap* (2012) achieved usable accuracy on small datasets (50–100 species) but degraded sharply as the catalog grew.

### Convolutional networks (2015–2020)

The breakthrough came with the application of ImageNet-pretrained CNNs to plant data via transfer learning. Sünderhauf et al. (2014) and later Lee et al. (2017) demonstrated that AlexNet and VGG-16, fine-tuned on plant photographs, surpassed all hand-engineered baselines. The PlantCLEF challenges, run annually as part of the LifeCLEF evaluation campaign, drove rapid progress: by 2019, ResNet-50 and Inception-v3 routinely scored above 80% top-1 on PlantCLEF test sets of several hundred species.

### Vision transformers and self-supervised learning (2020–present)

Vision Transformers (Dosovitskiy et al., 2020) opened a new frontier. ViT and its successors — Swin Transformer, ConvNeXt — match or surpass CNNs on PlantNet-style benchmarks. Self-supervised pretraining (DINOv2, MAE) has further closed the gap with supervised baselines, making it possible to fine-tune competitive plant classifiers with a few thousand labeled images.

## 4.2 Public datasets

| Dataset | Year | Species | Images | Use |
|---|---|---|---|---|
| Leafsnap | 2012 | 184 | 30,000 | Tree species, North American |
| Flavia | 2007 | 32 | 1,907 | Leaf images, plain background |
| PlantCLEF | 2011– | 1,000+ | 1M+ | Yearly challenge, full plants |
| PlantNet-300K | 2021 | 1,081 | 306,146 | Large-scale, long-tailed |
| iNaturalist Plants | 2017– | 4,000+ | 800,000+ | Citizen science, very diverse |
| House Plant Species (Kaggle) | 2024 | 47 | ~14,000 | Indoor plants only — used by LeafLens |

The PlantNet-300K release was a turning point because it explicitly modeled the long-tailed distribution found in nature and provided strong baselines. PlantCLEF benchmarks have also adopted the practice of separating "trusted" curated images from "noisy" web-scraped imagery, an important methodological lesson for academic work.

## 4.3 Commercial products

### PictureThis (Glority)

Currently the dominant consumer plant identification app, with reported revenue above USD 200 million in 2024. PictureThis uses a proprietary multi-model ensemble and a database of more than 17,000 species. Its core value proposition is not the model itself but the integration: identification, care reminders, diagnosis of common pests, community Q&A.

### PlantNet

A non-profit alternative driven by the Pl@ntNet consortium of French research labs. PlantNet's strength is breadth (more than 30,000 species worldwide) and its citizen-science backbone — every uploaded photograph contributes to the labeled corpus. Free to use, ad-supported, and openly published model checkpoints.

### Google Lens / Apple Visual Look Up

Both major mobile platforms now ship visual search features that include plant identification. They are excellent for breadth but ship no specialized care features.

## 4.4 Approaches relevant to LeafLens

LeafLens does not attempt to compete with PictureThis on scale or commercial polish. Its design is informed by three concrete choices that the literature supports:

1. **Transfer learning is sufficient.** Multiple independent studies (Mohanty et al., 2016; Pourreza et al., 2019) confirm that ImageNet-pretrained CNNs fine-tuned for 20–100 hours converge to greater than 90% top-1 on focused datasets.
2. **Architecture diversity matters for the ensemble case.** A CNN and a transformer make different mistakes; comparing both is good empirical practice. LeafLens compares EfficientNet-B0, ResNet-50, and ViT-Base.
3. **Care information should not come from the model.** The literature is clear that classifiers should classify; downstream attributes should be looked up in a structured knowledge base. LeafLens follows this separation strictly.

## 4.5 Gap LeafLens addresses

Most academic plant classifiers stop at the classification step and report accuracy numbers. Most commercial products integrate everything but are closed-source. LeafLens occupies a useful middle ground: an open, reproducible end-to-end system that demonstrates the full pipeline — data, training, comparison, serving, and consumer-facing UI — at academic scale.

## References

- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.* arXiv:2010.11929.
- Kumar, N. et al. (2012). *Leafsnap: A Computer Vision System for Automatic Plant Species Identification.* ECCV.
- Garcin, C. et al. (2021). *PlantNet-300K: a plant image dataset with high label ambiguity and a long-tailed distribution.* NeurIPS Datasets and Benchmarks Track.
- Mohanty, S. P., Hughes, D. P., & Salathé, M. (2016). *Using Deep Learning for Image-Based Plant Disease Detection.* Frontiers in Plant Science.
- Tan, M., & Le, Q. V. (2019). *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks.* ICML.
- He, K. et al. (2016). *Deep Residual Learning for Image Recognition.* CVPR.
