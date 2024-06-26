from ya_business_api.service.base_api import BaseServiceAPI
from ya_business_api.service.router import ServiceRouter


class TestBaseAPI:
	def test_make_router(self):
		api = BaseServiceAPI()
		assert isinstance(api.make_router(), ServiceRouter)
