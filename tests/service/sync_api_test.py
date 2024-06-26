from ya_business_api.service.sync_api import SyncServiceAPI

from json import dumps
from unittest.mock import patch

from requests.sessions import Session
from requests.models import Response


class TestSyncServiceAPI:
	def test_get_csrf_token(self):
		session = Session()
		api = SyncServiceAPI(session)
		response = Response()
		response.status_code = 200

		with patch.object(session, 'post', return_value=response) as session_post_method:
			result = api.get_csrf_token()
			assert result is None
			session_post_method.assert_called_once()

			response.status_code = 488
			response._content = dumps({}).encode()
			result = api.get_csrf_token()
			assert result is None

			response._content = dumps({api.CSRF_TOKEN_FIELD: "TOKEN"}).encode()
			result = api.get_csrf_token()
			assert result == "TOKEN"
