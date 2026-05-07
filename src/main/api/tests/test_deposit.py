import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.fixture_models import (
    AccountFixtureModel,
    DepositDataFixtureModel,
)


@allure.feature("Депозит")
@pytest.mark.api
class TestDeposit:

    @allure.title("Пополнение счета")
    def test_deposit(
            self,
            api_manager: ApiManager,
            test_account: AccountFixtureModel,
            deposit_data: DepositDataFixtureModel
    ):
        response = api_manager.user_steps.deposit_to_account(
            account_id=test_account.account_id,
            amount=deposit_data.amount,
            username=test_account.username,
            password=test_account.password
        )

        assert response.id == test_account.account_id
        assert response.balance == test_account.balance + deposit_data.amount

    @allure.title("Пополнение счета суммой меньше минимальной")
    def test_deposit_amount_too_low(
            self,
            api_manager: ApiManager,
            test_account: AccountFixtureModel,
            deposit_data: DepositDataFixtureModel
    ):
        response = api_manager.user_steps.deposit_invalid_amount(
            account_id=test_account.account_id,
            amount=deposit_data.invalid_low_amount,
            username=test_account.username,
            password=test_account.password
        )

        assert "amount" in response.text.lower() or "between" in response.text.lower()

    @allure.title("Проверка БД после пополнения счета")
    def test_deposit_db(
            self,
            db_session: Session,
            api_manager: ApiManager,
            test_account: AccountFixtureModel,
            deposit_data: DepositDataFixtureModel
    ):
        response = api_manager.user_steps.deposit_to_account(
            account_id=test_account.account_id,
            amount=deposit_data.amount,
            username=test_account.username,
            password=test_account.password
        )

        account_from_db = AccountCrudDb.get_account_by_id(
            db_session,
            test_account.account_id
        )

        assert account_from_db.balance == response.balance
        assert account_from_db.balance == test_account.balance + deposit_data.amount