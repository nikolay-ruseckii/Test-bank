from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
import pytest

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

@pytest.fixture
def credit_user(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    user_response = api_manager.admin_steps.create_user(user_request)
    account_response = api_manager.user_steps.create_account(user_request)

    return {
        "user_id": user_response.id,
        "username": user_request.username,
        "password": user_request.password,
        "role": user_request.role,
        "account_id": account_response.id,
        "balance": account_response.balance
    }

@pytest.fixture
def credit_user_with_two_accounts(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    user_response = api_manager.admin_steps.create_user(user_request)

    acc1 = api_manager.user_steps.create_account(user_request)
    acc2 = api_manager.user_steps.create_account(user_request)

    return {
        "user_id": user_response.id,
        "username": user_request.username,
        "password": user_request.password,
        "account_1": acc1.id,
        "account_2": acc2.id
    }