# LeafLens — HTML presentation

Reveal.js slide deck. Open in any browser, no build step.

## How to view

```bash
# Just open the file:
open index.html

# Or serve it locally (better for camera/clipboard demos):
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Keyboard shortcuts

| Key | Action |
|---|---|
| `→` / `Space` / `N` | Next slide |
| `←` / `P` | Previous slide |
| `Esc` / `O` | Slide overview |
| `S` | Open speaker notes window |
| `B` | Black out / pause |
| `F` | Toggle fullscreen |
| `?` | Show all shortcuts |

## Export to PDF

1. Open `index.html?print-pdf` in Chrome
2. File → Print → Save as PDF
3. Settings: A4 landscape, no margins, background graphics ON

## Files

- `index.html` — all 12 slides in one file
- `styles.css` — sage botanical theme
- Loads `reveal.js` 5 from CDN (no install needed)

## Speaker notes

Each slide has speaker notes (`<aside class="notes">`). Press **S** during presentation to open the notes window on a second screen.
