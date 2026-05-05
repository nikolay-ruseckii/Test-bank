import pytest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def test_account(api_manager, created_user):
    account_response = api_manager.user_steps.create_account(
        CreateUserRequest(
            username=created_user["username"],
            password=created_user["password"],
            role=created_user["role"]
        )
    )

    return {
        "account_id": account_response.id,
        "user_id": created_user["id"],
        "username": created_user["username"],
        "password": created_user["password"],
        "balance": account_response.balance
    }