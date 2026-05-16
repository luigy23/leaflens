import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import CareCard from "../components/CareCard.jsx";
import { fetchSpecies } from "../api/client.js";

export default function SpeciesDetailPage() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSpecies(id)
      .then(setData)
      .catch((err) => setError(err?.response?.data?.error || err.message));
  }, [id]);

  if (error) return <p className="text-red-600 text-sm">{error}</p>;
  if (!data) return <p className="text-sage-500 text-sm">Loading…</p>;

  return (
    <article className="space-y-6 max-w-2xl">
      <Link to="/catalog" className="text-sm text-sage-600 hover:underline">
        ← Back to catalog
      </Link>
      <header>
        <h1 className="font-display text-3xl text-sage-800">{data.common_name}</h1>
        <p className="text-sm italic text-sage-500">{data.scientific_name}</p>
        {data.family && (
          <p className="text-xs text-sage-400 mt-1">Family: {data.family}</p>
        )}
      </header>
      {data.description && <p className="text-sage-700">{data.description}</p>}
      <section className="card">
        <h2 className="font-display text-lg text-sage-700 mb-3">Care</h2>
        <CareCard care={data.care} toxicity={data.toxicity} />
      </section>
    </article>
  );
}
