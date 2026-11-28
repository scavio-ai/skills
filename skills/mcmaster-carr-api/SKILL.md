---
name: mcmaster-carr-api
description: "McMaster-Carr API for McMaster-Carr (mcmaster.com, the US industrial-supply catalog; United States, USD) - what a McMaster-Carr part costs today for one order unit, what that is per piece when it is sold in a pack, its quantity breaks, the delivery promise the page shows, its specifications and compliance details, and which parts a catalogue page lists with their prices, as mcmaster.com shows it to a visitor who is not signed in (on 2026-11-28 part 91251A540, a black-oxide alloy steel socket head screw 1/4\"-20 x 3/4\" long, read $12.42 per pack of 50, $0.25 per piece, US origin, \"Delivers Monday 3-5 pm\"; the search \"hose clamps\" opened Hose and Tube Clamps, 6,125 products in 39 product families, the first row a pack of 10 worm-drive clamps at $21.61, $2.16 per piece; the Worm-Drive Clamps family held 327 products; the catalogue's top level listed 27 categories) with price, price basis (Pkg. or Each), package quantity, package price, unit price, quantity breaks, discontinued and replacement part, specifications by group and compliance (country of origin, DFARS, ECCN, Schedule B, RoHS, REACH, USMCA); one part by part number or link; a keyword or category page with the part-number rows, product families with their counts and slugs, related categories and facets; the top-level categories. 3 endpoints, 1 credit each. McMaster-Carr part numbers only: no manufacturer part numbers, UPCs, reviews, stores or deals; large families can take up to about 4 minutes."
version: 1.0.0
tags: mcmaster-carr, mcmaster, mcmaster-com, mcmaster-carr-api, mcmaster-api, mcmaster-carr-prices, mcmaster-carr-part-number, mcmaster-part-lookup, mcmaster-search, mcmaster-product, mcmaster-categories, mcmaster-catalog, industrial-supply, industrial-supplies, industrial-parts, mro, mro-supplies, mro-prices, fasteners, screws, bolts, hose-clamps, fittings, bearings, hardware, raw-materials, b2b-prices, procurement, purchasing, part-number-lookup, pack-price, per-piece-price, unit-price, quantity-breaks, specifications, country-of-origin, rohs, reach, dfars, eccn, price-monitoring, price-tracking, product-data, usd, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/mcmaster-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api
---

# McMaster-Carr API - Industrial Parts Prices, Pack and Per-Piece Price, Specs

Read McMaster-Carr (mcmaster.com, the US industrial-supply catalog): one part by part number with its price, pack and per-piece price, quantity breaks, delivery promise, specifications and compliance; a keyword or category page with its part-number rows, product families and facets; and the top-level categories. United States, USD, as shown to a visitor who is not signed in.

**The job this skill is for: what a McMaster-Carr part costs, per order unit and per piece.** McMaster-Carr sells many parts in packs: `price` is the price of one order unit as the page shows it, `package_price` that price when the unit is a pack, and `unit_price` the price of one piece. On 2026-11-28 part 91251A540, a black-oxide alloy steel socket head screw, read $12.42 per pack of 50, $0.25 per piece.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Pack price and per-piece price, labelled.** `unit_of_measure` says Each or Pack of N. On search rows `price_basis` says whether the price cell is per package (`Pkg.`) or per piece (`Each`); for `Pkg.` rows Scavio computes `unit_price` as `package_price` / `package_quantity`.
- **McMaster-Carr part numbers only.** The site shows no manufacturer part numbers or UPCs, and it has no reviews, stores, store stock or deals. CAD and PDF files are not returned.
- **Slow search pages.** Keyword and category pages are large: usually 10-80 seconds, up to about 240. Allow a client timeout of at least 300 seconds. The largest families (socket head screws, about 29,000 products on one page) can exceed the time limit: narrow them with a family or facet slug.
- **An unknown part number is not answered.** The site does not answer for a part number it does not know; the call ends in an unbilled `502` after about 2 minutes.
- **No stock counts or history.** `delivery_message` is the delivery promise shown; no stock counts are published. Everything is the page at the moment of the call; poll and store your own series.

McMaster-Carr offers no public, self-serve API for its catalogue prices. The parts are shown on mcmaster.com, and this skill reads those public pages with one Scavio key.

See also: Zoro `zoro-api`, MSC Industrial Supply `msc-industrial-api` and Global Industrial `global-industrial-api` (US industrial and MRO supply), Home Depot `home-depot-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a McMaster-Carr part by part number (`91251A540`): per order unit, per pack and per piece, with quantity breaks
- Read a part's specifications, compliance rows (country of origin, DFARS, ECCN, Schedule B, RoHS, REACH, USMCA), discontinued status and replacement part
- Search mcmaster.com by keyword ("hose clamps", "socket head screws") and list the part-number rows with prices
- Walk the catalogue: top-level categories, then product families and facets by slug

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/mcmaster/product` | One part by part number or part link: price, pack and per-piece price, quantity breaks, delivery promise, specifications, compliance, compatible products | 1 |
| `POST /api/v1/mcmaster/search` | A keyword page or a category page: part-number rows with price and price basis, product families with counts and slugs, related categories, facets | 1 |
| `POST /api/v1/mcmaster/categories` | The top level of the catalogue, each category with the slug search takes | 1 |

United States only: every answer carries `country` (us) and `currency` (USD).

## Workflow

1. **One part.** `/product` with `part_number` (e.g. `91251A540`) or `url` (a mcmaster.com part link).
2. **Find parts.** `/search` with `query`; if the keywords are a part number, `redirected_to` says so and `product` holds that part.
3. **Browse.** `/categories` for the top level, then `/search` with `category` set to a slug (`categories[].slug`, `product_families[].slug`, `facets[].values[].slug` or `breadcrumbs[].slug`). Send `query` or `category`, not both.
4. **More rows.** Send `offset` = previous `offset` + `count` while `has_more` is true; `per_page` sets the rows per answer (default 50, up to 100).
5. **Watching prices:** there is no history. Poll the same part numbers on a schedule and store each answer with its `fetched_at`.

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `part_number` | product | A McMaster-Carr part number (`items[].part_number` of a search) |
| `url` | product | A mcmaster.com part link, instead of `part_number` |
| `query` | search | Keywords as typed into the McMaster-Carr search box, 1-120 characters |
| `category` | search | A category slug (e.g. `hose-clamps/worm-drive-clamps~~`) or a mcmaster.com/products/ link, instead of `query` |
| `per_page` | search | Part-number rows per answer, 1-100 (default 50) |
| `offset` | search | Rows to skip on the page (default 0) |

## Examples

### One part

Request `{"part_number": "91251A540"}` (1 credit), abridged:

```json
{
  "part_number": "91251A540",
  "title": "Black-Oxide Alloy Steel Socket Head Screw, US Origin, 1/4\"-20 Thread Size, 3/4\" Long",
  "product_family": "Socket Head Screws",
  "catalog_page": 3544,
  "unit_of_measure": "Pack of 50",
  "package_quantity": 50,
  "price": 12.42,
  "price_text": "$12.42 per pack of 50",
  "package_price": 12.42,
  "unit_price": 0.25,
  "per_piece_price_text": "$0.25 per piece",
  "price_levels": [],
  "delivery_message": "Delivers Monday 3-5 pm",
  "discontinued": false,
  "specifications": [{ "name": "Size", "value": "1/4\"-20", "group": "Thread" }, { "name": "Spacing", "value": "Coarse", "group": "Thread" }],
  "compliance": { "country_of_origin": "United States", "eccn": "EAR99", "schedule_b": "731815.9000", "rohs": "RoHS 3 (2015/863/EU) Compliant", "usmca_qualifying": "Yes" }
}
```

### One search row

Request `{"query": "hose clamps", "per_page": 10}` (1 credit): `heading` "Hose and Tube Clamps", `total` 6,125, `rows_on_page` 439, 39 `product_families`. The first row, abridged:

```json
{
  "position": 1,
  "part_number": "5413K49",
  "presentation": "Worm-Drive Clamps",
  "groups": ["Slotted Band", "200 Series Stainless Steel with Zinc-Plated Steel Screw"],
  "price": 21.61,
  "price_basis": "Pkg.",
  "package_quantity": 10,
  "package_price": 21.61,
  "unit_price": 2.161,
  "specs": [{ "name": "Clamp ID Range Inch", "value": "1/2\" to 7/8\"" }, { "name": "SAE Hose Clamp Size", "value": "6" }],
  "currency": "USD"
}
```

A family tile reads `{"name": "Worm-Drive Clamps", "product_count": 327, "slug": "hose-clamps/worm-drive-clamps~~"}`; send its slug as `category` for that family.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def mcmaster(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/mcmaster/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. One part (1 credit)
part = mcmaster("product", {"part_number": "91251A540"})["data"]
print(part["unit_of_measure"], part["package_price"], part["unit_price"], part["delivery_message"])

# 2. A family page, 10 rows at a time (1 credit; can take minutes)
page = mcmaster("search", {"category": "hose-clamps/worm-drive-clamps~~", "per_page": 10})["data"]
for row in page["items"]:
    print(row["part_number"], row["price"], row["price_basis"], row["package_quantity"], row["unit_price"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **product** - `country`, `currency`, `part_number`, `requested_part_number`, `title`, `name`, `detail`, `url`, `product_family`, `part_family`, `catalog_page`, `catalog_status`, `unit_of_measure`, `package_quantity`, `price`, `price_text`, `price_unit`, `package_price`, `unit_price`, `per_piece_price_text`, `price_levels[]` {`quantity`, `price`, `price_text`}, `delivery_message`, `stock_message`, `discontinued`, `discontinued_message`, `replacement_part_number`, `specifications[]` {`name`, `value`, `group`}, `compliance` {`country_of_origin`, `dfars`, `eccn`, `schedule_b`, `rohs`, `reach`, `usmca_qualifying`}, `images`, `breadcrumbs[]`, `compatible_products[]`, `note`.
- **search** - `country`, `currency`, `query`, `category`, `url`, `redirected_to`, `heading`, `total`, `rows_on_page`, `offset`, `per_page`, `count`, `has_more`, `items[]` {`position`, `part_number`, `url`, `currency`, `presentation`, `groups`, `price`, `price_basis`, `package_quantity`, `package_price`, `unit_price`, `prices[]` {`label`, `price`}, `specs[]` {`name`, `value`}}, `breadcrumbs`, `product_families[]` {`name`, `product_count`, `slug`, `url`}, `related_categories`, `presentations[]` {`name`, `row_count`}, `facets[]` {`name`, `value_count`, `values[]` {`value`, `product_count`, `slug`}}, `note`.
- **categories** - `country`, `currency`, `count`, `categories[]` {`name`, `slug`, `url`}, `note`.

## Guardrails

- Name it "McMaster-Carr (mcmaster.com, the US industrial-supply catalog)" on first mention.
- Prices: quote `price` with `unit_of_measure` and `unit_price` as the per-piece price, in USD, with the `fetched_at` date. Say when `unit_price` is computed by Scavio (search rows with `price_basis` Pkg.). Never present a pack price as a piece price.
- Stock: `delivery_message` is the delivery promise shown, not a stock count.
- Use: keep any use descriptive - looking up a part's price, pack size, specifications and compliance for purchasing.
- Links and content: refer to parts by McMaster-Carr part number; do not republish McMaster-Carr's photos, drawings or catalogue copy, and do not use the answers to copy or rebuild its catalogue.
- Not available: manufacturer part numbers, UPCs, reviews, stores, store stock, deals, CAD or PDF files, account pricing, search-box suggestions, price history (poll and store), ordering.
- Terms: Scavio does not store McMaster-Carr data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. McMaster-Carr's terms restrict how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, part numbers or specifications. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "part_number or url is required"; "Pass query (keywords, e.g. hose clamps) or category (a slug from the categories endpoint or a result's product_families[].slug), not both."; "query must contain letters or digits."; "country must be us (default): McMaster-Carr (mcmaster.com) has one United States storefront in USD."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: a part page or category slug the site answers as not found.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api).
- `502` and `503` mean McMaster-Carr data was temporarily unavailable, or the part number is unknown to the site (an unbilled `502` after about 2 minutes). They are not charged.
- Product usually takes 8-30 seconds, categories 3-40, search 10-80 and up to about 240. Allow a client timeout of at least 300 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.108.0
npm install scavio@0.109.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: part } = await scavio.mcmaster.product({ part_number: "91251A540" });
const { data: page } = await scavio.mcmaster.search({ query: "hose clamps", per_page: 10 });
const { data: top } = await scavio.mcmaster.categories();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.mcmaster.product(...)`, `search` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 3 endpoints as tools: `get_mcmaster_product`, `search_mcmaster` and `get_mcmaster_categories`. McMaster-Carr is opt-in: add `mcmaster` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.108.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,mcmaster"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/mcmaster-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api), [product](https://scavio.dev/docs/mcmaster-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api), [categories](https://scavio.dev/docs/mcmaster-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api). Platform page: [scavio.dev/mcmaster-api](https://scavio.dev/mcmaster-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=mcmaster-carr-api).
