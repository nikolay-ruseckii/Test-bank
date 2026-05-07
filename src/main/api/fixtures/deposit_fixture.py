import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.deposit_data_generator import DepositDataGenerator
from src.main.api.models.fixture_models import DepositDataFixtureModel, UserFixtureModel
from src.main.api.models.fixture_models import AccountFixtureModel


@pytest.fixture
def test_account(
        api_manager: ApiManager,
        created_user: UserFixtureModel
) -> AccountFixtureModel:
    user_request = CreateUserRequest(
        username=created_user.username,
        password=created_user.password,
        role=created_user.role
    )

    account_response = api_manager.user_steps.create_account(user_request)

    return AccountFixtureModel(
        user_id=created_user.user_id,
        username=created_user.username,
        password=created_user.password,
        role=created_user.role,
        account_id=account_response.id,
        balance=account_response.balance
    )

@pytest.fixture
def deposit_data() -> DepositDataFixtureModel:
    return DepositDataFixtureModel(
        amount=DepositDataGenerator.amount(),
        invalid_low_amount=DepositDataGenerator.invalid_low_amount()
    )