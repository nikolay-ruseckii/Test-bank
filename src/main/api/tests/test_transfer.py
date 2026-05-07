import allure
from requests import Session
import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.fixture_models import FundedTwoAccountsFixtureModel
from src.main.api.models.fixture_models import TwoAccountsFixtureModel


@allure.feature("Transfer")
@pytest.mark.api
class TestTransfer:

    @allure.title("Перевод между своими счетами")
    def test_transfer(
            self,
            api_manager: ApiManager,
            funded_two_accounts: FundedTwoAccountsFixtureModel
    ):
        response = api_manager.user_steps.transfer_between_accounts(
            from_account_id=funded_two_accounts.account_1,
            to_account_id=funded_two_accounts.account_2,
            amount=funded_two_accounts.transfer_amount,
            username=funded_two_accounts.username,
            password=funded_two_accounts.password
        )

        assert response.from_account_id == funded_two_accounts.account_1
        assert response.to_account_id == funded_two_accounts.account_2
        assert response.from_account_id_balance == (
                funded_two_accounts.start_balance - funded_two_accounts.transfer_amount
        )

    @allure.title("Перевод при недостаточном балансе")
    def test_transfer_insufficient_funds(
            self,
            api_manager: ApiManager,
            user_with_two_accounts: TwoAccountsFixtureModel,
            transfer_data: dict
    ):
        response = api_manager.user_steps.transfer_insufficient_funds(
            from_account_id=user_with_two_accounts.account_1,
            to_account_id=user_with_two_accounts.account_2,
            amount=transfer_data["insufficient_funds_amount"],
            username=user_with_two_accounts.username,
            password=user_with_two_accounts.password
        )

        assert "Insufficient funds" in response.text

    @allure.title("Проверка БД после перевода")
    def test_transfer_db(
            self,
            db_session: Session,
            api_manager: ApiManager,
            funded_two_accounts: dict
    ):
        api_manager.user_steps.transfer_between_accounts(
            from_account_id=funded_two_accounts.account_1,
            to_account_id=funded_two_accounts.account_2,
            amount=funded_two_accounts.transfer_amount,
            username=funded_two_accounts.username,
            password=funded_two_accounts.password
        )

        acc1 = AccountCrudDb.get_account_by_id(
            db_session,
            funded_two_accounts.account_1
        )

        acc2 = AccountCrudDb.get_account_by_id(
            db_session,
            funded_two_accounts.account_2
        )

        assert acc1.balance == funded_two_accounts.start_balance - funded_two_accounts.transfer_amount
        assert acc2.balance == funded_two_accounts.transfer_amount