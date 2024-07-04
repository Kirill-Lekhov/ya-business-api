from typing import Tuple, List, Dict, Union, Optional, Any

from pydantic.main import BaseModel
from pydantic.fields import Field


Number = Union[float, int]


class LocalizedValue(BaseModel):
	locale: str
	value: str


class Position(BaseModel):
	coordinates: Tuple[Number, Number]
	type: str		# Point


class AddressComponent(BaseModel):
	kind: str		# country, province, area, locality, street, house
	name: LocalizedValue


class AddressEntrance(BaseModel):
	normal_azimuth: Number
	pos: Position
	type: str		# main


class AddressTranslation(BaseModel):
	components: List[AddressComponent]
	formatted: LocalizedValue


class Address(BaseModel):
	formatted: LocalizedValue
	geo_id: int
	is_auto: bool
	translocal: str
	is_manual_one_line: bool

	# Optional fields
	components: List[AddressComponent] = []
	bounding_box: List[Tuple[Number, Number]] = []
	entrances: List[AddressEntrance] = []
	infos: List[LocalizedValue] = []
	translations: List[AddressTranslation] = []
	address_id: Optional[int] = None
	postal_code: Optional[str] = None
	precision: Optional[str] = None			# exact
	region_code: Optional[str] = None		# RU
	pos: Optional[Position] = None


class WorkInterval(BaseModel):
	day: str		# weekdays
	time_minutes_begin: int
	time_minutes_end: int


class GeoCampaign(BaseModel):
	has_active: bool = Field(alias="hasActive")
	has_draft: bool = Field(alias="hasDraft")


class Name(BaseModel):
	type: str		# main, synonym
	value: LocalizedValue


class PanoramaDirection(BaseModel):
	bearing: Number
	pitch: Number


class PanoramaSpan(BaseModel):
	horizontal: Number
	vertical: Number


class Panorama(BaseModel):
	direction: PanoramaDirection
	id: str
	pos: Position
	provider_id: int
	span: PanoramaSpan


class Phone(BaseModel):
	country_code: str
	region_code: str
	number: str
	formatted: str
	hide: bool
	type: str				# phone

	# Optional fields
	check_status: Optional[str] = None		# checked


class Rubric(BaseModel):
	features: List[Any]		# ???
	id: int
	is_main: bool = Field(alias="isMain")
	name: str


class ServiceProfile(BaseModel):
	external_path: str
	published: bool
	type: str		# maps, serp


class CompanyURL(BaseModel):
	hide: bool
	type: str									# main, social
	value: str

	# Optional fields
	social_login: Optional[str] = None
	social_network: Optional[str] = None		# vkontakte


class CompanyLogoAuthor(BaseModel):
	uid: int


class CompanyLogo(BaseModel):
	id: str
	tags: List[str]		# logo
	time_published: int
	url_template: str

	# Optional fields
	author: Optional[CompanyLogoAuthor] = None


class Chain(BaseModel):
	id: int
	permanent_id: int
	phones: List[Phone]
	urls: List[CompanyURL]
	display_name: str = Field(alias="displayName")
	names: List[Name]
	rubrics: List[Dict[str, Rubric]]
	brand_count: int = Field(alias="brandCount")


class Company(BaseModel):
	id: int
	tycoon_id: int
	permanent_id: int

	address: Address
	base_work_intervals: List[WorkInterval]
	display_name: str = Field(alias="displayName")
	emails: List[str]
	feature_values: List[Any]					# ???
	geo_campaign: GeoCampaign = Field(alias="geoCampaign")
	has_owner: bool
	is_top_rated: Optional[bool]
	legal_info: dict							# ???
	nail: dict									# ???
	names: List[Name]
	no_access: bool = Field(alias="noAccess")
	object_role: str							# owner, delegate
	phones: List[Phone]
	photos: List[Any]							# ???
	price_lists: List[Any]						# ???
	profile: dict								# ???
	publishing_status: str						# publish
	rubrics: List[Dict[str, Rubric]]
	scheduled_work_intervals: List[Any]			# ???
	service_area: dict		# ???
	type: str									# ordinal, chain
	urls: List[CompanyURL]
	user_has_ydo_account: bool
	work_intervals: List[WorkInterval]

	# Optional fields
	diffs: Dict[str, int] = {}
	service_profiles: List[ServiceProfile] = []
	logo: Optional[CompanyLogo] = None
	from_geosearch: Optional[bool] = Field(None, alias="fromGeosearch")
	is_online: Optional[bool] = None
	owner: Optional[int] = None
	panorama: Optional[Panorama] = None
	rating: Optional[Number] = None
	reviews_count: Optional[int] = Field(None, alias="reviewsCount")


class CompaniesResponse(BaseModel):
	limit: int
	list_companies: List[Company] = Field(alias="listCompanies")
	page: int
	total: int
