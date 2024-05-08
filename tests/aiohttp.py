from typing import Any
from json import loads


class Response:
	status: int
	content: str

	def __init__(self, status: int = 200, content: str = "") -> None:
		self.status = status
		self.content = content

	async def json(self) -> Any:
		return loads(self.content)

	async def text(self) -> str:
		return self.content


class RequestContextManager:
	def __init__(self, response: Response) -> None:
		self.response = response

	async def __aenter__(self, *args, **kwargs):
		return self.response

	async def __aexit__(self, *args, **kwargs):
		pass
