---
name: threads-net-api
description: "Threads (threads.net) API: read a profile, page a user's posts and replies, fetch a single post by id or threads.net URL, walk its comment tree, and search Threads people, all as structured JSON. 6 endpoints, 2 credits by user_id and 4 by username. People search only, there is no keyword or hashtag content search."
version: 1.0.0
tags: threads, threads-api, threads-net, meta-threads, social-media, profiles, posts, replies, comments, people-search, social-listening, competitor-research, agents, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F9F5"
    homepage: https://scavio.dev/docs/threads-profile?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api
---

# Threads API - Profiles, Posts, Replies, Reposters

Read a Threads profile, page a user's posts and replies, fetch a single post by id or URL, walk its comment tree, and search Threads for people. All endpoints return structured JSON.

Two things to know before you start: **`user_id` costs half what a username costs**, and **Threads has no content search** — only people search.

## When to trigger

Use this skill when the user asks to:
- Look up a Threads profile and its follower/post counts
- Pull a Threads user's recent posts or their replies
- Read a single Threads post by id or by a threads.net URL
- Read the replies under a Threads post
- Find Threads accounts by name or handle
- Research a creator, brand or competitor's Threads presence
- Monitor what an account is posting on Threads

Do NOT reach for this skill to search Threads for a topic, keyword or hashtag. That capability does not exist. See Guardrails.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=threads-net-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/threads/profile` | 2 by `user_id`, 4 by `username` | Profile details for a Threads user |
| `POST /api/v1/threads/user/posts` | 2 by `user_id`, 4 by `username` | A user's posts, cursor-paginated |
| `POST /api/v1/threads/user/replies` | 2 by `user_id`, 4 by `username` | A user's replies, cursor-paginated |
| `POST /api/v1/threads/post` | 2 | A single post by id or threads.net URL |
| `POST /api/v1/threads/post/comments` | 2 | Replies to a post, cursor-paginated |
| `POST /api/v1/threads/search/users` | 2 | Threads profiles matching a name or handle |

### Cost rule: the handle surcharge

Cost is a function of the request body, not a constant.

- Addressed by **`user_id`: 2 credits.** This is the cheap path.
- Addressed by **`username`: 4 credits.** A handle costs double.

The reason is upstream: the provider's username lookup is dead, so passing a handle forces a second upstream call to resolve it to an id first. You pay for both.

Only `/profile`, `/user/posts` and `/user/replies` accept a username at all, so only those three can cost 4. `/post`, `/post/comments` and `/search/users` are always 2.

**Resolve once, reuse the id.** Call `/profile` or `/search/users` once with the handle, keep the `user_id`, and address everything after that by id. A 20-page crawl by handle costs 80 credits; by id it costs 40.

## Workflow

1. **Resolve the handle:** call `/threads/search/users` with the name or handle (2 credits), or `/threads/profile` with `username` (4 credits). Keep the `user_id` you get back.
2. **Profile:** call `/threads/profile` with `user_id` (2 credits).
3. **Posts and replies:** call `/threads/user/posts` and `/threads/user/replies` with `user_id`. Both return `next_cursor`; pass it back as `cursor` for the next page and stop when it is null.
4. **A single post:** call `/threads/post` with `post_id` or a threads.net `url`.
5. **Comments:** call `/threads/post/comments` with `post_id`. It is cursor-paginated the same way. Note this endpoint takes `post_id` only, never a username.

`profile`, `post` and `search/users` do not paginate. `user/posts`, `user/replies` and `post/comments` are cursor-paginated.

## Parameters

### Profile (`/profile`)

`username` or `user_id` is required.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string | one of | Numeric id, e.g. `63625256886`. The 2-credit path |
| `username` | string | one of | Handle without the `@`, e.g. `natgeo` (1-60 chars). Costs 2 extra credits |

### User posts (`/user/posts`) and user replies (`/user/replies`)

`username` or `user_id` is required.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string | one of | Numeric id. The 2-credit path |
| `username` | string | one of | Handle without the `@` (1-60 chars). Costs 2 extra credits |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Post (`/post`)

`post_id` or `url` is required.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `post_id` | string | one of | Post id, e.g. `3349029093483693129` |
| `url` | string | one of | A threads.net post URL |

### Post comments (`/post/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `post_id` | string | required | Post id. This endpoint does NOT accept a username or a URL |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### User search (`/search/users`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Name or handle to match (1-200 chars) |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Resolve the handle ONCE (2 credits), then work by id
found = requests.post(f"{BASE}/api/v1/threads/search/users", headers=HEADERS,
    json={"query": "national geographic"}).json()

user_id = "63625256886"  # taken from the search result, then reused

# 2. Profile by id: 2 credits. By username it would be 4.
profile = requests.post(f"{BASE}/api/v1/threads/profile", headers=HEADERS,
    json={"user_id": user_id}).json()

# 3. Page their posts by id (2 credits per page)
page = requests.post(f"{BASE}/api/v1/threads/user/posts", headers=HEADERS,
    json={"user_id": user_id}).json()
cursor = page["data"]["next_cursor"]
if cursor:
    page2 = requests.post(f"{BASE}/api/v1/threads/user/posts", headers=HEADERS,
        json={"user_id": user_id, "cursor": cursor}).json()

# 4. Their replies, same pattern
replies = requests.post(f"{BASE}/api/v1/threads/user/replies", headers=HEADERS,
    json={"user_id": user_id}).json()

# 5. A single post, then its comment tree (post_id only, never a handle)
post = requests.post(f"{BASE}/api/v1/threads/post", headers=HEADERS,
    json={"post_id": "3349029093483693129"}).json()
comments = requests.post(f"{BASE}/api/v1/threads/post/comments", headers=HEADERS,
    json={"post_id": "3349029093483693129"}).json()
```

## Response

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **profile** returns the user's profile details.
- **user/posts**, **user/replies** and **post/comments** return their rows plus `next_cursor`. A null `next_cursor` means there are no more pages.
- **post** returns the single post.
- **search/users** returns the matching profiles.

Read `credits_used` on the response rather than assuming a cost. It will read 4 whenever you addressed a user-keyed endpoint by handle.

## Guardrails

- **There is no Threads content search.** Searching Threads for a keyword, topic or hashtag is not possible through this API — the upstream's `search_top` and `search_recent` fail on every attempt. `/search/users` is people search and nothing else. If the user asks to search Threads posts for a term, tell them plainly that Threads does not expose this, and offer the alternative of pulling a known account's posts with `/user/posts` and filtering client-side. Never imply a content search exists.
- **Prefer `user_id` over `username` everywhere.** A handle doubles the cost of `/profile`, `/user/posts` and `/user/replies`, from 2 credits to 4. Resolve the handle once and reuse the id for the rest of the session.
- Do not send `username` and `user_id` together on the same request. Conflicting identifiers are rejected with a `422`.
- `/post/comments` takes `post_id` only. It has no username form and no URL form.
- Never fabricate post text, handles, follower counts or engagement numbers. Only return data the API returned.
- Preserve author attribution when summarising a thread.
- Threads content is public posts only. Do not present it as anything more.

## Failure handling

Threads uses different error codes from the retail endpoints. **There is no `400` and no `503` here.**

- `422` means a missing or conflicting identifier: no `username` and no `user_id`, or both at once. Send exactly one.
- `404` means no matching user was found. Check the handle spelling, or resolve it through `/search/users` first.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means a rate or usage limit was exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api).
- `502` means the upstream errored. Wait a few seconds and retry once.
- If a paginated call returns a null `next_cursor`, that is the end of the data, not a failure. Stop paging.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Docs

- [Threads profile](https://scavio.dev/docs/threads-profile?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Threads user posts](https://scavio.dev/docs/threads-user-posts?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Threads user replies](https://scavio.dev/docs/threads-user-replies?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Threads post](https://scavio.dev/docs/threads-post?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Threads post comments](https://scavio.dev/docs/threads-post-comments?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Threads user search](https://scavio.dev/docs/threads-user-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
