from ya_business_api.service.async_api import AsyncServiceAPI
from tests.aiohttp import Response, RequestContextManager

from json import dumps
from unittest.mock import patch

import pytest
from aiohttp.client import ClientSession


@pytest.mark.asyncio
class TestAsyncServiceAPI:
	async def test_get_csrf_token(self):
		session = ClientSession()
		api = AsyncServiceAPI(session)
		response = Response()
		request_context_manager = RequestContextManager(response)

		with patch.object(session, "post", return_value=request_context_manager) as session_post_method:
			result = await api.get_csrf_token()
			assert result is None
			session_post_method.assert_called_once()

			response.status = 488
			response.content = dumps({})
			result = await api.get_csrf_token()
			assert result is None

			response.content = dumps({api.CSRF_TOKEN_FIELD: "TOKEN"})
			result = await api.get_csrf_token()
			assert result == "TOKEN"
