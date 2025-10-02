from ya_business_api.core.dataclass.base_phone import BasePhone
from ya_business_api.core.dataclass.base_url import BaseURL
from ya_business_api.core.dataclass.base_name import BaseName
from ya_business_api.core.dataclass.base_rubric import BaseRubric

from typing import List

from pydantic.main import BaseModel
from pydantic.fields import Field


class BaseChain(BaseModel):
	id: int
	permanent_id: int
	phones: List[BasePhone]
	urls: List[BaseURL]
	display_name: str = Field(validation_alias="displayName")
	names: List[BaseName]
	rubrics: List[BaseRubric]
