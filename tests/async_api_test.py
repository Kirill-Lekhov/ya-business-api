from ya_business_api.async_api import AsyncAPI
from ya_business_api.core.constants import Cookie

from unittest.mock import patch

from aiohttp.client import ClientSession
import pytest


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
		api = AsyncAPI(1212, "CSRFTOKEN", session)
		assert api.reviews.permanent_id == api.permanent_id == 1212
		assert api.reviews.csrf_token == api.reviews.csrf_token == "CSRFTOKEN"
		assert api.reviews.session is api.session is session

	async def test_make_session(self):
		session = await AsyncAPI.make_session("SESSIONID1", "SESSIONID2")
		cookies = {cookie.key: cookie.value for cookie in session.cookie_jar}
		assert isinstance(session, ClientSession)
		assert cookies.get(Cookie.SESSION_ID.value) == "SESSIONID1"
		assert cookies.get(Cookie.SESSION_ID2.value) == "SESSIONID2"

	async def test_build(self):
		with patch.object(AsyncAPI, "make_session", wraps=AsyncAPI.make_session) as make_session_method:
			api = await AsyncAPI.build(1212, "CSRFTOKEN", "SESSION1", "SESSION2")
			cookies = {cookie.key: cookie.value for cookie in api.session.cookie_jar}
			make_session_method.assert_called_once()
			assert api.permanent_id == 1212
			assert api.csrf_token == "CSRFTOKEN"
			assert cookies.get(Cookie.SESSION_ID.value) == "SESSION1"
			assert cookies.get(Cookie.SESSION_ID2.value) == "SESSION2"
