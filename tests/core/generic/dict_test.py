from ya_business_api.core.generic.dict import get_from_deep

import pytest


class TestGetFromDeep:
	def test_type_error(self):
		with pytest.raises(TypeError, match="Node is not a dictionary"):
			get_from_deep([], "A")		# type: ignore - for testing purposes

	def test_value_error(self):
		with pytest.raises(ValueError, match="Key \"B\" is missing"):
			get_from_deep({"A": {}}, "AB")

	def test_normal(self):
		assert get_from_deep({}, "") == {}
		assert get_from_deep({"A": {}}, "A") == {}
		assert get_from_deep({"A": {"B": 1, "C": 2}}, "AB") == 1
		assert get_from_deep({"A": {"B": 1, "C": 2}}, "AC") == 2
