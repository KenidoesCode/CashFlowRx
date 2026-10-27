from pyvis.network import Network
from pipeline.behaviour_map import map_transaction_to_behavior
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

def build_risk_graph(df, scores):
    net = Network(
        height="550px",
        bgcolor="#0b1020",
        font_color="#e5e7eb",
        directed=True
    )

    # ---- Final Risk Node ----
    net.add_node(
        "FINAL_RISK",
        label=f"Final Risk\nScore: {scores['final_score']}",
        size=40,
        color="#ef4444",
        shape="box"
    )

    # ---- Risk Dimensions ----
    risk_nodes = {
        "Income Stability": scores["income_risk"],
        "Spending Discipline": scores["spending_risk"],
        "Liquidity Health": scores["liquidity_risk"],
        "Debt Load": scores["debt_risk"],
        "Cash Dependency": scores["cash_risk"],
    }

    for name, score in risk_nodes.items():
        color = (
            "#22c55e" if score < 30 else
            "#f59e0b" if score < 60 else
            "#ef4444"
        )

        net.add_node(
            name,
            label=f"{name}\nRisk: {score}",
            size=25,
            color=color
        )

        net.add_edge(
            name,
            "FINAL_RISK",
            value=score,
            title=f"{name} contributes {score}"
        )

    # ---- Behavior Nodes ----
    behaviors = {}

    for _, row in df.iterrows():
        behavior = map_transaction_to_behavior(row)
        behaviors.setdefault(behavior, []).append(row)

    for behavior, rows in behaviors.items():
        net.add_node(
            behavior,
            label=f"{behavior}\n({len(rows)} txns)",
            size=20,
            color="#38bdf8"
        )

        # Link behavior to appropriate risk dimension
        if behavior == "High Cash Usage":
            net.add_edge(behavior, "Cash Dependency")
        elif behavior == "Debt Obligation":
            net.add_edge(behavior, "Debt Load")
        elif behavior == "Large Outflow":
            net.add_edge(behavior, "Spending Discipline")
        elif behavior == "Income Event":
            net.add_edge(behavior, "Income Stability")
        else:
            net.add_edge(behavior, "Liquidity Health")

    # ---- Transaction Nodes (sampled to avoid clutter) ----
    sample_df = df.sample(min(25, len(df)))

    for idx, row in sample_df.iterrows():
        tx_id = f"TX_{idx}"
        label = f"{row.date}\n₹{row.amount}\n{row.category}"

        net.add_node(
            tx_id,
            label=label,
            size=12,
            color="#94a3b8"
        )

        behavior = map_transaction_to_behavior(row)
        net.add_edge(tx_id, behavior)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graph_path = OUTPUT_DIR / "risk_graph.html"
    # Generate in memory, then write directly to the resolved project path.
    # This avoids PyVis resolving a relative path against Streamlit's cwd.
    graph_html = net.generate_html()
    graph_path.write_text(graph_html, encoding="utf-8")
    return str(graph_path)
