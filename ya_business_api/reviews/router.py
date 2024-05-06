from ya_business_api.core.router import Router
from ya_business_api.core.constants import BASE_URL


class ReviewsRouter(Router):
	permanent_id: int

	def __init__(self, permanent_id: int) -> None:
		self.permanent_id = permanent_id

	def reviews(self) -> str:
		return f"{BASE_URL}/api/{self.permanent_id}/reviews"

	def answer(self) -> str:
		return f"{BASE_URL}/api/ugcpub/business-answer"
