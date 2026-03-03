# import re
# from dateutil import parser as date_parser
# from rapidfuzz import process

# SECTOR_VARIANTS = {
#     "Mining": ["mining", "minerals", "extraction"],
#     "Powerline": ["powerline", "utilities", "energy"],
#     "Renewables": ["renewables", "solar", "wind", "clean energy"],
#     "Railways": ["railways", "trains", "transportation"],
#     "Construction": ["construction", "building", "infrastructure"],
#     "Others": ["others", "misc", "various"],
# }

# def normalize_sector(raw: str) -> str:
#     if not raw:
#         return "Unknown"
#     raw_lower = raw.strip().lower()
#     for canonical, variants in SECTOR_VARIANTS.items():
#         if raw_lower in variants:
#             return canonical.title()
#     # fuzzy match fallback
#     all_variants = [v for variants in SECTOR_VARIANTS.values() for v in variants]
#     match, score, _ = process.extractOne(raw_lower, all_variants)
#     if score > 80:
#         for canonical, variants in SECTOR_VARIANTS.items():
#             if match in variants:
#                 return canonical.title()
#     return raw.strip().title()

# def normalize_currency(raw: str) -> float | None:
#     if not raw:
#         return None
#     cleaned = re.sub(r"[^\d.]", "", raw.replace("k", "000").replace("K", "000"))
#     try:
#         return float(cleaned)
#     except:
#         return None

# def normalize_date(raw: str) -> str | None:
#     if not raw:
#         return None
#     try:
#         return date_parser.parse(raw).strftime("%Y-%m-%d")
#     except:
#         return None

# def normalize_items(items: list[dict]) -> tuple[list[dict], list[str]]:
#     cleaned = []
#     caveats = []
#     for item in items:
#         normalized = {"name": item["name"], "id": item["id"], "columns": {}}
#         missing_fields = []
#         for col in item["column_values"]:
#             val = col["text"]
#             col_id = col["id"].lower()
#             if not val:
#                 missing_fields.append(col_id)
#                 normalized["columns"][col_id] = None
#             elif "sector" in col_id or "industry" in col_id:
#                 normalized["columns"][col_id] = normalize_sector(val)
#             elif any(x in col_id for x in ["revenue", "amount", "value", "price"]):
#                 normalized["columns"][col_id] = normalize_currency(val)
#             elif "date" in col_id:
#                 normalized["columns"][col_id] = normalize_date(val)
#             else:
#                 normalized["columns"][col_id] = val.strip()
#         if missing_fields:
#             caveats.append(f"Item '{item['name']}' missing: {', '.join(missing_fields)}")
#         cleaned.append(normalized)
#     return cleaned, caveats

import re
from dateutil import parser as date_parser
from rapidfuzz import process

# Deals column ID mapping
DEALS_COLUMN_MAP = {
    "color_mm108wkh": "owner",
    "dropdown_mm109jeh": "company",
    "color_mm10j30k": "status",
    "date_mm10kj50": "close_date",
    "color_mm10agwz": "priority",
    "numeric_mm104r8v": "deal_value",
    "date_mm10gwnb": "created_date",
    "color_mm10x4ch": "deal_stage",
    "color_mm10f8vm": "product_service",
    "color_mm10z7s4": "sector",
    "date_mm104s96": "expected_close_date"
}

# Work Orders column ID mapping
WORK_ORDERS_COLUMN_MAP = {
    "dropdown_mm102e28": "company",
    "dropdown_mm10hwmv": "linked_deal",
    "color_mm10y19m": "project_type",
    "color_mm102rjb": "sub_status",
    "color_mm103qjg": "status",
    "date_mm10mmf6": "start_date",
    "date_mm10aaa4": "end_date",
    "color_mm10aajn": "order_type",
    "date_mm10gx4d": "delivery_date",
    "date_mm1036mt": "actual_delivery_date",
    "color_mm10dmws": "owner",
    "color_mm10zhq": "sector",
    "color_mm10b8fp": "deliverable_type",
    "color_mm10x6x": "sub_deliverable",
    "date_mm105fb": "invoice_date",
    "dropdown_mm10ptdj": "invoice_number",
    "numeric_mm107djg": "contract_value",
    "numeric_mm10hd7g": "total_value",
    "numeric_mm10yxjy": "tax_amount",
    "numeric_mm106jw2": "discount",
    "numeric_mm10g4n": "other_charges",
    "numeric_mm10b5e8": "paid_amount",
    "numeric_mm10zzm": "balance",
    "numeric_mm10jkac": "retention",
    "color_mm10mt54": "payment_status",
    "numeric_mm10zryj": "area",
    "dropdown_mm1067ht": "area_unit",
    "numeric_mm103txe": "area_value",
    "text_mm10s3g": "notes",
    "color_mm10cvda": "update_status"
}

SECTOR_VARIANTS = {
    "Mining": ["mining", "minerals", "extraction", "mine"],
    "Powerline": ["powerline", "power line", "utilities", "power"],
    "Renewables": ["renewables", "renewable", "solar", "wind", "clean energy"],
    "Railways": ["railways", "railway", "trains", "train", "transportation", "rail"],
    "Construction": ["construction", "building", "infrastructure", "construct"],
    "Others": ["others", "other", "misc", "various", "none"],
}

def normalize_sector(raw: str) -> str:
    if not raw:
        return "Unknown"
    raw_lower = raw.strip().lower()
    for canonical, variants in SECTOR_VARIANTS.items():
        if raw_lower in variants:
            return canonical
    all_variants = [v for variants in SECTOR_VARIANTS.values() for v in variants]
    match_result = process.extractOne(raw_lower, all_variants)
    if match_result and match_result[1] > 80:
        match = match_result[0]
        for canonical, variants in SECTOR_VARIANTS.items():
            if match in variants:
                return canonical
    return raw.strip().title()

def normalize_currency(raw: str) -> float | None:
    if not raw:
        return None
    try:
        cleaned = re.sub(r"[^\d.]", "", str(raw).replace("k", "000").replace("K", "000"))
        return float(cleaned) if cleaned else None
    except:
        return None

def normalize_date(raw: str) -> str | None:
    if not raw:
        return None
    try:
        return date_parser.parse(raw).strftime("%Y-%m-%d")
    except:
        return None

def normalize_items(items: list[dict], board_type: str = "deals") -> tuple[list[dict], list[str]]:
    cleaned = []
    caveats = []

    # Pick the right column map based on board type
    column_map = DEALS_COLUMN_MAP if board_type == "deals" else WORK_ORDERS_COLUMN_MAP

    # Columns we expect to have values — flag if missing
    important_columns = {
        "deals": ["company", "deal_value", "sector", "deal_stage", "status"],
        "work_orders": ["company", "status", "sector", "contract_value"]
    }
    important = important_columns.get(board_type, [])

    for item in items:
        normalized = {
            "name": item["name"],
            "id": item["id"],
        }
        missing_fields = []

        for col in item["column_values"]:
            raw_id = col["id"]
            val = col["text"]

            # Map to readable name, fallback to raw ID
            readable_name = column_map.get(raw_id, raw_id)

            if not val or val.strip() == "":
                normalized[readable_name] = None
                # Only flag as missing if it's an important column
                if readable_name in important:
                    missing_fields.append(readable_name)
            elif readable_name == "sector":
                normalized[readable_name] = normalize_sector(val)
            elif any(x in readable_name for x in ["value", "amount", "paid", "balance", "contract", "tax", "discount"]):
                normalized[readable_name] = normalize_currency(val)
            elif "date" in readable_name:
                normalized[readable_name] = normalize_date(val)
            else:
                normalized[readable_name] = val.strip()

        if missing_fields:
            caveats.append(f"'{item['name']}' missing: {', '.join(missing_fields)}")

        cleaned.append(normalized)

    return cleaned, caveats