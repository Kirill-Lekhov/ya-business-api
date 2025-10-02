from pydantic.main import BaseModel


class NameValue(BaseModel):
	value: str
	locale: str		# "ru", "en"


class BaseName(BaseModel):
	value: NameValue
	type: str		# "main", "synonym"
