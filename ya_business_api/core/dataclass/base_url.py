from pydantic.main import BaseModel


class BaseURL(BaseModel):
	hide: bool
	type: str		# "main", "social"
	value: str
