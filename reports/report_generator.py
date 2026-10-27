from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os


def generate_report(df, scores, credit_score, risk_level):
    """
    Generate a professional, explainable bank risk PDF report.
    """

    os.makedirs("output", exist_ok=True)
    path = "output/bank_risk_report.pdf"

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---- Title ----
    elements.append(Paragraph(
        "<b>Bank Statement Risk Assessment Report</b>",
        styles["Title"]
    ))
    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %B %Y')}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    # ---- Executive Summary ----
    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(
        f"""
        Based on the analysis of the provided bank statements, the account
        has been classified as <b>{risk_level}</b> with an indicative
        credit health score of <b>{credit_score}</b>.
        """,
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # ---- Risk Breakdown ----
    elements.append(Paragraph("<b>Risk Dimension Breakdown</b>", styles["Heading2"]))

    risk_table = [
        ["Risk Dimension", "Score (0–100)", "Interpretation"],
        ["Income Stability", scores["income_risk"], interpret(scores["income_risk"])],
        ["Spending Discipline", scores["spending_risk"], interpret(scores["spending_risk"])],
        ["Liquidity Health", scores["liquidity_risk"], interpret(scores["liquidity_risk"])],
        ["Debt Load", scores["debt_risk"], interpret(scores["debt_risk"])],
        ["Cash Dependency", scores["cash_risk"], interpret(scores["cash_risk"])],
        ["Final Composite Risk", scores["final_score"], risk_level],
    ]

    t = Table(risk_table, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elements.append(t)
    elements.append(Spacer(1, 18))

    # ---- Key Observations ----
    elements.append(Paragraph("<b>Key Observations</b>", styles["Heading2"]))

    observations = [
        f"Total transactions analysed: {len(df)}",
        f"Cash withdrawals observed: {len(df[df.category == 'Cash Withdrawal'])}",
        f"Loan/EMI related transactions: {len(df[df.category == 'Loan/EMI'])}",
        f"Net cashflow: {round(df.amount.sum(), 2)}",
    ]

    for o in observations:
        elements.append(Paragraph(f"• {o}", styles["Normal"]))

    elements.append(Spacer(1, 16))

    # ---- Sample Transactions ----
    elements.append(Paragraph("<b>Transaction Snapshot</b>", styles["Heading2"]))

    sample = df.head(15)[["date", "category", "amount", "risk_tag"]]
    table_data = [["Date", "Category", "Amount", "Risk Tag"]] + sample.values.tolist()

    tx_table = Table(table_data, hAlign="LEFT")
    tx_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
    ]))

    elements.append(tx_table)

    doc.build(elements)
    return path


def interpret(score):
    if score < 30:
        return "Low Risk"
    if score < 60:
        return "Moderate Risk"
    return "High Risk"
