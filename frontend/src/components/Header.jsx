import { NavLink, Link } from "react-router-dom";

const linkClass = ({ isActive }) =>
  `text-sm font-medium px-3 py-1 rounded-full transition ${
    isActive ? "bg-sage-100 text-sage-800" : "text-sage-600 hover:text-sage-800"
  }`;

export default function Header() {
  return (
    <header className="border-b border-sage-100 bg-white">
      <div className="max-w-5xl mx-auto px-5 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-display text-xl text-sage-800">
          <img src="/leaf.svg" alt="" className="w-6 h-6" />
          LeafLens
        </Link>
        <nav className="flex items-center gap-1">
          <NavLink to="/" className={linkClass} end>
            Home
          </NavLink>
          <NavLink to="/catalog" className={linkClass}>
            Catalog
          </NavLink>
          <NavLink to="/about" className={linkClass}>
            About
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
