---
name: linkedin-scraper-api
description: LinkedIn person and company profiles, their posts, job search by keyword and location, single job detail, and post comments as structured JSON. 9 endpoints from 1 to 30 credits, four of them paginated. People search and contact info were retired upstream and return 410, so they are not covered.
version: 2.1.0
tags: linkedin, linkedin-api, linkedin-scraper, b2b, profiles, company-data, jobs, job-search, lead-generation, prospecting, recruiting, sales-intelligence, langchain, crewai, autogen, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4BC"
    homepage: https://scavio.dev/docs/linkedin-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-scraper-api
---

# LinkedIn Scraper API - Person and Company Profiles, Posts, Jobs

Look up LinkedIn people and companies, read their posts, search job listings, and read a single job or post with its comments. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Look up a LinkedIn member's profile, about section, or recent posts
- See what a member engages with rather than what they publish - the posts they commented on or reacted to
- Look up a company profile or its recent posts
- Search for job listings by keyword and location
- Read a single job listing, or a single post with its comments
- Build B2B prospecting, recruiting, or market-research pipelines

Note: LinkedIn upstream can be slow. Set a client timeout of at least 60 seconds and be ready to retry.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=linkedin-scraper-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/linkedin`. Cost is **not** uniform - check the table before planning a run.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/linkedin/person` | 1 | Full profile: about, experience, education, links |
| `POST /api/v1/linkedin/person/about` | 1 | Just the narrative sections of a profile |
| `POST /api/v1/linkedin/person/posts` | 10 per page | A member's posts, or the posts they commented on or reacted to. 50 per page, paginated |
| `POST /api/v1/linkedin/company` | 1 | Company profile, locations, related companies |
| `POST /api/v1/linkedin/company/posts` | 10 per page | A company's posts, 50 per page, paginated |
| `POST /api/v1/linkedin/search/jobs` | 10 per page | Job listings by keyword and location, 25 per page, paginated |
| `POST /api/v1/linkedin/job` | 30 | Full detail for one job listing |
| `POST /api/v1/linkedin/post` | 1 | Full detail for one post |
| `POST /api/v1/linkedin/post/comments` | 10 per page | Comments on a post, paginated by page number |

`/job` is by far the most expensive call here. Job search already returns title, company, location, posted time, workplace type and salary for every hit, so only call `/job` for listings the user has actually picked out - never in a loop over search results.

**Every reference param also accepts a full LinkedIn URL.** `{"username": "williamhgates"}` and `{"url": "https://www.linkedin.com/in/williamhgates/"}` are equivalent, and the same holds for `company`, `job_id` and `post_id`.

### Retired endpoints

The upstream data provider withdrew five datasets. These paths still exist but always return HTTP **410** with `{"code": "endpoint_retired", "reason": ...}` and are **never billed**. Do not retry them, and never describe the data as temporarily unavailable - it is gone.

| Retired | Closest substitute |
|---|---|
| `/person/contact` | None. Public contact info is no longer available. |
| `/company/people` | `/company` returns `featured_employees`, a sample of 4-6 staff. |
| `/company/jobs` | `/search/jobs` with the company name as `search`. |
| `/search/people` | None. |
| `/search/posts` | None. |

## Workflow

1. **A person:** call `/linkedin/person` with `username` (the vanity handle) or `url`. Use `/linkedin/person/about` when you only need the narrative sections, and `/linkedin/person/posts` for their feed - `type` selects whether that feed is their own posts, the posts they commented on, or the posts they reacted to.
2. **A company:** call `/linkedin/company` with `company` (a slug like `microsoft`) or `url`. Use `/linkedin/company/posts` for its feed.
3. **Jobs:** `/linkedin/search/jobs` with a `search` keyword and optional `location`, then `/linkedin/job` with a `job_id` from the results for full detail.
4. **Posts:** `/linkedin/post` with a `post_id` (bare id or activity urn), and `/linkedin/post/comments` with the same id for its comment thread.

### Pagination

Four endpoints paginate, in two different styles. Every page is a separate call and costs 10 credits, so decide up front how many pages the user actually needs. The other five (`/person`, `/person/about`, `/company`, `/job`, `/post`) return a single object and take no paging parameter.

**Cursor style - `/person/posts`, `/company/posts`, `/search/jobs`.** The response carries `has_more` and `next_cursor`. While `has_more` is true, send `next_cursor` back verbatim as `cursor` on the next call; stop when `has_more` is false, at which point `next_cursor` is `null`. The cursor is opaque - it is not an offset and must not be parsed, constructed or incremented - and it belongs to the endpoint and the query that produced it, so never move one between endpoints or reuse it after changing `username`, `company`, `search` or `type`. A cursor the API cannot read is not an error: it silently restarts at page one, so a mangled cursor shows up as a paging loop that never advances.

Page sizes are 50 posts for the two feeds and 25 listings for job search.

**Page-number style - `/post/comments`.** Pass a 1-based `page`. Two upstream quirks mean you cannot use page size to detect the end: the page size **varies** (10, 10, 8 and 9 comments were observed on a single thread), so a short page does not mean the last page, and `total` is only returned on **page 1** - it is `null` on every later page, so there is no running count to compare against. The only reliable stop signal is an empty page. Keep incrementing until a page comes back with no comments; `has_more` says exactly that (this page had at least one comment) and `next_page` carries the number to ask for.

**`/search/jobs` pages, but is not a snapshot.** Upstream rotates its result set, so pages overlap slightly and two identical searches return different listings. Paginate it to widen coverage, dedupe by job `id` across pages, and never present the union as the complete set of matching jobs or diff two runs to infer new postings.

## Parameters

### Person (`/person`, `/person/about`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | one of | Public identifier (vanity handle), e.g. `williamhgates` |
| `url` | string | one of | Full LinkedIn profile URL |

### Person posts (`/person/posts`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `username` | string | one of | Public identifier (vanity handle) |
| `url` | string | one of | Full LinkedIn profile URL |
| `type` | string | `posts` | Which feed: `posts` (the member's own), `comments` (posts they commented on) or `reactions` (posts they reacted to). Any other value is a `400`. |
| `cursor` | string | -- | Opaque cursor: the previous response's `next_cursor`. Omit for page 1. |

### Company (`/company`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company` | string | one of | Company universal name (slug), e.g. `microsoft` |
| `url` | string | one of | Full LinkedIn company URL |

### Company posts (`/company/posts`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company` | string | one of | Company universal name (slug) |
| `url` | string | one of | Full LinkedIn company URL |
| `cursor` | string | -- | Opaque cursor: the previous response's `next_cursor`. Omit for page 1. |

### Search jobs (`/search/jobs`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | string | required | Keyword, e.g. `software engineer` |
| `location` | string | -- | Geographic filter, e.g. `United States`. Omit to search everywhere. |
| `cursor` | string | -- | Opaque cursor: the previous response's `next_cursor`. Omit for page 1. |

### Job (`/job`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `job_id` | string | one of | Job listing id, e.g. `4415427228` |
| `url` | string | one of | Full LinkedIn job URL |

### Post (`/post`) and post comments (`/post/comments`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `post_id` | string | one of | Post id or activity urn, e.g. `7488618410256523265` |
| `url` | string | one of | Full LinkedIn post URL |
| `page` | number | 1 | (comments only) 1-based page. Page size varies, so page until a page comes back empty. |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. A person's profile, with experience and education inline
person = requests.post(f"{BASE}/api/v1/linkedin/person", headers=HEADERS,
    json={"username": "williamhgates"}).json()

# 2. Their recent posts (a full URL works just as well as a handle)
posts = requests.post(f"{BASE}/api/v1/linkedin/person/posts", headers=HEADERS,
    json={"url": "https://www.linkedin.com/in/williamhgates/"}).json()

# 2b. The posts they reacted to instead of the ones they wrote
reactions = requests.post(f"{BASE}/api/v1/linkedin/person/posts", headers=HEADERS,
    json={"username": "williamhgates", "type": "reactions"}).json()

# 3. A company profile
company = requests.post(f"{BASE}/api/v1/linkedin/company", headers=HEADERS,
    json={"company": "microsoft"}).json()

# 4. Jobs at that company: search by name, then pull one listing in full
found = requests.post(f"{BASE}/api/v1/linkedin/search/jobs", headers=HEADERS,
    json={"search": "Microsoft software engineer", "location": "United States"}).json()

job = requests.post(f"{BASE}/api/v1/linkedin/job", headers=HEADERS,
    json={"job_id": found["data"]["data"][0]["id"]}).json()

# 5. A post and page 1 of its comments
comments = requests.post(f"{BASE}/api/v1/linkedin/post/comments", headers=HEADERS,
    json={"post_id": "7488618410256523265", "page": 1}).json()
```

Cursor paging, capped so it cannot run away with the user's credits. `next_cursor`
is echoed back untouched; each page is 10 credits.

```python
def paged(path, body, max_pages=3):
    """Walk a cursor-paginated LinkedIn endpoint. 10 credits per page."""
    cursor, out = None, []
    for _ in range(max_pages):
        payload = {**body, **({"cursor": cursor} if cursor else {})}
        data = requests.post(f"{BASE}/api/v1/linkedin/{path}",
                             headers=HEADERS, json=payload).json()["data"]
        out += data["data"]
        if not data["has_more"]:
            break
        cursor = data["next_cursor"]
    return out

feed = paged("person/posts", {"username": "williamhgates"})
jobs = paged("search/jobs", {"search": "software engineer", "location": "United States"})
# Job search rotates upstream, so pages overlap - dedupe by id.
jobs = list({j["id"]: j for j in jobs}.values())
```

Comment paging is by page number, and only an empty page means the end - page
size varies and `total` is on page 1 only.

```python
def all_comments(post_id, max_pages=5):
    out, total = [], None
    for page in range(1, max_pages + 1):
        data = requests.post(f"{BASE}/api/v1/linkedin/post/comments", headers=HEADERS,
                             json={"post_id": post_id, "page": page}).json()["data"]
        if page == 1:
            total = data["total"]          # null on every later page
        if not data["data"]:
            break                          # the only reliable stop signal
        out += data["data"]
    return out, total
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields per endpoint:

- **person** — `id`, `public_identifier`, `first_name`, `last_name`, `full_name`, `headline`, `about`, `location`, `city`, `country_code`, `avatar`, `banner`, `follower_count`, `connection_count`, `current_company{name,company_id,title}`, `experiences[]`, `educations[]`, `education_summary`, `honors_and_awards[]`, `bio_links[]`, `people_also_viewed[]`, `similar_profiles[]`, `url`.
- **person/about** — `about`, `headline`, `education_summary`, `experiences[]`, `educations[]`, `honors_and_awards[]`, `bio_links[]`.
- **person/posts**, **company/posts** — `data[]` (`id`, `share_urn`, `text`, `url`, `created_at`, `posted_relative`, `is_reshare`, `num_comments`, `num_reposts`, `reactions{total,likes,appreciations,empathy,interests,praises,entertainments}`, `images[]`, `article`, `author`), `count`, `has_more`, `next_cursor` (`null` on the last page). 50 per page.
- **company** — `id`, `universal_name`, `name`, `description`, `about`, `website`, `industries[]`, `specialties[]`, `company_size`, `organization_type`, `employee_count`, `follower_count`, `headquarters`, `locations[]`, `country_codes[]`, `logo`, `cover`, `featured_employees[]`, `similar_companies[]`, `affiliated_companies[]`, `recent_updates[]`, `url`.
- **search/jobs** — `data[]` (`id`, `title`, `url`, `company`, `company_url`, `company_logo`, `location`, `posted_at`, `workplace_type`, `salary`), `count`, `has_more`, `next_cursor` (`null` on the last page). 25 per page.
- **job** — `id`, `title`, `url`, `description`, `location`, `employment_type`, `experience_level`, `job_functions[]`, `industries[]`, `benefits[]`, `skills[]`, `is_remote`, `is_closed`, `expires_at`, `posted_at`, `applicant_count`, `view_count`, `salary`, `company{id,name,url,employee_count,employee_range,follower_count,headquarters{...}}`.
- **post** — `id`, `post_type`, `title`, `headline`, `text`, `url`, `created_at`, `hashtags[]`, `embedded_links[]`, `images[]`, `videos[]`, `num_likes`, `num_comments`, `tagged_companies[]`, `tagged_people[]`, `top_comments[]`, `author{public_identifier,full_name,avatar,url,follower_count,post_count}`.
- **post/comments** — `data[]` (`text`, `url`, `created_at`, `is_pinned`, `author{urn,full_name,headline,avatar,url}`, `replies[]`), `page`, `total` (**page 1 only**, `null` afterwards), `has_more` (this page carried at least one comment), `next_page` (`null` when the page was empty).

An experience entry has two shapes. A single role carries `company` plus its own dates. Several roles at the same employer are grouped: `title` holds the company name and each role sits in `positions[]` with its own title and dates.

```json
{
  "data": {
    "full_name": "Bill Gates",
    "headline": "Chair, Gates Foundation and Founder, Breakthrough Energy",
    "public_identifier": "williamhgates",
    "follower_count": 40550634,
    "current_company": { "name": "Gates Foundation", "title": "Co-chair" },
    "experiences": [
      {
        "title": "Co-chair",
        "company": "Gates Foundation",
        "start_date": "2000",
        "positions": []
      }
    ],
    "education_summary": "Harvard University"
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- Cost varies by endpoint: the four profile and single-item reads are 1 credit, the four paginated endpoints are 10 credits **per page**, and `/job` is 30. A ten-page job search is 100 credits, so cap any paging loop and tell the user the credit cost you intend to spend before you start.
- `/person` already contains the about text, experience and education - do not call `/person/about` as well for the same member, it is the same upstream fetch billed twice.
- Stop paging on the signal the endpoint actually gives you: `has_more` false for the three cursor endpoints, an empty `data[]` for `/post/comments`. Never stop on a short page of comments and never use `total` as a page budget - it is present on page 1 only.
- Cursors are opaque and endpoint-specific. Echo `next_cursor` back unchanged; do not parse, build or increment one, and do not carry a cursor across endpoints or across a changed `username`, `company`, `search` or `type`. An unreadable cursor silently returns page one instead of erroring, which looks like a loop that never advances.
- `/search/jobs` rotates its result set upstream, so pages overlap and a repeated search returns different listings. Dedupe by job `id`, do not present the pages you walked as an exhaustive list, and do not diff two runs to infer new postings.
- A `410` is permanent. Report the data as unavailable and move on rather than retrying or substituting a guess.
- Never fabricate names, titles, employers, job listings, post text, or counts. Only return API data.
- This is public profile data - treat it accordingly and do not infer private details.

## Failure handling

- `400` means an invalid or missing parameter (e.g. neither `username` nor `url`, or a `type` outside `posts` / `comments` / `reactions`) - fix and retry. A bad `cursor` is the exception: it does not 400, it quietly returns page one.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` on `/job` means the listing has no detail record upstream. **Not billed.** Roughly one job id in five returned by `/search/jobs` answers this way - expired and delisted postings linger in search after their detail page is gone. Skip that id and move to the next; retrying will not produce a record.
- `410` means the endpoint was retired upstream. Permanent - do not retry. Read `reason` in the body.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-scraper-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry, up to a few times.
- If a search returns no results, relax filters or try different keywords.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no LinkedIn tool - use the Scavio SDK directly (it handles the auth header, and `next_cursor` is passed straight back as `cursor`):

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

profile = client.linkedin.person(username="williamhgates")
feed = client.linkedin.person_posts(username="williamhgates", type="reactions")
more = client.linkedin.person_posts(username="williamhgates", cursor=feed["data"]["next_cursor"])
jobs = client.linkedin.search_jobs("software engineer", location="United States")
```
