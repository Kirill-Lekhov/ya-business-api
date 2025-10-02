from typing import List, Any

from pydantic.main import BaseModel
from pydantic.fields import Field


class RubricRubric(BaseModel):
	id: int
	is_main: bool = Field(validation_alias="isMain")
	name: str
	features: List[Any]		# UNKNOWN


class BaseRubric(BaseModel):
	rubric: RubricRubric
