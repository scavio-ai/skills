---
name: sec-edgar-api
description: "SEC EDGAR filings by ticker: resolve a ticker or company name to its CIK, then pull the filer profile (SIC, EIN, LEI, addresses), page filings with direct document links, read any XBRL concept's full reported history, and run EDGAR full-text search back to 2001. 6 endpoints, 1 credit each, structured JSON."
version: 1.0.0
tags: sec-edgar, edgar-api, sec-filings, 10-k, 10-q, 8-k, cik-lookup, xbrl, financial-data, full-text-search, investment-research, due-diligence, langchain, crewai, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3DB"
    homepage: https://scavio.dev/docs/sec-edgar-lookup?utm_source=agent-skills&utm_medium=skill&utm_campaign=sec-edgar-api
---

# SEC EDGAR API - Ticker to CIK, Filings, Filing Documents

Resolve a ticker or company name to its CIK, then read the filer's profile, page its filings, pull the full reported history of any XBRL concept, list every concept it reports, and run EDGAR full-text search back to 2001. All six endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find a company's CIK from a ticker or name
- List a company's SEC filings, filtered by form type or date
- Pull a reported financial number over time (revenue, net income, EPS) straight from XBRL
- Discover which financial concepts a filer actually reports
- Search the full text of SEC filings for a phrase, a risk factor, or a named party
- Check a filer's SIC industry, EIN, LEI, state of incorporation or fiscal year end
- Build investment research, fundamentals datasets, or filing-monitoring pipelines

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sec-edgar-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=sec-edgar-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/sec`. Every endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/sec/lookup` | 1 | **Start here.** Ticker or name to CIK, with the listing exchange |
| `POST /api/v1/sec/company` | 1 | Filer profile: names, SIC, EIN, LEI, addresses, tickers, filing habits |
| `POST /api/v1/sec/filings` | 1 | A page of filings with direct document links |
| `POST /api/v1/sec/concept` | 1 | Every value a filer reported for one XBRL concept |
| `POST /api/v1/sec/facts` | 1 | The index of every XBRL concept a filer reports |
| `POST /api/v1/sec/search` | 1 | EDGAR full-text search, 2001-today, with facets |

This runs on the SEC's own free JSON API, so the data is first-party.

## Workflow

**Look up first.** Callers hold a ticker (`AAPL`); EDGAR is keyed by CIK (`0000320193`).

1. **Resolve:** call `/sec/lookup` with `query` - a ticker, a company name, or a fragment. Each row carries its match tier as `match`, plus ready-made submissions, company-facts and EDGAR URLs.
2. **Profile:** call `/sec/company` with the `cik` (or a `ticker` - both fields accept either spelling, which softens the lookup step but does not remove it).
3. **Filings:** call `/sec/filings` with `cik` or `ticker`, filtered by `form` and dates.
4. **Financials, in two steps:** call `/sec/facts` to discover which XBRL tags the filer actually reports, then `/sec/concept` with one of those tags to pull its full reported history.
5. **Full text:** call `/sec/search` to find the documents that mention a phrase, across all filers.

`/sec/lookup`, `/sec/company`, `/sec/concept` and `/sec/facts` do not paginate. `/sec/filings` and `/sec/search` do.

### Pagination

- **`/sec/filings`** - `page` (1-based) with `limit` (1-500, default 50).
- **`/sec/search`** - `page`, **capped at 100**, 100 documents per page. The index refuses a result window past 10,000, which is where the cap comes from.
- `limit` on `/lookup`, `/concept` and `/facts` sizes the response. It is **not** a page parameter and there is no second page.

## Parameters

### Lookup (`/lookup`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Ticker, company name, or a fragment (1-200 chars) |
| `limit` | integer | `10` | 1-100. Sizes the response; not a page param. |
| `exchange` | string | -- | `NASDAQ`, `NYSE`, `OTC`, `CBOE`, matched case-insensitively |

Filers the SEC lists with **no** exchange at all are excluded by **any** `exchange` value - omit it if you might be chasing an OTC or unlisted filer.

### Company (`/company`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `cik` | string | one of | `320193`, `0000320193` or `CIK0000320193` (1-20 chars). A ticker is accepted here too. |
| `ticker` | string | one of | Dotted or dashed (`BRK.B` / `BRK-B`). **Wins over `cik`** when both are given. |

`cik` or `ticker` is required.

### Filings (`/filings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `cik` | string | one of | See above |
| `ticker` | string | one of | See above |
| `form` | string or array | -- | `"10-K"`, `["10-K","10-Q"]` or `"10-K,8-K"` (up to 25). Matched against the form **and its root form**. |
| `date_from` | string | -- | `YYYY-MM-DD` |
| `date_to` | string | -- | `YYYY-MM-DD` |
| `page` | integer | -- | 1-based |
| `limit` | integer | `50` | 1-500 |
| `include_history` | boolean | `false` | Reach past the "recent" block into up to 10 archived shards. Still 1 credit. |

`cik` or `ticker` is required.

### Concept (`/concept`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `concept` | string | required | **Case-sensitive** XBRL tag, e.g. `NetIncomeLoss` (1-120 chars, `^[A-Za-z][A-Za-z0-9]*$`) |
| `cik` | string | one of | See above |
| `ticker` | string | one of | See above |
| `taxonomy` | string | `us-gaap` | `us-gaap`, `dei`, `ifrs-full`, `srt` |
| `unit` | string | -- | e.g. `USD` vs `USD/shares` |
| `form` | string | -- | **Exact** match here - `10-K` excludes `10-K/A` |
| `limit` | integer | `250` | 1-2000. Sizes the response. |

`cik` or `ticker` is required.

### Facts (`/facts`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `cik` | string | one of | See above |
| `ticker` | string | one of | See above |
| `taxonomy` | string | -- | Restrict to one taxonomy |
| `query` | string | -- | Case-insensitive substring against tag name and label (1-200 chars) |
| `limit` | integer | `250` | 1-2000 |

`cik` or `ticker` is required.

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | -- | Quoted phrase for exact, bare words for a bag of terms (1-500 chars). **Optional.** |
| `cik` | string or array | -- | Up to 25. Tickers accepted here too. |
| `ticker` | string or array | -- | Up to 25 |
| `form` | string or array | -- | Up to 25 |
| `date_from` | string | -- | `YYYY-MM-DD`. Coverage starts **2001**. |
| `date_to` | string | -- | `YYYY-MM-DD` |
| `location` | string or array | -- | EDGAR's own two-character codes: `CA`, `NY`, and alphanumeric codes for foreign jurisdictions |
| `sort` | string | `relevance` | `relevance`, `newest`, `oldest` |
| `page` | integer | -- | 1-100, 100 documents per page |

`/search` accepts **no query at all** - a `cik`, `ticker`, `form` or date filter on its own is a valid search.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Resolve the ticker to a CIK - always start here
hits = requests.post(f"{BASE}/api/v1/sec/lookup", headers=HEADERS,
    json={"query": "AAPL"}).json()

# 2. Filer profile
company = requests.post(f"{BASE}/api/v1/sec/company", headers=HEADERS,
    json={"ticker": "AAPL"}).json()

# 3. Annual reports only - note this also brings back 10-K/A amendments
filings = requests.post(f"{BASE}/api/v1/sec/filings", headers=HEADERS,
    json={"ticker": "AAPL", "form": "10-K", "date_from": "2015-01-01", "limit": 100}).json()

# 4. Financials in two steps: discover the tag, then pull its history
facts = requests.post(f"{BASE}/api/v1/sec/facts", headers=HEADERS,
    json={"ticker": "AAPL", "query": "revenue"}).json()

revenue = requests.post(f"{BASE}/api/v1/sec/concept", headers=HEADERS,
    json={"ticker": "AAPL", "concept": "RevenueFromContractWithCustomerExcludingAssessedTax",
          "taxonomy": "us-gaap", "unit": "USD"}).json()

# 5. Full-text search across all filers, 2001-today
mentions = requests.post(f"{BASE}/api/v1/sec/search", headers=HEADERS,
    json={"query": "\"material weakness\"", "form": "8-K",
          "date_from": "2024-01-01", "sort": "newest", "page": 1}).json()
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **lookup** - matching filers with symbol, listing exchange, and ready-made submissions / company-facts / EDGAR URLs, tiered by match quality; each row carries its tier as `match`.
- **company** - legal and former names, SIC industry, filer category, EIN, LEI, state of incorporation, fiscal year end, business and mailing addresses, every ticker with its exchange, which forms it files and how often, plus a preview of its 10 most recent filings.
- **filings** - accession number, form and root form, filing and period dates, 8-K item codes, direct links to the primary document, the filing index and the attachment directory. `history_truncated` is set when `include_history` hit the 10-shard cap.
- **concept** - every value the filer reported for that concept, newest period first, with the form and filing each number came from. Restatements are **kept, not collapsed**, and `latest` disambiguates a quarter from its year-to-date twin using the SEC's comparability flag.
- **facts** - every XBRL concept the filer reports: tag, label, description, units and most recent value, across `us-gaap`, `dei` and any other taxonomy it uses.
- **search** - each hit is the matching **document** with its URL, form, filing date and filer identity, plus facets breaking the whole result set down by company, form, industry and state.

## Guardrails

- Every call is 1 credit, including `include_history`, which can buy up to 10 upstream fetches for that one credit. Use it rather than paging blindly into the past.
- **XBRL tags are case-sensitive.** `netincomeloss` is a 404 upstream, not a fuzzy match. Never guess a tag - call `/sec/facts` and use one it actually reports.
- **`form` behaves differently on two endpoints.** On `/filings` it matches the form and its root form, so `10-K` also returns `10-K/A` amendments (ask for `10-K/A` to get amendments only). On `/concept` it is an exact match, so `10-K` excludes `10-K/A`. Do not carry an assumption from one to the other.
- EDGAR's "recent" block is **not a fixed window** - it can be a decade for a quiet filer and about a year for a prolific one. Never tell the user "this is everything" from a default `/filings` call; set `include_history` and check `history_truncated`.
- Full-text search coverage **starts in 2001**. A phrase absent from `/search` results is not proof it was never filed.
- Restatements are preserved in `/concept`. If you report a single number for a period, say which filing it came from.
- `ticker` wins over `cik` when both are sent - do not send a mismatched pair and expect the CIK to be honoured.
- Never fabricate CIKs, accession numbers, filing dates or reported figures. Only return API data, and cite the filing behind any number you quote.
- This is public regulatory data, not investment advice. Do not present a figure as a recommendation.

## Failure handling

- `400` means an invalid or missing parameter - e.g. neither `cik` nor `ticker`, or a malformed date. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` usually means the CIK, the concept tag or the taxonomy does not exist upstream. Re-resolve with `/lookup` or `/facts` rather than retrying the same value.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sec-edgar-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- If `/search` returns nothing, remember coverage starts in 2001 and try a looser phrase or a wider date range.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no SEC EDGAR tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

hits = client.sec.lookup("AAPL")
company = client.sec.company(ticker="AAPL")
filings = client.sec.filings(ticker="AAPL", form=["10-K", "10-Q"], include_history=True)
facts = client.sec.facts(ticker="AAPL", query="revenue")
history = client.sec.concept("NetIncomeLoss", ticker="AAPL", taxonomy="us-gaap")
docs = client.sec.search(query='"material weakness"', form="8-K", sort="newest")
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const hits = await scavio.sec.lookup({ query: "AAPL" });
const history = await scavio.sec.concept({ ticker: "AAPL", concept: "NetIncomeLoss" });
```
