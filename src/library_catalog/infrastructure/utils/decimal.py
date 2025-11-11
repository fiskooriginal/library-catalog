from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy import Numeric


def decimal_to_numeric(value: Decimal | None, quant: Decimal, rounding=ROUND_HALF_UP) -> Numeric | None:
    if value is None:
        return None
    return Numeric(str(value.quantize(quant, rounding=rounding)))


def numeric_to_decimal(value: Numeric | None, quant: Decimal, rounding=ROUND_HALF_UP) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value)).quantize(quant, rounding=rounding)


def float_to_decimal(value: float | int | None, quant: Decimal, rounding=ROUND_HALF_UP) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value)).quantize(quant, rounding=rounding)
