import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.fixture
def create_user_request():
    return RandomModelGenerator.generate(CreateUserRequest)


@pytest.fixture
def created_user(api_manager, create_user_request):
    user_response = api_manager.admin_steps.create_user(create_user_request)

    return {
        "id": user_response.id,
        "username": create_user_request.username,
        "password": create_user_request.password,
        "role": create_user_request.role
    }

@pytest.fixture
def user_account_without_credit_role(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_USER"

    user_response = api_manager.admin_steps.create_user(user_request)
    account_response = api_manager.user_steps.create_account(user_request)

    return {
        "user_id": user_response.id,
        "username": user_request.username,
        "password": user_request.password,
        "role": user_request.role,
        "account_id": account_response.id
    }