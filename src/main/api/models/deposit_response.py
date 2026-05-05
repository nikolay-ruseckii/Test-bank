from src.main.api.models.base_model import BaseModel
from pydantic import Field

class DepositResponse(BaseModel):
    id: int = Field(..., description="ID счета")
    balance: float = Field(..., description="Новый баланс")