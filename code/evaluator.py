"""Evaluator module for Buy or Wait financial agent.
Evaluates predictions against sample_requests.csv ground-truth values.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from data_loader import DataLoader
from finance_engine import FinanceEngine
from payment_planner import PaymentPlanner
from decision_engine import DecisionEngine


def run_evaluation(data_dir: str = "dataset") -> Dict[str, Any]:
    loader = DataLoader(data_dir)
    loader.load_all()

    finance_engine = FinanceEngine(loader)
    planner = PaymentPlanner(loader, finance_engine)
    engine = DecisionEngine(loader, finance_engine, planner)

    samples_df = loader.sample_requests_df
    if samples_df.empty:
        print("No sample_requests.csv found for evaluation.")
        return {}

    results = []
    for _, row in samples_df.iterrows():
        pred = engine.evaluate_request(row)
        results.append(pred)

    pred_df = pd.DataFrame(results)

    # Compare fields
    metrics = {}
    total = len(samples_df)

    # 1. affordability_status accuracy
    status_match = (samples_df["affordability_status"] == pred_df["affordability_status"]).sum()
    metrics["affordability_status_acc"] = status_match / total

    # 2. recommended_payment_method accuracy
    method_match = (samples_df["recommended_payment_method"] == pred_df["recommended_payment_method"]).sum()
    metrics["recommended_payment_method_acc"] = method_match / total

    # 3. payment_plan exact match
    plan_match = (samples_df["payment_plan"] == pred_df["payment_plan"]).sum()
    metrics["payment_plan_acc"] = plan_match / total

    # 4. earliest_date_for_full_payment match
    earliest_gt = samples_df["earliest_date_for_full_payment"].fillna("")
    earliest_pred = pred_df["earliest_date_for_full_payment"].fillna("")
    earliest_match = (earliest_gt == earliest_pred).sum()
    metrics["earliest_date_acc"] = earliest_match / total

    # 5. spending_changes_needed match
    spending_match = (samples_df["spending_changes_needed"] == pred_df["spending_changes_needed"]).sum()
    metrics["spending_changes_acc"] = spending_match / total

    # 6. amount_safe_to_pay MAE
    safe_diff = np.abs(samples_df["amount_safe_to_pay"] - pred_df["amount_safe_to_pay"])
    metrics["amount_safe_mae"] = float(safe_diff.mean())

    print("=" * 60)
    print(f"EVALUATION REPORT ON {total} SAMPLES")
    print("=" * 60)
    for k, v in metrics.items():
        if "acc" in k:
            print(f"{k:35s}: {v*100:6.2f}% ({(int(round(v*total)))}/{total})")
        else:
            print(f"{k:35s}: {v:10.2f}")
    print("=" * 60)

    # Print any mismatches
    print("\nDETAILED MISMATCHES:")
    for i in range(total):
        gt = samples_df.iloc[i]
        pr = pred_df.iloc[i]
        mismatches = []
        if gt["affordability_status"] != pr["affordability_status"]:
            mismatches.append(f"status: GT='{gt['affordability_status']}' vs Pred='{pr['affordability_status']}'")
        if gt["recommended_payment_method"] != pr["recommended_payment_method"]:
            mismatches.append(f"method: GT='{gt['recommended_payment_method']}' vs Pred='{pr['recommended_payment_method']}'")
        if gt["payment_plan"] != pr["payment_plan"]:
            mismatches.append(f"plan: GT='{gt['payment_plan']}' vs Pred='{pr['payment_plan']}'")
        if str(gt["earliest_date_for_full_payment"]) != str(pr["earliest_date_for_full_payment"]) and not (pd.isna(gt["earliest_date_for_full_payment"]) and pr["earliest_date_for_full_payment"] == ""):
            mismatches.append(f"earliest: GT='{gt['earliest_date_for_full_payment']}' vs Pred='{pr['earliest_date_for_full_payment']}'")
        if gt["spending_changes_needed"] != pr["spending_changes_needed"]:
            mismatches.append(f"changes: GT='{gt['spending_changes_needed']}' vs Pred='{pr['spending_changes_needed']}'")
        if abs(gt["amount_safe_to_pay"] - pr["amount_safe_to_pay"]) > 1.0:
            mismatches.append(f"safe_amt: GT={gt['amount_safe_to_pay']} vs Pred={pr['amount_safe_to_pay']}")

        if mismatches:
            print(f"[{gt['request_id']} ({gt['user_id']})]")
            for m in mismatches:
                print(f"   -> {m}")

    return metrics


if __name__ == "__main__":
    run_evaluation()
