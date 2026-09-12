"""Financial forecast engine for Buy or Wait agent.
Simulates daily cash flow over a 90-day horizon, enforces the minimum balance,
and calculates safe amounts and feasible dates.
"""
from typing import Dict, Any, List, Tuple, Optional, Set
from datetime import datetime, timedelta
import pandas as pd


class FinanceEngine:
    def __init__(self, data_loader):
        self.loader = data_loader

    def get_user_commitments(self, user_id: str, request_date: datetime.date) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Identify monthly recurring debits and salary details from history and messages."""
        prof = self.loader.get_user_profile(user_id)
        events = self.loader.get_user_events(user_id)
        msg_updates = self.loader.user_message_updates.get(user_id, {})
        
        events["s_date"] = pd.to_datetime(events["settlement_date"]).dt.date
        past = events[events["s_date"] < request_date]

        monthly_cats = [
            "rent", "utilities", "education", "debt_repayment", "insurance",
            "cloud_storage", "streaming", "music_subscription", "delivery_membership",
            "gym", "family_support", "housing", "shopping"
        ]
        variable_cats = {"groceries", "transport", "dining", "shopping", "healthcare"}

        recurring_debits = []
        for (cat, desc), grp in past.groupby(["category", "description"]):
            if cat in monthly_cats and cat not in {"groceries", "transport", "dining"}:
                if grp["direction"].iloc[-1] != "debit":
                    continue
                days = [d.day for d in grp["s_date"]]
                mode_day = max(set(days), key=days.count)
                latest_row = grp.sort_values("s_date").iloc[-1]
                amt = float(latest_row["amount"])
                flex = latest_row["flexibility"]
                last_id = latest_row["event_id"]
                min_amt = latest_row["minimum_allowed_amount"]
                if pd.isna(min_amt):
                    min_amt = None
                else:
                    min_amt = float(min_amt)

                if cat == "rent":
                    amt *= msg_updates.get("rent_multiplier", 1.0)

                recurring_debits.append({
                    "category": cat,
                    "description": desc,
                    "day": mode_day,
                    "amount": amt,
                    "event_id": last_id,
                    "flexibility": flex,
                    "minimum_allowed_amount": min_amt,
                })

        # Salary details
        salary_info = {
            "amount": 0.0,
            "day": 15,
            "ended": msg_updates.get("salary_ended", False)
        }
        past_sal = past[(past["category"] == "salary") & (past["direction"] == "credit")]
        if not past_sal.empty and not salary_info["ended"]:
            latest_sal = past_sal.sort_values("s_date").iloc[-1]
            desc_lower = str(latest_sal["description"]).lower()
            if "final" in desc_lower or "ended" in desc_lower:
                salary_info["ended"] = True

            all_descs = " ".join(past_sal["description"].astype(str).str.lower())
            if any(k in all_descs for k in ["platform payout", "app earnings", "task marketplace"]):
                salary_info["ended"] = True

            if not salary_info["ended"]:
                valid_sal = past_sal[past_sal["amount"].notna()]
                if not valid_sal.empty:
                    salary_info["amount"] = float(valid_sal.sort_values("s_date").iloc[-1]["amount"])
                days = [d.day for d in past_sal["s_date"]]
                if days:
                    salary_info["day"] = max(set(days), key=days.count)

        # Message overrides for salary
        if msg_updates.get("salary_amount") is not None:
            salary_info["amount"] = float(msg_updates["salary_amount"])
        if msg_updates.get("salary_date"):
            salary_info["day"] = datetime.strptime(msg_updates["salary_date"], "%Y-%m-%d").day

        # Check explicit scheduled salary in future
        future_sal = events[(events["s_date"] >= request_date) & (events["category"] == "salary") & (events["status"] == "scheduled")]
        if not future_sal.empty and msg_updates.get("salary_amount") is None:
            salary_info["amount"] = float(future_sal["amount"].iloc[0])
            salary_info["day"] = future_sal["s_date"].iloc[0].day

        return recurring_debits, salary_info

    def get_commitments_before_payday(self, user_id: str, request_date: datetime.date) -> float:
        """Calculate total cash outflow reserved between request_date and next payday."""
        recurring_debits, salary_info = self.get_user_commitments(user_id, request_date)
        events = self.loader.get_user_events(user_id)
        prof = self.loader.get_user_profile(user_id)
        events["s_date"] = pd.to_datetime(events["settlement_date"]).dt.date

        # If salary ended or no future salary, reserve all upcoming scheduled/pending debits for 90 days
        if salary_info["ended"] or salary_info["amount"] <= 0:
            end_date = request_date + timedelta(days=90)
            reserved = 0.0
            for _, row in events[events["direction"] == "debit"].iterrows():
                dt = row["s_date"]
                if request_date <= dt <= end_date and row["status"] in ["pending", "scheduled"]:
                    amt = float(row["amount"])
                    if row["currency"] != prof["home_currency"]:
                        amt *= self.loader.get_exchange_rate(str(dt), row["currency"], prof["home_currency"])
                    reserved += amt
            for deb in recurring_debits:
                reserved += deb["amount"] * 3
            return reserved
        
        # Determine next payday
        sal_day = salary_info["day"]
        # Find next payday date >= request_date
        y = request_date.year
        m = request_date.month
        try:
            candidate_payday = datetime(y, m, sal_day).date()
        except ValueError:
            candidate_payday = datetime(y, m, 28).date()

        if candidate_payday < request_date:
            m += 1
            if m > 12:
                m = 1
                y += 1
            try:
                candidate_payday = datetime(y, m, sal_day).date()
            except ValueError:
                candidate_payday = datetime(y, m, 28).date()

        reserved = 0.0

        # 1. Pending debits before next payday
        pending = events[(events["status"] == "pending") & (events["direction"] == "debit")]
        for _, row in pending.iterrows():
            ev_date = row["s_date"]
            if request_date <= ev_date <= candidate_payday:
                amt = float(row["amount"])
                if row["currency"] != prof["home_currency"]:
                    amt *= self.loader.get_exchange_rate(str(ev_date), row["currency"], prof["home_currency"])
                reserved += amt

        # 2. Scheduled events before next payday
        scheduled = events[(events["status"] == "scheduled") & (events["direction"] == "debit")]
        for _, row in scheduled.iterrows():
            ev_date = row["s_date"]
            if request_date <= ev_date <= candidate_payday:
                amt = float(row["amount"])
                if row["currency"] != prof["home_currency"]:
                    amt *= self.loader.get_exchange_rate(str(ev_date), row["currency"], prof["home_currency"])
                reserved += amt

        # 3. Monthly recurring debits that fall between request_date and candidate_payday
        scheduled_cats = set(scheduled[scheduled["s_date"] <= candidate_payday]["category"])
        for deb in recurring_debits:
            if deb["category"] in scheduled_cats:
                continue
            day = deb["day"]
            try:
                dt_this_month = datetime(request_date.year, request_date.month, day).date()
                if request_date <= dt_this_month <= candidate_payday:
                    reserved += deb["amount"]
            except ValueError:
                pass

        # 4. Conservative essential variable spending (groceries, transport) before next payday
        days_to_payday = max(0, (candidate_payday - request_date).days)
        daily_var = self.get_daily_variable_spend(user_id, request_date)
        reserved += daily_var * days_to_payday

        return reserved

    def get_daily_variable_spend(self, user_id: str, request_date: datetime.date) -> float:
        """Estimate average daily spend on essential variable categories (groceries, transport)."""
        prof = self.loader.get_user_profile(user_id)
        events = self.loader.get_user_events(user_id)
        events["s_date"] = pd.to_datetime(events["settlement_date"]).dt.date
        past = events[(events["s_date"] < request_date) & (events["direction"] == "debit")]
        protect_cats = set(prof.get("expense_categories_to_protect", []))
        var_cats = {"groceries", "transport"}.union(protect_cats.intersection({"dining", "shopping", "healthcare"}))
        var_past = past[past["category"].isin(var_cats)]
        if var_past.empty:
            return 0.0
        d_min = var_past["s_date"].min()
        d_max = var_past["s_date"].max()
        days = max(1, (d_max - d_min).days + 1)
        total_amt = 0.0
        for _, row in var_past.iterrows():
            amt = float(row["amount"]) if pd.notna(row["amount"]) else 0.0
            if row["currency"] != prof["home_currency"]:
                amt *= self.loader.get_exchange_rate(str(row["s_date"]), row["currency"], prof["home_currency"])
            total_amt += amt
        return total_amt / days

    def compute_amount_safe_to_pay(self, user_id: str, request_date: datetime.date, requested_amount: float) -> float:
        """Compute maximum safe payment on request_date before spending changes."""
        prof = self.loader.get_user_profile(user_id)
        current_bal = float(prof["current_available_balance"])
        min_bal = float(prof["minimum_balance_to_keep"])
        cushion = current_bal - min_bal
        if cushion <= 0:
            return 0.0

        reserved = self.get_commitments_before_payday(user_id, request_date)
        safe = cushion - reserved
        safe = max(0.0, min(requested_amount, safe))
        return round(safe, 2)

    def simulate_payment_plan(
        self,
        user_id: str,
        request_date: datetime.date,
        payment_schedule: List[Tuple[datetime.date, float]],
        spending_changes: Optional[List[str]] = None
    ) -> Tuple[bool, float]:
        """Simulate a proposed payment schedule over 90 days.
        Returns (is_safe, min_balance_observed).
        """
        prof = self.loader.get_user_profile(user_id)
        events = self.loader.get_user_events(user_id)
        min_bal = float(prof["minimum_balance_to_keep"])
        recurring_debits, salary_info = self.get_user_commitments(user_id, request_date)

        # Apply spending changes to recurring debits
        active_debits = []
        for d in recurring_debits:
            ev_id = d["event_id"]
            amt = d["amount"]
            if spending_changes:
                if f"stop:{ev_id}" in spending_changes:
                    amt = 0.0
                else:
                    for sc in spending_changes:
                        if sc.startswith(f"reduce_to:{ev_id}:"):
                            amt = float(sc.split(":")[-1])
            if amt > 0:
                copy_d = dict(d)
                copy_d["amount"] = amt
                active_debits.append(copy_d)

        # Build daily cash flow map for 90 days
        end_date = request_date + timedelta(days=90)
        daily_var = self.get_daily_variable_spend(user_id, request_date)
        daily_net: Dict[datetime.date, float] = {request_date + timedelta(days=i): -daily_var for i in range(91)}

        # Subtract proposed payments
        for pay_date, pay_amt in payment_schedule:
            if pay_date in daily_net:
                daily_net[pay_date] -= pay_amt

        # Add explicit future events from dataset
        events["s_date"] = pd.to_datetime(events["settlement_date"]).dt.date
        future_events = events[(events["s_date"] >= request_date) & (events["s_date"] <= end_date)]
        for _, row in future_events.iterrows():
            st = row["status"]
            dr = row["direction"]
            dt = row["s_date"]
            amt = float(row["amount"])
            if row["currency"] != prof["home_currency"]:
                amt *= self.loader.get_exchange_rate(str(dt), row["currency"], prof["home_currency"])

            if dr == "debit" and st in ["pending", "scheduled"]:
                if dt in daily_net:
                    daily_net[dt] -= amt
            elif dr == "credit" and st == "scheduled" and row["category"] == "salary":
                if dt in daily_net:
                    daily_net[dt] += amt

        # Add recurring monthly debits and salary
        cur_y = request_date.year
        cur_m = request_date.month
        scheduled_future_dates = set(future_events[future_events["category"] == "salary"]["s_date"])

        for m_idx in range(4):
            m = (cur_m - 1 + m_idx) % 12 + 1
            y = cur_y + ((cur_m - 1 + m_idx) // 12)

            # Salary
            if not salary_info["ended"] and salary_info["amount"] > 0:
                try:
                    s_dt = datetime(y, m, salary_info["day"]).date()
                    if request_date <= s_dt <= end_date and s_dt not in scheduled_future_dates:
                        daily_net[s_dt] += salary_info["amount"]
                except ValueError:
                    pass

            # Debits
            for deb in active_debits:
                try:
                    d_dt = datetime(y, m, deb["day"]).date()
                    if request_date < d_dt <= end_date:
                        daily_net[d_dt] -= deb["amount"]
                except ValueError:
                    pass

        # Simulate day-by-day balance
        bal = float(prof["current_available_balance"])
        min_observed = bal
        is_safe = True

        for i in range(91):
            dt = request_date + timedelta(days=i)
            bal += daily_net[dt]
            if bal < min_observed:
                min_observed = bal
            if bal < min_bal:
                is_safe = False

        return is_safe, round(min_observed, 2)

    def find_earliest_date_for_full_payment(
        self,
        user_id: str,
        request_date: datetime.date,
        requested_amount: float
    ) -> Optional[datetime.date]:
        """Find the earliest safe date within 90 days to pay the full requested amount in one payment."""
        # 1. Check if safe today
        safe_today = self.compute_amount_safe_to_pay(user_id, request_date, requested_amount)
        if safe_today >= requested_amount:
            return request_date

        recurring_debits, salary_info = self.get_user_commitments(user_id, request_date)
        if salary_info["ended"] or salary_info["amount"] <= 0:
            return None

        # Test candidate paydays within 90 days
        end_date = request_date + timedelta(days=90)
        sal_day = salary_info["day"]
        
        cur_y = request_date.year
        cur_m = request_date.month
        
        candidate_paydays = []
        for i in range(4):
            m = (cur_m - 1 + i) % 12 + 1
            y = cur_y + ((cur_m - 1 + i) // 12)
            try:
                p_date = datetime(y, m, sal_day).date()
            except ValueError:
                p_date = datetime(y, m, 28).date()
            if request_date < p_date <= end_date:
                candidate_paydays.append(p_date)
        
        for cand in candidate_paydays:
            schedule = [(cand, requested_amount)]
            is_safe, _ = self.simulate_payment_plan(user_id, request_date, schedule)
            if is_safe:
                return cand

        return None
