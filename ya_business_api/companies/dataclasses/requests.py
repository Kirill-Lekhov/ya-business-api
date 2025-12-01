from typing import Optional

from pydantic.main import BaseModel
from pydantic.fields import Field


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


class ChainBranchesRequest(BaseModel):
	tycoon_id: int

	# Query params
	permanent_id: int = Field(serialization_alias="chainPermalink")
	geo_id: int = Field(serialization_alias="geoId")

	page: Optional[int] = None

	def as_query_params(self) -> dict:
		return self.model_dump(include={"page", "permanent_id", "geo_id"}, exclude_none=True, by_alias=True)
