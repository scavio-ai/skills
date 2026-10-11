# Reddit Search API - Posts, Comments, Subreddits, Users

Search Reddit posts, comments and subreddits, read a post with its threaded comment tree, expand comment replies, and pull subreddit metadata and feeds, redditor profiles with their posts and comments, the site-wide popular feed, and trending search queries. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search Reddit for opinions, discussions, or public sentiment on a topic
- Search Reddit comments (not just posts) for a keyword, tool or brand mention
- Find subreddits about a topic, with subscriber counts
- Fetch the full text and comments of a Reddit post by id or URL
- Expand the reply tree under a specific comment
- Look up a subreddit's metadata or browse its post feed
- Look up a redditor and read their submitted posts or comments
- Browse the site-wide popular feed or current trending searches
- Research how developers or communities talk about a product, library, or issue
- Build RAG pipelines that need discussion-sourced context
- Monitor brand or competitor mentions across Reddit

Note: Reddit requests take 5-15 seconds. Set a client timeout of at least 30 seconds.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=reddit-search-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=reddit-search-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/reddit`. Every endpoint costs **1 credit**.

| Endpoint | Credits | Description |
|---|---|---|
| `POST /api/v1/reddit/search` | 1 | Search Reddit posts by query |
| `POST /api/v1/reddit/search/comments` | 1 | Search Reddit comments by query |
| `POST /api/v1/reddit/search/subreddits` | 1 | Search subreddits by query |
| `POST /api/v1/reddit/search/suggestions` | 1 | Autocomplete suggestions for a query |
| `POST /api/v1/reddit/post` | 1 | Full details for a single post |
| `POST /api/v1/reddit/post/comments` | 1 | Top-level comments for a post |
| `POST /api/v1/reddit/post/comments/replies` | 1 | Replies to a specific comment |
| `POST /api/v1/reddit/subreddit` | 1 | Metadata for a subreddit |
| `POST /api/v1/reddit/subreddit/posts` | 1 | A subreddit's post feed |
| `POST /api/v1/reddit/user` | 1 | A redditor's profile |
| `POST /api/v1/reddit/user/posts` | 1 | A redditor's submitted posts |
| `POST /api/v1/reddit/user/comments` | 1 | A redditor's comments |
| `POST /api/v1/reddit/popular` | 1 | The site-wide popular feed |
| `POST /api/v1/reddit/trending` | 1 | Current trending search queries |

## Workflow

1. **Find discussions:** call `/reddit/search` with `query`. Read `results[].post_id`.
2. **Comments and communities:** call `/reddit/search/comments` with `query` (optional `sort`) to find comments, each with its post and subreddit; call `/reddit/search/subreddits` with `query` to find communities, then pass a `name` to `/reddit/subreddit` or `/reddit/subreddit/posts`.
   **Autocomplete:** call `/reddit/search/suggestions` with `query` for typeahead strings.
3. **Read a post:** call `/reddit/post` with `post_id` (a `t3_...` fullname or bare id) or a full Reddit `url`.
4. **Comments:** call `/reddit/post/comments` with `post_id`. Each comment carries a `reply_cursor`; pass it to `/reddit/post/comments/replies` as `cursor` (with the same `post_id`) to expand that thread.
5. **Subreddits:** call `/reddit/subreddit` for metadata, `/reddit/subreddit/posts` for the feed.
6. **Redditors:** call `/reddit/user` for the profile, `/reddit/user/posts` and `/reddit/user/comments` for their activity.
7. **Discovery:** call `/reddit/popular` for the front-page feed and `/reddit/trending` for trending search queries.

Paginated endpoints return `next_cursor`; pass it back as `cursor` for the next page. Stop when `next_cursor` is `null`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Comment search (`/search/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `sort` | string | `RELEVANCE` | `RELEVANCE`, `HOT`, `TOP` or `NEW` |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Subreddit search (`/search/subreddits`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Search suggestions (`/search/suggestions`)

`query`* (1-500 chars).

### Post (`/post`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `post_id` | string | one of | Post fullname (`t3_...`) or bare id |
| `url` | string | one of | Full Reddit post URL |

Provide `post_id` or `url` (at least one is required).

### Post comments (`/post/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `post_id` | string | required | Post fullname (`t3_...`) |
| `sort` | string | `TOP` | `HOT`, `NEW`, `TOP`, `BEST`, `CONTROVERSIAL` |
| `cursor` | string | -- | Pagination cursor from a prior `next_cursor` |

### Comment replies (`/post/comments/replies`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `post_id` | string | required | Post fullname (`t3_...`) |
| `cursor` | string | required | A comment's `reply_cursor` from the comments endpoint |
| `sort` | string | `TOP` | `HOT`, `NEW`, `TOP`, `BEST`, `CONTROVERSIAL` |

### Subreddit (`/subreddit`)

`subreddit`* — a subreddit name (1-100 chars), e.g. `AskReddit`.

### Subreddit posts (`/subreddit/posts`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `subreddit` | string | required | Subreddit name |
| `sort` | string | `HOT` | `BEST`, `HOT`, `NEW`, `TOP`, `CONTROVERSIAL`, `RISING` |
| `cursor` | string | -- | Pagination cursor |

### User (`/user`)

`username`* — a redditor username (1-100 chars), without `u/`.

### User posts / comments (`/user/posts`, `/user/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | required | Redditor username |
| `sort` | string | `NEW` | `HOT`, `NEW`, `TOP`, `BEST`, `CONTROVERSIAL` |
| `cursor` | string | -- | Pagination cursor |

### Popular (`/popular`)

`cursor` (optional) — pagination cursor.

### Trending (`/trending`)

No parameters.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Search Reddit
results = requests.post(f"{BASE}/api/v1/reddit/search", headers=HEADERS,
    json={"query": "serpapi alternative"}).json()

post_id = results["data"]["results"][0]["post_id"]

# 2. Full post detail
post = requests.post(f"{BASE}/api/v1/reddit/post", headers=HEADERS,
    json={"post_id": post_id}).json()

# 3. Top comments, then expand one thread
comments = requests.post(f"{BASE}/api/v1/reddit/post/comments", headers=HEADERS,
    json={"post_id": post_id, "sort": "TOP"}).json()

reply_cursor = comments["data"]["comments"][0]["reply_cursor"]
replies = requests.post(f"{BASE}/api/v1/reddit/post/comments/replies", headers=HEADERS,
    json={"post_id": post_id, "cursor": reply_cursor}).json()

# 4. Subreddit feed
feed = requests.post(f"{BASE}/api/v1/reddit/subreddit/posts", headers=HEADERS,
    json={"subreddit": "Python", "sort": "TOP"}).json()

# 5. Comment search, newest first - each hit carries its post and subreddit
hits = requests.post(f"{BASE}/api/v1/reddit/search/comments", headers=HEADERS,
    json={"query": "web scraping api", "sort": "NEW"}).json()
for c in hits["data"]["results"]:
    print(c["subreddit"], c["score"], c["post"]["title"], c["permalink"])

# 6. Find communities on a topic
subs = requests.post(f"{BASE}/api/v1/reddit/search/subreddits", headers=HEADERS,
    json={"query": "web scraping"}).json()
for s in subs["data"]["results"]:
    print(s["prefixed_name"], s["subscribers"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields per endpoint:

- **search** — `results[]` (`post_id`, `title`, `url`, `text`, `subreddit`, `author`, `score`, `num_comments`, `created_at`, `is_nsfw`), `next_cursor`.
- **search/comments** — `results[]` (`comment_id`, `text`, `author`, `score`, `created_at`, `edited_at`, `is_op`, `permalink`, `subreddit`, `post{post_id,title,url,permalink,author,score,num_comments,created_at,is_nsfw}`), `next_cursor`, `has_more`.
- **search/subreddits** — `results[]` (`id`, `name`, `prefixed_name`, `public_description`, `subscribers`, `is_nsfw`, `is_quarantined`, `icon`, `url`), `next_cursor`, `has_more`.
- **search/suggestions** — `suggestions[]` (strings).
- **post** — `post_id`, `title`, `text`, `url`, `subreddit`, `author`, `score`, `upvote_ratio`, `num_comments`, `created_at`, `is_nsfw`, `is_video`, `thumbnail`, `media`.
- **post/comments** — `comments[]` (`comment_id`, `text`, `author`, `score`, `created_at`, `reply_cursor`), `next_cursor`.
- **post/comments/replies** — `replies[]` (same item shape as a comment), `next_cursor`.
- **subreddit** — `id`, `name`, `title`, `description`, `subscribers`, `type`, `is_nsfw`, `icon`, `banner`, `created_at`, `primary_color`.
- **subreddit/posts** — `posts[]` (`post_id`, `title`, `url`, `subreddit`, `author`, `score`, `num_comments`, `created_at`, `is_nsfw`), `next_cursor`.
- **user** — `id`, `name`, `is_employee`, `is_verified`, `account_type`, `is_accepting_pms`.
- **user/posts** — `posts[]` (same item shape as a feed post), `next_cursor`.
- **user/comments** — `comments[]` (`comment_id`, `text`, `author`, `post{id,title}`, `score`, `created_at`), `next_cursor`.
- **popular** — `posts[]` (`post_id`, `title`, `subreddit`, `author`, `score`, `num_comments`, `url`, `created_at`), `next_cursor`.
- **trending** — `trending[]` (`query`, `raw_query`).

```json
{
  "data": {
    "results": [
      {
        "post_id": "t3_1v6ngaf",
        "title": "Best SerpAPI alternative for an agent pipeline in 2026?",
        "url": "https://www.reddit.com/r/webscraping/comments/1v6ngaf/best_serpapi_alternative/",
        "text": "We outgrew our current provider and need something cheaper...",
        "subreddit": "webscraping",
        "author": "data_plumber",
        "score": 128,
        "num_comments": 43,
        "created_at": "2026-05-11T14:22:07+0000",
        "is_nsfw": false
      }
    ],
    "next_cursor": "eyJjYW5kaWRhdGVzX3JldH..."
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- Every Reddit endpoint costs **1 credit** (this changed from 2 in an earlier version — all Reddit calls are now 1 credit each).
- Never fabricate post titles, authors, scores, or comment content. Only return API data.
- Requests take 5-15 seconds. If the user's UX is time-sensitive, recommend async or streaming patterns.
- Do not filter out NSFW posts silently — surface the `is_nsfw` flag so the user can decide.
- When summarizing comment threads, preserve the author attribution.
- To expand a comment thread, the replies endpoint needs both the `post_id` and that comment's `reply_cursor` (passed as `cursor`).
- Search pagination moves forward: pass `next_cursor` back as `cursor` and each page returns new results (about 10 per page for comment and subreddit search).

## Failure handling

- `400` means an invalid or missing parameter (e.g. no `post_id`/`url`) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=reddit-search-api).
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If search returns no results, suggest different keywords.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio==4.0.2
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="reddit")
```
