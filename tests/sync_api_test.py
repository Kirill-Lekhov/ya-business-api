from ya_business_api.sync_api import SyncAPI
from ya_business_api.core.constants import Cookie

from unittest.mock import patch

from requests.sessions import Session


class TestSyncAPI:
	def test___init__(self):
		session = Session()
		session.cookies.set(Cookie.SESSION_ID.value, "SESSIONID")
		session.cookies.set(Cookie.SESSION_ID2.value, "SESSIONID2")
		api = SyncAPI(1212, "CSRFTOKEN", session)
		assert api.reviews.permanent_id == api.permanent_id == 1212
		assert api.reviews.csrf_token == api.csrf_token == "CSRFTOKEN"
		assert api.reviews.session is api.session is session

	def test_make_session(self):
		api = SyncAPI.build(1, "", "", "")
		session = api.make_session("SESSION-ID", "SESSION-ID2")

		assert isinstance(session, Session)
		assert session.cookies.get(Cookie.SESSION_ID.value) == "SESSION-ID"
		assert session.cookies.get(Cookie.SESSION_ID2.value) == "SESSION-ID2"

	def test_build(self):
		with patch.object(SyncAPI, "make_session", wraps=SyncAPI.make_session) as make_session_method:
			api = SyncAPI.build(1212, "CSRFTOKEN", "SESSION1", "SESSION2")
			make_session_method.assert_called_once()
			assert api.permanent_id == 1212
			assert api.csrf_token == "CSRFTOKEN"
			assert api.session.cookies.get(Cookie.SESSION_ID.value) == "SESSION1"
			assert api.session.cookies.get(Cookie.SESSION_ID2.value) == "SESSION2"
