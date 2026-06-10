"""
Local Task 1 compliance review tool.

Run:
    python app.py

Then open:
    http://127.0.0.1:8000

No external APIs are used. The app wraps run_task1.py in a small local web
interface for reviewing inputs and downloading the generated report.
"""

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote
import html
import mimetypes
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
HOST = "127.0.0.1"
PORT = 8000

REQUIRED_PDFS = [
    "DSS_GZES230100125901_combined-1.pdf",
    "Manufacturer PDF 2 - 188_1115.pdf",
    "NEPQA 2025 (Nepal).pdf",
]


def file_status() -> list[tuple[str, bool, str]]:
    rows = []
    for name in REQUIRED_PDFS:
        path = BASE_DIR / name
        size = f"{path.stat().st_size:,} bytes" if path.exists() else "missing"
        rows.append((name, path.exists(), size))
    return rows


def output_status() -> list[tuple[str, bool, str]]:
    rows = []
    for name in [
        "compliance_draft.md",
        "compliance_draft.pdf",
        "approach_note.md",
        "review_checklist.md",
    ]:
        path = OUTPUT_DIR / name
        size = f"{path.stat().st_size:,} bytes" if path.exists() else "not generated"
        rows.append((name, path.exists(), size))
    return rows


def run_generator() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "run_task1.py"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode == 0, output


def pdf_available() -> bool:
    return (OUTPUT_DIR / "compliance_draft.pdf").exists()


def doc_cards() -> str:
    cards = []
    for name, exists, size in file_status():
        short = name[:42] + "…" if len(name) > 45 else name
        status_class = "doc-status--ready" if exists else "doc-status--missing"
        status_label = "Ready" if exists else "Missing"
        icon = "✓" if exists else "!"
        cards.append(f"""
        <div class="doc-card {'doc-card--ready' if exists else 'doc-card--missing'}">
          <div class="doc-card__icon" aria-hidden="true">
            <svg width="20" height="24" viewBox="0 0 20 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 2C2 0.895431 2.89543 0 4 0H13L19 6V22C19 23.1046 18.1046 24 17 24H4C2.89543 24 2 23.1046 2 22V2Z" fill="currentColor" opacity="0.15"/>
              <path d="M13 0L19 6H14C13.4477 6 13 5.55228 13 5V0Z" fill="currentColor" opacity="0.4"/>
              <path d="M2 2C2 0.895431 2.89543 0 4 0H13L19 6V22C19 23.1046 18.1046 24 17 24H4C2.89543 24 2 23.1046 2 22V2Z" stroke="currentColor" stroke-width="1.2"/>
            </svg>
          </div>
          <div class="doc-card__body">
            <span class="doc-card__name" title="{html.escape(name)}">{html.escape(short)}</span>
            <span class="doc-card__size">{html.escape(size)}</span>
          </div>
          <span class="{status_class}" title="{status_label}">{icon}</span>
        </div>""")
    return "\n".join(cards)


def output_rows_html() -> str:
    rows = []
    for name, exists, size in output_status():
        ext = name.rsplit(".", 1)[-1].upper()
        if exists:
            if name.endswith(".pdf"):
                action = f'<a class="dl-btn" href="/download/{html.escape(name)}">Download PDF</a>'
            else:
                action = '<span class="out-badge out-badge--ready">Generated</span>'
        else:
            action = '<span class="out-badge out-badge--pending">Pending</span>'
        rows.append(f"""
          <tr>
            <td class="col-name">
              <div class="col-name-inner">
                <span class="col-name-file"><span class="ext-tag">{ext}</span>{html.escape(name)}</span>
                <span class="col-size">{html.escape(size)}</span>
              </div>
            </td>
            <td class="col-action">{action}</td>
          </tr>""")
    return "\n".join(rows)


def page(message: str = "", run_ok: bool | None = None) -> str:
    has_pdf = pdf_available()

    log_class = ""
    if run_ok is True:
        log_class = "log--ok"
    elif run_ok is False:
        log_class = "log--fail"

    if has_pdf:
        preview_section = """
      <section class="preview-section">
        <header class="section-header">
          <h2>Compliance draft</h2>
          <span class="section-meta">compliance_draft.pdf</span>
        </header>
        <iframe class="pdf-viewer" src="/download/compliance_draft.pdf?view" title="Compliance draft PDF"></iframe>
      </section>"""
    else:
        preview_section = """
      <section class="preview-section">
        <header class="section-header">
          <h2>Compliance draft</h2>
        </header>
        <div class="preview-empty">
          <p>No draft generated yet.<br>Click <strong>Run compliance check</strong> to begin.</p>
        </div>
      </section>"""

    log_content = html.escape(message) if message else "Waiting to run."
    log_section = f"""
        <section class="log-section">
          <h2 class="section-label">Run log</h2>
          <pre class="log {log_class}">{log_content}</pre>
        </section>"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nepal Compliance Review</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --navy:       #1C2B3A;
      --navy-mid:   #2A3D52;
      --teal:       #2D6A4F;
      --teal-lt:    #E6F4EF;
      --teal-mid:   #52987A;
      --amber:      #B36B1A;
      --amber-lt:   #FEF5E7;
      --red:        #A0301E;
      --red-lt:     #FAEAE7;
      --ink:        #1A2630;
      --ink-mid:    #4A5A68;
      --ink-lt:     #8A9AA8;
      --border:     #D5DDE5;
      --border-lt:  #EBF0F4;
      --surface:    #FFFFFF;
      --bg:         #F2F4F7;
      --mono:       'DM Mono', Consolas, monospace;
      --sans:       'DM Sans', system-ui, sans-serif;
    }}

    body {{
      font-family: var(--sans);
      color: var(--ink);
      background: var(--bg);
      min-height: 100vh;
    }}

    /* ── Header ── */
    .site-header {{
      background: var(--navy);
      color: #fff;
      padding: 18px 32px;
      display: flex;
      align-items: baseline;
      gap: 16px;
    }}
    .site-header__title {{
      font-size: 16px;
      font-weight: 600;
      letter-spacing: 0.01em;
      color: #fff;
    }}
    .site-header__badge {{
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      background: rgba(255,255,255,0.12);
      color: rgba(255,255,255,0.7);
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .site-header__sub {{
      margin-left: auto;
      font-size: 12px;
      color: rgba(255,255,255,0.45);
    }}

    /* ── Layout ── */
    .layout {{
      display: grid;
      grid-template-columns: 400px 1fr;
      gap: 0;
      min-height: calc(100vh - 58px);
    }}

    /* ── Sidebar ── */
    .sidebar {{
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 0;
    }}
    .sidebar-block {{
      padding: 20px 22px;
      border-bottom: 1px solid var(--border-lt);
    }}
    .sidebar-block:last-child {{ border-bottom: none; flex: 1; }}

    .block-label {{
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-lt);
      margin-bottom: 14px;
    }}

    /* ── Document cards ── */
    .doc-card {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      margin-bottom: 8px;
      background: var(--bg);
    }}
    .doc-card--ready {{ border-color: #B8D9C9; background: #F4FAF7; }}
    .doc-card--missing {{ border-color: #EAC3BB; background: var(--red-lt); }}
    .doc-card--ready .doc-card__icon {{ color: var(--teal); }}
    .doc-card--missing .doc-card__icon {{ color: var(--red); }}
    .doc-card__body {{ flex: 1; min-width: 0; }}
    .doc-card__name {{
      display: block;
      font-size: 12px;
      font-weight: 500;
      color: var(--ink);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      font-family: var(--mono);
    }}
    .doc-card__size {{ font-size: 11px; color: var(--ink-lt); font-family: var(--mono); }}
    .doc-status--ready {{
      font-size: 12px;
      font-weight: 700;
      color: var(--teal);
      background: var(--teal-lt);
      border-radius: 50%;
      width: 22px; height: 22px;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }}
    .doc-status--missing {{
      font-size: 12px;
      font-weight: 700;
      color: var(--red);
      background: var(--red-lt);
      border-radius: 50%;
      width: 22px; height: 22px;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }}

    /* ── Run button ── */
    .run-form {{ display: flex; flex-direction: column; gap: 10px; }}
    .run-btn {{
      display: block;
      width: 100%;
      background: var(--teal);
      color: white;
      border: none;
      border-radius: 8px;
      padding: 12px 16px;
      font-family: var(--sans);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: background 0.15s;
    }}
    .run-btn:hover {{ background: #1f5037; }}
    .run-btn:active {{ background: #164029; }}
    .run-note {{
      font-size: 11px;
      color: var(--ink-lt);
      line-height: 1.5;
    }}

    /* ── Log ── */
    .log {{
      font-family: var(--mono);
      font-size: 11px;
      line-height: 1.6;
      color: var(--ink-mid);
      background: var(--bg);
      border: 1px solid var(--border-lt);
      border-radius: 6px;
      padding: 10px 12px;
      white-space: pre-wrap;
      max-height: 140px;
      overflow-y: auto;
    }}
    .log--ok {{ border-color: #B8D9C9; background: #F4FAF7; color: var(--teal); }}
    .log--fail {{ border-color: #EAC3BB; background: var(--red-lt); color: var(--red); }}

    /* ── Outputs table ── */
    .out-table {{ width: 100%; border-collapse: collapse; font-size: 12px; table-layout: fixed; }}
    .out-table td {{
      padding: 10px 6px;
      border-bottom: 1px solid var(--border-lt);
      vertical-align: middle;
      color: var(--ink-mid);
    }}
    .out-table tr:last-child td {{ border-bottom: none; }}
    .col-name {{ width: auto; }}
    .col-name-inner {{ display: flex; flex-direction: column; gap: 2px; }}
    .col-name-file {{ font-size: 12px; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .col-size {{ font-size: 11px; color: var(--ink-lt); font-family: var(--mono); }}
    .col-action {{ text-align: right; white-space: nowrap; width: 110px; }}

    .ext-tag {{
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.04em;
      background: var(--border-lt);
      color: var(--ink-mid);
      padding: 2px 5px;
      border-radius: 3px;
      margin-right: 4px;
    }}
    .dl-btn {{
      display: inline-block;
      background: var(--navy);
      color: #fff;
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: 5px;
      transition: background 0.15s;
    }}
    .dl-btn:hover {{ background: var(--navy-mid); }}
    .out-badge {{
      display: inline-block;
      font-size: 11px;
      font-weight: 500;
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .out-badge--ready {{ background: var(--teal-lt); color: var(--teal); }}
    .out-badge--pending {{ background: var(--border-lt); color: var(--ink-lt); }}

    /* ── Main area ── */
    .main-area {{
      display: flex;
      flex-direction: column;
      padding: 0;
      gap: 0;
      height: calc(100vh - 58px);
      overflow: hidden;
    }}
    .preview-section {{
      display: flex;
      flex-direction: column;
      flex: 1;
      min-height: 0;
      padding: 24px 32px;
    }}

    .section-header {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 12px;
      flex-shrink: 0;
    }}
    .section-header h2 {{
      font-size: 16px;
      font-weight: 600;
      color: var(--ink);
    }}
    .section-meta {{
      font-size: 12px;
      color: var(--ink-lt);
      font-family: var(--mono);
    }}

    .pdf-viewer {{
      width: 100%;
      flex: 1;
      min-height: 0;
      height: 0;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      display: block;
    }}

    .preview-empty {{
      background: var(--surface);
      border: 1px dashed var(--border);
      border-radius: 8px;
      padding: 56px 32px;
      text-align: center;
      color: var(--ink-lt);
      font-size: 14px;
      line-height: 1.7;
      min-height: 240px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .log-section {{ margin-top: 0; }}
    .section-label {{
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-lt);
      margin-bottom: 8px;
    }}

    .disclaimer {{
      font-size: 11px;
      color: var(--ink-lt);
      line-height: 1.6;
      padding-top: 16px;
      border-top: 1px solid var(--border-lt);
      margin-top: 6px;
    }}

    @media (max-width: 860px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ border-right: none; border-bottom: 1px solid var(--border); }}
      .site-header__sub {{ display: none; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <span class="site-header__title">Nepal Compliance Review</span>
    <span class="site-header__badge">Task 1</span>
    <span class="site-header__sub">SunBridge Trading · Local workflow · No external APIs</span>
  </header>

  <div class="layout">

    <aside class="sidebar">

      <div class="sidebar-block">
        <p class="block-label">Source documents</p>
        {doc_cards()}
      </div>

      <div class="sidebar-block">
        <form class="run-form" method="post" action="/generate">
          <button class="run-btn" type="submit">Run compliance check</button>
          <p class="run-note">Reads all three source PDFs and writes the draft report, approach note, and review checklist to <code>output/</code>.</p>
        </form>
      </div>

      {log_section}

      <div class="sidebar-block">
        <p class="block-label">Outputs</p>
        <table class="out-table">
          <tbody>
            {output_rows_html()}
          </tbody>
        </table>
        <p class="disclaimer">This tool organises the available paperwork, flags mismatches, and lists follow-up questions for the Nepal import agent. Compliance decisions remain with the responsible officer.</p>
      </div>

    </aside>

    <main class="main-area">
      {preview_section}
    </main>

  </div>

</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/":
            self.respond_html(page())
            return
        if self.path.startswith("/download/"):
            self.serve_download()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        if self.path == "/generate":
            ok, output = run_generator()
            prefix = "Done.\n\n" if ok else "Failed.\n\n"
            self.respond_html(page(prefix + output, run_ok=ok))
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def serve_download(self) -> None:
        raw = unquote(self.path.removeprefix("/download/"))
        name = raw.removesuffix("?view")
        path = OUTPUT_DIR / name

        if path.parent != OUTPUT_DIR or not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Output not found")
            return

        # PDF-only downloads
        if path.suffix.lower() != ".pdf":
            self.send_error(HTTPStatus.FORBIDDEN, "Only PDF downloads are available")
            return

        content_type = "application/pdf"
        data = path.read_bytes()
        # Use inline disposition so the iframe can render it;
        # the browser's built-in PDF viewer handles display.
        disposition = "inline" if self.path.endswith("?view") else f'attachment; filename="{path.name}"'
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition", disposition)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def respond_html(self, body: str) -> None:
        data = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # Suppress default server-side request logging
        pass


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Nepal compliance review tool: http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()