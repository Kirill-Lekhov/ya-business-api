from ya_business_api.companies.dataclasses.companies import (
	LocalizedValue, Position, AddressComponent, AddressEntrance, AddressTranslation, Address, WorkInterval, GeoCampaign,
	Name, PanoramaDirection, PanoramaSpan, Panorama, Phone, Rubric, ServiceProfile, CompanyURL, CompanyLogo, Company,
	CompaniesResponse,
)


def make_localized_value() -> dict:
	return {'locale': 'ru', 'value': 'Российская Федерация'}


def make_position() -> dict:
	return {
		"coordinates": [0.15, 0.11],
		"type": "Point",
	}


def make_address_component() -> dict:
	return {
		'kind': 'country',
		'name': make_localized_value(),
	}


def make_address_entrance() -> dict:
	return {
		"normal_azimuth": 8.0123456789,
		"pos": make_position(),
		"type": "main",
	}


def make_address_translation() -> dict:
	return {
		"components": [make_address_component(), make_address_component()],
		"formatted": make_localized_value(),
	}


def make_address() -> dict:
	return {
		"address_id": 117755,
		"bounding_box": [[11, 0.13], [0.13, 11]],
		"components": [make_address_component(), make_address_component()],
		"entrances": [make_address_entrance(), make_address_entrance()],
		"formatted": make_localized_value(),
		"geo_id": 2340987234,
		"infos": [make_localized_value(), make_localized_value()],
		"is_auto": False,
		"pos": make_position(),
		"postal_code": '000000',
		"precision": 'exact',
		"region_code": 'RU',
		"translations": [make_address_translation()],
		"translocal": "Адрес",
		"is_manual_one_line": False,
	}


def make_work_interval() -> dict:
	return {
		"day": "weekdays",
		"time_minutes_begin": 0,
		"time_minutes_end": 1200,
	}


def make_geo_campaign() -> dict:
	return {
		"hasActive": True,
		"hasDraft": False,
	}


def make_name() -> dict:
	return {
		"type": "main",
		"value": make_localized_value(),
	}


def make_panorama_direction() -> dict:
	return {
		"bearing": 11.44,
		"pitch": 44,
	}


def make_panorama_span() -> dict:
	return {
		"horizontal": 12,
		"vertical": 0.12,
	}


def make_panorama() -> dict:
	return {
		"direction": make_panorama_direction(),
		"id": "identifier",
		"pos": make_position(),
		"provider_id": 112233,
		"span": make_panorama_span(),
	}


def make_phone() -> dict:
	return {
		"country_code": "7",
		"formatted": "+7 (8412) 38-58-78",
		"hide": True,
		"number": "385878",
		"region_code": "8412",
		"type": "phone",
	}


def make_rubric() -> dict:
	return {
		"features": [],
		"id": 123,
		"isMain": True,
		"name": "Rubric",
	}


def make_service_profile() -> dict:
	return {
		"external_path": "/maps/org/67123879",
		"published": True,
		"type": 'maps',
	}


def make_company_url() -> dict:
	return {
		"hide": False,
		"type": 'main',
		"value": "https://ya.ru",
	}


def make_company_logo() -> dict:
	return {
		"id": "identifier",
		"tags": ["tag1", "tag2"],
		"time_published": 1715159227,
		"url_template": "https://avatars.mds.yandex.net/get-altay/.../.../%s",
	}


def make_company() -> dict:
	return {
		"address": make_address(),
		"base_work_intervals": [make_work_interval(), make_work_interval()],
		"displayName": "Display Name",
		"emails": ["email1@example.com", "email2@example.com"],
		"feature_values": [],
		"fromGeosearch": True,
		"geoCampaign": make_geo_campaign(),
		"has_owner": True,
		"id": 112233,
		"is_online": True,
		"is_top_rated": True,
		"legal_info": {},
		"nail": {},
		"names": [make_name(), make_name()],
		"noAccess": True,
		"object_role": 'owner',
		"owner": 67237823487,
		"panorama": make_panorama(),
		"permanent_id": 136215736112,
		"phones": [make_phone(), make_phone()],
		"photos": [],
		"price_lists": [],
		"profile": {},
		"publishing_status": "publish",
		"rating": 4.99,
		"reviewsCount": 999,
		"rubrics": [{'Rubric': make_rubric()}, {'Rubric': make_rubric()}],
		"scheduled_work_intervals": [],
		"service_area": {},
		"service_profiles": [make_service_profile(), make_service_profile()],
		"tycoon_id": 112233,
		"type": "ordinal",
		"urls": [make_company_url(), make_company_url()],
		"user_has_ydo_account": False,
		"work_intervals": [make_work_interval(), make_work_interval()],
		"logo": None,
	}


def make_companies_response() -> dict:
	return {
		"limit": 10,
		"listCompanies": [make_company(), make_company()],
		"page": 1,
		"total": 100,
	}


class TestLocalizedValue:
	def test_validation(self):
		localized_value = LocalizedValue(**make_localized_value())
		assert isinstance(localized_value, LocalizedValue)
		assert localized_value.locale == "ru"
		assert localized_value.value == "Российская Федерация"


class TestPosition:
	def test_validation(self):
		position = Position(**make_position())
		assert isinstance(position, Position)
		assert position.coordinates == (0.15, 0.11)
		assert position.type == "Point"


class TestAddressComponent:
	def test_validation(self):
		component = AddressComponent(**make_address_component())
		assert isinstance(component, AddressComponent)
		assert component.kind == 'country'
		assert isinstance(component.name, LocalizedValue)
		assert component.name.locale == 'ru'
		assert component.name.value == 'Российская Федерация'


class TestAddressEntrance:
	def test_validation(self):
		entrance = AddressEntrance(**make_address_entrance())

		assert isinstance(entrance, AddressEntrance)
		assert entrance.normal_azimuth == 8.0123456789
		assert isinstance(entrance.pos, Position)
		assert entrance.pos.coordinates == (0.15, 0.11)
		assert entrance.pos.type == "Point"
		assert entrance.type == "main"


class TestAddressTranslation:
	def test_validation(self):
		translation = AddressTranslation(**make_address_translation())
		assert isinstance(translation, AddressTranslation)
		assert isinstance(translation.components, list)
		assert len(translation.components) == 2
		assert isinstance(translation.components[0], AddressComponent)
		assert isinstance(translation.components[1], AddressComponent)
		assert isinstance(translation.formatted, LocalizedValue)
		assert translation.formatted.locale == "ru"
		assert translation.formatted.value == "Российская Федерация"


class TestAddress:
	def test_validation(self):
		address = Address(**make_address())
		assert address.address_id == 117755
		assert len(address.bounding_box) == 2
		assert len(address.components) == 2
		assert len(address.entrances) == 2
		assert isinstance(address.formatted, LocalizedValue)
		assert address.geo_id == 2340987234
		assert len(address.infos) == 2
		assert not address.is_auto
		assert isinstance(address.pos, Position)
		assert address.postal_code == "000000"
		assert address.precision == "exact"
		assert address.region_code == "RU"
		assert len(address.translations) == 1
		assert address.translocal == "Адрес"


class TestWorkInterval:
	def test_validation(self):
		work_interval = WorkInterval(**make_work_interval())
		assert isinstance(work_interval, WorkInterval)
		assert work_interval.day == "weekdays"
		assert work_interval.time_minutes_begin == 0
		assert work_interval.time_minutes_end == 1200


class TestGeoCampaign:
	def test_validation(self):
		geo_campaign = GeoCampaign(**make_geo_campaign())
		assert isinstance(geo_campaign, GeoCampaign)
		assert geo_campaign.hasActive
		assert not geo_campaign.hasDraft


class TestName:
	def test_validation(self):
		name = Name(**make_name())
		assert isinstance(name, Name)
		assert name.type == 'main'
		assert isinstance(name.value, LocalizedValue)


class TestPanoramaDirection:
	def test_validation(self):
		direction = PanoramaDirection(**make_panorama_direction())
		assert isinstance(direction, PanoramaDirection)
		assert direction.bearing == 11.44
		assert direction.pitch == 44


class TestPanoramaSpan:
	def test_validation(self):
		span = PanoramaSpan(**make_panorama_span())
		assert isinstance(span, PanoramaSpan)
		assert span.horizontal == 12
		assert span.vertical == 0.12


class TestPanorama:
	def test_validation(self):
		panorama = Panorama(**make_panorama())
		assert isinstance(panorama, Panorama)
		assert isinstance(panorama.direction, PanoramaDirection)
		assert panorama.id == "identifier"
		assert isinstance(panorama.pos, Position)
		assert panorama.provider_id == 112233
		assert isinstance(panorama.span, PanoramaSpan)


class TestPhone:
	def test_validation(self):
		phone = Phone(**make_phone())
		assert isinstance(phone, Phone)
		assert phone.country_code == "7"
		assert phone.formatted == "+7 (8412) 38-58-78"
		assert phone.hide
		assert phone.number == "385878"
		assert phone.region_code == "8412"
		assert phone.type == "phone"


class TestRubric:
	def test_validation(self):
		rubric = Rubric(**make_rubric())
		assert isinstance(rubric, Rubric)
		assert rubric.features == []
		assert rubric.id == 123
		assert rubric.isMain
		assert rubric.name == "Rubric"


class TestServiceProfile:
	def test_validation(self):
		service_profile = ServiceProfile(**make_service_profile())
		assert isinstance(service_profile, ServiceProfile)
		assert service_profile.external_path == "/maps/org/67123879"
		assert service_profile.published
		assert service_profile.type == "maps"


class TestCompanyURL:
	def test_validation(self):
		company_url = CompanyURL(**make_company_url())
		assert isinstance(company_url, CompanyURL)
		assert not company_url.hide
		assert company_url.type == "main"
		assert company_url.value == "https://ya.ru"
		assert company_url.social_login is None
		assert company_url.social_network is None

		url_data = make_company_url()
		url_data['social_login'] = "ya"
		url_data['social_network'] = "vkontakte"
		company_url = CompanyURL(**url_data)
		assert company_url.social_login == "ya"
		assert company_url.social_network == "vkontakte"


class TestCompanyLogo:
	def test_validation(self):
		company_logo = CompanyLogo(**make_company_logo())
		assert isinstance(company_logo, CompanyLogo)
		assert company_logo.id == "identifier"
		assert company_logo.tags == ["tag1", "tag2"]
		assert company_logo.time_published == 1715159227
		assert company_logo.url_template == "https://avatars.mds.yandex.net/get-altay/.../.../%s"


class TestCompany:
	def test_validation(self):
		company = Company(**make_company())
		assert isinstance(company, Company)
		assert isinstance(company.address, Address)
		assert len(company.base_work_intervals) == 2
		assert company.displayName == "Display Name"
		assert company.emails == ["email1@example.com", "email2@example.com"]
		assert company.feature_values == []
		assert company.fromGeosearch
		assert isinstance(company.geoCampaign, GeoCampaign)
		assert company.has_owner
		assert company.id == 112233
		assert company.is_online
		assert company.is_top_rated
		assert company.legal_info == {}
		assert company.nail == {}
		assert len(company.names) == 2
		assert company.noAccess
		assert company.object_role == "owner"
		assert company.owner == 67237823487
		assert isinstance(company.panorama, Panorama)
		assert company.permanent_id == 136215736112
		assert len(company.phones) == 2
		assert company.photos == []
		assert company.price_lists == []
		assert company.profile == {}
		assert company.publishing_status == "publish"
		assert company.rating == 4.99
		assert company.reviewsCount == 999
		assert len(company.rubrics) == 2
		assert {tuple(i.keys())[0] for i in company.rubrics} == {'Rubric'}
		assert company.scheduled_work_intervals == []
		assert company.service_area == {}
		assert len(company.service_profiles) == 2
		assert company.tycoon_id == 112233
		assert company.type == "ordinal"
		assert len(company.urls) == 2
		assert not company.user_has_ydo_account
		assert len(company.work_intervals) == 2
		assert company.logo is None

		data = make_company()
		data['logo'] = make_company_logo()
		company = Company(**data)
		assert isinstance(company.logo, CompanyLogo)


class TestCompaniesResponse:
	def test_validation(self):
		response = CompaniesResponse(**make_companies_response())
		assert response.limit == 10
		assert len(response.listCompanies) == 2
		assert response.page == 1
		assert response.total == 100
