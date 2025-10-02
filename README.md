# Yandex business (sprav) API client [![codecov](https://codecov.io/gh/Kirill-Lekhov/ya-business-api/graph/badge.svg?token=9Q77PG68W1)](https://codecov.io/gh/Kirill-Lekhov/ya-business-api)

## Installation
```sh
# Sync only mode
pip install ya_business_api[sync]
# Async only mode
pip install ya_business_api[async]
# All modes
pip install ya_business_api[all]
```

## Instantiating
There are several ways to work with the API (synchronous and asynchronous).
Both interfaces have the same signatures, the only difference is the need to use async/await keywords.

```python
from ya_business_api.sync_api import SyncAPI		# Sync mode
from ya_business_api.async_api import AsyncAPI		# Async mode


def main() -> None:
	api = SyncAPI.build(
		session_id=...,
		session_id2=...,
		csrf_token=...,		# Optional
	)

	# Do things here...


async def main() -> None:
	api = await AsyncAPI.build(
		session_id=...,
		session_id2=...,
		csrf_token=...,		# Optional
	)

	# Do things here...

	await api.session.close()
```

### Where can I get the data for the client?
On the reviews page (https://yandex.ru/sprav/.../edit/reviews), open the developer console (usually `F12`) from the first request, copy values of cookies (`Session_id` and `sessionid2`).

In the console, run the following script:
```JS
function getData() {
	console.info({
		"CSRFToken": window?.__PRELOAD_DATA?.initialState?.env?.csrf,
		"PermanentId": window?.__PRELOAD_DATA?.initialState?.edit?.company?.permanent_id,
	})
}

getData()

/**
 * {CSRFToken: "...", PermanentId: 00000000000}
*/
```

### ⚠️WARNING⚠️
1. The `PermanentId` belong to certain companies and cannot be used to respond to reviews from another company.
2. The `CSRFToken` can be fetched automatically if it is not explicitly specified when calling the build method.

## Reviews
### Reviews fetching
* Async mode support: ✅;
* Validation disabling: ✅.
```python
# Sync mode
from ya_business_api.sync_api import SyncAPI
from ya_business_api.reviews.dataclasses.requests import ReviewsRequest


api = SyncAPI.build(...)
# Requesting unread reviews only
request = ReviewsRequest(
	permanent_id=<permanent_id>,
	unread=True,
	ranking=Ranking.BY_RATING_DESC,			# Optional
	continue_token="CONTINUE_TOKEN",		# Optional
)
# Requesting all reviews
request = ReviewsRequest(
	permanent_id=<permanent_id>,
	page=9999,								# Optional
	ranking=Ranking.BY_RATING_DESC,			# Optional
)
response = api.reviews.get_reviews(
	request,
	raw=False,		# Optional
)
```

### Answering to reviews
* Async mode support: ✅;
* Validation disabling: ❌.
```python
from ya_business_api.sync_api import SyncAPI
from ya_business_api.reviews.dataclasses.requests import AnswerRequest


api = SyncAPI.build(...)
reviews = api.reviews.get_reviews()
# Legacy
request = AnswerRequest(
	review_id=reviews.list.items[0].id,
	text="Thank you!",
	reviews_csrf_token=reviews.list.csrf_token,
	answer_csrf_token=reviews.list.items[0].business_answer_csrf_token,
)
# New
request = AnswerRequest(
	review_id=reviews.list.items[0].id,
	text="Thank you!",
	reviews_csrf_token="",
)
response = api.reviews.send_answer(request)
```

## Companies
### Receiving companies
* Async mode support: ✅;
* Validation disabling: ✅.
```python
from ya_business_api.sync_api import SyncAPI
from ya_business_api.companies.dataclasses.requests import CompaniesRequest


api = SyncAPI.build(...)
request = CompaniesRequest(filter="My Company", page=5)
response = api.companies.get_companies(
	request,		# Optional
	raw=False,		# Optional
)
```

### Receiving company chain branches
Some companies have several branches, in such cases the company will have the "chain" type.
This method will allow you to get a list of all branches.

* Async mode support: ✅;
* Validation disabling: ✅.
```python
from ya_business_api.sync_api import SyncAPI
from ya_business_api.companies.dataclasses.requests import ChainBranchesRequest


api = SyncAPI.build(...)
request = ChainListRequest(
	tycoon_id=<tycoon_id>,		# Note: Some API endpoints returns companies without `tycoon_id`.
	page=1,						# Optional
)
response = api.companies.get_chain_branches(
	request,
	raw=False,		# Optional
)
```

## Service
### Receiving CSRF token
* Async mode support: ✅;
* Validation disabling: ❌.
```python
from ya_business_api.sync_api import SyncAPI


api = SyncAPI.build(...)
csrf_token = api.service.get_csrf_token()
```

## Shortcuts
### Answers deleting
```python
api.reviews.send_answer(AnswerRequest(text="", ...))
```

### Automatic closing of the session (async mode)
```python
async with await AsyncAPI.make_session(session_id=..., session_id2=...) as session:
	api = AsyncAPI(permanent_id=..., csrf_token=..., session=session)
	...
```

## Examples
### Receiving all unread reviews from all companies
```python
from ya_business_api.async_api import AsyncAPI
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainBranchesRequest
from ya_business_api.reviews.dataclasses.requests import ReviewsRequest
from ya_business_api.reviews.dataclasses.reviews import Review
from ya_business_api.core.dataclass.base_company import BaseCompany

from asyncio import run
from os import getenv
from typing import AsyncGenerator
from logging import basicConfig, DEBUG


async def get_companies(api: AsyncAPI) -> AsyncGenerator[BaseCompany, None]:
	page = 1
	companies_response = await api.companies.get_companies()

	while companies_response.list_companies:
		for company in companies_response.list_companies:
			if company.type == "ordinal":
				yield company
			elif company.type == "chain":
				async for branch in get_ordinal_branches(api, company.tycoon_id):
					yield branch
			else:
				print(f"Company {company.permanent_id} with unknown type '{company.type}' was skipped")

		page += 1
		companies_request = CompaniesRequest(page=page)
		companies_response = await api.companies.get_companies(companies_request)


async def get_ordinal_branches(api: AsyncAPI, tycoon_id: int) -> AsyncGenerator[BaseCompany, None]:
	page = 1
	chain_branches_request = ChainBranchesRequest(tycoon_id=tycoon_id)
	chain_branches_response = await api.companies.get_chain_branches(chain_branches_request)

	while chain_branches_response.chain_data.companies:
		for company in chain_branches_response.chain_data.companies:
			if company.type == "ordinal":
				yield company
			elif company.type == "chain":
				raise RuntimeError(f"Unexpected chain company {company.permanent_id}")
			else:
				print(f"Company {company.permanent_id} with unknown type '{company.type}' was skipped")

		page += 1
		chain_branches_request = ChainBranchesRequest(tycoon_id=tycoon_id, page=page)
		chain_branches_response = await api.companies.get_chain_branches(chain_branches_request)


async def get_reviews(api: AsyncAPI, company_permanent_id: int) -> AsyncGenerator[Review, None]:
	request = ReviewsRequest(permanent_id=company_permanent_id, unread=True)
	response = await api.reviews.get_reviews(request)

	while response.list.items:
		for review in response.list.items:
			yield review

		continue_token = response.list.pager.continue_token
		request = ReviewsRequest(permanent_id=company_permanent_id, unread=True, continue_token=continue_token)
		response = await api.reviews.get_reviews(request)


async def main():
	basicConfig(
		format='[%(levelname)s | %(asctime)s | %(name)s] %(message)s',
		level=getenv('LOG_LEVEL', DEBUG),
	)
	session_id = getenv("YM_SESSION_ID")
	session_id2 = getenv("YM_SESSION_ID2")

	if not session_id:
		raise RuntimeError("YM_SESSION_ID is required")

	if not session_id2:
		raise RuntimeError("YM_SESSION_ID2 is required")

	api = await AsyncAPI.build(session_id=session_id, session_id2=session_id2)

	try:
		async for company in get_companies(api):
			print(company.permanent_id, company.display_name)

			async for review in get_reviews(api, company.permanent_id):
				print(review.id, review.full_text)

	finally:
		await api.session.close()


if __name__ == "__main__":
	run(main())
```
