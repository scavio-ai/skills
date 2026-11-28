# Mouser API - Electronic Component Prices, Stock, On-Order Dates, Lead Times

Read Mouser Electronics (mouser.com, the electronic component distributor) in two markets: us (mouser.com, USD) and uk (mouser.co.uk, GBP). Search by keyword or part number across the catalog or within a category, read one part in full, walk the category tree and read a manufacturer's profile.

**The job this skill is for: price and check a part for a bill of materials - its price at each quantity break, the stock Mouser shows, what is on order and when, and the factory lead time.** On 2026-11-28 Mouser part number 595-NE555P (the Texas Instruments NE555P timer) read 0.59 USD at 1 piece and 0.27 USD at 1,000, with 67,171 in stock and a 26-week factory lead time.

Six limits shape every answer, so say them plainly:
- **Credits.** Every call costs 2 credits. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Search rows show the row's breaks.** A search row lists the price breaks the row shows; product returns the full price table, grouped as the page groups it (e.g. Cut Tape / MouseReel, Full Reel with its order multiple).
- **Part numbers with a slash.** A Mouser part number with a "/" (e.g. `595-LM7805S/NOPB`) does not open by number: pass the search row's `url` (with its `qs=` part) to product.
- **Stock as fetched.** `in_stock_quantity` and `on_order` (quantity and expected date) are what the page showed when fetched. Quote them with the `fetched_at` time.
- **No sort, no similar parts.** Search returns 25 parts a page in Mouser's own order; page through with `page` (up to 200). Categories reads mouser.com only; its paths work unchanged in a uk search.
- **Slow pages.** Usually 30-160 seconds, up to about 240. Allow at least 300.

Mouser offers its own API, with registration and API keys. This skill reads Mouser's public storefront pages instead, with one Scavio key and one response shape it shares with DigiKey and RS Components.

See also: DigiKey `digikey-api` (US, Canada and Germany), RS Components `rs-components-api` (UK, Germany and Australia), Newegg `newegg-api`, Micro Center `micro-center-api`.

## When to trigger

Use this skill when the user asks to:
- Look up a part on Mouser by manufacturer part number (`NE555P`) or Mouser part number (`595-NE555P`): price breaks, stock, on-order quantities, factory lead time
- Price a bill of materials line by line at the quantities the user needs, in USD or GBP
- Check when more stock is expected (`on_order` with `expected_date`) and whether a part is marked End of Life or NRND
- Read a part's specifications, datasheet, product change notices, ECCN, HTS codes and country of origin
- List the parts of a Mouser category, or browse the category tree with part counts
- Read a manufacturer's profile on Mouser and the categories Mouser links for it

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call costs 2 credits, so 50 credits cover 25 calls.

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
| `POST /api/v1/mouser/search` | By keyword or part number, across the catalog or in a category, 25 parts a page: price breaks per packaging, stock, on-order, factory lead time, lifecycle; matching categories and manufacturers | 2 |
| `POST /api/v1/mouser/product` | One part by Mouser part number or a search row's url: full price table, stock, on-order, lead time, specifications, documents, compliance codes, country of origin | 2 |
| `POST /api/v1/mouser/categories` | The electronic components category tree with part counts (mouser.com) | 2 |
| `POST /api/v1/mouser/manufacturer` | One manufacturer's profile by slug or link: logo, ECIA authorized flag, sections, linked categories | 2 |

## Workflow

1. **Find parts.** `/search` with `query`. Keyword searches return `categories` (with subcategories and part counts) and `manufacturers` (with counts). When Mouser answers with a product page, `redirected_to` says so and `items` holds that part.
2. **Narrow.** `/search` with `category` (a `category` value from `categories[]` or from `/categories`), with or without `query`.
3. **More rows.** Send `page` (1-200) while `has_more` is true.
4. **One part.** `/product` with `mouser_part_number` (`items[].mouser_part_number`), or `url` (`items[].url`) when the number holds a "/".
5. **Browse.** `/categories` for the tree; `/manufacturer` with `manufacturer` (`items[].manufacturer_slug`) for a profile.

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `query` | search | Keywords, a manufacturer part number or a Mouser part number, 1-200 characters. Send `query`, `category` or both |
| `category` | search | A Mouser category path (`categories[].category`) or a Mouser category link |
| `page` | search | Results page, 1-200 (25 parts a page) |
| `mouser_part_number` | product | The Mouser part number (`items[].mouser_part_number`) |
| `url` | product, manufacturer | The exact product link of a search row (with its `qs=` part), or a Mouser manufacturer link |
| `manufacturer` | manufacturer | The manufacturer's Mouser slug (`items[].manufacturer_slug`), e.g. `texas-instruments` |
| `country` | all | `us` (default, mouser.com, USD) or `uk` (mouser.co.uk, GBP; `gb` accepted). Categories serves `us` only |

## Examples

### One part

Request `{"mouser_part_number": "595-NE555P"}` (2 credits), abridged:

```json
{
  "country": "us",
  "currency": "USD",
  "mouser_part_number": "595-NE555P",
  "mfr_part_number": "NE555P",
  "manufacturer": "Texas Instruments",
  "manufacturer_slug": "texas-instruments",
  "description": "Timers & Support Products Precision",
  "price": 0.59,
  "availability": "In Stock",
  "in_stock_quantity": 67171,
  "stock_note": "Can Ship Immediately",
  "on_order": [],
  "factory_lead_time_weeks": 26,
  "minimum_order_quantity": 1,
  "order_multiple": 1,
  "price_table": [
    {
      "heading": null,
      "order_multiple": null,
      "breaks": [
        { "quantity": 1, "unit_price": 0.59, "extended_price": 0.59 },
        { "quantity": 100, "unit_price": 0.318, "extended_price": 31.8 },
        { "quantity": 1000, "unit_price": 0.27, "extended_price": 270 }
      ]
    }
  ],
  "packaging": ["Tube"],
  "rohs_compliant": true,
  "compliance": { "ushts": "8542390090", "mxhts": "8542399999", "eccn": "EAR99" },
  "country_of_origin": "Mexico"
}
```

### One search row

Request `{"query": "LM7805"}` (2 credits): `total` 33 over 2 pages, `manufacturers` listed with counts. The second row, abridged:

```json
{
  "position": 2,
  "mouser_part_number": "595-LM7805S/NOPB",
  "mfr_part_number": "LM7805S/NOPB",
  "manufacturer": "Texas Instruments",
  "manufacturer_slug": "texas-instruments",
  "currency": "USD",
  "availability": "In Stock",
  "in_stock_quantity": 66,
  "on_order_quantity": 1350,
  "on_order": [{ "quantity": 1350, "expected": "Expected 12/18/2026", "expected_date": "2026-12-18" }],
  "price_breaks": [{ "packaging": null, "quantity": 1, "unit_price": 2.37 }, { "packaging": null, "quantity": 10, "unit_price": 1.75 }, { "packaging": null, "quantity": 5040, "unit_price": 1.19 }],
  "minimum_order_quantity": 1,
  "order_multiple": 1,
  "has_alternative_packaging": true
}
```

That part number holds a "/", so product takes its `url` from the search row, not the number.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def mouser(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/mouser/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. Search (2 credits)
res = mouser("search", {"query": "LM7805"})["data"]
for it in res["items"][:5]:
    print(it["mouser_part_number"], it["availability"], it["in_stock_quantity"], it["on_order"])

# 2. One part: by number, or by the row's url when the number holds a "/" (2 credits)
row = res["items"][0]
body = {"url": row["url"]} if "/" in row["mouser_part_number"] else {"mouser_part_number": row["mouser_part_number"]}
part = mouser("product", body)["data"]
for group in part["price_table"]:
    print(group["heading"], [(b["quantity"], b["unit_price"]) for b in group["breaks"]])
print(part["factory_lead_time_weeks"], part["compliance"], part["country_of_origin"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `country`, `currency`, `query`, `category`, `redirected_to` {`type`, `mouser_part_number`, `url`}, `page`, `page_size`, `heading`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `mouser_part_number`, `mfr_part_number`, `manufacturer`, `manufacturer_slug`, `description`, `url`, `image`, `datasheet_url`, `currency`, `availability`, `in_stock_quantity`, `on_order_quantity`, `on_order[]` {`quantity`, `expected`, `expected_date`}, `factory_lead_time_weeks`, `lifecycle`, `price_breaks[]` {`packaging`, `quantity`, `unit_price`}, `minimum_order_quantity`, `order_multiple`, `reel_quantity`, `mousereel_available`, `has_alternative_packaging`}, `categories[]` {`name`, `category`, `url`, `subcategories[]` {`name`, `category`, `url`, `product_count`}}, `manufacturers[]` {`name`, `count`}, `facets[]` {`name`, `values`}, `breadcrumbs`, `note`.
- **product** - `country`, `currency`, `mouser_part_number`, `requested_mouser_part_number`, `mfr_part_number`, `manufacturer`, `manufacturer_slug`, `name`, `description`, `url`, `image`, `datasheet_url`, `price`, `availability`, `in_stock`, `in_stock_quantity`, `stock_note`, `on_order_quantity`, `on_order[]`, `factory_lead_time_weeks`, `minimum_order_quantity`, `order_multiple`, `full_reel_quantity`, `price_table[]` {`heading`, `order_multiple`, `breaks[]` {`quantity`, `unit_price`, `extended_price`}}, `packaging`, `rohs_compliant`, `lifecycle`, `specifications[]` {`name`, `value`}, `documents[]` {`type`, `title`, `url`}, `compliance` {`ushts`, `mxhts`, `eccn`, ...}, `country_of_origin`, `assembly_country_of_origin`, `country_of_diffusion`, `breadcrumbs`, `category`, `note`.
- **categories** - `country`, `currency`, `count`, `subcategory_count`, `categories[]` {`name`, `category`, `url`, `groups[]` {`name`, `category`, `url`, `subcategories[]` {`name`, `category`, `url`, `product_count`}}}, `note`.
- **manufacturer** - `country`, `currency`, `name`, `slug`, `url`, `logo`, `ecia_authorized`, `sections[]` {`name`, `url`}, `products_url`, `newest_products_url`, `categories[]` {`name`, `category`, `url`}, `note`.

## Guardrails

- Name it "Mouser Electronics (mouser.com, the electronic component distributor)" on first mention.
- Prices: quote `unit_price` at the quantity break and packaging group it belongs to, in USD or GBP, with the `fetched_at` time, as shown to a visitor who is not signed in. A Full Reel break needs its `order_multiple`; never apply it to a cut-tape quantity.
- Stock and lead time: say `in_stock_quantity` and `on_order` are what the page showed when fetched, never a promise of what will ship. `factory_lead_time_weeks` is the manufacturer's lead time Mouser shows for quantities beyond stock, not a delivery date.
- Use: keep any use descriptive - looking up parts, prices, stock and lead times for a purchase or design decision.
- Links and content: refer to parts by Mouser part number and manufacturer part number; do not republish Mouser's photos or product copy, and do not use the answers to copy or rebuild its catalogue.
- Not available: sorting, similar or alternative parts, ordering, account pricing, price history, a uk category tree (use the mouser.com paths).
- Terms: Scavio does not store Mouser data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read Mouser's current site terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, part numbers, stock or lead times. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "query or category is required"; "mouser_part_number or url is required"; a part number with a "/" ("pass the item's url ... instead"); "url must be the exact product link of a search row, with its qs= part"; "country must be us for categories"; "country must be us (default, mouser.com, USD) or uk (mouser.co.uk, GBP)."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: an unknown Mouser part number, category or manufacturer slug.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api).
- `502` and `503` mean Mouser data was temporarily unavailable. They are not charged.
- Calls usually take 30-160 seconds, up to about 240. Allow a client timeout of at least 300 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.110.0
npm install scavio@0.111.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: res } = await scavio.mouser.search({ query: "LM7805" });
const { data: part } = await scavio.mouser.product({ mouser_part_number: "595-NE555P" });
const { data: tree } = await scavio.mouser.categories();
const { data: mfr } = await scavio.mouser.manufacturer({ manufacturer: "texas-instruments" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.mouser.search(...)`, `product`, `categories` and `manufacturer`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_mouser`, `get_mouser_product`, `get_mouser_categories` and `get_mouser_manufacturer`. Mouser is opt-in: add `mouser` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.110.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,mouser"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/mouser-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api), [product](https://scavio.dev/docs/mouser-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api), [categories](https://scavio.dev/docs/mouser-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api), [manufacturer](https://scavio.dev/docs/mouser-manufacturer?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api). Platform page: [scavio.dev/mouser-api](https://scavio.dev/mouser-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=mouser-api).
