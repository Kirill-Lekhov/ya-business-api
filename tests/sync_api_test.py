from ya_business_api.sync_api import SyncAPI
from ya_business_api.core.constants import Cookie
from ya_business_api.core.exceptions import CSRFTokenError

from typing import Optional
from unittest.mock import patch
from logging import DEBUG

import pytest
from requests.sessions import Session


class FakeGetCSRFTokenFunction:
	def __init__(self, token: Optional[str] = None):
		self.token = token

	def __call__(self, *args, **kwargs) -> Optional[str]:
		return self.token


class TestSyncAPI:
	def test___init__(self):
		session = Session()
		session.cookies.set(Cookie.SESSION_ID.value, "SESSIONID")
		session.cookies.set(Cookie.SESSION_ID2.value, "SESSIONID2")
		api = SyncAPI("CSRFTOKEN", session)
		assert api.reviews.csrf_token == api.csrf_token == "CSRFTOKEN"
		assert api.reviews.session is api.session is session

	def test_make_session(self):
		api = SyncAPI.build("", "", "")
		session = api.make_session("SESSION-ID", "SESSION-ID2")

		assert isinstance(session, Session)
		assert session.cookies.get(Cookie.SESSION_ID.value) == "SESSION-ID"
		assert session.cookies.get(Cookie.SESSION_ID2.value) == "SESSION-ID2"

	def test_build(self, caplog):
		with patch.object(SyncAPI, "make_session", wraps=SyncAPI.make_session) as make_session_method:
			api = SyncAPI.build("SESSION1", "SESSION2", "CSRFTOKEN")
			make_session_method.assert_called_once()
			assert api.csrf_token == "CSRFTOKEN"
			assert api.session.cookies.get(Cookie.SESSION_ID.value) == "SESSION1"
			assert api.session.cookies.get(Cookie.SESSION_ID2.value) == "SESSION2"

		caplog.set_level(DEBUG)

		with patch("ya_business_api.sync_api.SyncServiceAPI.get_csrf_token", FakeGetCSRFTokenFunction("TOKEN")):
			api = SyncAPI.build("SESSION1", "SESSION2")
			assert api.csrf_token == "TOKEN"
			assert api.session.cookies.get(Cookie.SESSION_ID.value) == "SESSION1"
			assert api.session.cookies.get(Cookie.SESSION_ID2.value) == "SESSION2"

			for record in caplog.records:
				assert record.levelname == "INFO"

			assert "CSRF token was not specified. Attempting to receive a token automatically..." in caplog.text

		with pytest.raises(
			CSRFTokenError,
			match=r"Failed to get CSRF token\. It is not possible to create a client instance"
		):
			with patch("ya_business_api.sync_api.SyncServiceAPI.get_csrf_token", FakeGetCSRFTokenFunction(None)):
				api = SyncAPI.build("SESSION1", "SESSION2")
