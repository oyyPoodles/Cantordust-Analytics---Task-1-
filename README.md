# Task 1 - Nepal Import Compliance Draft

This repository completes Task 1 from the Cantordust AI Engineer Assessment:

- Export country: China
- Import country: Nepal
- Client: SunBridge Trading Pvt. Ltd.
- Output: a clear working draft that SunBridge can share with its Nepal import agent.

No external API is used. The draft is generated from the local resource PDFs in this folder.

## Local Resources

Required files:

- `DSS_GZES230100125901_combined-1.pdf`
- `Manufacturer PDF 2 - 188_1115.pdf`
- `NEPQA 2025 (Nepal).pdf`

The two manufacturer PDFs are treated as source data. NEPQA 2025 is used only as Nepal import-side reference guidance, not as product evidence and not as a form to copy.

## How To Run

Generate the outputs directly:

```bash
python run_task1.py
```

The script validates that the required PDFs are present and writes:

- `output/compliance_draft.md`
- `output/compliance_draft.pdf`
- `output/approach_note.md`
- `output/review_checklist.md`
- `demo_script.md`

Or run the local review tool:

```bash
python app.py
```

Then open `http://127.0.0.1:8000`. The tool shows source document status, runs the generator, previews the draft, and provides download links for the Markdown and PDF outputs.

## Main Finding

The two manufacturer PDFs appear to describe different inverter product families:

- Source A covers CE-1P single-phase PV inverter models rated 300 W to 2000 W.
- Source B covers SUN-G06P3 three-phase PV inverter models rated 3 kW to 15 kW.

The draft therefore does not force the sources into one product record. It shows the mismatch clearly and lists follow-up actions for SunBridge and the Nepal import agent.

## Project Structure

```text
Task1/
  DSS_GZES230100125901_combined-1.pdf
  Manufacturer PDF 2 - 188_1115.pdf
  NEPQA 2025 (Nepal).pdf
  run_task1.py
  app.py
  README.md
  requirements.txt
  .gitignore
  demo_script.md
  output/
    compliance_draft.md
    compliance_draft.pdf
    approach_note.md
    review_checklist.md
```

## Method

1. Read Task 1 only and ignored Task 2.
2. Extracted product, manufacturer, testing, labeling, and technical information from the two manufacturer PDFs.
3. Used NEPQA 2025 only to identify Nepal-side review topics such as certificates, technical datasheets, labels, and warranty/importer documentation.
4. Compared the two sources field by field.
5. Marked conflicts, one-sided information, and gaps without guessing.

## Limitations

This is a working draft, not a final Nepal compliance filing. It does not claim the product complies with Nepal requirements. SunBridge should confirm the exact model, manufacturer relationship, certificate set, label, and warranty documentation with the manufacturer and Nepal import agent.

## Video Demo Guidance

Use `demo_script.md` for a short 3-8 minute walkthrough. Show the local PDFs, run `python app.py`, generate the report in the browser, then walk through the generated compliance draft and the mismatch/follow-up sections.
