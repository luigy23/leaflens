export default function AboutPage() {
  return (
    <article className="prose prose-sage max-w-2xl space-y-4 text-sage-700">
      <h1 className="font-display text-3xl text-sage-800">About LeafLens</h1>
      <p>
        LeafLens classifies houseplants from photographs and returns care
        instructions. It was built as an academic project at Universidad
        Surcolombiana for the Artificial Intelligence course.
      </p>

      <h2 className="font-display text-xl text-sage-800">How it works</h2>
      <ul className="list-disc pl-5 space-y-1">
        <li>Upload a photo of a houseplant.</li>
        <li>
          A deep learning model (Vision Transformer, fine-tuned on the House
          Plant Species dataset) classifies it among 47 species.
        </li>
        <li>
          The system looks up watering, light, temperature, and toxicity
          information from a curated database.
        </li>
      </ul>

      <h2 className="font-display text-xl text-sage-800">Dataset</h2>
      <p>Kaggle House Plant Species (47 classes, ~14,000 images).</p>

      <h2 className="font-display text-xl text-sage-800">Models compared</h2>
      <p>EfficientNet-B0, ResNet-50, ViT-Base. The most accurate is used in production.</p>

      <h2 className="font-display text-xl text-sage-800">Privacy</h2>
      <p>Uploaded images are not stored.</p>
    </article>
  );
}
