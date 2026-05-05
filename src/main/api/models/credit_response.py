from pydantic import Field
from src.main.api.models.base_model import BaseModel


class CreditResponse(BaseModel):
    id: int
    amount: int
    term_months: int = Field(..., alias="termMonths")
    balance: int
    credit_id: int = Field(..., alias="creditId")