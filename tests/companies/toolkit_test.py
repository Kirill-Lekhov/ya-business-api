from ya_business_api.companies.toolkit import parse_org_permanent_id

from typing import Final

import pytest


CONTENT_INVALID_PERMANENT_ID: Final[str] = """\
<script>
	window.__PRELOAD_DATA = {
		"initialState": {
			"edit": {
				"navigation": {
					"company": {
						"permanent_id": []
					}
				}
			}
		}
	};
</script>
"""
CONTENT_NORMAL_PERMANENT_ID_INT: Final[str] = """\
<script>
	window.__PRELOAD_DATA = {
		"initialState": {
			"edit": {
				"navigation": {
					"company": {
						"permanent_id": 512
					}
				}
			}
		}
	};
</script>
"""
CONTENT_NORMAL_PERMANENT_ID_STR: Final[str] = """\
<script>
	window.__PRELOAD_DATA = {
		"initialState": {
			"edit": {
				"navigation": {
					"company": {
						"permanent_id": "512"
					}
				}
			}
		}
	};
</script>
"""


class TestParseOrgPermanentId:
	def test_nodata_error(self):
		with pytest.raises(RuntimeError, match="Required data was not found"):
			parse_org_permanent_id("")

	def test_unexpected_data_format_error(self):
		with pytest.raises(RuntimeError, match="Unexpected data format"):
			parse_org_permanent_id("<script>window.__PRELOAD_DATA = [];</script>")

		with pytest.raises(RuntimeError, match="Unexpected data format"):
			parse_org_permanent_id(CONTENT_INVALID_PERMANENT_ID)

	def test_normal_permanent_id_int(self):
		assert parse_org_permanent_id(CONTENT_NORMAL_PERMANENT_ID_INT) == 512

	def test_normal_permanent_id_str(self):
		assert parse_org_permanent_id(CONTENT_NORMAL_PERMANENT_ID_STR) == 512
