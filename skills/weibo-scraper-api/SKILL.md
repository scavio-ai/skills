---
name: weibo-scraper-api
description: Pull Weibo user profiles and posts, post comments/likes/reposts, keyword search across posts, videos, users, topics and images, the hot-search board and ranking boards, and channel feeds. 31 endpoints, 1 credit each, structured JSON.
version: 1.0.0
tags: weibo, weibo-api, china-social-media, microblog, social-media-data, posts, comments, keyword-search, hot-search, trending, user-data, china-market, influencer-data, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4AC"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api
---

# Weibo Scraper API - Users, Posts, Search, Hot Search

Pull Weibo user profiles and posts, a post's comments, likes and reposts, run keyword search across posts, videos, users, topics and images, read the hot-search board and ranking boards, and pull channel feeds. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Read a Weibo user's profile (by numeric id or handle), their posts or original-only posts, their fans, following or videos
- Read a post in full, or its comments, sub-comments, likes or reposts
- Search Weibo by keyword - posts (advanced or realtime), videos, users, topics, images, similar terms, or an AI-assisted answer
- Read the hot-search board and the entertainment / life / social ranking boards
- Pull a named channel's popular content
- Do China-market social listening, trend spotting or creator/topic research on Weibo

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=weibo-scraper-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Weibo endpoint costs **1 credit**.

### User

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/weibo/user/info` | Profile details for a user by `uid` or `custom` handle |
| `POST /api/v1/weibo/user/info-detail` | Extended profile details |
| `POST /api/v1/weibo/user/posts` | A user's posts, with an optional detail level (`feature` 0-3) |
| `POST /api/v1/weibo/user/original-posts` | A user's original (non-repost) posts |
| `POST /api/v1/weibo/user/fans` | A user's followers |
| `POST /api/v1/weibo/user/following` | Accounts a user follows |
| `POST /api/v1/weibo/user/videos` | A user's published videos |
| `POST /api/v1/weibo/user/video-collections` | A user's video collection folders |
| `POST /api/v1/weibo/user/video-collection` | Videos inside a collection folder (`cid`) |
| `POST /api/v1/weibo/user/search-posts` | Search within one user's posts |
| `POST /api/v1/weibo/user/recommend-timeline` | The recommended home timeline |

### Post

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/weibo/post` | Full detail for a single post by `id` (optional full long-text) |
| `POST /api/v1/weibo/post/comments` | Top-level comments on a post |
| `POST /api/v1/weibo/post/sub-comments` | Replies under a post's comments |
| `POST /api/v1/weibo/post/likes` | Accounts that liked a post |
| `POST /api/v1/weibo/post/reposts` | Reposts of a post |

### Search

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/weibo/search/advanced` | Keyword search with type and time filters |
| `POST /api/v1/weibo/search/realtime` | Newest posts matching a keyword |
| `POST /api/v1/weibo/search/videos` | Videos matching a keyword |
| `POST /api/v1/weibo/search/users` | Users matching a keyword and filters |
| `POST /api/v1/weibo/search/topics` | Topics matching a keyword |
| `POST /api/v1/weibo/search/pics` | Image posts matching a keyword |
| `POST /api/v1/weibo/search/similar` | Related search terms and accounts for a keyword |
| `POST /api/v1/weibo/search/ai` | AI-assisted answer for a query |

### Hot / rankings / feed

| Endpoint | What it returns |
|---|---|
| `POST /api/v1/weibo/hot-search` | The current hot-search board |
| `POST /api/v1/weibo/hot-search/index` | The top hot-search entries |
| `POST /api/v1/weibo/rankings/hot-timeline` | Trending posts over a time window (`ranking_type`) |
| `POST /api/v1/weibo/rankings/entertainment` | The entertainment ranking board |
| `POST /api/v1/weibo/rankings/life` | The lifestyle ranking board |
| `POST /api/v1/weibo/rankings/social` | The social ranking board |
| `POST /api/v1/weibo/channel-feed` | Popular content within a named channel |

## Key identifiers

- **`uid`** - a numeric user id (e.g. `7277477906`). `user/info` also accepts a `custom` handle instead.
- **`id`** - a post id (e.g. `5092682368025584`). Used by every `post/*` endpoint.
- User post lists paginate with `page` (and `since_id` where offered); comment/timeline endpoints paginate with `max_id` from the previous response.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. A user's profile, then their posts
info = requests.post(f"{BASE}/api/v1/weibo/user/info", headers=HEADERS,
    json={"uid": "7277477906"}).json()
posts = requests.post(f"{BASE}/api/v1/weibo/user/posts", headers=HEADERS,
    json={"uid": "7277477906", "page": 1}).json()

# 2. A post and its comments
post = requests.post(f"{BASE}/api/v1/weibo/post", headers=HEADERS,
    json={"id": "5092682368025584", "is_get_long_text": "true"}).json()
comments = requests.post(f"{BASE}/api/v1/weibo/post/comments", headers=HEADERS,
    json={"id": "5092682368025584", "count": 50}).json()

# 3. Realtime keyword search and the hot-search board
realtime = requests.post(f"{BASE}/api/v1/weibo/search/realtime", headers=HEADERS,
    json={"query": "yu7"}).json()
hot = requests.post(f"{BASE}/api/v1/weibo/hot-search", headers=HEADERS,
    json={}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/weibo/hot-search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the user / post / search payload, with lists under keys like `posts`, `comments`, `users`, `reposts` and cursors for pagination.

## Guardrails

- Every Weibo call is **1 credit**, including one that comes back empty.
- `user/info` needs either `uid` or `custom`; the `post/*` endpoints need `id`. A missing identifier is a `422`, not an outage.
- Paginate only with the cursor the previous response returned (`page`, `since_id` or `max_id`); stop when it stops advancing.
- Hot-search and ranking boards are point-in-time snapshots - re-fetch for a fresh board.
- Never fabricate follower counts, post text, comment text or user details. Only return what the API returned.
- Posts and comments are written by real people. Summarise; do not build profiles of individuals.

## Failure handling

- `400` means malformed input. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `422` means a required identifier is missing (e.g. no `uid`/`custom` or no `id`). Supply it and retry.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api).
- `502` means the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
