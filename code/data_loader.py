"""Data loader module for Buy or Wait financial agent.
Loads and joins CSV data from dataset/ with currency conversions and media extraction.
"""
from typing import Dict, Any, List, Optional
import os
import pandas as pd
from extractor import extract_amount_from_image, parse_message_updates


class DataLoader:
    def __init__(self, data_dir: str = "dataset"):
        self.data_dir = data_dir
        self.requests_df: pd.DataFrame = pd.DataFrame()
        self.sample_requests_df: pd.DataFrame = pd.DataFrame()
        self.financial_profiles_df: pd.DataFrame = pd.DataFrame()
        self.financial_events_df: pd.DataFrame = pd.DataFrame()
        self.exchange_rates_df: pd.DataFrame = pd.DataFrame()
        self.payment_options_df: pd.DataFrame = pd.DataFrame()
        self.messages_df: pd.DataFrame = pd.DataFrame()
        self.images_df: pd.DataFrame = pd.DataFrame()
        self.user_message_updates: Dict[str, Dict[str, Any]] = {}
        self.rate_map: Dict[tuple, float] = {}

    def load_all(self):
        """Load all CSV files and perform initial preprocessing."""
        self.requests_df = pd.read_csv(os.path.join(self.data_dir, "requests.csv"))
        if os.path.exists(os.path.join(self.data_dir, "sample_requests.csv")):
            self.sample_requests_df = pd.read_csv(os.path.join(self.data_dir, "sample_requests.csv"))

        self.financial_profiles_df = pd.read_csv(os.path.join(self.data_dir, "financial_profiles.csv"))
        self.financial_events_df = pd.read_csv(os.path.join(self.data_dir, "financial_events.csv"))
        self.exchange_rates_df = pd.read_csv(os.path.join(self.data_dir, "exchange_rates.csv"))
        self.payment_options_df = pd.read_csv(os.path.join(self.data_dir, "request_payment_options.csv"))
        self.messages_df = pd.read_csv(os.path.join(self.data_dir, "messages.csv"))
        self.images_df = pd.read_csv(os.path.join(self.data_dir, "images.csv"))

        # Build exchange rate lookup: (rate_date, from_currency, to_currency) -> rate
        for _, row in self.exchange_rates_df.iterrows():
            key = (str(row["rate_date"]), str(row["from_currency"]), str(row["to_currency"]))
            self.rate_map[key] = float(row["rate"])

        # Parse message updates
        self.user_message_updates = parse_message_updates(self.messages_df)

        # Fill blank amounts in financial_events from images
        self._fill_image_amounts()

        # Pre-process profile columns
        self._clean_profiles()

    def _fill_image_amounts(self):
        """Fill missing amounts using images.csv and media extraction."""
        image_event_map = dict(zip(self.images_df["related_event_id"], self.images_df["image_id"]))
        for idx, row in self.financial_events_df.iterrows():
            if pd.isna(row["amount"]):
                ev_id = str(row["event_id"])
                if ev_id in image_event_map:
                    img_id = image_event_map[ev_id]
                    extracted_val = extract_amount_from_image(img_id)
                    if extracted_val is not None:
                        self.financial_events_df.at[idx, "amount"] = extracted_val

    def _clean_profiles(self):
        """Parse string list fields in financial profiles."""
        list_cols = [
            "financial_priorities",
            "expense_categories_to_protect",
            "expense_categories_user_is_willing_to_reduce",
            "expense_categories_user_is_willing_to_stop",
            "payment_methods_user_will_consider"
        ]
        for col in list_cols:
            if col in self.financial_profiles_df.columns:
                self.financial_profiles_df[col] = self.financial_profiles_df[col].fillna("").apply(
                    lambda s: [x.strip() for x in str(s).split("|") if x.strip()]
                )

    def get_exchange_rate(self, rate_date: str, from_curr: str, to_curr: str) -> float:
        """Get dated conversion rate."""
        if from_curr == to_curr:
            return 1.0
        # Exact match
        key = (rate_date, from_curr, to_curr)
        if key in self.rate_map:
            return self.rate_map[key]
        # Inverted match
        inv_key = (rate_date, to_curr, from_curr)
        if inv_key in self.rate_map:
            return 1.0 / self.rate_map[inv_key]
        # Fallback to closest available date
        candidates = [v for (d, f, t), v in self.rate_map.items() if f == from_curr and t == to_curr]
        if candidates:
            return candidates[-1]
        return 1.0

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Return financial profile dict for user."""
        row = self.financial_profiles_df[self.financial_profiles_df["user_id"] == user_id]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()

    def get_user_events(self, user_id: str) -> pd.DataFrame:
        """Return financial events for user."""
        return self.financial_events_df[self.financial_events_df["user_id"] == user_id].copy()

    def get_request_payment_options(self, request_id: str) -> pd.DataFrame:
        """Return seller/provider payment options for request."""
        return self.payment_options_df[self.payment_options_df["request_id"] == request_id].copy()
