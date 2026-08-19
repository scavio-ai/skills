---
name: youtube-data-api
description: "YouTube data API: search videos, Shorts and channels, then pull video metadata, comments and replies, transcripts, related videos, download streams, and channel info, videos and community posts. Returns title, view count, duration, published time, channel and caption fields as JSON. 15 endpoints, 1-8 credits each."
version: 3.0.0
tags: youtube, youtube-api, youtube-data-api, video-search, transcripts, captions, comments, channels, shorts, video-metadata, content-research, rag, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "▶"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=youtube-data-api
---

# YouTube Data API - Search, Videos, Comments, Transcripts, Channels

Search YouTube and retrieve videos, shorts, search suggestions, video metadata, comments, transcripts, related videos, download streams, and full channel data (info, videos, shorts, community posts). All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find YouTube videos, shorts, or channels on a topic
- Get a video's metadata, view count, duration, or captions list
- Read a video's comments and comment replies
- Pull a full transcript or timed subtitles for a video
- Get related videos or direct download stream URLs
- Look up a channel's info, videos, shorts, or community posts
- Resolve a channel handle or URL to a channel ID

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=youtube-data-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/youtube`.

### Video endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/youtube/search` | 2 | Search videos (and channels/playlists) |
| `POST /api/v1/youtube/shorts` | 2 | Search Shorts |
| `POST /api/v1/youtube/suggestions` | 1 | Search autocomplete suggestions |
| `POST /api/v1/youtube/video` | 1 | Full video metadata and captions list |
| `POST /api/v1/youtube/comments` | 1 | Top-level comments for a video |
| `POST /api/v1/youtube/comments/replies` | 1 | Replies to a specific comment |
| `POST /api/v1/youtube/transcript` | 8 | Full transcript or timed subtitles |
| `POST /api/v1/youtube/related` | 1 | Videos related to a video |
| `POST /api/v1/youtube/streams` | 3 | Direct playable/downloadable stream URLs |

### Channel endpoints

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/youtube/channel/search` | 1 | Search channels |
| `POST /api/v1/youtube/channel` | 1 | Full channel info |
| `POST /api/v1/youtube/channel/videos` | 1 | A channel's videos |
| `POST /api/v1/youtube/channel/shorts` | 1 | A channel's Shorts |
| `POST /api/v1/youtube/channel/community` | 1 | A channel's community posts |
| `POST /api/v1/youtube/channel/resolve` | 1 | Resolve a handle or URL to a channel ID |

> `POST /api/v1/youtube/metadata` still works as a **deprecated alias** of `/video`. Use `/video` for new code.

## Workflow

1. **Find a video:** call `/search` with `search`. Use `sort_by: view_count` for the most-watched result. Read `results[].video_id`.
2. **Get metadata:** call `/video` with `video_id` (accepts a full watch URL too) for description, `length_seconds`, `view_count`, `keywords`, and `captions[]`.
3. **Read discussion:** call `/comments`, then `/comments/replies` with a comment's `reply_cursor` to expand a thread.
4. **Get the text:** call `/transcript` for a plain transcript (`format: text`) or timed subtitles (`format: srt`).
5. **Download:** call `/streams` for direct format URLs.
6. **Channels:** resolve a handle with `/channel/resolve`, then call `/channel`, `/channel/videos`, `/channel/shorts`, or `/channel/community`.

Paginated endpoints return `next_cursor` and `has_more`; pass `next_cursor` back as `cursor` for the next page.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | string | required | Search query — note: this field is `search`, not `query` |
| `upload_date` | string | -- | `last_hour`, `today`, `this_week`, `this_month`, `this_year` |
| `type` | string | -- | `video`, `channel`, `playlist`, or `movie` |
| `duration` | string | -- | `short`, `medium`, `long` |
| `sort_by` | string | `relevance` | `relevance`, `date`, `view_count`, `rating` |
| `features` | string[] | -- | Any of `hd`, `4k`, `subtitles`, `creative_commons`, `live`, `360`, `3d`, `hdr`, `vr180` |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

Legacy boolean flags (`subtitles`, `creative_commons`, `hd`, `4k`, `live`, `360`, `3d`, `hdr`, `vr180`) are still accepted for backward compatibility; prefer the `features` array.

### Shorts (`/shorts`)

`search`* , `sort_by`, `cursor`.

### Suggestions (`/suggestions`)

`search`* , `language` (default `en`), `region` (default `US`).

### Video (`/video`) and metadata alias

`video_id`* — accepts a raw ID or a full watch URL.

### Comments (`/comments`)

`video_id`* , `cursor`.

### Comment replies (`/comments/replies`)

`video_id`* , `reply_cursor`* (a comment's `reply_cursor`), `cursor`.

### Transcript (`/transcript`)

`video_id`* , `language` (default `en`), `format` (`text` for plain, `srt` for timed; default `text`).

### Related (`/related`)

`video_id`* , `cursor`.

### Streams (`/streams`)

`video_id`* .

### Channel search (`/channel/search`)

`search`* , `cursor`.

### Channel (`/channel`)

`channel_id`* — accepts a channel ID, `@handle`, or channel URL.

### Channel videos / shorts / community

`channel_id`* , `cursor`.

### Channel resolve (`/channel/resolve`)

`channel`* — a `@handle` or channel URL. Returns `channel_id` and `channel_url`.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=youtube-data-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search — use "search" field, not "query"
search = requests.post(f"{BASE}/api/v1/youtube/search", headers=HEADERS,
    json={"search": "langchain tutorial", "type": "video", "sort_by": "view_count"}).json()

video_id = search["data"]["results"][0]["video_id"]

# 2. Full video metadata (captions list included)
video = requests.post(f"{BASE}/api/v1/youtube/video", headers=HEADERS,
    json={"video_id": video_id}).json()

# 3. Transcript as plain text
transcript = requests.post(f"{BASE}/api/v1/youtube/transcript", headers=HEADERS,
    json={"video_id": video_id, "language": "en", "format": "text"}).json()

# 4. Resolve a handle, then pull the channel's videos
resolved = requests.post(f"{BASE}/api/v1/youtube/channel/resolve", headers=HEADERS,
    json={"channel": "@freecodecamp"}).json()
channel_id = resolved["data"]["channel_id"]

videos = requests.post(f"{BASE}/api/v1/youtube/channel/videos", headers=HEADERS,
    json={"channel_id": channel_id}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields per endpoint:

- **search** — `results[]` (`type`, `video_id`, `title`, `url`, `description_snippet`, `thumbnail`, `duration_text`, `view_count`, `published_time`, `channel{id,name,url}`), plus `shorts`, `channels`, `playlists`, `next_cursor`, `has_more`.
- **shorts** — `results[]` (`video_id`, `title`, `url`, `thumbnail`, `view_count`, `published_time`, `author`, `channel_id`), `next_cursor`, `has_more`.
- **suggestions** — `suggestions[]` (strings), `total_count`.
- **video** — `video_id`, `title`, `author`, `channel_id`, `channel_url`, `published_at`, `description`, `length_seconds`, `view_count`, `keywords[]`, `thumbnail`, `playability_status`, `chapters`, `captions[]` (`language_code`, `language_name`, `url`).
- **comments** — `comments[]` (`comment_id`, `text`, `like_count`, `reply_count`, `published_time`, `reply_cursor`, `author{channel_id,name,url,avatar,is_verified,is_creator}`), `next_cursor`, `has_more`.
- **comments/replies** — `replies[]` (same item shape as a comment), `next_cursor`, `has_more`.
- **transcript** — `video_id`, `language_code`, `language_name`, `format`, `content`.
- **related** — `results[]` (`video_id`, `title`, `url`, `author`, `channel_id`, `channel_url`, `thumbnail`, `view_count`, `published_time`, `length_seconds`), `total_count`.
- **channel/search** — `results[]` (`channel_id`, `name`, `handle`, `url`, `thumbnail`, `subscriber_count`, `description`, `verified`), `next_cursor`, `has_more`, `total_count`.
- **channel** — `channel_id`, `title`, `description`, `handle`, `url`, `subscriber_count`, `video_count`, `view_count`, `country`, `creation_date`, `verified`, `has_business_email`, `avatar`, `banner`, `links[]`.
- **channel/videos** — `channel_id`, `results[]` (`video_id`, `title`, `url`, `thumbnail`, `duration_text`, `view_count`, `published_time`, `is_live`), `next_cursor`, `has_more`.
- **channel/shorts** — `channel_id`, `results[]` (`video_id`, `title`, `url`, `thumbnail`, `view_count`), `next_cursor`, `has_more`, `total_count`.
- **channel/community** — `channel_id`, `posts[]` (`post_id`, `url`, `text`, `author_name`, `author_channel_id`, `published_time`, `vote_count`, `comment_count`, `images[]`, `attachment_type`), `next_cursor`, `has_more`.
- **channel/resolve** — `channel_id`, `channel_url`.
- **streams** — `video_id`, `title`, `author`, `length_seconds`, `view_count`, `is_live`, `formats[]`, `adaptive_formats[]`, `available_qualities[]`, `expires_in_seconds`.

```json
{
  "data": {
    "results": [
      {
        "type": "video",
        "video_id": "sVcwVQRHIc8",
        "title": "Learn RAG From Scratch - Python AI Tutorial",
        "url": "https://www.youtube.com/watch?v=sVcwVQRHIc8",
        "duration_text": "2:33:11",
        "view_count": 1258310,
        "published_time": "1 year ago",
        "thumbnail": "https://i.ytimg.com/vi/sVcwVQRHIc8/hq720.jpg",
        "channel": { "id": "UC8butISFwT-Wl7EV0hUK0BQ", "name": "freeCodeCamp.org", "url": "https://www.youtube.com/@freecodecamp" }
      }
    ],
    "next_cursor": "EpMD...",
    "has_more": true
  },
  "credits_used": 2,
  "credits_remaining": 998
}
```

## Guardrails

- The search parameter is `search`, not `query` — this is different from other Scavio endpoints.
- Credits are not uniform: `search` and `shorts` cost 2, `streams` costs 3, `transcript` costs 8, and every other endpoint costs 1. Inform the user before paginating through many pages, especially transcripts.
- `/metadata` is a deprecated alias of `/video`; use `/video` in new code.
- Stream URLs from `/streams` expire (`expires_in_seconds`) — use them promptly.
- Never fabricate video IDs, view counts, transcripts, comments, or channel data. Only return API data.

## Failure handling

- `400` means an invalid parameter (e.g. a missing `video_id` or `channel_id`) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=youtube-data-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest different keywords or relaxing filters.
- If a transcript is unavailable in the requested `language`, retry with `language: en` or check `/video` `captions[]` for available languages.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="youtube")
```
