function lightLabel(level) {
  switch (level) {
    case "low":
      return "Low light";
    case "medium-indirect":
      return "Medium, indirect light";
    case "bright-indirect":
      return "Bright, indirect light";
    case "direct":
      return "Direct sunlight";
    default:
      return level;
  }
}

function toxicityBadge(records) {
  if (!records || records.length === 0) return null;
  const toxic = records.filter((r) => r.level === "toxic").map((r) => r.animal);
  const mild = records.filter((r) => r.level === "mild").map((r) => r.animal);
  if (toxic.length === 0 && mild.length === 0) {
    return <span className="text-emerald-700 text-sm">✓ Safe for cats and dogs</span>;
  }
  return (
    <span className="text-amber-700 text-sm">
      ⚠ {toxic.length ? `Toxic to ${toxic.join(" and ")}.` : ""}{" "}
      {mild.length ? `Mild for ${mild.join(" and ")}.` : ""}
    </span>
  );
}

export default function CareCard({ care, toxicity }) {
  if (!care) {
    return <p className="text-sage-500 text-sm">No care profile available.</p>;
  }
  return (
    <div className="space-y-3 text-sm text-sage-700">
      <p>
        💧 Water every <strong>{care.watering_days_min}–{care.watering_days_max} days</strong>
      </p>
      <p>☀ {lightLabel(care.light_level)}</p>
      <p>
        🌡 {care.temperature_min_c}–{care.temperature_max_c} °C
      </p>
      {care.humidity_pct && <p>💨 Humidity {care.humidity_pct}%</p>}
      {care.fertilizer_schedule && <p>🌱 Fertilize {care.fertilizer_schedule}</p>}
      <div className="pt-2">{toxicityBadge(toxicity)}</div>
    </div>
  );
}
