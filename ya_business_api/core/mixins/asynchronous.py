from aiohttp.client import ClientSession


class AsyncAPIMixin:
	session: ClientSession

	def __init__(self, session: ClientSession, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		self.session = session
