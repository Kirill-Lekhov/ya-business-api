from typing import Optional

from pydantic.main import BaseModel


class CompaniesRequest(BaseModel):
	filter: Optional[str] = None
	page: Optional[int] = None

	def as_query_params(self) -> dict:
		result = {}

		if self.filter:
			result['filter'] = self.filter

		if self.page:
			result['page'] = self.page

		return result


class ChainListRequest(BaseModel):
	tycoon_id: int
	geo_id: Optional[int] = None
	page: Optional[int] = None

	def as_query_params(self) -> dict:
		result = {}

		if self.geo_id:
			result['geo_id'] = self.geo_id

		if self.page:
			result['page'] = self.page

		return result
