import allure
import pytest

from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.models.credit_table import Credit
from src.main.api.db.crud.account_crud import AccountCrudDb


@pytest.mark.api
@allure.feature("Кредит")
class TestCredit:

    @allure.title("Позитивный тест запроса кредита")
    def test_credit_request_positive(self, api_manager, credit_user):
        credit_request = CreditRequest(
            account_id=credit_user["account_id"],
            amount=10000,
            term_months=12
        )

        response = api_manager.user_steps.credit_request(
            credit_request,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        assert response is not None

    @allure.title("Негативный тест: пользователь без роли не может взять кредит")
    def test_credit_request_without_role(self, api_manager, user_account_without_credit_role):
        body = {
            "accountId": user_account_without_credit_role["account_id"],
            "amount": 10000,
            "termMonths": 12
        }

        response = api_manager.user_steps.credit_request_raw(
            body,
            username=user_account_without_credit_role["username"],
            password=user_account_without_credit_role["password"]
        )

        assert response.status_code == 403

    @allure.title("Позитивный тест: погашение кредита")
    def test_credit_repay_positive(self, api_manager, credit_user):
        # 1. берём кредит
        credit_request = CreditRequest(
            account_id=credit_user["account_id"],
            amount=10000,
            term_months=12
        )

        credit_response = api_manager.user_steps.credit_request(
            credit_request,
            username=credit_user["username"],
            password=credit_user["password"]
        )
        body = {
            "creditId": credit_response.credit_id,
            "accountId": credit_user["account_id"],
            "amount": 10000
        }

        # 2. гасим кредит
        response = api_manager.user_steps.credit_repay(
            body,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        assert response is not None

    @allure.title("Негативный тест: повторное погашение кредита")
    def test_credit_repay_twice(self, api_manager, credit_user):
        credit_request = CreditRequest(
            account_id=credit_user["account_id"],
            amount=10000,
            term_months=12
        )

        credit_response = api_manager.user_steps.credit_request(
            credit_request,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        body = {
            "creditId": credit_response.credit_id,
            "accountId": credit_user["account_id"],
            "amount": 10000
        }

        # первый раз — ок
        api_manager.user_steps.credit_repay(
            body,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        # второй раз — ошибка
        response = api_manager.user_steps.credit_repay_raw(
            body,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        assert response.status_code == 422

    @allure.title("Негативный тест: нельзя взять второй кредит")
    def test_second_credit_not_allowed(self, api_manager, credit_user):
        credit_request = CreditRequest(
            account_id=credit_user["account_id"],
            amount=10000,
            term_months=12
        )

        api_manager.user_steps.credit_request(
            credit_request,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        response = api_manager.user_steps.credit_request_second_raw(
            {
                "accountId": credit_user["account_id"],
                "amount": 10000,
                "termMonths": 12
            },
            username=credit_user["username"],
            password=credit_user["password"]
        )

        assert response.status_code == 404

    @allure.title("Негативный тест: нельзя взять кредит на второй счет")
    def test_credit_on_second_account_not_allowed(self, api_manager, credit_user_with_two_accounts):
        # первый кредит — ок
        first_credit = CreditRequest(
            account_id=credit_user_with_two_accounts["account_1"],
            amount=10000,
            term_months=12
        )

        api_manager.user_steps.credit_request(
            first_credit,
            username=credit_user_with_two_accounts["username"],
            password=credit_user_with_two_accounts["password"]
        )

        # второй кредит на другой счет — ошибка
        response = api_manager.user_steps.credit_request_second_raw(
            {
                "accountId": credit_user_with_two_accounts["account_2"],
                "amount": 10000,
                "termMonths": 12
            },
            username=credit_user_with_two_accounts["username"],
            password=credit_user_with_two_accounts["password"]
        )

        assert response.status_code == 404

    @allure.title("Проверка БД после запроса кредита")
    def test_credit_request_db(self, db_session, api_manager, credit_user):
        credit_request = CreditRequest(
            account_id=credit_user["account_id"],
            amount=10000,
            term_months=12
        )

        response = api_manager.user_steps.credit_request(
            credit_request,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        credit_from_db = Credit.get_credit_by_id(
            db_session,
            response.credit_id
        )

        assert credit_from_db is not None, "Кредит не записался в БД"
        assert credit_from_db.amount == 10000

    @allure.title("Проверка БД после погашения кредита")
    def test_credit_repay_db(self, db_session, api_manager, credit_user):
        credit_request = CreditRequest(
            account_id=credit_user["account_id"],
            amount=10000,
            term_months=12
        )

        response = api_manager.user_steps.credit_request(
            credit_request,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        body = {
            "creditId": response.credit_id,
            "accountId": credit_user["account_id"],
            "amount": 10000
        }

        api_manager.user_steps.credit_repay(
            body,
            username=credit_user["username"],
            password=credit_user["password"]
        )

        credit_from_db = Credit.get_credit_by_id(
            db_session,
            response.credit_id
        )

        account_from_db = AccountCrudDb.get_account_by_id(
            db_session,
            credit_user["account_id"]
        )

        assert credit_from_db is not None, "Кредитная запись пропала из БД"
        assert account_from_db.balance == 0, "Кредит не списался с баланса"
