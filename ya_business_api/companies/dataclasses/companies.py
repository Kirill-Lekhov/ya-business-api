from ya_business_api.core.dataclass.base_company import BaseCompany

from typing import List, Optional

from pydantic.main import BaseModel
from pydantic.fields import Field


class Diffs(BaseModel):
	total: int


class Company(BaseCompany):
	tycoon_id: int
	object_role: str		# "delegate"
	diffs: Optional[Diffs] = None


class CompaniesResponse(BaseModel):
	limit: int
	list_companies: List[Company] = Field(alias="listCompanies")
	page: int
	total: int
