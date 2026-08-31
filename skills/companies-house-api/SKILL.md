---
name: companies-house-api
description: "Companies House API for the UK register: search by company name (current and former names), then pull the full register entry with status, SIC codes, registered office and accounts due dates, the officers current and resigned, and filing history with the filed PDF. 4 endpoints, 1 credit each, structured JSON."
version: 1.0.0
tags: companies-house, uk-company-search, company-registry, company-number, officers, directors, filing-history, kyb, kyc, due-diligence, sic-codes, b2b-data, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F3E2"
    homepage: https://scavio.dev/docs/companies-house-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=companies-house-api
---

# Companies House API - UK Company Search, Officers, Filings

Search the UK register by company name, then read the full register entry, the officers current and resigned, and the complete filing history. All four endpoints return structured JSON from the official UK registry.

## When to trigger

Use this skill when the user asks to:
- Find a UK company's registration number from its name
- Check whether a UK company is active, dissolved, or overdue on its accounts
- List a company's directors and secretaries, current and resigned
- Read a company's filing history and pull the filed PDFs
- Run KYB or due-diligence checks on a UK counterparty
- Look up SIC codes, incorporation dates, registered offices or previous names
- Build UK B2B datasets or company-monitoring pipelines

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=companies-house-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=companies-house-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. All paths are under `/api/v1/companieshouse`. Every endpoint costs **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/companieshouse/search` | 1 | **Start here.** Name search returning the company number |
| `POST /api/v1/companieshouse/company` | 1 | Full register entry for one company |
| `POST /api/v1/companieshouse/officers` | 1 | Officers current and resigned, 35 per page |
| `POST /api/v1/companieshouse/filing-history` | 1 | Filings, most recent first, with the filed PDF |

Note the last path is **hyphenated**: `/filing-history`.

## Workflow

**Search first.** Everything except `/search` is keyed by the company number.

1. **Find the company:** call `/companieshouse/search` with `query`. The register matches **current and former names**, so a rebranded company is still findable under its old one.
2. **Read the entry:** call `/companieshouse/company` with `company_number`.
3. **People:** call `/companieshouse/officers` with the same number.
4. **Filings:** call `/companieshouse/filing-history` with the same number.

### Company numbers are normalised for you

`company_number` is deliberately loose - there is no format check. The register 404s on `/company/445790` and `/company/sc090312` for companies that genuinely exist, so the transport zero-pads and upper-cases the value before sending it. That means a number copied off a letterhead, or one a spreadsheet stripped the leading zeros from, still resolves.

Registry prefixes supported: `SC` (Scotland), `NI` (Northern Ireland), `OC` / `SO` / `NC` (LLPs), `FC` (overseas), `BR` (UK establishment), `CE` (charitable incorporated organisation).

### Pagination

The three paginated endpoints behave differently at the end of the list, and it matters.

- **`/search`** - `page` 1-50, **20 results per page, hard-capped at page 50**. The register serves a 1000-result window per term whatever hit count it prints: it will claim 10,000 hits for a broad term and then answer page 51 with an HTTP 416. Narrow the query rather than paging deeper.
- **`/officers`** - `page`, **35 per page, no upper bound**. Past the last page the register answers an ordinary `200` with an empty list.
- **`/filing-history`** - `page`, **no upper bound**, same empty-`200` behaviour past the end.

So on officers and filings, an empty page is the stop signal - and it is **indistinguishable** from a company that has no officers or no filings at all. Check page 1 before concluding anything.

`/company` returns a single object and takes no paging parameter.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Company name or fragment (1-200 chars, non-blank). Matches current **and former** names. |
| `page` | integer | `1` | 1-50. 20 results per page; the register only serves the first 1000 matches. |

### Company (`/company`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company_number` | string | required | 1-20 chars. Zero-padded and upper-cased for you. |

### Officers (`/officers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company_number` | string | required | |
| `page` | integer | `1` | 35 per page. No upper bound - past the last page is a `200` with an empty list. |

### Filing history (`/filing-history`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company_number` | string | required | |
| `page` | integer | `1` | No upper bound - past the last page is a `200` with an empty list. |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Find the company number - matches former names too
hits = requests.post(f"{BASE}/api/v1/companieshouse/search", headers=HEADERS,
    json={"query": "Monzo Bank", "page": 1}).json()

# 2. Full register entry. Loose numbers are fine - "445790" and "sc090312" both work.
company = requests.post(f"{BASE}/api/v1/companieshouse/company", headers=HEADERS,
    json={"company_number": "09446231"}).json()

# 3. Officers, current and resigned
officers = requests.post(f"{BASE}/api/v1/companieshouse/officers", headers=HEADERS,
    json={"company_number": "09446231", "page": 1}).json()

# 4. Filings, most recent first (note the hyphen in the path)
filings = requests.post(f"{BASE}/api/v1/companieshouse/filing-history", headers=HEADERS,
    json={"company_number": "09446231", "page": 1}).json()
```

Officers and filings have no upper page bound, so page until a page comes back
empty - that is the only stop signal:

```python
def walk(path, company_number, max_pages=10):
    """1 credit per page. Stop on the first empty page."""
    pages = []
    for page in range(1, max_pages + 1):
        data = requests.post(f"{BASE}/api/v1/companieshouse/{path}", headers=HEADERS,
                             json={"company_number": company_number, "page": page}).json()["data"]
        if not data:
            break                     # empty page: past the end (or nothing to list at all)
        pages.append(data)
    return pages
```

## Response shapes

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

- **search** - company number, name, status, incorporation or dissolution date, registered office address, and the matched former names. 20 per page.
- **company** - status, type, incorporation and dissolution dates, registered office, SIC codes, previous names, accounts and confirmation-statement due dates with overdue flags, and whether it has charges, insolvency history, officers or UK establishments. An `FC` company also returns home registry, legal form and governing law; a `BR` returns its parent; a `CE` returns the charity number.
- **officers** - name, role, appointment and resignation dates, correspondence address, nationality, country of residence, month-and-year date of birth, and identity-verification status. 35 per page.
- **filing-history** - date, filing type code (`AA`, `CS01`, `SH03`), description, register annotations and child documents, and a link to the filed PDF with its page count.

**Counting active officers.** `officers_count` is every appointment ever made and `resignations_count` is how many of those ended, so the number of currently-appointed officers is the **difference**, not `officers_count`. There is no server-side active/resigned filter - the register does that client-side - so filter on each officer's `status` in the response.

**A filing still being processed** carries a `processing_note` instead of a document. That is not an error and the document is not missing permanently.

## Guardrails

- Every call is 1 credit. A full profile (search + company + officers + filings) is 4.
- **Search is capped at page 50.** The register serves a 1000-result window per term no matter what hit count it prints, and page 51 is an HTTP 416. Never promise an exhaustive list from a broad term - narrow the query.
- On officers and filing history, an empty page means either "past the end" or "there are none". Do not report "no directors" from an empty page 3 - check page 1.
- Do not compute active officers as `officers_count`. Subtract `resignations_count`, or count rows whose `status` says active.
- A missing document with a `processing_note` is a filing the register has not finished processing. Say that, rather than "the document is unavailable".
- Officer records include a partial date of birth and a correspondence address. This is public register data, but treat it with care: do not compile it into profiles of private individuals beyond what the user actually asked for.
- Never fabricate company numbers, officer names, dates or filing codes. Only return API data, and quote the company number alongside the name so the user can verify.

## Failure handling

- `400` means an invalid or missing parameter, e.g. a blank `query`. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the company number does not resolve. The transport already pads and upper-cases, so re-check the number via `/search` rather than reformatting it yourself.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=companies-house-api).
- `502` / `503` mean upstream is temporarily unavailable - wait a few seconds and retry.
- If a name search returns nothing, try a shorter fragment - the register matches former names, so an old trading name is worth a second attempt.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no Companies House tool - use the Scavio SDK directly:

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

hits = client.companies_house.search("Monzo Bank")
company = client.companies_house.company("09446231")
officers = client.companies_house.officers("09446231", page=1)
filings = client.companies_house.filing_history("09446231", page=1)
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const hits = await scavio.companiesHouse.search({ query: "Monzo Bank" });
const filings = await scavio.companiesHouse.filingHistory({ company_number: "09446231" });
```
