import allure
import pytest
from sqlalchemy.orm.session import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.models.credit_table import Credit
from src.main.api.models.fixture_models import (
    AccountFixtureModel,
    CreditFixtureModel,
    UserWithCreditAndSecondAccountFixtureModel,
    CreditDataFixtureModel
)


@pytest.mark.api
@allure.feature("Кредит")
class TestCredit:

    @allure.title("Запрос кредита")
    def test_credit_request(
            self,
            api_manager: ApiManager,
            credit_user: AccountFixtureModel,
            credit_data: CreditDataFixtureModel
    ):
        response = api_manager.user_steps.request_credit_for_account(
            account_id=credit_user.account_id,
            amount=credit_data.amount,
            term_months=credit_data.term_months,
            username=credit_user.username,
            password=credit_user.password
        )

        assert response.id == credit_user.account_id
        assert response.amount == credit_data.amount
        assert response.term_months == credit_data.term_months
        assert response.balance == credit_data.amount

    @allure.title("Запрос кредита пользователем без кредитной роли")
    def test_credit_request_without_role(
            self,
            api_manager: ApiManager,
            user_account_without_credit_role: AccountFixtureModel,
            credit_data: CreditDataFixtureModel
    ):
        response = api_manager.user_steps.request_credit_raw(
            account_id=user_account_without_credit_role.account_id,
            amount=credit_data.amount,
            term_months=credit_data.term_months,
            username=user_account_without_credit_role.username,
            password=user_account_without_credit_role.password
        )

        assert "ROLE_CREDIT" in response.text or "Forbidden" in response.text

    @allure.title("Погашение кредита")
    def test_credit_repay(
            self,
            api_manager: ApiManager,
            active_credit: CreditFixtureModel
    ):
        response = api_manager.user_steps.repay_credit(
            credit_id=active_credit.credit_id,
            account_id=active_credit.account_id,
            amount=active_credit.amount,
            username=active_credit.username,
            password=active_credit.password
        )

        assert "error" not in response.text.lower()

    @allure.title("Повторное погашение кредита запрещено")
    def test_credit_repay_twice(
            self,
            api_manager: ApiManager,
            active_credit: CreditFixtureModel
    ):
        api_manager.user_steps.repay_credit(
            credit_id=active_credit.credit_id,
            account_id=active_credit.account_id,
            amount=active_credit.amount,
            username=active_credit.username,
            password=active_credit.password
        )

        response = api_manager.user_steps.repay_credit_raw(
            credit_id=active_credit.credit_id,
            account_id=active_credit.account_id,
            amount=active_credit.amount,
            username=active_credit.username,
            password=active_credit.password
        )

        assert "Insufficient funds" in response.text

    @allure.title("Запрос второго кредита запрещён")
    def test_second_credit_not_allowed(
            self,
            api_manager: ApiManager,
            active_credit: CreditFixtureModel
    ):
        response = api_manager.user_steps.request_second_credit_raw(
            account_id=active_credit.account_id,
            amount=active_credit.amount,
            term_months=active_credit.term_months,
            username=active_credit.username,
            password=active_credit.password
        )

        assert "Only one active credit allowed" in response.text

    @allure.title("Запрос кредита на второй счёт запрещён")
    def test_credit_on_second_account_not_allowed(
            self,
            api_manager: ApiManager,
            user_with_credit_and_second_account: UserWithCreditAndSecondAccountFixtureModel
    ):
        response = api_manager.user_steps.request_second_credit_raw(
            account_id=user_with_credit_and_second_account.account_2,
            amount=user_with_credit_and_second_account.amount,
            term_months=user_with_credit_and_second_account.term_months,
            username=user_with_credit_and_second_account.username,
            password=user_with_credit_and_second_account.password
        )

        assert "Only one active credit allowed" in response.text

    @allure.title("Проверка БД после запроса кредита")
    def test_credit_request_db(
            self,
            db_session: Session,
            active_credit: CreditFixtureModel
    ):
        credit_from_db = Credit.get_credit_by_id(
            db_session,
            active_credit.credit_id
        )

        assert credit_from_db is not None, "Кредит не записался в БД"
        assert credit_from_db.amount == active_credit.amount

    @allure.title("Проверка БД после погашения кредита")
    def test_credit_repay_db(
            self,
            db_session: Session,
            api_manager: ApiManager,
            active_credit: CreditFixtureModel
    ):
        api_manager.user_steps.repay_credit(
            credit_id=active_credit.credit_id,
            account_id=active_credit.account_id,
            amount=active_credit.amount,
            username=active_credit.username,
            password=active_credit.password
        )

        credit_from_db = Credit.get_credit_by_id(
            db_session,
            active_credit.credit_id
        )

        account_from_db = AccountCrudDb.get_account_by_id(
            db_session,
            active_credit.account_id
        )

        assert credit_from_db is not None, "Кредитная запись пропала из БД"
        assert account_from_db.balance == 0, "Кредит не списался с баланса"
