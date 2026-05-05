from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from requests import Response
import requests
import allure

class CrudRequester(HttpRequester):
    def post(self, model: Optional [BaseModel]) -> Response:
        body = model.model_dump(by_alias=True) if model is not None else {}

        with allure.step(f"POST{Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

        response = requests.post (
            url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
            headers = self.request_spec,
            json = body
        )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )

        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        formatted_url = self.endpoint.value.url.format(user_id=user_id)

        response = requests.delete (
            url = f"{Config.fetch('backendUrl')}{formatted_url}",
            headers = self.request_spec
        )
        self.response_spec(response)
        return response

    def post_raw(self, body: dict) -> Response:
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )

        self.response_spec(response)
        return response