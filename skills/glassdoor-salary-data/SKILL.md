---
name: glassdoor-salary-data
description: "Glassdoor salary data API: resolve a company name to an employer id, then pull salary percentiles P10-P90 for base and total pay by job title, the employer profile with per-category ratings, star distribution and CEO approval, and up to three full reviews with pros, cons and employer response. 4 endpoints, 1 credit each."
version: 1.0.0
tags: glassdoor, glassdoor-salaries, salary-data, compensation, salary-benchmarking, employer-reviews, company-reviews, ceo-approval, employer-brand, recruiting, hr-tech, talent-intelligence, agents, scraping-api, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    emoji: "\U0001F3E2"
    homepage: https://scavio.dev/docs/glassdoor-companies?utm_source=agent-skills&utm_medium=skill&utm_campaign=glassdoor-salary-data
---

# Glassdoor Salary Data API - Employer Profiles, Salaries, Reviews

Resolve a company name to its Glassdoor employer id, then read the employer profile, employee reviews and salary percentiles by job title. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Look up a company's Glassdoor rating, star distribution, CEO approval and per-category scores
- Read employee reviews with pros, cons, advice and the employer's response
- Pull salary percentiles (P10-P90, base and total pay) by job title for an employer
- Benchmark compensation or employer brand across companies
- Turn a company NAME into the employer id Glassdoor's URLs use

Note: Glassdoor is the slowest surface on this API. A profile call runs 3-47 seconds, reviews around 75, salaries around 41, and a call that ultimately fails can take up to ~170 seconds before it reports a 502. Set a client timeout of at least 180 seconds and expect the occasional retry.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=glassdoor-salary-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Glassdoor endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/glassdoor/companies` | 1 | **START HERE.** Search Glassdoor for a company by name and resolve it to an `employer_id` |
| `POST /api/v1/glassdoor/company` | 1 | Employer profile: description, mission, industry, sector, HQ, size and revenue bands, stock symbol, year founded, overall and per-category ratings, star distribution, CEO approval, awards, FAQ, five server-rendered reviews, **plus `reviews_url` / `salaries_url`** |
| `POST /api/v1/glassdoor/reviews` | 1 | Up to **three** full reviews with per-axis scores, pros, cons, advice, job title, location, employment status and employer response - plus complete rating statistics, star distribution, aggregate pro/con highlight terms and per-job-title review counts |
| `POST /api/v1/glassdoor/salaries` | 1 | Salaries by job title, 10 per page: base-pay and total-pay percentiles P10-P90 with medians, sample counts, currency, pay period, last-reported date |

## Workflow

**Start at `/companies`.** `/company`, `/reviews` and `/salaries` all need an `employer_id` that exists only inside Glassdoor's `/Overview/` URLs.

1. **Resolve the name:** call `/glassdoor/companies` with `query`. Each result row carries `employer_id`, `name` and `url`.
2. **Profile:** call `/glassdoor/company` with that `employer_id`. Keep the `reviews_url` and `salaries_url` it returns.
3. **Reviews and salaries:** call `/glassdoor/reviews` and `/glassdoor/salaries` passing those saved URLs back as **`url`**. That is the single-fetch path - addressing them by `employer_id` instead makes the API resolve the case-sensitive `/Reviews/` and `/Salary/` slugs off the profile first, which is two upstream fetches for the same one credit and roughly twice the latency on the slowest surface here.

`employer_id` must be a **string** - a JSON number is rejected. `1699`, `E1699` and `IE1699` are all accepted.

`company` is **cosmetic**. The profile resolves on `employer_id` alone, `company` is ignored entirely when `url` is set, and it does **not** satisfy the required-identifier rule: a request carrying only `company` is rejected.

### Pagination

- **`/reviews` has no `page` parameter and never will.** Glassdoor's login wall caps the response at **three reviews**. Move the window with `category` and `employment_status`, and read `filtered_review_count` to see how many reviews match the current filter (against `total_review_count` for the employer overall). Do not build a paging loop here and never claim you can retrieve all reviews.
- **`/salaries`** pages with a 1-based `page` at **10 job titles per page**; `page_count` on the response says how many pages exist.
- **`/companies`** and **`/company`** return a single response and take no paging parameter.

## Parameters

### Companies lookup (`/companies`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Company name (1-120 chars) |

### Company (`/company`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `employer_id` | string | one of | `1699`, `E1699` or `IE1699`. **String, not a number** |
| `url` | string | one of | Any glassdoor.com employer URL (`/Overview/`, `/Reviews/`, `/Salary/`). Non-glassdoor.com hosts are rejected |
| `company` | string | -- | Cosmetic only; ignored when `url` is set; does not satisfy the identifier requirement |

`employer_id` or `url` is required.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `employer_id` | string | one of | Employer id |
| `url` | string | one of | Pass back `reviews_url` from `/company` to skip the resolve fetch |
| `company` | string | -- | Cosmetic |
| `category` | string | -- | `career_development`, `compensation`, `culture`, `diversity_and_inclusion`, `management`, `work_life_balance` |
| `employment_status` | string | -- | `full_time`, `part_time`, `contract`, `intern` |

`employer_id` or `url` is required. There is **no `page` parameter.** Both filters are closed sets: Glassdoor ignores an unknown value and serves the unfiltered set under a `200`, so an invented filter is a credit spent on nothing. A freelance status is absent because it was never confirmed to change the result set.

### Salaries (`/salaries`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `employer_id` | string | one of | Employer id |
| `url` | string | one of | Pass back `salaries_url` from `/company` to skip the resolve fetch |
| `company` | string | -- | Cosmetic |
| `page` | integer | -- | 1-based, 10 job titles per page; `page_count` is on the response |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
TIMEOUT = 180          # Glassdoor is slow - do not use a short client timeout

# 1. ALWAYS START HERE - a name is not an employer id
hits = requests.post(f"{BASE}/api/v1/glassdoor/companies", headers=HEADERS,
    json={"query": "Anthropic"}, timeout=TIMEOUT).json()

employer_id = hits["data"]["results"][0]["employer_id"]   # a STRING

# 2. Profile - keep the two URLs it hands back
company = requests.post(f"{BASE}/api/v1/glassdoor/company", headers=HEADERS,
    json={"employer_id": employer_id}, timeout=TIMEOUT).json()["data"]

reviews_url, salaries_url = company["reviews_url"], company["salaries_url"]

# 3. Reviews via the saved URL - one upstream fetch instead of two.
#    Up to THREE reviews. There is no page param; move the window with filters.
reviews = requests.post(f"{BASE}/api/v1/glassdoor/reviews", headers=HEADERS,
    json={"url": reviews_url, "category": "work_life_balance",
          "employment_status": "full_time"}, timeout=TIMEOUT).json()["data"]

print(reviews["count"], reviews["filtered_review_count"], reviews["total_review_count"])

# 4. Salary percentiles by job title, 10 per page
salaries = requests.post(f"{BASE}/api/v1/glassdoor/salaries", headers=HEADERS,
    json={"url": salaries_url, "page": 1}, timeout=TIMEOUT).json()["data"]

print(salaries["page"], "of", salaries["page_count"], salaries["pay_period"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Key `data` fields:

- **companies** — `count`, `results[]` (`pos`, `employer_id`, `name`, `url`).
- **company** — `employer_id`, `name`, `short_name`, `url`, `reviews_url`, `salaries_url`, `website`, `description`, `mission`, `logo`, `cover_photo`, `headquarters`, `size`, `type`, `revenue`, `stock_symbol`, `year_founded`, `industry`, `sector`, `office_count`, `is_active`, `rating`, `rating_max`, `rating_count`, `review_count`, `salary_count`, `ratings`, `industry_ratings`, `rating_distribution`, `ceo`, `awards`, `faq`, `breadcrumbs`, `reviews[]` (the five server-rendered ones).
- **reviews** — `employer_id`, `name`, `url`, `reviews_url`, `salaries_url`, `rating`, `total_review_count`, `rating_count`, `filtered_review_count`, `ratings`, `rating_distribution`, `highlights[]` (`term`, `type`, `text`), `reviews_by_job_title`, `count` (at most 3), `reviews[]` (`pos`, `review_id`, `url`, `title`, `pros`, `cons`, `advice`, `rating`, `rating_career_opportunities`, `rating_compensation_and_benefits`, `rating_culture_and_values`, `rating_diversity_and_inclusion`, `rating_senior_management`, `rating_work_life_balance`, `business_outlook`, `ceo_opinion`, `recommends`, `job_title`, `location`, `employment_status`, `is_current_employee`, `years_employed`, `published_date`, `helpful_count`, `employer_response`, `employer_response_date`).
- **salaries** — `employer_id`, `name`, `url`, `location`, `pay_period`, `currency`, `salary_count`, `job_title_count`, `page`, `page_count`, `count`, `salaries[]` (`pos`, `job_title`, `job_title_id`, `salary_count`, `currency`, `base_pay`, `total_pay`, `median_base_pay`, `median_total_pay`, `most_recent`).

```json
{
  "data": {
    "employer_id": "1699",
    "name": "Example Corp",
    "rating": 3.9,
    "total_review_count": 17798,
    "filtered_review_count": 13251,
    "count": 3,
    "reviews": [
      {
        "pos": 1,
        "review_id": "98765432",
        "title": "Good pay, heavy workload",
        "pros": "Compensation is above market and the tooling is excellent.",
        "cons": "On-call rotation is punishing during launches.",
        "rating": 4,
        "rating_work_life_balance": 3,
        "job_title": "Software Engineer",
        "location": "Austin, TX",
        "employment_status": "full_time",
        "is_current_employee": true,
        "published_date": "2026-06-14"
      }
    ]
  },
  "credits_used": 1,
  "credits_remaining": 999
}
```

## Guardrails

- Every call is **1 credit**, including one that comes back empty or times out into a 502.
- **Reviews are capped at three per response.** Never promise, imply or attempt a full review dump, and never invent a `page` parameter for `/reviews`. Report the cap, and use `filtered_review_count` / `total_review_count` to give the user the scale of what exists.
- Three reviews are not a sample you can generalise from. Use the aggregate blocks - `rating_distribution`, `ratings`, `highlights`, `reviews_by_job_title` - for anything sentiment-shaped, and quote the individual reviews as anecdotes.
- Chain `reviews_url` / `salaries_url` from `/company` whenever you already have them. Same price, half the upstream work, materially faster on a slow surface.
- `employer_id` must be a string. Send `"1699"`, not `1699`.
- Never send `company` on its own expecting it to address an employer - it is cosmetic and the request is rejected without `employer_id` or `url`.
- Salary figures are **Glassdoor's estimates for the job title**, not individual reported salaries. Say so whenever you quote one, along with `pay_period` and `currency`.
- Never fabricate employer ids, ratings, salary figures or review text. Only return what the API returned.
- Reviews are written by identifiable employees. Summarise them; do not try to identify who wrote one.

## Failure handling

- `400` means an invalid or missing parameter - neither `employer_id` nor `url`, a numeric `employer_id`, a non-glassdoor.com `url`, or a `category` / `employment_status` outside its set. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the employer id or URL does not resolve. Re-run `/companies` rather than guessing another id.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=glassdoor-salary-data).
- `502` / `503` mean upstream is temporarily unavailable. **This is the common failure here** - Glassdoor sits behind a render-only, degraded pool. A failing call can take ~170 seconds before it reports. Retry once or twice with a short pause; do not hammer it, and do not shorten the client timeout to "fail faster" - you will abandon calls that were about to succeed.
- If `/companies` returns nothing useful, try the legal entity name or a shorter form of the brand.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

hits = client.glassdoor.companies("Anthropic")
employer_id = hits["data"]["results"][0]["employer_id"]

company = client.glassdoor.company(employer_id=employer_id)["data"]
reviews = client.glassdoor.reviews(url=company["reviews_url"], category="compensation")
salaries = client.glassdoor.salaries(url=company["salaries_url"], page=1)
```

```bash
npm install scavio@0.15.0
```

```javascript
import { Scavio } from "scavio";

const client = new Scavio(); // reads SCAVIO_API_KEY
const hits = await client.glassdoor.companies({ query: "Anthropic" });
const company = await client.glassdoor.company({ employer_id: hits.data.results[0].employer_id });
const salaries = await client.glassdoor.salaries({ url: company.data.salaries_url, page: 1 });
```
