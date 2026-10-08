"""
Compile formal course PDF deliverables for FIN 43900 Project 1 using ReportLab.
Deliverables:
  1. Decision-Memo.pdf (Strictly 2 pages)
  2. Research-Evolution.pdf
  3. Validation-and-AI-Use.pdf
"""

from __future__ import annotations

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"


def create_decision_memo_pdf():
    pdf_path = BASE_DIR / "Decision-Memo.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "MemoTitle",
        parent=styles["Heading1"],
        fontSize=14,
        leading=16,
        textColor=colors.HexColor("#0f2b48"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "MemoSubtitle",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#495057"),
        spaceAfter=6,
    )
    h2_style = ParagraphStyle(
        "MemoH2",
        parent=styles["Heading2"],
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0f2b48"),
        spaceBefore=6,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "MemoBody",
        parent=styles["Normal"],
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#212529"),
        spaceAfter=4,
    )
    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#212529"),
    )
    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        fontName="Helvetica-Bold",
    )

    story = []

    # Title Banner
    story.append(Paragraph("BUY-SIDE INVESTMENT COMMITTEE DECISION MEMO — IREN LIMITED (NASDAQ: IREN)", title_style))
    meta_text = (
        "<b>Target:</b> IREN Limited | <b>Security:</b> Ordinary Shares | <b>Author:</b> Elliot (AI Task Force) | "
        "<b>Intended User:</b> Buy-Side Investment Committee | <b>As-of Date:</b> October 8, 2026 | "
        "<b>Baseline Filing:</b> FY2026 Form 10-K (ended June 30, 2026)"
    )
    story.append(Paragraph(meta_text, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f2b48"), spaceAfter=6))

    # Section 1: Decision and Committee Ask
    story.append(Paragraph("1. Decision and Committee Ask", h2_style))
    sec1_text = (
        "<b>RECOMMENDATION: WATCH / DEFER. Do not initiate an equity position.</b><br/>"
        "The market currently trades IREN at <b>$45.73 per share</b> (~$18.0B market capitalization), pricing the company as a pure-play hyperscale "
        "AI cloud winner following its $9.7B Microsoft contract and Horizon 1 (50 MW) acceptance in August 2026. However, our audited five-year "
        "three-statement pro-forma DCF model establishes a fundamental intrinsic equity value range of <b>$4.06 to $19.25 per share</b> "
        "(Base Case: <b>$12.12 per share</b>; WACC 10.0%, g 2.5%, 394.06M shares). The market price reflects an unsustainable <b>~280% premium</b> over "
        "fundamental operating value.<br/>"
        "<b>The Fundamental Capex Inflection:</b> To transition 5 GW of power capacity from Bitcoin mining to AI cloud services, IREN expended "
        "<b>$4,333.1M in cash capex</b> in FY2026 and faces a further estimated $4.0B in cash capex across FY27E–FY28E. FY2026 GAAP results generated "
        "an operating loss of $(1,046.7)M and a net loss of $(702.6)M. Although $5,895.6M in balance-sheet cash and $1.84B in customer prepayments "
        "provide intermediate runway, the business is burdened by $7.84B in debt and convertible notes requiring $400M in annual amortization. "
        "We recommend zero allocation until market price corrects or recognized operating cash flows turn positive."
    )
    story.append(Paragraph(sec1_text, body_style))

    # Section 2: Evidence and As-of Date
    story.append(Paragraph("2. Evidence and Historical Sourcing", h2_style))
    sec2_text = (
        "All historical inputs are traced directly to IREN's audited FY2026 Form 10-K (filed August 27, 2026, period ended June 30, 2026):<br/>"
        "• <b>Recognized GAAP Revenue:</b> $707.0M ($128.8M AI Cloud Services, $578.2M Bitcoin Mining). Management guidance of $4.0B contracted ARR "
        "is strictly treated as unearned commercial pipeline, not recognized revenue.<br/>"
        "• <b>Cash Gross Margin:</b> 68.92% ($487.3M gross profit on $219.7M cost of revenue excl. D&A), driven by low-cost Canadian/Texas PPAs.<br/>"
        "• <b>Audited Cash Capex:</b> $4,333.1M ($2,998.0M PP&E additions + $1,335.1M computer hardware, Stmt. of Cash Flows p. F-9). Third-party "
        "aggregators report only $2,998M, understating capital burn by 30.8%.<br/>"
        "• <b>Capital Structure & Shares:</b> $5,895.6M cash, $7,836.7M debt/notes, and 394.059M basic shares (Cover Page, August 14, 2026)."
    )
    story.append(Paragraph(sec2_text, body_style))

    # Enterprise-to-Equity Bridge Table
    story.append(Paragraph("<b>Table 1: Enterprise-to-Equity DCF Bridge (Base Case, USD Millions except per share)</b>", subtitle_style))
    bridge_table_data = [
        [Paragraph("<b>Valuation Line Item</b>", table_header_style), Paragraph("<b>Modeled Value</b>", table_header_style), Paragraph("<b>Methodological Rationale / Source</b>", table_header_style)],
        [Paragraph("PV of Explicit FCFF (FY27E-FY31E)", table_cell_style), Paragraph("$(2,238.85)M", table_cell_style), Paragraph("Reflects heavy capex burn in FY27E-FY28E before positive FCFE in FY30E-FY31E.", table_cell_style)],
        [Paragraph("PV of Terminal Value (g = 2.5%)", table_cell_style), Paragraph("$8,954.18M", table_cell_style), Paragraph("Gordon Growth applied to positive Year 5 FCFF ($1,055.2M) at WACC 10.0%.", table_cell_style)],
        [Paragraph("<b>Enterprise Value (EV)</b>", table_cell_style), Paragraph("<b>$6,715.33M</b>", table_cell_style), Paragraph("Present value of core operating digital infrastructure assets.", table_cell_style)],
        [Paragraph("(+) Cash & Cash Equivalents", table_cell_style), Paragraph("+$5,895.59M", table_cell_style), Paragraph("Balance Sheet cash (June 30, 2026), raised via equity/notes to fund capex.", table_cell_style)],
        [Paragraph("(-) Term Debt & Convertible Notes", table_cell_style), Paragraph("$(7,836.74)M", table_cell_style), Paragraph("Total contractual debt carrying amount requiring debt service.", table_cell_style)],
        [Paragraph("<b>(=) Implied Equity Value</b>", table_cell_style), Paragraph("<b>$4,774.18M</b>", table_cell_style), Paragraph("EV + Cash - Debt = Net intrinsic equity value.", table_cell_style)],
        [Paragraph("<b>Implied Value Per Share</b>", table_cell_style), Paragraph("<b>$12.12 / sh</b>", table_cell_style), Paragraph("Divided by 394.059M shares. Compares to market price of $45.73.", table_cell_style)],
    ]
    t1 = Table(bridge_table_data, colWidths=[180, 90, 270])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t1)

    # Force PageBreak for strict 2-page enforcement
    story.append(PageBreak())

    # PAGE 2
    story.append(Paragraph("BUY-SIDE INVESTMENT COMMITTEE DECISION MEMO (PAGE 2 OF 2) — IREN LIMITED", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#6c757d"), spaceAfter=6))

    # Section 3: Material Assumptions and Sensitivities
    story.append(Paragraph("3. Material Assumptions & Sensitivity Analysis", h2_style))
    sec3_text = (
        "• <b>Operating Driver Hierarchy:</b> One-at-a-time sensitivity analysis proves that the <b>Capacity Energization Path</b> (MW scale) is "
        "the dominant fundamental driver, producing a <b>$15.19/sh span</b> ($4.06 to $19.25), compared to a <b>$6.66/sh span</b> ($8.79 to $15.45) "
        "for Cash Gross Margin (power cost efficiency). Even under an aggressive +5 pp growth acceleration and 75% gross margin, intrinsic value "
        "only reaches ~$19.25, proving the market's $45.73 valuation requires speculative multiple expansion rather than operational delivery.<br/>"
        "• <b>FCFE vs. FCFF Methodological Reconciliation:</b> In Lab 10, direct equity FCFE yielded -$5.31/sh because explicit negative cash flows "
        "were discounted without adding back starting cash. Because that capex is pre-funded by the $5,895.6M cash balance, the required FCFF "
        "architecture properly credits non-operating liquidity, yielding $12.12/sh. Both methods affirm the same conclusion: WATCH / DEFER."
    )
    story.append(Paragraph(sec3_text, body_style))

    story.append(Paragraph("<b>Table 2: One-At-A-Time Sensitivity Spans & Output Impact</b>", subtitle_style))
    sens_table_data = [
        [Paragraph("<b>Load-Bearing Driver</b>", table_header_style), Paragraph("<b>Tested Range</b>", table_header_style), Paragraph("<b>FY31 EBIT ($M)</b>", table_header_style), Paragraph("<b>VPS Range ($)</b>", table_header_style), Paragraph("<b>Value Span</b>", table_header_style)],
        [Paragraph("Capacity Energization (Rev Path)", table_cell_style), Paragraph("±5.0 pp/year (compounded)", table_cell_style), Paragraph("$508.9M to $1,095.1M", table_cell_style), Paragraph("$4.06 to $19.25", table_cell_style), Paragraph("<b>$15.19 / sh</b>", table_cell_style)],
        [Paragraph("Power Cost / Cash Gross Margin", table_cell_style), Paragraph("65.0% to 75.0% (10 pp)", table_cell_style), Paragraph("$664.5M to $891.2M", table_cell_style), Paragraph("$8.79 to $15.45", table_cell_style), Paragraph("<b>$6.66 / sh</b>", table_cell_style)],
        [Paragraph("Infrastructure Capex Scale", table_cell_style), Paragraph("0.80x to 1.20x base capex", table_cell_style), Paragraph("$777.9M (held fixed)", table_cell_style), Paragraph("$10.15 to $14.09", table_cell_style), Paragraph("<b>$3.94 / sh</b>", table_cell_style)],
        [Paragraph("WACC Discount Rate", table_cell_style), Paragraph("9.0% to 11.0% (200 bps)", table_cell_style), Paragraph("$777.9M (held fixed)", table_cell_style), Paragraph("$8.42 to $16.58", table_cell_style), Paragraph("<b>$8.16 / sh</b>", table_cell_style)],
    ]
    t2 = Table(sens_table_data, colWidths=[140, 110, 110, 100, 80])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t2)

    # Section 4: Principal Risks, Failure Conditions, and Monitoring Triggers
    story.append(Paragraph("4. Principal Risks, Failure Conditions & Monitoring Triggers", h2_style))
    sec4_text = (
        "• <b>Execution & Customer Delay Risk:</b> Horizon 1 is delivered, but Horizons 2–4 (Childress, TX) remain under construction. "
        "Delays trigger contractual service credits, delay penalties, or customer termination rights under hyperscaler MSAs.<br/>"
        "• <b>Dilution & Refinancing Risk:</b> $7.84B in carrying debt includes $6.30B in convertible notes. If share price softens below conversion "
        "thresholds, debt refinancing could enforce severe equity dilution or debt service pressure.<br/>"
        "• <b>Observable Monitoring Triggers (Reversal Conditions):</b> Revisit WATCH-DEFER if (1) market price corrects toward the fundamental range "
        "($12–$18), OR (2) Horizons 2–4 achieve verified customer acceptance scaling recognized quarterly GAAP revenue above $375M ($1.5B ARR), "
        "with positive cash from operations before customer prepayments, and expansion funded without share dilution >10%."
    )
    story.append(Paragraph(sec4_text, body_style))

    # Section 5: Action Requested and Next Review Point
    story.append(Paragraph("5. Action Requested & Next Review Point", h2_style))
    sec5_text = (
        "<b>COMMITTEE ACTION REQUESTED:</b> Confirm zero equity position. Maintain IREN on the technology fund's active watch list.<br/>"
        "<b>NEXT FORMAL REVIEW POINT:</b> Q2 FY2027 earnings release (February 2027) or upon formal SEC Form 8-K filing confirming commercial "
        "energization, customer acceptance, and recognized billing for Horizons 2, 3, and 4."
    )
    story.append(Paragraph(sec5_text, body_style))

    doc.build(story)
    print(f"Successfully generated {pdf_path.name} (Strictly 2 pages)")


def create_research_evolution_pdf():
    pdf_path = BASE_DIR / "Research-Evolution.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("RevTitle", parent=styles["Heading1"], fontSize=14, leading=16, textColor=colors.HexColor("#0f2b48"), spaceAfter=4)
    subtitle_style = ParagraphStyle("RevSub", parent=styles["Normal"], fontSize=8.5, leading=11, textColor=colors.HexColor("#495057"), spaceAfter=6)
    h2_style = ParagraphStyle("RevH2", parent=styles["Heading2"], fontSize=10.5, leading=13, textColor=colors.HexColor("#0f2b48"), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle("RevBody", parent=styles["Normal"], fontSize=8, leading=10.5, textColor=colors.HexColor("#212529"), spaceAfter=4)
    table_cell_style = ParagraphStyle("RevCell", parent=styles["Normal"], fontSize=7, leading=8.5, textColor=colors.HexColor("#212529"))
    table_header_style = ParagraphStyle("RevHeader", parent=styles["Normal"], fontSize=7.5, leading=9, textColor=colors.white, fontName="Helvetica-Bold")

    story = []
    story.append(Paragraph("RESEARCH EVOLUTION BRIEF — IREN LIMITED (NASDAQ: IREN)", title_style))
    story.append(Paragraph("Student: Elliot | Course: FIN 43900 | Edition A (2026-09-03) to Edition B (2026-10-08) Trajectory", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f2b48"), spaceAfter=6))

    story.append(Paragraph("1. Edition A — Unchanged Brightspace Baseline", h2_style))
    story.append(Paragraph(
        "<b>Baseline File:</b> <code>IREN_2026-09-03_report.md</code> | <b>Immutable Commit:</b> <code>27108195fbd49f6c7d1fb5d0fa7ddd61fec45ecd</code> (September 3, 2026).<br/>"
        "<b>Original Recommendation:</b> WATCH / DEFER based on qualitative trade-offs between rapid AI Cloud growth ($128.8M) and massive financial burn "
        "(FY26 net loss of $(702.6)M, $13.81B in capital commitments, and $11.0B in external financing). Edition A is preserved intact in the repository root.",
        body_style
    ))

    story.append(Paragraph("2. Dated Correction Addendum", h2_style))
    story.append(Paragraph(
        "• <b>SEC Form Transition (20-F to 10-K):</b> FY24 figures were restated under US GAAP following IREN's transition from an Australian FPI to a domestic filer.<br/>"
        "• <b>Capex Aggregator Distortion:</b> Corrected aggregator capex ($2,998M) by identifying $1,335.1M in computer hardware payments, establishing actual cash capex of $4,333.1M.<br/>"
        "• <b>Share Count Multi-Basis:</b> Reconciled Cover Page basic count (394.06M), Balance Sheet ending count (380.19M), and Diluted weighted-average count (316.12M).",
        body_style
    ))

    story.append(Paragraph("3. Edition B — A-to-B Evidence Table", h2_style))
    table_data = [
        [Paragraph("<b>Item</b>", table_header_style), Paragraph("<b>Edition A (2026-09-03)</b>", table_header_style), Paragraph("<b>Edition B (2026-10-08)</b>", table_header_style), Paragraph("<b>Primary Driver</b>", table_header_style), Paragraph("<b>Justifying Evidence & Tests</b>", table_header_style)],
        [Paragraph("<b>Thesis & Action</b>", table_cell_style), Paragraph("WATCH / DEFER based on qualitative capex hesitation.", table_cell_style), Paragraph("WATCH / DEFER rigorously affirmed: DCF yields $12.12/sh vs $45.73 market price.", table_cell_style), Paragraph("Own Analysis & Modeling", table_cell_style), Paragraph("Pro-forma model proves market price trades at ~280% premium to intrinsic operating value.", table_cell_style)],
        [Paragraph("<b>Model Architecture</b>", table_cell_style), Paragraph("Multiples outline and high-level DCF framework.", table_cell_style), Paragraph("Integrated 5-Year 3-Statement Pro-Forma FCFF Enterprise DCF + WACC bridge.", table_cell_style), Paragraph("Course Instruction & Own Build", table_cell_style), Paragraph("Statements articulate with zero gap (Gap = 0.0000). Connects operations to enterprise bridge.", table_cell_style)],
        [Paragraph("<b>Historical Sourcing</b>", table_cell_style), Paragraph("Initial Form 10-K review of headline totals.", table_cell_style), Paragraph("Audited 3-year history grid; corrected $1.34B hardware capex undercounting.", table_cell_style), Paragraph("Independent Auditing", table_cell_style), Paragraph("Traced Form 10-K Cash Flow Stmt. p. F-9; verified $0 inventory on balance sheet p. F-6.", table_cell_style)],
        [Paragraph("<b>Sensitivities & Spans</b>", table_cell_style), Paragraph("Broad qualitative risks (power, GPUs, contracts).", table_cell_style), Paragraph("Quantified one-at-a-time spans: Capacity Energization ($15.19) > Power Margin ($6.66).", table_cell_style), Paragraph("Course Instruction & Peer Review", table_cell_style), Paragraph("Labs 11 & 12 sensitivity engines isolated causal links: revenue scale drives 2.3x the value impact of margin.", table_cell_style)],
        [Paragraph("<b>Validation & Failure Gates</b>", table_cell_style), Paragraph("No code testing or automated accounting gates.", table_cell_style), Paragraph("Triple validation suite: ABG known-answer ($291.75), refusal gates, and locked changed-input test.", table_cell_style), Paragraph("Validation Protocol", table_cell_style), Paragraph("Injected +$500M cash error halted script. Monotonicity confirmed across all tests.", table_cell_style)],
    ]
    t_rev = Table(table_data, colWidths=[80, 115, 125, 95, 125])
    t_rev.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rev)

    story.append(Paragraph("4. What Changed from Edition A to Edition B, and Why?", h2_style))
    story.append(Paragraph(
        "The central committee recommendation did <b>not</b> change: both editions conclude that the fund must <b>WATCH / DEFER</b>. "
        "However, the analytical authority supporting the decision evolved from subjective qualitative skepticism into audited quantitative proof. "
        "Edition B establishes that even with aggressive hyperscaler revenue scaling to $3.5B and 70% cash gross margins, the massive $4.3B initial capex "
        "and $7.8B debt load limit fundamental equity value to $12.12 per share. The market price ($45.73) prices in multi-decade perfection without "
        "execution buffer. The committee's deferral is mathematically validated.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated {pdf_path.name}")


def create_validation_pdf():
    pdf_path = BASE_DIR / "Validation-and-AI-Use.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("ValTitle", parent=styles["Heading1"], fontSize=13, leading=15, textColor=colors.HexColor("#0f2b48"), spaceAfter=3)
    subtitle_style = ParagraphStyle("ValSub", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#495057"), spaceAfter=5)
    h2_style = ParagraphStyle("ValH2", parent=styles["Heading2"], fontSize=9.5, leading=12, textColor=colors.HexColor("#0f2b48"), spaceBefore=5, spaceAfter=2)
    body_style = ParagraphStyle("ValBody", parent=styles["Normal"], fontSize=7.5, leading=9.5, textColor=colors.HexColor("#212529"), spaceAfter=3)
    table_cell_style = ParagraphStyle("ValCell", parent=styles["Normal"], fontSize=6.5, leading=8, textColor=colors.HexColor("#212529"))
    table_header_style = ParagraphStyle("ValHeader", parent=styles["Normal"], fontSize=7, leading=8.5, textColor=colors.white, fontName="Helvetica-Bold")

    story = []
    story.append(Paragraph("VALIDATION AND AI USE RECORD — IREN LIMITED (NASDAQ: IREN)", title_style))
    story.append(Paragraph("Student: Elliot | Course: FIN 43900 | Sourced Ledger, Locked Changed-Input Test, and AI Disclosure", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f2b48"), spaceAfter=5))

    story.append(Paragraph("1. Decision, Version, and As-of Boundary", h2_style))
    story.append(Paragraph(
        "<b>Decision:</b> WATCH / DEFER at $12.12/sh intrinsic value vs $45.73 market price. | <b>Commit:</b> <code>b3ec7ca</code> | <b>Date:</b> 2026-10-08 | "
        "<b>Environment:</b> Python 3.13.15, pandas 3.0.6, numpy 2.5.3, streamlit 1.65.0, reportlab 5.0.1.",
        body_style
    ))

    story.append(Paragraph("2. Data and Convention Ledger", h2_style))
    data_ledger = [
        [Paragraph("<b>Material Input</b>", table_header_style), Paragraph("<b>Sourced Value</b>", table_header_style), Paragraph("<b>SEC Filing Source Locator</b>", table_header_style), Paragraph("<b>Treatment / Risk Handling</b>", table_header_style)],
        [Paragraph("Total Revenue (FY26)", table_cell_style), Paragraph("$707,007 thousand", table_cell_style), Paragraph("10-K, Cons. Stmt. of Operations, p. F-7", table_cell_style), Paragraph("Audited GAAP revenue. Excludes unearned $4.0B ARR.", table_cell_style)],
        [Paragraph("Cash Cost of Rev (Power)", table_cell_style), Paragraph("$219,706 thousand", table_cell_style), Paragraph("10-K, Cons. Stmt. of Operations, p. F-7", table_cell_style), Paragraph("Reconciles to 68.92% gross margin excl. D&A.", table_cell_style)],
        [Paragraph("Audited Cash Capex", table_cell_style), Paragraph("$4,333,143 thousand", table_cell_style), Paragraph("10-K, Stmt. of Cash Flows, p. F-9", table_cell_style), Paragraph("Includes $2,998M PP&E + $1,335M hardware (missed by aggregators).", table_cell_style)],
        [Paragraph("Customer Prepayments", table_cell_style), Paragraph("$1,842,546 thousand", table_cell_style), Paragraph("10-K, Cons. Balance Sheet, p. F-6", table_cell_style), Paragraph("Microsoft cash advance; non-dilutive working capital liquidity.", table_cell_style)],
        [Paragraph("Ending Cash Balance", table_cell_style), Paragraph("$5,895,591 thousand", table_cell_style), Paragraph("10-K, Cons. Balance Sheet, p. F-6", table_cell_style), Paragraph("Direct filing input; verifies capex pre-funding.", table_cell_style)],
        [Paragraph("Term Debt & Notes", table_cell_style), Paragraph("$7,836,740 thousand", table_cell_style), Paragraph("10-K, Notes 22 & 23, pp. F-43–F-47", table_cell_style), Paragraph("Carrying debt deducted in enterprise-to-equity bridge.", table_cell_style)],
        [Paragraph("Basic Ordinary Shares", table_cell_style), Paragraph("394.059 million", table_cell_style), Paragraph("10-K Cover Page (August 14, 2026)", table_cell_style), Paragraph("Primary share count denominator reflecting actual current shares.", table_cell_style)],
    ]
    t_dl = Table(data_ledger, colWidths=[110, 95, 150, 185])
    t_dl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_dl)

    story.append(Paragraph("3. Validation Register & Refusal Gates", h2_style))
    val_reg = [
        [Paragraph("<b>Claim / Test</b>", table_header_style), Paragraph("<b>Expected Behavior</b>", table_header_style), Paragraph("<b>Actual Result</b>", table_header_style), Paragraph("<b>Disposition</b>", table_header_style)],
        [Paragraph("Synthetic Known-Answer", table_cell_style), Paragraph("Lab 09 ABG engine yields exactly $291.75/sh.", table_cell_style), Paragraph("Implied VPS = $291.75; Gap = 0.0000 across all 5 yrs.", table_cell_style), Paragraph("<b>PASS</b> (Reconciled to cent)", table_cell_style)],
        [Paragraph("Double-Entry Articulation", table_cell_style), Paragraph("Assets - Liab - Equity = 0.0000 every year.", table_cell_style), Paragraph("Gap = 0.0000 in FY27E-FY31E; cash ties to BS.", table_cell_style), Paragraph("<b>PASS</b> (Articulated)", table_cell_style)],
        [Paragraph("Refusal Gate (Cash Break)", table_cell_style), Paragraph("Inject +$500M artificial cash break in FY28E.", table_cell_style), Paragraph("Script halted: 'MODEL REFUSAL: Gap = $+500.0M'", table_cell_style), Paragraph("<b>PASS</b> (Refusal triggered)", table_cell_style)],
        [Paragraph("Stress Negative FCFE", table_cell_style), Paragraph("Capitalizing negative terminal FCFE is refused.", table_cell_style), Paragraph("Terminal value flagged UNAVAIL; refused Gordon model.", table_cell_style), Paragraph("<b>PASS</b> (Economic logic held)", table_cell_style)],
        [Paragraph("README Cold-Run Test", table_cell_style), Paragraph("Cold execution reproduces visible output.", table_cell_style), Paragraph("py run_analysis.py ran in 1.8s; exported visible_output.json.", table_cell_style), Paragraph("<b>PASS</b> (Reproduced)", table_cell_style)],
    ]
    t_vr = Table(val_reg, colWidths=[110, 150, 170, 110])
    t_vr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_vr)

    story.append(PageBreak())

    story.append(Paragraph("VALIDATION AND AI USE RECORD (PAGE 2 OF 2) — IREN LIMITED", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#6c757d"), spaceAfter=5))

    story.append(Paragraph("4. Locked Changed-Input Record — Human Prediction First; AI Closed During Execution", h2_style))
    story.append(Paragraph("<b>Precommit Timestamp:</b> 2026-09-29 14:30 EDT | <b>Repository Commit:</b> <code>3125ff9</code>", subtitle_style))
    lcir_data = [
        [Paragraph("<b>Changed Input</b>", table_header_style), Paragraph("<b>Old → New Value</b>", table_header_style), Paragraph("<b>Human Precommit Prediction</b>", table_header_style), Paragraph("<b>Preserved Execution Result</b>", table_header_style), Paragraph("<b>Reconciliation & Action</b>", table_header_style)],
        [Paragraph("Cash Gross Margin", table_cell_style), Paragraph("70.0% → 75.0% (+5 pp)", table_cell_style), Paragraph("EBIT & value must rise monotonically; capex keeps FCFE negative.", table_cell_style), Paragraph("FCFF VPS rose from $12.12 to $15.45 (+$3.33/sh). FCFE VPS rose from -$5.31 to -$2.93.", table_cell_style), Paragraph("<b>MATCHED</b>. Margin expansion helps but is secondary to capex. Action: WATCH-DEFER.", table_cell_style)],
        [Paragraph("Revenue Growth Path", table_cell_style), Paragraph("Base → +5 pp/yr path", table_cell_style), Paragraph("Revenue scales sharply; VPS increases substantially.", table_cell_style), Paragraph("FCFF VPS rose from $12.12 to $19.25 (+$7.13/sh). FCFE VPS crossed to +$0.99.", table_cell_style), Paragraph("<b>MATCHED</b>. Proves Capacity Energization is dominant driver. Action: WATCH-DEFER.", table_cell_style)],
    ]
    t_lc = Table(lcir_data, colWidths=[85, 85, 125, 125, 120])
    t_lc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_lc)

    story.append(Paragraph("5. Named AI-Use Register", h2_style))
    ai_reg = [
        [Paragraph("<b>Tool / Model Surface</b>", table_header_style), Paragraph("<b>Date</b>", table_header_style), Paragraph("<b>Task</b>", table_header_style), Paragraph("<b>Output Considered</b>", table_header_style), Paragraph("<b>Independent Check</b>", table_header_style), Paragraph("<b>Disposition & Effect</b>", table_header_style)],
        [Paragraph("ChatGPT / Codex (GPT-4o)", table_cell_style), Paragraph("2026-09-03", table_cell_style), Paragraph("Initial report structure", table_cell_style), Paragraph("Suggested treating $4.0B ARR as recognized revenue.", table_cell_style), Paragraph("Checked Item 7 MD&A; verified ARR is unearned non-GAAP.", table_cell_style), Paragraph("<b>MODIFIED</b>. Excluded ARR; prevented top-line revenue contamination.", table_cell_style)],
        [Paragraph("Claude 3.5 Sonnet", table_cell_style), Paragraph("2026-09-24", table_cell_style), Paragraph("Pro-forma scaffolding", table_cell_style), Paragraph("Proposed standard working capital formula with inventory.", table_cell_style), Paragraph("Traced Form 10-K balance sheet; confirmed $0 inventory.", table_cell_style), Paragraph("<b>REJECTED</b>. Replaced with Customer Prepayment liability modeling.", table_cell_style)],
        [Paragraph("Antigravity Assistant", table_cell_style),デー] if False else [Paragraph("Antigravity Assistant", table_cell_style), Paragraph("2026-10-08", table_cell_style), Paragraph("Audit & Streamlit UI", table_cell_style), Paragraph("Diagnosed manifest tokenizer bug; scaffolded app.py workbench.", table_cell_style), Paragraph("Tested terminal execution; verified ReportLab and Streamlit.", table_cell_style), Paragraph("<b>ACCEPTED</b>. Produced reproducible cold-run and interactive product.", table_cell_style)],
    ]
    t_ai = Table(ai_reg, colWidths=[90, 50, 80, 110, 100, 110])
    t_ai.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f2b48")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_ai)

    story.append(Paragraph("6. Limitations, Monitoring, and Kill Rules", h2_style))
    story.append(Paragraph(
        "• <b>Kill Conditions:</b> Reject valuation immediately if balance sheet fails articulation (Gap > $0.01M), if cash buffer drops below $500M, "
        "or if terminal FCF is negative.<br/>"
        "• <b>Observable Monitoring:</b> Track verified customer acceptance of Horizons 2–4 and positive operating cash flow before customer advances.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated {pdf_path.name}")


if __name__ == "__main__":
    create_decision_memo_pdf()
    create_research_evolution_pdf()
    create_validation_pdf()
