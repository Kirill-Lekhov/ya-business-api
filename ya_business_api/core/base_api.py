from ya_business_api.core.router import Router

from abc import ABC, abstractmethod


class BaseAPI(ABC):
	router: Router

	def __init__(self) -> None:
		self.router = self.make_router()

	@abstractmethod
	def make_router(self) -> Router: ...
