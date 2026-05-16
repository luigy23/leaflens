import { useState } from "react";
import UploadDropzone from "../components/UploadDropzone.jsx";
import LoadingState from "../components/LoadingState.jsx";
import ResultCard from "../components/ResultCard.jsx";
import { predictSpecies } from "../api/client.js";

export default function HomePage() {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  function reset() {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  }

  async function handleFile(file) {
    reset();
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setLoading(true);
    try {
      const data = await predictSpecies(file);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.error || err.message || "Unknown error.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      {!result && !loading && (
        <section className="text-center max-w-2xl mx-auto">
          <h1 className="font-display text-4xl text-sage-800 mb-3">
            Identify any houseplant in seconds.
          </h1>
          <p className="text-sage-600">
            Upload a photo and LeafLens will tell you what species it is and how to care for it.
          </p>
        </section>
      )}

      {!result && !loading && <UploadDropzone onFile={handleFile} disabled={loading} />}
      {loading && <LoadingState previewUrl={previewUrl} />}
      {result && <ResultCard data={result} previewUrl={previewUrl} onReset={reset} />}
      {error && !loading && (
        <div className="card">
          <p className="text-red-700">{error}</p>
          <button className="btn-ghost mt-4" onClick={reset}>
            Try again
          </button>
        </div>
      )}
    </div>
  );
}
