import os
import warnings

# ---- Streamlit safety flags ----
os.environ["STREAMLIT_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

warnings.filterwarnings("ignore")

# ---- Core imports ----
import streamlit as st
import pandas as pd

from pipeline import extract, enrich, risk
from pipeline.credit_score import estimate_credit_score
from pipeline.volatility import cashflow
from pipeline.risk_engine import risk_scores
from pipeline.risk_graph import build_risk_graph
from reports.report_generator import generate_report


# ---- Page setup ----
st.set_page_config(layout="wide")
st.title("🏦 Bank Statement Risk Analyzer")

pdfs = st.file_uploader(
    "Upload bank statement PDFs",
    type="pdf",
    accept_multiple_files=True
)

if pdfs:
    dfs = []

    # ---- Process PDFs ----
    for pdf in pdfs:
        df = extract.process(pdf)
        df = enrich.enrich(df)
        df = risk.tag_risks(df)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)

    # ---- Risk analytics ----
    scores = risk_scores(full_df)
    credit_score = estimate_credit_score(full_df)

    # ---- Top KPIs ----
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Indicative Credit Score", credit_score)
    col2.metric("Final Risk Score", scores["final_score"])
    col3.metric("Cash Withdrawals", len(full_df[full_df.category == "Cash Withdrawal"]))
    col4.metric("EMI Transactions", len(full_df[full_df.category == "Loan/EMI"]))

    # ---- Risk interpretation ----
    st.subheader("🧠 Risk Breakdown (Explainable)")
    st.json(scores)

    # ---- Obsidian-style risk graph ----
    st.subheader("🕸️ Risk Relationship Graph")
    graph_path = build_risk_graph(full_df,scores)
    st.components.v1.html(open(graph_path).read(), height=450)

    # ---- Transactions table ----
    st.subheader("📊 Transactions")
    st.dataframe(full_df, use_container_width=True)

    # ---- Cashflow volatility ----
    st.subheader("📉 Cashflow Volatility")
    st.line_chart(cashflow(full_df))

   # ---- Report generation ----
if "report_path" not in st.session_state:
    st.session_state.report_path = None

if st.button("📄 Generate PDF Report"):
    st.session_state.report_path = generate_report(
        full_df,
        scores,
        credit_score,
        "Low Risk" if scores["final_score"] < 30 else
        "Medium Risk" if scores["final_score"] < 60 else
        "High Risk"
    )

# ---- Download appears only if report exists ----
if st.session_state.report_path:
    with open(st.session_state.report_path, "rb") as f:
        st.download_button(
            "⬇️ Download Risk Report",
            f,
            file_name="final_report.pdf"
        )
