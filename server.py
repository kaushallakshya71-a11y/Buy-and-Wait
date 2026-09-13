"""Flask Web Dashboard for Buy or Wait? — AI Financial Decision Agent.
Bilingual Support: English (Default / Priority 1) and Hindi/Hinglish (Priority 2).
"""
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string

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


TEXTS = {
    "en": {
        "title": "Buy or Wait? — AI Financial Decision Agent",
        "subtitle": "Autonomous AI Financial Affordability & Cash-Flow Advisor — Tailored for Indian Household Economics",
        "emergency_protected": "Emergency Fund Protected",
        "tab_custom": "1. Test a Purchase (Simulator)",
        "tab_eval": "2. Benchmark Requests Explorer (250 Cases)",
        "tab_guide": "3. Financial Principles & Guidelines",
        "tab_user_guide": "4. User Guide & FAQs",
        "how_it_works_title": "How to Use in 3 Simple Steps",
        "step_1": "Enter Your Finances: Current balance, in-hand salary, and minimum emergency reserve.",
        "step_2": "Specify Your Purchase: Item name, price, and payment preferences.",
        "step_3": "Get AI Verdict: Real-time decision whether to pay in full, use EMI, wait for payday, or postpone.",
        "form_title": "Enter Your Purchase & Financial Details",
        "lbl_item_name": "What do you plan to buy? (Item Name)",
        "lbl_item_price": "Purchase Price (₹)",
        "lbl_bank_balance": "Current Bank Balance",
        "lbl_min_balance": "Emergency Fund to Keep",
        "lbl_min_balance_sub": "Safety reserve (never touch)",
        "lbl_salary": "Monthly In-Hand Salary",
        "lbl_payday": "Salary Credit Date",
        "lbl_expenses": "Monthly Fixed Expenses (Rent + Kirana + EMIs + Bills)",
        "lbl_emi": "Is No-Cost EMI Available?",
        "emi_yes": "Yes (3 / 6 Months No-Cost EMI Available)",
        "emi_no": "No (Full Payment Only)",
        "btn_calculate": "Run AI Financial Reality Check",
        "res_title": "AI Decision & Recommendation",
        "metric_safe_today": "Safe To Pay Today",
        "metric_cushion": "Available Cash Cushion",
        "metric_savings": "Monthly Net Savings",
        "lbl_plan_action": "Recommended Action Plan",
        "lbl_action": "Action",
        "lbl_schedule": "Schedule",
        "lbl_earliest_safe": "Earliest Safe Date",
        "lbl_tip_title": "Financial Insight & Prudence Tip",
        "eval_select_title": "Select Evaluation Request",
        "eval_choose_lbl": "Choose Request ID (1 to 250):",
        "eval_profile_title": "User Financial Profile Context",
        "eval_cat": "Category",
        "eval_req": "Requested",
        "eval_bal": "Available Balance",
        "eval_min": "Min Balance",
        "eval_rationale": "Grounded Decision Explanation",
        "eval_timeline": "Payment Plan Timeline:",
        "guide_title": "Indian Household Financial Principles",
        "guide_sub": "Core financial ground rules designed for Indian middle-class and salaried households:",
        "g1_title": "1. Emergency Nidhi (Safety Reserve)",
        "g1_desc": "Households require 3 to 6 months of living expenses for health crises, job shifts, or unforeseen events. The AI agent strictly enforces that this minimum balance is never breached.",
        "g2_title": "2. Essential Needs & Family Support",
        "g2_desc": "Rent, groceries/ration, school fees, and allowances sent to parents (Family Support) are protected categories. Zero cuts are permitted from these essential commitments.",
        "g3_title": "3. Salary Cycle & Month-End Crunch",
        "g3_desc": "When purchases occur late in the monthly salary cycle (25th–30th), the AI recommends waiting a few days for salary settlement to prevent month-end liquidity stress.",
        "g4_title": "4. Zero-Cost EMI vs Debt Trap Prevention",
        "g4_desc": "Installments are recommended only when the monthly commitment is comfortably covered by net surplus savings, ensuring you never fall into credit card rollover debt.",
        "user_guide_heading": "Comprehensive User Guide & Help Center",
        "user_guide_subheading": "Everything you need to know about making smart, debt-free financial decisions with Buy or Wait AI.",
        "ug_card1_title": "Understanding Financial Inputs",
        "ug_card1_desc": "Your Available Balance is liquid cash today. Emergency Fund is your untouchable safety cushion (3-6 months living expenses).",
        "ug_card2_title": "How 90-Day Simulation Works",
        "ug_card2_desc": "The engine tests every single day over the next 90 days, subtracting rent, bills, groceries, and debt EMIs to guarantee you never drop below your emergency threshold.",
        "ug_card3_title": "Interpreting AI Verdicts",
        "ug_card3_desc": "🟢 Affordable Now = Buy today. 🔵 Affordable with Plan = Take No-Cost EMI. 🟡 Affordable Later = Wait for Payday. 🔴 Not Affordable = Postpone.",
        "faq1_q": "Why was my purchase rejected even though my bank balance is higher than the price?",
        "faq1_a": "Because of your Emergency Fund and upcoming fixed debits (rent, groceries, bills) before your next salary credit. If your balance is ₹50,000 and the item is ₹40,000, but your emergency reserve is ₹25,000, your spendable cushion is only ₹25,000. The AI strictly refuses to gamble with your safety net.",
        "faq2_q": "When does the AI recommend a No-Cost EMI instead of full payment?",
        "faq2_a": "When paying in full would drain your emergency reserve below the safety threshold, but your monthly surplus savings (Salary minus Fixed Expenses) can comfortably cover the monthly installment.",
        "faq3_q": "What is the '30-Day Bachat Rule' behind the Wait recommendation?",
        "faq3_a": "When a purchase is deferred until your next salary date, it protects your month-end liquidity and prevents impulse spending. If you still desire the item after payday, you can purchase it safely.",
        "faq4_q": "Is my personal financial data secure and private?",
        "faq4_a": "Yes, 100%. All calculations and simulations execute entirely locally on your machine. Zero financial data is sent to external servers or cloud APIs."
    },
    "hi": {
        "title": "Buy or Wait? (खरीदें या रुकें?)",
        "subtitle": "Autonomous AI Financial Affordability Advisor — Indian Household Cash Flow & Smart Budgeting",
        "emergency_protected": "Emergency Fund Surakshit",
        "tab_custom": "1. Naya Kharch Test Karein (New User Simulator)",
        "tab_eval": "2. Benchmark Requests Explorer (250 Cases)",
        "tab_guide": "3. Desi Bachat & Rulebook Guide",
        "tab_user_guide": "4. User Guide & FAQs (सवालों के जवाब)",
        "how_it_works_title": "Naye User Isko Kaise Use Karein? (3 Simple Steps)",
        "step_1": "Apna Budget Bhariye: Bank balance, in-hand salary aur emergency fund enter karein.",
        "step_2": "Kharch Details Daaliye: Jo phone, bike, ya shopping karni hai uska price likhiye.",
        "step_3": "AI Verdict Dekhiye: AI batayega ki abhi lena safe hai, EMI leni chahiye, ya salary ka wait karna hai.",
        "form_title": "Apna Kharch & Balance Daalein",
        "lbl_item_name": "Kya khareedna chahte hain? (Item Name)",
        "lbl_item_price": "Khareed Amount (₹ Price)",
        "lbl_bank_balance": "Bank Balance (Today)",
        "lbl_min_balance": "Emergency Fund (Min Balance)",
        "lbl_min_balance_sub": "Suraksha Nidhi (jo kabhi nahi chhedna)",
        "lbl_salary": "Monthly In-Hand Salary",
        "lbl_payday": "Salary Credit Date",
        "lbl_expenses": "Monthly Fixed Kharch (Rent + Kirana + EMIs + Bills)",
        "lbl_emi": "Kya EMI Option Available Hai?",
        "emi_yes": "Haan (3 / 6 Mahine Ki No-Cost EMI Available Hai)",
        "emi_no": "Nahi (Full Payment Only)",
        "btn_calculate": "AI Financial Reality Check Karein",
        "res_title": "AI Recommendation Result",
        "metric_safe_today": "Safe To Pay Today",
        "metric_cushion": "Available Cushion",
        "metric_savings": "Monthly Net Savings",
        "lbl_plan_action": "Recommended Action Plan",
        "lbl_action": "Action",
        "lbl_schedule": "Schedule",
        "lbl_earliest_safe": "Earliest Safe Date",
        "lbl_tip_title": "Desi Financial Advice",
        "eval_select_title": "Select Evaluation Request",
        "eval_choose_lbl": "Request Chuniye (1 to 250):",
        "eval_profile_title": "Financial Profile Context",
        "eval_cat": "Category",
        "eval_req": "Requested",
        "eval_bal": "Available Balance",
        "eval_min": "Min Balance",
        "eval_rationale": "AI Decision Rationale",
        "eval_timeline": "Payment Plan Timeline:",
        "guide_title": "Indian Household Financial Principles & Culture",
        "guide_sub": "Ye system Indian middle-class aur salaried families ke real-world financial rules par adharit hai:",
        "g1_title": "1. Suraksha Kavach (Emergency Nidhi)",
        "g1_desc": "Indian households hamesha 3 se 6 mahine ka emergency balance bachakar rakhte hain. AI kisi bhi purchase ke liye is minimum balance ko kabhi touch nahi karta.",
        "g2_title": "2. Roti, Kirana & Parivaar Support",
        "g2_desc": "Rent, bijli ka bill, bacchon ki school fees, aur parents ko bheje jaane wale paise (Family Support) protected hain. Inme se ₹1 ki bhi katauti nahi hoti.",
        "g3_title": "3. Mahine Ka Aakhri Hafta (Salary Cycle)",
        "g3_desc": "Agar purchase month-end par ho raha ho, toh AI user ko bolta hai: 'Salary aane tak 5-10 din wait kar lo', taaki month-end cash crunch na ho.",
        "g4_title": "4. No-Cost EMI vs Debt Trap Check",
        "g4_desc": "EMIs tabhi recommend hoti hain jab monthly installment user ke surplus cash flow mein fit ho rahi ho, taaki credit card debt trap se bacha ja sake.",
        "user_guide_heading": "User Guide & Madad Kendra (FAQs)",
        "user_guide_subheading": "Buy or Wait AI ke saath bina kisi karz (debt) ke smart financial decision lene ki poori jaankari.",
        "ug_card1_title": "Financial Inputs Ko Samajhein",
        "ug_card1_desc": "Bank Balance aapka aaj ka liquid paisa hai. Emergency Fund aapka suraksha kavach hai (3-6 mahine ka kharcha) jise kabhi chhedna nahi hai.",
        "ug_card2_title": "90-Din Ka Simulation Kaise Kaam Karta Hai",
        "ug_card2_desc": "Engine agle 90 din ke har ek din par check karta hai aur rent, ration, EMIs nikaalne ke baad dekhta hai ki balance safe hai ya nahi.",
        "ug_card3_title": "AI Verdicts Ka Matlab",
        "ug_card3_desc": "🟢 Affordable Now = Aaj khareedo. 🔵 Affordable with Plan = No-Cost EMI lo. 🟡 Affordable Later = Salary ka wait karo. 🔴 Not Affordable = Abhi cancel karo.",
        "faq1_q": "Bank balance hone ke baad bhi AI ne purchase reject kyu kiya?",
        "faq1_a": "Kyunki aapke balance mein se Emergency Fund aur agle salary aane tak ke zaroori kharche (Rent, Ration, Bills) minus kiye jaate hain. Agar balance ₹50,000 hai aur phone ₹40,000 ka hai lekin Emergency fund ₹25,000 hai, toh safe bachat sirf ₹25,000 hai. AI aapki safety se samjhauta nahi karta.",
        "faq2_q": "Full payment ke badle No-Cost EMI kab recommend hoti hai?",
        "faq2_a": "Jab ek saath poora paisa dene se emergency fund kam ho raha ho, lekin aapki monthly bachat (Salary minus Kharch) aasaani se har mahine ki installment nikaal sakti ho.",
        "faq3_q": "Wait recommendation ke peeche '30-Day Bachat Niyam' kya hai?",
        "faq3_a": "Jab kisi bade kharch ko agli salary tak taal diya jata hai, toh impulsive shopping se bachav hota hai aur mahine ke aakhri dino mein cash crunch nahi hota.",
        "faq4_q": "Kya mera financial data safe aur private hai?",
        "faq4_a": "Haan, bilkul 100%. Saare calculations aapke computer par locally run hote hain. Koi bhi data kisi third-party server par nahi jata."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t['title'] }} — Autonomous AI Financial Decision Agent</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        :root {
            --primary: #047857;
            --primary-dark: #065f46;
            --primary-light: #10b981;
            --slate-900: #0f172a;
            --slate-800: #1e293b;
            --slate-700: #334155;
            --slate-100: #f1f5f9;
            --slate-50: #f8fafc;
        }
        body { 
            background-color: #f8fafc; 
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            color: #1e293b; 
            overflow-x: hidden;
        }
        /* Sticky Glass Navbar */
        .glass-navbar {
            background: rgba(15, 23, 42, 0.94);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
            padding: 12px 0;
            z-index: 1050;
        }
        .brand-logo-badge {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #10b981, #047857);
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
        }
        .brand-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        .brand-dot {
            color: #10b981;
        }
        .badge-orchestrate {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 8px;
        }
        .navbar-nav .nav-link {
            font-weight: 600;
            font-size: 0.9rem;
            color: #94a3b8;
            padding: 8px 16px;
            border-radius: 20px;
            transition: all 0.2s ease;
            margin: 0 3px;
        }
        .navbar-nav .nav-link:hover {
            color: #f1f5f9;
            background: rgba(255, 255, 255, 0.06);
        }
        .navbar-nav .nav-link.active {
            background: #047857;
            color: #ffffff;
            box-shadow: 0 2px 10px rgba(4, 120, 87, 0.4);
        }
        .live-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            background: rgba(16, 185, 129, 0.12);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.25);
            padding: 5px 12px;
            border-radius: 20px;
        }
        .pulse-dot {
            width: 7px;
            height: 7px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            animation: pulse-glow 2s infinite;
        }
        @keyframes pulse-glow {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* Hero Section */
        .hero-section {
            background: radial-gradient(circle at 80% 20%, rgba(4, 120, 87, 0.25) 0%, transparent 50%),
                        radial-gradient(circle at 10% 80%, rgba(30, 58, 138, 0.25) 0%, transparent 50%),
                        linear-gradient(135deg, #0b1329 0%, #0f172a 100%);
            color: white;
            padding: 50px 0 40px;
            margin-bottom: 30px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            position: relative;
        }
        .hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 30px;
            padding: 6px 16px;
            font-size: 0.82rem;
            color: #cbd5e1;
            margin-bottom: 16px;
        }
        .hero-title {
            font-size: 2.3rem;
            font-weight: 800;
            line-height: 1.25;
            letter-spacing: -0.5px;
            margin-bottom: 14px;
        }
        .hero-title .highlight {
            background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-desc {
            font-size: 1.02rem;
            color: #94a3b8;
            max-width: 720px;
            line-height: 1.6;
            margin-bottom: 24px;
        }
        .trust-stat-box {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 12px 18px;
            text-align: center;
            backdrop-filter: blur(8px);
        }
        .trust-stat-num {
            font-size: 1.3rem;
            font-weight: 800;
            color: #ffffff;
        }
        .trust-stat-lbl {
            font-size: 0.72rem;
            color: #94a3b8;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        /* Modern Card Styling */
        .card { 
            border-radius: 16px; 
            box-shadow: 0 6px 20px rgba(0,0,0,0.04); 
            border: 1px solid #e2e8f0; 
            margin-bottom: 24px; 
            background: #ffffff;
            transition: all 0.2s ease;
        }
        .badge-status { 
            font-size: 0.92rem; 
            padding: 8px 18px; 
            border-radius: 30px; 
            font-weight: 800; 
            display: inline-block; 
            letter-spacing: 0.3px;
        }
        .status-affordable_now { background-color: #dcfce7; color: #15803d; border: 1.5px solid #86efac; }
        .status-affordable_with_plan { background-color: #dbeafe; color: #1d4ed8; border: 1.5px solid #93c5fd; }
        .status-affordable_later { background-color: #fef9c3; color: #a16207; border: 1.5px solid #fde047; }
        .status-not_affordable { background-color: #fee2e2; color: #b91c1c; border: 1.5px solid #fca5a5; }
        
        .metric-card {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            padding: 16px;
            text-align: center;
            height: 100%;
        }
        .metric-title { font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px; }
        .metric-value { font-size: 1.45rem; font-weight: 800; color: #0f172a; }
        
        .tip-box { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 16px; border-radius: 10px; }
        .warning-box { background-color: #fffbeb; border-left: 5px solid #f59e0b; padding: 16px; border-radius: 10px; }
        .danger-box { background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 16px; border-radius: 10px; }
        .step-badge { background-color: #047857; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 8px; }
        
        /* Form Inputs */
        .form-control, .form-select {
            border-radius: 10px;
            padding: 10px 14px;
            border: 1.5px solid #cbd5e1;
            font-size: 0.95rem;
            color: #0f172a;
            font-weight: 500;
        }
        .form-control:focus, .form-select:focus {
            border-color: #047857;
            box-shadow: 0 0 0 4px rgba(4, 120, 87, 0.12);
        }
        .btn-primary-action {
            background: linear-gradient(135deg, #047857 0%, #065f46 100%);
            color: white;
            font-weight: 700;
            border-radius: 12px;
            padding: 14px 24px;
            font-size: 1rem;
            border: none;
            box-shadow: 0 4px 14px rgba(4, 120, 87, 0.35);
            transition: all 0.2s ease;
        }
        .btn-primary-action:hover {
            background: linear-gradient(135deg, #065f46 0%, #047857 100%);
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(4, 120, 87, 0.45);
        }

        /* Footer */
        .site-footer {
            background: #0f172a;
            color: #94a3b8;
            padding: 40px 0 25px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            margin-top: 60px;
        }
        .site-footer a {
            color: #cbd5e1;
            text-decoration: none;
            transition: color 0.2s;
        }
        .site-footer a:hover {
            color: #34d399;
        }
    </style>
</head>
<body>
    <!-- 1. STICKY PROFESSIONAL NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top glass-navbar">
        <div class="container">
            <!-- Brand Logo & Title -->
            <a class="navbar-brand d-flex align-items-center gap-2" href="/">
                <div class="brand-logo-badge">
                    <i class="bi bi-wallet2"></i>
                </div>
                <div>
                    <span class="brand-title">Buy or Wait<span class="brand-dot">.AI</span></span>
                    <span class="badge rounded-pill badge-orchestrate ms-1">HackerRank '26</span>
                </div>
            </a>

            <!-- Mobile Toggle Button -->
            <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Navbar Links & Controls -->
            <div class="collapse navbar-collapse" id="navbarContent">
                <!-- Navigation Tabs in Navbar -->
                <ul class="navbar-nav mx-auto mb-2 mb-lg-0 nav-pills" id="pills-tab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link {% if active_tab == 'custom' %}active{% endif %}" id="custom-tab" data-bs-toggle="pill" data-bs-target="#tab-custom" type="button">
                            <i class="bi bi-calculator me-1"></i> {{ t['tab_custom'] }}
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link {% if active_tab == 'eval' %}active{% endif %}" id="eval-tab" data-bs-toggle="pill" data-bs-target="#tab-eval" type="button">
                            <i class="bi bi-database-check me-1"></i> {{ t['tab_eval'] }}
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="guide-tab" data-bs-toggle="pill" data-bs-target="#tab-guide" type="button">
                            <i class="bi bi-shield-check me-1"></i> {{ t['tab_guide'] }}
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="faq-tab" data-bs-toggle="pill" data-bs-target="#tab-faq" type="button">
                            <i class="bi bi-question-circle me-1"></i> {{ t['tab_user_guide'] }}
                        </button>
                    </li>
                </ul>

                <!-- Right Side Actions -->
                <div class="d-flex align-items-center gap-2 mt-3 mt-lg-0 flex-wrap">
                    <!-- Live Mobile App Link -->
                    <a href="http://localhost:8081" target="_blank" class="btn btn-sm btn-outline-light rounded-pill px-3 py-1">
                        <i class="bi bi-phone me-1"></i> Mobile App
                    </a>

                    <!-- Language Switcher (EN / HI) -->
                    <div class="btn-group p-1 rounded-pill" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);">
                        <a href="?lang=en&tab={{ active_tab }}&request_id={{ selected_id }}" class="btn btn-sm rounded-pill px-2 py-1 {% if lang == 'en' %}btn-success text-white fw-bold{% else %}text-light opacity-75{% endif %}">
                            EN 🇬🇧
                        </a>
                        <a href="?lang=hi&tab={{ active_tab }}&request_id={{ selected_id }}" class="btn btn-sm rounded-pill px-2 py-1 {% if lang == 'hi' %}btn-success text-white fw-bold{% else %}text-light opacity-75{% endif %}">
                            HI 🇮🇳
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- 2. MODERN FINTECH HERO SECTION -->
    <section class="hero-section">
        <div class="container">
            <div class="row align-items-center g-4">
                <div class="col-lg-8">
                    <div class="hero-pill">
                        <span class="pulse-dot"></span>
                        <span>Autonomous Financial Reality-Check & Cash-Flow Engine</span>
                    </div>
                    <h1 class="hero-title">
                        Smart Purchase Decisions Before Checkout.<br>
                        <span class="highlight">Zero Debt Traps. 100% Reserve Safety.</span>
                    </h1>
                    <p class="hero-desc">
                        {{ t['subtitle'] }}. Reconstructs real-time financial positions across recurring EMIs, essential family support, and confirmed salary cycles over a 90-day horizon.
                    </p>
                    <div class="d-flex align-items-center gap-3 flex-wrap">
                        <span class="live-status-pill">
                            <i class="bi bi-shield-fill-check"></i>
                            {{ t['emergency_protected'] }}
                        </span>
                        <span class="live-status-pill" style="color: #60a5fa; border-color: rgba(96, 165, 250, 0.25); background: rgba(96, 165, 250, 0.1);">
                            <i class="bi bi-cpu-fill"></i>
                            100% Deterministic (Zero Hallucinations)
                        </span>
                        <span class="live-status-pill" style="color: #facc15; border-color: rgba(250, 204, 21, 0.25); background: rgba(250, 204, 21, 0.1);">
                            <i class="bi bi-incognito"></i>
                            100% Local Device Privacy
                        </span>
                    </div>
                </div>
                <!-- Right Side Quick Stats -->
                <div class="col-lg-4">
                    <div class="row g-3">
                        <div class="col-6">
                            <div class="trust-stat-box">
                                <div class="trust-stat-num text-success">90 Days</div>
                                <div class="trust-stat-lbl">Cash Flow Forecast</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="trust-stat-box">
                                <div class="trust-stat-num text-primary">250 Cases</div>
                                <div class="trust-stat-lbl">Benchmark Requests</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="trust-stat-box">
                                <div class="trust-stat-num text-warning">₹0 Cost</div>
                                <div class="trust-stat-lbl">Zero Token Hallucination</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="trust-stat-box">
                                <div class="trust-stat-num text-info">₹ Lakhs / Cr</div>
                                <div class="trust-stat-lbl">Indian Currency System</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="container mb-5">
        <div class="tab-content" id="pills-tabContent">
            <!-- TAB 1: NEW USER SIMULATOR -->
            <div class="tab-pane fade {% if active_tab == 'custom' %}show active{% endif %}" id="tab-custom">
                <!-- How to use banner -->
                <div class="card p-3 mb-4 bg-light border-0">
                    <h6 class="fw-bold mb-2"><i class="bi bi-info-circle-fill text-success me-2"></i>{{ t['how_it_works_title'] }}</h6>
                    <div class="row g-3 small">
                        <div class="col-md-4">
                            <span class="step-badge">1</span> {{ t['step_1'] }}
                        </div>
                        <div class="col-md-4">
                            <span class="step-badge">2</span> {{ t['step_2'] }}
                        </div>
                        <div class="col-md-4">
                            <span class="step-badge">3</span> {{ t['step_3'] }}
                        </div>
                    </div>
                </div>

                <div class="row">
                    <!-- Form Column -->
                    <div class="col-lg-5">
                        <div class="card p-4">
                            <h5 class="fw-bold mb-3"><i class="bi bi-calculator me-2"></i>{{ t['form_title'] }}</h5>
                            <form method="POST" action="/simulate?lang={{ lang }}">
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">{{ t['lbl_item_name'] }}</label>
                                    <input type="text" name="item_name" class="form-control" value="{{ sim_data.item_name }}" placeholder="e.g. OnePlus Smartphone, Laptop, Bike" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">{{ t['lbl_item_price'] }}</label>
                                    <input type="number" name="item_price" class="form-control" value="{{ sim_data.item_price }}" placeholder="e.g. 45000" required>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">{{ t['lbl_bank_balance'] }}</label>
                                        <input type="number" name="bank_balance" class="form-control" value="{{ sim_data.bank_balance }}" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">{{ t['lbl_min_balance'] }}</label>
                                        <input type="number" name="min_balance" class="form-control" value="{{ sim_data.min_balance }}" required>
                                        <small class="text-muted">{{ t['lbl_min_balance_sub'] }}</small>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">{{ t['lbl_salary'] }}</label>
                                        <input type="number" name="salary" class="form-control" value="{{ sim_data.salary }}" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label fw-semibold">{{ t['lbl_payday'] }}</label>
                                        <select name="payday" class="form-select">
                                            <option value="1" {% if sim_data.payday == 1 %}selected{% endif %}>1st of Month</option>
                                            <option value="7" {% if sim_data.payday == 7 %}selected{% endif %}>7th of Month</option>
                                            <option value="15" {% if sim_data.payday == 15 %}selected{% endif %}>15th of Month</option>
                                            <option value="30" {% if sim_data.payday == 30 %}selected{% endif %}>Month End (30th)</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">{{ t['lbl_expenses'] }}</label>
                                    <input type="number" name="monthly_expenses" class="form-control" value="{{ sim_data.monthly_expenses }}" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-semibold">{{ t['lbl_emi'] }}</label>
                                    <select name="emi_available" class="form-select">
                                        <option value="yes" {% if sim_data.emi_available == 'yes' %}selected{% endif %}>{{ t['emi_yes'] }}</option>
                                        <option value="no" {% if sim_data.emi_available == 'no' %}selected{% endif %}>{{ t['emi_no'] }}</option>
                                    </select>
                                </div>
                                <button type="submit" class="btn btn-success w-100 py-2 fw-bold">
                                    <i class="bi bi-shield-check me-1"></i> {{ t['btn_calculate'] }}
                                </button>
                            </form>
                        </div>
                    </div>

                    <!-- Result Column -->
                    <div class="col-lg-7">
                        <div class="card p-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold mb-0"><i class="bi bi-award me-2"></i>{{ t['res_title'] }}</h5>
                                <span class="badge-status status-{{ sim_result.status_code }}">
                                    {{ sim_result.status_label }}
                                </span>
                            </div>

                            <!-- Key Metrics Row -->
                            <div class="row mb-4">
                                <div class="col-sm-4">
                                    <div class="metric-title">{{ t['metric_safe_today'] }}</div>
                                    <div class="metric-value text-success">{{ format_inr(sim_result.safe_today) }}</div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="metric-title">{{ t['metric_cushion'] }}</div>
                                    <div class="metric-value text-primary">{{ format_inr(sim_result.cushion) }}</div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="metric-title">{{ t['metric_savings'] }}</div>
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
                                <h6 class="fw-bold text-muted mb-2"><i class="bi bi-calendar-event me-2"></i>{{ t['lbl_plan_action'] }}</h6>
                                <p class="mb-1"><strong>{{ t['lbl_action'] }}:</strong> <span class="badge bg-secondary">{{ sim_result.recommended_method }}</span></p>
                                <p class="mb-1"><strong>{{ t['lbl_schedule'] }}:</strong> {{ sim_result.plan_text }}</p>
                                {% if sim_result.wait_date %}
                                <p class="mb-0"><strong>{{ t['lbl_earliest_safe'] }}:</strong> <code>{{ sim_result.wait_date }}</code></p>
                                {% endif %}
                            </div>

                            <!-- Wisdom Tip -->
                            <div class="tip-box">
                                <strong><i class="bi bi-lightbulb-fill text-warning me-1"></i> {{ t['lbl_tip_title'] }}:</strong><br>
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
                            <h5 class="fw-bold mb-3">{{ t['eval_select_title'] }}</h5>
                            <form method="GET" action="/">
                                <input type="hidden" name="tab" value="eval">
                                <input type="hidden" name="lang" value="{{ lang }}">
                                <div class="mb-3">
                                    <label class="form-label text-muted">{{ t['eval_choose_lbl'] }}</label>
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
                            <h6 class="fw-bold text-muted">{{ t['eval_profile_title'] }}</h6>
                            <ul class="list-unstyled small text-muted">
                                <li><strong>User ID:</strong> {{ user_id }}</li>
                                <li><strong>Currency:</strong> {{ currency }}</li>
                                <li><strong>Protected Categories:</strong> {{ profile['expense_categories_to_protect'] }}</li>
                                <li><strong>Allowed Reductions:</strong> {{ profile['expense_categories_user_is_willing_to_reduce'] }}</li>
                                <li><strong>Accepted Methods:</strong> {{ profile['payment_methods_user_will_consider'] }}</li>
                            </ul>
                        </div>
                    </div>

                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">{{ t['eval_cat'] }}</div>
                                    <div class="metric-value fs-6">{{ req_row['request_type']|capitalize }}</div>
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">{{ t['eval_req'] }}</div>
                                    <div class="metric-value fs-6">{{ format_inr(req_row['requested_amount']) }}</div>
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">{{ t['eval_bal'] }}</div>
                                    <div class="metric-value fs-6">{{ format_inr(profile['current_available_balance']) }}</div>
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="card p-3 text-center">
                                    <div class="metric-title">{{ t['eval_min'] }}</div>
                                    <div class="metric-value fs-6">{{ format_inr(profile['minimum_balance_to_keep']) }}</div>
                                </div>
                            </div>
                        </div>

                        <div class="card p-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold mb-0">{{ t['eval_rationale'] }}</h5>
                                <span class="badge-status status-{{ pred['affordability_status'] }}">
                                    {{ pred['affordability_status'].replace('_', ' ') }}
                                </span>
                            </div>

                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <p class="mb-1 text-muted">Recommended Payment Method:</p>
                                    <h5 class="text-primary fw-bold">{{ pred['recommended_payment_method'].replace('_', ' ').title() }}</h5>
                                </div>
                                <div class="col-md-6">
                                    <p class="mb-1 text-muted">Amount Safe to Pay Today:</p>
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
                            <h6 class="fw-bold mt-3">{{ t['eval_timeline'] }}</h6>
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

            <!-- TAB 3: GUIDELINES -->
            <div class="tab-pane fade" id="tab-guide">
                <div class="card p-4">
                    <h4 class="fw-bold mb-3"><i class="bi bi-compass me-2"></i>{{ t['guide_title'] }}</h4>
                    <p class="text-muted">{{ t['guide_sub'] }}</p>

                    <div class="row g-4 mt-2">
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-success border-4">
                                <h6 class="fw-bold text-success"><i class="bi bi-shield-lock me-2"></i>{{ t['g1_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['g1_desc'] }}</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-primary border-4">
                                <h6 class="fw-bold text-primary"><i class="bi bi-cart4 me-2"></i>{{ t['g2_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['g2_desc'] }}</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-warning border-4">
                                <h6 class="fw-bold text-warning"><i class="bi bi-clock-history me-2"></i>{{ t['g3_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['g3_desc'] }}</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card p-3 h-100 border-start border-danger border-4">
                                <h6 class="fw-bold text-danger"><i class="bi bi-credit-card-2-front me-2"></i>{{ t['g4_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['g4_desc'] }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 4: USER GUIDE & FAQS -->
            <div class="tab-pane fade" id="tab-faq">
                <div class="card p-4">
                    <h4 class="fw-bold mb-2"><i class="bi bi-question-circle-fill text-primary me-2"></i>{{ t['user_guide_heading'] }}</h4>
                    <p class="text-muted mb-4">{{ t['user_guide_subheading'] }}</p>

                    <!-- 3 Feature Cards -->
                    <div class="row g-3 mb-4">
                        <div class="col-md-4">
                            <div class="card h-100 p-3 bg-light border-0 shadow-none">
                                <h6 class="fw-bold text-dark"><i class="bi bi-1-circle-fill text-success me-2"></i>{{ t['ug_card1_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['ug_card1_desc'] }}</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100 p-3 bg-light border-0 shadow-none">
                                <h6 class="fw-bold text-dark"><i class="bi bi-2-circle-fill text-primary me-2"></i>{{ t['ug_card2_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['ug_card2_desc'] }}</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100 p-3 bg-light border-0 shadow-none">
                                <h6 class="fw-bold text-dark"><i class="bi bi-3-circle-fill text-warning me-2"></i>{{ t['ug_card3_title'] }}</h6>
                                <p class="small text-muted mb-0">{{ t['ug_card3_desc'] }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- FAQs Accordion -->
                    <h5 class="fw-bold mb-3"><i class="bi bi-chat-left-dots-fill text-info me-2"></i>Frequently Asked Questions (FAQs)</h5>
                    <div class="accordion" id="faqAccordion">
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqHead1">
                                <button class="accordion-button fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                                    {{ t['faq1_q'] }}
                                </button>
                            </h2>
                            <div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    {{ t['faq1_a'] }}
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqHead2">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">
                                    {{ t['faq2_q'] }}
                                </button>
                            </h2>
                            <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    {{ t['faq2_a'] }}
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqHead3">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faq3">
                                    {{ t['faq3_q'] }}
                                </button>
                            </h2>
                            <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    {{ t['faq3_a'] }}
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqHead4">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faq4">
                                    {{ t['faq4_q'] }}
                                </button>
                            </h2>
                            <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    {{ t['faq4_a'] }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 3. PROFESSIONAL CORPORATE FOOTER -->
    <footer class="site-footer">
        <div class="container">
            <div class="row g-4 mb-4">
                <div class="col-lg-4">
                    <div class="d-flex align-items-center gap-2 mb-3">
                        <div class="brand-logo-badge">
                            <i class="bi bi-wallet2"></i>
                        </div>
                        <span class="brand-title">Buy or Wait<span class="brand-dot">.AI</span></span>
                    </div>
                    <p class="small text-muted mb-3">
                        Autonomous AI Financial Affordability & Cash-Flow Intelligence Agent designed for HackerRank Orchestrate (September 2026). Safeguarding household wealth and eliminating debt traps.
                    </p>
                    <div class="d-flex gap-3">
                        <a href="https://github.com/kaushallakshya71-a11y/Buy-and-Wait" target="_blank" class="text-muted fs-5"><i class="bi bi-github"></i></a>
                        <a href="https://www.hackerrank.com/contests/hackerrank-orchestrate-september26/challenges/buy-or-wait/submission" target="_blank" class="text-muted fs-5"><i class="bi bi-trophy"></i></a>
                        <a href="http://localhost:8081" target="_blank" class="text-muted fs-5"><i class="bi bi-phone"></i></a>
                    </div>
                </div>

                <div class="col-sm-6 col-lg-2">
                    <h6 class="text-white fw-bold mb-3">Core Modules</h6>
                    <ul class="list-unstyled small text-muted mb-0">
                        <li class="mb-2"><a href="#tab-custom" data-bs-toggle="pill" data-bs-target="#tab-custom">Simulator</a></li>
                        <li class="mb-2"><a href="#tab-eval" data-bs-toggle="pill" data-bs-target="#tab-eval">250 Benchmark Cases</a></li>
                        <li class="mb-2"><a href="#tab-guide" data-bs-toggle="pill" data-bs-target="#tab-guide">Rulebook Guidelines</a></li>
                        <li class="mb-2"><a href="#tab-faq" data-bs-toggle="pill" data-bs-target="#tab-faq">User Guide & FAQs</a></li>
                    </ul>
                </div>

                <div class="col-sm-6 col-lg-3">
                    <h6 class="text-white fw-bold mb-3">Financial Guardrails</h6>
                    <ul class="list-unstyled small text-muted mb-0">
                        <li class="mb-2"><i class="bi bi-check2 text-success me-1"></i> Emergency Nidhi Protection</li>
                        <li class="mb-2"><i class="bi bi-check2 text-success me-1"></i> Roti & Kirana Budget Lock</li>
                        <li class="mb-2"><i class="bi bi-check2 text-success me-1"></i> Month-End Payday Sync</li>
                        <li class="mb-2"><i class="bi bi-check2 text-success me-1"></i> No-Cost EMI Debt Filter</li>
                    </ul>
                </div>

                <div class="col-lg-3">
                    <h6 class="text-white fw-bold mb-3">Hackathon Submission</h6>
                    <p class="small text-muted mb-2">
                        Official competition entry for <strong>HackerRank Orchestrate</strong>.
                    </p>
                    <a href="https://www.hackerrank.com/contests/hackerrank-orchestrate-september26/challenges/buy-or-wait/submission" target="_blank" class="btn btn-sm btn-outline-success rounded-pill px-3 py-2 w-100 text-truncate">
                        <i class="bi bi-box-arrow-up-right me-1"></i> Submit on HackerRank
                    </a>
                </div>
            </div>

            <hr class="border-secondary opacity-25">

            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 small text-muted">
                <div>
                    © 2026 Buy or Wait AI. Built for HackerRank Orchestrate. All calculations are deterministic and run locally.
                </div>
                <div>
                    <span class="badge bg-dark border border-secondary border-opacity-50 text-light py-1 px-2">
                        <i class="bi bi-lock-fill text-success me-1"></i> Zero External Data Leaks
                    </span>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


def calculate_simulation(item_name, item_price, bank_balance, min_balance, salary, payday, monthly_expenses, emi_available, lang="en"):
    """Run an Indian cultural affordability logic on custom user inputs with bilingual support."""
    cushion = max(0.0, bank_balance - min_balance)
    monthly_savings = max(0.0, salary - monthly_expenses)
    
    sim_current_day = 12
    if payday >= sim_current_day:
        days_to_payday = payday - sim_current_day
    else:
        days_to_payday = (30 - sim_current_day) + payday
    
    daily_spend = monthly_expenses / 30.0
    commitments_before_payday = daily_spend * days_to_payday
    safe_today = max(0.0, min(item_price, cushion - commitments_before_payday))
    
    today = datetime(2026, 9, 12).date()
    next_payday = today + timedelta(days=days_to_payday)
    payday_2 = next_payday + timedelta(days=30)

    # 1. Full Payment Affordable Now
    if safe_today >= item_price:
        if lang == "en":
            return {
                "status_code": "affordable_now",
                "status_label": "AFFORDABLE NOW (Safe to Buy Today)",
                "safe_today": safe_today,
                "cushion": cushion,
                "monthly_savings": monthly_savings,
                "headline": f"You can safely buy {item_name} today in full!",
                "detailed_explanation": f"Your emergency fund ({format_inr(min_balance)}) remains fully intact, and you have sufficient liquidity to cover all living expenses until your next salary credit.",
                "recommended_method": "Full Payment (One-Time)",
                "plan_text": f"Pay full {format_inr(item_price)} today.",
                "wait_date": None,
                "box_class": "tip-box",
                "icon_class": "bi bi-check-circle-fill text-success",
                "desi_tip": f"Prudent decision! After making this purchase, you still retain a safe cash cushion of {format_inr(min_balance)}."
            }
        else:
            return {
                "status_code": "affordable_now",
                "status_label": "AFFORDABLE NOW (खूब आराम से ले सकते हैं)",
                "safe_today": safe_today,
                "cushion": cushion,
                "monthly_savings": monthly_savings,
                "headline": f"Aap {item_name} abhi khareed sakte hain!",
                "detailed_explanation": f"Aapka emergency fund ({format_inr(min_balance)}) surakshit hai aur agle mahine ki salary aane tak ke saare kharche nikaalne ke baad bhi balance bacha hai.",
                "recommended_method": "Full Payment (One-Time)",
                "plan_text": f"Poora {format_inr(item_price)} aaj hi pay kar dein.",
                "wait_date": None,
                "box_class": "tip-box",
                "icon_class": "bi bi-check-circle-fill text-success",
                "desi_tip": f"Badiya decision! Khareedne ke baad bhi bank mein kam se kam {format_inr(min_balance)} ka suraksha kavach bana rahega."
            }

    # 2. Affordable with EMI
    if emi_available == "yes":
        for months in [3, 6]:
            monthly_emi = item_price / months
            if monthly_savings >= monthly_emi * 1.2 and cushion >= monthly_emi:
                if lang == "en":
                    return {
                        "status_code": "affordable_with_plan",
                        "status_label": f"AFFORDABLE WITH PLAN ({months}-Month No-Cost EMI)",
                        "safe_today": safe_today,
                        "cushion": cushion,
                        "monthly_savings": monthly_savings,
                        "headline": f"Avoid large upfront outflow: opt for a {months}-Month No-Cost EMI!",
                        "detailed_explanation": f"Paying {format_inr(item_price)} in full today would excessively deplete your emergency reserves. However, your monthly net savings ({format_inr(monthly_savings)}/month) comfortably support an installment of {format_inr(monthly_emi)}/month.",
                        "recommended_method": f"Installments ({months} Months)",
                        "plan_text": f"{months} monthly payments of {format_inr(monthly_emi)} each.",
                        "wait_date": None,
                        "box_class": "tip-box",
                        "icon_class": "bi bi-credit-card text-primary",
                        "desi_tip": "Opt for verified No-Cost EMI to ensure zero interest charges while keeping cash liquid in your savings account."
                    }
                else:
                    return {
                        "status_code": "affordable_with_plan",
                        "status_label": f"AFFORDABLE WITH PLAN ({months} Mahine Ki EMI)",
                        "safe_today": safe_today,
                        "cushion": cushion,
                        "monthly_savings": monthly_savings,
                        "headline": f"Full payment se bachein, {months} Mahine ki No-Cost EMI lein!",
                        "detailed_explanation": f"Ek saath {format_inr(item_price)} dene se emergency balance kam ho jayega. Lekin aapki bachat ({format_inr(monthly_savings)}/month) se {format_inr(monthly_emi)}/month ki EMI aasaani se nikal jayegi.",
                        "recommended_method": f"Installments ({months} Months)",
                        "plan_text": f"{months} kishtein of {format_inr(monthly_emi)} har mahine.",
                        "wait_date": None,
                        "box_class": "tip-box",
                        "icon_class": "bi bi-credit-card text-primary",
                        "desi_tip": "No-Cost EMI chuniyega taaki koi extra interest na lage, aur emergency fund safe rahe."
                    }

    # 3. Affordable Later (Wait for Payday)
    if cushion + monthly_savings >= item_price:
        wait_date_str = next_payday.strftime("%d %B %Y")
        if lang == "en":
            return {
                "status_code": "affordable_later",
                "status_label": "AFFORDABLE LATER (Wait for Upcoming Payday)",
                "safe_today": safe_today,
                "cushion": cushion,
                "monthly_savings": monthly_savings,
                "headline": f"Hold on! Wait until your upcoming payday on {wait_date_str}.",
                "detailed_explanation": f"Only {format_inr(safe_today)} is safe to spend today without risking month-end liquidity. Once your next salary credit settles on {wait_date_str}, you can complete this purchase in full safely.",
                "recommended_method": "Wait for Payday",
                "plan_text": f"Pay {format_inr(item_price)} on {wait_date_str}.",
                "wait_date": wait_date_str,
                "box_class": "warning-box",
                "icon_class": "bi bi-hourglass-split text-warning",
                "desi_tip": "30-Day Rule: Postponing big purchases until the next salary credit curbs impulse buying and protects household cash flow."
            }
        else:
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
        if lang == "en":
            return {
                "status_code": "affordable_later",
                "status_label": "AFFORDABLE LATER (Save Across 2 Paydays)",
                "safe_today": safe_today,
                "cushion": cushion,
                "monthly_savings": monthly_savings,
                "headline": f"Defer this purchase until {wait_date_str} to accumulate sufficient surplus.",
                "detailed_explanation": f"With monthly net savings of {format_inr(monthly_savings)}, you will accumulate sufficient cash reserves over the next 2 paydays to afford this purchase without compromising your emergency fund.",
                "recommended_method": "Wait (2 Paydays)",
                "plan_text": f"Pay {format_inr(item_price)} on {wait_date_str}.",
                "wait_date": wait_date_str,
                "box_class": "warning-box",
                "icon_class": "bi bi-hourglass-split text-warning",
                "desi_tip": "Check if upcoming festival sales (e.g. Diwali/Great Indian Festival) offer discounts when your savings target is reached."
            }
        else:
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
                "desi_tip": "Festival sale aane tak wait karein, cashback ya bank discounts mil sakte hain!"
            }

    # 4. Not Affordable
    if lang == "en":
        return {
            "status_code": "not_affordable",
            "status_label": "NOT AFFORDABLE (Postpone Discretionary Spending)",
            "safe_today": safe_today,
            "cushion": cushion,
            "monthly_savings": monthly_savings,
            "headline": f"Purchasing {item_name} now significantly compromises your financial safety!",
            "detailed_explanation": f"The requested price ({format_inr(item_price)}) exceeds your available financial cushion ({format_inr(cushion)}). Proceeding with this purchase would deplete your emergency fund and risk default on essential bills.",
            "recommended_method": "Not Recommended (Postpone)",
            "plan_text": "No immediate payment plan is recommended at this time.",
            "wait_date": None,
            "box_class": "danger-box",
            "icon_class": "bi bi-exclamation-octagon-fill text-danger",
            "desi_tip": "Avoid high-cost personal loans or liquidating emergency reserves for discretionary purchases. Build an RD or SIP first."
        }
    else:
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
            "desi_tip": "Karz (debt) lekar ya Emergency fund tod kar aisi purchases na karein. Pehle SIP ya RD mein bachat karein."
        }


@app.route("/", methods=["GET"])
def home():
    lang = request.args.get("lang", "en")
    if lang not in ["en", "hi"]:
        lang = "en"
    t = TEXTS[lang]

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
    sim_result = calculate_simulation(**default_sim_data, lang=lang)

    return render_template_string(
        HTML_TEMPLATE,
        lang=lang,
        t=t,
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
    lang = request.args.get("lang", "en")
    if lang not in ["en", "hi"]:
        lang = "en"
    t = TEXTS[lang]

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
    sim_result = calculate_simulation(**sim_data, lang=lang)

    requests_df = loader.requests_df
    request_ids = requests_df["request_id"].tolist()
    req_row = requests_df.iloc[0]
    user_id = str(req_row["user_id"])
    prof = loader.get_user_profile(user_id)
    pred = engine.evaluate_request(req_row)
    requests_map = {r["request_id"]: {"user_id": r["user_id"]} for _, r in requests_df.iterrows()}

    return render_template_string(
        HTML_TEMPLATE,
        lang=lang,
        t=t,
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
