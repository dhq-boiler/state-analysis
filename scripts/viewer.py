"""Extract mermaid blocks from .md files and open in browser with mermaid.js rendering."""
import sys
import re
import os
import json
import base64
import tempfile
import webbrowser
from pathlib import Path
from urllib.parse import quote


def extract_mermaid_blocks(filepath: str) -> list[tuple[str, str]]:
    """Return list of (title, mermaid_code) from a markdown file."""
    text = Path(filepath).read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\s*\n(.*?)```", text, re.DOTALL)
    title = Path(filepath).stem
    return [(title, block.strip()) for block in blocks if "stateDiagram" in block]


def make_mermaid_live_url(code: str) -> str:
    """Generate a mermaid.live edit URL for a single diagram."""
    import zlib
    state = json.dumps({"code": code, "mermaid": {"theme": "default"}, "autoSync": True})
    compressed = zlib.compress(state.encode("utf-8"), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    return f"https://mermaid.live/edit#pako:{encoded}"


def generate_html(diagrams: list[tuple[str, str, str]]) -> str:
    """Generate HTML with mermaid.js CDN rendering. diagrams = [(title, code, source_path)]"""
    cards = ""
    for i, (title, code, source) in enumerate(diagrams):
        live_url = make_mermaid_live_url(code)
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        cards += f"""
    <div class="card">
      <div class="card-header">
        <h2>{title}</h2>
        <span class="source">{source}</span>
        <a href="{live_url}" target="_blank" class="live-link">Mermaid Live Editor で開く</a>
      </div>
      <pre class="mermaid">{escaped}</pre>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>State Diagrams</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
  h1 {{ color: #333; margin-bottom: 24px; }}
  .card {{ background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 24px; padding: 24px; }}
  .card-header {{ display: flex; align-items: baseline; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }}
  .card-header h2 {{ margin: 0; color: #1a1a1a; }}
  .source {{ color: #888; font-size: 13px; font-family: monospace; }}
  .live-link {{ font-size: 13px; margin-left: auto; color: #0066cc; text-decoration: none; }}
  .live-link:hover {{ text-decoration: underline; }}
  .mermaid {{ display: flex; justify-content: center; }}
  .count {{ color: #666; font-size: 14px; margin-bottom: 16px; }}
</style>
</head>
<body>
<h1>State Diagrams</h1>
<p class="count">{len(diagrams)} diagram(s) found</p>
{cards}
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: 'default' }});</script>
</body>
</html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: viewer.py <file1.md> [file2.md ...]")
        sys.exit(1)

    diagrams = []
    seen = set()
    for filepath in sys.argv[1:]:
        real = os.path.realpath(filepath)
        if real in seen:
            continue
        seen.add(real)
        for title, code in extract_mermaid_blocks(filepath):
            diagrams.append((title, code, filepath))

    if not diagrams:
        print("No stateDiagram blocks found.")
        sys.exit(0)

    html = generate_html(diagrams)
    out = Path(tempfile.gettempdir()) / "state_diagrams_viewer.html"
    out.write_text(html, encoding="utf-8")
    print(f"Viewer: {out}")
    webbrowser.open(str(out))


if __name__ == "__main__":
    main()
