from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.core.exceptions import AuthenticationError, CSRFTokenError
from ya_business_api.core.constants import INVALID_TOKEN_STATUSES, Cookie

import pytest
from requests.models import Response
from requests.sessions import Session


class Next:
	def __init__(self, url: str) -> None:
		self.url = url


class TestSyncAPIMixin:
	def test_check_response(self):
		response = Response()
		response.status_code = 302
		setattr(response, '_next', Next("https://passport.yandex.ru/auth/..."))

		with pytest.raises(AuthenticationError):
			SyncAPIMixin.check_response(response)

		for status in INVALID_TOKEN_STATUSES:
			with pytest.raises(CSRFTokenError):
				response.status_code = status
				SyncAPIMixin.check_response(response)

		with pytest.raises(AssertionError):
			response.status_code = 500
			SyncAPIMixin.check_response(response)

		response.status_code = 200
		SyncAPIMixin.check_response(response)

	def test_set_i_cookie(self):
		session = Session()
		mixin = SyncAPIMixin(session)
		mixin.set_i_cookie()
		assert session.cookies.get_dict().get(Cookie.I.value) == ""

		session.cookies.set(Cookie.I.value, "I COOKIE VALUE")
		mixin.set_i_cookie()
		assert session.cookies.get_dict().get(Cookie.I.value) == "I COOKIE VALUE"
