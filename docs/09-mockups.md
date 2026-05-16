# 9. GUI Mockups

The frontend is a single-page React application styled with Tailwind CSS. The visual language is calm and botanical: warm whites for background, sage and forest greens for accents, generous whitespace, rounded corners. The mockups below are described in ASCII for portability; a Figma file is referenced in section 12.

## 9.1 Home page (desktop)

```
+-------------------------------------------------------------------------+
|  🌿 LeafLens          Home   Catalog   About                            |
+-------------------------------------------------------------------------+
|                                                                         |
|                  Identify any houseplant in seconds.                    |
|                                                                         |
|             +-----------------------------------------------+           |
|             |                                               |           |
|             |       ┌──────────────────────────────┐        |           |
|             |       │     Drop a photo here        │        |           |
|             |       │            or                │        |           |
|             |       │     [ Choose a file ]        │        |           |
|             |       └──────────────────────────────┘        |           |
|             |                                               |           |
|             |  Accepted: JPG, PNG, WebP  (max 10 MB)        |           |
|             |                                               |           |
|             +-----------------------------------------------+           |
|                                                                         |
|             How it works   ·   Privacy   ·   Open source                |
+-------------------------------------------------------------------------+
```

## 9.2 Home page (mobile)

```
+----------------------+
|  🌿 LeafLens   ☰     |
+----------------------+
|                      |
|  Identify any        |
|  houseplant in       |
|  seconds.            |
|                      |
|  ┌────────────────┐  |
|  │  Drop a photo  │  |
|  │      or        │  |
|  │ [Choose a file]│  |
|  └────────────────┘  |
|                      |
|  JPG, PNG, WebP      |
|  max 10 MB           |
|                      |
+----------------------+
```

## 9.3 Loading state

```
+-------------------------------------------------------------------------+
|                                                                         |
|             +---------------------------------+                          |
|             |        [ uploaded photo ]       |                          |
|             |                                 |                          |
|             |                                 |                          |
|             +---------------------------------+                          |
|                                                                         |
|                  Identifying species...                                  |
|                  ●○○ analyzing leaf shape                                |
|                  ●●○ comparing against catalog                           |
|                  ●●● writing care card                                   |
|                                                                         |
+-------------------------------------------------------------------------+
```

## 9.4 Result card (high confidence)

```
+-------------------------------------------------------------------------+
|                                                                         |
|  +-------------------+    Golden Pothos                                  |
|  | [user's photo]    |    Epipremnum aureum  ·  Araceae                  |
|  |                   |    Confidence  ███████░░░  92%                    |
|  +-------------------+                                                   |
|                                                                         |
|  🩺  Care                                                                |
|       Water every 7-10 days   ·   Bright indirect light                  |
|       Temperature 18-30 °C    ·   Humidity 40-60 %                       |
|       Fertilize monthly in spring and summer                             |
|                                                                         |
|  🐾  Pet safety                                                          |
|       ⚠ Toxic to cats and dogs (calcium oxalate crystals).               |
|                                                                         |
|  Other possibilities                                                     |
|   • Heartleaf Philodendron  (5%)                                         |
|   • Satin Pothos            (2%)                                         |
|                                                                         |
|  [ Identify another plant ]                                              |
+-------------------------------------------------------------------------+
```

## 9.5 Result card (low confidence)

```
+-------------------------------------------------------------------------+
|                                                                         |
|  ⚠ Low confidence                                                        |
|                                                                         |
|  The most likely match is Snake Plant, but only with 34% confidence.    |
|  For a better identification, try a photo that:                          |
|                                                                         |
|     • Shows the entire plant including the pot                           |
|     • Has even daylight (avoid harsh backlight)                          |
|     • Focuses on the leaves                                              |
|                                                                         |
|  [ Try a different photo ]                                               |
+-------------------------------------------------------------------------+
```

## 9.6 Catalog grid

```
+-------------------------------------------------------------------------+
|  Browse 47 species                                                      |
|  [ Search... ]                                                          |
|                                                                         |
|  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐         |
|  │ [thumb]    │  │ [thumb]    │  │ [thumb]    │  │ [thumb]    │         |
|  │ Aloe Vera  │  │ Anthurium  │  │ Areca Palm │  │ Begonia    │         |
|  └────────────┘  └────────────┘  └────────────┘  └────────────┘         |
|                                                                         |
|  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐         |
|  │ [thumb]    │  │ [thumb]    │  │ [thumb]    │  │ [thumb]    │         |
|  │ Boston Fern│  │ Bromeliad  │  │ Cast Iron  │  │ ChinaDoll  │         |
|  └────────────┘  └────────────┘  └────────────┘  └────────────┘         |
|                                                                         |
|  ... 47 cards total ...                                                  |
+-------------------------------------------------------------------------+
```

## 9.7 About page

```
+-------------------------------------------------------------------------+
|  About LeafLens                                                         |
|                                                                         |
|  LeafLens classifies houseplants from photographs and returns care      |
|  instructions. It was built as an academic project at Universidad      |
|  Surcolombiana for the Artificial Intelligence course.                  |
|                                                                         |
|  How it works                                                           |
|  - Upload a photo of a houseplant.                                     |
|  - A deep learning model (Vision Transformer, fine-tuned on the         |
|    House Plant Species dataset) classifies it among 47 species.        |
|  - The system looks up watering, light, temperature, and toxicity      |
|    information from a curated database.                                |
|                                                                         |
|  Dataset                                                                |
|  - Kaggle House Plant Species (47 classes, ~14,000 images).            |
|                                                                         |
|  Models compared                                                        |
|  - EfficientNet-B0, ResNet-50, ViT-Base. Best in production.           |
|                                                                         |
|  Privacy                                                                |
|  - Uploaded images are not stored.                                     |
|                                                                         |
|  Source code                                                            |
|  - github.com/luigy/leaflens                                            |
+-------------------------------------------------------------------------+
```
