---
name: twitch-api
description: Pull a Twitch channel's profile and live status, list its VODs / highlights / uploads, read its stream schedule, and resolve a clip to downloadable MP4 qualities. 4 endpoints, 1 credit each, structured JSON.
version: 1.0.0
tags: twitch, twitch-api, streaming, live-stream, creator-data, vod, clips, channel-data, stream-schedule, gaming, influencer-data, video-download, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3AE"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitch-api
---

# Twitch API - Profiles, VODs, Clips, Schedule

Pull a Twitch channel's profile and live status, list its videos, read its stream schedule, and resolve a clip to its downloadable MP4 qualities. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Look up a Twitch channel's profile, follower count and whether it is live right now
- List a channel's VODs (past broadcasts), highlights or uploads, sorted by time or views
- Read a channel's upcoming stream schedule
- Resolve a Twitch clip to its metadata and directly-downloadable MP4 qualities
- Do creator research, live-status monitoring or clip archival on Twitch

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitch-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=twitch-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Twitch endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/twitch/profile` | 1 | A channel's profile, follower count, live status and current stream |
| `POST /api/v1/twitch/user/videos` | 1 | A channel's VODs / highlights / uploads, paginated and sortable |
| `POST /api/v1/twitch/user/schedule` | 1 | A channel's stream schedule segments (`null` when the channel has none) |
| `POST /api/v1/twitch/clip` | 1 | A single clip's metadata and directly-downloadable MP4 qualities |

## Parameters

### Profile (`/profile`) and Schedule (`/user/schedule`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `handle` | string | required | Username, `@handle`, or a `twitch.tv/<user>` URL |

### User Videos (`/user/videos`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `handle` | string | required | Username, `@handle`, or a `twitch.tv/<user>` URL |
| `type` | string | `ARCHIVE` | `ARCHIVE` (past broadcasts), `HIGHLIGHT`, `UPLOAD`, `PAST_PREMIERE` |
| `sort_by` | string | `TIME` | `TIME` (newest first) or `VIEWS` |
| `first` | integer | `30` | Videos per page, 1-100 |
| `cursor` | string | -- | Pagination cursor from a previous response (see the note below) |

### Clip (`/clip`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `clip` | string | required | Clip slug or clip URL (`clips.twitch.tv/<slug>` or `twitch.tv/<channel>/clip/<slug>`) |

## Video pagination

Twitch does not allow anonymous pagination past the first page of videos. The first page (up to 100 with `first`) covers any channel with 100 or fewer videos of the requested type. If you need more than the first page, request a larger `first` (up to 100) rather than passing `cursor` - a `cursor` past page 1 returns a `422` telling you exactly this.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Is the channel live, and how many followers?
profile = requests.post(f"{BASE}/api/v1/twitch/profile", headers=HEADERS,
    json={"handle": "shroud"}).json()

# 2. The channel's 100 most-viewed highlights
videos = requests.post(f"{BASE}/api/v1/twitch/user/videos", headers=HEADERS,
    json={"handle": "shroud", "type": "HIGHLIGHT", "sort_by": "VIEWS",
          "first": 100}).json()

# 3. Resolve a clip to downloadable MP4 qualities
clip = requests.post(f"{BASE}/api/v1/twitch/clip", headers=HEADERS,
    json={"clip": "DeliciousDelightfulPicklesWOOP"}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/twitch/profile \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handle":"pokimane"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the profile / `videos[]` / `schedule` / clip payload described above.

## Guardrails

- Every Twitch call is **1 credit**. A `400` (bad input) and a `404` (unknown channel or clip) cost nothing - only a fully-served response is billed.
- To read more than the first page of videos, raise `first` (up to 100); do not page with `cursor`, which is gated past page 1 and returns a `422`.
- A channel with no schedule returns `schedule: null` - that is a valid answer, not an error.
- Clip MP4 URLs are directly downloadable but signed with a short expiry; use them promptly.
- Never fabricate follower counts, video titles, view counts or clip URLs. Only return what the API returned.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the channel or clip does not exist.
- `422` means you asked for video pagination past the first page - raise `first` instead of using `cursor`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitch-api).
- `502` means the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
