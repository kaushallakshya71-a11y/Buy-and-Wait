"""Decision engine module for Buy or Wait financial agent.
Synthesizes the forecast and payment planner results into the final output row
and generates grounded, consistent decision explanations.
"""
from typing import Dict, Any, Tuple
from datetime import datetime
import pandas as pd
from finance_engine import FinanceEngine
from payment_planner import PaymentPlanner, PlanCandidate


class DecisionEngine:
    def __init__(self, data_loader, finance_engine: FinanceEngine, payment_planner: PaymentPlanner):
        self.loader = data_loader
        self.engine = finance_engine
        self.planner = payment_planner

    def format_amount(self, amt: float, currency: str) -> str:
        """Format amount with currency and commas."""
        if amt == int(amt):
            return f"{currency} {int(amt):,}"
        else:
            return f"{currency} {amt:,.2f}"

    def format_date_str(self, dt: datetime.date) -> str:
        """Format date as 'DD Month YYYY' (e.g. 15 June 2024)."""
        day = dt.day
        month_name = dt.strftime("%B")
        year = dt.year
        return f"{day} {month_name} {year}"

    def generate_explanation(
        self,
        request_row: pd.Series,
        plan: PlanCandidate,
        safe_today: float,
        earliest_full: str
    ) -> str:
        """Generate concise grounded decision explanation."""
        user_id = str(request_row["user_id"])
        prof = self.loader.get_user_profile(user_id)
        curr = prof.get("home_currency", "USD")
        min_bal = float(prof.get("minimum_balance_to_keep", 0.0))
        min_bal_str = self.format_amount(min_bal, curr)

        req_amt = float(request_row["requested_amount"])
        req_amt_str = self.format_amount(req_amt, curr)
        safe_str = self.format_amount(safe_today, curr)
        deadline = datetime.strptime(str(request_row["desired_completion_date"]), "%Y-%m-%d").date()
        deadline_str = self.format_date_str(deadline)

        method = plan.method

        if method == "full_payment":
            if plan.spending_changes:
                change_descs = []
                for sc in plan.spending_changes:
                    parts = sc.split(":")
                    action = parts[0]
                    ev_id = parts[1]
                    ev_row = self.loader.financial_events_df[self.loader.financial_events_df["event_id"] == ev_id]
                    desc = ev_row["description"].iloc[0].lower() if not ev_row.empty else "subscription"
                    if action == "stop":
                        change_descs.append(f"Stop the {desc}")
                    elif action == "reduce_to":
                        new_amt = float(parts[2])
                        new_amt_str = self.format_amount(new_amt, curr)
                        change_descs.append(f"reduce the {desc} to {new_amt_str}")
                changes_phrase = " and ".join(change_descs)
                return f"{changes_phrase}, then pay {req_amt_str} today. This leaves at least {min_bal_str} available."
            else:
                return f"Pay {req_amt_str} today. This leaves at least {min_bal_str} available over the next 90 days."

        elif method == "installments":
            n_payments = plan.num_payments
            inst_amt = plan.schedule[0][1]
            inst_amt_str = self.format_amount(inst_amt, curr)
            start_date_str = self.format_date_str(plan.start_date)
            return f"Use {n_payments} installments of {inst_amt_str}, starting {start_date_str}. This leaves at least {min_bal_str} available."

        elif method == "partial_payment":
            p1_amt = plan.schedule[0][1]
            p2_amt = plan.schedule[1][1]
            p1_str = self.format_amount(p1_amt, curr)
            p2_str = self.format_amount(p2_amt, curr)
            p2_date_str = self.format_date_str(plan.schedule[1][0])
            return f"Pay {p1_str} today and the remaining {p2_str} on {p2_date_str}. This completes the full request and keeps the {min_bal_str} minimum protected."

        elif method == "wait":
            wait_date_str = self.format_date_str(plan.start_date)
            return f"Pay {req_amt_str} in full on {wait_date_str}. Paying earlier would take the balance below the {min_bal_str} minimum."

        else:  # not_recommended
            if safe_today > 0:
                return f"Do not proceed with the {req_amt_str} request. Although {safe_str} is available today, the full amount cannot be completed safely within 90 days."
            else:
                return f"Do not make this payment by {deadline_str}. None of the available options keeps the {min_bal_str} minimum protected."

    def evaluate_request(self, request_row: pd.Series) -> Dict[str, Any]:
        """Process one request row and produce the dictionary of output fields."""
        req_id = str(request_row["request_id"])
        user_id = str(request_row["user_id"])
        req_date = datetime.strptime(str(request_row["request_date"]), "%Y-%m-%d").date()
        req_amt = float(request_row["requested_amount"])

        # Compute safe today and earliest full date
        safe_today = self.engine.compute_amount_safe_to_pay(user_id, req_date, req_amt)
        earliest_full_date = self.engine.find_earliest_date_for_full_payment(user_id, req_date, req_amt)

        # Plan the best safe payment option
        best_plan = self.planner.plan_request(request_row)

        earliest_str = earliest_full_date.strftime("%Y-%m-%d") if earliest_full_date else ""
        if best_plan.status == "affordable_now":
            earliest_str = req_date.strftime("%Y-%m-%d")

        explanation = self.generate_explanation(request_row, best_plan, safe_today, earliest_str)

        return {
            "request_id": req_id,
            "amount_safe_to_pay": safe_today,
            "affordability_status": best_plan.status,
            "recommended_payment_method": best_plan.method,
            "payment_plan": best_plan.plan_string(),
            "earliest_date_for_full_payment": earliest_str,
            "spending_changes_needed": best_plan.spending_changes_string(),
            "decision_explanation": explanation
        }
