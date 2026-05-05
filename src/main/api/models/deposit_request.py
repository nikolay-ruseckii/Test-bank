from src.main.api.models.base_model import BaseModel
from pydantic import Field

class DepositRequest(BaseModel):
    account_id: int = Field(..., alias="accountId", description="ID банковского счета")
    amount: float = Field(..., ge=1000, le=9000, description="Сумма пополнения (мин 1000, макс 9000)")