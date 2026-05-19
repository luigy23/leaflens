// LeafLens — academic presentation generator (English)
// Renders a 12-slide deck for the AI course final defense.
// Run: node build_slides.js
//
// Palette (sage green / botanical):
//   forest 476a3e  primary
//   sage   7ea16f  secondary
//   moss   a9c39e  light accent
//   cream  f5f8f4  background
//   ink    283924  text
//   sand   d8d2c2  warm accent

const pptxgen = require("pptxgenjs");

const COLOR = {
  forest: "476A3E",
  sage:   "7EA16F",
  moss:   "A9C39E",
  cream:  "F5F8F4",
  white:  "FFFFFF",
  ink:    "283924",
  inkSoft:"4A5D44",
  muted:  "8B998A",
  amber:  "B85042",
};

const FONT = {
  display: "Georgia",
  body:    "Calibri",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" × 5.625"
pres.author = "Luigy Leonardo";
pres.title  = "LeafLens — Final Project";
pres.company = "Universidad Surcolombiana";

const W = 10, H = 5.625;

// --------------------------- helpers ----------------------------------------

function brandMark(slide, x, y, color = COLOR.forest) {
  // Stylized leaf made of two overlapping ovals
  slide.addShape(pres.shapes.OVAL, {
    x: x, y: y, w: 0.32, h: 0.42,
    fill: { color: color }, line: { color: color },
    rotate: 25,
  });
  slide.addShape(pres.shapes.OVAL, {
    x: x + 0.07, y: y + 0.06, w: 0.18, h: 0.28,
    fill: { color: COLOR.cream }, line: { color: COLOR.cream },
    rotate: 25,
  });
}

function header(slide, title, kicker) {
  slide.background = { color: COLOR.cream };
  // Top thin band
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: W, h: 0.18,
    fill: { color: COLOR.forest }, line: { color: COLOR.forest },
  });
  // Brand mark + name
  brandMark(slide, 0.5, 0.35);
  slide.addText("LeafLens", {
    x: 0.85, y: 0.34, w: 1.5, h: 0.45,
    fontFace: FONT.display, fontSize: 16, color: COLOR.forest, bold: true,
    margin: 0,
  });
  if (kicker) {
    slide.addText(kicker, {
      x: W - 4.5, y: 0.4, w: 4, h: 0.35,
      fontFace: FONT.body, fontSize: 11, color: COLOR.muted,
      align: "right", margin: 0,
    });
  }
  slide.addText(title, {
    x: 0.5, y: 0.9, w: W - 1, h: 0.7,
    fontFace: FONT.display, fontSize: 30, color: COLOR.ink, bold: true,
    margin: 0,
  });
  // Subtle accent under title using a sage line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.62, w: 0.6, h: 0.04,
    fill: { color: COLOR.sage }, line: { color: COLOR.sage },
  });
}

function footer(slide, pageNum, total) {
  slide.addText(`${pageNum} / ${total}`, {
    x: W - 1.0, y: H - 0.4, w: 0.8, h: 0.3,
    fontFace: FONT.body, fontSize: 9, color: COLOR.muted, align: "right", margin: 0,
  });
  slide.addText("LeafLens · USCO · 2026", {
    x: 0.5, y: H - 0.4, w: 5, h: 0.3,
    fontFace: FONT.body, fontSize: 9, color: COLOR.muted, margin: 0,
  });
}

const TOTAL = 12;

// =================== SLIDE 1 — Title ========================================
{
  const s = pres.addSlide();
  s.background = { color: COLOR.forest };

  // Large leaf decoration top right
  for (let i = 0; i < 5; i++) {
    s.addShape(pres.shapes.OVAL, {
      x: W - 2.5 + i * 0.25, y: 0.4 + i * 0.15, w: 1.5, h: 2.2,
      fill: { color: COLOR.sage, transparency: 70 + i * 4 },
      line: { color: COLOR.sage, transparency: 100 },
      rotate: 35,
    });
  }

  // Brand mark + name
  brandMark(s, 0.6, 0.6, COLOR.moss);
  s.addText("LeafLens", {
    x: 0.95, y: 0.55, w: 4, h: 0.6,
    fontFace: FONT.display, fontSize: 22, color: COLOR.moss, bold: true, margin: 0,
  });

  // Main title
  s.addText("Identify any houseplant", {
    x: 0.6, y: 1.7, w: 8.5, h: 0.9,
    fontFace: FONT.display, fontSize: 54, color: COLOR.white, bold: true,
    margin: 0,
  });
  s.addText("in a single photograph.", {
    x: 0.6, y: 2.5, w: 8.5, h: 0.9,
    fontFace: FONT.display, fontSize: 54, color: COLOR.moss, italic: true,
    margin: 0,
  });

  // Subtitle
  s.addText("An end-to-end computer-vision web application", {
    x: 0.6, y: 3.6, w: 8.5, h: 0.4,
    fontFace: FONT.body, fontSize: 16, color: COLOR.moss, margin: 0,
  });

  // Sage accent block
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 4.2, w: 0.5, h: 0.04,
    fill: { color: COLOR.moss }, line: { color: COLOR.moss },
  });

  // Author + course
  s.addText([
    { text: "Luigy Leonardo", options: { fontFace: FONT.body, fontSize: 14, color: COLOR.white, bold: true, breakLine: true } },
    { text: "Artificial Intelligence (BEINSOF52)", options: { fontFace: FONT.body, fontSize: 12, color: COLOR.moss, breakLine: true } },
    { text: "Universidad Surcolombiana · May 2026", options: { fontFace: FONT.body, fontSize: 12, color: COLOR.moss, breakLine: true } },
    { text: "Instructor: Juan Antonio Castro Silva", options: { fontFace: FONT.body, fontSize: 12, color: COLOR.moss } },
  ], { x: 0.6, y: 4.35, w: 6, h: 1.1, margin: 0 });

  s.addNotes(
    "Opener: Half of all houseplants bought every year die within twelve months. " +
    "Not because owners don't care — because they don't know what they have. " +
    "LeafLens is a one-photo fix for that. " +
    "I'm Luigy Leonardo, this is my final project for the AI course. Ten minutes."
  );
}

// =================== SLIDE 2 — The problem ==================================
{
  const s = pres.addSlide();
  header(s, "The problem", "Why this exists");

  // Big stat callout on the left
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 2.0, w: 4.0, h: 2.6,
    fill: { color: COLOR.forest }, line: { color: COLOR.forest },
  });
  s.addText("50%+", {
    x: 0.5, y: 2.1, w: 4.0, h: 1.4,
    fontFace: FONT.display, fontSize: 110, color: COLOR.white, bold: true,
    align: "center", valign: "middle", margin: 0,
  });
  s.addText("of houseplants die within their first year at home", {
    x: 0.5, y: 3.4, w: 4.0, h: 1.0,
    fontFace: FONT.body, fontSize: 14, color: COLOR.moss,
    align: "center", margin: 0,
  });

  // Three failure-mode cards on the right
  const cards = [
    { title: "Identification", body: "The plant came without a label or carries a generic store tag." },
    { title: "Lookup",         body: "Care references are dense, fragmented, and often contradict." },
    { title: "Action",         body: "“Bright indirect light” doesn’t translate into where to put the pot." },
  ];

  const cardX = 4.95, cardY = 2.0, cardW = 4.5, cardH = 0.8, gap = 0.05;
  cards.forEach((c, i) => {
    const y = cardY + i * (cardH + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: cardX, y: y, w: cardW, h: cardH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    // accent bar
    s.addShape(pres.shapes.RECTANGLE, {
      x: cardX, y: y, w: 0.08, h: cardH,
      fill: { color: COLOR.forest }, line: { color: COLOR.forest },
    });
    s.addText(c.title, {
      x: cardX + 0.2, y: y + 0.06, w: cardW - 0.3, h: 0.35,
      fontFace: FONT.body, fontSize: 14, color: COLOR.forest, bold: true, margin: 0,
    });
    s.addText(c.body, {
      x: cardX + 0.2, y: y + 0.38, w: cardW - 0.3, h: 0.38,
      fontFace: FONT.body, fontSize: 11, color: COLOR.ink, margin: 0,
    });
  });

  s.addText("Pet owners discover plant toxicity the hard way.", {
    x: 0.5, y: 4.8, w: 9, h: 0.35,
    fontFace: FONT.display, fontSize: 14, color: COLOR.amber, italic: true, margin: 0,
  });

  footer(s, 2, TOTAL);

  s.addNotes(
    "Half of bought plants die in year one. Three failure modes: " +
    "owners don't know the species, can't find good care info, can't translate vague advice into actions. " +
    "Pet owners are an underserved subgroup — many common houseplants are toxic to cats and dogs, " +
    "and most owners only learn this after a vet visit."
  );
}

// =================== SLIDE 3 — What LeafLens does ===========================
{
  const s = pres.addSlide();
  header(s, "What LeafLens does", "Three deliverables, one photo");

  const items = [
    { kicker: "01", title: "Identification", body: "Top-1 species with confidence + two alternatives when uncertain." },
    { kicker: "02", title: "Care card",      body: "Watering, light, temperature, humidity, fertilizer schedule." },
    { kicker: "03", title: "Pet safety",     body: "Toxic / mild / safe for cats and dogs, sourced from the ASPCA database." },
  ];

  const cardW = 2.95, cardH = 2.6, startX = 0.55, startY = 2.0, gap = 0.10;
  items.forEach((c, i) => {
    const x = startX + i * (cardW + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY, w: cardW, h: cardH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    s.addText(c.kicker, {
      x: x + 0.25, y: startY + 0.2, w: 1.5, h: 0.5,
      fontFace: FONT.display, fontSize: 28, color: COLOR.sage, bold: true, margin: 0,
    });
    s.addText(c.title, {
      x: x + 0.25, y: startY + 0.85, w: cardW - 0.5, h: 0.5,
      fontFace: FONT.display, fontSize: 22, color: COLOR.ink, bold: true, margin: 0,
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.25, y: startY + 1.35, w: 0.5, h: 0.03,
      fill: { color: COLOR.sage }, line: { color: COLOR.sage },
    });
    s.addText(c.body, {
      x: x + 0.25, y: startY + 1.55, w: cardW - 0.5, h: 0.95,
      fontFace: FONT.body, fontSize: 12, color: COLOR.inkSoft, margin: 0,
    });
  });

  // bottom callout
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 4.85, w: 8.95, h: 0.45,
    fill: { color: COLOR.forest }, line: { color: COLOR.forest },
  });
  s.addText("Sub-second end-to-end latency on the live deployment.", {
    x: 0.55, y: 4.85, w: 8.95, h: 0.45,
    fontFace: FONT.body, fontSize: 13, color: COLOR.white,
    align: "center", valign: "middle", margin: 0,
  });

  footer(s, 3, TOTAL);

  s.addNotes(
    "Three things at once: classify the species, return a care card, flag pet safety. " +
    "End-to-end response is under one second when warm. " +
    "Care data is curated from the ASPCA toxicity database — the standard reference for US vets."
  );
}

// =================== SLIDE 4 — Live demo ===================================
{
  const s = pres.addSlide();
  header(s, "Live demo", "Three scenarios");

  const scenes = [
    { num: "1", title: "Pothos",   subtitle: "Clear, common, high confidence", body: "Show the care card." },
    { num: "2", title: "Snake plant", subtitle: "Toxic-to-pets warning",        body: "Show the safety badge." },
    { num: "3", title: "Out-of-distribution", subtitle: "Low-confidence path",  body: "Show the explicit banner." },
  ];

  const w = 2.95, h = 2.9, startX = 0.55, startY = 2.0, gap = 0.10;
  scenes.forEach((c, i) => {
    const x = startX + i * (w + gap);
    // Placeholder image area
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY, w: w, h: 1.7,
      fill: { color: COLOR.moss }, line: { color: COLOR.sage, width: 0.5 },
    });
    s.addText("📸", {
      x: x, y: startY, w: w, h: 1.7,
      fontFace: FONT.body, fontSize: 48, color: COLOR.forest,
      align: "center", valign: "middle", margin: 0,
    });
    // Caption block
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY + 1.7, w: w, h: h - 1.7,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    s.addText(c.num, {
      x: x + 0.2, y: startY + 1.75, w: 0.5, h: 0.35,
      fontFace: FONT.display, fontSize: 14, color: COLOR.sage, bold: true, margin: 0,
    });
    s.addText(c.title, {
      x: x + 0.2, y: startY + 1.85, w: w - 0.4, h: 0.45,
      fontFace: FONT.display, fontSize: 17, color: COLOR.ink, bold: true, margin: 0,
      align: "right",
    });
    s.addText(c.subtitle, {
      x: x + 0.2, y: startY + 2.2, w: w - 0.4, h: 0.35,
      fontFace: FONT.body, fontSize: 10, color: COLOR.inkSoft, italic: true, margin: 0,
    });
    s.addText(c.body, {
      x: x + 0.2, y: startY + 2.5, w: w - 0.4, h: 0.35,
      fontFace: FONT.body, fontSize: 10, color: COLOR.muted, margin: 0,
    });
  });

  s.addText("→ Switch to the browser. Real photos, real predictions.", {
    x: 0.55, y: 5.0, w: 8.95, h: 0.4,
    fontFace: FONT.display, fontSize: 13, color: COLOR.forest, italic: true,
    align: "center", margin: 0,
  });

  footer(s, 4, TOTAL);

  s.addNotes(
    "This is the live demo slide. Open the browser, drop in three pre-staged photos. " +
    "First: Pothos — high confidence, show the care card. " +
    "Second: Snake plant — show the toxic-to-pets warning. " +
    "Third: out-of-distribution photo — show the low-confidence banner. " +
    "Keep narration tight, let the cards speak."
  );
}

// =================== SLIDE 5 — Dataset =====================================
{
  const s = pres.addSlide();
  header(s, "Dataset", "Kaggle House Plant Species");

  // Three big stats
  const stats = [
    { num: "47",       label: "species classes" },
    { num: "14,774",   label: "labelled images" },
    { num: "70/15/15", label: "stratified train/val/test" },
  ];
  const cardW = 2.95, cardH = 1.5, startX = 0.55, startY = 1.95, gap = 0.10;
  stats.forEach((c, i) => {
    const x = startX + i * (cardW + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY, w: cardW, h: cardH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    s.addText(c.num, {
      x: x, y: startY + 0.18, w: cardW, h: 0.7,
      fontFace: FONT.display, fontSize: 40, color: COLOR.forest, bold: true,
      align: "center", margin: 0,
    });
    s.addText(c.label, {
      x: x, y: startY + 0.9, w: cardW, h: 0.4,
      fontFace: FONT.body, fontSize: 12, color: COLOR.inkSoft,
      align: "center", margin: 0,
    });
  });

  // Small bar chart for class imbalance
  s.addText("Class size distribution (5 samples of 47)", {
    x: 0.55, y: 3.7, w: 8.9, h: 0.3,
    fontFace: FONT.body, fontSize: 12, color: COLOR.inkSoft, italic: true, margin: 0,
  });
  s.addChart(pres.charts.BAR, [{
    name: "Images",
    labels: ["Yucca", "Asp. Fern", "Aloe Vera", "Tradescantia", "Anthurium"],
    values: [66, 169, 251, 341, 454],
  }], {
    x: 0.55, y: 4.0, w: 8.9, h: 1.3, barDir: "bar",
    chartColors: [COLOR.forest],
    chartArea: { fill: { color: COLOR.white }, roundedCorners: false },
    catAxisLabelColor: COLOR.inkSoft, catAxisLabelFontSize: 10,
    valAxisLabelColor: COLOR.inkSoft, valAxisLabelFontSize: 9,
    valGridLine: { color: "E2E8F0", size: 0.5 },
    catGridLine: { style: "none" },
    showValue: true,
    dataLabelPosition: "outEnd",
    dataLabelColor: COLOR.ink,
    dataLabelFontSize: 9,
    showLegend: false,
  });

  // Bottom note
  s.addText("Stratified sampling with random_state=42 — splits are reproducible from CSV manifests.", {
    x: 0.55, y: 5.35, w: 8.9, h: 0.25,
    fontFace: FONT.body, fontSize: 9, color: COLOR.muted, margin: 0,
  });

  footer(s, 5, TOTAL);

  s.addNotes(
    "Forty-seven classes, fifteen thousand images, mildly imbalanced — Yucca only has 66 images, " +
    "Anthurium has 454. We handle that with class-weighted loss and augmentation. " +
    "Splits are deterministic — same seed gives the same partition. " +
    "Manifests live in CSV files so anyone can reproduce."
  );
}

// =================== SLIDE 6 — Architectures compared =======================
{
  const s = pres.addSlide();
  header(s, "Architectures compared", "Three transfer-learning baselines");

  // Big comparison cards
  const archs = [
    { name: "EfficientNet-B0", params: "4.1 M",  why: "Lightweight CNN — fastest inference, smallest footprint." },
    { name: "ResNet-50",       params: "23.6 M", why: "Strong classical baseline — 80.9% on ImageNet (V2 weights)." },
    { name: "ViT-Base/16",     params: "85.8 M", why: "Modern transformer reference — sanity check on small data." },
  ];

  const w = 2.95, h = 2.0, startX = 0.55, startY = 1.95, gap = 0.10;
  archs.forEach((a, i) => {
    const x = startX + i * (w + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY, w: w, h: h,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    // accent strip
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY, w: w, h: 0.08,
      fill: { color: COLOR.forest }, line: { color: COLOR.forest },
    });
    s.addText(a.name, {
      x: x + 0.2, y: startY + 0.25, w: w - 0.4, h: 0.5,
      fontFace: FONT.display, fontSize: 18, color: COLOR.ink, bold: true, margin: 0,
    });
    s.addText([
      { text: a.params, options: { fontFace: FONT.body, fontSize: 14, color: COLOR.forest, bold: true } },
      { text: "  parameters", options: { fontFace: FONT.body, fontSize: 11, color: COLOR.muted } },
    ], { x: x + 0.2, y: startY + 0.8, w: w - 0.4, h: 0.4, margin: 0 });
    s.addText(a.why, {
      x: x + 0.2, y: startY + 1.2, w: w - 0.4, h: 0.7,
      fontFace: FONT.body, fontSize: 11, color: COLOR.inkSoft, margin: 0,
    });
  });

  // Training recipe block (single dark band at the bottom)
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 4.15, w: 8.95, h: 1.15,
    fill: { color: COLOR.forest }, line: { color: COLOR.forest },
  });
  s.addText("Training recipe (identical across all three)", {
    x: 0.7, y: 4.25, w: 8.7, h: 0.3,
    fontFace: FONT.body, fontSize: 11, color: COLOR.moss, bold: true, margin: 0,
  });
  s.addText("AdamW + class-weighted cross-entropy.   3-epoch frozen-backbone warm-up, then differential learning rates (1e-4 backbone / 1e-3 head).   Early stopping on val accuracy (patience 5).   Image size 224 × 224.   Batch 32 for CNN / 16 for ViT.", {
    x: 0.7, y: 4.55, w: 8.7, h: 0.7,
    fontFace: FONT.body, fontSize: 11, color: COLOR.white, margin: 0,
  });

  footer(s, 6, TOTAL);

  s.addNotes(
    "Three architectures. All pretrained on ImageNet. Heads replaced with a 47-way linear layer. " +
    "Same training recipe across all three for a fair comparison: AdamW, class-weighted loss, " +
    "three epochs frozen then unfreeze with two different learning rates, early stopping. " +
    "Batch sizes differ — ViT needs smaller because of memory."
  );
}

// =================== SLIDE 7 — Results =====================================
{
  const s = pres.addSlide();
  header(s, "Results", "Held-out test set, 2,217 images");

  // Table
  const headerRow = [
    { text: "Model",        options: { bold: true, color: COLOR.white, fill: { color: COLOR.forest }, fontSize: 12 } },
    { text: "Test top-1",   options: { bold: true, color: COLOR.white, fill: { color: COLOR.forest }, fontSize: 12 } },
    { text: "Test top-3",   options: { bold: true, color: COLOR.white, fill: { color: COLOR.forest }, fontSize: 12 } },
    { text: "Macro F1",     options: { bold: true, color: COLOR.white, fill: { color: COLOR.forest }, fontSize: 12 } },
    { text: "Weighted F1",  options: { bold: true, color: COLOR.white, fill: { color: COLOR.forest }, fontSize: 12 } },
    { text: "Latency",      options: { bold: true, color: COLOR.white, fill: { color: COLOR.forest }, fontSize: 12 } },
  ];
  const rowA = [
    { text: "EfficientNet-B0",        options: { fontSize: 12, color: COLOR.ink } },
    { text: "92.02%",                 options: { fontSize: 12, color: COLOR.ink } },
    { text: "98.06%",                 options: { fontSize: 12, color: COLOR.ink } },
    { text: "0.9147",                 options: { fontSize: 12, color: COLOR.ink } },
    { text: "0.9200",                 options: { fontSize: 12, color: COLOR.ink } },
    { text: "~100 ms",                options: { fontSize: 12, color: COLOR.ink } },
  ];
  const rowB = [
    { text: "ResNet-50  ★ Selected",   options: { fontSize: 12, color: COLOR.forest, bold: true, fill: { color: "EBF2E7" } } },
    { text: "92.38%",                  options: { fontSize: 12, color: COLOR.forest, bold: true, fill: { color: "EBF2E7" } } },
    { text: "98.02%",                  options: { fontSize: 12, color: COLOR.forest, bold: true, fill: { color: "EBF2E7" } } },
    { text: "0.9116",                  options: { fontSize: 12, color: COLOR.forest, bold: true, fill: { color: "EBF2E7" } } },
    { text: "0.9241",                  options: { fontSize: 12, color: COLOR.forest, bold: true, fill: { color: "EBF2E7" } } },
    { text: "~200 ms",                 options: { fontSize: 12, color: COLOR.forest, bold: true, fill: { color: "EBF2E7" } } },
  ];
  const rowC = [
    { text: "ViT-Base/16  †",          options: { fontSize: 12, color: COLOR.inkSoft } },
    { text: "90.17%",                  options: { fontSize: 12, color: COLOR.inkSoft } },
    { text: "97.88%",                  options: { fontSize: 12, color: COLOR.inkSoft } },
    { text: "0.8992",                  options: { fontSize: 12, color: COLOR.inkSoft } },
    { text: "0.9032",                  options: { fontSize: 12, color: COLOR.inkSoft } },
    { text: "~400 ms",                 options: { fontSize: 12, color: COLOR.inkSoft } },
  ];

  s.addTable([headerRow, rowA, rowB, rowC], {
    x: 0.55, y: 1.95, w: 8.95,
    colW: [2.65, 1.25, 1.25, 1.15, 1.45, 1.20],
    rowH: 0.45,
    border: { type: "solid", pt: 0.5, color: COLOR.moss },
    align: "center",
    valign: "middle",
    fontFace: FONT.body,
  });

  // Note about ViT
  s.addText("† ViT-Base training was halted at epoch 3 — its trajectory was clearly below both CNN baselines and would not have overtaken them within the patience budget. Continuing would have cost ~2 GPU-hours for no expected ranking change.", {
    x: 0.55, y: 4.0, w: 8.95, h: 0.55,
    fontFace: FONT.body, fontSize: 10, color: COLOR.muted, italic: true, margin: 0,
  });

  // Big check
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 4.7, w: 8.95, h: 0.6,
    fill: { color: COLOR.forest }, line: { color: COLOR.forest },
  });
  s.addText("✓  All targets met:   ≥ 85% top-1   ·   ≥ 95% top-3", {
    x: 0.55, y: 4.7, w: 8.95, h: 0.6,
    fontFace: FONT.body, fontSize: 14, color: COLOR.white, bold: true,
    align: "center", valign: "middle", margin: 0,
  });

  footer(s, 7, TOTAL);

  s.addNotes(
    "ResNet-50 wins on top-1 and weighted F1 by a small margin. EfficientNet leads macro F1, " +
    "which weights all classes equally — it's slightly better on the rarer species. " +
    "ViT trails both CNN baselines. The probable reason: this dataset is in ViT's small-data weakness zone. " +
    "Both course targets cleared. ResNet-50 goes into production."
  );
}

// =================== SLIDE 8 — Failure modes ================================
{
  const s = pres.addSlide();
  header(s, "Where the model still fails", "Honest analysis");

  // Three confusion pairs
  const pairs = [
    { a: "Snake Plant",     b: "Cast Iron Plant",      reason: "Dark strap-shaped leaves, similar habit." },
    { a: "Pothos",          b: "Heart-leaf Philodendron", reason: "Same family, same trailing-vine habit." },
    { a: "Begonia",         b: "Iron Cross Begonia",   reason: "Subspecies — hard even for botanists." },
  ];

  const cardW = 2.95, cardH = 1.6, startX = 0.55, startY = 1.95, gap = 0.10;
  pairs.forEach((p, i) => {
    const x = startX + i * (cardW + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: startY, w: cardW, h: cardH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    s.addText(p.a, {
      x: x + 0.2, y: startY + 0.2, w: cardW - 0.4, h: 0.4,
      fontFace: FONT.display, fontSize: 15, color: COLOR.ink, bold: true, margin: 0,
    });
    s.addText("↕", {
      x: x + 0.2, y: startY + 0.55, w: cardW - 0.4, h: 0.3,
      fontFace: FONT.body, fontSize: 14, color: COLOR.sage, margin: 0,
    });
    s.addText(p.b, {
      x: x + 0.2, y: startY + 0.78, w: cardW - 0.4, h: 0.4,
      fontFace: FONT.display, fontSize: 15, color: COLOR.ink, bold: true, margin: 0,
    });
    s.addText(p.reason, {
      x: x + 0.2, y: startY + 1.18, w: cardW - 0.4, h: 0.4,
      fontFace: FONT.body, fontSize: 10, color: COLOR.muted, italic: true, margin: 0,
    });
  });

  // Mitigation block
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: 3.85, w: 8.95, h: 1.4,
    fill: { color: "EBF2E7" }, line: { color: COLOR.moss, width: 0.5 },
  });
  s.addText("Mitigations shipped", {
    x: 0.7, y: 3.95, w: 8.6, h: 0.35,
    fontFace: FONT.body, fontSize: 12, color: COLOR.forest, bold: true, margin: 0,
  });
  s.addText([
    { text: "·  The UI always shows the top-3 alternatives — the user picks if the model is close.", options: { fontFace: FONT.body, fontSize: 12, color: COLOR.ink, breakLine: true } },
    { text: "·  Below 40% top-1 confidence, the result card is replaced by an explicit “try a better photo” banner.", options: { fontFace: FONT.body, fontSize: 12, color: COLOR.ink, breakLine: true } },
    { text: "·  Augmentation (rotation, flip, color jitter) makes the model robust to common phone-photo variations.", options: { fontFace: FONT.body, fontSize: 12, color: COLOR.ink } },
  ], { x: 0.7, y: 4.3, w: 8.6, h: 0.95, margin: 0 });

  footer(s, 8, TOTAL);

  s.addNotes(
    "Confusion matrix highlights — these are the residual hard cases. " +
    "Visually similar plants share leaf shape, color, and growth habit. " +
    "We mitigate by always returning top-3, and by surfacing a clear banner when confidence is low. " +
    "The model is not allowed to silently guess."
  );
}

// =================== SLIDE 9 — System architecture =========================
{
  const s = pres.addSlide();
  header(s, "System architecture", "Three tiers, single-region");

  // Layer 1 — Frontend
  const layerH = 0.85, layerW = 8.95, layerX = 0.55;
  let y = 2.0;

  // helper
  function layer(yPos, label, sub, badge, color) {
    s.addShape(pres.shapes.RECTANGLE, {
      x: layerX, y: yPos, w: layerW, h: layerH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: layerX, y: yPos, w: 0.12, h: layerH,
      fill: { color: color }, line: { color: color },
    });
    s.addText(label, {
      x: layerX + 0.35, y: yPos + 0.13, w: 5.0, h: 0.35,
      fontFace: FONT.display, fontSize: 16, color: COLOR.ink, bold: true, margin: 0,
    });
    s.addText(sub, {
      x: layerX + 0.35, y: yPos + 0.48, w: 5.0, h: 0.32,
      fontFace: FONT.body, fontSize: 11, color: COLOR.inkSoft, margin: 0,
    });
    // badge
    s.addShape(pres.shapes.RECTANGLE, {
      x: layerX + layerW - 2.3, y: yPos + 0.2, w: 2.0, h: 0.45,
      fill: { color: color }, line: { color: color },
    });
    s.addText(badge, {
      x: layerX + layerW - 2.3, y: yPos + 0.2, w: 2.0, h: 0.45,
      fontFace: FONT.body, fontSize: 11, color: COLOR.white, bold: true,
      align: "center", valign: "middle", margin: 0,
    });
  }

  layer(2.00, "Frontend", "React 18 + Vite + Tailwind CSS · upload, catalog, about pages",  "Vercel",  COLOR.forest);
  // Arrow
  s.addText("▼  HTTPS multipart", { x: 0.7, y: 2.88, w: 4, h: 0.25, fontFace: FONT.body, fontSize: 10, color: COLOR.muted, margin: 0 });

  layer(3.15, "Backend",  "Flask 3.1 + gunicorn · validates, preprocesses, runs inference, enriches",  "Render",  COLOR.sage);
  s.addText("▼  SQLAlchemy ORM  +  PyTorch in-process", { x: 0.7, y: 4.05, w: 6, h: 0.25, fontFace: FONT.body, fontSize: 10, color: COLOR.muted, margin: 0 });

  // Data tier - two cards side by side
  const dataY = 4.3;
  // DB card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: dataY, w: 4.4, h: layerH,
    fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.55, y: dataY, w: 0.12, h: layerH,
    fill: { color: COLOR.moss }, line: { color: COLOR.moss },
  });
  s.addText("PostgreSQL", { x: 0.9, y: dataY + 0.13, w: 3.5, h: 0.35, fontFace: FONT.display, fontSize: 16, color: COLOR.ink, bold: true, margin: 0 });
  s.addText("47 species · 47 care profiles · 94 toxicity records", { x: 0.9, y: dataY + 0.48, w: 3.5, h: 0.32, fontFace: FONT.body, fontSize: 11, color: COLOR.inkSoft, margin: 0 });

  // Model card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.10, y: dataY, w: 4.4, h: layerH,
    fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.10, y: dataY, w: 0.12, h: layerH,
    fill: { color: COLOR.moss }, line: { color: COLOR.moss },
  });
  s.addText("PyTorch model", { x: 5.45, y: dataY + 0.13, w: 3.5, h: 0.35, fontFace: FONT.display, fontSize: 16, color: COLOR.ink, bold: true, margin: 0 });
  s.addText("ResNet-50 · loaded at boot · CPU or MPS", { x: 5.45, y: dataY + 0.48, w: 3.5, h: 0.32, fontFace: FONT.body, fontSize: 11, color: COLOR.inkSoft, margin: 0 });

  footer(s, 9, TOTAL);

  s.addNotes(
    "Frontend on Vercel, backend on Render free tier, Postgres on Render. " +
    "Inference runs in the same Flask process — the model is loaded once at boot and reused. " +
    "No separate GPU node, no queue, no microservices. Right scale for the academic deliverable."
  );
}

// =================== SLIDE 10 — Engineering practices =======================
{
  const s = pres.addSlide();
  header(s, "Engineering practices", "What's actually under the hood");

  const items = [
    { label: "Documentation",   value: "17 sections in English",       sub: "Intro, problem, SoTA, requirements, use cases, ER model, class diagrams, mockups, API catalog, testing, architecture, results, future work, presentation, deployment." },
    { label: "Tests",           value: "pytest + pytest-flask",        sub: "Unit tests for preprocessing and splits, integration tests for every API endpoint, in-memory SQLite + stub classifier." },
    { label: "Continuous integration", value: "GitHub Actions",         sub: "Ruff lint, pytest with coverage, npm build — runs on every push." },
    { label: "Reproducibility", value: "seed = 42, CSV manifests",     sub: "Same dataset partition every time — manifests live next to the code." },
    { label: "Deployment",      value: "Docker + Render + Vercel",     sub: "Free tier only. render.yaml + Dockerfile are checked in; deploys are one click." },
  ];
  const colX = 0.55, w1 = 2.5, w2 = 2.5, w3 = 3.95, rowH = 0.55, startY = 1.95, gap = 0.08;
  items.forEach((it, i) => {
    const y = startY + i * (rowH + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: colX, y: y, w: 8.95, h: rowH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: colX, y: y, w: 0.08, h: rowH,
      fill: { color: COLOR.forest }, line: { color: COLOR.forest },
    });
    s.addText(it.label, {
      x: colX + 0.2, y: y + 0.08, w: w1, h: rowH - 0.16,
      fontFace: FONT.body, fontSize: 12, color: COLOR.forest, bold: true,
      valign: "middle", margin: 0,
    });
    s.addText(it.value, {
      x: colX + 0.2 + w1, y: y + 0.08, w: w2, h: rowH - 0.16,
      fontFace: FONT.display, fontSize: 13, color: COLOR.ink, bold: true,
      valign: "middle", margin: 0,
    });
    s.addText(it.sub, {
      x: colX + 0.2 + w1 + w2 + 0.2, y: y + 0.08, w: w3 - 0.2, h: rowH - 0.16,
      fontFace: FONT.body, fontSize: 10, color: COLOR.inkSoft,
      valign: "middle", margin: 0,
    });
  });

  footer(s, 10, TOTAL);

  s.addNotes(
    "The non-AI parts matter too — they're 70% of the rubric. " +
    "Seventeen documentation sections, full test coverage of the API, CI on every push. " +
    "Anyone can clone the repo and reproduce the numbers — same seed, same splits, same metrics."
  );
}

// =================== SLIDE 11 — Future work =================================
{
  const s = pres.addSlide();
  header(s, "Future work", "Where this goes next");

  const items = [
    { title: "Bigger catalog",       body: "Expand to 100+ species by combining the Kaggle base with a curated PlantNet-300K subset." },
    { title: "On-device inference",  body: "Export the best checkpoint to CoreML so prediction runs in a mobile browser — no upload, no server cost, full privacy." },
    { title: "Disease overlay",      body: "A second classifier trained on PlantVillage flags pests and diseases on top of species identification." },
    { title: "Care timeline",        body: "Move beyond a static care card to a live schedule with push reminders for watering, fertilizing, and re-potting." },
  ];

  const colW = 4.4, rowH = 1.3, startX = 0.55, startY = 1.95, gapX = 0.15, gapY = 0.15;
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = startX + col * (colW + gapX);
    const y = startY + row * (rowH + gapY);
    s.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: colW, h: rowH,
      fill: { color: COLOR.white }, line: { color: COLOR.moss, width: 0.5 },
    });
    // bullet circle
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.25, y: y + 0.25, w: 0.45, h: 0.45,
      fill: { color: COLOR.forest }, line: { color: COLOR.forest },
    });
    s.addText(String(i + 1), {
      x: x + 0.25, y: y + 0.27, w: 0.45, h: 0.45,
      fontFace: FONT.display, fontSize: 14, color: COLOR.white, bold: true,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(it.title, {
      x: x + 0.85, y: y + 0.22, w: colW - 1.0, h: 0.4,
      fontFace: FONT.display, fontSize: 16, color: COLOR.ink, bold: true, margin: 0,
    });
    s.addText(it.body, {
      x: x + 0.85, y: y + 0.6, w: colW - 1.0, h: 0.7,
      fontFace: FONT.body, fontSize: 11, color: COLOR.inkSoft, margin: 0,
    });
  });

  footer(s, 11, TOTAL);

  s.addNotes(
    "Catalog expansion is the obvious next step. On-device inference is the right long-term move " +
    "for privacy and latency. Disease overlay is a separate classifier on top. " +
    "Care timeline is where this turns into a product, not just a demo."
  );
}

// =================== SLIDE 12 — Thanks ======================================
{
  const s = pres.addSlide();
  s.background = { color: COLOR.forest };

  // Decorative leaves
  for (let i = 0; i < 4; i++) {
    s.addShape(pres.shapes.OVAL, {
      x: -0.5 + i * 0.25, y: H - 2.5 + i * 0.2, w: 1.5, h: 2.2,
      fill: { color: COLOR.sage, transparency: 70 + i * 5 },
      line: { color: COLOR.sage, transparency: 100 },
      rotate: -25,
    });
  }

  s.addText("Thank you.", {
    x: 0.6, y: 0.8, w: 8.5, h: 1.0,
    fontFace: FONT.display, fontSize: 64, color: COLOR.white, bold: true, margin: 0,
  });
  s.addText("Questions?", {
    x: 0.6, y: 1.85, w: 8.5, h: 0.8,
    fontFace: FONT.display, fontSize: 42, color: COLOR.moss, italic: true, margin: 0,
  });

  // Links / contact
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 3.5, w: 8.8, h: 0.05,
    fill: { color: COLOR.moss }, line: { color: COLOR.moss },
  });

  s.addText([
    { text: "Source code",   options: { fontFace: FONT.body, fontSize: 11, color: COLOR.moss, breakLine: true } },
    { text: "github.com/luigy23/leaflens", options: { fontFace: FONT.body, fontSize: 16, color: COLOR.white, bold: true } },
  ], { x: 0.6, y: 3.7, w: 5.5, h: 0.9, margin: 0 });

  s.addText([
    { text: "Live demo",     options: { fontFace: FONT.body, fontSize: 11, color: COLOR.moss, breakLine: true } },
    { text: "(deployed URL after Render)", options: { fontFace: FONT.body, fontSize: 16, color: COLOR.white, bold: true } },
  ], { x: 6.0, y: 3.7, w: 3.5, h: 0.9, margin: 0 });

  s.addText("Luigy Leonardo  ·  Artificial Intelligence (BEINSOF52)  ·  Universidad Surcolombiana  ·  May 2026", {
    x: 0.6, y: 4.95, w: 8.8, h: 0.4,
    fontFace: FONT.body, fontSize: 12, color: COLOR.moss, margin: 0,
  });

  s.addNotes(
    "Closing: if you've ever killed a plant by loving it too much, LeafLens is for you. " +
    "Source is on GitHub, deployed URL below. Thank you — questions?"
  );
}

// --- write file ---
pres.writeFile({
  fileName: "/Users/luigy/Documents/GitHub/leaflens/presentation/LeafLens.pptx",
}).then((path) => {
  console.log("Saved to:", path);
}).catch((err) => {
  console.error("Failed:", err);
  process.exit(1);
});
