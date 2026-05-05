import allure
from requests import Session
import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb

@allure.feature("Transfer")
@pytest.mark.api
class TestTransfer:

    @allure.title("Позитивный перевод между своими счетами")
    def test_transfer_positive(self, api_manager, user_with_two_accounts):
        deposit_request = DepositRequest(
            account_id=user_with_two_accounts["account_1"],
            amount=5000
        )
        api_manager.user_steps.deposit(
            deposit_request,
            username=user_with_two_accounts["username"],
            password=user_with_two_accounts["password"]
        )


        transfer_request = TransferRequest(
            from_account_id=user_with_two_accounts["account_1"],
            to_account_id=user_with_two_accounts["account_2"],
            amount=1000
        )

        response = api_manager.user_steps.transfer(
            transfer_request,
            username=user_with_two_accounts["username"],
            password=user_with_two_accounts["password"]
        )

        assert response is not None


    @allure.title("Негативный тест: недостаточно средств")
    def test_transfer_insufficient_funds(self, api_manager, user_with_two_accounts):

        body = {
            "fromAccountId": user_with_two_accounts["account_1"],
            "toAccountId": user_with_two_accounts["account_2"],
            "amount": 999999
        }

        response = api_manager.user_steps.transfer_raw(
            body,
            username=user_with_two_accounts["username"],
            password=user_with_two_accounts["password"]
        )

        assert response.status_code == 400

    @pytest.mark.api
    def test_transfer_db(self, db_session: Session, api_manager: ApiManager, user_with_two_accounts):

        # пополняем
        deposit_request = DepositRequest(
            account_id=user_with_two_accounts["account_1"],
            amount=5000
        )

        api_manager.user_steps.deposit(
            deposit_request,
            username=user_with_two_accounts["username"],
            password=user_with_two_accounts["password"]
        )

        # перевод
        transfer_request = TransferRequest(
            from_account_id=user_with_two_accounts["account_1"],
            to_account_id=user_with_two_accounts["account_2"],
            amount=1000
        )

        api_manager.user_steps.transfer(
            transfer_request,
            username=user_with_two_accounts["username"],
            password=user_with_two_accounts["password"]
        )

        # DB проверка
        acc1 = AccountCrudDb.get_account_by_id(
            db_session,
            user_with_two_accounts["account_1"]
        )

        acc2 = AccountCrudDb.get_account_by_id(
            db_session,
            user_with_two_accounts["account_2"]
        )

        assert acc1.balance == 4000, "Ошибка списания"
        assert acc2.balance == 1000, "Ошибка зачисления"