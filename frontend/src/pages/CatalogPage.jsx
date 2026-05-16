import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchCatalog } from "../api/client.js";

export default function CatalogPage() {
  const [items, setItems] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError(null);
    fetchCatalog(query)
      .then((data) => {
        if (alive) setItems(data.items);
      })
      .catch((err) => {
        if (alive) setError(err?.response?.data?.error || err.message);
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, [query]);

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="font-display text-3xl text-sage-800">Browse species</h1>
        <input
          type="search"
          placeholder="Search by name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="px-4 py-2 rounded-full border border-sage-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-sage-300"
        />
      </header>

      {loading && <p className="text-sage-500 text-sm">Loading…</p>}
      {error && <p className="text-red-600 text-sm">{error}</p>}

      <ul className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {items.map((sp) => (
          <li key={sp.id}>
            <Link
              to={`/species/${sp.id}`}
              className="card hover:shadow-md transition block h-full"
            >
              <h3 className="font-display text-lg text-sage-800">{sp.common_name}</h3>
              <p className="text-xs italic text-sage-500 mt-1">{sp.scientific_name}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
