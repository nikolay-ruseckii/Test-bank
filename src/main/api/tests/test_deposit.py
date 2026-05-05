import allure
import pytest
from sqlalchemy.orm import Session


from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.deposit_request import DepositRequest
from pydantic import ValidationError


@allure.feature("Депозит")
@pytest.mark.api
class TestDeposit:

    @allure.title("Позитивный тест пополнения счета")
    def test_deposit_positive(self, api_manager, test_account):
        deposit_request = DepositRequest(
            account_id=test_account["account_id"],
            amount=5000
        )

        deposit_response = api_manager.user_steps.deposit(
            deposit_request,
            username=test_account["username"],
            password=test_account["password"]
        )

        assert deposit_response.id == test_account["account_id"]
        assert deposit_response.balance == test_account["balance"] + 5000



    @allure.title("Негативный тест: сумма меньше 1000 (API)")
    def test_deposit_negative_amount_too_low_api(self, api_manager, test_account):
        body = {
            "accountId": test_account["account_id"],
            "amount": 500
        }

        response = api_manager.user_steps.deposit_raw(
            body,
            username=test_account["username"],
            password=test_account["password"]
        )

        assert response.status_code == 400

    def test_deposit_db(self, db_session: Session, api_manager: ApiManager, test_account):

        deposit_request = DepositRequest(
            account_id=test_account["account_id"],
            amount=5000
        )

        response = api_manager.user_steps.deposit(
            deposit_request,
            username=test_account["username"],
            password=test_account["password"]
        )

        # API проверка
        assert response.balance == 5000

        # DB проверка
        account_from_db = AccountCrudDb.get_account_by_id(
            db_session,
            test_account["account_id"]
        )

        assert account_from_db.balance == 5000, "Баланс не обновился в БД"
