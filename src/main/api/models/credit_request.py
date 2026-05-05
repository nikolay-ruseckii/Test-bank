from pydantic import Field
from src.main.api.models.base_model import BaseModel


class CreditRequest(BaseModel):
    account_id: int = Field(..., alias="accountId")
    amount: int = Field(..., ge=5000, le=15000)
    term_months: int = Field(..., alias="termMonths")