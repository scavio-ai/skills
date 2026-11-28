---
name: supplyhouse-api
description: SupplyHouse.com API for SupplyHouse.com (supplyhouse.com, the US online plumbing, HVAC and electrical supply store; United States, USD) - what a fitting, igniter, circulator, valve or any SupplyHouse part costs today per piece and per box, its quantity-break prices, how many SupplyHouse has available, how many ship by which date from which warehouse, its specs and spec sheets, and what buyers rate and ask about it, as supplyhouse.com shows it to a visitor who is not signed in (on 2026-11-28 the Bluefin PXLE038 3/8 in. poly PEX crimp elbow read $0.62 each or $27.50 a box of 50, 1,919 available, 828 promised by Wed, Dec 2 and 1,091 by Thu, Dec 3 from 4 warehouses, rated 4.47 over 17 ratings; the search "hot surface igniter" matched 551 products, the first a Supco universal silicon nitride igniter at $21.77 with 2,705 available; the PEX Pipe Fittings category listed 19 subcategories; the PVI brand page 20 products; the Taco 007-F5 circulator had 77 questions; the menu listed 8 departments) with unit price, box price, box quantity, sale prices, quantity-break prices, stock status, Total Available, rating and key specs; keyword, part number or SKU search (a keyword the site sends to a category or product is followed), category pages (subcategories, sub-type groups or products) and brand listings, 48 a page, with facets; one product with lead times per warehouse, alternatives, accessories, specifications, documents and shipping dimensions; reviews and questions, 10 a page, newest first, no names; the top-level departments. 7 endpoints, 1 credit each. Hidden prices answer null; slow pages (allow 250 s); no ZIP delivery dates or price history.
version: 1.0.0
tags: supplyhouse, supplyhouse-com, supply-house, supplyhouse-api, supplyhouse-prices, supplyhouse-search, supplyhouse-product, supplyhouse-category, supplyhouse-brand, supplyhouse-reviews, supplyhouse-questions, supplyhouse-sku, plumbing-supply, plumbing-supplies, plumbing-parts, hvac-supply, hvac-parts, hvac-supplies, electrical-supplies, pex, pex-fittings, fittings, valves, circulators, igniters, water-heater-parts, boiler-parts, furnace-parts, b2b-prices, procurement, purchasing, part-number-lookup, unit-price, box-price, quantity-breaks, lead-times, warehouse-stock, total-available, product-reviews, product-questions, spec-sheets, product-data, us-retail, usd, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 250
    throttle: 1
    homepage: https://scavio.dev/supplyhouse-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api
---

# SupplyHouse.com API - Plumbing and HVAC Supply Prices, Lead Times, Reviews, Q&A

Read SupplyHouse.com (supplyhouse.com, the US online plumbing, HVAC and electrical supply store): keyword, part number or SKU search, category pages and brand listings with the unit price and box price labelled, quantity-break prices and SupplyHouse's Total Available; one product with lead times per warehouse, specs and documents; customer reviews and questions; and the top-level departments. United States, USD, as shown to a visitor who is not signed in.

**The job this skill is for: what a SupplyHouse part costs per piece and per box, how many are available, and when they ship.** `unit_price` is the price of one piece, `box_price` the price of one box of `box_quantity` pieces, and `lead_times` says how many ship by which date from which warehouse. On 2026-11-28 the Bluefin PXLE038 PEX crimp elbow read $0.62 each or $27.50 a box of 50, with 1,919 available.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Unit price and box price, labelled.** Never present a box price as a piece price. `*_special_price` is a sale price when SupplyHouse shows one (`discount_reason` says why); `price_tiers` are SupplyHouse's quantity-break prices as given.
- **Hidden prices answer null.** `price_hidden` true means SupplyHouse does not show the price on the page (shown in the cart, or kept for pro accounts), so no price is returned.
- **National stock, not per ZIP.** `in_stock`, `inventory_status` and `total_available` are SupplyHouse's own national figures. `lead_times` are for SupplyHouse's default delivery estimate; delivery dates for a ZIP code are not returned.
- **Slow pages.** SupplyHouse pages usually take 20-120 seconds and up to about 240. Allow a client timeout of at least 250 seconds; categories usually answer in 5-30.
- **No names in reviews or questions.** Reviewer, asker and answerer names and locations are not returned; `is_expert` marks SupplyHouse staff answers.

SupplyHouse.com offers no public, self-serve API for its catalogue prices. The products are shown on supplyhouse.com, and this skill reads those public pages with one Scavio key.

See also: Ferguson `ferguson-api` (US plumbing, HVAC and waterworks distributor), Zoro `zoro-api`, Home Depot `home-depot-product-data`, Lowe's `lowes-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a SupplyHouse part by SKU (`PXLE038`, `007-F5`) or link: per piece, per box, quantity breaks and sale price
- Check how many SupplyHouse has available and when a quantity ships, from which warehouse
- Search supplyhouse.com by keyword or part number ("hot surface igniter", "PEX crimp elbow") and list prices and availability
- Walk the catalogue: departments, category pages, a brand's products
- Read a product's reviews (rating histogram, verified buyers) or customer questions with staff answers

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api) - email or Google, no card required.
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
| `POST /api/v1/supplyhouse/search` | Keyword, part number or SKU search, 48 a page: items with unit and box price, quantity breaks, Total Available, rating, key specs; facets | 1 |
| `POST /api/v1/supplyhouse/category` | One category page: its subcategories, sub-type groups or products, 48 a page | 1 |
| `POST /api/v1/supplyhouse/brand` | One brand's products, 48 a page | 1 |
| `POST /api/v1/supplyhouse/product` | One product by SKU or link: prices, Total Available, lead times per warehouse, variants, alternatives, accessories, specs, documents, shipping | 1 |
| `POST /api/v1/supplyhouse/reviews` | Customer reviews, 10 a page, newest first, with the rating histogram | 1 |
| `POST /api/v1/supplyhouse/questions` | Customer questions and answers, 10 a page, newest first | 1 |
| `POST /api/v1/supplyhouse/categories` | The top-level departments as the site menu lists them | 1 |

United States only: every answer carries `country` (us) and `currency` (USD).

## Workflow

1. **Find parts.** `/search` with `query`. A keyword that names a category answers that category page, and an exact part number its product page: `redirected_to` says where.
2. **Browse.** `/categories` for the departments, then `/category` with a `path` (`categories[].path`, `subcategories[].path`, `groups[].path`). `page_type` says whether the page lists subcategories, sub-type groups or products. `/brand` with a `brand_path` (e.g. `Taco`, `PVI`) lists one brand.
3. **More rows.** Send `page` (1-100) while `has_more` is true.
4. **One part.** `/product` with `product_id` (the SKU, e.g. `PXLE038`) or `url`.
5. **What buyers say.** `/reviews` and `/questions` with the same `product_id`, `page` 1-200.
6. **No history.** Each answer is the page at the moment of the call; keep the `fetched_at` time with any figure you quote.

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `query` | search | Keywords, a part number or a SupplyHouse SKU, 1-200 characters |
| `category` | category | A supplyhouse.com category path (e.g. `PEX-Fittings-525000`) or link |
| `brand` | brand | A brand path (`items[].brand_path`, e.g. `Taco`, `PVI`, `Bluefin`) or brand link |
| `product_id` | product, reviews, questions | The SupplyHouse SKU (`items[].product_id`) |
| `url` | product, reviews, questions | A supplyhouse.com product link or path, instead of `product_id` |
| `page` | search, category, brand (1-100, 48 a page); reviews, questions (1-200, 10 a page) | Results page |

## Examples

### One product

Request `{"product_id": "PXLE038"}` (1 credit), abridged:

```json
{
  "product_id": "PXLE038",
  "name": "3/8\" Poly PEX Crimp Elbow",
  "brand": "Bluefin",
  "unit_price": 0.62,
  "unit_special_price": null,
  "box_price": 27.5,
  "box_quantity": 50,
  "price_tiers": [],
  "price_hidden": false,
  "currency": "USD",
  "in_stock": true,
  "inventory_status": "IN_STOCK",
  "total_available": 1919,
  "lead_times": [
    { "quantity": 828, "promise_date": "Wed, Dec 2", "sources": [{ "source_id": "PEXWAREHOUSE05", "quantity": 555, "is_warehouse": true }, { "source_id": "PEXWAREHOUSE04", "quantity": 273, "is_warehouse": true }] },
    { "quantity": 1091, "promise_date": "Thu, Dec 3", "sources": [{ "source_id": "PEXWAREHOUSE07", "quantity": 948, "is_warehouse": true }, { "source_id": "PEXWAREHOUSE06", "quantity": 143, "is_warehouse": true }] }
  ],
  "key_specs": [{ "name": "Thread Type", "values": ["PEX Crimp"] }, { "name": "Size", "values": ["3/8\""] }],
  "documents": [{ "name": "Specification Sheet", "file_name": "Bluefin-PXLE038-Submittal-Sheet.pdf" }],
  "rating": 4.5,
  "reviews_count": 17,
  "questions_count": 1
}
```

### One search item

Request `{"query": "hot surface igniter"}` (1 credit): `total` 551 over 12 pages, 10 facets (Inventory, Product Type, Brand, Size, Fuel Type ...). The first item, abridged:

```json
{
  "position": 1,
  "product_id": "SSN2000",
  "name": "Universal Silicon Nitride Igniter (120V)",
  "brand": "Supco",
  "unit_price": 21.77,
  "box_price": null,
  "price_hidden": false,
  "in_stock": true,
  "total_available": 2705,
  "rating": 4.9,
  "reviews_count": 15,
  "key_specs": [{ "name": "Type", "values": ["Ignitor"] }, { "name": "Voltage", "values": ["120v"] }]
}
```

A question on the Taco 007-F5 circulator (77 in all) reads `{"question": "... would this work?", "answer_count": 1, "answers": [{"answer": "Hi. Yes, the 007-F5 is the direct replacement for the 007-F4.", "is_expert": true}]}`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def supplyhouse(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/supplyhouse/{endpoint}", headers=HEADERS, json=body, timeout=250)
    r.raise_for_status()
    return r.json()

# 1. Search (1 credit; can take minutes)
res = supplyhouse("search", {"query": "hot surface igniter"})["data"]
for it in res["items"][:5]:
    print(it["product_id"], it["name"], it["unit_price"], it["box_price"], it["total_available"])

# 2. One part with its lead times (1 credit)
item = supplyhouse("product", {"product_id": "PXLE038"})["data"]
print(item["unit_price"], item["box_price"], item["box_quantity"], item["total_available"])
for lt in item["lead_times"]:
    print(lt["quantity"], lt["promise_date"], [s["source_id"] for s in lt["sources"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search / category / brand** - `country`, `currency`, `query` and `redirected_to` and `did_you_mean` (search), `category` {`id`, `name`, `path`, `url`, `type`} (category), `brand` {`id`, `name`, `path`, `url`} (brand), `page_type`, `breadcrumbs[]`, `total`, `page`, `page_size`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `name`, `brand`, `brand_path`, `url`, `image`, `unit_price`, `unit_special_price`, `box_price`, `box_special_price`, `box_quantity`, `price_tiers`, `discount_reason`, `price_hidden`, `currency`, `in_stock`, `inventory_status`, `total_available`, `rating`, `reviews_count`, `questions_count`, `key_specs`, `discontinued`, `replacement_product_id`, `ships_by_freight`, `call_to_order`}, `subcategories[]`, `groups[]`, `facets[]` {`name`, `values[]` {`value`, `count`, `selected`, `category_path`}}, `notes`.
- **product** - the item fields plus `requested`, `model_number`, `breadcrumbs`, `lead_times[]` {`quantity`, `promise_date`, `date_from`, `date_to`, `message`, `sources[]` {`source_id`, `quantity`, `is_warehouse`}}, `out_of_stock_lead_time`, `temporarily_unavailable`, `limit_order_quantity`, `discontinuation_reason`, `sales_discontinuation_date`, `replacement_type`, `replacement_product`, `out_of_stock_substitute`, `variants` {`family_name`, `attributes[]`}, `alternatives[]`, `accessories[]`, `replacement_parts[]`, `specifications[]` {`name`, `values`}, `images`, `videos[]`, `documents[]` {`name`, `file_name`, `url`}, `shipping` {`width`, `height`, `depth`, `weight`, `freight_class`, `ships_by_freight`}, `returnable`, `contains_lead`, `california_prop65`, `notes`.
- **reviews** - `product_id`, `name`, `brand`, `url`, `average_rating`, `rating_count`, `recommended_ratio`, `rating_histogram` {1-5}, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `headline`, `comments`, `created_at`, `verified_buyer`, `helpful_votes`, `not_helpful_votes`, `photos`, `merchant_response`, `merchant_response_date`}, `notes`.
- **questions** - `product_id`, `name`, `brand`, `url`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `questions[]` {`question_id`, `question`, `created_at`, `answer_count`, `answers[]` {`answer_id`, `answer`, `created_at`, `is_expert`, `verified_buyer`, `helpful_votes`, `not_helpful_votes`}}, `notes`.
- **categories** - `country`, `currency`, `count`, `total_nodes`, `categories[]` {`id`, `name`, `menu_name`, `path`, `url`, `image`, `documents`, `children`}, `notes`.

## Guardrails

- Name it "SupplyHouse.com (supplyhouse.com, the US online plumbing, HVAC and electrical supply store)" on first mention.
- Prices: quote `unit_price` as the piece price and `box_price` with `box_quantity` as the box price, in USD, with the `fetched_at` date. When `price_hidden` is true, say the page does not show the price; never estimate it.
- Stock: `total_available` is SupplyHouse's national figure; `lead_times` are its default delivery estimate, not a promise for a given ZIP code.
- Reviews and questions: quote ratings, headlines and answers as written; never add names (none are returned).
- Links and content: refer to parts by SupplyHouse SKU; do not republish SupplyHouse's photos or product copy.
- Use: keep any use descriptive - looking up a part's price, availability, lead times, specs and buyer feedback for a purchase decision.
- Not available: delivery dates for a ZIP code, pro or account pricing, search suggestions, price history, ordering.
- Terms: Scavio does not store SupplyHouse.com data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. SupplyHouse.com's terms govern how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, SKUs, stock figures or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required (a SupplyHouse SKU such as PXLE038, or a supplyhouse.com product link)."; "product_id must be a SupplyHouse SKU: letters, digits, - . or _, e.g. PXLE038 or 007-F5 (items[].product_id)."; "category is required: a supplyhouse.com category link or path, e.g. PEX-Fittings-525000 (categories[].path)."; "country must be us: SupplyHouse (supplyhouse.com) serves the United States."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: an unknown SKU, category or brand.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api).
- `502` and `503` mean SupplyHouse data was temporarily unavailable. They are not charged.
- Pages usually take 20-120 seconds and up to about 240; categories 5-30. Allow a client timeout of at least 250 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.109.0
npm install scavio@0.110.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: res } = await scavio.supplyhouse.search({ query: "hot surface igniter" });
const { data: item } = await scavio.supplyhouse.product({ product_id: "PXLE038" });
const { data: reviews } = await scavio.supplyhouse.reviews({ product_id: "PXLE038" });
const { data: top } = await scavio.supplyhouse.categories();
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.supplyhouse.search(...)`, `category`, `brand`, `product`, `reviews`, `questions` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_supplyhouse`, `get_supplyhouse_category`, `get_supplyhouse_brand`, `get_supplyhouse_product`, `get_supplyhouse_reviews`, `get_supplyhouse_questions` and `get_supplyhouse_categories`. SupplyHouse.com is opt-in: add `supplyhouse` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.109.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,supplyhouse"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/supplyhouse-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api), [category](https://scavio.dev/docs/supplyhouse-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api), [brand](https://scavio.dev/docs/supplyhouse-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api), [product](https://scavio.dev/docs/supplyhouse-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api), [reviews](https://scavio.dev/docs/supplyhouse-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api), [questions](https://scavio.dev/docs/supplyhouse-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api), [categories](https://scavio.dev/docs/supplyhouse-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api). Platform page: [scavio.dev/supplyhouse-api](https://scavio.dev/supplyhouse-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=supplyhouse-api).
