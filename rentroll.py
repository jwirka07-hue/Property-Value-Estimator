"""
Read an owner's rent roll (CSV or Excel) without making them reformat it.
Finds the unit / rent / status columns by common names.
"""
import pandas as pd

ALIASES = {
    "unit": ["unit", "unit #", "unit number", "unit no", "apt", "apartment", "unit id"],
    "rent": ["rent", "current rent", "in-place rent", "in place rent", "actual rent",
             "lease rent", "contract rent", "monthly rent"],
    "market_rent": ["market rent", "market", "asking rent"],
    "status": ["status", "unit status", "occupancy", "occupancy status"],
}
VACANT_WORDS = ("vacant", "down", "model", "offline", "non-rev", "admin")


def _norm(s) -> str:
    return str(s).strip().lower().replace("_", " ")


def _find(columns, field):
    norm = {_norm(c): c for c in columns}
    for alias in ALIASES[field]:
        if alias in norm:
            return norm[alias]
    if field == "rent":  # fallback: any column with 'rent' that isn't market rent
        for n, c in norm.items():
            if "rent" in n and "market" not in n and "asking" not in n:
                return c
    return None


def _money(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(r"[$,\s]", "", regex=True), errors="coerce"
    ).fillna(0)


def read_file(uploaded) -> pd.DataFrame:
    name = getattr(uploaded, "name", str(uploaded)).lower()
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded)
    return pd.read_csv(uploaded)


def summarize(df: pd.DataFrame) -> dict:
    df = df.dropna(how="all")
    rent_col = _find(df.columns, "rent")
    if rent_col is None:
        raise ValueError("Couldn't find a rent column. Name it 'Rent' and try again.")

    status_col = _find(df.columns, "status")
    mkt_col = _find(df.columns, "market_rent")
    warnings = []

    rent = _money(df[rent_col])
    if status_col:
        status = df[status_col].astype(str).str.lower()
        vacant = status.apply(lambda s: any(w in s for w in VACANT_WORDS)) | (rent <= 0)
    else:
        vacant = rent <= 0
        warnings.append("No status column found — units with $0 rent were treated as vacant.")

    units = len(df)
    occupied = int((~vacant).sum())
    if occupied == 0:
        raise ValueError("Every unit looks vacant. Check that the rent column has amounts.")

    avg_occ_rent = rent[~vacant].mean()

    # Vacant units are counted at market rent if given, otherwise at the average occupied rent
    if mkt_col:
        mkt = _money(df[mkt_col])
        vacant_rent = mkt[vacant].where(mkt[vacant] > 0, avg_occ_rent)
    else:
        vacant_rent = pd.Series(avg_occ_rent, index=df.index[vacant])
        if vacant.any():
            warnings.append("No market rent column — vacant units were valued at the average occupied rent.")

    gpr_monthly = rent[~vacant].sum() + vacant_rent.sum()

    return {
        "units": units,
        "occupied": occupied,
        "vacant": units - occupied,
        "physical_vacancy": (units - occupied) / units,
        "avg_in_place_rent": avg_occ_rent,
        "gpr_annual": gpr_monthly * 12,
        "warnings": warnings,
    }


def template() -> pd.DataFrame:
    return pd.DataFrame({
        "Unit": ["101", "102", "103"],
        "Rent": [1450, 1500, 0],
        "Market Rent": [1500, 1550, 1500],
        "Status": ["Occupied", "Occupied", "Vacant"],
    })
