<div align="center">

# 🇳🇵 Task 1 — Nepal Import Compliance Draft Generator

### Cantordust AI Engineer Assessment

A local compliance review tool that generates a structured Nepal import compliance draft for **SunBridge Trading Pvt. Ltd.** using manufacturer documentation and Nepal import review guidelines.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Offline](https://img.shields.io/badge/Offline-Processing-2D6A4F?style=for-the-badge)
![PDF](https://img.shields.io/badge/PDF-Report-B30B00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-Output-000000?style=for-the-badge&logo=markdown&logoColor=white)

</div>

---

## 📖 Overview

This project automates the preparation of a **Nepal Import Compliance Review Package** by analyzing manufacturer-provided documentation and organizing the findings into a structured report.

The generated package helps importers and compliance reviewers quickly understand:

- Product information
- Manufacturer details
- Technical specifications
- Certification evidence
- Labeling information
- Documentation gaps
- Recommended follow-up actions

---

## ✨ Features

- 📄 Generates a detailed compliance draft report
- 📑 Exports reports in **Markdown** and **PDF**
- 📋 Produces a review checklist
- 📝 Generates an approach note
- 🎥 Includes a demo walkthrough script
- 🌐 Local web dashboard for report generation and preview
- 🔒 Fully offline workflow
- ⚡ No external APIs required

---

## 📂 Required Documents

Place the following files in the project root directory:

```text
Resource1.pdf
Resource2.pdf
Resource3.pdf
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone <repository-url>
cd Task1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install reportlab
```

---

## 🖥️ Usage

### Generate Compliance Reports

```bash
python run_task1.py
```

Generated outputs:

```text
output/
├── compliance_draft.md
├── compliance_draft.pdf
├── approach_note.md
└── review_checklist.md
```

---

### Launch Review Dashboard

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:8000
```

### Dashboard Features

- ✅ Source document validation
- ✅ One-click report generation
- ✅ PDF preview
- ✅ Download generated outputs
- ✅ Execution logs

---

## 📁 Project Structure

```text
Task1/
│
├── run_task1.py
├── app.py
├── requirements.txt
├── README.md
│
├── Resources1.pdf
├── Resources2.pdf
├── Resources3.pdf
│
└── output/
    ├── compliance_draft.md
    ├── compliance_draft.pdf
    ├── approach_note.md
    └── review_checklist.md
```

---

## ⚙️ Workflow

```text
Source PDFs
      │
      ▼
Document Validation
      │
      ▼
Information Extraction
      │
      ▼
Compliance Review
      │
      ▼
Gap & Consistency Analysis
      │
      ▼
Report Generation
```

---

## 📦 Generated Outputs

### 📄 Compliance Draft

A structured compliance review containing:

- Product Identification
- Manufacturer Information
- Technical Specifications
- Certification & Testing Evidence
- Labeling Review
- Consistency Checks
- Documentation Gaps
- Recommended Follow-Up Actions

### 📝 Approach Note

Summarizes the methodology used to prepare the compliance review.

### ✅ Review Checklist

Provides a final verification checklist before submission to the Nepal import agent.

### 🎥 Demo Script

Guides a short project walkthrough and demonstration.

---

## 🔧 Technology Stack

| Component | Technology |
|------------|------------|
| Backend | Python |
| PDF Generation | ReportLab |
| Dashboard | Python HTTP Server |
| Outputs | Markdown, PDF |
| Processing | Local / Offline |

---

## ⚠️ Disclaimer

This project generates a **working compliance review draft** intended to support discussions with the Nepal import agent.

The generated outputs:

- Do **not** constitute legal advice.
- Do **not** guarantee regulatory approval.
- Do **not** replace official review by relevant authorities.

Final compliance decisions remain the responsibility of the importer and regulatory reviewers.

---

## 🎯 Assessment Scope

This repository implements:

**Task 1 — China → Nepal Import Compliance Review**

for the **Cantordust AI Engineer Assessment**.

---

<div align="center">

Built for the Cantordust AI Engineer Assessment

</div>
