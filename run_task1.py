"""
Task 1 - Nepal Import Compliance Draft Generator

No API version. This script uses facts extracted from the local PDFs in this
folder and writes the Task 1 deliverables to output/.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

SOURCE_A = "DSS_GZES230100125901_combined-1.pdf"
SOURCE_B = "Manufacturer PDF 2 - 188_1115.pdf"
NEPQA = "NEPQA 2025 (Nepal).pdf"


def timestamp_npt() -> str:
    npt = timezone(timedelta(hours=5, minutes=45))
    return datetime.now(npt).strftime("%Y-%m-%d %H:%M:%S NPT")


def validate_inputs() -> None:
    missing = [name for name in (SOURCE_A, SOURCE_B, NEPQA) if not (BASE_DIR / name).exists()]
    if missing:
        joined = "\n  - ".join(missing)
        raise SystemExit(f"Missing required PDF(s):\n  - {joined}")


COMPLIANCE_DRAFT = """# Nepal Import Compliance Draft

Prepared for: SunBridge Trading Pvt. Ltd.  
Prepared by: Cantordust Analytics  
Status: Working Draft - For Import Agent Review  
Sources: DSS_GZES230100125901_combined-1.pdf; Manufacturer PDF 2 - 188_1115.pdf; NEPQA 2025 (Nepal) used as import-side reference only

## 1. Document Purpose and Scope

This working draft summarizes the available China manufacturer paperwork for a proposed Nepal import of grid-connected photovoltaic inverters by SunBridge Trading Pvt. Ltd. It is based on two manufacturer PDFs and uses NEPQA 2025 only as a rough import-side reference for topics Nepal reviewers commonly ask about, such as product identity, test evidence, technical ratings, labeling, and importer documentation.

This draft does not determine Nepal compliance. Final review, acceptance, and document naming should be confirmed by SunBridge's Nepal import agent and the relevant Nepal authorities.

## 2. Product Identification

**Important finding: the two manufacturer PDFs appear to describe different inverter product families, not simply the same product in two formats. Source A covers single-phase CE-1P models rated 300 W to 2000 W. Source B covers three-phase SUN-G06P3 models rated 3 kW to 15 kW. SunBridge should confirm which exact model family and variant is being imported before this file is used as a compliance package.**

| Field | Source A - DSS_GZES230100125901_combined-1.pdf | Source B - Manufacturer PDF 2 - 188_1115.pdf |
|---|---|---|
| Document type | Test Report, IEC/EN 62109-1 | Certificate of Conformity (COC) |
| Product type | Grid-connected PV inverter / single phase inverter | Grid-connected PV inverter |
| Model family | CE-1P series | SUN-G06P3-EU-AM2 and SUN-G06P3-EU-AM2-P1 series - **MISMATCH** |
| Models listed | CE-1P3001G-230-EU, CE-1P5001G-230-EU, CE-1P6001G-230-EU, CE-1P8001G-230-EU, CE-1P10001G-230-EU, CE-1P13001G-230-EU, CE-1P16001G-230-EU, CE-1P18001G-230-EU, CE-1P20001G-230-EU | SUN-3K/4K/5K/6K/7K/8K/9K/10K/12K/15K-G06P3-EU-AM2 and matching AM2-P1 variants - **MISMATCH** |
| Rated output power range | 300 W, 500 W, 600 W, 800 W, 1000 W, 1300 W, 1600 W, 1800 W, 2000 W | 3 kW, 4 kW, 5 kW, 6 kW, 7 kW, 8 kW, 9 kW, 10 kW, 12 kW, 15 kW - **MISMATCH** |
| Phase configuration | Single phase inverter; rated grid voltage 230 V | Three-phase notation: 3L/N/PE 230/400 V - **MISMATCH** |
| Installation type | Indoor or outdoor installation | Not stated |
| Transformer topology | Transformerless | Transformerless |
| Variant note | Other tests mainly on CE-1P20001G-230-EU except mains supply electrical data for all models | AM2 and AM2-P1 differ in maximum input current and maximum short-circuit current |

The paperwork should not be treated as one clean product file yet. Source A appears to be a safety test report for a single-phase low-power CE-1P inverter family, while Source B is a later certificate for a three-phase Deye SUN-G06P3 inverter family. The files may both relate to PV inverters from China, but they do not currently establish a single confirmed model or variant for Nepal import review.

## 3. Manufacturer Information

| Field | Source A | Source B |
|---|---|---|
| Applicant / certificate holder | Zhejiang CHISAGE New Energy Technology Co., Ltd | NingBo Deye Inverter Technology Co., Ltd - **MISMATCH** |
| Manufacturer named in document | Zhejiang CHISAGE New Energy Technology Co., Ltd | Not separately stated; certificate holder is NingBo Deye Inverter Technology Co., Ltd - **MISMATCH** |
| Applicant / holder address | No. 1828 Fuqing South RD. Panhuo ST. Yinzhou District Ningbo Zhejiang 315000 China | No. 26 South YongJiang Road, Daqi, Beilun, NingBo, China - **MISMATCH** |
| Factory address | NingBo Deye Inverter Technology Co., Ltd., No.26 South YongJiang Road, Daqi, Beilun, NingBo, China | Not stated separately; same address stated for certificate holder |
| Country of manufacture / origin | China, inferred from stated manufacturer/factory addresses | China, inferred from stated certificate holder address |
| Testing laboratory | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch |
| Testing laboratory address | 198 Kezhu Road, Science City, Economic & Technology Development Area, Guangzhou, Guangdong, China | Not stated in Source B |
| Certification body / issuer | Test report issued under SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch responsibility | SGS Testing & Control Services Singapore Pte Ltd |
| Website / contact | SGS terms URL appears in report disclaimer; manufacturer website/contact not stated | SGS terms URL appears in certificate disclaimer; manufacturer website/contact not stated |

The manufacturer chain needs clarification. Source A names Zhejiang CHISAGE New Energy Technology Co., Ltd. as applicant/manufacturer and separately names NingBo Deye Inverter Technology Co., Ltd. as a factory. Source B names NingBo Deye Inverter Technology Co., Ltd. as certificate holder. This may be explainable commercially, but it should be confirmed before submission.

## 4. Key Technical Specifications

### DC Input

| Specification | Source A | Source B |
|---|---|---|
| Product family | CE-1P single-phase series | SUN-G06P3 three-phase series - **MISMATCH** |
| Recommended / maximum PV input power | 400 W, 600 W, 800 W, 1200 W, 1200 W, 1600 W, 2400 W, 2400 W, 2400 W by listed model | 3.9 kW, 5.2 kW, 6.5 kW, 7.8 kW, 9.1 kW, 10.4 kW, 11.7 kW, 13 kW, 15.6 kW, 19.5 kW by listed model - **MISMATCH** |
| Maximum input voltage | 60 V | 1100 V - **MISMATCH** |
| Start-up operating voltage | Not stated | 140 V |
| Rated input voltage | Not stated | 600 V |
| MPPT operating voltage range | 25-55 V | 120-1000 V - **MISMATCH** |
| Full-power MPPT voltage range | Not stated | 350-850 V for 3 kW to 6 kW models; 480-850 V for 7 kW to 15 kW models |
| Maximum input current | 13 A; 13 A x 2; or 13 A x 4 depending on CE-1P model | AM2-P1: 20+20 A except 15 kW is 20+26 A. AM2: 13+13 A except 15 kW is 13+26 A - **MISMATCH** |
| Maximum short-circuit current | Not stated | AM2-P1: 30+30 A except 15 kW is 30+39 A. AM2: 19.5+19.5 A except 15 kW is 19.5+39 A |

### AC Output

| Specification | Source A | Source B |
|---|---|---|
| Rated grid / nominal grid voltage | 230 V | 3L/N/PE 230/400 V - **MISMATCH** |
| Rated / nominal grid frequency | 50 Hz | 50/60 Hz |
| Rated output / AC power | 300 W to 2000 W by listed model | 3 kW to 15 kW by listed model - **MISMATCH** |
| Maximum AC power | Not stated | 3.3 kW, 4.4 kW, 5.5 kW, 6.6 kW, 7.7 kW, 8.8 kW, 9.9 kW, 11 kW, 13.2 kW, 16.5 kW |
| Rated output / AC current | 1.3 A, 2.2 A, 2.6 A, 3.8 A, 4.8 A, 6.2 A, 7.7 A, 8.6 A, 9.6 A | 4.4 A, 5.8 A, 7.3 A, 8.7 A, 10.2 A, 11.6 A, 13.1 A, 14.5 A, 17.4 A, 21.8 A - **MISMATCH** |
| Maximum AC current | Not stated | 4.8 A, 6.4 A, 8.0 A, 9.6 A, 11.2 A, 12.8 A, 14.4 A, 16.0 A, 19.2 A, 24.0 A |
| Power factor | >0.99 | 0.8 leading to 0.8 lagging - **MISMATCH** |
| THD | Not stated | Not stated |

### Efficiency

| Specification | Source A | Source B |
|---|---|---|
| Peak inverter efficiency | Not stated | Not stated |
| Euro / weighted efficiency | Not stated | Not stated |
| MPPT efficiency | Not stated | Not stated |
| Efficiency curve | Not stated | Not stated |
| No-load loss | Not stated | Not stated |

### Protection and Ratings

| Specification | Source A | Source B |
|---|---|---|
| Ingress protection | IP67 | IP65 - **MISMATCH** |
| Protective class | Class I | Class I |
| Pollution degree | Outside PD3; Inside PD2 | Not stated |
| Overvoltage category | Shown in checklist format, but selected category is not clearly extractable from text | Not stated |
| Environmental category | Outdoor indicated in text extraction; indoor options also appear in checklist text, so final selection should be confirmed visually | Not stated |
| Tested power system | TN systems | Not stated |
| Backfeed / single fault / electrical ratings tests | Clauses listed as pass in IEC/EN 62109-1 report | Not stated in certificate |
| Reverse polarity indication / DC terminal polarity marking | "+" and "-" marking provided adjacent to DC input terminal | Not stated |
| Cooling method | Not stated | Free cooling |
| Topology | Transformerless | Transformerless |

### Physical

| Specification | Source A | Source B |
|---|---|---|
| Mass / weight | 3.5 kg for all model | Not stated |
| Dimensions | Not stated | Not stated |
| Operating temperature | -40 deg C to 65 deg C | -25 deg C to 60 deg C, derating above 45 deg C - **MISMATCH** |
| Storage temperature | Not stated | Not stated |
| Humidity range | Not stated | Not stated |
| Installation / mobility | Fixed equipment appears selected; indoor or outdoor installation described | Not stated |

## 5. Test and Certification Information

| Certification / Standard | Mentioned In | Number / Code | Issuing Body |
|---|---|---|---|
| IEC/EN 62109-1 safety test report | Source A | Report No. GZES230100125901; date of issue 2023-02-01 | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch |
| EN 62109-1:2010 | Source A | Test specification standard | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch |
| IEC 62109-1:2010 First Edition | Source A | Test specification standard | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch |
| IEC62109_1B Test Report Form | Source A | TRF No. IEC62109_1B; Master TRF dated 2016-04 | VDE Testing and Certification Institute named as TRF originator |
| Original report reference | Source A | GZES210602035101 | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch stated in summary |
| Certificate of Conformity | Source B | Certificate No. PCS-24-1022; original issue 2024-03-26; expiry 2027-03-25 | SGS Testing & Control Services Singapore Pte Ltd |
| IEC 62116:2014 | Source B | Test standard on certificate | SGS Testing & Control Services Singapore Pte Ltd, with SGS-CSTC Guangzhou as test laboratory |
| IEC 61727:2004 | Source B | Test standard on certificate | SGS Testing & Control Services Singapore Pte Ltd, with SGS-CSTC Guangzhou as test laboratory |
| Testing reports for Source B | Source B | GZES220300424901 and GZES220300424902, both dated 2023-12-02, Amendment 01 dated 2024-03-05 | SGS-CSTC Standards Technical Services Co., Ltd. Guangzhou Branch |
| ISO/IEC 17065:2012 | Source B | Certificate states product is certified according to ISO/IEC 17065:2012 | SGS Testing & Control Services Singapore Pte Ltd |
| IEC 62109-2:2011 | NEPQA reference only | Expected topic for PV inverter import review; not found in either manufacturer PDF | Not stated in Source A or Source B |
| IEC 62891:2020 | NEPQA reference only | Expected topic for MPPT efficiency; not found in either manufacturer PDF | Not stated in Source A or Source B |

Based on NEPQA 2025's PV inverter section, Nepal import review may look for PV inverter test certificates covering IEC 61727, IEC 62116, IEC 62891, and IEC 62109-1 / IEC 62109-2, plus importer-manufacturer warranty documentation and a catalogue or technical datasheet. The current source set contains IEC/EN 62109-1 evidence in Source A and IEC 62116 / IEC 61727 evidence in Source B, but those are attached to apparently different model families. No Nepal-specific approval, IEC 62109-2 certificate, IEC 62891 evidence, importer-manufacturer warranty agreement, or complete single-model technical datasheet was found in the two manufacturer PDFs.

## 6. Labeling Review

Source A includes a representative marking plate page and marking/documentation clauses. The text extraction confirms that the label is attached on the side surface of the enclosure and visible after installation. Source A also states that labels for other models are the same as CE-1P20001G-230-EU except for rating parameters. It says the marking plate is on the outer surface of the enclosure, model identification is marked, input and output ratings are on the rating plate, IP rating is on the rating plate, the "+" and "-" polarity marks are provided near the DC input terminal, PE/protective conductor markings are present, warning markings met minimum size checks, and a hot-surface warning symbol is provided on the marking plate.

Source A further states that importer and manufacturer name, registered trade name or trademark, and postal address would be marked on products before being placed on the market, with contact details in a language easily understood by end users and market surveillance authorities. That is a declaration about intended production marking; it is not the same as a final Nepal import label photograph for the exact imported model.

Source B does not include a label photograph, label specification sheet, nameplate image, serial-number marking, warning-symbol details, label dimensions, or language information. It provides product ratings in certificate appendix tables, but not final physical labeling evidence.

NEPQA 2025's PV inverter section suggests Nepal-side reviewers commonly care about label topics such as manufacturer name, brand/model/type, rated power, input and output voltage and frequency, maximum input voltage, MPPT voltage range, and serial number. Source A covers several of these in a representative safety-marking context for CE-1P models. Source B provides many rating fields but does not show a label. Neither PDF provides a confirmed final label for the exact model SunBridge plans to import into Nepal.

## 7. Consistency Check - Mismatches and Gaps

### CONFLICTS

| Field | Source A value | Source B value |
|---|---|---|
| Product family | CE-1P series | SUN-G06P3-EU-AM2 / AM2-P1 series |
| Phase configuration | Single phase inverter; 230 V | Three-phase notation 3L/N/PE 230/400 V |
| Rated output power range | 300 W to 2000 W | 3 kW to 15 kW |
| Manufacturer / holder | Zhejiang CHISAGE New Energy Technology Co., Ltd as applicant/manufacturer; NingBo Deye listed as factory | NingBo Deye Inverter Technology Co., Ltd as certificate holder |
| Maximum input voltage | 60 V | 1100 V |
| MPPT voltage range | 25-55 V | 120-1000 V |
| Rated / nominal grid frequency | 50 Hz | 50/60 Hz |
| Power factor | >0.99 | 0.8 leading to 0.8 lagging |
| IP rating | IP67 | IP65 |
| Operating temperature | -40 deg C to 65 deg C | -25 deg C to 60 deg C, derating above 45 deg C |
| Test evidence family | IEC/EN 62109-1 report for CE-1P models | IEC 62116 / IEC 61727 COC for SUN-G06P3 models |

### ONE-SIDED INFORMATION

| Field | Present in | Note |
|---|---|---|
| Source A report number and issue date | Source A only | GZES230100125901, issued 2023-02-01 |
| Source B certificate number and expiry | Source B only | PCS-24-1022, issued 2024-03-26, expires 2027-03-25 |
| Factory declaration | Source A only | NingBo Deye factory address appears in Source A |
| Hardware / software versions | Source A only | Hardware Ver2.3; DC software Ver0107; AC software Ver2.5 |
| Weight | Source A only | 3.5 kg for all models |
| Pollution degree | Source A only | Outside PD3; Inside PD2 |
| Tested power systems | Source A only | TN systems |
| Marking plate / label placement evidence | Source A only | Representative marking plate, side-surface placement, warning marking checks |
| Start-up voltage / rated input voltage | Source B only | 140 V start-up; 600 V rated input |
| Full-power MPPT range | Source B only | 350-850 V or 480-850 V depending model range |
| Maximum AC power and maximum AC current | Source B only | Listed for SUN models |
| Cooling method | Source B only | Free cooling |
| AM2 vs AM2-P1 variant distinction | Source B only | Difference is maximum input current and maximum short-circuit current |

### GAPS - INFORMATION NOT FOUND IN EITHER SOURCE

| Gap | Why it matters for Nepal import review |
|---|---|
| Confirmed exact model and variant to be imported | The two sources appear to describe different product families; Nepal review should be tied to the actual shipment model. |
| Single complete certificate set for one confirmed model family | NEPQA-style review may expect relevant PV inverter certificates for the actual model, not mixed evidence from different product families. |
| IEC 62109-2 evidence | NEPQA 2025 references IEC 62109-1 and IEC 62109-2 for PV inverter safety; only IEC/EN 62109-1 was found in Source A. |
| IEC 62891 / MPPT efficiency evidence | NEPQA 2025 references MPPT efficiency testing; neither manufacturer PDF gives IEC 62891 evidence or MPPT efficiency figures. |
| Efficiency values and efficiency curve | NEPQA 2025 flags inverter and Euro efficiency; neither PDF provides peak efficiency, Euro efficiency, or an efficiency curve. |
| THD, flicker, DC injection, voltage/frequency operating range, anti-islanding details for the exact model | NEPQA 2025 points to grid interface topics; Source B has IEC 62116 / IEC 61727 certificate evidence, but not detailed values in the certificate pages. |
| Importer-manufacturer warranty agreement | NEPQA 2025 says a local importer should provide an agreement with the principal manufacturer stating PV inverter warranty period. |
| Catalogue / full technical datasheet for the exact import model | NEPQA 2025 expects catalogue and technical datasheet; the available files are a safety test report and COC, not a complete datasheet package. |
| Final label photo or label artwork for the exact imported model | Source A has representative marking evidence; Source B has no label image; neither confirms final Nepal-shipment label for the exact model. |
| Serial-number format for Source B models | NEPQA label topics include serial number; Source B does not show serial-number labeling. |
| Warranty period | NEPQA 2025 references PV inverter warranty expectations; no warranty period is stated in either manufacturer PDF. |
| Dimensions and storage/humidity limits | Useful for technical file completeness; not stated in either source. |

## 8. Items Pending or Requiring Follow-up

1. Ask SunBridge and the factory to confirm the exact model number, model family, phase configuration, and variant being imported into Nepal.
2. Resolve whether the CE-1P safety test report and SUN-G06P3 certificate are meant to support the same shipment. If yes, request a written explanation from the manufacturer linking the two document sets; if no, separate the compliance file by product family.
3. Obtain a complete certificate set for the confirmed import model, especially evidence for IEC 62109-1, IEC 62109-2, IEC 61727, IEC 62116, and IEC 62891 where applicable to the Nepal import review.
4. Request the complete technical datasheet or catalogue for the exact model and variant, including efficiency, Euro efficiency, MPPT efficiency, THD, operating grid ranges, protection functions, dimensions, storage temperature, and humidity range.
5. Request a final label photograph or label artwork for the exact imported model, including manufacturer name, brand/model/type, rated power, input/output voltage and frequency, maximum input voltage, MPPT range, serial number, warning symbols, and label language.
6. Ask for the importer-manufacturer agreement or warranty letter required for Nepal-side review, including the warranty period and authorized signatures/stamps.
7. Clarify the manufacturer relationship between Zhejiang CHISAGE New Energy Technology Co., Ltd and NingBo Deye Inverter Technology Co., Ltd, including which entity is the principal manufacturer for SunBridge's shipment.
8. Ask the Nepal import agent whether the SGS certificate body and laboratory documents are acceptable for the relevant NEPQA-style review, and whether CBTL/NCB/IECEE/IECRE listing evidence must be attached.
9. Keep this draft marked as a working draft until the above model, certification, label, and warranty gaps are resolved.

## 9. Preparer's Note

The two source PDFs reviewed here appear to contain a 72-page SGS IEC/EN 62109-1 safety test report for CE-1P single-phase inverter models and a 4-page SGS Certificate of Conformity for Deye SUN-G06P3 three-phase inverter models. NEPQA 2025 was used only to identify the import-side topics SunBridge's Nepal agent may ask about; it was not used as product source data and was not copied as a form. The main limitation is that the two manufacturer PDFs do not currently line up as one confirmed model file, so SunBridge should treat this draft as a structured starting point for discussion with its import agent and manufacturer rather than a final compliance filing.
"""


APPROACH_NOTE = """# Approach Note

I completed Task 1 only: China to Nepal.

## How I approached the work

1. Read the Task 1 brief and treated NEPQA 2025 as an import-side reference, not as product evidence.
2. Reviewed the two manufacturer PDFs as source data:
   - Source A: DSS_GZES230100125901_combined-1.pdf
   - Source B: Manufacturer PDF 2 - 188_1115.pdf
3. Extracted product identity, manufacturer details, test/certification evidence, ratings, labeling evidence, and missing items.
4. Compared the sources field by field instead of merging them into one assumed product.
5. Built the draft around the central risk: the two PDFs appear to describe different inverter families.

## Main judgement call

I did not try to force the two PDFs into one product record. Source A is a single-phase CE-1P safety test report up to 2 kW. Source B is a three-phase SUN-G06P3 certificate from 3 kW to 15 kW. The honest output for SunBridge is therefore a working Nepal import draft plus a clear follow-up list.

## Limitations

The draft is not a legal or regulatory opinion. It does not assert Nepal compliance. It identifies what is present, what conflicts, and what SunBridge should ask the manufacturer/import agent to confirm.
"""


REVIEW_CHECKLIST = """# Review Checklist

Use this checklist before sending the file to SunBridge or a Nepal import agent.

- [ ] Confirm exact model and variant being imported.
- [ ] Confirm whether Source A and Source B are intended to support the same shipment.
- [ ] Resolve single-phase CE-1P vs three-phase SUN-G06P3 mismatch.
- [ ] Confirm principal manufacturer and factory relationship.
- [ ] Obtain certificates for the exact model family.
- [ ] Check whether IEC 62109-2 evidence is required.
- [ ] Check whether IEC 62891 / MPPT efficiency evidence is required.
- [ ] Obtain complete datasheet or catalogue for the exact model.
- [ ] Obtain final label photo/artwork for the exact model.
- [ ] Obtain importer-manufacturer warranty agreement or warranty letter.
- [ ] Ask the Nepal import agent to confirm document names, authority expectations, and acceptable certification bodies.
"""


DEMO_SCRIPT = """# 3-8 Minute Video Demo Script

1. Show the Task 1 brief and explain that only the Nepal task was completed.
2. Show the three local PDFs in the project folder.
3. Explain the method: manufacturer PDFs were treated as source data; NEPQA 2025 was used only as Nepal import-side guidance.
4. Open `output/compliance_draft.md`.
5. Highlight the central finding: Source A and Source B appear to describe different inverter families.
6. Walk through the comparison tables for product identity, manufacturer information, specifications, certificates, and labeling.
7. Show Section 7 and Section 8, which make mismatches and follow-up items easy for SunBridge's import agent to review.
8. Show `output/approach_note.md` and `output/review_checklist.md`.
9. Run `python run_task1.py` to demonstrate the no-API generator recreates the outputs from the local project facts.
"""


# ── Black and white palette ───────────────────────────────────────────────────
BLACK      = colors.black
DARK_GREY  = colors.HexColor("#222222")
MID_GREY   = colors.HexColor("#555555")
RULE_GREY  = colors.HexColor("#999999")
HDR_BG     = colors.HexColor("#DDDDDD")   # table header fill
ALT_BG     = colors.HexColor("#F5F5F5")   # alternating row fill
MM_BG      = colors.HexColor("#EEEEEE")   # mismatch row fill (light grey)
BORDER     = colors.HexColor("#BBBBBB")
SURFACE    = colors.white
BG         = colors.white


def build_styles():
    base = getSampleStyleSheet()
    normal_font = "Helvetica"
    bold_font   = "Helvetica-Bold"

    def S(name, parent="Normal", **kw):
        kw.setdefault("fontName", normal_font)
        kw.setdefault("textColor", BLACK)
        return ParagraphStyle(name, parent=base[parent], **kw)

    return {
        "meta":    S("meta",    fontSize=8,  textColor=MID_GREY, leading=13),
        "h1":      S("h1",      fontSize=16, fontName=bold_font, textColor=BLACK,
                               leading=22, spaceAfter=4),
        "h2":      S("h2",      fontSize=11, fontName=bold_font, textColor=BLACK,
                               leading=16, spaceBefore=14, spaceAfter=4),
        "h3":      S("h3",      fontSize=9,  fontName=bold_font, textColor=BLACK,
                               leading=14, spaceBefore=8, spaceAfter=2),
        "body":    S("body",    fontSize=9,  leading=14, spaceAfter=6),
        "warning": S("warning", fontSize=9,  leading=14, spaceAfter=6,
                               textColor=BLACK, fontName=bold_font),
        "li":      S("li",      fontSize=9,  leading=14, leftIndent=14,
                               spaceAfter=3, firstLineIndent=-10),
        "th":      S("th",      fontSize=8,  fontName=bold_font,
                               textColor=BLACK, leading=11),
        "td":      S("td",      fontSize=8,  leading=11, textColor=BLACK),
        "td_mm":   S("td_mm",   fontSize=8,  leading=11, textColor=BLACK,
                               fontName=bold_font),
    }


def _escape(text: str) -> str:
    """Minimal XML escaping for ReportLab paragraphs."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _para_style(text: str, styles: dict) -> str:
    """Pick body vs warning style name based on content."""
    return "warning" if "**MISMATCH**" in text or "MISMATCH" in text else "body"


def _inline_bold(text: str, styles: dict, style_name: str = "body") -> Paragraph:
    """Convert **bold** markers to <b> tags inside a Paragraph."""
    escaped = _escape(text)
    # Replace **text** with <b>text</b>
    formatted = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    # Pick red style if MISMATCH is mentioned
    if "MISMATCH" in text:
        style_name = "warning"
    return Paragraph(formatted, styles[style_name])


def parse_markdown_to_flowables(markdown_text: str, styles: dict) -> list:
    """
    Convert the draft markdown into ReportLab flowables:
    headings, body paragraphs, markdown tables, and numbered/bullet lists.
    """
    story = []
    lines = markdown_text.splitlines()
    i = 0
    PAGE_W = A4[0] - 2 * 20 * mm  # usable width after margins

    while i < len(lines):
        line = lines[i]

        # Skip generator comment
        if line.startswith("<!--"):
            i += 1
            continue

        # Blank line
        if not line.strip():
            i += 1
            continue

        # H1
        if line.startswith("# ") and not line.startswith("## "):
            story.append(Paragraph(_escape(line[2:].strip()), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=1,
                                    color=BLACK, spaceAfter=6))
            i += 1
            continue

        # H2
        if line.startswith("## ") and not line.startswith("### "):
            story.append(Paragraph(_escape(line[3:].strip()), styles["h2"]))
            i += 1
            continue

        # H3
        if line.startswith("### "):
            story.append(Paragraph(_escape(line[4:].strip()), styles["h3"]))
            i += 1
            continue

        # Metadata block (lines like "Key: Value" right after H1)
        if ": " in line and not line.startswith("|") and not line.startswith("-"):
            story.append(Paragraph(_escape(line.strip()), styles["meta"]))
            i += 1
            continue

        # Numbered list item
        if re.match(r'^\d+\.\s', line):
            num, _, rest = line.partition(". ")
            text = f"{num}.  {rest.strip()}"
            story.append(_inline_bold(text, styles, "li"))
            i += 1
            continue

        # Bullet / checkbox list item
        if line.strip().startswith("- "):
            text = line.strip()[2:]
            story.append(_inline_bold("• " + text, styles, "li"))
            i += 1
            continue

        # Markdown table — collect all rows
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1

            # Drop separator row (---|---)
            data_lines = [l for l in table_lines
                          if not re.match(r'^\|[-| :]+\|$', l)]

            table_data = []
            is_mismatch_row = []
            for tl in data_lines:
                cells = [c.strip() for c in tl.strip().strip("|").split("|")]
                row_has_mismatch = any("MISMATCH" in c for c in cells)
                is_mismatch_row.append(row_has_mismatch)
                table_data.append(cells)

            if not table_data:
                continue

            # Determine column count and widths
            ncols = max(len(row) for row in table_data)
            # Pad short rows
            table_data = [row + [""] * (ncols - len(row)) for row in table_data]

            # Build Paragraph cells
            col_width = PAGE_W / ncols
            para_data = []
            for r_idx, row in enumerate(table_data):
                is_header = r_idx == 0
                para_row = []
                for c_idx, cell in enumerate(row):
                    raw = cell.replace("**MISMATCH**", "MISMATCH")
                    escaped = _escape(raw)
                    formatted = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
                    if is_header:
                        p = Paragraph(formatted, styles["th"])
                    elif "MISMATCH" in raw:
                        p = Paragraph(formatted, styles["td_mm"])
                    else:
                        p = Paragraph(formatted, styles["td"])
                    para_row.append(p)
                para_data.append(para_row)

            col_widths = [col_width] * ncols

            tbl = Table(para_data, colWidths=col_widths, repeatRows=1)

            # Row commands
            row_cmds = [
                # Header row — light grey background, black bold text
                ("BACKGROUND",    (0, 0), (-1, 0), HDR_BG),
                ("TEXTCOLOR",     (0, 0), (-1, 0), BLACK),
                ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, 0), 8),
                ("TOPPADDING",    (0, 0), (-1, 0), 5),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                # Body rows
                ("FONTSIZE",      (0, 1), (-1, -1), 8),
                ("TOPPADDING",    (0, 1), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
                ("LEFTPADDING",   (0, 0), (-1, -1), 6),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
                ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SURFACE, ALT_BG]),
            ]

            # Mismatch rows — slightly darker grey, bold text (already set via td_mm style)
            for r_idx, has_mm in enumerate(is_mismatch_row):
                if has_mm and r_idx > 0:
                    row_cmds.append(("BACKGROUND", (0, r_idx), (-1, r_idx), MM_BG))

            tbl.setStyle(TableStyle(row_cmds))
            story.append(tbl)
            story.append(Spacer(1, 6))
            continue

        # Regular paragraph
        story.append(_inline_bold(line.strip(), styles, "body"))
        i += 1

    return story


def build_pdf_cover(story: list, title: str, subtitle: str,
                    meta_lines: list[str], styles: dict) -> None:
    """Prepend a cover block to the story list."""
    cover = [
        Spacer(1, 8 * mm),
        Paragraph(_escape(title), styles["h1"]),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8),
    ]
    for m in meta_lines:
        cover.append(Paragraph(_escape(m), styles["meta"]))
    cover.append(Spacer(1, 4 * mm))
    story[:0] = cover


def _page_footer(canvas, doc):
    """Draw page number and a thin rule at the bottom of every page."""
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MID_GREY)
    w, h = A4
    canvas.setStrokeColor(RULE_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, 14 * mm, w - 20 * mm, 14 * mm)
    canvas.drawString(20 * mm, 10 * mm, "Nepal Import Compliance Draft — SunBridge Trading Pvt. Ltd. — Working Draft")
    canvas.drawRightString(w - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def write_pdf_from_markdown(markdown_path: Path, pdf_path: Path) -> None:
    """Render a polished PDF from the generated markdown using ReportLab."""
    source = markdown_path.read_text(encoding="utf-8")
    styles = build_styles()

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title="Nepal Import Compliance Draft",
        author="Cantordust Analytics",
        subject="SunBridge Trading Pvt. Ltd. — PV Inverter Import Review",
    )

    story = parse_markdown_to_flowables(source, styles)
    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)


def write_file(name: str, content: str) -> None:
    header = f"<!-- Generated locally for Task 1 on {timestamp_npt()} -->\n\n"
    (OUTPUT_DIR / name).write_text(header + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    validate_inputs()
    OUTPUT_DIR.mkdir(exist_ok=True)
    write_file("compliance_draft.md", COMPLIANCE_DRAFT)
    write_file("approach_note.md", APPROACH_NOTE)
    write_file("review_checklist.md", REVIEW_CHECKLIST)
    write_pdf_from_markdown(
        OUTPUT_DIR / "compliance_draft.md",
        OUTPUT_DIR / "compliance_draft.pdf",
    )
    (BASE_DIR / "demo_script.md").write_text(DEMO_SCRIPT.strip() + "\n", encoding="utf-8")
    print("Task 1 outputs generated:")
    print(f"  {OUTPUT_DIR / 'compliance_draft.md'}")
    print(f"  {OUTPUT_DIR / 'compliance_draft.pdf'}")
    print(f"  {OUTPUT_DIR / 'approach_note.md'}")
    print(f"  {OUTPUT_DIR / 'review_checklist.md'}")
    print(f"  {BASE_DIR / 'demo_script.md'}")


if __name__ == "__main__":
    main()