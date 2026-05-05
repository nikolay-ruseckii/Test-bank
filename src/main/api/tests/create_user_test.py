import pytest
import allure
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.db.crud.user_crud import UserCrudDb

@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Созданного пользователя не нашли в БД'


    @pytest.mark.parametrize(
        "username,password",
        [("абв", "Pas!sw0rd"),
         ("ab", "Pas!sw0rd"),
         ("abv!", "Pas!sw0rd"),
         ("Maxx1", "Pas!sw0rД"),
         ("Maxx2", "Pas!sw0"),
         ("Maxx3", "pas!sw0rd"),
         ("Maxx4", "PAS!SW0RD"),
         ("Maxx5", "PASSW0RD"),
         ("Maxx6", "PAS!WRRD"),
         ]
    )
    def test_create_user_invalid(self,db_session: Session, username:str, password:str, api_manager: ApiManager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'Пользоватьель создан, ошибка'

    @allure.title("Админ может удалить пользователя")
    def test_admin_delete_user(self, api_manager, db_session, create_user_request):
        user_response = api_manager.admin_steps.create_user(create_user_request)

        api_manager.admin_steps.delete_user(user_response.id)

        user_from_db = UserCrudDb.get_user_by_username(
            db_session,
            create_user_request.username
        )

        assert user_from_db is not None
        assert user_from_db.deleted_at is not None, "Пользователь не удалился из БД"


