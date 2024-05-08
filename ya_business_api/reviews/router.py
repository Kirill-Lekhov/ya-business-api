from ya_business_api.core.router import Router
from ya_business_api.core.constants import BASE_URL


class ReviewsRouter(Router):
	def reviews(self, permanent_id: int) -> str:
		return f"{BASE_URL}/api/{permanent_id}/reviews"

	def answer(self) -> str:
		return f"{BASE_URL}/api/ugcpub/business-answer"
