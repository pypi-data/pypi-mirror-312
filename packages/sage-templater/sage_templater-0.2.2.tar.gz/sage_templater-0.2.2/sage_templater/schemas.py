from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SmallBoxRecordSchema(BaseModel):
    """Small box record schema."""

    code: Optional[str] = None
    national_id: Optional[str] = None
    verification_digit: Optional[str] = None
    name: str
    invoice: Optional[str] = None
    date: str
    amount: Decimal
    tax: Decimal
    total: Decimal
    description: str
    source_file: Optional[str] = None
    source_sheet: Optional[str] = None
