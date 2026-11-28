# Ferguson API - Plumbing, HVAC and Waterworks Products, Part Numbers, Specs, Prices

Read Ferguson (ferguson.com, the US plumbing, HVAC and waterworks distributor): keyword search and category listings with item numbers, part numbers, brands, ratings and shipping flags, and one product with its price, list price, package quantities, variants, specifications, certifications and documents. US only, USD, as shown to a visitor who is not signed in.

**The job this skill is for: look up a Ferguson item - what it is, its part numbers and specs, how it is packaged, and the price Ferguson shows for it.** On 2026-11-28 item 4606091, an FNW 1/2 in. brass full port press ball valve (Ferguson part FNWX432D, UPC 781889249888), read $33.24 each, sold in inner packs of 40, cases of 80 and pallets of 2,800.

Six limits shape every answer, so say them plainly:
- **Credits differ by endpoint.** Search and category cost 2 credits; product costs 4 (the page and its price; 2 when the page names no price). A keyword Ferguson sends to a category, asked for a later page or `best_selling`, can cost 4. `credits_used` in the response is the truth. A not-found (`404`) is charged 2; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Listings carry no prices.** Ferguson fills prices in after its results page loads, so search and category items have no price. Ask product with the item number for its price.
- **Some prices are for signed-in customers only.** `price_shown` false on a listing item, and `price` null with a `note` on the product, mean Ferguson shows that price only to signed-in customers. Scavio returns no hidden or account price.
- **Prices follow the region Ferguson picks.** The price is the one Ferguson shows for the region it assigns the visitor, so the same item can read a different price on another read. Quote it with the `fetched_at` time.
- **No store stock, reviews or questions.** Store pickup counts depend on the store Ferguson picks for the visitor and are not returned.
- **Slow listings.** Search and category usually take 30-60 seconds (allow at least 240); product 10-25 (allow at least 180).

Ferguson offers no public, self-serve API for its product catalogue. The products are shown on ferguson.com, and this skill reads those public pages with one Scavio key.

See also: SupplyHouse.com `supplyhouse-api` (US online plumbing, HVAC and electrical supply), Home Depot `home-depot-product-data`, Lowe's `lowes-product-data`, Zoro `zoro-api`.

## When to trigger

Use this skill when the user asks to:
- Look up a Ferguson item by item number (`4606091`) or ferguson.com link: name, brand, part numbers, UPC, specs, documents and price
- Search ferguson.com by keyword ("pex tubing", "1/2 ball valve", a brand or a part number) and list the items with their item and part numbers
- Walk a Ferguson category (`water-heaters/tankless-water-heaters`) with its breadcrumbs and subcategories
- Check how an item is packaged (Each, Inner Pack, Case, Pallet) and which variants (sizes) it comes in

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. A search or category call costs 2 credits and a product call 4, so 50 credits cover 25 searches or 12 product lookups.

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
| `POST /api/v1/ferguson/search` | Keyword search, 24 a page, best match or best selling: items with item number, part numbers, brand, rating, shipping flags; the matching categories | 2 (4 for a later page or best_selling of a keyword Ferguson sends to a category) |
| `POST /api/v1/ferguson/category` | One category by path, paged and sorted like search, with breadcrumbs and subcategories | 2 |
| `POST /api/v1/ferguson/product` | One product by item number or link: price, list price, price per unit, package quantities, variants, specs, certifications, documents | 4 (2 when the page names no price) |

US only: English, prices in USD, never Pro or account pricing.

## Workflow

1. **Find items.** `/search` with `q`; `categories[].path` names the matching categories. A keyword Ferguson sends straight to a category answers that category's products and says so in `redirected_to`.
2. **Browse.** `/category` with `category` set to a path (`categories[].path`, `subcategories[].path`, or the part after `/category/` in a ferguson.com link).
3. **More rows.** Send `page` (1-100) while `has_more` is true; `sort` is `best_match` (default) or `best_selling`.
4. **One item.** `/product` with `item` (e.g. `4606091`) or `url` (a ferguson.com /product/ link) for its price, packaging, variants, specs and documents. Check `price_shown` on a listing item first: false means the product answer will carry `price` null.

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `q` | search | Keywords as a buyer types them on ferguson.com (product type, brand, part or item number), 1-200 characters |
| `category` | category | A Ferguson category path (e.g. `water-heaters/tankless-water-heaters`) or a ferguson.com /category/ link |
| `page` | search, category | Results page, 1-100 (24 products a page) |
| `sort` | search, category | `best_match` (default, Ferguson's own order) or `best_selling` |
| `item` | product | A Ferguson item number (`items[].item`: the digits after Item # on ferguson.com) |
| `url` | product | A ferguson.com /product/ link, instead of `item` |

## Examples

### One product

Request `{"item": "4606091"}` (4 credits), abridged:

```json
{
  "item": "4606091",
  "name": "1/2 in. Brass Full Port Press Ball Valve",
  "brand": "FNW®",
  "collection": "Figure X432",
  "part_number": "FNWX432D",
  "manufacturer_part_number": "FNWX432D",
  "upc": "781889249888",
  "price_shown": true,
  "price": 33.24,
  "list_price": 33.24,
  "price_per_unit": 33.24,
  "currency": "USD",
  "call_for_pricing": false,
  "note": null,
  "unit_of_measure": "EACH",
  "order_multiple": 1,
  "package_quantities": [{ "package": "Each", "quantity": 1 }, { "package": "Inner Pack", "quantity": 40 }, { "package": "Case", "quantity": 80 }, { "package": "Pallet", "quantity": 2800 }],
  "variants": [{ "item": "4606091", "attribute": "Valve Size", "value": "1/2 in", "selected": true, "price": null }, { "item": "4606092", "attribute": "Valve Size", "value": "3/4 in", "selected": false, "price": null }],
  "certifications": ["Lead Law Compliant"],
  "prop65_warning": true
}
```

### One search item

Request `{"q": "pex tubing"}` (2 credits): `total` 253 over 11 pages, 8 `categories` (Pipe & Tubing 158, Tools 48, Pipe Fittings 24 ...). The first item, abridged:

```json
{
  "position": 1,
  "item": "1897383",
  "name": "1/2 in. x 20 ft. PEX Tubing in White",
  "brand": "Uponor",
  "collection": "AquaPEX®",
  "part_number": "UF1930500",
  "manufacturer_part_number": "F1930500",
  "rating": 3.6,
  "variant_attribute": { "name": "PipeTubing Size", "values": ["1/2 in", "3/4 in", "1 in", "1-1/4 in", "1-1/2 in", "2 in", "2-1/2 in", "3 in"], "selected": "1/2 in" },
  "unit_of_measure": "per 20 FOOT",
  "price_shown": true,
  "availability": { "can_ship": true, "has_shipping_inventory": true, "shipping_restricted": false, "ready_to_order": true, "tariff_applies": false }
}
```

A category answer for `water-heaters/tankless-water-heaters` read `total` 138 over 6 pages, with `breadcrumbs` All Products > Water Heaters > Tankless Water Heaters; 5 of its first 24 items had `price_shown` false.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ferguson(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/ferguson/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search (2 credits; listings carry no prices)
res = ferguson("search", {"q": "pex tubing"})["data"]
for it in res["items"][:5]:
    print(it["item"], it["name"], it["brand"], it["part_number"], it["price_shown"])

# 2. One product (4 credits; 2 when the page names no price)
item = ferguson("product", {"item": "4606091"})["data"]
print(item["name"], item["price"], item["unit_of_measure"], item["note"])
for pk in item["package_quantities"]:
    print(pk["package"], pk["quantity"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `query`, `redirected_to` {`category_path`, `name`, `url`}, `page`, `page_size`, `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `item`, `name`, `brand`, `collection`, `url`, `image`, `part_number`, `manufacturer_part_number`, `family_id`, `rating`, `variant_attribute` {`name`, `values`, `selected`}, `unit_of_measure`, `price_shown`, `availability` {`can_ship`, `has_shipping_inventory`, `shipping_restricted`, `ready_to_order`, `tariff_applies`}, `compliance`}, `categories[]` {`name`, `path`, `count`}, `notes`.
- **category** - `category_path`, `name`, `url`, `breadcrumbs[]` {`name`, `path`}, `page`, `page_size`, `sort`, `total`, `total_pages`, `has_more`, `count`, `items[]` (as search), `subcategories[]` {`name`, `path`, `count`}, `notes`.
- **product** - `item`, `name`, `brand`, `collection`, `url`, `part_number`, `manufacturer_part_number`, `upc`, `family_id`, `rating`, `breadcrumbs`, `images`, `price_shown`, `price`, `list_price`, `price_per_unit`, `currency`, `call_for_pricing`, `note`, `unit_of_measure`, `order_multiple`, `max_order_quantity`, `package_quantities[]` {`package`, `quantity`}, `variants[]` {`item`, `attribute`, `value`, `selected`, `price`}, `specs[]` {`group`, `items[]` {`name`, `value`}}, `certifications`, `documents[]` {`type`, `url`}, `has_parts_or_replacements`, `prop65_warning`, `notes`.

## Guardrails

- Name it "Ferguson (ferguson.com, the US plumbing, HVAC and waterworks distributor)" on first mention.
- Prices: quote `price` per `unit_of_measure` in USD with the `fetched_at` time, and say it is the price shown to a visitor who is not signed in for the region Ferguson assigned. Package prices are not computed: never multiply `price` by a package quantity and present it as Ferguson's price.
- Hidden prices: when `price` is null, say why from `note` (signed-in customers only, or Call for Pricing). Never estimate or infer a hidden price.
- Use: keep any use descriptive - looking up one item's details, part numbers, specs, packaging and price for a purchase decision.
- Links and content: refer to items by Ferguson item number; do not republish Ferguson's photos or product copy, and do not use the answers to copy or rebuild its catalogue.
- Not available: store stock or pickup counts, reviews, questions, search suggestions, Pro or account pricing, price history, ordering.
- Terms: Scavio does not store Ferguson data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Ferguson's terms of use restrict automated use of its site and its prices; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, item numbers or specifications. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "q is required"; "q must contain letters or digits."; "category is required"; "item or url is required"; "Pass item or url, not both."; "sort must be one of best_match, best_selling."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 2 credits: an unknown item number or category path.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api).
- `502` and `503` mean Ferguson data was temporarily unavailable. They are not charged.
- Search and category usually take 30-60 seconds; product 10-25. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.109.0
npm install scavio@0.110.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: res } = await scavio.ferguson.search({ q: "pex tubing" });
const { data: cat } = await scavio.ferguson.category({ category: "water-heaters/tankless-water-heaters", sort: "best_selling" });
const { data: item } = await scavio.ferguson.product({ item: "4606091" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.ferguson.search(...)`, `category` and `product`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 3 endpoints as tools: `search_ferguson`, `get_ferguson_category` and `get_ferguson_product`. Ferguson is opt-in: add `ferguson` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.109.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,ferguson"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/ferguson-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api), [category](https://scavio.dev/docs/ferguson-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api), [product](https://scavio.dev/docs/ferguson-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api). Platform page: [scavio.dev/ferguson-api](https://scavio.dev/ferguson-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ferguson-api).
