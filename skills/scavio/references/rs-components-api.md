# RS Components API - Component Prices, Pack Prices, Stock per Market

Read RS Components (rs-online.com, RS Group's electronic and industrial component distributor) in three markets: uk (uk.rs-online.com, GBP), de (de.rs-online.com, EUR, German text) and au (au.rs-online.com, AUD). Search by keyword, MPN or RS stock number, list a category or a brand, and read one product in full.

**The job this skill is for: price and check a part for a bill of materials in the UK, Germany or Australia - its unit and pack price at each quantity break, the price with VAT, and how many the market holds with the dates they ship.** On 2026-11-28 RS stock number 221-5535 (the Texas Instruments NE555P timer) on uk.rs-online.com read 0.304 GBP a unit (0.365 with VAT), sold in packs of 50 at 15.20 GBP, with 2,600 shipping from 2026-11-30 and 27,700 available across 3 scheduled shipments.

Six limits shape every answer, so say them plainly:
- **Credits.** Every call costs 2 credits. `credits_used` in the response is the truth. A not-found (`404`) and an empty search are charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Unit price and pack price are different numbers.** `unit_price` is one `base_unit` (each); `pack_price` is one `sales_unit` (a pack, tube or reel of `pack_size` units). RS sells in sales units, from `first_break_qty`. Prices exclude VAT; product adds `unit_price_inc_vat` at `vat_rate_percent`.
- **Stock differs per market.** Availability is the market's own warehouse, as the page shows it when fetched: `quantity` ships from `ship_date`, `total_available` counts every scheduled shipment, `schedule` lists them. RS shows no lead time in weeks. Quote stock with the `fetched_at` time.
- **Filters are listed, not applied.** `facets` lists the site's filters with their counts; RS applies them in the browser, so they cannot be sent back as filters. There is no sort.
- **No alternative products.** The product page carries none and none are returned.
- **RS Americas is a different site.** us.rs-online.com is not covered; `us`, `ca` and `mx` are refused (not charged).

RS Components offers its own API, with registration, keys and rate limits. This skill reads the public rs-online.com pages instead, with one Scavio key and one response shape it shares with DigiKey and Mouser.

See also: DigiKey `digikey-api` (US, Canada and Germany), Mouser Electronics `mouser-api` (US and UK), Argos `argos-stock-checker-api`, Zoro `zoro-api`.

## When to trigger

Use this skill when the user asks to:
- Look up a part on RS Components by RS stock number (`221-5535`), manufacturer part number (`NE555P`) or keyword: unit and pack price, price breaks, stock and ship dates
- Price a bill of materials in GBP, EUR or AUD, with or without VAT
- Check how many a UK, German or Australian RS market holds and when each batch ships
- List a category (`semiconductors/power-management-ics/voltage-regulators`) or a brand (`texas-instruments`) with stock status and the site's filter counts
- Read a product's RoHS status, country of origin, datasheets and specifications

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api) - email or Google, no card required.
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
| `POST /api/v1/rscomponents/search` | By keyword, MPN or stock number, 20 a page: unit and pack price, pack size, stock status, lifecycle, key specs; the site's filters with counts | 2 |
| `POST /api/v1/rscomponents/product` | One product by stock number or link: price breaks, VAT-inclusive prices, pack size, availability with its ship-date schedule, RoHS, country of origin, datasheets, specs | 2 |
| `POST /api/v1/rscomponents/category` | One category by path or link: breadcrumbs, child categories, the site's curated filtered listings and its products, 20 a page | 2 |
| `POST /api/v1/rscomponents/brand` | One brand's products by slug or link, 20 a page | 2 |

## Workflow

1. **Find products.** `/search` with `query`. A search the site sends straight to a product, category or brand page returns that page's rows and says so in `redirected_to`; `spell_corrected_to` shows a corrected keyword.
2. **Browse.** `/category` with `path` (`child_categories[].path`, `categories[].path` of a product, or a /web/c/ link); `/brand` with `brand` (`brand_slug` of a product, or a /web/b/ link).
3. **More rows.** Send `page` (1-500) while `has_more` is true.
4. **One product.** `/product` with `stock_number` (`items[].stock_number`, with or without the dash) or `url` for price breaks, VAT, availability and the ship-date schedule.
5. **Another market.** Send `country` `de` or `au`; a link sent as `url`, `path` or `brand` picks its own market.

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `query` | search | Keywords, a manufacturer part number (MPN) or an RS stock number, 1-120 characters |
| `stock_number` | product | The RS stock number (`items[].stock_number`): `221-5535`, `2215535` or `197-7393P` |
| `url` | product | An RS product link (uk, de or au), instead of `stock_number` |
| `path` | category | A category path as the market writes it, or its /web/c/ link |
| `brand` | brand | A brand slug (e.g. `texas-instruments`) or its /web/b/ link |
| `page` | search, category, brand | Results page, 1-500 (20 a page) |
| `country` | all | `uk` (default, GBP), `de` (EUR, German text) or `au` (AUD); `gb` accepted |

## Examples

### One product

Request `{"stock_number": "221-5535"}` (2 credits), abridged:

```json
{
  "country": "uk",
  "site": "uk.rs-online.com",
  "currency": "GBP",
  "stock_number": "2215535",
  "rs_stock_number": "221-5535",
  "title": "Texas Instruments NE NE555P Monostable Circuit, 1, 8-Pin PDIP",
  "mpn": "NE555P",
  "brand": "Texas Instruments",
  "brand_slug": "texas-instruments",
  "prices_include_vat": false,
  "vat_rate_percent": 20,
  "unit_price": 0.304,
  "unit_price_inc_vat": 0.365,
  "pack_price": 15.2,
  "price_breaks": [
    { "quantity": 50, "unit_price": 0.304, "unit_price_inc_vat": 0.365, "pack_price": 15.2 },
    { "quantity": 100, "unit_price": 0.252, "unit_price_inc_vat": 0.302, "pack_price": 12.6 },
    { "quantity": 1000, "unit_price": 0.233, "unit_price_inc_vat": 0.28, "pack_price": 11.65 }
  ],
  "uom_message": "Each (In a Pack of 50)",
  "minimum_order_qty": 50,
  "pack_size": 50,
  "sales_unit": "PK",
  "base_unit": "EA",
  "rohs_status": "COMPLIANT",
  "country_of_origin": "MX",
  "availability": {
    "status": "In Stock",
    "status_code": "IN_STOCK",
    "in_stock": true,
    "quantity": 2600,
    "total_available": 27700,
    "ship_date": "2026-11-30",
    "schedule": [
      { "quantity": 2600, "ship_date": "2026-11-30", "ship_date_text": "30 November 2026" },
      { "quantity": 900, "ship_date": "2026-11-30", "ship_date_text": "30 November 2026" },
      { "quantity": 24200, "ship_date": "2026-12-04", "ship_date_text": "04 December 2026" }
    ],
    "backorder_allowed": true,
    "orderable": true,
    "market": "uk"
  }
}
```

### One search row

Request `{"query": "BC547"}` (2 credits): `total` 10, one page. The first row, abridged:

```json
{
  "position": 1,
  "stock_number": "6711113",
  "title": "onsemi BC547BTA Transistor, 100 mA NPN, 45 V, 3-Pin TO-92",
  "mpn": "BC547BTA",
  "brand": "onsemi",
  "category": "Bipolar Transistors",
  "currency": "GBP",
  "unit_price": 0.126,
  "pack_price": 3.15,
  "pack_size": 25,
  "sales_unit": "PK",
  "base_unit": "EA",
  "first_break_qty": 25,
  "stock_status": "IN_STOCK",
  "in_stock": true,
  "lifecycle": null
}
```

The category `semiconductors/power-management-ics/voltage-regulators` read `total` 7,928 over 397 pages with 29 facets (Brand, Product Type, Regulator Type, Maximum Output Current, Package Type ...).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rs(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rscomponents/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search (2 credits)
res = rs("search", {"query": "BC547"})["data"]
for it in res["items"][:5]:
    print(it["stock_number"], it["mpn"], it["unit_price"], it["pack_price"], it["pack_size"], it["stock_status"])

# 2. One product: price breaks, VAT and the ship-date schedule (2 credits)
item = rs("product", {"stock_number": "221-5535"})["data"]
print(item["unit_price"], item["unit_price_inc_vat"], item["uom_message"])
for s in item["availability"]["schedule"]:
    print(s["quantity"], s["ship_date"])

# 3. The same product in Germany (2 credits; EUR, German text, the German warehouse)
de = rs("product", {"stock_number": "221-5535", "country": "de"})["data"]
print(de["currency"], de["unit_price"], de["availability"]["quantity"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `country`, `site`, `currency`, `language`, `query`, `url`, `spell_corrected_to`, `redirected_to`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `stock_number`, `title`, `mpn`, `brand`, `url`, `image`, `category`, `currency`, `unit_price`, `price_display`, `pack_price`, `pack_size`, `pack_type`, `sales_unit`, `base_unit`, `unit_priced`, `first_break_qty`, `stock_status`, `in_stock`, `lifecycle`, `last_stock`, `has_datasheets`, `specs[]` {`name`, `value`}}, `facets[]` {`name`, `key`, `type`, `values[]` {`value`, `count`}}, `notes`.
- **product** - `country`, `site`, `currency`, `language`, `requested_stock_number`, `stock_number`, `rs_stock_number`, `title`, `mpn`, `brand`, `brand_slug`, `brand_url`, `url`, `prices_include_vat`, `vat_rate_percent`, `unit_price`, `unit_price_inc_vat`, `pack_price`, `price_breaks[]` {`quantity`, `unit_price`, `unit_price_inc_vat`, `pack_price`}, `was_price`, `uom_message`, `minimum_order_qty`, `pack_size`, `pack_type`, `sales_unit`, `base_unit`, `unit_priced`, `has_pack_variants`, `pack_variant` {`stock_number`, `url`}, `rohs_status`, `country_of_origin`, `is_new`, `availability` {`status`, `status_code`, `in_stock`, `lifecycle`, `last_stock`, `quantity`, `total_available`, `ship_date`, `schedule[]` {`quantity`, `ship_date`, `ship_date_text`}, `backorder_allowed`, `orderable`, `market`}, `documents[]` {`title`, `type`, `url`}, `datasheet_url`, `specs[]`, `categories[]` {`name`, `level`, `path`, `url`}, `images`, `notes`.
- **category** - `country`, `site`, `currency`, `language`, `path`, `url`, `category` {`name`, `breadcrumbs[]`, `is_last_level`}, `child_categories[]` {`name`, `path`, `url`, `children`}, `indexable_filters[]` {`name`, `slug`, `url`}, then the listing fields of search.
- **brand** - `country`, `site`, `currency`, `language`, `brand` {`name`, `slug`, `logo`, `url`}, `url`, then the listing fields of search.

## Guardrails

- Name it "RS Components (rs-online.com, RS Group's electronic and industrial component distributor)" on first mention, with the market's site (uk.rs-online.com, de.rs-online.com or au.rs-online.com).
- Prices: say whether a figure is per unit (`unit_price`) or per pack (`pack_price`, `pack_size` units), say it excludes VAT unless you quote `unit_price_inc_vat`, and give the currency and the `fetched_at` time. Never multiply a unit price into a pack price of your own.
- Stock: say availability is the market's own, as the page showed it when fetched, with its ship dates; never carry one market's stock over to another.
- Use: keep any use descriptive - looking up parts, prices and stock for a purchase or design decision.
- Links and content: refer to products by RS stock number and manufacturer part number; do not republish RS photos or product copy, and do not use the answers to copy or rebuild its catalogue.
- Not available: RS Americas (us.rs-online.com), sorting, applying the site's filters, alternative products, lead times in weeks, account or contract pricing, price history, ordering.
- Terms: Scavio does not store RS data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read RS Components' current site terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, stock numbers, stock or ship dates. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "stock_number or url is required"; "Send stock_number or url, not both."; "stock_number must be an RS stock number, e.g. 221-5535, 2215535 or 197-7393P"; "path must be an RS category path"; "brand must be an RS brand slug"; "country: RS Americas (us.rs-online.com) is a different site and is not covered. Use uk, de or au."; "page must be a whole number from 1 to 500."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: an unknown stock number, category or brand.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api).
- `502` and `503` mean RS data was temporarily unavailable. They are not charged.
- Calls usually take 15-120 seconds. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.110.0
npm install scavio@0.111.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: res } = await scavio.rscomponents.search({ query: "BC547" });
const { data: item } = await scavio.rscomponents.product({ stock_number: "221-5535" });
const { data: cat } = await scavio.rscomponents.category({ path: "semiconductors/power-management-ics/voltage-regulators", page: 2 });
const { data: brand } = await scavio.rscomponents.brand({ brand: "texas-instruments", country: "de" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rscomponents.search(...)`, `product`, `category` and `brand`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_rscomponents`, `get_rscomponents_product`, `get_rscomponents_category` and `get_rscomponents_brand`. RS Components is opt-in: add `rscomponents` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.110.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rscomponents"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/rscomponents-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api), [product](https://scavio.dev/docs/rscomponents-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api), [category](https://scavio.dev/docs/rscomponents-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api), [brand](https://scavio.dev/docs/rscomponents-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api). Platform page: [scavio.dev/rscomponents-api](https://scavio.dev/rscomponents-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rs-components-api).
