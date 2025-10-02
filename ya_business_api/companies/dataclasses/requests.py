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


class ChainBranchesRequest(BaseModel):
	tycoon_id: int

	page: Optional[int] = None

	def as_query_params(self) -> dict:
		return self.model_dump(include={"page"}, exclude_none=True)
