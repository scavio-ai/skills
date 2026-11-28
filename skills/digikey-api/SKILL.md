---
name: digikey-api
description: DigiKey API for DigiKey (digikey.com, the electronic component distributor; us USD, ca CAD, de EUR) - which parts match a manufacturer or DigiKey part number, what a part costs at each quantity break per packaging, how many DigiKey has in stock, the manufacturer's standard lead time, its Part Status and its RoHS, REACH, MSL, ECCN and HTSUS classifications, as DigiKey lists them to a visitor who is not signed in (on 2026-11-28 DigiKey part number 497-1575-5-ND, STMicroelectronics LM317T, read 1.19 USD at 1 piece and 0.59215 USD at 1,000 in a tube, 101,976 in stock, Active, 30-week standard lead time, 9 substitutes listed by DigiKey; LM317 in the linear voltage regulator category with Manufacturer Texas Instruments and In Stock matched 62 parts) with exact part matches and the categories holding them, a leaf category's first 25 rows narrowed by DigiKey's own filters, one product with price breaks, minimum order and multiple, documents, related parts and substitutes, and the category tree with product counts. 3 endpoints, 2 credits each; a product looked up by DigiKey part number is held at 4. Stock is one number for every market; search serves us and de; later pages of a category are not offered.
version: 1.0.0
tags: digikey, digi-key, digikey-com, digikey-api, digikey-search, digikey-product, digikey-categories, digikey-part-number, digikey-prices, digikey-stock, electronic-components, electronic-component-prices, component-prices, component-availability, component-stock, price-breaks, quantity-breaks, lead-times, standard-lead-time, part-status, lifecycle-status, obsolete-parts, substitutes, mpn-lookup, manufacturer-part-number, part-number-lookup, bom, bom-pricing, procurement, purchasing, hardware-engineering, semiconductors, integrated-circuits, voltage-regulators, rohs, reach, eccn, htsus, datasheets, usd, cad, eur, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 300
    throttle: 1
    homepage: https://scavio.dev/digikey-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api
---

# DigiKey API - Electronic Component Prices, Price Breaks, Stock, Lead Times

Read DigiKey (digikey.com, the electronic component distributor) in three markets: us (digikey.com, USD), ca (digikey.ca, CAD) and de (digikey.de, EUR, German labels, prices without VAT). Search by keyword or part number, read a category's part rows with price breaks and stock, read one part in full, and walk the category tree.

**The job this skill is for: price and check a part for a bill of materials - its price at each quantity break, the stock DigiKey shows, the manufacturer's standard lead time and whether the part is still Active.** On 2026-11-28 DigiKey part number 497-1575-5-ND (STMicroelectronics LM317T) read 1.19 USD at 1 piece, 0.7256 USD at 50 (the standard package) and 0.59215 USD at 1,000, with 101,976 in stock, Part Status Active and a 30-week standard lead time.

Six limits shape every answer, so say them plainly:
- **Credits.** Every call costs 2 credits. A product looked up by DigiKey part number is held at 4: DigiKey resolves the number through a search page first, then the market's product page (2 when the number lands straight on a digikey.com product page). A product by link is 2. `credits_used` in the response is the truth. A not-found (`404`) is charged what it spent; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Two-step search.** A keyword search returns DigiKey's category view: `exact_matches` (parts whose manufacturer part number matches) and `categories` with product counts. Search again with `category_id` and the same keywords for the part rows with prices and stock.
- **Page 1 only.** Category rows are DigiKey's first page, 25 rows in DigiKey's order. Later pages are not offered: narrow with keywords and `filters` (ids from `facets` and `common_filters`). `filter_check` says per filter whether the page shows it applied.
- **Stock is one global number.** `quantity_available` is DigiKey's own stock, the same on digikey.com, digikey.ca and digikey.de, as the page shows it when fetched. Quote it with the `fetched_at` time.
- **Markets.** Search serves us and de; for digikey.ca use product and categories. On digikey.de labels and specs are in German and prices are without VAT (`vat` carries both figures where the page shows them).
- **Slow pages.** Usually 10-40 seconds, up to about 200 when DigiKey is slow. Allow at least 300.

DigiKey offers its own official API, with registration, API keys and rate limits. This skill reads DigiKey's public storefront pages instead, with one Scavio key and one response shape it shares with Mouser and RS Components.

See also: Mouser Electronics `mouser-api` (US and UK electronic component distributor), RS Components `rs-components-api` (UK, Germany and Australia), Newegg `newegg-api`, Micro Center `micro-center-api`.

## When to trigger

Use this skill when the user asks to:
- Look up a part on DigiKey by manufacturer part number (`LM317T`) or DigiKey part number (`497-1575-5-ND`): price breaks, stock, lead time, Part Status
- Price a bill of materials line by line at the quantities the user needs, per packaging (Cut Tape, Tape & Reel, Tube)
- Find which DigiKey category holds a part, then list that category's rows narrowed by manufacturer, stocking option or other DigiKey filters
- Check whether a part is Active, Obsolete or Not For New Designs, and read the substitutes DigiKey's page lists
- Read a part's RoHS, REACH, MSL, ECCN and HTSUS classifications and its datasheet link
- Compare a part's price in USD, CAD and EUR across digikey.com, digikey.ca and digikey.de

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. A call costs 2 credits (a product by DigiKey part number up to 4), so 50 credits cover 25 searches or at least 12 part lookups.

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
| `POST /api/v1/digikey/search` | By keyword or part number: exact part matches and the categories holding them; with `category_id`, page 1 of that category's rows (25) with price breaks, stock and specs, narrowed by `filters` | 2 |
| `POST /api/v1/digikey/product` | One part by link or DigiKey part number: price breaks per packaging, stock, standard lead time, Part Status, classifications, documents, related parts, substitutes | 2 by link; 4 by DigiKey part number (2 when it lands straight on a digikey.com product page) |
| `POST /api/v1/digikey/categories` | The top-level categories, or one category with its subcategories and product counts | 2 |

## Workflow

1. **Find the category.** `/search` with `query` (keywords or a part number). The answer lists `exact_matches` and `categories` [{`id`, `name`, `parent`, `product_count`}]. An exact part number can land on one product (`result_type` product).
2. **List the rows.** `/search` again with `category_id` (a category whose `leaf` is true) and the same `query`: 25 rows with `pricing`, `quantity_available` and `specs`, plus `facets` and `common_filters`.
3. **Narrow.** Add `filters` {`<facet id>`: [`<option id>`, ...]}, e.g. `{"-1": ["296"]}` for Manufacturer Texas Instruments and `{"-2": ["5"]}` for In Stock. Read `filter_check` to see which filters the page shows applied.
4. **One part.** `/product` with `digikey_part_number` (from `items[].digikey_part_number`) or `url` (from `items[].url`) for the full price table per packaging, lead time, Part Status, classifications, documents and substitutes.
5. **Browse.** `/categories` with no input for the top-level categories, or `category_id` for one category's subcategories and counts.

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `query` | search | Keywords, a manufacturer part number or a DigiKey part number, 1-120 characters. Send `query`, `category_id` or both |
| `category_id` | search, categories | A category id (`categories[].id`, e.g. `699`) or a DigiKey category link. On search it must be a leaf category |
| `filters` | search | With `category_id`: {`<facet id>`: [`<option id>`, ...]} from `facets[]` and `common_filters[]`, up to 10 filters |
| `url` | product | A DigiKey product link (`items[].url`); the link's site sets the market |
| `digikey_part_number` | product | A DigiKey part number (`items[].digikey_part_number`), instead of `url` |
| `country` | all | `us` (default, USD), `ca` (CAD; product and categories only) or `de` (EUR, German labels, prices without VAT) |

## Examples

### One part by DigiKey part number

Request `{"digikey_part_number": "497-1575-5-ND"}` (held at 4 credits), abridged:

```json
{
  "country": "us",
  "currency": "USD",
  "product_id": "591677",
  "digikey_part_numbers": ["497-1575-5-ND"],
  "mpn": "LM317T",
  "manufacturer": "STMicroelectronics",
  "description": "IC REG LINEAR POS ADJ 1.5A TO220",
  "lifecycle_status": "Active",
  "normally_stocking": true,
  "quantity_available": 101976,
  "standard_lead_time": "30 Weeks",
  "standard_lead_time_weeks": 30,
  "unit_price": 1.19,
  "standard_package_quantity": 50,
  "pricing": [
    {
      "digikey_part_number": "497-1575-5-ND",
      "packaging": "Tube",
      "min_order_quantity": 1,
      "order_multiple": 1,
      "price_breaks": [
        { "quantity": 1, "unit_price": 1.19, "extended_price": 1.19 },
        { "quantity": 50, "unit_price": 0.7256, "extended_price": 36.28, "standard_package": true },
        { "quantity": 1000, "unit_price": 0.59215, "extended_price": 592.15 }
      ]
    }
  ],
  "environmental": { "rohs_status": "ROHS3 Compliant", "reach_status": "REACH Unaffected", "moisture_sensitivity_level": "1 (Unlimited)", "eccn": "EAR99", "htsus": "8542.39.0070" },
  "substitutes": [{ "product_id": "1493969", "mpn": "LM317KCSE3", "manufacturer": "Texas Instruments", "unit_price": 3.17, "quantity_available": 807, "substitute_type": "Direct" }]
}
```

`substitutes` held 9 parts and `related_parts` (DigiKey's "You May Also Be Interested In" list) 10; `documents` listed datasheets, PCNs and EDA models.

### Category rows with filters

Request `{"query": "LM317", "category_id": "699", "filters": {"-1": ["296"], "-2": ["5"]}}` (2 credits): `result_type` products, `total` 62, `count` 25, `filter_check` {`-1`: applied, `-2`: applied}. The first row, abridged:

```json
{
  "position": 1,
  "digikey_part_number": "296-20678-1-ND",
  "digikey_part_number_packaging": "Cut Tape (CT)",
  "mpn": "LM317LIDR",
  "manufacturer": "Texas Instruments",
  "description": "IC REG LIN POS ADJ 100MA 8-SOIC",
  "rohs_compliant": true,
  "quantity_available": 78226,
  "unit_price": 0.33,
  "product_status": "Active",
  "pricing": [{ "packaging": "Cut Tape (CT)", "min_order_quantity": 1, "unit_price": 0.33, "price_breaks": [{ "quantity": 1, "unit_price": 0.33, "extended_price": 0.33 }, { "quantity": 10, "unit_price": 0.227, "extended_price": 2.27 }] }]
}
```

A keyword search alone for `LM7805` returned the category view: 4 `categories`, the first id 699 (Voltage Regulators - Linear, Low Drop Out (LDO) Regulators, 17 matching products).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
ENDPOINTS = f"{BASE}/api/v1/digikey"

def digikey(endpoint, body):
    r = requests.post(f"{ENDPOINTS}/{endpoint}", headers=HEADERS, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

# 1. Which categories hold the part (2 credits)
res = digikey("search", {"query": "LM317"})["data"]
print([(c["id"], c["name"], c["product_count"]) for c in res["categories"]])

# 2. The rows of one category, In Stock only (2 credits)
rows = digikey("search", {"query": "LM317", "category_id": "699", "filters": {"-2": ["5"]}})["data"]
for it in rows["items"][:5]:
    breaks = it["pricing"][0]["price_breaks"] if it["pricing"] else []
    print(it["digikey_part_number"], it["mpn"], it["quantity_available"], [(b["quantity"], b["unit_price"]) for b in breaks[:3]])

# 3. One part (held at 4 credits by DigiKey part number)
part = digikey("product", {"digikey_part_number": "497-1575-5-ND"})["data"]
print(part["mpn"], part["lifecycle_status"], part["standard_lead_time"], part["quantity_available"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `country`, `currency`, `language`, `query`, `category_id`, `filters`, `result_type` (categories, products or product), `total`, `page`, `page_size`, `count`, `has_more`, `items[]` {`position`, `product_id`, `digikey_part_number`, `digikey_part_number_packaging`, `mpn`, `manufacturer`, `manufacturer_id`, `description`, `url`, `image`, `datasheet_url`, `rohs_compliant`, `quantity_available`, `stock[]` {`label`, `quantity`}, `unit_price`, `pricing[]` {`packaging`, `min_order_quantity`, `unit_price`, `price_breaks[]` {`quantity`, `unit_price`, `extended_price`}}, `product_status`, `series`, `packaging`, `tariff_note`, `specs[]` {`id`, `name`, `value`}}, `exact_matches[]` {`product_id`, `mpn`, `manufacturer`, `description`, `url`, `image`, `unit_price`}, `categories[]` {`id`, `name`, `parent`, `product_count`, `url`}, `category`, `breadcrumbs`, `facets[]` and `common_filters[]` {`id`, `name`, `type`, `options[]` {`id`, `name`, `product_count`}}, `applied`, `filter_check`, `product`, `note`.
- **product** - `country`, `currency`, `language`, `requested`, `product_id`, `digikey_part_numbers`, `mpn`, `manufacturer`, `manufacturer_id`, `description`, `detailed_description`, `url`, `images`, `datasheet_url`, `lifecycle_status`, `series`, `is_new_product`, `normally_stocking`, `quantity_available`, `standard_lead_time`, `standard_lead_time_weeks`, `pricing[]` {`digikey_part_number`, `packaging`, `min_order_quantity`, `order_multiple`, `price_breaks[]`}, `unit_price`, `vat`, `standard_package_quantity`, `marketplace` {`is_marketplace_only`, `ships_from_note`}, `notes`, `environmental` {`rohs_status`, `reach_status`, `moisture_sensitivity_level`, `eccn`, `htsus`}, `specs[]`, `part_number_aliases`, `category`, `breadcrumbs`, `documents[]` {`type`, `title`, `url`}, `related_parts[]`, `substitutes[]` {`product_id`, `mpn`, `manufacturer`, `unit_price`, `quantity_available`, `substitute_type`, `datasheet_url`}, `note`.
- **categories** - `country`, `currency`, `language`, `category_id`, `total_categories`, `count`, `categories[]` {`id`, `name`, `url`, `product_count`, `new_product_count`, `leaf`, `subcategories_listed`, `subcategories[]`}, `category`, `breadcrumbs`, `note`.

## Guardrails

- Name it "DigiKey (digikey.com, the electronic component distributor)" on first mention.
- Prices: quote `unit_price` at the quantity break and packaging it belongs to, in the market's currency, with the `fetched_at` time, as DigiKey's list price for a visitor who is not signed in. A Tape & Reel price needs a full reel (`min_order_quantity`); never apply a reel break to a cut-tape quantity.
- Stock and lead time: say `quantity_available` is the stock the page showed when fetched, never a promise of what will ship. `standard_lead_time` is the manufacturer's standard lead time as DigiKey states it, not a delivery date.
- Substitutes: quote `substitutes` as the parts DigiKey's page lists, with DigiKey's `substitute_type`. `related_parts` are DigiKey's "You May Also Be Interested In" list, not equivalents. Never present either as an engineering approval; the user checks the datasheet.
- Use: keep any use descriptive - looking up parts, prices, stock and lead times for a purchase or design decision.
- Links and content: refer to parts by DigiKey part number and manufacturer part number; do not republish DigiKey's photos or product copy, and do not use the answers to copy or rebuild its catalogue.
- Not available: later pages of a category, sorting, ordering, account or contract pricing, price history, search on digikey.ca.
- Terms: Scavio does not store DigiKey data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. DigiKey's terms of use restrict automated access to its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, part numbers, stock or lead times. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "query or category_id is required"; "filters apply inside a category: pass category_id (categories[].id of a search) with filters."; "url or digikey_part_number is required"; "search serves country us (digikey.com) and de (digikey.de); for digikey.ca use product ... and categories."; "country must be us (digikey.com, USD), ca (digikey.ca, CAD) or de (digikey.de, EUR)."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged what it spent: an unknown product, DigiKey part number or category id.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api).
- `502` and `503` mean DigiKey data was temporarily unavailable. They are not charged.
- Calls usually take 10-40 seconds, up to about 200. Allow a client timeout of at least 300 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.110.0
npm install scavio@0.111.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: res } = await scavio.digikey.search({ query: "LM317" });
const { data: rows } = await scavio.digikey.search({ query: "LM317", category_id: "699", filters: { "-2": ["5"] } });
const { data: part } = await scavio.digikey.product({ digikey_part_number: "497-1575-5-ND" });
const { data: tree } = await scavio.digikey.categories({ category_id: 32 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.digikey.search(...)`, `product` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 3 endpoints as tools: `search_digikey`, `get_digikey_product` and `get_digikey_categories`. DigiKey is opt-in: add `digikey` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.110.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,digikey"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/digikey-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api), [product](https://scavio.dev/docs/digikey-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api), [categories](https://scavio.dev/docs/digikey-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api). Platform page: [scavio.dev/digikey-api](https://scavio.dev/digikey-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=digikey-api).
