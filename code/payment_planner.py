"""Payment option simulator and planner for Buy or Wait agent.
Generates candidate payment plans, evaluates spending adjustments,
and ranks options according to the challenge rules.
"""
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
import pandas as pd


class PlanCandidate:
    def __init__(
        self,
        method: str,
        status: str,
        schedule: List[Tuple[datetime.date, float]],
        total_paid: float,
        spending_changes: Optional[List[str]] = None,
        option_id: Optional[str] = None
    ):
        self.method = method  # full_payment, partial_payment, installments, wait, not_recommended
        self.status = status  # affordable_now, affordable_with_plan, affordable_later, not_affordable
        self.schedule = schedule
        self.total_paid = total_paid
        self.spending_changes = spending_changes or []
        self.option_id = option_id or "zz_none"

    @property
    def start_date(self) -> datetime.date:
        if not self.schedule:
            return datetime.max.date()
        return self.schedule[0][0]

    @property
    def end_date(self) -> datetime.date:
        if not self.schedule:
            return datetime.max.date()
        return self.schedule[-1][0]

    @property
    def num_payments(self) -> int:
        return len(self.schedule)

    def plan_string(self) -> str:
        if not self.schedule or self.method == "not_recommended":
            return "none"
        parts = []
        for dt, amt in self.schedule:
            if amt == int(amt):
                amt_str = f"{int(amt)}"
            else:
                amt_str = f"{amt:.2f}".rstrip("0").rstrip(".")
                if "." in amt_str and len(amt_str.split(".")[1]) == 1:
                    amt_str = f"{amt:.2f}"
            parts.append(f"{dt.strftime('%Y-%m-%d')}:{amt_str}")
        return "|".join(parts)

    def spending_changes_string(self) -> str:
        if not self.spending_changes:
            return "none"
        return "|".join(self.spending_changes)


class PaymentPlanner:
    def __init__(self, data_loader, finance_engine):
        self.loader = data_loader
        self.engine = finance_engine

    def plan_request(self, request_row: pd.Series) -> PlanCandidate:
        """Evaluate all candidate plans for a request and return the best ranked safe plan."""
        req_id = str(request_row["request_id"])
        user_id = str(request_row["user_id"])
        req_date = datetime.strptime(str(request_row["request_date"]), "%Y-%m-%d").date()
        desired_deadline = datetime.strptime(str(request_row["desired_completion_date"]), "%Y-%m-%d").date()
        req_amt = float(request_row["requested_amount"])
        allows_partial = bool(request_row.get("allows_partial_payment", False))

        prof = self.loader.get_user_profile(user_id)
        considered_methods = set(prof.get("payment_methods_user_will_consider", []))
        max_install_months = prof.get("max_installment_months")
        if pd.isna(max_install_months):
            max_install_months = None
        else:
            max_install_months = float(max_install_months)

        # Base financial capacities
        safe_today = self.engine.compute_amount_safe_to_pay(user_id, req_date, req_amt)
        earliest_full_date = self.engine.find_earliest_date_for_full_payment(user_id, req_date, req_amt)

        safe_candidates: List[PlanCandidate] = []

        # 1. Candidate: full_payment today (no spending changes)
        if "full_payment" in considered_methods:
            if safe_today >= req_amt:
                safe_candidates.append(PlanCandidate(
                    method="full_payment",
                    status="affordable_now",
                    schedule=[(req_date, req_amt)],
                    total_paid=req_amt,
                    option_id="00_full_now"
                ))

        # 2. Candidate: Installment options from request_payment_options.csv
        options_df = self.loader.get_request_payment_options(req_id)
        if "installments" in considered_methods and not options_df.empty:
            for _, opt in options_df.iterrows():
                opt_id = str(opt["payment_option_id"])
                opt_method = str(opt["payment_method"])
                if opt_method != "installments":
                    continue
                num_payments = int(opt["number_of_payments"])
                if max_install_months is not None and num_payments > max_install_months:
                    continue

                pay_amt = float(opt["payment_amount"])
                first_date = datetime.strptime(str(opt["first_payment_date"]), "%Y-%m-%d").date()
                freq_days = int(opt["payment_frequency_days"]) if pd.notna(opt["payment_frequency_days"]) else 30
                total_payable = float(opt["total_payable_amount"])

                # Build schedule
                schedule = []
                for p_i in range(num_payments):
                    p_date = first_date + timedelta(days=p_i * freq_days)
                    schedule.append((p_date, pay_amt))

                # Check safety
                is_safe, _ = self.engine.simulate_payment_plan(user_id, req_date, schedule)
                if is_safe:
                    safe_candidates.append(PlanCandidate(
                        method="installments",
                        status="affordable_with_plan",
                        schedule=schedule,
                        total_paid=total_payable,
                        option_id=opt_id
                    ))

        # 3. Candidate: partial_payment
        if allows_partial and "partial_payment" in considered_methods:
            if 0 < safe_today < req_amt and earliest_full_date is not None:
                if earliest_full_date <= desired_deadline:
                    rem_amt = round(req_amt - safe_today, 2)
                    p_schedule = [(req_date, safe_today), (earliest_full_date, rem_amt)]
                    is_safe, _ = self.engine.simulate_payment_plan(user_id, req_date, p_schedule)
                    if is_safe:
                        safe_candidates.append(PlanCandidate(
                            method="partial_payment",
                            status="affordable_with_plan",
                            schedule=p_schedule,
                            total_paid=req_amt,
                            option_id="10_partial"
                        ))

        # 4. Candidate: wait
        if "full_payment" in considered_methods and earliest_full_date is not None:
            if earliest_full_date <= desired_deadline and earliest_full_date > req_date:
                wait_schedule = [(earliest_full_date, req_amt)]
                is_safe, _ = self.engine.simulate_payment_plan(user_id, req_date, wait_schedule)
                if is_safe:
                    safe_candidates.append(PlanCandidate(
                        method="wait",
                        status="affordable_later",
                        schedule=wait_schedule,
                        total_paid=req_amt,
                        option_id="20_wait"
                    ))

        # 5. Candidate: Spending changes if needed
        # If no safe plan finishes by deadline without changes, test spending changes
        best_candidate = self._pick_best_candidate(safe_candidates, desired_deadline)
        if best_candidate is None:
            spending_plan = self._try_spending_changes(user_id, req_date, req_amt, desired_deadline, considered_methods)
            if spending_plan is not None:
                safe_candidates.append(spending_plan)

        # Final selection
        best_candidate = self._pick_best_candidate(safe_candidates, desired_deadline)
        if best_candidate is not None:
            return best_candidate

        # Fallback: not_recommended
        return PlanCandidate(
            method="not_recommended",
            status="not_affordable",
            schedule=[],
            total_paid=0.0,
            option_id="99_not_recommended"
        )

    def _try_spending_changes(
        self,
        user_id: str,
        req_date: datetime.date,
        req_amt: float,
        deadline: datetime.date,
        considered_methods: set
    ) -> Optional[PlanCandidate]:
        """Test combinations of eligible flexible spending reductions/stops."""
        prof = self.loader.get_user_profile(user_id)
        protect_cats = set(prof.get("expense_categories_to_protect", []))
        stop_cats = set(prof.get("expense_categories_user_is_willing_to_stop", []))
        reduce_cats = set(prof.get("expense_categories_user_is_willing_to_reduce", []))

        recurring_debits, _ = self.engine.get_user_commitments(user_id, req_date)
        
        # Build candidate changes
        candidate_changes = []
        for deb in recurring_debits:
            cat = deb["category"]
            if cat in protect_cats:
                continue
            ev_id = deb["event_id"]
            flex = deb["flexibility"]
            min_allowed = deb.get("minimum_allowed_amount")

            # Check stop
            if cat in stop_cats and flex in ["stoppable", "reducible_or_stoppable"]:
                candidate_changes.append(f"stop:{ev_id}")

            # Check reduce
            if cat in reduce_cats and flex in ["reducible", "reducible_or_stoppable"] and min_allowed is not None:
                amt_str = f"{int(min_allowed)}" if min_allowed == int(min_allowed) else f"{min_allowed:.2f}"
                candidate_changes.append(f"reduce_to:{ev_id}:{amt_str}")

        # Test single and pairs of changes
        import itertools
        for r in range(1, min(3, len(candidate_changes)) + 1):
            for combo in itertools.combinations(candidate_changes, r):
                # Ensure no conflicting changes on the same event
                event_ids = [c.split(":")[1] for c in combo]
                if len(event_ids) != len(set(event_ids)):
                    continue

                # Check if full payment today is safe with these changes
                sched = [(req_date, req_amt)]
                is_safe, _ = self.engine.simulate_payment_plan(user_id, req_date, sched, spending_changes=list(combo))
                if is_safe and "full_payment" in considered_methods:
                    return PlanCandidate(
                        method="full_payment",
                        status="affordable_with_plan",
                        schedule=sched,
                        total_paid=req_amt,
                        spending_changes=list(combo),
                        option_id="05_full_with_changes"
                    )

        return None

    def _pick_best_candidate(self, candidates: List[PlanCandidate], deadline: datetime.date) -> Optional[PlanCandidate]:
        """Rank safe candidates according to Section 189 rules:
        1. Complete by desired_completion_date
        2. Require no spending changes
        3. Minimize total amount paid
        4. Start payment earlier
        5. Use fewer payments
        6. Lowest payment_option_id
        """
        if not candidates:
            return None

        def rank_key(p: PlanCandidate):
            # Rule 1: Completes by deadline
            completes_by_deadline = (p.end_date <= deadline)
            r1 = 0 if completes_by_deadline else 1

            # Rule 2: Require no spending changes
            no_changes = (len(p.spending_changes) == 0)
            r2 = 0 if no_changes else 1

            # Rule 3: Minimize total amount paid
            r3 = round(p.total_paid, 2)

            # Rule 4: Start payment earlier
            r4 = p.start_date

            # Rule 5: Use fewer payments
            r5 = p.num_payments

            # Rule 6: Lowest payment_option_id
            r6 = p.option_id

            return (r1, r2, r3, r4, r5, r6)

        sorted_candidates = sorted(candidates, key=rank_key)
        # Prefer candidates that complete by deadline
        if sorted_candidates[0].end_date <= deadline:
            return sorted_candidates[0]

        return None
