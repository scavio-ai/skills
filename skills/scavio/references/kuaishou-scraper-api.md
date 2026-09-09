# Kuaishou Scraper API - Profiles, Videos, Comments, Search

Read public data from Kuaishou, the Chinese short-video platform: user profiles, their posts and live status, single videos and batches of them, comment threads and their replies, hashtag feeds, the platform leaderboards, and four separate search endpoints. All endpoints return structured JSON.

**This is Kuaishou China (kuaishou.com), not Kwai.** Kwai international (kwai.com) is not served by this API. See Guardrails.

**Pricing is per endpoint, from 1 to 40 credits.** There is no flat platform price. Read the cost column before every call.

## When to trigger

Use this skill when the user asks to:
- Look up a Kuaishou creator's profile, posts or current live status
- Turn a Kuaishou share link into a user id
- Read a Kuaishou video by photo id or URL, or several at once
- Read the comments on a Kuaishou video, or the replies under one comment
- Search Kuaishou for videos, users, live streams, or all of them at once
- Pull the posts under a Kuaishou hashtag
- Read the Kuaishou hot, live, shopping, brand or music leaderboards
- Research Chinese short-video creators or trends

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. **Costs differ by up to 40x between endpoints.** Copy the path verbatim from this table.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/kuaishou/profile` | **10** | Profile details for a user |
| `POST /api/v1/kuaishou/user/posts` | 1 | A user's top posts, cursor-paginated |
| `POST /api/v1/kuaishou/user/live` | 1 | A user's current live-stream status |
| `POST /api/v1/kuaishou/user/resolve` | 1 | Turns a Kuaishou share link into a user id |
| `POST /api/v1/kuaishou/video` | **2** | A single video by photo id or URL |
| `POST /api/v1/kuaishou/video/comments` | 1 | Comments on a video, cursor-paginated |
| `POST /api/v1/kuaishou/video/sub-comments` | 1 | Replies under one root comment, cursor-paginated |
| `POST /api/v1/kuaishou/videos/batch` | **40** | Up to 20 videos in one call |
| `POST /api/v1/kuaishou/search` | **10** | Mixed-result search |
| `POST /api/v1/kuaishou/search/videos` | **10** | Video search |
| `POST /api/v1/kuaishou/search/users` | **10** | User search |
| `POST /api/v1/kuaishou/search/live` | **10** | Live-stream search |
| `POST /api/v1/kuaishou/tag/feed` | 1 | Posts under a hashtag, cursor-paginated |
| `POST /api/v1/kuaishou/trending` | 1 | Hot, live, shopping, brand and music leaderboards |

Summary of the four tiers: `videos/batch` is 40. `profile` and all four search endpoints are 10. `video` is 2. Everything else is 1.

### Cost planning

- `/profile` at 10 credits is the dearest single-object call on the platform. If all you need is a creator's recent posts, `/user/posts` at 1 credit may be enough on its own.
- `/videos/batch` at 40 credits is the dearest call, full stop. It is capped at 20 photo ids. Twenty individual `/video` calls would cost 40 credits too, so batching saves round trips, not money. Do not reach for it to fetch two or three videos.
- The four search endpoints each cost 10. Do not fan out a keyword across all four when one will answer the question.

## Workflow

1. **From a share link:** call `/kuaishou/user/resolve` with `share_link` (1 credit) to get a `user_id`.
2. **Creator research:** `/kuaishou/user/posts` with `user_id` (1 credit) for the feed. Only spend the 10 credits on `/kuaishou/profile` if you need the profile fields themselves.
3. **Live check:** `/kuaishou/user/live` with `user_id` (1 credit).
4. **A video:** `/kuaishou/video` with `photo_id` or `url` (2 credits).
5. **Comments:** `/kuaishou/video/comments` with `photo_id` (1 credit). To expand one thread, call `/kuaishou/video/sub-comments` with the same `photo_id` plus that comment's `root_comment_id`.
6. **Discovery:** `/kuaishou/search` (mixed), `/kuaishou/search/videos`, `/kuaishou/search/users` or `/kuaishou/search/live`, all with `keyword`, all 10 credits. `/kuaishou/tag/feed` and `/kuaishou/trending` are 1 credit each and are the cheap discovery route.

Cursor-paginated: `user/posts`, `video/comments`, `video/sub-comments`, all four search endpoints, and `tag/feed`. Each returns `next_cursor`; pass it back as `cursor` and stop when it is null. **Every page of a search costs another 10 credits.**

Not paginated at all: `profile`, `user/live`, `user/resolve`, `video`, `videos/batch`, `trending`.

## Parameters

### Profile (`/profile`) — 10 credits

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string | required | Kuaishou user id, e.g. `5518803932` |

### User posts (`/user/posts`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string | required | Kuaishou user id |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### User live (`/user/live`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string | required | Kuaishou user id |

### User resolve (`/user/resolve`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `share_link` | string (URL) | required | A `kuaishou.com` or `v.kuaishou.com` link, e.g. `https://v.kuaishou.com/KcdKDwFp`. `kwai.com` is not supported |

### Video (`/video`) — 2 credits

`photo_id` or `url` is required.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `photo_id` | string | one of | Kuaishou photo id, e.g. `3xtdqvdnqd3psuc` |
| `url` | string (URL) | one of | A Kuaishou video URL |

### Video comments (`/video/comments`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `photo_id` | string | required | Kuaishou photo id |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Comment replies (`/video/sub-comments`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `photo_id` | string | required | Kuaishou photo id |
| `root_comment_id` | string | required | The id of the comment whose replies you want |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |
| `count` | integer 1-50 | -- | Replies per page |

### Videos batch (`/videos/batch`) — 40 credits

| Parameter | Type | Default | Description |
|---|---|---|---|
| `photo_ids` | array of string | required | 1 to 20 photo ids. The cap of 20 is hard |

### Search (`/search`, `/search/videos`, `/search/users`, `/search/live`) — 10 credits each

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search keyword (1-200 chars) |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Tag feed (`/tag/feed`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tag` | string | required | Hashtag text (1-200 chars) |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Trending (`/trending`) — 1 credit

| Parameter | Type | Default | Description |
|---|---|---|---|
| `board` | string | `hot` | `hot`, `live`, `shopping`, `brand`, `music` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Share link -> user id (1 credit)
resolved = requests.post(f"{BASE}/api/v1/kuaishou/user/resolve", headers=HEADERS,
    json={"share_link": "https://v.kuaishou.com/KcdKDwFp"}).json()

user_id = "5518803932"

# 2. Their posts (1 credit) - far cheaper than /profile, which is 10
posts = requests.post(f"{BASE}/api/v1/kuaishou/user/posts", headers=HEADERS,
    json={"user_id": user_id}).json()

# 3. Full profile - 10 credits, only call it if you need the profile fields
profile = requests.post(f"{BASE}/api/v1/kuaishou/profile", headers=HEADERS,
    json={"user_id": user_id}).json()

# 4. A single video (2 credits)
video = requests.post(f"{BASE}/api/v1/kuaishou/video", headers=HEADERS,
    json={"photo_id": "3xtdqvdnqd3psuc"}).json()

# 5. Comments (1 credit), then one thread's replies (1 credit).
#    NOTE the path is /video/sub-comments.
comments = requests.post(f"{BASE}/api/v1/kuaishou/video/comments", headers=HEADERS,
    json={"photo_id": "5218546261880462502"}).json()
replies = requests.post(f"{BASE}/api/v1/kuaishou/video/sub-comments", headers=HEADERS,
    json={"photo_id": "5218546261880462502",
          "root_comment_id": "14000000123456789", "count": 20}).json()

# 6. Search - 10 credits PER PAGE
found = requests.post(f"{BASE}/api/v1/kuaishou/search/videos", headers=HEADERS,
    json={"keyword": "美妆"}).json()

# 7. Cheap discovery: hashtag feed and leaderboards, 1 credit each
tag = requests.post(f"{BASE}/api/v1/kuaishou/tag/feed", headers=HEADERS,
    json={"tag": "挑战"}).json()
board = requests.post(f"{BASE}/api/v1/kuaishou/trending", headers=HEADERS,
    json={"board": "hot"}).json()

# 8. Batch - 40 credits, max 20 ids
batch = requests.post(f"{BASE}/api/v1/kuaishou/videos/batch", headers=HEADERS,
    json={"photo_ids": ["5228960823332207296", "5196309727975443273"]}).json()
```

## Response

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **profile**, **user/live**, **user/resolve**, **video** and **trending** return a single object each: profile details, live status, the resolved user id, the video, and the requested leaderboard.
- **user/posts**, **video/comments**, **video/sub-comments**, the four search endpoints and **tag/feed** return their rows plus `next_cursor`. A null `next_cursor` means the end of the data.
- **videos/batch** returns the requested videos in one payload.

Always read `credits_used` off the response rather than assuming. The per-call cost ranges from 1 to 40.

## Guardrails

- **Call it Kuaishou, or Kuaishou (China). Never Kwai.** This API serves kuaishou.com only. Kwai international (kwai.com) is not served: a real kwai.com photo id comes back as an empty envelope, not an error. If the user says "Kwai" or gives a kwai.com link, tell them this API covers Kuaishou China only before spending any credits.
- `/user/resolve` accepts `kuaishou.com` and `v.kuaishou.com` links only.
- **Quote the per-endpoint cost, never a platform cost.** Saying "Kuaishou calls cost 1 credit" is wrong by up to 40x. `profile` is 10, `video` is 2, `videos/batch` is 40, all four search endpoints are 10, everything else is 1.
- Before a multi-page search, tell the user the running cost. Ten pages of `/search/videos` is 100 credits.
- `/videos/batch` is capped at 20 photo ids. That cap exists precisely because this is the one call that fans out upstream spend. Do not attempt to work around it by chaining batches without telling the user what it will cost.
- **The path is `/api/v1/kuaishou/video/sub-comments`.** Do not derive it from the name "comment replies". Copy the path from the table.
- Never fabricate view counts, follower counts, video ids, comment text or leaderboard positions. Only return data the API returned.
- Content and interface text are largely in Chinese. Translate for the user when helpful, but keep the original text alongside so ids and handles stay verifiable.
- Live status is a snapshot. A creator shown as live may have ended the stream seconds later; say so when it matters.

## Failure handling

Kuaishou uses a narrow set of error codes. **There is no `400`, no `404` and no `503` here.**

- `422` means a missing identifier, e.g. no `photo_id` and no `url` on `/video`. Send one.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means a rate or usage limit was exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api).
- `502` is the one to understand. **Kuaishou hides its errors inside HTTP 200 responses**, returning a success status with a failure code in the body. Those are detected and surfaced to you as a `502`. So a 502 here does not necessarily mean the upstream is down; it often means the id, link or keyword was rejected. Re-check the identifier before retrying blindly, and do not retry more than once or twice.
- An empty result set from a kwai.com id is expected, not a bug. See Guardrails.
- If a paginated call returns a null `next_cursor`, that is the end of the data. Stop paging, especially on the 10-credit search endpoints.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Docs

- [Kuaishou profile](https://scavio.dev/docs/kuaishou-profile?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou user posts](https://scavio.dev/docs/kuaishou-user-posts?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou user live](https://scavio.dev/docs/kuaishou-user-live?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou user resolve](https://scavio.dev/docs/kuaishou-user-resolve?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou video](https://scavio.dev/docs/kuaishou-video?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou video comments](https://scavio.dev/docs/kuaishou-video-comments?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou comment replies](https://scavio.dev/docs/kuaishou-comment-replies?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou videos batch](https://scavio.dev/docs/kuaishou-videos-batch?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou search](https://scavio.dev/docs/kuaishou-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou video search](https://scavio.dev/docs/kuaishou-video-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou user search](https://scavio.dev/docs/kuaishou-user-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou live search](https://scavio.dev/docs/kuaishou-live-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou tag feed](https://scavio.dev/docs/kuaishou-tag-feed?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Kuaishou trending](https://scavio.dev/docs/kuaishou-trending?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
