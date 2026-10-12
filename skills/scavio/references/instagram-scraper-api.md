# Instagram Scraper API - Profiles, Posts, Reels, Stories, Followers

Read public Instagram data as JSON: profiles, timeline posts, reels, tagged posts, active stories and saved highlights, single-post detail, comment threads, post likers, follower, following and similar-account lists, and search across users, hashtags, Reels, music and locations.

## When to trigger

Use this skill when the user asks to:
- Look up an Instagram profile: follower count, bio, verified status, category
- Pull a creator's recent posts, reels, or the posts they were tagged in
- Read a creator's active stories or the stories saved in their highlights
- Read a specific post: caption, media URLs, like and comment counts
- Mine the comments on a post, the replies under one comment, or who liked a post
- List who follows an account, who it follows, or which accounts are similar to it
- Find accounts, hashtags, Reels, audio tracks or places by keyword
- See which Reels use a given song or sound
- Do influencer vetting, competitor tracking, or creator-discovery research on Instagram

For TikTok creators use `scavio-tiktok`. For TikTok Shop products use `scavio-tiktok-shop`.

## Three things to read before you call anything

**1. Most calls cost 1 or 2 credits. Know which is which before you loop.** `/profile`, `/user/reels`, `/user/tagged` and `/music/posts` typically cost **1 credit**; every other endpoint typically costs **2**. Three exceptions to plan around:

- `/user/reels` and `/user/tagged` cost 2 the first time a given username is looked up, then 1. Sending `user_id` instead of `username` keeps them at 1.
- `/search/users` and `/search/hashtags` cost **8** when you send a `cursor`. Page 1 is 2. Only ask for page 2 when page 1 genuinely was not enough.
- Any request can cost more (never more than **10**) when it needs extra work to answer. `credits_used` in every response is the exact charge, so read it rather than assuming the typical price.

On the free plan's 50 one-time credits that is about 50 profile lookups or 25 post-detail calls. The full table is below.

**2. Post identifiers differ per endpoint.** The post endpoints take different identity sets:

| Endpoint | Accepts | Does NOT accept |
|---|---|---|
| `/post` | `url`, `media_id`, or `shortcode` | -- |
| `/post/comments` | `shortcode` or `url` | `media_id` |
| `/post/likers` | `shortcode` or `url` | `media_id` |
| `/post/comments/replies` | `media_id` + `comment_id` | `shortcode`, `url` |

To get replies, take `media_id` and `pk` from a comment in the `/post/comments` response (every comment carries both) and pass them as `media_id` and `comment_id`. Comments then replies is 2 + 2 = 4 credits.

**3. Responses keep Instagram's own field names, not a normalized Scavio shape.** Unlike Reddit, YouTube or LinkedIn, Instagram responses keep Instagram's structure, and it differs per endpoint (the per-endpoint notes below say where the list lives). Consequences:

- **Field names are Instagram's, not friendly ones.** On `/post`, the video URL is at `video_versions[].url` and the cover image at `image_versions2.candidates[]`. `media_type` is the integer `1` (image), `2` (video), or `8` (carousel).
- **Each endpoint answers in one structure**, but structures differ between endpoints: `/user/posts` lists items at `data.data.items`, `/user/reels` at `data.items`, `/post/comments` at `data.comments`. Read the notes below rather than guessing.

Do not invent friendlier field names when reporting results, and do not claim a field is missing until you have checked the raw keys actually returned.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=instagram-scraper-api) (50 one-time credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=instagram-scraper-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 or 2 credits each, as the table below says.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/instagram`. Credits are the typical cost per call (per page for paginated endpoints); `credits_used` in each response is the exact charge, never more than 10.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/instagram/profile` | **1** | Profile: bio, follower/following/media counts, verified, category |
| `POST /api/v1/instagram/user/posts` | **2** | Timeline posts for a user, about 12 per page |
| `POST /api/v1/instagram/user/reels` | **1** (2 on a username's first lookup) | A user's reels |
| `POST /api/v1/instagram/user/tagged` | **1** (2 on a username's first lookup) | Posts a user was tagged in |
| `POST /api/v1/instagram/user/stories` | **2** | Currently active stories |
| `POST /api/v1/instagram/user/highlights` | **2** | A user's story highlights: id, title, cover, item count |
| `POST /api/v1/instagram/highlight/stories` | **2** | Every story saved in one highlight, with media URLs |
| `POST /api/v1/instagram/post` | **2** | Full detail for one post |
| `POST /api/v1/instagram/post/comments` | **2** | Top-level comments on a post |
| `POST /api/v1/instagram/post/comments/replies` | **2** | Replies under one comment |
| `POST /api/v1/instagram/post/likers` | **2** | Accounts that liked a post (up to about 1,000) and the total like count |
| `POST /api/v1/instagram/user/followers` | **2** | Who follows this account |
| `POST /api/v1/instagram/user/followings` | **2** | Who this account follows |
| `POST /api/v1/instagram/user/similar` | **2** | Accounts similar to this one |
| `POST /api/v1/instagram/search/users` | **2** (8 with a `cursor`) | Find accounts by keyword |
| `POST /api/v1/instagram/search/hashtags` | **2** (8 with a `cursor`) | Find hashtags by keyword |
| `POST /api/v1/instagram/search/reels` | **2** | Find Reels by keyword |
| `POST /api/v1/instagram/search/music` | **2** | Find audio tracks by song or artist |
| `POST /api/v1/instagram/music/posts` | **1** | Reels that use one audio track, plus its total reel count |
| `POST /api/v1/instagram/search/locations` | **2** | Find places by name: id, address, coordinates |

## Workflow

1. **Start from a username.** Every user endpoint accepts `username` (without the `@`). You do not need to resolve an id first, unlike TikTok.
2. **Prefer `user_id` once you have it.** `/profile` returns it as `id` (and `pk`). When both are sent, `user_id` wins and is more stable than a username, which can be changed by its owner. On `/user/reels` and `/user/tagged` it also avoids the 2-credit first lookup.
3. **Cheapest useful path for "what is this creator about":** `/profile` (1 credit) for counts and bio, then `/user/reels` (1) or `/user/posts` (2) for recent content with captions and engagement counts.
4. **Paginate with `cursor`.** Pass the continuation token from the previous response back as `cursor`. Its name depends on the endpoint: `pagination_token` (user posts, Reels search), `next_max_id` (reels, tagged, followers, followings), `next_min_id` (comments), `paging_info.max_id` (music posts). Stop when none is present or `has_more` / `more_available` is false.
5. **Do not rely on `count`.** `/user/posts` returns about 12 items per page whatever `count` says. Read how many items you actually got rather than assuming.

## Parameters

### Identity: `username` vs `user_id`

Nine endpoints take a user identity. Both fields are optional individually but **at least one is required**; omitting both is a 400. `user_id` takes precedence when both are sent. `user_id` is a **string**, even though it looks like a number.

### Profile (`/profile`), stories (`/user/stories`), highlights (`/user/highlights`), similar accounts (`/user/similar`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | Instagram handle without `@` |
| `user_id` | string | -- | Numeric id as a string. Wins over `username` |

No `count`, no `cursor`.

- `/profile` returns the profile **inlined at the root of `data`**: `data.username`, `data.full_name`, `data.follower_count`, `data.following_count`, `data.media_count`, `data.biography`, `data.is_verified`, `data.is_private`, `data.category`, `data.external_url`. There is no `data.user` wrapper.
- `/user/stories` lists live stories at `data.items` (also grouped per user under `data.reels.<user_id>.items`), each with `taken_at`, `expiring_at`, `media_type`, `thumbnail_url` and `video_url`. An account with no active stories returns an empty list, which is a normal result and not an error.
- `/user/highlights` lists highlights at `data.data.items`, each with `id` (for example `highlight:18149897764550869`), `title`, `media_count`, `cover_media` and `created_at`.
- `/user/similar` lists accounts at `data.data.items` with `id`, `username`, `full_name`, `is_verified`, `is_private`. It works for most creator accounts; some brand accounts return none, which is a normal empty result.

### Highlight stories (`/highlight/stories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `highlight_id` | string | required | An `id` from `/user/highlights`, with or without the `highlight:` prefix |

Stories are at `data.data.items`, each with `taken_at`, `media_type`, `image_versions`, and on video items `video_url` and `video_versions`. The highlight's own title is at `data.data.additional_data.title`.

### User posts (`/user/posts`), reels (`/user/reels`), tagged (`/user/tagged`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | Handle without `@` |
| `user_id` | string | -- | Wins over `username` |
| `count` | number | `12` | Items per page, 1-50 (not honored on `/user/posts`) |
| `cursor` | string | -- | Continuation token from the previous response |

- `/user/posts`: items at `data.data.items`, next page token at `data.pagination_token`. Each item carries `code`, `caption.text`, `like_count`, `comment_count`, `taken_at`, `media_type`, `image_versions` and `thumbnail_url`; video items add `video_url`, `video_versions` and `play_count`.
- `/user/reels` and `/user/tagged`: items at `data.items`, next page token at `data.next_max_id`. Each item is compact: `code`, `shortcode`, `media_type`, `is_video`, `like_count`, `comment_count`, `view_count`, `taken_at`, `caption_text`, `thumbnail_url`, `video_url`, `owner`.
- On `/user/tagged`, `video_url` is `null` on video items and `owner.full_name` / `owner.is_verified` are `null`. To get a tagged video's URL, call `/post` with its `code`.

### Followers (`/user/followers`), followings (`/user/followings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | -- | Handle without `@` |
| `user_id` | string | -- | Wins over `username` |
| `count` | number | `12` | Users per page, 1-100 |
| `cursor` | string | -- | Continuation token (`next_max_id`) |

Users are at `data.users`. The path is `followings`, plural. Follower lists on large accounts are effectively bottomless -- Instagram will not hand over millions of rows. Each page is 2 credits; set an explicit page budget with the user before starting, and stop when the continuation token stops coming back.

### Post detail (`/post`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | -- | Full post URL, e.g. `https://www.instagram.com/p/DUajw4YkorV/` |
| `media_id` | string | -- | Numeric media id as a string. **Highest precedence** |
| `shortcode` | string | -- | The code from the URL, e.g. `DUajw4YkorV` |

One of the three is required. The post is at `data.items[0]`. Within it: `media_type` `1`/`2`/`8`, `caption.text`, `like_count`, `comment_count`, `play_count`, `user`, `usertags`, video at `video_versions[].url`, cover at `image_versions2.candidates[]`. For a carousel (`media_type: 8`) the children are under `carousel_media[]` -- walk them rather than expecting one media URL.

### Post comments (`/post/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `shortcode` | string | -- | The code from the post URL |
| `url` | string | -- | Full post URL |
| `cursor` | string | -- | Continuation token (`next_min_id`) |
| `sort_order` | string | `popular` | `popular` or `newest` |

One of `shortcode` / `url` is required. **`media_id` is not accepted here.** Comments are at `data.comments`, each with `pk`, `text`, `user`, `comment_like_count`, `child_comment_count`, `created_at` and `media_id`; `data.comment_count` and `data.has_more_comments` describe the thread.

**Pass a canonical post URL or a bare shortcode only.** A `/share/` link, a profile URL, or any URL that is not of the form `instagram.com/p/<code>`, `/reel/<code>`, `/reels/<code>` or `/tv/<code>` fails. Extract the shortcode yourself and send that instead.

### Comment replies (`/post/comments/replies`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `media_id` | string | required | The post's numeric media id (the `media_id` on any comment) |
| `comment_id` | string | required | The comment's `pk` from `/post/comments` |
| `cursor` | string | -- | Continuation token |

Replies are at `data.child_comments`; the comment they answer is at `data.parent_comment`.

### Post likers (`/post/likers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `shortcode` | string | -- | The code from the post URL |
| `url` | string | -- | Full post URL |

One of the two is required; no cursor. Accounts are at `data.data.items` (`id`, `username`, `full_name`, `is_verified`, `is_private`), up to about 1,000 per post. `data.data.total` is the post's total like count, `data.data.count` how many accounts came back.

### Search users (`/search/users`), search hashtags (`/search/hashtags`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search term, 1-500 chars |
| `cursor` | string | -- | Rank token from a previous response. Makes the call cost 8 |

The field is `keyword`, not `query` or `search`. There is **no `count`**. Users are at `data.users` (`pk`, `username`, `full_name`, `is_verified`); hashtags at `data.hashtags` (`id`, `name`, `media_count`).

### Search Reels (`/search/reels`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Search term |
| `cursor` | string | -- | `pagination_token` from the previous response |

Reels are at `data.data.items`, each with `code`, `caption.text`, `user`, `play_count`, `like_count`, `comment_count`, `taken_at` and `video_versions`. Next page token at `data.pagination_token`; each page is 2 credits.

### Search music (`/search/music`) and music posts (`/music/posts`)

| Endpoint | Parameter | Type | Description |
|---|---|---|---|
| `/search/music` | `keyword` | string, required | Song title or artist |
| `/music/posts` | `music_id` | string, required | The `id` of a track from `/search/music` (numeric) |
| `/music/posts` | `cursor` | string | `paging_info.max_id` from the previous response |

`/search/music` lists tracks at `data.data.items` with `id`, `title`, `display_artist`, `duration_in_ms` and `progressive_download_url`. Pass the track's `id` (not `audio_id`) as `music_id`.

`/music/posts` lists the Reels using that track at `data.items[].media` (`code`, `play_count`, `like_count`, `comment_count`, `video_versions`), with the track's total reel count at `data.media_count.clips_count` and `data.formatted_media_count`. More pages while `data.paging_info.more_available` is true; 1 credit per page.

### Search locations (`/search/locations`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | required | Place name |

Places are at `data.data.items` with `id`, `name`, `address`, `city`, `latitude` and `longitude`.

## Errors

| Status | Meaning | What to do |
|---|---|---|
| 400 | Invalid body. The `details` array names the offending field | Fix and resend. Usually a missing identity field |
| 401 | Bad or missing API key | Check `SCAVIO_API_KEY` |
| 402 | Out of credits | Stop. Tell the user, do not retry |
| 429 | Too many requests in flight at once | Wait for one to finish, then retry. Not a cooldown |
| 500 | Unparseable post URL on `/post/comments` | Send a bare shortcode instead |
| 502 | Instagram data temporarily unavailable | Retry once after a short delay, then give up |

A 402 or 429 means stop, not retry harder. Report the condition to the user rather than burning the remaining balance.

## Credits and spend discipline

Every successful response carries `credits_used` and `credits_remaining` next to `data`. Read `credits_remaining` as you go. To check the balance without spending anything, call `GET /api/v1/usage` (0 credits, no body).

Concurrency is capped per plan -- 1 simultaneous request on free and pay-as-you-go, up to 50 on Growth. Exceeding it returns 429 immediately. Do not fan out parallel Instagram calls unless you know the plan allows it.

Before any multi-call workflow, state the credit cost to the user. "Scanning this account's 500 followers is 2 credits per page of up to 100, so about 10 credits" is the kind of thing to say **before** starting, not after.

## Example

```bash
# 1. Follower count and bio -- 1 credit
curl -X POST 'https://api.scavio.dev/api/v1/instagram/profile' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"username": "nasa"}'

# 2. Recent reels for the same creator -- 1 credit
curl -X POST 'https://api.scavio.dev/api/v1/instagram/user/reels' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"username": "nasa"}'

# 3. Who liked one post, plus the total like count -- 2 credits
curl -X POST 'https://api.scavio.dev/api/v1/instagram/post/likers' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"shortcode": "DeJ28eTxo4s"}'

# 4. Which Reels use a song: find the track, then its Reels -- 2 + 1 credits
curl -X POST 'https://api.scavio.dev/api/v1/instagram/search/music' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "espresso"}'
curl -X POST 'https://api.scavio.dev/api/v1/instagram/music/posts' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"music_id": "1747512212697470"}'

# 5. A creator's highlights, then the stories in one -- 2 + 2 credits
curl -X POST 'https://api.scavio.dev/api/v1/instagram/user/highlights' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"username": "natgeo"}'
curl -X POST 'https://api.scavio.dev/api/v1/instagram/highlight/stories' \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"highlight_id": "highlight:18149897764550869"}'
```

## Related skills

- `scavio-tiktok` -- TikTok creator profiles, videos, comments, hashtags
- `scavio-tiktok-shop` -- TikTok Shop products, prices, reviews
- `scavio-x` -- X (Twitter) posts, users, timelines, trends
- `scavio-linkedin` -- LinkedIn people, companies, jobs, posts
- `scavio-youtube` -- YouTube search, videos, channels, transcripts
