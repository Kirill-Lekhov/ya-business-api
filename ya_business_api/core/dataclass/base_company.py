from ya_business_api.core.dataclass.base_phone import BasePhone
from ya_business_api.core.dataclass.base_logo import BaseLogo
from ya_business_api.core.dataclass.base_rubric import BaseRubric
from ya_business_api.core.dataclass.base_chain import BaseChain
from ya_business_api.core.dataclass.base_url import BaseURL
from ya_business_api.core.dataclass.base_name import BaseName
from ya_business_api.core.dataclass.base_pos import BasePos

from typing import List, Any, Optional, Tuple

from pydantic.main import BaseModel
from pydantic.fields import Field


class Formatted(BaseModel):
	value: str
	locale: str		# "ru", "en"


class ComponentName(BaseModel):
	value: str
	locale: str		# "ru", "en"


class Component(BaseModel):
	kind: str		# "country", "province", "locality", "street", "house"
	name: ComponentName


class AddressEntrance(BaseModel):
	pos: BasePos
	type: str		# "other"
	normal_azimuth: Optional[float] = None


class AddressTranslation(BaseModel):
	formatted: Formatted
	components: List[Component]
	is_manual: bool


class Address(BaseModel):
	geo_id: int
	formatted: Formatted
	is_auto: bool
	translocal: str
	is_manual_one_line: bool

	# Optional fields
	region_code: Optional[str] = None		# "RU"
	pos: Optional[BasePos] = None
	bounding_box: List[Tuple[float, float]] = Field(default_factory=list)
	precision: Optional[str] = None		# exact
	components: List[Component] = Field(default_factory=list)
	postal_code: Optional[str] = None
	infos: List[Any] = Field(default_factory=list)		# UNKNOWN
	entrances: List[AddressEntrance] = Field(default_factory=list)
	translations: List[AddressTranslation] = Field(default_factory=list)
	info_components: List[Any] = Field(default_factory=list)
	address_id: Optional[int] = None
	building_id: Optional[int] = None


class WorkInterval(BaseModel):
	day: Optional[str] = None		# "everyday"
	time_minutes_begin: Optional[int] = None
	time_minutes_end: Optional[int] = None
	iso_date: Optional[str] = None
	is_holiday: Optional[bool] = None


class BaseCompany(BaseModel):
	id: int
	permanent_id: int

	publishing_status: str		# "publish"
	type: str		# "ordinal", "chain"
	display_name: str = Field(alias="displayName")
	has_owner: bool
	no_access: bool = Field(alias="noAccess")

	work_intervals: List[WorkInterval]
	base_work_intervals: List[WorkInterval]
	names: List[BaseName]
	emails: List[str]
	phones: List[BasePhone]
	urls: List[BaseURL]
	rubrics: List[BaseRubric]

	address: Address

	profile: dict		# UNKNOWN
	nail: dict		# UNKNOWN
	legal_info: dict		# UNKNOWN
	service_area: dict		# UNKNOWN
	feature_values: List[Any]		# UNKNOWN
	scheduled_work_intervals: List[Any]		# UNKNOWN
	price_lists: List[Any]		# UNKNOWN
	photos: List[Any]		# UNKNOWN

	is_online: Optional[bool] = None
	not_for_search: Optional[bool] = None
	owner: Optional[int] = None
	rating: Optional[float] = None
	reviews_count: Optional[int] = Field(default=None, validation_alias="reviewsCount")
	from_geosearch: Optional[bool] = Field(default=None, validation_alias="fromGeosearch")
	logo: Optional[BaseLogo] = None
	chain: Optional[BaseChain] = None
