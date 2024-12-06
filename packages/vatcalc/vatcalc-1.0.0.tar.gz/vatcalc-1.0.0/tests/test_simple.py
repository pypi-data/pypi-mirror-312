import pytest
from decimal import Decimal as D
from vatcalc import (
    net_to_gross,
    gross_to_net,
    vat_amount_from_net,
    vat_amount_from_gross,
    discount_percent,
    discount_amount,
)


@pytest.fixture
def de_vat():
    return D(19)


def test_net_to_gross(de_vat):
    assert net_to_gross(D(200), de_vat) == D(238)
    assert net_to_gross(200, de_vat) == D(238)
    assert net_to_gross("200", de_vat) == D(238)


def test_gross_to_net(de_vat):
    assert gross_to_net(D(238), de_vat) == D(200)
    assert gross_to_net(238, de_vat) == D(200)
    assert gross_to_net("238", de_vat) == D(200)


def test_vat_amount_from_gross(de_vat):
    assert vat_amount_from_gross(D(238), de_vat) == D(38)
    assert vat_amount_from_gross(238, de_vat) == D(38)
    assert vat_amount_from_gross("238", de_vat) == D(38)


def test_vat_amount_from_net(de_vat):
    assert vat_amount_from_net(D(200), de_vat) == D(38)
    assert vat_amount_from_net(200, de_vat) == D(38)
    assert vat_amount_from_net("200", de_vat) == D(38)


def test_discount_percent(de_vat):
    assert discount_percent(D(200), D(10)) == D(180)
    assert discount_percent(200, 10) == D(180)
    assert discount_percent("200", "10") == D(180)


def test_discount_amount(de_vat):
    assert discount_amount(D(200), D(10)) == D(190)
    assert discount_amount(200, 10) == D(190)
    assert discount_amount("200", "10") == D(190)
