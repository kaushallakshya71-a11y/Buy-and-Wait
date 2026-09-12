# 📖 User Guide — Buy or Wait? AI Financial Advisor

Welcome to the **Buy or Wait?** Financial Affordability Agent. This user guide explains how to use the interactive dashboard, interpret AI decisions, and make smart, debt-free financial choices.

---

## 🚀 1. Quick Start (Running the Dashboard)

1. Open your terminal and navigate to the project directory:
   ```bash
   cd "/Users/lakshya/Desktop/ help/AI agents"
   ```
2. Start the local web dashboard:
   ```bash
   python3 server.py
   ```
3. Open your browser and go to:
   👉 **English (Default):** [http://localhost:8080](http://localhost:8080)  
   👉 **Hindi / Hinglish:** [http://localhost:8080/?lang=hi](http://localhost:8080/?lang=hi)

---

## 🎯 2. How to Test a Purchase (Simulator Walkthrough)

Under the **"Test a Purchase (Simulator)"** tab, you can test any planned expense (e.g., iPhone, Bike, Laptop, Holiday, Festival Shopping).

### Step 1: Enter Your Financial Profile
- **Current Bank Balance:** Total liquid cash in your savings/checking account today.
- **Emergency Fund (Minimum to Keep):** Your *Suraksha Nidhi* (3–6 months of essential living expenses). The AI guarantees this balance is **never touched**.
- **Monthly In-Hand Salary & Payday:** Your net take-home salary and the day of the month it hits your account (e.g., 1st, 7th, 15th, or 30th).
- **Monthly Fixed Commitments:** Total non-negotiable monthly expenses (Rent, Groceries/Ration, Existing EMIs, Utility Bills, Parents' Allowance).

### Step 2: Enter Purchase Details
- **Item Name:** What you want to buy (e.g., *OnePlus 12*, *Sony Bravia TV*).
- **Price (₹):** Total cost of the item.
- **EMI Option:** Choose whether a 3 or 6-month verified No-Cost EMI is available.

### Step 3: Click "Run AI Financial Reality Check"
The AI will immediately forecast your daily cash flow over the next 90 days and output an actionable recommendation.

---

## 🚦 3. Understanding the 4 AI Verdicts

| Verdict Badge | Meaning | When Is It Recommended? |
|---|---|---|
| 🟢 **AFFORDABLE NOW** | **Buy in Full Today** | You have surplus cash above your Emergency Fund, and all commitments before your next salary are fully covered. |
| 🔵 **AFFORDABLE WITH PLAN** | **Opt for 3/6-Month No-Cost EMI** | Paying 100% upfront would breach your emergency cushion, but your monthly surplus savings easily covers the installment. |
| 🟡 **AFFORDABLE LATER** | **Wait for Upcoming Payday** | You are currently near month-end liquidity limits. Waiting 5–15 days for salary credit lets you buy safely without debt. |
| 🔴 **NOT AFFORDABLE** | **Postpone Discretionary Purchase** | The price exceeds your financial capacity. Buying now risks default on rent, EMIs, or depleting emergency savings. |

---

## 💡 4. Real-World Indian Household Scenarios

### Scenario A: The Month-End Dilemma
- **User:** Rohan (IT Employee, Bengaluru)
- **Salary:** ₹65,000 (Credited on 1st). Bank Balance on 26th: ₹22,000.
- **Emergency Fund:** ₹15,000.
- **Wants to buy:** ₹18,000 Smartwatch during a flash sale.
- **AI Verdict:** 🟡 **AFFORDABLE LATER (Wait for 1st)**
- **Reason:** On the 26th, Rohan has only ₹7,000 free cushion (`₹22,000 - ₹15,000`). Spending ₹18,000 now leaves him with just ₹4,000, endangering rent/bills. Waiting 5 days until his ₹65,000 salary credits makes the purchase 100% safe.

### Scenario B: The Smartphone Upgrade (No-Cost EMI)
- **User:** Priya (Marketing Specialist, Pune)
- **Salary:** ₹50,000 (Credited on 7th). Balance: ₹60,000.
- **Emergency Fund:** ₹40,000.
- **Wants to buy:** ₹45,000 Smartphone.
- **AI Verdict:** 🔵 **AFFORDABLE WITH PLAN (3-Month EMI)**
- **Reason:** Paying ₹45,000 in full drops Priya's balance to ₹15,000 (severely breaching her ₹40,000 safety fund). But her monthly net savings is ₹15,000. A 3-month EMI of ₹15,000/month keeps her emergency fund completely intact.

---

## ❓ 5. Frequently Asked Questions (FAQ)

### Q1: Why did the AI reject my purchase even though my bank balance is higher than the price?
> **Answer:** Because of your **Emergency Fund** and **Upcoming Fixed Debits**. If your balance is ₹50,000 and the phone is ₹40,000, but your emergency reserve is ₹25,000, you only have ₹25,000 in spendable cushion. The AI refuses to gamble with your safety net.

### Q2: What is the 30-Day Rule?
> **Answer:** If an item is marked **"AFFORDABLE LATER"**, waiting until your next salary cycle gives you time to decide whether you genuinely need the item or if it was an impulsive emotional urge.

### Q3: How do I switch the language to Hindi?
> **Answer:** Click the **`[ हिंदी 🇮🇳 ]`** button at the top-right header of the web page, or add `?lang=hi` to the URL.

### Q4: Does this store or leak my financial data?
> **Answer:** **No.** The calculations run 100% locally on your machine. Zero data is transmitted to external servers or cloud APIs.
