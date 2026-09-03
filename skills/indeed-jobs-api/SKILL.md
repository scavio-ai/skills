---
name: indeed-jobs-api
description: Indeed job search by keyword, location, radius, job type and posting age, plus one posting in full with description, structured salary, benefits and the original ATS link, employer profiles and employee reviews. 4 endpoints, 2 credits each. Salary filters match Indeed's estimate, not a posted figure.
version: 1.0.0
tags: indeed, indeed-api, indeed-jobs, job-search, job-postings, jobs-api, recruiting, hiring, salary-data, labor-market, employer-reviews, talent-intelligence, web-scraping, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4CB"
    homepage: https://scavio.dev/docs/indeed-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=indeed-jobs-api
---

# Indeed Jobs API - Job Search and Full Posting Detail

Search Indeed job postings, read one posting in full, and pull an employer's profile and employee reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find job postings by keyword, location, radius, job type, posting age or remote status
- List every posting in a metro, with or without a keyword
- Read one posting in full - description text and HTML, structured salary, benefits, geocoded address, applicant count, the original ATS link
- Look up an employer's profile - industry, HQ, size, revenue, CEO approval, ratings, reported salaries, open roles
- Read employee reviews with per-category ratings, pros and cons
- Build hiring-signal, talent-intelligence or labour-market pipelines

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=indeed-jobs-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=indeed-jobs-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Every Indeed endpoint costs **2 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/indeed/search` | 2 | Job postings: title, employer, rating, location, salary range, job type, benefits, posting age, apply route |
| `POST /api/v1/indeed/job` | 2 | One posting in full: description text and HTML, structured salary, employment types, benefits, geocoded address, applicant count, original ATS link |
| `POST /api/v1/indeed/company` | 2 | Employer profile: description, industry, HQ, size, revenue, CEO approval, per-category ratings, reported salaries, open roles, locations |
| `POST /api/v1/indeed/company/reviews` | 2 | Employee reviews with per-category ratings, pros/cons, reviewer job title and location, plus aggregated sentiment and topic/location/title breakdowns |

## Workflow

1. **Find postings:** call `/indeed/search` with `query`, `location`, or both. A **location-only search is valid** - it returns every posting in that metro.
2. **One posting:** call `/indeed/job` with `job_id` - the 16-hex job key, or any indeed.com URL carrying `jk=` (`/viewjob`, `/rc/clk`, `/pagead/clk`).
3. **The employer:** call `/indeed/company` with the `indeed.com/cmp/<slug>` slug or a full profile URL. Slugs are untidy - `Tata-Consultancy-Services-(tcs)` is a real one, so copy it rather than constructing it.
4. **Employee reviews:** call `/indeed/company/reviews` with the same `company` value.

### The three closed filters, and why they matter

Indeed does not reject a filter value it does not recognise - it **ignores** it and serves the unfiltered set under a `200`, which you still pay for.

- **`radius`** is one of `0, 5, 10, 15, 25, 35, 50, 100` miles. Ask for 7 miles and Indeed bills you for a search covering fifty. Indeed's own default is `50`.
- **`max_age_days`** is one of `1, 3, 7, 14`.
- **`min_salary` filters on Indeed's own ESTIMATE for the role, not on a posted figure.** Postings that publish no salary at all still match. Never tell the user a result set is "jobs paying at least $X" - it is "roles Indeed estimates at $X or more".

### Pagination

- **`/search`** takes a 1-based `page` that steps in Indeed's ten-result offsets (page 2 starts at result 10). Read `count` for what the page actually returned, `total_results` for Indeed's headline count, and `unique_results` for its de-duplicated figure.
- **`/company/reviews`** takes a 1-based `page` at **20 reviews per page**.
- **`/job`** and **`/company`** return a single object and take no paging parameter.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keyword (1-500 chars) |
| `location` | string | one of | City+state, postal code, state, country or `Remote` (1-200 chars). Usable **without** a query |
| `page` | integer | -- | 1-based, ten-result offsets |
| `radius` | integer | `50` | Miles. Only `0`, `5`, `10`, `15`, `25`, `35`, `50`, `100` |
| `max_age_days` | integer | -- | Only `1`, `3`, `7`, `14` |
| `job_type` | string | -- | `full_time`, `part_time`, `contract`, `temporary`, `internship` |
| `min_salary` | number | -- | Filters on **Indeed's estimate** for the role, not a posted figure |
| `remote` | boolean | -- | Remote postings only |

`query` or `location` is required.

### Job (`/job`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `job_id` | string | required | 16-hex job key, or any indeed.com URL carrying `jk=` |

### Company (`/company`) and company reviews (`/company/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company` | string | required | `indeed.com/cmp/<slug>` slug or full profile URL (1-200 chars) |
| `page` | integer | -- | (reviews only) 1-based, 20 reviews per page |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Keyword + location, inside a radius Indeed actually honours
found = requests.post(f"{BASE}/api/v1/indeed/search", headers=HEADERS,
    json={"query": "data engineer", "location": "Austin, TX",
          "radius": 25, "max_age_days": 7, "job_type": "full_time"}).json()

job_key = found["data"]["jobs"][0]["job_key"]

# 2. One posting in full, including the original ATS link
job = requests.post(f"{BASE}/api/v1/indeed/job", headers=HEADERS,
    json={"job_id": job_key}).json()

print(job["data"]["title"], job["data"]["original_job_url"])

# 3. Everything hiring in a metro - no query at all
metro = requests.post(f"{BASE}/api/v1/indeed/search", headers=HEADERS,
    json={"location": "Austin, TX", "remote": False}).json()

# 4. The employer, then its reviews (copy the slug, do not build it)
company = requests.post(f"{BASE}/api/v1/indeed/company", headers=HEADERS,
    json={"company": job["data"]["company_slug"]}).json()

reviews = requests.post(f"{BASE}/api/v1/indeed/company/reviews", headers=HEADERS,
    json={"company": job["data"]["company_slug"], "page": 1}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **search** — `query`, `location`, `url`, `page`, `total_results`, `unique_results`, `radius`, `count`, `jobs[]`, `related_queries`.
  A job row: `pos`, `job_key`, `title`, `url`, `company`, `company_url`, `company_reviews_url`, `company_rating`, `company_review_count`, `company_logo`, `location`, `city`, `state`, `postal_code`, `country`, `remote`, `location_count`, `salary_text`, `salary_min`, `salary_max`, `salary_period`, `salary_currency`, `salary_source`, `job_types`, `shifts`, `schedules`, `benefits`, `remote_types`, `attributes`, `posted_at`, `posted_relative`, `is_new`, `urgently_hiring`, `hiring_event`, `indeed_apply`, `third_party_apply`, `expired`, `snippet`, `sponsored`, `featured_employer`, `top_rated_employer`, `apply_count`.
- **job** — `job_key`, `title`, `url`, `description`, `description_html`, `company`, `company_url`, `company_slug`, `company_reviews_url`, `company_rating`, `company_review_count`, `location`, `street_address`, `latitude`, `longitude`, `city`, `state`, `postal_code`, `country`, `remote`, `salary_text`, `salary_min`, `salary_max`, `salary_currency`, `salary_period`, `salary_source`, `job_types`, `employment_types`, `benefits`, `highlighted_attributes`, `posted_at`, `valid_through`, `posted_relative`, `applicant_count`, `urgently_hiring`, `indeed_apply`, `expired`, `source`, `original_job_url`, `phone`, `related_links`.
- **company** — `company`, `name`, `url`, `logo`, `website`, `description`, `industry`, `sectors`, `headquarters`, `founded`, `employee_range`, `revenue`, `ceo_name`, `ceo_approval_percent`, `rating`, `review_count`, `reviews_url`, `rating_categories`, `ratings_by_year`, `happiness_score`, `happiness_ratings`, `total_jobs`, `jobs_url`, `job_locations`, `jobs`, `job_titles`, `locations`, `salaries`, `reviews`, `interview_difficulty`, `interview_duration`, `faqs`, `questions`, `similar_companies`.
- **company/reviews** — `company`, `name`, `url`, `page`, `count`, `total_results`, `total_ratings`, `rating`, `rating_categories`, `pros`, `cons`, `topics`, `locations`, `job_titles`, `reviews[]` (`review_id`, `title`, `text`, `pros`, `cons`, `rating`, `rating_categories`, `job_title`, `location`, `country`, `current_employee`, `submitted_on`, `helpful_count`, `unhelpful_count`, `url`).

```json
{
  "data": {
    "query": "data engineer",
    "location": "Austin, TX",
    "page": 1,
    "radius": 25,
    "total_results": 1237,
    "unique_results": 1198,
    "count": 15,
    "jobs": [
      {
        "pos": 1,
        "job_key": "a1b2c3d4e5f60718",
        "title": "Senior Data Engineer",
        "company": "Example Corp",
        "company_rating": 3.8,
        "location": "Austin, TX",
        "salary_min": 135000,
        "salary_max": 165000,
        "salary_period": "YEARLY",
        "salary_source": "ESTIMATED",
        "job_types": ["Full-time"],
        "posted_relative": "3 days ago",
        "url": "https://www.indeed.com/viewjob?jk=a1b2c3d4e5f60718"
      }
    ]
  },
  "credits_used": 2,
  "credits_remaining": 998
}
```

## Guardrails

- Every call is **2 credits**, including one that comes back empty. Search pages and review pages are 2 credits each - cap any loop and state the spend first.
- Never send a `radius` or `max_age_days` outside the closed sets. Round the user's number to the nearest allowed value and **tell them you rounded**; the alternative is a billed search that quietly ignored the filter.
- When `min_salary` is in play, describe results as roles Indeed *estimates* at that level. Check `salary_source` on each row before quoting a figure as the employer's.
- `/job` is a per-posting call. Do not loop it over a whole search page - search already returns title, employer, location, salary range, job type and posting age.
- Copy company slugs from `company_slug` or a profile URL. Hand-built slugs 404, and that 404 is billed.
- Reviews are self-reported by employees. Attribute them and do not present aggregate sentiment as fact about the employer.
- Never fabricate job titles, employers, salaries, postings or review text. Only return what the API returned.
- Always include the posting `url` (or `original_job_url`) so the user can apply through a real link.

## Failure handling

- `400` means an invalid or missing parameter - neither `query` nor `location`, or a `radius` / `max_age_days` / `job_type` outside its set. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the job key or company slug does not exist. It is a real **billed** 404 - re-derive the id from a search result rather than retrying it.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=indeed-jobs-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry, up to a few times.
- An empty search is usually the filters: widen `radius`, drop `max_age_days`, or remove `min_salary`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.indeed.search(query="data engineer", location="Austin, TX", radius=25)
job = client.indeed.job(found["data"]["jobs"][0]["job_key"])
company = client.indeed.company(job["data"]["company_slug"])
reviews = client.indeed.company_reviews(job["data"]["company_slug"], page=1)
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const found = await client.indeed.search({ query: "data engineer", location: "Austin, TX", radius: 25 });
const reviews = await client.indeed.companyReviews({ company: "example-corp", page: 1 });
```
