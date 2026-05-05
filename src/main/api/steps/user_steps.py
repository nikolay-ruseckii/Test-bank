from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester



class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, deposit_request: DepositRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)

        self.created_obj.append(response)
        return response

    def deposit_raw(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad()
        ).post_raw(body)

    def transfer(self, transfer_request: TransferRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)

        return response

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

    def credit_request_raw(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden()
        ).post_raw(body)

    def credit_repay(self, body: dict,  username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post_raw(body)

    def credit_repay_raw(self, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post_row(None)

    def credit_repay_raw(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable_entity()
        ).post_raw(body)

    def credit_request_second_raw(self, body: dict, username: str, password: str):
        return CrudRequester(
            RequestSpecs.auth_headers(username=username, password=password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_not_found()
        ).post_raw(body)