"""Extract mermaid blocks from .md files and render in HTML, Markdown, or PDF."""
import sys
import re
import os
import json
import base64
import tempfile
import webbrowser
import argparse
import shutil
import subprocess
import time
from pathlib import Path


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


def generate_html(diagrams: list[tuple[str, str, str]], for_pdf: bool = False) -> str:
    """Generate HTML with mermaid.js CDN rendering. diagrams = [(title, code, source_path)]"""
    cards = ""
    for i, (title, code, source) in enumerate(diagrams):
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        live_link = ""
        if not for_pdf:
            live_url = make_mermaid_live_url(code)
            live_link = f'<a href="{live_url}" target="_blank" class="live-link">Mermaid Live Editor で開く</a>'
        cards += f"""
    <div class="card">
      <div class="card-header">
        <h2>{title}</h2>
        <span class="source">{source}</span>
        {live_link}
      </div>
      <pre class="mermaid">{escaped}</pre>
    </div>"""

    pdf_style = ""
    if for_pdf:
        pdf_style = """
  @media print {
    body { background: #fff; padding: 10px; }
    .card { box-shadow: none; border: 1px solid #ddd; break-inside: avoid; }
  }"""

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
  .count {{ color: #666; font-size: 14px; margin-bottom: 16px; }}{pdf_style}
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


def generate_markdown(diagrams: list[tuple[str, str, str]]) -> str:
    """Generate consolidated Markdown with all diagrams."""
    lines = ["# State Diagrams", ""]
    for i, (title, code, source) in enumerate(diagrams):
        lines.append(f"## {title}")
        lines.append(f"")
        lines.append(f"Source: `{source}`")
        lines.append("")
        lines.append("```mermaid")
        lines.append(code)
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def find_browser_for_pdf() -> str | None:
    """Find a Chromium-based browser for headless PDF generation."""
    candidates = [
        shutil.which("msedge"),
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chrome"),
    ]
    # Windows-specific paths
    win_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if path:
            return path
    for path in win_paths:
        if os.path.isfile(path):
            return path
    return None


def generate_pdf(html_content: str, output_path: Path) -> bool:
    """Generate PDF from HTML using a headless Chromium-based browser."""
    browser = find_browser_for_pdf()
    if not browser:
        return False

    # Write HTML to temp file
    html_path = Path(tempfile.gettempdir()) / "state_diagrams_pdf_src.html"
    html_path.write_text(html_content, encoding="utf-8")

    # Use headless browser to print to PDF
    # Add a delay via JS to let mermaid render before printing
    result = subprocess.run(
        [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={output_path}",
            str(html_path),
        ],
        capture_output=True,
        timeout=30,
    )
    return output_path.exists()


def collect_diagrams(filepaths: list[str]) -> list[tuple[str, str, str]]:
    """Collect diagrams from files with deduplication."""
    diagrams = []
    seen = set()
    for filepath in filepaths:
        real = os.path.realpath(filepath)
        if real in seen:
            continue
        seen.add(real)
        for title, code in extract_mermaid_blocks(filepath):
            diagrams.append((title, code, filepath))
    return diagrams


def main():
    parser = argparse.ArgumentParser(description="State diagram viewer/exporter")
    parser.add_argument("files", nargs="+", help="Markdown files containing mermaid diagrams")
    parser.add_argument("--format", choices=["html", "md", "pdf"], default="html",
                        help="Output format (default: html)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file path (default: auto-generated in temp dir)")
    args = parser.parse_args()

    diagrams = collect_diagrams(args.files)

    if not diagrams:
        print("No stateDiagram blocks found.")
        sys.exit(0)

    fmt = args.format

    if fmt == "html":
        html = generate_html(diagrams)
        out = Path(args.output) if args.output else Path(tempfile.gettempdir()) / "state_diagrams_viewer.html"
        out.write_text(html, encoding="utf-8")
        print(f"Output: {out}")
        webbrowser.open(str(out))

    elif fmt == "md":
        md = generate_markdown(diagrams)
        out = Path(args.output) if args.output else Path(tempfile.gettempdir()) / "state_diagrams.md"
        out.write_text(md, encoding="utf-8")
        print(f"Output: {out}")

    elif fmt == "pdf":
        html = generate_html(diagrams, for_pdf=True)
        out = Path(args.output) if args.output else Path(tempfile.gettempdir()) / "state_diagrams.pdf"
        if generate_pdf(html, out):
            print(f"Output: {out}")
        else:
            # Fallback: save HTML and inform user
            fallback = Path(tempfile.gettempdir()) / "state_diagrams_viewer.html"
            fallback.write_text(html, encoding="utf-8")
            print(f"PDF generation failed: Chromium-based browser not found.")
            print(f"HTML fallback saved: {fallback}")
            print("Open the HTML file and use Ctrl+P to save as PDF.")
            webbrowser.open(str(fallback))
            sys.exit(1)


if __name__ == "__main__":
    main()
