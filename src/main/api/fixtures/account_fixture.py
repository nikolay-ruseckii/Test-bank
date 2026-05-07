import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.fixture_models import UserFixtureModel, TwoAccountsFixtureModel


@pytest.fixture
def user_with_two_accounts(
        api_manager: ApiManager,
        created_user: UserFixtureModel
) -> TwoAccountsFixtureModel:
    user_request = CreateUserRequest(
        username=created_user.username,
        password=created_user.password,
        role=created_user.role
    )

    acc1 = api_manager.user_steps.create_account(user_request)
    acc2 = api_manager.user_steps.create_account(user_request)

    return TwoAccountsFixtureModel(
        user_id=created_user.user_id,
        username=created_user.username,
        password=created_user.password,
        role=created_user.role,
        account_1=acc1.id,
        account_2=acc2.id
    )