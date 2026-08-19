---
name: tiktok-scraper-api
description: "TikTok scraper API: look up profiles by username or sec_user_id, list a user's videos, read full video detail, comments and comment replies, search videos and users by keyword, pull hashtag stats and hashtag videos, and walk followers and followings. 11 endpoints, all 1 credit, structured JSON."
version: 1.0.4
tags: tiktok, tiktok-scraper, tiktok-api, social-media, short-video, profiles, videos, comments, hashtags, followers, influencer-marketing, social-listening, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F3B5"
    homepage: https://scavio.dev/docs/tiktok-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api
---

# TikTok Scraper API - Profiles, Videos, Comments, Hashtags

Search TikTok videos and users, look up profiles, read comments and replies, explore hashtags, and list followers/followings. Returns structured JSON with engagement stats, video metadata, and social graph data.

## When to trigger

Use this skill when the user asks to:
- Look up a TikTok creator's profile, follower count, or bio
- Search TikTok for videos by keyword or topic
- Search for TikTok users/creators
- Get details, stats, or engagement metrics for a specific TikTok video
- Read comments or replies on a TikTok video
- Explore a hashtag's stats or trending videos
- List a creator's followers or who they follow
- Analyze TikTok trends, influencer reach, or content performance
- Build RAG pipelines that need short-form video context

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Workflow

1. **Resolving a username:** most endpoints require a `sec_user_id`. Call `/tiktok/profile` with a `username` first, then use `data.user.sec_uid` for subsequent requests.
2. **Browsing a creator's videos:** call `/tiktok/user/posts` with the `sec_user_id`. Use `sort_type: "1"` for most popular.
3. **Video deep-dive:** call `/tiktok/video` with a `video_id` for full details including play URLs, cover images, and duration.
4. **Reading comments:** call `/tiktok/video/comments` for top-level comments, then `/tiktok/video/comments/replies` with a `comment_id` for threaded replies.
5. **Searching:** call `/tiktok/search/videos` or `/tiktok/search/users` with a keyword. Filter by `publish_time` and `sort_type`.
6. **Hashtag research:** call `/tiktok/hashtag` by name to get the `hashtag_id` and view counts, then `/tiktok/hashtag/videos` to list videos under it.
7. **Social graph:** call `/tiktok/user/followers` or `/tiktok/user/followings` with a `sec_user_id`.

## Endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v1/tiktok/profile` | 1 | Get user profile by username or sec_user_id |
| `POST https://api.scavio.dev/api/v1/tiktok/user/posts` | 1 | List a user's videos (paginated, sortable) |
| `POST https://api.scavio.dev/api/v1/tiktok/video` | 1 | Get full details for a single video |
| `POST https://api.scavio.dev/api/v1/tiktok/video/comments` | 1 | List comments on a video |
| `POST https://api.scavio.dev/api/v1/tiktok/video/comments/replies` | 1 | List replies to a specific comment |
| `POST https://api.scavio.dev/api/v1/tiktok/search/videos` | 1 | Search videos by keyword |
| `POST https://api.scavio.dev/api/v1/tiktok/search/users` | 1 | Search users by keyword |
| `POST https://api.scavio.dev/api/v1/tiktok/hashtag` | 1 | Get hashtag details and stats |
| `POST https://api.scavio.dev/api/v1/tiktok/hashtag/videos` | 1 | List videos for a hashtag |
| `POST https://api.scavio.dev/api/v1/tiktok/user/followers` | 1 | List a user's followers |
| `POST https://api.scavio.dev/api/v1/tiktok/user/followings` | 1 | List accounts a user follows |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Profile Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | TikTok handle (without @). One of `username` or `sec_user_id` required. |
| `sec_user_id` | string | -- | Secure user ID. One of `username` or `sec_user_id` required. |

## User Posts Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sec_user_id` | string | required | Secure user ID from profile endpoint |
| `cursor` | string | `"0"` | Pagination cursor. Use `data.max_cursor` from previous response. |
| `count` | number | `20` | Results per page (1-30) |
| `sort_type` | string | `"0"` | `"0"` = latest, `"1"` = popular |

## Video Detail Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `video_id` | string | required | TikTok video ID |

## Video Comments Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `video_id` | string | required | Video ID |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `20` | Results per page (1-50) |

## Comment Replies Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `video_id` | string | required | Video ID |
| `comment_id` | string | required | Comment ID (`cid` from comments endpoint) |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `20` | Results per page (1-50) |

## Search Videos Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search query (1-500 chars) |
| `cursor` | string | `"0"` | Pagination offset |
| `count` | number | `20` | Results per page (1-30) |
| `sort_type` | string | `"0"` | `"0"` = relevance, `"1"` = most likes |
| `publish_time` | string | `"0"` | `"0"` = all time, `"1"` = last day, `"7"` = week, `"30"` = month, `"90"` = 3 months, `"180"` = 6 months |

## Search Users Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search query (1-500 chars) |
| `cursor` | string | `"0"` | Pagination offset |
| `count` | number | `20` | Results per page (1-30) |

## Hashtag Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `hashtag_name` | string | -- | Hashtag text (without #). One of `hashtag_name` or `hashtag_id` required. |
| `hashtag_id` | string | -- | Numeric hashtag ID. One of `hashtag_name` or `hashtag_id` required. |

## Hashtag Videos Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `hashtag_id` | string | required | From hashtag info endpoint |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `20` | Results per page (1-30) |

## Followers / Followings Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sec_user_id` | string | required | From profile endpoint |
| `count` | number | `20` | Results per page (1-20) |
| `page_token` | string | -- | From previous response `data.next_page_token` |
| `min_time` | number | -- | From previous response `data.min_time` |

## Pagination Reference

| Style | Endpoints | Next page | Stop condition |
|---|---|---|---|
| Cursor string | user/posts | `cursor = data.max_cursor` | `data.has_more === 0` |
| Offset number | search/*, hashtag/videos, video/comments, video/comments/replies | `cursor = data.cursor` | `data.has_more === 0` |
| Token + time | user/followers, user/followings | `page_token` + `min_time` | `data.has_more === false` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Look up a profile
profile = requests.post(f"{BASE}/api/v1/tiktok/profile", headers=HEADERS,
    json={"username": "tiktok"}).json()

sec_uid = profile["data"]["user"]["sec_uid"]
print(f"{profile['data']['user']['nickname']}: {profile['data']['user']['follower_count']} followers")

# 2. List their most popular videos
posts = requests.post(f"{BASE}/api/v1/tiktok/user/posts", headers=HEADERS,
    json={"sec_user_id": sec_uid, "sort_type": "1", "count": 5}).json()

for v in posts["data"]["aweme_list"]:
    print(f"{v['desc'][:60]}  -- {v['statistics']['play_count']} views")

# 3. Get details for a specific video
video = requests.post(f"{BASE}/api/v1/tiktok/video", headers=HEADERS,
    json={"video_id": "7350810998023949599"}).json()

detail = video["data"]["aweme_detail"]
print(f"Likes: {detail['statistics']['digg_count']}, Comments: {detail['statistics']['comment_count']}")

# 4. Read comments on that video
comments = requests.post(f"{BASE}/api/v1/tiktok/video/comments", headers=HEADERS,
    json={"video_id": "7350810998023949599", "count": 10}).json()

for c in comments["data"]["comments"]:
    print(f"@{c['user']['unique_id']}: {c['text']}")

# 5. Search for videos
results = requests.post(f"{BASE}/api/v1/tiktok/search/videos", headers=HEADERS,
    json={"keyword": "cooking recipe", "count": 10, "publish_time": "7"}).json()

# 6. Explore a hashtag
tag = requests.post(f"{BASE}/api/v1/tiktok/hashtag", headers=HEADERS,
    json={"hashtag_name": "fyp"}).json()

tag_id = tag["data"]["challengeInfo"]["challenge"]["id"]
print(f"#{tag['data']['challengeInfo']['challenge']['title']}: {tag['data']['challengeInfo']['stats']['viewCount']} views")

# 7. List hashtag videos
tag_vids = requests.post(f"{BASE}/api/v1/tiktok/hashtag/videos", headers=HEADERS,
    json={"hashtag_id": tag_id, "count": 10}).json()
```

## Profile Response

```json
{
  "data": {
    "user": {
      "unique_id": "tiktok",
      "nickname": "TikTok",
      "sec_uid": "MS4wLjABAAAAv7iSuuXDJGDvJkmH_vz1qkDZYo1apxgzaxdBSeIuPiM",
      "uid": "107955",
      "signature": "One TikTok can make a big impact",
      "bio_url": "linktr.ee/tiktok",
      "follower_count": 94066595,
      "following_count": 1,
      "aweme_count": 1511,
      "total_favorited": 458010199
    }
  },
  "response_time": 1428,
  "credits_used": 1,
  "credits_remaining": 6545
}
```

## Video Detail Response

```json
{
  "data": {
    "aweme_detail": {
      "aweme_id": "7350810998023949599",
      "desc": "im so sick of being tired im so tired of being sick",
      "create_time": 1711494099,
      "statistics": {
        "digg_count": 2002382,
        "comment_count": 8119,
        "play_count": 12171757,
        "share_count": 274978,
        "collect_count": 211332
      }
    }
  },
  "response_time": 1605,
  "credits_used": 1,
  "credits_remaining": 6544
}
```

## Hashtag Response

```json
{
  "data": {
    "challengeInfo": {
      "challenge": {
        "id": "229207",
        "title": "fyp",
        "desc": "",
        "stats": {
          "videoCount": 0,
          "viewCount": 119178100000000
        }
      }
    }
  },
  "response_time": 969,
  "credits_used": 1,
  "credits_remaining": 6543
}
```

## Guardrails

- All TikTok calls cost 1 credit each. Inform the user before paginating through many pages.
- Never fabricate usernames, video captions, follower counts, or comment text. Only return API data.
- Most endpoints require a `sec_user_id`, not a username. Always resolve via the profile endpoint first.
- All `create_time` fields are Unix timestamps in seconds. Multiply by 1000 for JavaScript `Date`.
- Avatar and image fields return an object with a `url_list` array. Use `.url_list[0]` for the URL.
- Do not silently omit any data. Surface all fields so the user can decide what to use.

## Failure handling

- `401` means the API key is invalid or missing. Prompt the user to check their `SCAVIO_API_KEY`.
- `429` means rate limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest different keywords, a broader `publish_time`, or a different `sort_type`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="tiktok")
```
