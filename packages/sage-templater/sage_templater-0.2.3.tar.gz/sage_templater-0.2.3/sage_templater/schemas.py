from decimal import Decimal
from typing import Annotated, AnyStr, Optional

from pydantic import AfterValidator, BaseModel, BeforeValidator


def validate_tax(value: AnyStr):
    """Validate the tax value."""
    if isinstance(value, tuple):
        value = value[0]
    if value is None or len(value) == 0 or value == "None":
        return Decimal("0.0")
    return Decimal(value)


Tax = Annotated[Decimal, BeforeValidator(validate_tax)]


class SmallBoxRecordSchema(BaseModel):
    """Small box record schema."""

    code: Optional[str] = None
    national_id: Optional[str] = None
    verification_digit: Optional[str] = None
    name: str
    invoice: Optional[str] = None
    date: str
    amount: Decimal
    tax: Tax
    total: Decimal
    description: str
    source_file: Optional[str] = None
    source_sheet: Optional[str] = None
