---
name: twitter-scraper-api
description: "Twitter (X) scraper API: search tweets and people, read a tweet with its replies and retweeters, and pull user profiles, tweets, replies, media, followers and followings, plus trending topics by country. Returns text, favorites, retweets, replies, quotes, views and follower counts as JSON. 11 endpoints, 1 credit each."
version: 1.0.1
tags: twitter, x, twitter-api, twitter-scraper, tweet-search, user-profiles, followers, trending-topics, social-media, social-listening, brand-monitoring, sentiment-analysis, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F426"
    homepage: https://scavio.dev/docs/x-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitter-scraper-api
---

# Twitter (X) Scraper API - Tweet Search, Profiles, Followers

Search X, read a single tweet with its replies and retweeters, pull a user's profile and their tweets, replies, media, followers, and followings, and get trending topics by country. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search tweets or people on X for a topic or keyword
- Read a tweet's full details, its replies, or who retweeted it
- Look up a user's profile by handle
- Pull a user's tweets, replies, or media
- List a user's followers or the accounts they follow
- Get trending topics for a country
- Monitor brand, competitor, or campaign mentions
- Build RAG or sentiment pipelines that need social context

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitter-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/x`. Every endpoint costs **1 credit**.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/x/search` | 1 | Search tweets and people |
| `POST /api/v1/x/tweet` | 1 | Full details for a single tweet |
| `POST /api/v1/x/tweet/comments` | 1 | Replies to a tweet (ranked or chronological) |
| `POST /api/v1/x/tweet/retweeters` | 1 | Users who retweeted a tweet |
| `POST /api/v1/x/user` | 1 | Profile details for a user |
| `POST /api/v1/x/user/tweets` | 1 | A user's tweets |
| `POST /api/v1/x/user/replies` | 1 | A user's tweets and replies |
| `POST /api/v1/x/user/media` | 1 | A user's media tweets |
| `POST /api/v1/x/user/followers` | 1 | A user's followers |
| `POST /api/v1/x/user/followings` | 1 | Accounts a user follows |
| `POST /api/v1/x/trending` | 1 | Trending topics for a country |

## Workflow

1. **Find tweets or people:** call `/x/search` with `search`. Use `search_type` to switch category (`Top`, `Latest`, `People`, `Photos`, `Videos`). Read `timeline[].tweet_id`.
2. **Read a tweet:** call `/x/tweet` with `tweet_id` for full metrics.
3. **Read the conversation:** call `/x/tweet/comments` with `tweet_id` (set `rank: latest` for chronological), and `/x/tweet/retweeters` for who retweeted.
4. **Look up a user:** call `/x/user` with `screen_name` (a handle without `@`).
5. **User activity:** call `/x/user/tweets`, `/x/user/replies`, or `/x/user/media` with `screen_name`.
6. **Social graph:** call `/x/user/followers` and `/x/user/followings`.
7. **Discovery:** call `/x/trending` with a `country` name.

Paginated endpoints return `next_cursor` (and often `prev_cursor`); pass `next_cursor` back as `cursor` for the next page. Stop when it is `null`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | string | required | Search query (1-500 chars) |
| `search_type` | string | `Top` | `Top`, `Latest`, `People`, `Photos`, `Videos` |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Tweet (`/tweet`)

`tweet_id`* — a tweet id, e.g. `1808168603721650364`.

### Tweet comments (`/tweet/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tweet_id` | string | required | Tweet id |
| `rank` | string | `top` | `top` (ranked) or `latest` (chronological) |
| `cursor` | string | -- | Pagination cursor |

### Tweet retweeters (`/tweet/retweeters`)

`tweet_id`* , `cursor` (optional).

### User (`/user`)

`screen_name`* — an X handle without `@`, e.g. `elonmusk`.

### User tweets / replies / media / followers / followings

| Parameter | Type | Default | Description |
|---|---|---|---|
| `screen_name` | string | required | Handle without `@` |
| `cursor` | string | -- | Pagination cursor |

### Trending (`/trending`)

`country` (optional, default `UnitedStates`) — a country name.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitter-scraper-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search — use "search", not "query"
results = requests.post(f"{BASE}/api/v1/x/search", headers=HEADERS,
    json={"search": "AI agents", "search_type": "Latest"}).json()

tweet_id = results["data"]["timeline"][0]["tweet_id"]

# 2. Full tweet + its replies
tweet = requests.post(f"{BASE}/api/v1/x/tweet", headers=HEADERS,
    json={"tweet_id": tweet_id}).json()

comments = requests.post(f"{BASE}/api/v1/x/tweet/comments", headers=HEADERS,
    json={"tweet_id": tweet_id, "rank": "latest"}).json()

# 3. A user's recent tweets
user_tweets = requests.post(f"{BASE}/api/v1/x/user/tweets", headers=HEADERS,
    json={"screen_name": "elonmusk"}).json()

# 4. Trending in a country
trending = requests.post(f"{BASE}/api/v1/x/trending", headers=HEADERS,
    json={"country": "UnitedStates"}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields per endpoint:

- **search** — `timeline[]` (`type`, `tweet_id`, `screen_name`, `text`, `lang`, `created_at`, `favorites`, `retweets`, `replies`, `quotes`, `bookmarks`, `views`, `source`), `next_cursor`, `prev_cursor`.
- **tweet** — `tweet_id`, `text`, `display_text`, `created_at`, `lang`, `favorites`, `retweets`, `replies`, `quotes`, `bookmarks`, `views`, `source`, `reply_to`.
- **tweet/comments** — `timeline[]` (`tweet_id`, `screen_name`, `text`, `created_at`, `favorites`, ...), `next_cursor`, `prev_cursor`.
- **tweet/retweeters** — `retweeters[]` (`user_id`, `screen_name`, `name`, `description`, `followers_count`, `friends_count`, `statuses_count`, `media_count`, `profile_image`), `next_cursor`.
- **user** — `rest_id`, `screen_name`, `name`, `description`, `followers_count`, `friends_count`, `statuses_count`, `media_count`, `blue_verified`, `avatar`, `header_image`, `created_at`, `location`, `website`.
- **user/tweets** — `pinned` (a tweet), `timeline[]` (`tweet_id`, `text`, `created_at`, `favorites`, `retweets`, `replies`, `quotes`, `views`, `conversation_id`), `next_cursor`.
- **user/replies** — `timeline[]` (same tweet item shape), `user`, `next_cursor`.
- **user/media** — `timeline[]` (same tweet item shape), `user`, `next_cursor`.
- **user/followers** — `followers_count`, `followers[]` (`user_id`, `screen_name`, `name`, `description`, `followers_count`, `blue_verified`, `location`), `next_cursor`.
- **user/followings** — `following[]` (same user item shape), `next_cursor`, `more_users`.
- **trending** — `trends[]` (`name`, `description`, `context`).

```json
{
  "data": {
    "timeline": [
      {
        "type": "tweet",
        "tweet_id": "1808168603721650364",
        "screen_name": "OpenAIDevs",
        "text": "Shipping agent tooling this week.",
        "lang": "en",
        "created_at": "2026-06-30T18:04:11+0000",
        "favorites": 4821,
        "retweets": 902,
        "replies": 311,
        "quotes": 77,
        "views": 512340,
        "source": "Twitter Web App"
      }
    ],
    "next_cursor": "DAADDAABCgAB...",
    "prev_cursor": "DAABCgABCgAB..."
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- The search field is `search`, not `query` — this differs from some other Scavio endpoints.
- `screen_name` is a handle without the leading `@`.
- Every X endpoint costs **1 credit**. Inform the user before paginating through many pages.
- Never fabricate tweet ids, handles, metrics, or replies. Only return API data.
- Surface engagement metrics as-is; do not round or invent counts.

## Failure handling

- `400` means an invalid or missing parameter (e.g. no `tweet_id` or `screen_name`) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitter-scraper-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest different keywords or a different `search_type`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="x")
```
