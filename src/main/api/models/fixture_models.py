from src.main.api.models.base_model import BaseModel


class UserFixtureModel(BaseModel):
    user_id: int | None = None
    username: str
    password: str
    role: str | None = None


class AccountFixtureModel(UserFixtureModel):
    account_id: int
    balance: float | int = 0


class TwoAccountsFixtureModel(UserFixtureModel):
    account_1: int
    account_2: int


class FundedTwoAccountsFixtureModel(TwoAccountsFixtureModel):
    start_balance: float | int
    transfer_amount: float | int


class CreditFixtureModel(AccountFixtureModel):
    credit_id: int | None = None
    amount: int | None = None
    term_months: int | None = None


class CreditUserWithTwoAccountsFixtureModel(TwoAccountsFixtureModel):
    pass


class UserWithCreditAndSecondAccountFixtureModel(TwoAccountsFixtureModel):
    credit_id: int
    amount: int
    term_months: int

class CreditDataFixtureModel(BaseModel):
    amount: int
    term_months: int


class DepositDataFixtureModel(BaseModel):
    amount: int
    invalid_low_amount: int


class TransferDataFixtureModel(BaseModel):
    amount: int
    insufficient_funds_amount: int