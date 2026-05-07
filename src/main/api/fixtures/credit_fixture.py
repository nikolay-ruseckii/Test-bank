import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.credit_data_generator import CreditDataGenerator
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.fixture_models import CreditDataFixtureModel
from src.main.api.models.fixture_models import (
    AccountFixtureModel,
    CreditFixtureModel,
    TwoAccountsFixtureModel,
    UserWithCreditAndSecondAccountFixtureModel,
)



@pytest.fixture
def credit_data() -> CreditDataFixtureModel:
    return CreditDataFixtureModel(
        amount=CreditDataGenerator.amount(),
        term_months=CreditDataGenerator.term_months()
    )


@pytest.fixture
def credit_user(api_manager: ApiManager) -> AccountFixtureModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    user_response = api_manager.admin_steps.create_user(user_request)
    account_response = api_manager.user_steps.create_account(user_request)

    return AccountFixtureModel(
        user_id=user_response.id,
        username=user_request.username,
        password=user_request.password,
        role=user_request.role,
        account_id=account_response.id,
        balance=account_response.balance
    )


@pytest.fixture
def credit_user_with_two_accounts(api_manager: ApiManager) -> TwoAccountsFixtureModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    user_response = api_manager.admin_steps.create_user(user_request)

    acc1 = api_manager.user_steps.create_account(user_request)
    acc2 = api_manager.user_steps.create_account(user_request)

    return TwoAccountsFixtureModel(
        user_id=user_response.id,
        username=user_request.username,
        password=user_request.password,
        role=user_request.role,
        account_1=acc1.id,
        account_2=acc2.id
    )


@pytest.fixture
def user_account_without_credit_role(api_manager: ApiManager) -> AccountFixtureModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_USER"

    user_response = api_manager.admin_steps.create_user(user_request)
    account_response = api_manager.user_steps.create_account(user_request)

    return AccountFixtureModel(
        user_id=user_response.id,
        username=user_request.username,
        password=user_request.password,
        role=user_request.role,
        account_id=account_response.id,
        balance=account_response.balance
    )


@pytest.fixture
def active_credit(
        api_manager: ApiManager,
        credit_user: AccountFixtureModel,
        credit_data: CreditDataFixtureModel
) -> CreditFixtureModel:
    credit_response = api_manager.user_steps.request_credit_for_account(
        account_id=credit_user.account_id,
        amount=credit_data.amount,
        term_months=credit_data.term_months,
        username=credit_user.username,
        password=credit_user.password
    )

    return CreditFixtureModel(
        user_id=credit_user.user_id,
        username=credit_user.username,
        password=credit_user.password,
        role=credit_user.role,
        account_id=credit_user.account_id,
        balance=credit_response.balance,
        credit_id=credit_response.credit_id,
        amount=credit_response.amount,
        term_months=credit_response.term_months
    )


@pytest.fixture
def user_with_credit_and_second_account(
        api_manager: ApiManager,
        credit_user_with_two_accounts: TwoAccountsFixtureModel,
        credit_data: CreditDataFixtureModel
) -> UserWithCreditAndSecondAccountFixtureModel:
    credit_response = api_manager.user_steps.request_credit_for_account(
        account_id=credit_user_with_two_accounts.account_1,
        amount=credit_data.amount,
        term_months=credit_data.term_months,
        username=credit_user_with_two_accounts.username,
        password=credit_user_with_two_accounts.password
    )

    return UserWithCreditAndSecondAccountFixtureModel(
        user_id=credit_user_with_two_accounts.user_id,
        username=credit_user_with_two_accounts.username,
        password=credit_user_with_two_accounts.password,
        role=credit_user_with_two_accounts.role,
        account_1=credit_user_with_two_accounts.account_1,
        account_2=credit_user_with_two_accounts.account_2,
        credit_id=credit_response.credit_id,
        amount=credit_response.amount,
        term_months=credit_response.term_months
    )