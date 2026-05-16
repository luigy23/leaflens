import { useCallback, useRef, useState } from "react";

const MAX_BYTES = 10 * 1024 * 1024;
const ACCEPTED = ["image/jpeg", "image/png", "image/webp"];

export default function UploadDropzone({ onFile, disabled }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState(null);

  const handleFiles = useCallback(
    (files) => {
      setError(null);
      const file = files?.[0];
      if (!file) return;
      if (!ACCEPTED.includes(file.type)) {
        setError("Please choose a JPG, PNG or WebP file.");
        return;
      }
      if (file.size > MAX_BYTES) {
        setError("File is larger than 10 MB.");
        return;
      }
      onFile(file);
    },
    [onFile],
  );

  return (
    <div className="card text-center">
      <div
        className={`border-2 border-dashed rounded-xl p-10 transition ${
          dragging ? "border-sage-500 bg-sage-50" : "border-sage-200"
        }`}
        onDragEnter={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          setDragging(false);
        }}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
      >
        <p className="text-sage-700">Drop a photo here</p>
        <p className="text-sage-400 my-2 text-sm">or</p>
        <button
          type="button"
          className="btn-primary"
          disabled={disabled}
          onClick={() => inputRef.current?.click()}
        >
          Choose a file
        </button>
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED.join(",")}
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <p className="text-xs text-sage-500 mt-4">JPG, PNG or WebP · max 10 MB</p>
        {error && <p className="text-sm text-red-600 mt-3">{error}</p>}
      </div>
    </div>
  );
}
