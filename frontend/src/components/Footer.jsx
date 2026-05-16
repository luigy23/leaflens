export default function Footer() {
  return (
    <footer className="border-t border-sage-100 bg-white">
      <div className="max-w-5xl mx-auto px-5 py-6 text-xs text-sage-500 flex justify-between">
        <span>LeafLens · Academic project, Universidad Surcolombiana</span>
        <span>© {new Date().getFullYear()}</span>
      </div>
    </footer>
  );
}
