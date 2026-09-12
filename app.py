"""Streamlit Web Application for Buy or Wait? — AI Financial Decision Agent.
"""
import os
import sys
import pandas as pd
import streamlit as st
from datetime import datetime

# Add code directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.join(current_dir, "code")
if code_dir not in sys.path:
    sys.path.append(code_dir)

from data_loader import DataLoader
from finance_engine import FinanceEngine
from payment_planner import PaymentPlanner
from decision_engine import DecisionEngine

st.set_page_config(
    page_title="Buy or Wait? — AI Financial Agent",
    page_icon="💳",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
    .badge-affordable_now { background-color: #d4edda; color: #155724; padding: 6px 12px; border-radius: 6px; font-weight: bold; }
    .badge-affordable_with_plan { background-color: #cce5ff; color: #004085; padding: 6px 12px; border-radius: 6px; font-weight: bold; }
    .badge-affordable_later { background-color: #fff3cd; color: #856404; padding: 6px 12px; border-radius: 6px; font-weight: bold; }
    .badge-not_affordable { background-color: #f8d7da; color: #721c24; padding: 6px 12px; border-radius: 6px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_system():
    loader = DataLoader("dataset")
    loader.load_all()
    finance_engine = FinanceEngine(loader)
    planner = PaymentPlanner(loader, finance_engine)
    engine = DecisionEngine(loader, finance_engine, planner)
    return loader, finance_engine, planner, engine


loader, finance_engine, planner, engine = load_system()

st.title("💳 Buy or Wait? — AI Financial Decision Agent")
st.markdown("**HackerRank Orchestrate — Autonomous Financial Affordability & Cash-Flow Simulator**")

# Sidebar for request selection
st.sidebar.header("Select Request")
requests_df = loader.requests_df

req_ids = requests_df["request_id"].tolist()
selected_req_id = st.sidebar.selectbox("Choose Evaluation Request:", req_ids)

req_row = requests_df[requests_df["request_id"] == selected_req_id].iloc[0]
user_id = req_row["user_id"]
prof = loader.get_user_profile(user_id)
currency = prof["home_currency"]

# Evaluate through agent
pred = engine.evaluate_request(req_row)

# Header columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Requested Item / Type", str(req_row["request_type"]).title())
with col2:
    st.metric("Requested Amount", f"{currency} {float(req_row['requested_amount']):,.2f}")
with col3:
    st.metric("Available Balance", f"{currency} {float(prof['current_available_balance']):,.2f}")
with col4:
    st.metric("Emergency Minimum", f"{currency} {float(prof['minimum_balance_to_keep']):,.2f}")

st.markdown("---")

# Decision Showcase
st.subheader("🎯 Agent Recommendation & Decision")

status = pred["affordability_status"]
method = pred["recommended_payment_method"]

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.markdown(f"**Affordability Status:**")
    st.markdown(f"<span class='badge-{status}'>{status.upper().replace('_', ' ')}</span>", unsafe_allow_html=True)
    
    st.markdown(f"<br>**Recommended Method:**", unsafe_allow_html=True)
    st.info(f"**{method.upper().replace('_', ' ')}**")

    st.markdown(f"**Safe to Pay Today:** `{currency} {float(pred['amount_safe_to_pay']):,.2f}`")
    
    if pred["earliest_date_for_full_payment"]:
        st.markdown(f"**Earliest Safe Full Date:** `{pred['earliest_date_for_full_payment']}`")

with col_res2:
    st.markdown("**Decision Explanation:**")
    st.success(pred["decision_explanation"])

    if pred["payment_plan"] != "none":
        st.markdown("**Payment Plan Schedule:**")
        plan_items = pred["payment_plan"].split("|")
        plan_data = []
        for item in plan_items:
            dt, amt = item.split(":")
            plan_data.append({"Payment Date": dt, f"Amount ({currency})": float(amt)})
        st.table(pd.DataFrame(plan_data))

    if pred["spending_changes_needed"] != "none":
        st.markdown("**Required Spending Adjustments:**")
        st.warning(pred["spending_changes_needed"])

st.markdown("---")

# User Financial Profile & Context
st.subheader("👤 User Financial Profile & Preferences")
pcol1, pcol2 = st.columns(2)

with pcol1:
    st.write(f"- **User ID:** `{user_id}`")
    st.write(f"- **Protected Categories:** {prof['expense_categories_to_protect']}")
    st.write(f"- **Allowed Reductions:** {prof['expense_categories_user_is_willing_to_reduce']}")

with pcol2:
    st.write(f"- **Considered Payment Methods:** {prof['payment_methods_user_will_consider']}")
    st.write(f"- **Max Installment Months:** {prof['max_installment_months']}")
    st.write(f"- **Allows Partial Payment:** {req_row['allows_partial_payment']}")

# Show raw CSV prediction
st.markdown("---")
with st.expander("📄 View Evaluation Output Row for Submission"):
    st.json(pred)
