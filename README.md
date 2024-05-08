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
		csrf_token=...,
		session_id=...,
		session_id2=...,
	)

	# Do things here...


async def main() -> None:
	api = await AsyncAPI.build(
		csrf_token=...,
		session_id=...,
		session_id2=...,
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
The `PermanentId` belong to certain companies and cannot be used to respond to reviews from another company.

## Reviews
### Reviews fetching
```python
# Sync mode
from ya_business_api.sync_api import SyncAPI
from ya_business_api.reviews.dataclasses.requests import ReviewsRequest


api = SyncAPI.build(**kwargs)
request = ReviewsRequest(permanent_id=<permanent_id>)
response = api.reviews.get_reviews(request)

# Async mode
from ya_business_api.async_api import AsyncAPI
from ya_business_api.reviews.dataclasses.requests import ReviewsRequest


api = await AsyncAPI.build(**kwargs)
request = ReviewsRequest(permanent_id=<permanent_id>)
response = await api.reviews.get_reviews(request)
await api.session.close()
```

#### Filtering and ordering
```python
from ya_business_api.sync_api import SyncAPI
from ya_business_api.reviews.dataclasses.requests import ReviewsRequest
from ya_business_api.reviews.constants import Ranking


api = SyncAPI.build(**kwargs)
request = ReviewsRequest(
	permanent_id=<permanent_id>,
	ranking=Ranking.BY_RATING_DESC,
	unread=True,
	page=5,
)
response = api.reviews.get_reviews(request)
```

### Answering to reviews
```python
# Sync mode
from ya_business_api.sync_api import SyncAPI
from ya_business_api.reviews.dataclasses.requests import AnswerRequest


api = SyncAPI.build(**kwargs)
reviews = api.reviews.get_reviews()
request = AnswerRequest(
	review_id=reviews.list.items[0].id,
	text="Thank you!",
	reviews_csrf_token=reviews.list.csrf_token,
	answer_csrf_token=reviews.list.items[0].business_answer_csrf_token,
)
response = api.reviews.send_answer(request)

# Async mode
from ya_business_api.async_api import AsyncAPI
from ya_business_api.reviews.dataclasses.requests import AnswerRequest


api = await AsyncAPI.build(**kwargs)
reviews = await api.reviews.get_reviews()
request = AnswerRequest(
	review_id=reviews.list.items[0].id,
	text="Thank you!",
	reviews_csrf_token=reviews.list.csrf_token,
	answer_csrf_token=reviews.list.items[0].business_answer_csrf_token,
)
response = await api.reviews.send_answer(request)
await api.session.close()
```

## Companies
### Receiving companies
```python
# Sync mode
from ya_business_api.sync_api import SyncAPI


api = SyncAPI.build(**kwargs)
response = api.companies.get_companies()

# Async mode
from ya_business_api.async_mode


api = await AsyncAPI.build(**kwargs)
response = await api.companies.get_companies()

await api.session.close()
```

#### Filtering and pagination
```python
from ya_business_api.sync_api import SyncAPI
from ya_business_api.companies.dataclasses.requests import CompaniesRequest


api = SyncAPI.build(**kwargs)
request = CompaniesRequest(filter="My Company", page=5)
response = api.companies.get_companies(request)
```

## Shortcuts
### Answers deleting
```python
api.reviews.send_answer(AnswerRequest(text="", **kwargs))
```

### Automatic closing of the session (async mode)
```python
async with await AsyncAPI.make_session(session_id=..., session_id2=...) as session:
	api = AsyncAPI(permanent_id=..., csrf_token=..., session=session)
	...
```
