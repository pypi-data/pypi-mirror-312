from decimal import Decimal


def quant2(d: Decimal) -> Decimal:
    """Quantize input to 2 decimal places."""
    return d.quantize(Decimal("0.01"))


def net_to_gross(amount: Decimal, vat: Decimal) -> Decimal:
    """Calculate gross amount from a net amount."""
    return quant2(Decimal(amount) * (100 + vat) / 100)


def gross_to_net(amount: Decimal, vat: Decimal) -> Decimal:
    """Calculate net amount from a gross amount."""
    return quant2(100 * Decimal(amount) / (100 + vat))


def vat_amount_from_net(amount: Decimal, vat: Decimal) -> Decimal:
    """Calculate VAT amount from a net amount."""
    return quant2(Decimal(amount) * vat / 100)


def vat_amount_from_gross(amount: Decimal, vat: Decimal) -> Decimal:
    """Calculate VAT amount from a gross (VAT-inclusive) amount."""
    da = Decimal(amount)
    return quant2(da - (da / (100 + vat) * 100))


def discount_percent(amount: Decimal, discount: Decimal) -> Decimal:
    """Calculate an amount after applying a percent discount."""
    da = Decimal(amount)
    dd = Decimal(discount)
    return quant2(Decimal(da - (da * dd / 100)))


def discount_amount(amount: Decimal, discount: Decimal) -> Decimal:
    """Calculate an amount after applying a fixed amount discount."""
    return quant2(Decimal(amount) - Decimal(discount))
