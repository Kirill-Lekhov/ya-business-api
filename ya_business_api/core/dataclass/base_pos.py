from typing import Tuple

from pydantic.main import BaseModel


class BasePos(BaseModel):
	type: str		# "Point"
	coordinates: Tuple[float, float]
