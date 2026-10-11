---
name: tiktok-scraper-api
description: "TikTok scraper API: look up profiles by username or sec_user_id, list a user's videos, read full video detail, transcripts, comments and comment replies, search videos, users and sounds, pull hashtag stats and videos, sound detail and the Top 50 and Viral 50 charts, trending searches and videos, similar creators, playlists, live status and account region, and walk followers and followings. 24 endpoints, all 1 credit, structured JSON."
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

Search TikTok videos, users and sounds, look up profiles, read comments, replies and transcripts, explore hashtags, sounds and the sound charts, read trending searches and videos, find similar creators, list playlists, check live status and account region, and list followers/followings. Returns structured JSON with engagement stats, video metadata, and social graph data.

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
- Get the spoken-word transcript of a TikTok video
- See what is trending on TikTok now (searches, videos) or get search autocomplete for a keyword
- Look up a TikTok sound, the videos that use it, sound search, or the Top 50 / Viral 50 sound chart
- Find creators similar to a given account (lookalike influencer discovery)
- List a creator's playlists (series) or the videos in a playlist
- Check whether a creator is live right now, or which country an account is registered in

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

## Workflow

1. **Resolving a username:** most endpoints require a `sec_user_id`. Call `/tiktok/profile` with a `username` first, then use `data.user.sec_uid` for subsequent requests.
2. **Browsing a creator's videos:** call `/tiktok/user/posts` with the `sec_user_id`. Use `sort_type: "1"` for most popular.
3. **Video deep-dive:** call `/tiktok/video` with a `video_id` for full details including play URLs, cover images, and duration.
4. **Reading comments:** call `/tiktok/video/comments` for top-level comments, then `/tiktok/video/comments/replies` with a `comment_id` for threaded replies.
5. **Searching:** call `/tiktok/search/videos` or `/tiktok/search/users` with a keyword. Filter by `publish_time` and `sort_type`.
6. **Hashtag research:** call `/tiktok/hashtag` by name to get the `hashtag_id` and view counts, then `/tiktok/hashtag/videos` to list videos under it.
7. **Social graph:** call `/tiktok/user/followers` or `/tiktok/user/followings` with a `sec_user_id`.
8. **Transcript:** call `/tiktok/video/transcript` with a `video_id` or `url`. Check `data.available` before reading `segments` or `text`.
9. **Trending:** call `/tiktok/trending/searches` (no params) for trending search terms, `/tiktok/trending/videos` for a fresh sample of trending videos, and `/tiktok/search/suggestions` with a `keyword` for autocomplete.
10. **Sounds:** call `/tiktok/search/music` with a `keyword` or `/tiktok/music/chart` (`chart: "top"` or `"viral"`), take a sound's `id_str`, then call `/tiktok/music` for detail or `/tiktok/music/videos` for the videos that use it.
11. **Lookalikes and playlists:** call `/tiktok/user/similar` or `/tiktok/user/playlists` with a `sec_user_id`; pass a playlist's `mixId` as `playlist_id` to `/tiktok/playlist/videos`.
12. **Live and region by username:** call `/tiktok/user/live` or `/tiktok/user/region` with a `username`. `/tiktok/user/region` also returns `sec_user_id`, so it is a cheap username-to-sec_user_id lookup.

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
| `POST https://api.scavio.dev/api/v1/tiktok/video/transcript` | 1 | Spoken-word transcript of a video (segments + full text) |
| `POST https://api.scavio.dev/api/v1/tiktok/trending/searches` | 1 | Search terms trending now (about 90 per call) |
| `POST https://api.scavio.dev/api/v1/tiktok/trending/videos` | 1 | A fresh sample of trending videos (about 6-15 per call) |
| `POST https://api.scavio.dev/api/v1/tiktok/search/suggestions` | 1 | Search autocomplete for a keyword |
| `POST https://api.scavio.dev/api/v1/tiktok/search/music` | 1 | Search sounds by keyword |
| `POST https://api.scavio.dev/api/v1/tiktok/music` | 1 | Sound detail by `music_id` |
| `POST https://api.scavio.dev/api/v1/tiktok/music/videos` | 1 | Videos that use a sound |
| `POST https://api.scavio.dev/api/v1/tiktok/music/chart` | 1 | Top 50 or Viral 50 sound chart |
| `POST https://api.scavio.dev/api/v1/tiktok/user/similar` | 1 | Creators similar to a user (about 30 per page) |
| `POST https://api.scavio.dev/api/v1/tiktok/user/playlists` | 1 | A user's playlists (series) |
| `POST https://api.scavio.dev/api/v1/tiktok/playlist/videos` | 1 | Videos in a playlist |
| `POST https://api.scavio.dev/api/v1/tiktok/user/live` | 1 | Whether a user is live now, with viewer count |
| `POST https://api.scavio.dev/api/v1/tiktok/user/region` | 1 | Country an account is registered in, plus `sec_user_id` |

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

## Video Transcript Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `video_id` | string | -- | TikTok video ID. One of `video_id` or `url` required. |
| `url` | string | -- | TikTok video or share URL. One of `video_id` or `url` required. |
| `language` | string | -- | Two-letter code to pick a caption track when there are several, e.g. `en` |

## Trending Searches Parameters

No parameters. Send `{}`.

## Trending Videos Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `count` | number | `15` | Requested videos (1-15). Each call returns about 6-15 whatever you ask for. |

## Search Suggestions Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Partial or full search term (1-500 chars) |

## Search Sounds Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search term (1-500 chars) |
| `cursor` | string | `"0"` | Pagination offset (`data.cursor` from the previous response) |
| `count` | number | `20` | Sounds per page (1-20) |

## Sound Detail Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `music_id` | string | required | Numeric sound ID. Use `id_str` from search/music or music/chart. |

## Sound Videos Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `music_id` | string | required | Numeric sound ID |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `10` | Accepted (1-30) but ignored upstream; about 14 videos per page |

## Sound Chart Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chart` | string | `"top"` | `"top"` = Top 50, `"viral"` = Viral 50 |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `50` | Sounds per page (1-50) |

## Similar Creators Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sec_user_id` | string | required | From profile or user/region |
| `page_token` | string | -- | `data.next_page_token` from the previous response |

## User Playlists Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sec_user_id` | string | required | From profile or user/region |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `30` | Playlists per page (1-30) |

## Playlist Videos Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `playlist_id` | string | required | Numeric playlist ID (`mixId` from user/playlists) |
| `cursor` | string | `"0"` | Pagination cursor |
| `count` | number | `30` | Videos per page (1-30) |

## Live Status / Account Region Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | required | TikTok handle, with or without the @ |

## Pagination Reference

| Style | Endpoints | Next page | Stop condition |
|---|---|---|---|
| Cursor string | user/posts | `cursor = data.max_cursor` | `data.has_more === 0` |
| Offset number | search/*, hashtag/videos, video/comments, video/comments/replies | `cursor = data.cursor` | `data.has_more === 0` |
| Token + time | user/followers, user/followings | `page_token` + `min_time` | `data.has_more === false` |
| Offset number | search/music, music/videos, music/chart | `cursor = data.cursor` | `data.has_more === 0` |
| Cursor string | user/playlists, playlist/videos | `cursor = data.cursor` | `data.hasMore === false` |
| Page token | user/similar | `page_token = data.next_page_token` | `data.has_more === false` |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
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

# 8. Top 50 sound chart, then the videos using the first sound
chart = requests.post(f"{BASE}/api/v1/tiktok/music/chart", headers=HEADERS,
    json={"chart": "top"}).json()
first = chart["data"]["music_list"][0]["music_info"]
print(first["title"], first["author"], first["user_count"], "videos")

sound_vids = requests.post(f"{BASE}/api/v1/tiktok/music/videos", headers=HEADERS,
    json={"music_id": first["id_str"]}).json()

# 9. Is the creator live right now? liveRoom.status 2 = live, 4 = not live
live = requests.post(f"{BASE}/api/v1/tiktok/user/live", headers=HEADERS,
    json={"username": "mrbeast"}).json()
room = live["data"]["data"]["liveRoom"]
print("live" if room["status"] == 2 else "not live", room["liveRoomStats"]["userCount"], "viewers")

# 10. Registered country plus sec_user_id from a username
region = requests.post(f"{BASE}/api/v1/tiktok/user/region", headers=HEADERS,
    json={"username": "mrbeast"}).json()
print(region["data"]["country"], region["data"]["sec_user_id"])
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

## Sound Detail Response

```json
{
  "data": {
    "music_info": {
      "id": 7364498342501435000,
      "id_str": "7364498342501435408",
      "title": "Espresso",
      "author": "Sabrina Carpenter",
      "album": "Espresso",
      "duration": 60,
      "user_count": 526809,
      "is_original": false,
      "is_commerce_music": true,
      "create_time": 1714681438
    },
    "music_chart_rank": {
      "desc": "Music Charts"
    },
    "status_code": 0,
    "msg": "success"
  },
  "response_time": 1922,
  "credits_used": 1
}
```

Note how numeric `id` lost precision while `id_str` kept it - always read `id_str`.

## Account Region Response

```json
{
  "data": {
    "username": "mrbeast",
    "username_modify_time": 1791756213,
    "user_id": 6614519312189948000,
    "sec_user_id": "MS4wLjABAAAABKjQkOz_IIzXXzEAl_9LGsWhvK-gBnlczwRPXK8EmxAp6K3X0qiaP5_OEqmm0XwG",
    "country": "CA",
    "api_version": "v1"
  },
  "response_time": 1463,
  "credits_used": 1
}
```

## Guardrails

- All TikTok calls cost 1 credit each. Inform the user before paginating through many pages.
- Never fabricate usernames, video captions, follower counts, or comment text. Only return API data.
- Most endpoints require a `sec_user_id`, not a username. Always resolve via the profile endpoint first.
- All `create_time` fields are Unix timestamps in seconds. Multiply by 1000 for JavaScript `Date`.
- Avatar and image fields return an object with a `url_list` array. Use `.url_list[0]` for the URL.
- Do not silently omit any data. Surface all fields so the user can decide what to use.
- The sound, trending, playlist, similar-creator and live endpoints return TikTok's raw JSON. Large numeric ids lose precision when parsed as JSON numbers: read `id_str`, `sec_uid` / `secUid` / `sec_user_id`, never a numeric `id` or `user_id`.
- Trending videos is a sample of about 6-15 per call, not a ranked list; call again for a fresh sample. Trending searches, trending videos and the sound chart are global (no region filter).
- `/tiktok/music/videos` ignores `count` and returns about 14 videos per page.
- `/tiktok/search/suggestions` can return an empty list for long-tail keywords; the call is still billed.
- `/tiktok/user/region` returns the country the account is registered in, not the creator's nationality.
- A user's liked videos, posts by location and Creative Center boards are not offered. Say so rather than improvising.

## Failure handling

- `401` means the API key is invalid or missing. Prompt the user to check their `SCAVIO_API_KEY`.
- `429` means rate limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-scraper-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest different keywords, a broader `publish_time`, or a different `sort_type`.
- `404` from `/tiktok/user/live` means no user has that username; it is billed (1 credit). `404` from `/tiktok/user/region` means the same and is not billed.
- Failed upstream calls (`502`) are never billed.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="tiktok")
```
