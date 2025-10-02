from typing import List

from pydantic.main import BaseModel


class BaseLogo(BaseModel):
	id: str
	tags: List[str]
	url_template: str
	time_published: int
