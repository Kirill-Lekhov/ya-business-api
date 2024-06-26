from typing import Optional

from pydantic import BaseModel


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
