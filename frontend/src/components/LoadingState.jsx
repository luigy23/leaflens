export default function LoadingState({ previewUrl }) {
  return (
    <div className="card flex flex-col items-center">
      {previewUrl && (
        <img
          src={previewUrl}
          alt="Uploaded plant"
          className="max-h-64 rounded-xl object-contain mb-6"
        />
      )}
      <p className="text-sage-700 font-medium mb-2">Identifying species...</p>
      <ul className="text-sm text-sage-500 space-y-1">
        <li>Analyzing leaf shape</li>
        <li>Comparing against catalog</li>
        <li>Writing care card</li>
      </ul>
      <div className="mt-4 w-32 h-1 rounded-full bg-sage-100 overflow-hidden">
        <div className="h-full bg-sage-500 animate-pulse w-1/2" />
      </div>
    </div>
  );
}
