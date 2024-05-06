from ya_business_api.core.base_api import BaseAPI
from ya_business_api.core.router import Router

from unittest.mock import patch


class DummyRouter(Router):
	pass


class DummyAPI(BaseAPI):
	def make_router(self) -> DummyRouter:
		return DummyRouter()


class TestAPI:
	def test___init__(self):
		with patch.object(DummyAPI, 'make_router') as make_router_method:
			api = DummyAPI()
			make_router_method.assert_called_once()
			assert api.router is make_router_method.return_value
