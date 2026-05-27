// Class distribution from data/processed/class_distribution.csv (seed 42).
// Sorted by total image count descending.
const SPECIES = [
  { name: "Monstera Deliciosa", train: 383, val: 82, test: 82, total: 547 },
  { name: "Dumb Cane (Dieffenbachia spp.)", train: 379, val: 81, test: 81, total: 541 },
  { name: "Chinese evergreen (Aglaonema)", train: 360, val: 77, test: 77, total: 514 },
  { name: "Lilium (Hemerocallis)", train: 335, val: 72, test: 72, total: 479 },
  { name: "Anthurium (Anthurium andraeanum)", train: 318, val: 68, test: 68, total: 454 },
  { name: "ZZ Plant (Zamioculcas zamiifolia)", train: 306, val: 66, test: 66, total: 438 },
  { name: "Daffodils (Narcissus spp.)", train: 295, val: 63, test: 63, total: 421 },
  { name: "Lily of the valley (Convallaria majalis)", train: 288, val: 62, test: 62, total: 412 },
  { name: "Prayer Plant (Maranta leuconeura)", train: 280, val: 60, test: 60, total: 400 },
  { name: "Snake plant (Sanseviera)", train: 277, val: 60, test: 59, total: 396 },
  { name: "Peace lily", train: 269, val: 58, test: 58, total: 385 },
  { name: "Chinese Money Plant (Pilea peperomioides)", train: 268, val: 57, test: 57, total: 382 },
  { name: "Money Tree (Pachira aquatica)", train: 251, val: 54, test: 54, total: 359 },
  { name: "Jade plant (Crassula ovata)", train: 247, val: 53, test: 53, total: 353 },
  { name: "Ctenanthe", train: 240, val: 52, test: 52, total: 344 },
  { name: "Tradescantia", train: 239, val: 51, test: 51, total: 341 },
  { name: "Polka Dot Plant (Hypoestes phyllostachya)", train: 239, val: 51, test: 51, total: 341 },
  { name: "Tulip", train: 238, val: 51, test: 51, total: 340 },
  { name: "African Violet (Saintpaulia ionantha)", train: 236, val: 50, test: 51, total: 337 },
  { name: "Elephant Ear (Alocasia spp.)", train: 232, val: 50, test: 50, total: 332 },
  { name: "Calathea", train: 231, val: 49, test: 50, total: 330 },
  { name: "Parlor Palm (Chamaedorea elegans)", train: 231, val: 49, test: 49, total: 329 },
  { name: "Schefflera", train: 228, val: 49, test: 49, total: 326 },
  { name: "Hyacinth (Hyacinthus orientalis)", train: 222, val: 48, test: 48, total: 318 },
  { name: "Rattlesnake Plant (Calathea lancifolia)", train: 221, val: 47, test: 47, total: 315 },
  { name: "Christmas Cactus (Schlumbergera bridgesii)", train: 218, val: 47, test: 47, total: 312 },
  { name: "Boston Fern (Nephrolepis exaltata)", train: 214, val: 46, test: 46, total: 306 },
  { name: "Poinsettia (Euphorbia pulcherrima)", train: 214, val: 46, test: 46, total: 306 },
  { name: "Rubber Plant (Ficus elastica)", train: 203, val: 44, test: 44, total: 291 },
  { name: "Birds Nest Fern (Asplenium nidus)", train: 203, val: 43, test: 44, total: 290 },
  { name: "Cast Iron Plant (Aspidistra elatior)", train: 186, val: 40, test: 40, total: 266 },
  { name: "Iron Cross begonia (Begonia masoniana)", train: 186, val: 40, test: 40, total: 266 },
  { name: "Dracaena", train: 183, val: 39, test: 39, total: 261 },
  { name: "Aloe Vera", train: 175, val: 38, test: 38, total: 251 },
  { name: "Pothos (Ivy arum)", train: 170, val: 37, test: 36, total: 243 },
  { name: "English Ivy (Hedera helix)", train: 168, val: 36, test: 36, total: 240 },
  { name: "Orchid", train: 164, val: 35, test: 35, total: 234 },
  { name: "Begonia (Begonia spp.)", train: 163, val: 35, test: 35, total: 233 },
  { name: "Chrysanthemum", train: 147, val: 31, test: 31, total: 209 },
  { name: "Sago Palm (Cycas revoluta)", train: 142, val: 30, test: 30, total: 202 },
  { name: "Venus Flytrap", train: 139, val: 30, test: 30, total: 199 },
  { name: "Ponytail Palm (Beaucarnea recurvata)", train: 138, val: 29, test: 30, total: 197 },
  { name: "Areca Palm (Dypsis lutescens)", train: 133, val: 28, test: 28, total: 189 },
  { name: "Bird of Paradise (Strelitzia reginae)", train: 126, val: 27, test: 27, total: 180 },
  { name: "Asparagus Fern (Asparagus setaceus)", train: 119, val: 25, test: 25, total: 169 },
  { name: "Kalanchoe", train: 91, val: 20, test: 19, total: 130 },
  { name: "Yucca", train: 46, val: 10, test: 10, total: 66 },
];

const TOTAL_IMAGES = SPECIES.reduce((acc, s) => acc + s.total, 0);
const TOTAL_TRAIN = SPECIES.reduce((acc, s) => acc + s.train, 0);
const TOTAL_VAL = SPECIES.reduce((acc, s) => acc + s.val, 0);
const TOTAL_TEST = SPECIES.reduce((acc, s) => acc + s.test, 0);
const MAX_TOTAL = SPECIES[0].total; // biggest class for bar scaling

export default function AboutPage() {
  return (
    <article className="prose prose-sage max-w-3xl space-y-6 text-sage-700">
      <h1 className="font-display text-3xl text-sage-800">About LeafLens</h1>
      <p>
        LeafLens classifies houseplants from photographs and returns care
        instructions. It was built as an academic project at Universidad
        Surcolombiana for the Artificial Intelligence course.
      </p>

      <section>
        <h2 className="font-display text-xl text-sage-800">How it works</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>Upload a photo of a houseplant.</li>
          <li>
            A deep learning model (ResNet-50, fine-tuned on the House Plant
            Species dataset) classifies it among 47 species.
          </li>
          <li>
            The system looks up watering, light, temperature, and toxicity
            information from a curated database.
          </li>
        </ul>
      </section>

      <section>
        <h2 className="font-display text-xl text-sage-800">Dataset</h2>
        <p>
          Source:{" "}
          <a
            href="https://www.kaggle.com/datasets/kacpergregorowicz/house-plant-species"
            target="_blank"
            rel="noreferrer"
            className="underline"
          >
            Kaggle — House Plant Species
          </a>{" "}
          (by <em>kacpergregorowicz</em>). Stratified 70 / 15 / 15 split with{" "}
          <code className="rounded bg-sage-100 px-1 py-0.5 text-xs">
            random_state=42
          </code>{" "}
          — reproducible from CSV manifests in <code>data/processed/</code>.
        </p>

        {/* Dataset summary cards */}
        <div className="not-prose mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
          <SummaryCard label="Classes" value="47" />
          <SummaryCard label="Total images" value={TOTAL_IMAGES.toLocaleString()} />
          <SummaryCard label="Train" value={TOTAL_TRAIN.toLocaleString()} sub="70%" />
          <SummaryCard label="Val + Test" value={(TOTAL_VAL + TOTAL_TEST).toLocaleString()} sub="15% / 15%" />
        </div>

        {/* All 47 species */}
        <div className="not-prose mt-6 rounded-2xl border border-sage-200 bg-white">
          <header className="flex items-center justify-between border-b border-sage-100 px-5 py-3">
            <h3 className="font-display text-base text-sage-800">
              All 47 species — image counts
            </h3>
            <span className="text-xs font-mono text-sage-500">
              sorted by total ↓
            </span>
          </header>

          <ol className="divide-y divide-sage-100">
            {SPECIES.map((s, idx) => (
              <li key={s.name} className="flex items-center gap-3 px-5 py-2.5 text-sm">
                <span className="w-6 text-right font-mono text-xs text-sage-400">
                  {String(idx + 1).padStart(2, "0")}
                </span>
                <span className="flex-1 truncate text-sage-800">{s.name}</span>
                <div className="flex hidden items-center gap-2 sm:flex">
                  <SplitChip label="train" value={s.train} />
                  <SplitChip label="val" value={s.val} />
                  <SplitChip label="test" value={s.test} />
                </div>
                <div className="w-32">
                  <div className="h-1.5 w-full overflow-hidden rounded-full bg-sage-100">
                    <div
                      className="h-full rounded-full bg-sage-500"
                      style={{ width: `${(s.total / MAX_TOTAL) * 100}%` }}
                    />
                  </div>
                </div>
                <span className="w-12 text-right font-mono text-sm font-semibold text-sage-800">
                  {s.total}
                </span>
              </li>
            ))}
          </ol>

          <footer className="flex flex-wrap items-center justify-between gap-2 border-t border-sage-100 px-5 py-3 text-xs text-sage-500">
            <span>Min: Yucca (66) · Max: Monstera (547) · Mean: 314 · Median: 318</span>
            <span className="font-mono">{TOTAL_IMAGES.toLocaleString()} images total</span>
          </footer>
        </div>
      </section>

      <section>
        <h2 className="font-display text-xl text-sage-800">Class balancing</h2>
        <p>
          Two layers: a{" "}
          <code className="rounded bg-sage-100 px-1 py-0.5 text-xs">
            WeightedRandomSampler
          </code>{" "}
          at the DataLoader oversamples minority classes so each minibatch is
          class-balanced before the model (measured ratio 8.3× → 1.36×).
          A class-weighted cross-entropy loss compensates any residual skew
          per batch.
        </p>
      </section>

      <section>
        <h2 className="font-display text-xl text-sage-800">Models compared</h2>
        <p>
          EfficientNet-B0 (92.02%), <strong>ResNet-50 (92.38% — deployed)</strong>,
          ViT-Base/16 (90.17%). All three use transfer learning from ImageNet
          weights, fine-tuned with a 3-epoch frozen-backbone warm-up followed
          by differential learning rates.
        </p>
      </section>

      <section>
        <h2 className="font-display text-xl text-sage-800">Privacy</h2>
        <p>
          Uploaded images are not stored. Only the anonymous prediction outcome
          (species id, confidence, latency) is logged for analytics.
        </p>
      </section>
    </article>
  );
}

function SummaryCard({ label, value, sub }) {
  return (
    <div className="rounded-xl border border-sage-200 bg-white px-4 py-3">
      <div className="text-xs font-mono uppercase tracking-wide text-sage-500">
        {label}
      </div>
      <div className="mt-1 font-display text-2xl text-sage-800">{value}</div>
      {sub && <div className="text-xs text-sage-400">{sub}</div>}
    </div>
  );
}

function SplitChip({ label, value }) {
  return (
    <span className="rounded-md bg-sage-50 px-1.5 py-0.5 text-[10px] font-mono text-sage-600">
      <span className="text-sage-400">{label}</span>{" "}
      <span className="font-semibold text-sage-800">{value}</span>
    </span>
  );
}
