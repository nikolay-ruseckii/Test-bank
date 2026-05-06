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

