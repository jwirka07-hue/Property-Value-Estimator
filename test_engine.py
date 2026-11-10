"""
Benchmark test: the spec's 120-unit Athens worked example.
If this fails, the engine is wrong. Run with: python -m pytest -q
"""
import pytest
from engine import OperatingInputs, TaxInputs, direct_cap, cap_rate_sensitivity

OP = OperatingInputs(
    units=120, avg_rent=1450, vacancy=0.06, concessions_bad_debt=0.02,
    other_income=75, opex_per_unit=5200, mgmt_fee=0.03, reserves_per_unit=300,
)
TAX = TaxInputs(current_tax_bill=180_000, assessment_ratio=0.40, millage=0.030)


def test_operating_statement():
    r = direct_cap(OP, TAX, 0.055)
    assert r["gpr"] == 2_088_000
    assert r["egi"] == pytest.approx(2_028_960)
    assert r["expenses_before_tax"] == pytest.approx(720_868.8)
    assert r["noi_before_tax"] == pytest.approx(1_308_091.2)


def test_broker_case():
    r = direct_cap(OP, TAX, 0.055, reassess=False)
    assert r["noi"] == pytest.approx(1_128_091, abs=1)
    assert r["value"] == pytest.approx(20_510_745, abs=5)  # spec rounds mgmt to $60,869 mid-calc; engine is unrounded


def test_adjusted_case():
    r = direct_cap(OP, TAX, 0.055, reassess=True)
    assert r["value"] == pytest.approx(19_523_746, abs=5)  # spec rounds mgmt to $60,869 mid-calc; engine is unrounded
    assert r["taxes"] == pytest.approx(234_285, abs=1)
    assert r["value_per_unit"] == pytest.approx(162_698, abs=1)
    # Internal consistency: NOI / cap must equal value
    assert r["noi"] / 0.055 == pytest.approx(r["value"])


def test_tax_flag_impact():
    broker = direct_cap(OP, TAX, 0.055, reassess=False)["value"]
    adjusted = direct_cap(OP, TAX, 0.055, reassess=True)["value"]
    assert broker - adjusted == pytest.approx(987_000, abs=1_000)
    assert (broker - adjusted) / broker == pytest.approx(0.048, abs=0.001)


def test_sensitivity_table():
    rows = cap_rate_sensitivity(OP, TAX, [0.0525, 0.055, 0.0575])
    for r, expected in zip(rows, [20_280_481, 19_523_746, 18_821_453]):
        assert r["value"] == pytest.approx(expected, abs=5)
