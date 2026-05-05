import pytest
import logging
from typing import List, Any

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.steps.user_steps import UserSteps


@pytest.fixture
def created_obj():
    objects: List[Any] = []
    yield objects
    clean_user(objects)

def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects)

    for u in objects:
        if isinstance(u, CreateUserResponse):
            try:
                api_manager.admin_steps.delete_user(u.id)
            except AssertionError as e:
                if "User not found" not in str(e):
                    raise
        else:
            logging.warning(f"Error in delete user_id : {u.id}")