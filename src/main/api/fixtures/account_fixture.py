from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
import pytest

from src.main.api.models.credit_request import CreditRequest


@pytest.fixture
def user_with_two_accounts(api_manager, created_user):
    user_data = CreateUserRequest(
        username=created_user["username"],
        password=created_user["password"],
        role=created_user["role"]
    )

    acc1 = api_manager.user_steps.create_account(user_data)
    acc2 = api_manager.user_steps.create_account(user_data)

    return {
        "username": created_user["username"],
        "password": created_user["password"],
        "account_1": acc1.id,
        "account_2": acc2.id
    }