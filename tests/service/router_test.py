from ya_business_api.service.router import ServiceRouter


class TestServiceRouter:
	def test_get_csrf_token(self):
		router = ServiceRouter()
		assert router.csrf_token() == "https://yandex.ru/sprav/api/view/chain/0/list/"
