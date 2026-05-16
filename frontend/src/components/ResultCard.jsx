import CareCard from "./CareCard.jsx";

function ConfidenceBar({ value }) {
  const pct = Math.round(value * 100);
  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-2 rounded-full bg-sage-100 overflow-hidden">
        <div className="h-full bg-sage-500" style={{ width: `${pct}%` }} />
      </div>
      <span className="text-sm font-semibold text-sage-700 w-12 text-right">{pct}%</span>
    </div>
  );
}

export default function ResultCard({ data, previewUrl, onReset }) {
  if (!data) return null;
  const top = data.topk[0];

  if (data.low_confidence) {
    return (
      <div className="card">
        <h3 className="font-display text-lg text-amber-700 mb-2">⚠ Low confidence</h3>
        <p className="text-sage-700 text-sm mb-4">
          The most likely match is <strong>{top.common_name}</strong>, but only with{" "}
          {Math.round(top.confidence * 100)}% confidence. For a better identification, try a
          photo that shows the entire plant, has even daylight, and focuses on the leaves.
        </p>
        <button className="btn-primary" onClick={onReset}>
          Try a different photo
        </button>
      </div>
    );
  }

  return (
    <div className="card space-y-6">
      <div className="flex flex-col sm:flex-row gap-6">
        {previewUrl && (
          <img
            src={previewUrl}
            alt="Uploaded plant"
            className="w-full sm:w-40 h-40 object-cover rounded-xl"
          />
        )}
        <div className="flex-1 space-y-2">
          <h2 className="font-display text-2xl text-sage-800">{top.common_name}</h2>
          <p className="text-sm italic text-sage-500">
            {top.scientific_name}
            {top.care && top.species_id ? " · " : ""}
          </p>
          <ConfidenceBar value={top.confidence} />
        </div>
      </div>

      <section>
        <h3 className="font-display text-base text-sage-700 mb-3">Care</h3>
        <CareCard care={top.care} toxicity={top.toxicity} />
      </section>

      {data.topk.length > 1 && (
        <section>
          <h3 className="font-display text-base text-sage-700 mb-3">Other possibilities</h3>
          <ul className="text-sm text-sage-600 space-y-1">
            {data.topk.slice(1).map((item) => (
              <li key={item.rank}>
                • {item.common_name} ({Math.round(item.confidence * 100)}%)
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="flex justify-end">
        <button className="btn-ghost" onClick={onReset}>
          Identify another plant
        </button>
      </div>
    </div>
  );
}
