import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.transfer_data_generator import TransferDataGenerator
from src.main.api.models.fixture_models import (FundedTwoAccountsFixtureModel, TwoAccountsFixtureModel)


@pytest.fixture
def transfer_data() -> dict:
    return {
        "amount": TransferDataGenerator.amount(),
        "insufficient_funds_amount": TransferDataGenerator.insufficient_funds_amount()
    }


@pytest.fixture
def funded_two_accounts(
        api_manager: ApiManager,
        user_with_two_accounts: TwoAccountsFixtureModel,
        transfer_data: dict
) -> FundedTwoAccountsFixtureModel:
    start_balance = TransferDataGenerator.start_balance(
        transfer_data["amount"]
    )

    api_manager.user_steps.deposit_to_account(
        account_id=user_with_two_accounts.account_1,
        amount=start_balance,
        username=user_with_two_accounts.username,
        password=user_with_two_accounts.password
    )

    return FundedTwoAccountsFixtureModel(
        user_id=user_with_two_accounts.user_id,
        username=user_with_two_accounts.username,
        password=user_with_two_accounts.password,
        role=user_with_two_accounts.role,
        account_1=user_with_two_accounts.account_1,
        account_2=user_with_two_accounts.account_2,
        start_balance=start_balance,
        transfer_amount=transfer_data["amount"]
    )
