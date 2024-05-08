from dataclasses import dataclass
from typing import Optional


@dataclass
class CompaniesRequest:
	filter: Optional[str] = None
	page: Optional[int] = None

	def as_query_params(self) -> dict:
		result = {}

		if self.filter:
			result['filter'] = self.filter

		if self.page:
			result['page'] = self.page

		return result
