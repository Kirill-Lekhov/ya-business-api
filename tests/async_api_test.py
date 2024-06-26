from ya_business_api.async_api import AsyncAPI
from ya_business_api.core.constants import Cookie
from ya_business_api.core.exceptions import CSRFTokenError

from typing import Optional
from unittest.mock import patch
from logging import DEBUG

from aiohttp.client import ClientSession
import pytest


class FakeGetCSRFTokenFunction:
	def __init__(self, token: Optional[str] = None):
		self.token = token

	async def __call__(self, *args, **kwargs) -> Optional[str]:
		return self.token


@pytest.mark.asyncio
class TestAsyncAPI:
	async def test___init__(self):
		session = ClientSession()
		session.cookie_jar.update_cookies(
			{
				Cookie.SESSION_ID.value: "SESSIONID",
				Cookie.SESSION_ID2.value: "SESSIONID2",
			},
		)
		api = AsyncAPI("CSRFTOKEN", session)
		assert api.reviews.csrf_token == api.reviews.csrf_token == "CSRFTOKEN"
		assert api.reviews.session is api.session is session

	async def test_make_session(self):
		session = await AsyncAPI.make_session("SESSIONID1", "SESSIONID2")
		cookies = {cookie.key: cookie.value for cookie in session.cookie_jar}
		assert isinstance(session, ClientSession)
		assert cookies.get(Cookie.SESSION_ID.value) == "SESSIONID1"
		assert cookies.get(Cookie.SESSION_ID2.value) == "SESSIONID2"

	async def test_build(self, caplog):
		with patch.object(AsyncAPI, "make_session", wraps=AsyncAPI.make_session) as make_session_method:
			api = await AsyncAPI.build("SESSION1", "SESSION2", "CSRFTOKEN")
			cookies = {cookie.key: cookie.value for cookie in api.session.cookie_jar}
			make_session_method.assert_called_once()
			assert api.csrf_token == "CSRFTOKEN"
			assert cookies.get(Cookie.SESSION_ID.value) == "SESSION1"
			assert cookies.get(Cookie.SESSION_ID2.value) == "SESSION2"
			await api.session.close()

		caplog.set_level(DEBUG)

		with patch("ya_business_api.async_api.AsyncServiceAPI.get_csrf_token", FakeGetCSRFTokenFunction("TOKEN")):
			api = await AsyncAPI.build("SESSION1", "SESSION2")
			cookies = {cookie.key: cookie.value for cookie in api.session.cookie_jar}
			assert api.csrf_token == "TOKEN"
			assert cookies.get(Cookie.SESSION_ID.value) == "SESSION1"
			assert cookies.get(Cookie.SESSION_ID2.value) == "SESSION2"

			for record in caplog.records:
				assert record.levelname == "INFO"

			assert "CSRF token was not specified. Attempting to receive a token automatically..." in caplog.text

		with pytest.raises(
			CSRFTokenError,
			match=r"Failed to get CSRF token\. It is not possible to create a client instance"
		):
			with patch("ya_business_api.async_api.AsyncServiceAPI.get_csrf_token", FakeGetCSRFTokenFunction(None)):
				api = await AsyncAPI.build("SESSION1", "SESSION2")
