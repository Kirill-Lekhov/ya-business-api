from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.core.exceptions import AuthenticationError, CSRFTokenError
from ya_business_api.core.constants import INVALID_TOKEN_STATUSES

import pytest


class Response:
	def __init__(self, status: int = 200, location: str = '') -> None:
		self.status = status
		self.headers = {'Location': location}


class TestAsyncAPIMixin:
	def test_check_response(self):
		with pytest.raises(AuthenticationError):
			AsyncAPIMixin.check_response(Response(302, "https://passport.yandex.ru/auth/..."))		# type: ignore

		for status in INVALID_TOKEN_STATUSES:
			with pytest.raises(CSRFTokenError):
				AsyncAPIMixin.check_response(Response(status))		# type: ignore

		with pytest.raises(AssertionError):
			AsyncAPIMixin.check_response(Response(500))		# type: ignore

		AsyncAPIMixin.check_response(Response(200))		# type: ignore
