---
name: instagram-scraper-api
description: "Instagram public data: profiles with follower counts and bio, timeline posts, reels, tagged posts, active stories, single-post detail, comments and replies, follower and following lists, and user and hashtag search. 12 endpoints, 2-10 credits each; responses are raw upstream JSON, not a normalized shape."
version: 1.0.0
tags: instagram, instagram-api, instagram-scraper, social-media, profiles, reels, stories, followers, comments, hashtags, influencer-marketing, social-listening, langchain, crewai, autogen, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4F8"
    homepage: https://scavio.dev/docs/instagram-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=instagram-scraper-api
---

# Instagram Scraper API - Profiles, Posts, Reels, Stories, Followers

Read public Instagram data as JSON: profiles, timeline posts, reels, tagged posts, active stories, single-post detail, comment threads, follower and following lists, and user/hashtag search.

## When to trigger

Use this skill when the user asks to:
- Look up an Instagram profile: follower count, bio, verified status, account type
- Pull a creator's recent posts, reels, or the posts they were tagged in
- Read a specific post: caption, media URLs, like and comment counts
- Mine the comments on a post, or the replies under one comment
- List who follows an account, or who it follows
- Find accounts or hashtags by keyword
- Do influencer vetting, competitor tracking, or creator-discovery research on Instagram

For TikTok creators use `scavio-tiktok`. For TikTok Shop products use `scavio-tiktok-shop`.

## Three things to read before you call anything

**1. Instagram is the most expensive family in the API. Budget before you loop.** Costs are per-endpoint and range 2 to 10 credits, unlike Google or Reddit where everything is 1. A profile lookup is **10 credits** — ten times a Google search. On the free plan's 50 one-time credits that is five calls. The full table is below; read it before writing any loop. The cheap endpoint is `/user/posts` at **2 credits** — prefer it, and reach for the 10-credit endpoints only when you genuinely need what they carry.

**2. There is no single post identifier that works everywhere.** The three post endpoints take three different, non-overlapping identity sets:

| Endpoint | Accepts | Does NOT accept |
|---|---|---|
| `/post` | `url`, `media_id`, or `shortcode` | -- |
| `/post/comments` | `shortcode` or `url` | `media_id` |
| `/post/comments/replies` | `media_id` + `comment_id` | `shortcode`, `url` |

So you cannot chain `/post/comments` straight into `/post/comments/replies` — comments are addressed by shortcode, replies by `media_id`. To get replies, call `/instagram/post` first to resolve the `media_id`, then pass it with the `comment_id` from the comments call. That chain costs 8 + 10 + 8 = 26 credits; make sure the user actually wants it.

**3. The response is a raw upstream passthrough, not a normalized Scavio shape.** Unlike Reddit, YouTube or LinkedIn, Instagram responses are handed back exactly as the provider returned them. Two consequences:

- **Field names are Instagram's, not friendly ones.** On a post, the video URL is at `video_versions[].url` — there is **no** `video_url`. The cover image is at `image_versions2.candidates[]` — there is **no** `thumbnail_url`. `media_type` is the integer `1` (image), `2` (video), or `8` (carousel).
- **The top-level keys inside `data` can vary between calls on the same endpoint**, because two upstream versions are raced and either may win. Always probe defensively: check for `items` and for `data`, take whichever is present, and never assume a key exists.

Do not invent friendlier field names when reporting results, and do not claim a field is missing until you have checked the raw keys actually returned.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=instagram-scraper-api) (50 one-time credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/instagram`.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/instagram/user/posts` | **2** | Timeline posts for a user. The cheap one -- start here |
| `POST /api/v1/instagram/post` | **8** | Full detail for one post |
| `POST /api/v1/instagram/post/comments/replies` | **8** | Replies under one comment |
| `POST /api/v1/instagram/profile` | **10** | Profile: bio, counts, verified, account type |
| `POST /api/v1/instagram/user/reels` | **10** | A user's reels |
| `POST /api/v1/instagram/user/tagged` | **10** | Posts a user was tagged in |
| `POST /api/v1/instagram/user/stories` | **10** | Currently active stories |
| `POST /api/v1/instagram/post/comments` | **10** | Top-level comments on a post |
| `POST /api/v1/instagram/user/followers` | **10** | Who follows this account |
| `POST /api/v1/instagram/user/followings` | **10** | Who this account follows |
| `POST /api/v1/instagram/search/users` | **10** | Find accounts by keyword |
| `POST /api/v1/instagram/search/hashtags` | **10** | Find hashtags by keyword |

The 8-vs-10 split is not arbitrary: the 10-credit endpoints race two upstream providers for reliability and are billed for both legs; the 8-credit ones have only a single provider. Nothing here is 1 credit.

## Workflow

1. **Start from a username.** Every user endpoint accepts `username` (without the `@`). You do not need to resolve an id first, unlike TikTok.
2. **Prefer `user_id` once you have it.** Every response that includes a profile carries `pk` / `id` — that is the `user_id`. When both are sent, `user_id` wins and is more stable than a username, which can be changed by its owner.
3. **Cheapest useful path:** `/user/posts` (2 credits) already carries captions, media, like and comment counts for recent posts. For "what is this creator posting about", that single call is often the whole answer.
4. **Add `/profile` (10) only when you need follower counts**, bio text, verified status, or account type. Do not call it reflexively before a feed call.
5. **Paginate with `cursor`.** Pass the continuation token from the previous response back as `cursor`. Names of the continuation field vary by endpoint and by which upstream leg won -- look for `next_max_id`, `pagination_token`, `next_min_id`, or `rank_token` and pass whichever is present. Stop when none is present or `has_more` / `more_available` is false.
6. **Raise `count` instead of making more calls.** Each call costs the same regardless of page size, so a single `count: 50` is five times cheaper than five `count: 10` calls.

## Parameters

### Identity: `username` vs `user_id`

Nine endpoints take a user identity. Both fields are optional individually but **at least one is required**; omitting both is a 400. `user_id` takes precedence when both are sent. `user_id` is a **string**, even though it looks like a number.

### Profile (`/profile`), Stories (`/user/stories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | Instagram handle without `@` |
| `user_id` | string | -- | Numeric id as a string. Wins over `username` |

No `count`, no `cursor`. Stories are not paginated -- you get whatever is currently live, and an account with no active stories returns an empty set, which is a normal result and not an error.

`/profile` returns the profile object **inlined at the root of `data`** -- there is no `data.user` wrapper. Read `data.follower_count`, not `data.user.follower_count`.

### User posts (`/user/posts`), reels (`/user/reels`), tagged (`/user/tagged`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | Handle without `@` |
| `user_id` | string | -- | Wins over `username` |
| `count` | number | `12` | Items per page, 1-50 |
| `cursor` | string | -- | Continuation token from the previous response |

Note on `/user/posts`: `count` is honored only when the newer upstream leg answers, and the older leg is the primary one here. Treat `count` as a request, not a guarantee, and read how many items you actually got rather than assuming.

Also on `/user/posts`: when you pass **only** `user_id`, the items may arrive **double-nested at `data.data`** rather than `data.items`. Probe both.

### Followers (`/user/followers`), followings (`/user/followings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | Handle without `@` |
| `user_id` | string | -- | Wins over `username` |
| `count` | number | `12` | Users per page, 1-**100** (the highest cap in the family) |
| `cursor` | string | -- | Continuation token |

The path is `followings`, plural. Follower lists on large accounts are effectively bottomless -- Instagram will not hand over millions of rows, and each page is 10 credits. Set an explicit page budget with the user before starting, and stop when the continuation token stops coming back.

### Post detail (`/post`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | -- | Full post URL, e.g. `https://www.instagram.com/p/DUajw4YkorV/` |
| `media_id` | string | -- | Numeric media id as a string. **Highest precedence** |
| `shortcode` | string | -- | The code from the URL, e.g. `DUajw4YkorV` |

One of the three is required. `media_id` wins over everything; `shortcode` is expanded into a URL internally.

The post is at `data.items[0]`. Within it: `media_type` `1`/`2`/`8`, video at `video_versions[].url`, cover at `image_versions2.candidates[]`. For a carousel (`media_type: 8`) the children are nested inside the item -- walk them rather than expecting one media URL.

### Post comments (`/post/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `shortcode` | string | -- | The code from the post URL |
| `url` | string | -- | Full post URL |
| `cursor` | string | -- | Continuation token |
| `sort_order` | string | `popular` | `popular` or `newest` |

One of `shortcode` / `url` is required. **`media_id` is not accepted here** even though the sibling endpoints take it.

Two cautions. First, `sort_order` is honored only when the newer upstream leg answers; if the older leg wins, your sort is silently ignored. Do not present comment ordering to the user as guaranteed. Second, **pass a canonical post URL or a bare shortcode only.** A `/share/` link, a profile URL, or any URL that is not of the form `instagram.com/p/<code>`, `/reel/<code>`, `/reels/<code>` or `/tv/<code>` currently fails as a **500**, not a clean 400. Extract the shortcode yourself and send that instead.

### Comment replies (`/post/comments/replies`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `media_id` | string | required | The post's numeric media id, as a string |
| `comment_id` | string | required | From a comment in the `/post/comments` response |
| `cursor` | string | -- | Continuation token |

Both ids are required. `/post/comments` does not return `media_id`, so resolve it with `/instagram/post` first. See caution 2 at the top.

### Search users (`/search/users`), search hashtags (`/search/hashtags`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search term, 1-500 chars |
| `cursor` | string | -- | Rank token from a previous response |

The field is `keyword`, not `query` or `search`. There is **no `count`** -- page size is not controllable. Pagination is best-effort: if the older upstream leg answers, the cursor is ignored and you get page 1 again. Detect this by comparing the returned ids to what you already have rather than assuming forward progress.

## Errors

| Status | Meaning | What to do |
|---|---|---|
| 400 | Invalid body. The `details` array names the offending field | Fix and resend. Usually a missing identity field |
| 401 | Bad or missing API key | Check `SCAVIO_API_KEY` |
| 402 | Out of credits | Stop. Tell the user, do not retry |
| 429 | Too many requests in flight at once | Wait for one to finish, then retry. Not a cooldown |
| 500 | Unparseable post URL on `/post/comments` | Send a bare shortcode instead |
| 502 | Upstream Instagram data temporarily unavailable | Retry once after a short delay, then give up |

A 402 or 429 means stop, not retry harder. Report the condition to the user rather than burning the remaining balance.

## Credits and spend discipline

Every successful response carries `credits_used` and `credits_remaining` next to `data`. Read `credits_remaining` as you go. To check the balance without spending anything, call `GET /api/v1/usage` (0 credits, no body).

Concurrency is capped per plan -- 1 simultaneous request on free and pay-as-you-go, up to 50 on Growth. Exceeding it returns 429 immediately. Do not fan out parallel Instagram calls unless you know the plan allows it.

Before any multi-call workflow, state the credit cost to the user. "Scanning this account's 500 followers is 10 credits per page of up to 100, so about 50 credits" is the kind of thing to say **before** starting, not after.

## Example

```bash
# 1. Recent posts for a creator -- 2 credits, usually enough on its own
curl -X POST 'https://api.scavio.dev/api/v1/instagram/user/posts' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"username": "instagram", "count": 24}'

# 2. Follower count and bio -- 10 credits, only when actually needed
curl -X POST 'https://api.scavio.dev/api/v1/instagram/profile' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"username": "instagram"}'

# 3. One post in full -- 8 credits
curl -X POST 'https://api.scavio.dev/api/v1/instagram/post' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"shortcode": "DUajw4YkorV"}'
```

## Related skills

- `scavio-tiktok` -- TikTok creator profiles, videos, comments, hashtags
- `scavio-tiktok-shop` -- TikTok Shop products, prices, reviews
- `scavio-x` -- X (Twitter) posts, users, timelines, trends
- `scavio-linkedin` -- LinkedIn people, companies, jobs, posts
- `scavio-youtube` -- YouTube search, videos, channels, transcripts
