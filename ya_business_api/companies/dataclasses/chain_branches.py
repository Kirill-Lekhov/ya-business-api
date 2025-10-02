from ya_business_api.core.dataclass.base_chain import BaseChain
from ya_business_api.core.dataclass.base_company import BaseCompany
from ya_business_api.core.dataclass.base_pos import BasePos

from typing import List, Optional

from pydantic.main import BaseModel
from pydantic.fields import Field


class Pager(BaseModel):
	offset: int
	limit: int
	total: int


class Diffs(BaseModel):
	reviews: int
	photos: Optional[bool] = None


class GeoCampaign(BaseModel):
	has_active: bool = Field(validation_alias="hasActive")
	has_draft: bool = Field(validation_alias="hasDraft")


class PanoramaDirection(BaseModel):
	bearing: float
	pitch: float


class PanoramaSpan(BaseModel):
	horizontal: float
	vertical: float


class Panorama(BaseModel):
	id: str
	direction: PanoramaDirection
	span: PanoramaSpan
	pos: BasePos
	provider_id: int


class ServiceProfile(BaseModel):
	type: str		# "maps"
	external_path: str
	published: bool


class Company(BaseCompany):
	service_profiles: List[ServiceProfile]
	geo_campaign: GeoCampaign = Field(validation_alias="geoCampaign")

	# Optional fields
	diffs: Optional[Diffs] = None
	panorama: Optional[Panorama] = None


class ChainData(BaseModel):
	pager: Pager
	companies: List[Company]

	# Optional fields
	chain: Optional[BaseChain] = None


class ChainBranchesResponse(BaseModel):
	chain_data: ChainData = Field(validation_alias="companyList")
	company_ids: List[int] = Field(validation_alias="companyIds")
