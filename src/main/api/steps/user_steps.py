from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()

    def deposit(self, deposit_request: DepositRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)

        self.created_obj.append(response)
        return response

    def deposit_invalid_amount(
            self,
            account_id: int,
            amount: int,
            username: str,
            password: str
    ):
        body = {
            "accountId": account_id,
            "amount": amount
        }

        return self.deposit_raw(
            body,
            username=username,
            password=password
        )

    def deposit_to_account(
            self,
            account_id: int,
            amount: int,
            username: str,
            password: str
    ):
        deposit_request = DepositRequest(
            account_id=account_id,
            amount=amount
        )

        return self.deposit(
            deposit_request,
            username=username,
            password=password
        )

    def deposit_raw(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad()
        ).post_raw(body)

    def transfer(self, transfer_request: TransferRequest, username: str, password: str):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)

    def transfer_between_accounts(
            self,
            from_account_id: int,
            to_account_id: int,
            amount: int,
            username: str,
            password: str
    ):
        transfer_request = TransferRequest(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount
        )

        return self.transfer(
            transfer_request,
            username=username,
            password=password
        )

    def transfer_invalid_amount(
            self,
            from_account_id: int,
            to_account_id: int,
            amount: int,
            username: str,
            password: str
    ):
        body = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": amount
        }

        return self.transfer_raw(
            body,
            username=username,
            password=password
        )

    def transfer_raw(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_bad()
        ).post_raw(body)

    def credit_request(self, credit_request: CreditRequest, username: str, password: str):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)

    def request_credit_for_account(
            self,
            account_id: int,
            amount: int,
            term_months: int,
            username: str,
            password: str
    ):
        credit_request = CreditRequest(
            account_id=account_id,
            amount=amount,
            term_months=term_months
        )

        return self.credit_request(
            credit_request,
            username=username,
            password=password
        )

    def request_credit_raw(
            self,
            account_id: int,
            amount: int,
            term_months: int,
            username: str,
            password: str
    ):
        body = {
            "accountId": account_id,
            "amount": amount,
            "termMonths": term_months
        }

        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden()
        ).post_raw(body)

    def request_second_credit_raw(
            self,
            account_id: int,
            amount: int,
            term_months: int,
            username: str,
            password: str
    ):
        body = {
            "accountId": account_id,
            "amount": amount,
            "termMonths": term_months
        }

        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_not_found()
        ).post_raw(body)

    def credit_repay(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post_raw(body)

    def repay_credit(
            self,
            credit_id: int,
            account_id: int,
            amount: int,
            username: str,
            password: str
    ):
        body = {
            "creditId": credit_id,
            "accountId": account_id,
            "amount": amount
        }

        return self.credit_repay(
            body,
            username=username,
            password=password
        )

    def repay_credit_raw(
            self,
            credit_id: int,
            account_id: int,
            amount: int,
            username: str,
            password: str
    ):
        body = {
            "creditId": credit_id,
            "accountId": account_id,
            "amount": amount
        }

        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable_entity()
        ).post_raw(body)

