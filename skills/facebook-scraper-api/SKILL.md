---
name: facebook-scraper-api
description: Pull a Facebook page's profile, posts, reels and photos, one post with its comments, a single reel/video with downloadable URLs, a public group and its posts, an event, and hashtag posts. 11 endpoints, 1 credit each, structured JSON.
version: 1.0.0
tags: facebook, facebook-api, social-media-data, page-data, posts, reels, comments, groups, events, hashtags, video-download, brand-monitoring, influencer-data, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F44D"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=facebook-scraper-api
---

# Facebook API - Pages, Posts, Reels, Groups, Events

Pull a Facebook page's profile, posts, reels and photos, one post with its comments, a single reel or video with downloadable URLs, a public group and its posts, an event, and the top posts for a hashtag. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Read a Facebook page or public profile: name, category, verified flag, likes, followers, and (where published) website, phone, email, address, hours, rating, profile and cover photos
- Read a page's recent top posts, its reels (with downloadable video URLs), or its photo grid
- Read one post in full with its reaction breakdown and top comments
- Resolve a reel / video / watch item to its downloadable HD and SD video URLs
- Read a public group's profile and its top posts
- Read a public event (time, location, host, going/interested counts)
- Read the top public posts for a hashtag
- Do brand monitoring, competitor page analysis or content research on Facebook

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=facebook-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=facebook-scraper-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Facebook endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/facebook/profile` | 1 | A page or public profile: name, category, verified flag, likes, followers, talking-about and were-here counts, bio, and where published website/phone/email/address/hours/rating/screenname/creation date/profile+cover photo |
| `POST /api/v1/facebook/profile/posts` | 1 | A page's most recent top posts: text, timestamp, reaction total and breakdown, comment and share counts, media, permalink |
| `POST /api/v1/facebook/profile/reels` | 1 | A page's reels: id, url, downloadable video URLs, thumbnail, duration, play count, owner id |
| `POST /api/v1/facebook/profile/photos` | 1 | A page's photo grid: photo id, image URL, accessibility caption |
| `POST /api/v1/facebook/post` | 1 | One post in full: author, text, timestamp, reaction breakdown, comment and share counts, top comments, media, permalink |
| `POST /api/v1/facebook/post/comments` | 1 | The top visible comments on a post: id, author, text, reaction count, time |
| `POST /api/v1/facebook/reel` | 1 | One reel/video/watch item: title, description, downloadable HD and SD video URLs, thumbnail, duration, view/play counts, reactions, comments, shares, owner, permalink |
| `POST /api/v1/facebook/group` | 1 | A public group's profile: id, name, visibility, member count, description, privacy |
| `POST /api/v1/facebook/group/posts` | 1 | The top posts in a public group: author, text, timestamp, reactions, comment and share counts, media, permalink |
| `POST /api/v1/facebook/event` | 1 | A public event: name, description, start/end time, location, host, going and interested counts, cover photo |
| `POST /api/v1/facebook/hashtag` | 1 | The top public posts for a hashtag: author, text, timestamp, reactions, media, permalink |

## Parameters

Every endpoint except `hashtag` takes a single `url`:

| Parameter | Type | Description |
|---|---|---|
| `url` | string | A Facebook URL for the requested surface - a page/profile, post permalink, reel/video, group, or event. `profile` and `group` also accept a bare page id / group id |

`hashtag` takes:

| Parameter | Type | Description |
|---|---|---|
| `tag` | string | A hashtag name, with or without the leading `#` |

## Scope notes

- The post and group-post endpoints return the **current top posts**, not the full historical feed.
- `post/comments` returns the **top visible comments**, not the full thread or nested replies.
- Private groups and locked profiles are reported as unavailable (a `404`), and cost nothing.
- Reel and video URLs are directly downloadable but signed with a **short expiry** - use them promptly.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. A page's profile, then its recent posts
profile = requests.post(f"{BASE}/api/v1/facebook/profile", headers=HEADERS,
    json={"url": "https://www.facebook.com/nike"}).json()
posts = requests.post(f"{BASE}/api/v1/facebook/profile/posts", headers=HEADERS,
    json={"url": "https://www.facebook.com/nike"}).json()

# 2. One post in full, plus its top comments
post = requests.post(f"{BASE}/api/v1/facebook/post", headers=HEADERS,
    json={"url": "https://www.facebook.com/nike/posts/pfbid0..."}).json()

# 3. A reel resolved to downloadable HD/SD URLs
reel = requests.post(f"{BASE}/api/v1/facebook/reel", headers=HEADERS,
    json={"url": "https://www.facebook.com/reel/1234567890"}).json()

# 4. Top posts for a hashtag
tag = requests.post(f"{BASE}/api/v1/facebook/hashtag", headers=HEADERS,
    json={"tag": "photography"}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/facebook/profile \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.facebook.com/nike"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the profile / posts / reel / group / event payload, with a `count` on the list endpoints.

## Guardrails

- Every Facebook call is **1 credit**. A `404` for a private group, locked profile or dead id is billed as `false` - the customer is not charged for data that was genuinely unavailable.
- Posts and group posts are the **current top posts**, not the full feed; comments are the **top visible** ones, not the full thread.
- Reel/video URLs expire quickly - download promptly rather than storing the URL.
- Never fabricate follower counts, post text, comment text or contact details. Only return what the API returned.
- Profiles, posts and comments involve real people. Summarise; do not build profiles of individuals, and respect that contact fields are only returned when the page itself published them.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the surface is not found or unavailable (e.g. a private group or locked profile).
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=facebook-scraper-api).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
