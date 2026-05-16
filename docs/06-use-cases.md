# 6. Use Cases & User Stories

## 6.1 Actors

| Actor | Role |
|---|---|
| **Visitor** | Anonymous user who lands on the website. No account required. |
| **Plant owner** | Visitor with a specific plant they want identified. Primary persona. |
| **Pet owner** | Visitor checking whether a plant is safe around their cat or dog. |
| **Catalog browser** | Visitor exploring the species catalog out of curiosity, without uploading. |
| **System** | The LeafLens server: receives images, runs inference, returns results. |

## 6.2 Use case diagram (textual)

```
                     +-------------------------+
                     |        LeafLens         |
                     |                         |
   (Plant owner) --->|  UC1 Identify plant     |
                     |                         |
   (Pet owner)   --->|  UC2 Check pet safety   |
                     |                         |
   (Visitor)     --->|  UC3 Browse catalog     |
                     |                         |
   (Visitor)     --->|  UC4 View About page    |
                     +-------------------------+
                                  |
                                  | <<includes>>
                                  v
                     +-------------------------+
                     |   UC5 Validate image    |
                     |   UC6 Run inference     |
                     |   UC7 Lookup care card  |
                     +-------------------------+
```

## 6.3 Use case details

### UC1 — Identify plant

| Field | Value |
|---|---|
| **Actor** | Plant owner |
| **Goal** | Learn what species a plant is. |
| **Precondition** | Visitor is on the home page with a photo on their device. |
| **Trigger** | Visitor drags a photo onto the drop zone or clicks "Choose file". |
| **Main flow** | 1. Visitor selects an image. 2. Client validates size and format. 3. Client uploads image to `POST /api/predict`. 4. Server validates content and runs inference. 5. Server returns species, confidence, top-3, and care card. 6. Client displays the result. |
| **Alternate flow A** | If client-side validation fails, the upload button is disabled and an error is displayed. |
| **Alternate flow B** | If the top-1 confidence is below 40%, the result card shows a "low confidence — try another photo" banner. |
| **Postcondition** | The prediction is displayed. The result is stored in `localStorage` for history. |

### UC2 — Check pet safety

| Field | Value |
|---|---|
| **Actor** | Pet owner |
| **Goal** | Verify that a plant is safe to have around a cat or dog. |
| **Precondition** | UC1 has run successfully. |
| **Trigger** | The care card displays toxicity badges next to the species name. |
| **Main flow** | 1. Plant owner reviews the toxicity row on the care card. 2. If toxic, a warning icon and "Keep away from pets" copy is shown. |
| **Postcondition** | The owner has clear pet-safety information. |

### UC3 — Browse catalog

| Field | Value |
|---|---|
| **Actor** | Catalog browser |
| **Goal** | Explore the full catalog without uploading. |
| **Trigger** | Visitor clicks "Browse catalog" in the navigation. |
| **Main flow** | 1. Client requests `GET /api/species`. 2. Server returns the alphabetized list of all 47 species. 3. Visitor selects one. 4. Client requests `GET /api/species/{id}`. 5. Server returns the care card. 6. Client displays it. |
| **Postcondition** | Visitor has viewed the care card for one or more species. |

### UC4 — View About page

| Field | Value |
|---|---|
| **Actor** | Visitor |
| **Goal** | Understand how LeafLens works. |
| **Trigger** | Visitor clicks "About" in the navigation. |
| **Main flow** | Static content is rendered explaining the model, dataset, and contributors. |

### UC5 — Validate image (included)

The server checks content type, file size, and image dimensions before invoking the model. Invalid images cause a `400 Bad Request`.

### UC6 — Run inference (included)

The server preprocesses the image (resize, normalize), runs it through the selected PyTorch model, and obtains a 47-dimensional probability vector. Top-3 indices are selected.

### UC7 — Lookup care card (included)

The server queries PostgreSQL for the care record of the predicted species and merges it into the response payload.

## 6.4 User stories

| ID | As a... | I want to... | So that... |
|---|---|---|---|
| US-01 | plant owner | upload a photo of my plant and get its species name | I stop calling it "the green one with stripes". |
| US-02 | plant owner | see watering and light requirements right after identification | I know how to keep it alive. |
| US-03 | pet owner | know if the plant is toxic to my cat | I do not accidentally poison her. |
| US-04 | plant owner | see the top three matches when the model is unsure | I can pick the one that looks most like mine. |
| US-05 | catalog browser | look at every species the system knows about | I can shop for a new plant with confidence. |
| US-06 | mobile user | use the site on my phone | I do not have to switch to a laptop while standing in front of my plant. |
| US-07 | user with a bad photo | be told that my photo is too blurry | I take a better one. |
| US-08 | privacy-conscious user | be assured my photo is not stored | I feel comfortable uploading. |
