"""Flask Web Dashboard for Buy or Wait? — AI Financial Decision Agent.
Serves an interactive web interface on http://localhost:5000.
"""
import os
import sys
import pandas as pd
from flask import Flask, request, render_template_string, jsonify

# Add code directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.join(current_dir, "code")
if code_dir not in sys.path:
    sys.path.append(code_dir)

from data_loader import DataLoader
from finance_engine import FinanceEngine
from payment_planner import PaymentPlanner
from decision_engine import DecisionEngine

app = Flask(__name__)

# Initialize engine
loader = DataLoader("dataset")
loader.load_all()
finance_engine = FinanceEngine(loader)
planner = PaymentPlanner(loader, finance_engine)
engine = DecisionEngine(loader, finance_engine, planner)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buy or Wait? — AI Financial Advisor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px 0; margin-bottom: 25px; }
        .card { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: none; margin-bottom: 20px; }
        .badge-status { font-size: 1rem; padding: 8px 16px; border-radius: 20px; text-transform: uppercase; font-weight: bold; }
        .status-affordable_now { background-color: #d4edda; color: #155724; }
        .status-affordable_with_plan { background-color: #cce5ff; color: #004085; }
        .status-affordable_later { background-color: #fff3cd; color: #856404; }
        .status-not_affordable { background-color: #f8d7da; color: #721c24; }
        .metric-title { font-size: 0.85rem; color: #6c757d; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-value { font-size: 1.5rem; font-weight: bold; color: #2c3e50; }
        .explanation-box { background-color: #e8f4f8; border-left: 5px solid #17a2b8; padding: 15px; border-radius: 6px; font-size: 1.05rem; }
    </style>
</head>
<body>
    <div class="hero">
        <div class="container">
            <h1 class="fw-bold">💳 Buy or Wait? — AI Financial Agent</h1>
            <p class="mb-0">HackerRank Orchestrate Autonomous Financial Decision & Cash-Flow Simulator</p>
        </div>
    </div>

    <div class="container">
        <div class="row">
            <!-- Sidebar / Selector -->
            <div class="col-md-4">
                <div class="card p-4">
                    <h5 class="fw-bold mb-3">Select Purchase Request</h5>
                    <form method="GET" action="/">
                        <div class="mb-3">
                            <label class="form-label text-muted">Choose Request ID (1 to 250):</label>
                            <select name="request_id" class="form-select form-select-lg" onchange="this.form.submit()">
                                {% for r_id in request_ids %}
                                    <option value="{{ r_id }}" {% if r_id == selected_id %}selected{% endif %}>
                                        {{ r_id }} ({{ requests_map[r_id]['user_id'] }})
                                    </option>
                                {% endfor %}
                            </select>
                        </div>
                    </form>

                    <hr>
                    <h6 class="fw-bold text-muted">User Context & Profile</h6>
                    <ul class="list-unstyled small text-muted">
                        <li><strong>User ID:</strong> {{ user_id }}</li>
                        <li><strong>Home Currency:</strong> {{ currency }}</li>
                        <li><strong>Protected Spending:</strong> {{ profile['expense_categories_to_protect'] }}</li>
                        <li><strong>Allowed Reductions:</strong> {{ profile['expense_categories_user_is_willing_to_reduce'] }}</li>
                        <li><strong>Considered Methods:</strong> {{ profile['payment_methods_user_will_consider'] }}</li>
                    </ul>
                </div>
            </div>

            <!-- Main Content Area -->
            <div class="col-md-8">
                <!-- Request Summary Cards -->
                <div class="row">
                    <div class="col-sm-3">
                        <div class="card p-3 text-center">
                            <div class="metric-title">Category</div>
                            <div class="metric-value">{{ req_row['request_type']|capitalize }}</div>
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="card p-3 text-center">
                            <div class="metric-title">Requested</div>
                            <div class="metric-value">{{ currency }} {{ "{:,.2f}".format(req_row['requested_amount']) }}</div>
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="card p-3 text-center">
                            <div class="metric-title">Balance</div>
                            <div class="metric-value">{{ currency }} {{ "{:,.2f}".format(profile['current_available_balance']) }}</div>
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="card p-3 text-center">
                            <div class="metric-title">Min Balance</div>
                            <div class="metric-value">{{ currency }} {{ "{:,.2f}".format(profile['minimum_balance_to_keep']) }}</div>
                        </div>
                    </div>
                </div>

                <!-- Decision Card -->
                <div class="card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="fw-bold mb-0">AI Recommendation</h4>
                        <span class="badge-status status-{{ pred['affordability_status'] }}">
                            {{ pred['affordability_status'].replace('_', ' ') }}
                        </span>
                    </div>

                    <div class="row mb-3">
                        <div class="col-md-6">
                            <p class="mb-1 text-muted">Recommended Payment Approach:</p>
                            <h4 class="text-primary fw-bold">{{ pred['recommended_payment_method'].replace('_', ' ').title() }}</h4>
                        </div>
                        <div class="col-md-6">
                            <p class="mb-1 text-muted">Amount Safe to Pay Today:</p>
                            <h4 class="text-success fw-bold">{{ currency }} {{ "{:,.2f}".format(pred['amount_safe_to_pay']) }}</h4>
                        </div>
                    </div>

                    <div class="explanation-box mb-3">
                        <strong>💡 AI Decision Rationale:</strong><br>
                        {{ pred['decision_explanation'] }}
                    </div>

                    {% if pred['earliest_date_for_full_payment'] %}
                    <p class="mb-2"><strong>Earliest Safe Date for Full Payment:</strong> <code>{{ pred['earliest_date_for_full_payment'] }}</code></p>
                    {% endif %}

                    {% if plan_data %}
                    <h6 class="fw-bold mt-3">Payment Schedule Breakdown:</h6>
                    <table class="table table-bordered table-sm mt-2">
                        <thead class="table-light">
                            <tr>
                                <th>#</th>
                                <th>Scheduled Date</th>
                                <th>Amount to Pay</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in plan_data %}
                            <tr>
                                <td>{{ loop.index }}</td>
                                <td><code>{{ row['date'] }}</code></td>
                                <td class="fw-bold">{{ currency }} {{ "{:,.2f}".format(row['amount']) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% endif %}

                    {% if pred['spending_changes_needed'] != 'none' %}
                    <div class="alert alert-warning mt-2">
                        <strong>⚠️ Spending Changes Required:</strong> {{ pred['spending_changes_needed'] }}
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    requests_df = loader.requests_df
    request_ids = requests_df["request_id"].tolist()
    
    selected_id = request.args.get("request_id", request_ids[0])
    if selected_id not in request_ids:
        selected_id = request_ids[0]
        
    req_row = requests_df[requests_df["request_id"] == selected_id].iloc[0]
    user_id = str(req_row["user_id"])
    prof = loader.get_user_profile(user_id)
    currency = prof.get("home_currency", "USD")
    
    # Run evaluation
    pred = engine.evaluate_request(req_row)
    
    # Format plan data
    plan_data = []
    if pred["payment_plan"] != "none":
        for item in pred["payment_plan"].split("|"):
            parts = item.split(":")
            plan_data.append({"date": parts[0], "amount": float(parts[1])})

    requests_map = {r["request_id"]: {"user_id": r["user_id"]} for _, r in requests_df.iterrows()}

    return render_template_string(
        HTML_TEMPLATE,
        request_ids=request_ids,
        selected_id=selected_id,
        requests_map=requests_map,
        req_row=req_row,
        user_id=user_id,
        profile=prof,
        currency=currency,
        pred=pred,
        plan_data=plan_data
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
