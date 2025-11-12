from decimal import ROUND_HALF_UP, Decimal

from src.library_catalog.domain.config import RATING_STEP


def to_decimal(
    value: Decimal | float | int | str | None,
    quant: Decimal = RATING_STEP,
    rounding: str = ROUND_HALF_UP,
) -> Decimal | None:
    """
    Convert various numeric types to Decimal with quantization.

    Args:
        value: Value to convert (Decimal, float, int, str, or None)
        quant: Quantization step (default: RATING_STEP)
        rounding: Rounding mode (default: ROUND_HALF_UP)

    Returns:
        Quantized Decimal or None if input is None

    Raises:
        ValueError: If value cannot be converted to Decimal
    """
    if value is None:
        return None

    try:
        # Always convert to Decimal via string to avoid float precision issues
        decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
        return decimal_value.quantize(quant, rounding=rounding)
    except (ValueError, TypeError, ArithmeticError) as e:
        raise ValueError(f"Cannot convert {value!r} (type: {type(value).__name__}) to Decimal: {e}") from e


def to_float(
    value: Decimal | float | int | str | None,
    quant: Decimal = RATING_STEP,
    rounding: str = ROUND_HALF_UP,
) -> float | None:
    """
    Convert various numeric types to float with quantization.

    Args:
        value: Value to convert (Decimal, float, int, str, or None)
        quant: Quantization step (default: RATING_STEP)
        rounding: Rounding mode (default: ROUND_HALF_UP)

    Returns:
        Quantized float or None if input is None

    Raises:
        ValueError: If value cannot be converted
    """
    decimal_value = to_decimal(value, quant, rounding)
    return float(decimal_value) if decimal_value is not None else None


def to_int(
    value: Decimal | float | int | str | None,
    quant: Decimal = RATING_STEP,
    rounding: str = ROUND_HALF_UP,
) -> int | None:
    """
    Convert various numeric types to int with quantization.

    Args:
        value: Value to convert (Decimal, float, int, str, or None)
        quant: Quantization step (default: RATING_STEP)
        rounding: Rounding mode (default: ROUND_HALF_UP)

    Returns:
        Quantized int or None if input is None

    Raises:
        ValueError: If value cannot be converted
    """
    decimal_value = to_decimal(value, quant, rounding)
    return int(decimal_value) if decimal_value is not None else None
