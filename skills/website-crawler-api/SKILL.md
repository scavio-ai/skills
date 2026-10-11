---
name: website-crawler-api
description: "Website crawler API: crawl a whole site to clean Markdown, map every URL from its sitemap, or batch extract up to 1,000 URLs in one job, with a status URL or a signed webhook. Map 1 credit; crawl and batch 1 credit per successful page (2 on ultra), failed pages free; robots.txt obeyed."
version: 1.0.0
tags: website-crawler, web-crawler-api, crawl-website, site-crawler, sitemap, sitemap-to-markdown, url-list, batch-scrape, batch-extract, website-to-markdown, rag, llm-context, knowledge-base, firecrawl-alternative, agent-tools, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/website-crawler-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api
---

# Website Crawler API - Map, Crawl and Batch Extract to Markdown

Crawl a whole website and get every page back as clean Markdown, plain text or HTML; list a site's URLs from its sitemap; or extract a list of URLs in one job. Three operations on the Extract family:

- **Map** - a site's page URLs from its sitemaps and start page. Synchronous, 1 credit.
- **Crawl** - discover and extract one site's pages breadth-first as a job. Billed per successful page.
- **Batch** - extract up to 1,000 URLs you already have as a job. Billed per successful page.

For a single page, use the `url-to-markdown-api` skill (`POST /api/v1/extract`) instead.

## When to trigger

Use this skill when the user asks to:
- Crawl a website, a docs site, a blog or a help center
- Turn a whole site (or a section of it) into Markdown for an LLM, a vector store or RAG
- List every URL on a site, read its sitemap, or find pages under a path
- Convert a sitemap into Markdown
- Scrape or extract a list of URLs in one go (batch scrape)
- Build a knowledge base or keep one fresh from a site

If the user pastes one link and asks about it, that is single-page Extract, not this skill.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: enough to map a site and crawl 10 pages on the Free plan.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request carries:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | What it does |
|---|---|---|
| `POST /api/v1/extract/map` | 1 | A site's page URLs, synchronous |
| `POST /api/v1/extract/crawl` | per successful page | Start a crawl; returns `202` with a job id |
| `GET /api/v1/extract/crawl/{id}` | free | Progress and page results, paged by cursor |
| `DELETE /api/v1/extract/crawl/{id}` | free | Cancel a crawl |
| `POST /api/v1/extract/batch` | per successful page | Start a batch of URLs; returns `202` with a job id |
| `GET /api/v1/extract/batch/{id}` | free | Progress and page results in input order |
| `DELETE /api/v1/extract/batch/{id}` | free | Cancel a batch |

## Cost

- **Map**: 1 credit on the default `normal` mode (up to 2 on `advanced`, up to 10 on `ultra`).
- **Crawl and batch**: each **successful** page costs Extract's price for the mode - `normal` 1, `advanced` 1, `ultra` 2 (`credits_per_page` in the `202`). Failed pages, 404s, robots-skipped pages and the sitemap and robots.txt reads cost nothing. Starting, polling and cancelling are free.
- Credits are taken page by page, with nothing reserved up front. If the balance runs out, the job stops cleanly with `stopped_reason: "insufficient_credits"` and keeps the pages it already fetched.
- The most a crawl can cost is `max_pages x credits_per_page`. **State that number to the user before starting a crawl or batch above 100 pages.**

| `mode` | What it handles | Credits per page |
|---|---|---|
| `normal` (default) | Static pages, docs, articles, most blogs | 1 |
| `advanced` | Renders JavaScript, for pages built in the browser | 1 |
| `ultra` | The hardest pages | 2 |

## Plan limits

| Plan | Pages per crawl | Active jobs | URLs per batch | Map links |
|---|---|---|---|---|
| Free | 10 | 1 | 10 | 500 |
| PAYG | 100 | 1 | 50 | 1,000 |
| Project | 500 | 2 | 100 | 5,000 |
| Bootstrap | 2,000 | 3 | 500 | 5,000 |
| Startup | 5,000 | 5 | 1,000 | 5,000 |
| Growth | 10,000 | 10 | 1,000 | 5,000 |

A value above the plan's limit returns `400` with `cap`, `plan` and `billing_url`. Starting a job while the plan's active jobs are all running returns `429` with `running_jobs` and a `Retry-After` header.

## Parameters

### Map - `POST /api/v1/extract/map`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | The site. A bare host is upgraded to `https`. |
| `search` | string | - | Keep URLs containing every word (case-insensitive substring). |
| `limit` | int | 1000 | 1-5,000, within the plan's map limit. |
| `sitemap` | string | `include` | `include` (sitemaps + start-page links), `only` (sitemaps; 404 when none), `skip` (start-page links). |
| `include_subdomains` | bool | false | Also return subdomain URLs. |
| `include_paths` / `exclude_paths` | string[] | - | Path globs, max 50. `*` within a segment, `**` across segments; no wildcard means that path and everything under it (`["/docs"]` covers `/docs` and `/docs/x`; `["/docs/**"]` does not match `/docs` itself). Excludes win. |
| `ignore_query_parameters` | bool | true | URLs that differ only by query string count once. |
| `mode` | string | `normal` | `normal`, `advanced`, `ultra`. |

Response `data`: `{ url, links: [{ url, source: "sitemap" | "page", lastmod? }], total_found, returned, truncated, sitemaps_read }`.

### Crawl - `POST /api/v1/extract/crawl`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | Start URL. Same site only; pages under its path are crawled first. |
| `max_pages` | int | 100 | 1-10,000, within the plan's limit. |
| `max_depth` | int | 3 | 0-10 links from the start page. 0 = the start page only. |
| `include_paths` / `exclude_paths` | string[] | - | Same globs as map. |
| `allow_subdomains` | bool | false | Also crawl subdomains. |
| `ignore_query_parameters` | bool | true | Query-string variants count as one page. |
| `sitemap` | string | `include` | `include` (sitemap seeds the crawl), `skip` (links only), `only` (sitemap pages, no link following). |
| `format` | string | `markdown` | `markdown`, `text`, `html`. |
| `mode` | string | `normal` | Sets the per-page price. |
| `webhook_url` | string | - | Public https URL for one signed completion event. |

Optional header `Idempotency-Key`: the same key within 24 hours returns the original job instead of starting a second one. Send one on every crawl and batch POST so a retried request never doubles a job.

### Batch - `POST /api/v1/extract/batch`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `urls` | string[] | required | 1-1,000 URLs within the plan's limit; duplicates removed. |
| `format` | string | `markdown` | `markdown`, `text`, `html`. |
| `mode` | string | `normal` | Sets the per-page price. |
| `webhook_url` | string | - | Public https URL for one signed completion event. |

The `202` adds `urls_count` and `invalid_urls: [{ url, error }]`; invalid URLs are never billed. If every URL is invalid the POST is a `400` and no job is created.

### Status - `GET /api/v1/extract/{crawl|batch}/{id}`

Query: `cursor` (`next_cursor` from the previous response), `limit` (1-100, default 25; also cut at about 5 MB of content), `status` (`succeeded`, `failed`, `skipped`), `include_content` (`true` default; `false` for a light progress poll).

## Examples

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Map: every URL under /docs, 1 credit
site = requests.post(f"{BASE}/api/v1/extract/map", headers=HEADERS,
    json={"url": "https://hono.dev", "include_paths": ["/docs"], "limit": 500}).json()
print(site["data"]["total_found"], [l["url"] for l in site["data"]["links"][:5]])

# 2. Crawl: start the job (202, 0 credits so far)
job = requests.post(f"{BASE}/api/v1/extract/crawl",
    headers={**HEADERS, "Idempotency-Key": "hono-docs-2026-10-11"},
    json={"url": "https://hono.dev/docs", "max_pages": 50, "include_paths": ["/docs"]}).json()
job_id = job["data"]["id"]

# 3. Poll progress for free, without content
while True:
    s = requests.get(f"{BASE}/api/v1/extract/crawl/{job_id}", headers=HEADERS,
                     params={"include_content": "false"}).json()["data"]
    if s["status"] in ("completed", "failed", "cancelled"):
        break
    time.sleep(5)
print(s["status"], s["stopped_reason"], s["pages"], s["credits_used"])

# 4. Page through the Markdown
pages, cursor = [], None
while True:
    params = {"status": "succeeded", "limit": 100}
    if cursor:
        params["cursor"] = cursor
    r = requests.get(f"{BASE}/api/v1/extract/crawl/{job_id}", headers=HEADERS, params=params).json()["data"]
    pages += [(p["url"], p["content"]) for p in r["results"]]
    cursor = r["next_cursor"]
    if not cursor:
        break

# 5. Batch: URLs you already have, results in input order
batch = requests.post(f"{BASE}/api/v1/extract/batch", headers=HEADERS,
    json={"urls": ["https://hono.dev/docs/api/routing", "https://hono.dev/docs/api/context"]}).json()
print(batch["data"]["id"], batch["data"]["urls_count"], batch["data"]["invalid_urls"])
```

### Webhooks

Set `webhook_url` and the `202` returns `webhook_secret` (`whsec_...`) once. When the job completes, fails or is cancelled, Scavio POSTs `{ "event": "completed" | "failed" | "cancelled", "job": { ...the status summary... }, "sent_at": "..." }` with headers `Scavio-Signature`, `Scavio-Event` and `Scavio-Job-Id`. Results are not in the body - read them from `job.status_url`. A delivery without a 2xx within 10 seconds is retried 30 seconds and 5 minutes later. Verify every delivery over the raw body:

```python
import hashlib, hmac, time

def verify(secret: str, header: str, raw_body: bytes, tolerance: int = 300) -> bool:
    """header is Scavio-Signature: t=<unix>,v1=<hex HMAC-SHA256 of "<t>.<raw body>">."""
    parts = dict(p.strip().split("=", 1) for p in header.split(",") if "=" in p)
    t, v1 = parts.get("t", ""), parts.get("v1", "")
    if not t.isdigit() or not v1 or abs(time.time() - int(t)) > tolerance:
        return False
    expected = hmac.new(secret.encode(), t.encode() + b"." + raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, v1)
```

## Response shapes

Crawl `202`:

```json
{
  "data": {
    "id": "crawl_01a12d2f-4c6c-7507-82b4-54a5a3035b81",
    "type": "crawl",
    "status": "queued",
    "url": "https://hono.dev/docs",
    "max_pages": 3,
    "max_depth": 3,
    "format": "markdown",
    "mode": "normal",
    "credits_per_page": 1,
    "status_url": "https://api.scavio.dev/api/v1/extract/crawl/crawl_01a12d2f-4c6c-7507-82b4-54a5a3035b81"
  },
  "credits_used": 0
}
```

Status (content cut with `...`):

```json
{
  "data": {
    "id": "crawl_01a12d21-fb42-7000-88cf-6887f653ee5d",
    "type": "crawl",
    "status": "completed",
    "stopped_reason": "max_pages",
    "error": null,
    "url": "https://hono.dev/docs",
    "format": "markdown",
    "mode": "normal",
    "pages": { "discovered": 3, "queued": 0, "succeeded": 3, "failed": 0, "skipped": 0 },
    "credits_used": 3,
    "expires_at": "2026-10-14T22:42:44.162Z",
    "webhook": null,
    "status_url": "https://api.scavio.dev/api/v1/extract/crawl/crawl_01a12d21-fb42-7000-88cf-6887f653ee5d",
    "results": [
      {
        "url": "https://hono.dev/docs/concepts/routers",
        "depth": 1,
        "status": "succeeded",
        "status_code": 200,
        "content_length": 9924,
        "truncated": false,
        "error": null,
        "skip_reason": null,
        "credits": 1,
        "content": "- Title: Routers - Hono\n\n...\n\nThe routers are the most important features for Hono..."
      }
    ],
    "next_cursor": null
  }
}
```

`status` moves `queued` -> `running` -> `completed` | `failed` | `cancelled`. `stopped_reason` on a job that ended early: `max_pages`, `insufficient_credits`, `time_limit` (6 hours), `storage_limit` (250 MB per job) or `cancelled`. Each result is `succeeded` (with `content`), `failed` (with `error` and `status_code`, 0 credits) or `skipped` (with `skip_reason`, for example `robots`, 0 credits).

## Guardrails

- **Gate the cost.** Before a crawl or batch above 100 pages, tell the user the ceiling (`max_pages x credits_per_page`) and confirm. Set `max_pages` to what the task needs, not the plan maximum.
- **Scope the crawl.** Start at the most specific path and use `include_paths` so pages go to the section the user cares about. Map first when you are unsure how big a site is - it costs 1 credit and `total_found` tells you.
- **Map + batch beats crawl** when the user wants specific pages: map, filter the URLs, then batch only those.
- **Robots.txt is always obeyed** by crawl and map; disallowed pages come back as `skipped`. Do not try to work around it, and do not batch URLs the user has no right to fetch.
- Poll with `include_content=false` every few seconds, then fetch content once the job ends. Do not re-start a job that is still `running` - poll it.
- Send an `Idempotency-Key` on every crawl and batch POST.
- Cancel a job that is crawling the wrong thing: `DELETE` stops billing immediately.
- Results are deleted 3 days after a job finishes (`expires_at`). Copy what the user needs.
- Use `markdown` or `text` for model context; `html` burns context.
- Never invent page content. If a page failed, say so, and keep the source URL next to anything you quote.

## Failure handling

- `400` - validation, a private or invalid URL, a bad `webhook_url`, or a value above the plan's limit (`cap`, `billing_url`). Not billed.
- `401` - API key invalid or missing. Check `SCAVIO_API_KEY`.
- `402` - balance below one page's cost (or one map). The body carries `billing_url`.
- `404` - unknown job id or expired results; for map, "No sitemap was found for this site." with `sitemap: "only"`.
- `409` - cancelling a job that already finished.
- `429` - active-job limit (`running_jobs`, `Retry-After`) or the per-request concurrency limit. Wait, or cancel a job.
- `502` on map - the site could not be fetched; the message names the next `mode` to try.
- `503` - temporarily at capacity. Retry after a minute.
- A failed page inside a job is not an error for the job: re-run just the failed URLs as a batch with `mode: "advanced"` or `"ultra"`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.23.0
```

```python
from scavio import ScavioClient, verify_webhook

client = ScavioClient()  # reads SCAVIO_API_KEY

site = client.extract.map("https://hono.dev", include_paths=["/docs"])
done = client.extract.crawl("https://hono.dev/docs", max_pages=50, wait=True)  # polls and collects every page
job = client.extract.batch(["https://hono.dev/docs/api/routing", "https://hono.dev/docs/api/context"])
status = client.extract.batch_status(job["data"]["id"], include_content=False)
client.extract.cancel_batch(job["data"]["id"])
page = client.extract("https://hono.dev/docs")  # single page, as before
```

```bash
npm install scavio@0.23.0
```

```js
import { Scavio, verifyWebhook } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const site = await scavio.extract.map({ url: "https://hono.dev", include_paths: ["/docs"] });
const done = await scavio.extract.crawl({ url: "https://hono.dev/docs", max_pages: 50 }, { wait: true });
const job = await scavio.extract.batch({ urls: ["https://hono.dev/docs/api/routing"] });
const status = await scavio.extract.batchStatus(job.data.id);
```

MCP: the Scavio MCP server registers `map_website`, `crawl_website`, `get_crawl_status`, `cancel_crawl`, `batch_extract`, `get_batch_status` and `cancel_batch` alongside `extract_url`. Extract is in the default tool set.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.21.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key"
      }
    }
  }
}
```

## Docs

Full reference: [Map](https://scavio.dev/docs/extract-map?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api), [Crawl](https://scavio.dev/docs/extract-crawl?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api) (plan limits and webhooks), [Crawl status](https://scavio.dev/docs/extract-crawl-status?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api), [Batch](https://scavio.dev/docs/extract-batch?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api), [Batch status](https://scavio.dev/docs/extract-batch-status?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api). Overview: [Website Crawler API](https://scavio.dev/website-crawler-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-crawler-api).
