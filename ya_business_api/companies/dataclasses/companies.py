from ya_business_api.core.dataclasses import ValidatedMixin, DictMixin

from typing import List, Any, Tuple, Optional, Dict, Union
from dataclasses import dataclass


Number = Union[float, int]


def is_valid_number(n: Number) -> bool:
	return isinstance(n, int) or isinstance(n, float)


@dataclass
class LocalizedValue(ValidatedMixin, DictMixin):
	__slots__ = 'locale', 'value'

	locale: str		# 'en', 'ru'
	value: str


@dataclass
class Position(ValidatedMixin, DictMixin):
	__slots__ = 'coordinates', 'type'

	coordinates: Tuple[Number, Number]
	type: str		# "Point"

	def __post_init__(self) -> None:
		super().__post_init__()

		assert len(self.coordinates) == 2 and all(map(lambda x: is_valid_number(x), self.coordinates))

	@classmethod
	def from_dict(cls, d: dict) -> "Position":
		d['coordinates'] = tuple(d.get('coordinates', []))
		return super().from_dict(d)


@dataclass
class AddressComponent(ValidatedMixin, DictMixin):
	__slots__ = 'kind', 'name'

	kind: str		# 'country', 'province', 'area', 'locality', 'street', 'house'
	name: LocalizedValue

	@classmethod
	def from_dict(cls, d: dict) -> "AddressComponent":
		d['name'] = LocalizedValue.from_dict(d.get('name', {}))
		return super().from_dict(d)


@dataclass
class AddressEntrance(ValidatedMixin, DictMixin):
	__slots__ = 'normal_azimuth', 'pos', 'type'

	normal_azimuth: Number
	pos: Position
	type: str		# 'main'

	@classmethod
	def from_dict(cls, d: dict) -> "AddressEntrance":
		d['pos'] = Position.from_dict(d.get('pos', {}))
		return super().from_dict(d)


@dataclass
class AddressTranslation(ValidatedMixin, DictMixin):
	__slots__ = 'components', 'formatted'

	components: List[AddressComponent]
	formatted: LocalizedValue

	def __post_init__(self) -> None:
		super().__post_init__()

		assert all(map(lambda x: isinstance(x, AddressComponent), self.components))

	@classmethod
	def from_dict(cls, d: dict) -> "AddressTranslation":
		d['components'] = [AddressComponent.from_dict(i) for i in d.get('components', [])]
		d['formatted'] = LocalizedValue.from_dict(d.get('formatted', {}))
		return super().from_dict(d)


@dataclass
class Address(ValidatedMixin, DictMixin):
	__slots__ = (
		'address_id', 'bounding_box', 'components', 'entrances', 'formatted', 'geo_id', 'infos', 'is_auto', 'pos',
		'postal_code', 'precision', 'region_code', 'translations', 'translocal',
	)

	address_id: int
	bounding_box: List[Tuple[Number, Number]]
	components: List[AddressComponent]
	entrances: List[AddressEntrance]
	formatted: LocalizedValue
	geo_id: int
	infos: List[LocalizedValue]
	is_auto: bool
	pos: Position
	postal_code: str
	precision: str		# 'exact'
	region_code: str		# 'RU'
	translations: List[AddressTranslation]
	translocal: str

	def __post_init__(self) -> None:
		super().__post_init__()

		assert all(
			map(
				lambda x: isinstance(x, tuple) and len(x) == 2 and is_valid_number(x[0]) and is_valid_number(x[1]),
				self.bounding_box,
			)
		), "Bounding box must be list of Number tuples"
		assert all(map(lambda x: isinstance(x, AddressComponent), self.components)), \
			"Each component must be of AddressComponent type"
		assert all(map(lambda x: isinstance(x, AddressEntrance), self.entrances)), \
			"Each entrance must be of AddressEntrance type"
		assert all(map(lambda x: isinstance(x, LocalizedValue), self.infos)), \
			"Each info must be of LocalizedValue type"
		assert all(map(lambda x: isinstance(x, AddressTranslation), self.translations)), \
			"Each translation must be of AddressTranslation type"

	@classmethod
	def from_dict(cls, d: dict) -> "Address":
		d['bounding_box'] = [tuple(i) for i in d.get('bounding_box', [])]
		d['components'] = [AddressComponent.from_dict(i) for i in d.get('components', [])]
		d['entrances'] = [AddressEntrance.from_dict(i) for i in d.get('entrances', [])]
		d['formatted'] = LocalizedValue.from_dict(d.get('formatted', {}))
		d['infos'] = [LocalizedValue.from_dict(i) for i in d.get('infos', [])]
		d['pos'] = Position.from_dict(d.get('pos', {}))
		d['translations'] = [AddressTranslation.from_dict(i) for i in d.get('translations', [])]
		return super().from_dict(d)


@dataclass
class WorkInterval(ValidatedMixin, DictMixin):
	__slots__ = 'day', 'time_minutes_begin', 'time_minutes_end'

	day: str		# 'weekdays'
	time_minutes_begin: int
	time_minutes_end: int


@dataclass
class GeoCampaign(ValidatedMixin, DictMixin):
	__slots__ = 'hasActive', 'hasDraft'

	hasActive: bool
	hasDraft: bool


@dataclass
class Name(ValidatedMixin, DictMixin):
	__slots__ = 'type', 'value'

	type: str		# 'main'
	value: LocalizedValue

	@classmethod
	def from_dict(cls, d: dict) -> "Name":
		d['value'] = LocalizedValue.from_dict(d.get('value', {}))
		return super().from_dict(d)


@dataclass
class PanoramaDirection(ValidatedMixin, DictMixin):
	__slots__ = 'bearing', 'pitch'

	bearing: Number
	pitch: Number


@dataclass
class PanoramaSpan(ValidatedMixin, DictMixin):
	__slots__ = 'horizontal', 'vertical'

	horizontal: Number
	vertical: Number


@dataclass
class Panorama(ValidatedMixin, DictMixin):
	__slots__ = 'direction', 'id', 'pos', 'provider_id', 'span'

	direction: PanoramaDirection
	id: str
	pos: Position
	provider_id: int
	span: PanoramaSpan

	@classmethod
	def from_dict(cls, d: dict) -> "Panorama":
		d['direction'] = PanoramaDirection.from_dict(d.get('direction', {}))
		d['pos'] = Position.from_dict(d.get('pos', {}))
		d['span'] = PanoramaSpan.from_dict(d.get('span', {}))
		return super().from_dict(d)


@dataclass
class Phone(ValidatedMixin, DictMixin):
	__slots__ = 'country_code', 'formatted', 'hide', 'number', 'region_code', 'type'

	country_code: str
	formatted: str
	hide: bool
	number: str
	region_code: str
	type: str		# phone


@dataclass
class Rubric(ValidatedMixin, DictMixin):
	__slots__ = 'features', 'id', 'isMain', 'name'

	features: List[Any]		# ???
	id: int
	isMain: bool
	name: str


@dataclass
class ServiceProfile(ValidatedMixin, DictMixin):
	__slots__ = 'external_path', 'published', 'type'

	external_path: str
	published: bool
	type: str		# 'maps', 'serp'


@dataclass
class CompanyURL(ValidatedMixin, DictMixin):
	__slots__ = 'hide', 'type', 'value', 'social_login', 'social_network'

	hide: bool
	type: str		# 'main', 'social'
	value: str
	social_login: Optional[str]
	social_network: Optional[str]		# 'vkontakte'

	def __init__(
		self,
		hide: bool,
		type: str,
		value: str,
		social_login: Optional[str] = None,
		social_network: Optional[str] = None,
	):
		self.hide = hide
		self.type = type
		self.value = value
		self.social_login = social_login
		self.social_network = social_network
		self.__post_init__()


@dataclass
class CompanyLogo(ValidatedMixin, DictMixin):
	__slots__ = 'id', 'tags', 'time_published', 'url_template'

	id: str
	tags: List[str]
	time_published: int
	url_template: str

	def __post_init__(self) -> None:
		super().__post_init__()

		assert all(map(lambda x: isinstance(x, str), self.tags)), "All tags must be of string type"


@dataclass
class Company(ValidatedMixin, DictMixin):
	"""
	TODO:
		* Add __slots__.
	"""
	address: Address
	base_work_intervals: List[WorkInterval]
	displayName: str
	emails: List[str]
	feature_values: List[Any]		# ???
	fromGeosearch: bool
	geoCampaign: GeoCampaign
	has_owner: bool
	id: int
	is_online: bool
	is_top_rated: bool
	legal_info: dict		# ???
	nail: dict		# ???
	names: List[Name]
	noAccess: bool
	object_role: str		# 'owner'
	owner: int
	panorama: Panorama
	permanent_id: int
	phones: List[Phone]
	photos: List[Any]		# ???
	price_lists: List[Any]		# ???
	profile: dict		# ???
	publishing_status: str		# 'publish'
	rating: Number
	reviewsCount: int
	rubrics: List[Dict[str, Rubric]]
	scheduled_work_intervals: List[Any]		# ???
	service_area: dict		# ???
	service_profiles: List[ServiceProfile]
	tycoon_id: int
	type: str		# 'ordinal'
	urls: List[CompanyURL]
	user_has_ydo_account: bool
	work_intervals: List[WorkInterval]
	logo: Optional[CompanyLogo] = None

	def __post_init__(self):
		super().__post_init__()

		assert all(map(lambda x: isinstance(x, WorkInterval), self.base_work_intervals)), \
			"All base work intervals must be of WorkInterval type"
		assert all(map(lambda x: isinstance(x, str), self.emails)), "All emails must be of str type"
		assert all(map(lambda x: isinstance(x, Name), self.names)), "All names must be of Name type"
		assert all(map(lambda x: isinstance(x, Phone), self.phones)), "All phones must be of Phone type"
		assert all(map(lambda x: isinstance(x, ServiceProfile), self.service_profiles)), \
			"All service profiles must be of ServiceProfile type"
		assert all(map(lambda x: isinstance(x, CompanyURL), self.urls)), "All urls must be of CompanyURL type"
		assert all(map(lambda x: isinstance(x, WorkInterval), self.work_intervals)), \
			"All work intervals must be of WorkInterval type"

		for rubric in self.rubrics:
			assert isinstance(rubric, dict)
			assert all(map(lambda x: isinstance(x, str), rubric.keys()))
			assert all(map(lambda x: isinstance(x, Rubric), rubric.values()))

	@classmethod
	def from_dict(cls, d: dict) -> "Company":
		d['address'] = Address.from_dict(d.get('address', {}))
		d['base_work_intervals'] = [WorkInterval.from_dict(i) for i in d.get('base_work_intervals', [])]
		d['geoCampaign'] = GeoCampaign.from_dict(d.get('geoCampaign', {}))
		d['names'] = [Name.from_dict(i) for i in d.get('names', [])]
		d['panorama'] = Panorama.from_dict(d.get('panorama', {}))
		d['phones'] = [Phone.from_dict(i) for i in d.get('phones', [])]
		d['service_profiles'] = [ServiceProfile.from_dict(i) for i in d.get('service_profiles', [])]
		d['urls'] = [CompanyURL.from_dict(i) for i in d.get('urls', [])]
		d['work_intervals'] = [WorkInterval.from_dict(i) for i in d.get('work_intervals', [])]

		if logo := d.get('logo'):
			d['logo'] = CompanyLogo.from_dict(logo)

		rubrics = []

		for rubric in d.get('rubrics', []):
			for label, body in rubric.items():
				rubric[label] = Rubric.from_dict(body)

			rubrics.append(rubric)

		d['rubrics'] = rubrics

		return super().from_dict(d)


@dataclass
class CompaniesResponse(ValidatedMixin, DictMixin):
	__slots__ = 'list', 'listCompanies', 'page', 'total'

	limit: int
	listCompanies: List[Company]
	page: int
	total: int

	def __post_init__(self) -> None:
		super().__post_init__()

		assert all(map(lambda x: isinstance(x, Company), self.listCompanies))

	@classmethod
	def from_dict(cls, d: dict) -> "CompaniesResponse":
		d['listCompanies'] = [Company.from_dict(i) for i in d.get('listCompanies', [])]
		return super().from_dict(d)
