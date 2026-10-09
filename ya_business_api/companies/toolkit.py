from ya_business_api.core.generic.dict import get_from_deep

import json

from bs4 import BeautifulSoup


def parse_org_permanent_id(response_content: str) -> int:
	"""
	Parses current org permanent id from the "get_org_permanent_id" response content.
	"""
	bs = BeautifulSoup(response_content, "html.parser")
	raw_script_content = ""

	for element in bs.find_all("script"):
		if "window.__PRELOAD_DATA" in element.text:
			raw_script_content = element.text.strip()[24:-1]
			break
	else:
		raise RuntimeError("Required data was not found")

	script_content = json.loads(raw_script_content)

	if not isinstance(script_content, dict):
		raise RuntimeError("Unexpected data format")

	raw_permanent_id = get_from_deep(
		script_content,
		["initialState", "edit", "navigation", "company", "permanent_id"],
	)

	if isinstance(raw_permanent_id, int):
		return raw_permanent_id
	elif isinstance(raw_permanent_id, str) and raw_permanent_id.isdigit():
		return int(raw_permanent_id)

	raise RuntimeError("Unexpected data format")
