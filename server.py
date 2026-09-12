"""Flask Web Dashboard for Buy or Wait? — AI Financial Decision Agent.
Tailored for Indian Households, Culture, and New User Interactive Simulation.
"""
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
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


def format_inr(val):
    """Format amount using Indian numbering system (Lakhs & Crores)."""
    try:
        val = float(val)
    except (ValueError, TypeError):
        return f"₹{val}"
    int_val = int(round(val))
    s = str(abs(int_val))
    if len(s) <= 3:
        res = s
    else:
        res = s[-3:]
        s = s[:-3]
        while len(s) > 2:
            res = s[-2:] + "," + res
            s = s[:-2]
        if s:
            res = s + "," + res
    prefix = "-₹" if val < 0 else "₹"
    return f"{prefix}{res}"


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buy or Wait? — AI Financial Advisor (Bachat & Kharch Guru)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1e293b; }
        .hero { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #047857 100%); color: white; padding: 35px 0; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .nav-pills .nav-link { font-weight: 600; border-radius: 8px; padding: 10px 20px; color: #475569; }
        .nav-pills .nav-link.active { background-color: #047857; color: white; }
        .card { border-radius: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .badge-status { font-size: 0.95rem; padding: 8px 16px; border-radius: 30px; font-weight: 700; display: inline-block; }
        .status-affordable_now { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
        .status-affordable_with_plan { background-color: #dbeafe; color: #1d4ed8; border: 1px solid #93c5fd; }
        .status-affordable_later { background-color: #fef9c3; color: #a16207; border: 1px solid #fde047; }
        .status-not_affordable { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
        .metric-title { font-size: 0.8rem; color: #64748b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
        .metric-value { font-size: 1.4rem; font-weight: 700; color: #0f172a; }
        .tip-box { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 15px; border-radius: 8px; }
        .warning-box { background-color: #fffbeb; border-left: 5px solid #f59e0b; padding: 15px; border-radius: 8px; }
        .danger-box { background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 15px; border-radius: 8px; }
        .step-badge { background-color: #047857; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 8px; }
    </style>
</head>
<body>
    <!-- Top Hero Banner -->
    <div class="hero">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h1 class="fw-bold mb-1"><i class="bi bi-wallet2 me-2"></i>Buy or Wait? (खरीदें या रुकें?)</h1>
                    <p class="mb-0 text-light opacity-75">Autonomous AI Financial Affordability Advisor — Tailored for Indian Household Cash Flow & Smart Budgeting</p>
                </div>
                <div class="text-end d-none d-md-block">
                    <span class="badge bg-success px-3 py-2 fs-6"><i class="bi bi-shield-check me-1"></i>Emergency Fund Protected</span>
                </div>
            </div>
        </div>
    </div>

    <div class="container mb-5">
        <!-- Tab Navigation -->
        <ul class="nav nav-pills mb-4" id="pills-tab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link {% if active_tab == 'custom' %}active{% endif %}" id="custom-tab" data-bs-toggle="pill" data-bs-target="#tab-custom" type="button">
                    <i class="bi bi-person-plus me-1"></i> 1. Naya Kharch Test Karein (New User Simulator)
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link {% if active_tab == 'eval' %}active{% endif %}" id="eval-tab" data-bs-toggle="pill" data-bs-target="#tab-eval" type="button">
                    <i class="bi bi-database-check me-1"></i> 2. Benchmark Requests Explorer (250 Cases)
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="guide-tab" data-bs-toggle="pill" data-bs-target="#tab-guide" type="button">
                    <i class="bi bi-book me-1"></i> 3. Desi Bachat & Rulebook Guide
                </button>
            </li>
        </ul>

        <div class="tab-content" id="pills-tabContent">
            <!-- TAB 1: NEW USER SIMULATOR -->
            <div class="tab-pane fade {% if active_tab == 'custom' %}show active{% endif %}" id="tab-custom">
                <!-- How to use banner -->
                <div class="card p-3 mb-4 bg-light border-0">
                    <h6 class="fw-bold mb-2"><i class="bi bi-info-circle-fill text-success me-2"></i>Naye User Isko Kaise Use Karein? (3 Simple Steps)</h6>
                    <div class="row g-3 small">
                        <div class="col-md-4">
                            <span class="step-badge">1</span> <strong>Apna Budget Bhariye:</strong> Bank balance, in-hand salary aur emergency fund enter karein.
                        </div>
                        <div class="col-md-4">
                            <span class="step-badge">2</span> <strong>Kharch Details Daaliye:</strong> Jo phone, bike, ya festival shopping karni hai uska price likhiye.
                        </div>
                        <div class="col-md-4">
                            <span class="step-badge">3</span> <strong>AI Verdict Dekhiye:</strong> AI batayega ki abhi lena safe hai, EMI leni chahiye, ya salary ka wait karna chahiye.
                        </div>
                    </div>
                </div>

                <div class="row">
                    <!-- Form Column -->
                    <div class="col-lg-5">
                        <div class="card p-4">
                            <h5 class="fw-bold mb-3"><i class="bi bi-calculator me-2"></i>Apna Kharch & Balance Daalein</h5>
                            <form method="POST" action="/simulate">
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">Kya khareedna chahte hain? (Item Name)</label>
                                    <input type="text" name="item_name" class="form-control" value="{{ sim_data.item_name }}" placeholder="e.g. iPhone 16, Royal Enfield, TV, Diwali Shopping" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">Khareed Amount (₹ Price)</label>
                                    <input type="number" name="item_price" class="form-control" value="{{ sim_data.item_price }}" placeholder="e.g. 50000" required>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">Bank Balance (Today)</label>
                                        <input type="number" name="bank_balance" class="form-control" value="{{ sim_data.bank_balance }}" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">Emergency Fund (Min)</label>
                                        <input type="number" name="min_balance" class="form-control" value="{{ sim_data.min_balance }}" required>
                                        <small class="text-muted">Suraksha Nidhi (never touch)</small>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">Monthly In-Hand Salary</label>
                                        <input type="number" name="salary" class="form-control" value="{{ sim_data.salary }}" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">Salary Day of Month</label>
                                        <select name="payday" class="form-select">
                                            <option value="1" {% if sim_data.payday == 1 %}selected{% endif %}>1st of Month</option>
                                            <option value="7" {% if sim_data.payday == 7 %}selected{% endif %}>7th of Month</option>
                                            <option value="15" {% if sim_data.payday == 15 %}selected{% endif %}>15th of Month</option>
                                            <option value="30" {% if sim_data.payday == 30 %}selected{% endif %}>Month End (30th)</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">Monthly Fixed Kharch (Rent + Kirana + EMIs + Bills)</label>
                                    <input type="number" name="monthly_expenses" class="form-control" value="{{ sim_data.monthly_expenses }}" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">EMI Option Available?</label>
                                    <select name="emi_available" class="form-select">
                                        <option value="yes" {% if sim_data.emi_available == 'yes' %}selected{% endif %}>Yes (3/6 Months No-Cost EMI Available)</option>
                                        <option value="no" {% if sim_data.emi_available == 'no' %}selected{% endif %}>No (Full Payment Only)</option>
                                    </select>
                                </div>
                                <button type="submit" class="btn btn-success w-100 py-2 fw-bold">
                                    <i class="bi bi-magic me-1"></i> AI Financial Reality Check Karein
                                </button>
                            </form>
                        </div>
                    </div>

                    <!-- Result Column -->
                    <div class="col-lg-7">
                        <div class="card p-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold mb-0"><i class="bi bi-award me-2"></i>AI Recommendation Result</h5>
                                <span class="badge-status status-{{ sim_result.status_code }}">
                                    {{ sim_result.status_label }}
                                </span>
                            </div>

                            <!-- Key Metrics Row -->
                            <div class="row mb-4">
                                <div class="col-sm-4">
                                    <div class="metric-title">Safe To Pay Today</div>
                                    <div class="metric-value text-success">{{ format_inr(sim_result.safe_today) }}</div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="metric-title">Available Cushion</div>
                                    <div class="metric-value text-primary">{{ format_inr(sim_result.cushion) }}</div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="metric-title">Monthly Net Savings</div>
                                    <div class="metric-value text-dark">{{ format_inr(sim_result.monthly_savings) }}</div>
                                </div>
                            </div>

                            <!-- Verdict Box -->
                            <div class="{{ sim_result.box_class }} mb-3">
                                <h6 class="fw-bold"><i class="{{ sim_result.icon_class }} me-2"></i>{{ sim_result.headline }}</h6>
                                <p class="mb-0">{{ sim_result.detailed_explanation }}</p>
                            </div>

                            <!-- Recommended Plan -->
                            <div class="card p-3 bg-light border-0 mb-3">
                                <h6 class="fw-bold text-muted mb-2"><i class="bi bi-calendar-event me-2"></i>Recommended Action Plan</h6>
                                <p class="mb-1"><strong>Action:</strong> <span class="badge bg-secondary">{{ sim_result.recommended_method }}</span></p>
                                <p class="mb-1"><strong>Schedule:</strong> {{ sim_result.plan_text }}</p>
                                {% if sim_result.wait_date %}
                                <p class="mb-0"><strong>Earliest Safe Date:</strong> <code>{{ sim_result.wait_date }}</code></p>
                                {% endif %}
                            </div>

                            <!-- Desi Financial Wisdom Tip -->
                            <div class="tip-box">
                                <strong><i class="bi bi-lightbulb-fill text-warning me-1"></i> Desi Financial Advice:</strong><br>
                                {{ sim_result.desi_tip }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 2: BENCHMARK DATASET EXPLORER -->
            <div class="tab-pane fade {% if active_tab == 'eval' %}show active{% endif %}" id="tab-eval">
                <div class="row">
                    <div class="col-md-4">
                        <div class="card p-4">
                            <h5 class="fw-bold mb-3">Select Evaluation Request</h5>
                            <form method="GET" action="/">
                                <input type="hidden" name="tab" value="eval">
                                <div class="mb-3">
                                    <label class="form-label text-muted">Choose Request (1 to 250):</label>
                                    <select name="request_id" class="form-select" onchange="this.form.submit()">
                                        {% for r_id in request_ids %}
                                            <option value="{{ r_id }}" {% if r_id == selected_id %}selected{% endif %}>
                                                {{ r_id }} ({{ requests_map[r_id]['user_id'] }})
                                            </option>
                                        {% endfor %}
                                    </select>
                                </div>
                            </form>
                            <hr>
                            <h6 class="fw-bold text-muted">Indian Financial Profile Context</h6>
                            <ul class="list-unstyled small text-muted">
                                <li><strong>User ID:</strong> {{ user_id }}</li>
                                <li><strong>Currency:</strong> {{ currency }}</li>
                                <li><strong>Protected Essentials:</strong> {{ profile['expense_categories_to_protect'] }}</li>
                                <li><strong>Allowed Adjustments:</strong> {{ profile['expense_categories_user_is_willing_to_reduce'] }}</li>
                                <li><strong>Payment Preference:</strong> {{ profile['payment_methods_user_will_consider'] }}</li>
                            </ul>
                        </div>
                    </div>

                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">Category</div>
                                    <div class="metric-value fs-6">{{ req_row['request_type']|capitalize }}</div>
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">Requested</div>
                                    <div class="metric-value fs-6">{{ format_inr(req_row['requested_amount']) }}</div>
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">Available Balance</div>
                                    <div class="metric-value fs-6">{{ format_inr(profile['current_available_balance']) }}</div>
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">Min Balance</div>
                                    <div class="metric-value fs-6">{{ format_inr(profile['minimum_balance_to_keep']) }}</div>
                                </div>
                            </div>
                        </div>

                        <div class="card p-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold mb-0">AI Decision Rationale</h5>
                                <span class="badge-status status-{{ pred['affordability_status'] }}">
                                    {{ pred['affordability_status'].replace('_', ' ') }}
                                </span>
                            </div>

                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <p class="mb-1 text-muted">Recommended Method:</p>
                                    <h5 class="text-primary fw-bold">{{ pred['recommended_payment_method'].replace('_', ' ').title() }}</h5>
                                </div>
                                <div class="col-md-6">
                                    <p class="mb-1 text-muted">Amount Safe Today:</p>
                                    <h5 class="text-success fw-bold">{{ format_inr(pred['amount_safe_to_pay']) }}</h5>
                                </div>
                            </div>

                            <div class="tip-box mb-3">
                                <strong>💡 Grounded Decision Explanation:</strong><br>
                                {{ pred['decision_explanation'] }}
                            </div>

                            {% if pred['earliest_date_for_full_payment'] %}
                            <p class="mb-2"><strong>Earliest Safe Date for Full Payment:</strong> <code>{{ pred['earliest_date_for_full_payment'] }}</code></p>
                            {% endif %}

                            {% if plan_data %}
                            <h6 class="fw-bold mt-3">Payment Plan Timeline:</h6>
                            <table class="table table-bordered table-sm mt-2">
                                <thead class="table-light">
                                    <tr>
                                        <th>Payment #</th>
                                        <th>Date</th>
                                        <th>Amount</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in plan_data %}
                                    <tr>
                                        <td>Payment {{ loop.index }}</td>
                                        <td><code>{{ row['date'] }}</code></td>
                                        <td class="fw-bold">{{ format_inr(row['amount']) }}</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                            {% endif %}

                            {% if pred['spending_changes_needed'] != 'none' %}
                            <div class="alert alert-warning mt-2">
                                <strong>⚠️ Recommended Spending Cut:</strong> {{ pred['spending_changes_needed'] }}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 3: DESI FINANCIAL RULEBOOK -->
            <div class="tab-pane fade" id="tab-guide">
                <div class="card p-4">
                    <h4 class="fw-bold mb-3"><i class="bi bi-compass me-2"></i>Indian Household Financial Principles & Culture</h4>
                    <p class="text-muted">Ye system Indian middle-class aur salaried families ke real-world financial rules par adharit hai:</p>

                    <div class="row g-4 mt-2">
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-success border-4">
                                <h6 class="fw-bold text-success"><i class="bi bi-shield-lock me-2"></i>1. Suraksha Kavach (Emergency Nidhi)</h6>
                                <p class="small text-muted mb-0">Indian households hamesha 3 se 6 mahine ka emergency balance rakhna chahte hain (health issues, job uncertainty, ya sudden expenses ke liye). AI agent kisi bhi purchase ke liye is minimum balance ko kabhi touch nahi karta.</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-primary border-4">
                                <h6 class="fw-bold text-primary"><i class="bi bi-cart4 me-2"></i>2. Roti, Kapda, Kirana & Parivaar Support</h6>
                                <p class="small text-muted mb-0">Rent, bijli ka bill, bacchon ki school fees, aur mata-pita ko bheje jane wale paise (Family Support) ko **Protected Categories** mein rakha gaya hai. AI inme se ek rupaye ki bhi katauti nahi karta.</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-warning border-4">
                                <h6 class="fw-bold text-warning"><i class="bi bi-clock-history me-2"></i>3. Mahine Ka Aakhri Hafta (Salary Cycle)</h6>
                                <p class="small text-muted mb-0">Agar purchase month-end par ho raha hai aur balance kam hai, toh AI user ko bolta hai: <em>"Salary aane tak 5-10 din wait kar lo"</em>, taaki mahine ke aakhri dino mein cash crunch na ho.</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-danger border-4">
                                <h6 class="fw-bold text-danger"><i class="bi bi-credit-card-2-front me-2"></i>4. No-Cost EMI vs Debt Trap Check</h6>
                                <p class="small text-muted mb-0">Credit card EMIs tabhi recommend ki jaati hain jab monthly installment user ke surplus cash flow ke andar fit ho rahi ho. Agar EMI se budget hilne ka risk ho, toh AI seedha mana kar deta hai.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


def calculate_simulation(item_name, item_price, bank_balance, min_balance, salary, payday, monthly_expenses, emi_available):
    """Run an Indian cultural affordability logic on custom user inputs."""
    cushion = max(0.0, bank_balance - min_balance)
    monthly_savings = max(0.0, salary - monthly_expenses)
    
    # Calculate days to next payday (simulate from 12th of month)
    sim_current_day = 12
    if payday >= sim_current_day:
        days_to_payday = payday - sim_current_day
    else:
        days_to_payday = (30 - sim_current_day) + payday
    
    # Conservative daily essential expenses before payday
    daily_spend = monthly_expenses / 30.0
    commitments_before_payday = daily_spend * days_to_payday
    safe_today = max(0.0, min(item_price, cushion - commitments_before_payday))
    
    # Today's date simulation
    today = datetime(2026, 9, 12).date()
    next_payday = today + timedelta(days=days_to_payday)
    payday_2 = next_payday + timedelta(days=30)
    payday_3 = payday_2 + timedelta(days=30)

    # 1. Full Payment Affordable Now
    if safe_today >= item_price:
        return {
            "status_code": "affordable_now",
            "status_label": "AFFORDABLE NOW (खूब आराम से ले सकते हैं)",
            "safe_today": safe_today,
            "cushion": cushion,
            "monthly_savings": monthly_savings,
            "headline": f"Aap {item_name} abhi khareed sakte hain!",
            "detailed_explanation": f"Aapka emergency fund ({format_inr(min_balance)}) poori tarah surakshit hai aur agle mahine ki salary aane tak ke saare kharche nikaalne ke baad bhi aapke paas poore paise hain.",
            "recommended_method": "Full Payment (One-Time)",
            "plan_text": f"Poora {format_inr(item_price)} aaj hi pay kar dein.",
            "wait_date": None,
            "box_class": "tip-box",
            "icon_class": "bi bi-check-circle-fill text-success",
            "desi_tip": f"Badiya decision! Khareedne ke baad bhi aapke bank mein kam se kam {format_inr(min_balance)} ka suraksha kavach bana rahega."
        }

    # 2. Affordable with EMI
    if emi_available == "yes":
        for months in [3, 6]:
            monthly_emi = item_price / months
            # Check if monthly_emi <= 60% of monthly savings
            if monthly_savings >= monthly_emi * 1.2 and cushion >= monthly_emi:
                return {
                    "status_code": "affordable_with_plan",
                    "status_label": f"AFFORDABLE WITH PLAN ({months} Mahine Ki EMI)",
                    "safe_today": safe_today,
                    "cushion": cushion,
                    "monthly_savings": monthly_savings,
                    "headline": f"Full payment se bachein, {months} Mahine ki No-Cost EMI lein!",
                    "detailed_explanation": f"Ek saath {format_inr(item_price)} dene se aapka emergency balance kam ho jayega. Lekin aapki bachat ({format_inr(monthly_savings)}/month) se {format_inr(monthly_emi)}/month ki EMI aasaani se nikal jayegi.",
                    "recommended_method": f"Installments ({months} Months)",
                    "plan_text": f"{months} kishtein of {format_inr(monthly_emi)} har mahine.",
                    "wait_date": None,
                    "box_class": "tip-box",
                    "icon_class": "bi bi-credit-card text-primary",
                    "desi_tip": f"No-Cost EMI chuniyega taaki koi extra interest na lage, aur pehli installment ke baad bhi budget stable rahe."
                }

    # 3. Affordable Later (Wait for Payday)
    # Check if Payday 1, 2 or 3 can cover it
    if cushion + monthly_savings >= item_price:
        wait_date_str = next_payday.strftime("%d %B %Y")
        return {
            "status_code": "affordable_later",
            "status_label": "AFFORDABLE LATER (अगली सैलरी तक रुकें)",
            "safe_today": safe_today,
            "cushion": cushion,
            "monthly_savings": monthly_savings,
            "headline": f"Abhi mat lijiye, {wait_date_str} (Payday) tak rukiye!",
            "detailed_explanation": f"Abhi aapke paas sirf {format_inr(safe_today)} safe hai. Agle salary credit ({wait_date_str}) ke baad aapka balance badhega aur aap bina kisi tension ke poora payment kar sakenge.",
            "recommended_method": "Wait for Payday",
            "plan_text": f"Pay {format_inr(item_price)} on {wait_date_str}.",
            "wait_date": wait_date_str,
            "box_class": "warning-box",
            "icon_class": "bi bi-hourglass-split text-warning",
            "desi_tip": "30-Day Rule: Kisi bhi bade kharch ko salary aane tak taalna impulse spending se bachne ka sabse badiya desi tareeqa hai."
        }
    elif cushion + 2 * monthly_savings >= item_price:
        wait_date_str = payday_2.strftime("%d %B %Y")
        return {
            "status_code": "affordable_later",
            "status_label": "AFFORDABLE LATER (2 Mahine Ki Bachat Baad)",
            "safe_today": safe_today,
            "cushion": cushion,
            "monthly_savings": monthly_savings,
            "headline": f"Thoda intezaar karein, {wait_date_str} ko lena safe hoga!",
            "detailed_explanation": f"Aapki monthly bachat {format_inr(monthly_savings)} hai. Agle 2 mahine mein zaroori bachat jama ho jayegi jisse emergency fund chhede bina purchase ho sakega.",
            "recommended_method": "Wait (2 Paydays)",
            "plan_text": f"Pay {format_inr(item_price)} on {wait_date_str}.",
            "wait_date": wait_date_str,
            "box_class": "warning-box",
            "icon_class": "bi bi-hourglass-split text-warning",
            "desi_tip": "Agar koi festival sale aane wali hai toh tab tak wait karein, cashback ya discount mil sakta hai!"
        }

    # 4. Not Affordable
    return {
        "status_code": "not_affordable",
        "status_label": "NOT AFFORDABLE (अभी बिल्कुल न लें)",
        "safe_today": safe_today,
        "cushion": cushion,
        "monthly_savings": monthly_savings,
        "headline": f"Abhi {item_name} lena budget ke liye khatarnaak hai!",
        "detailed_explanation": f"Aapka item price ({format_inr(item_price)}) aapke available cushion ({format_inr(cushion)}) se bohot zyada hai aur agle 90 dinon mein bhi ise safely afford nahi kiya ja sakta.",
        "recommended_method": "Not Recommended (Postpone)",
        "plan_text": "Abhi koi payment plan recommend nahi kiya jata.",
        "wait_date": None,
        "box_class": "danger-box",
        "icon_class": "bi bi-exclamation-octagon-fill text-danger",
        "desi_tip": "Karz (debt) lekar ya Emergency fund tod kar aisi purchases na karein. Pehle 3-6 mahine SIP ya RD mein bachat karein."
    }


@app.route("/", methods=["GET"])
def home():
    active_tab = request.args.get("tab", "custom")
    requests_df = loader.requests_df
    request_ids = requests_df["request_id"].tolist()
    selected_id = request.args.get("request_id", request_ids[0])
    if selected_id not in request_ids:
        selected_id = request_ids[0]

    req_row = requests_df[requests_df["request_id"] == selected_id].iloc[0]
    user_id = str(req_row["user_id"])
    prof = loader.get_user_profile(user_id)
    currency = prof.get("home_currency", "INR")
    pred = engine.evaluate_request(req_row)

    plan_data = []
    if pred["payment_plan"] != "none":
        for item in pred["payment_plan"].split("|"):
            parts = item.split(":")
            plan_data.append({"date": parts[0], "amount": float(parts[1])})

    requests_map = {r["request_id"]: {"user_id": r["user_id"]} for _, r in requests_df.iterrows()}

    # Default custom simulation data
    default_sim_data = {
        "item_name": "OnePlus Smartphone",
        "item_price": 38000,
        "bank_balance": 55000,
        "min_balance": 20000,
        "salary": 65000,
        "payday": 1,
        "monthly_expenses": 42000,
        "emi_available": "yes"
    }
    sim_result = calculate_simulation(**default_sim_data)

    return render_template_string(
        HTML_TEMPLATE,
        active_tab=active_tab,
        request_ids=request_ids,
        selected_id=selected_id,
        requests_map=requests_map,
        req_row=req_row,
        user_id=user_id,
        profile=prof,
        currency=currency,
        pred=pred,
        plan_data=plan_data,
        sim_data=default_sim_data,
        sim_result=sim_result,
        format_inr=format_inr
    )


@app.route("/simulate", methods=["POST"])
def simulate():
    sim_data = {
        "item_name": request.form.get("item_name", "Desired Purchase"),
        "item_price": float(request.form.get("item_price", 40000)),
        "bank_balance": float(request.form.get("bank_balance", 50000)),
        "min_balance": float(request.form.get("min_balance", 20000)),
        "salary": float(request.form.get("salary", 60000)),
        "payday": int(request.form.get("payday", 1)),
        "monthly_expenses": float(request.form.get("monthly_expenses", 35000)),
        "emi_available": request.form.get("emi_available", "yes")
    }
    sim_result = calculate_simulation(**sim_data)

    requests_df = loader.requests_df
    request_ids = requests_df["request_id"].tolist()
    req_row = requests_df.iloc[0]
    user_id = str(req_row["user_id"])
    prof = loader.get_user_profile(user_id)
    pred = engine.evaluate_request(req_row)
    requests_map = {r["request_id"]: {"user_id": r["user_id"]} for _, r in requests_df.iterrows()}

    return render_template_string(
        HTML_TEMPLATE,
        active_tab="custom",
        request_ids=request_ids,
        selected_id=request_ids[0],
        requests_map=requests_map,
        req_row=req_row,
        user_id=user_id,
        profile=prof,
        currency="INR",
        pred=pred,
        plan_data=[],
        sim_data=sim_data,
        sim_result=sim_result,
        format_inr=format_inr
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
