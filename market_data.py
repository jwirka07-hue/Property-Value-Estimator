"""
Market assumptions the owner doesn't have to know.
Every number carries its source. Update these each quarter.
Last updated: Nov 10, 2026.
"""

MARKETS = {
    "Atlanta": {
        "cap_rate_class_b": 0.0557,
        "cap_source": "Matthews, Atlanta Multifamily Market Report Q3 2026 — metro average cap rate 5.57%",
        "millage": 0.03936,
        "millage_source": "Property Tax Almanac (Fulton County) — City of Atlanta total ≈ 39.36 mills. "
                          "Lower outside city limits; varies by city and county.",
        "vacancy_floor": 0.059,
        "vacancy_source": "Matthews, Atlanta Q2 2026 — metro vacancy 5.9%",
    },
    "Athens": {
        "cap_rate_class_b": 0.0582,
        "cap_source": "ASSUMPTION — Atlanta average (5.57%) + 25 bps for a smaller, less liquid market. "
                      "Replace with Athens sales comps.",
        "millage": 0.03105,
        "millage_source": "Athens-Clarke County 12.25 mills (FY27 budget, 2026 tax year, unchanged) + "
                          "Clarke County School District 18.80 mills (held flat) = 31.05 mills",
        "vacancy_floor": 0.059,
        "vacancy_source": "ASSUMPTION — Atlanta metro vacancy (5.9%) used as a proxy; replace with Athens data",
    },
}

# Cap rate spread by property class, relative to Class B.
# From Apartment Loan Store's Atlanta survey (Oct 12, 2026): Suburban A 4.75%, B 5.18%, C 5.65%.
CLASS_SPREAD = {"A": -0.0043, "B": 0.0, "C": 0.0047}
CLASS_SOURCE = "Class spreads from Apartment Loan Store Atlanta survey, Oct 2026 (A −43 bps, C +47 bps vs. B)"


def property_class(year_built: int) -> str:
    """Simple vintage-based class. Owners rarely know their 'class'; they know the year built."""
    if year_built >= 2010:
        return "A"
    if year_built >= 1990:
        return "B"
    return "C"


# Standard underwriting a buyer would apply (from the v1 spec)
GEORGIA_ASSESSMENT_RATIO = 0.40     # Georgia law: assessed at 40% of fair market value
MGMT_FEE = 0.03                     # % of EGI, market rate even if self-managed
RESERVES_PER_UNIT = 300             # $/unit/year
CREDIT_LOSS = 0.02                  # concessions + bad debt, % of GPR
CAP_RANGE = 0.0025                  # ±25 bps around the market cap rate for the value range
