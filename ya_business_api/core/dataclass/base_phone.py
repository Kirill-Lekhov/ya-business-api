from pydantic.main import BaseModel


class BasePhone(BaseModel):
	country_code: str
	region_code: str
	number: str
	type: str		# "phone"
	hide: bool
	formatted: str
