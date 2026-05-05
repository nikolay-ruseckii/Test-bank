from pydantic import Field
from src.main.api.models.base_model import BaseModel


class TransferRequest(BaseModel):
    from_account_id: int = Field(..., alias="fromAccountId")
    to_account_id: int = Field(..., alias="toAccountId")
    amount: float = Field(..., ge=500, le=10000)