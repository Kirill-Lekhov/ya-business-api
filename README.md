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
request = ReviewsRequest(
	permanent_id=<permanent_id>,
	ranking=Ranking.BY_RATING_DESC,		# Optional
	unread=True,						# Optional
	page=5,								# Optional
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
request = AnswerRequest(
	review_id=reviews.list.items[0].id,
	text="Thank you!",
	reviews_csrf_token=reviews.list.csrf_token,
	answer_csrf_token=reviews.list.items[0].business_answer_csrf_token,
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

### Receiving company chains
Some companies have several branches, in such cases the company will have the "chain" type.
This method will allow you to get a list of all branches.



* Async mode support: ✅;
* Validation disabling: ✅.
```python
from ya_business_api.sync_api import SyncAPI
from ya_business_api.companies.dataclasses.request import ChainListRequest


api = SyncAPI.build(...)
request = ChainListRequest(
	tycoon_id=<tycoon_id>,		# Can be found in the Company dataclass.
	geo_id=0,					# Optional.
	page=1,						# Optional
)
response = api.companies.get_chain_list(
	request,		# Optional
	raw=False,		# Optional
)
```

#### ⚠️WARNING⚠️
Raw response of this method is HTML text.

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
### Getting the number of reviews asynchronously
```python
from ya_business_api.async_api import AsyncAPI
from ya_business_api.companies.dataclasses.requests import ChainListRequest
from ya_business_api.companies.dataclasses.chain_list import CompanyCardWithPhoto
from ya_business_api.reviews.dataclasses.requests import ReviewsRequest


api = await AsyncAPI.build(...)

try:
	companies_response = await api.companies.get_companies()
	open_companies = filter(lambda x: x.publishing_status != "closed", companies_response.list_companies)

	for company in open_companies:
		page = 1
		chain_list_request = ChainListRequest(tycoon_id=company.tycoon_id, page=page)
		chain_list_response = await api.companies.get_chain_list(chain_list_request)

		while len(chain_list_response.company_cards):
			company_cards = [i for i in chain_list_response.company_cards if isinstance(i, CompanyCardWithPhoto)]
			# Only company cards with photo contains permalink
			# It is possible that the branch also contains branches, but this is not taken into account in this guide

			for card in company_cards:
				reviews_request = ReviewsRequest(permanent_id=card.permalink)
				reviews_response = await api.reviews.get_reviews(reviews_request)
				print(company.permanent_id, card.permalink, reviews_response.list.pager.total)

			page += 1
			chain_list_request = ChainListRequest(tycoon_id=company.tycoon_id, page=page)
			chain_list_response = await api.companies.get_chain_list(chain_list_request)

finally:
	await api.session.close()
```
