import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.fixture_models import UserFixtureModel


@pytest.fixture
def create_user_request() -> CreateUserRequest:
    return RandomModelGenerator.generate(CreateUserRequest)

@pytest.fixture
def created_user(
        api_manager: ApiManager,
        create_user_request: CreateUserRequest
) -> UserFixtureModel:
    user_response = api_manager.admin_steps.create_user(create_user_request)

    return UserFixtureModel(
        user_id=user_response.id,
        username=create_user_request.username,
        password=create_user_request.password,
        role=create_user_request.role
    )

