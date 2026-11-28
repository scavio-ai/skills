---
name: global-industrial-api
description: Global Industrial API for Global Industrial (globalindustrial.com, the US industrial-equipment and MRO supplier; Global Industrial Canada at globalindustrial.ca in CAD) - what a hand truck, drum truck, pallet jack, case of gloves or any industrial, MRO or facility item costs at Global Industrial today, per selling unit and per piece, with the site's quantity breaks, the price before a promotion or clearance, the lead time and the freight flag, as globalindustrial.com shows it to a visitor who is not signed in (on 2026-11-28 the Wesco Dispenser Truck 240083 for poly and fiber drums read $399.95, shipping in 15 business days by truck freight; a case of Ammex GWRBN industrial nitrile gloves, 10 boxes of 100, read $339.50 a case or $33.95 a box; a Metro stainless wire shelf truck in clearance showed "See price in cart" under the manufacturer's minimum advertised price policy; the Carts & Trucks clearance held 65 products; Global Industrial Canada listed its 5,500 lb manual pallet jack at CAD 409.95 against CAD 515) with price, price type (regular, promotional, clearance), was price, savings, pack quantity, unit price, quantity breaks, minimum and maximum order, availability text, lead time, LTL freight, free shipping, hazardous and non-returnable flags, rating, review count, highlights and variants; keyword, item number or manufacturer part number search (a keyword the site sends to a category or a product is followed), category listings grouped by product group, brand listings and the clearance section, up to 42 products per listing with the full total; one product with UNSPSC, distributor part number, specs with units, manuals and spec sheets. 5 endpoints, 1 credit each. msrp is not shown on the page and can sit below the price; MAP items carry no price; no sort, reviews text, questions, stock counts or price history.
version: 1.0.0
tags: global-industrial, globalindustrial, globalindustrial-com, globalindustrial-ca, global-industrial-api, global-industrial-canada, global-industrial-prices, global-industrial-search, global-industrial-product, global-industrial-category, global-industrial-brand, global-industrial-clearance, global-industrial-quantity-breaks, global-industrial-lead-time, industrial-supply, industrial-supplies, industrial-equipment, mro, mro-supplies, mro-prices, mro-price-monitoring, facility-supplies, material-handling, hand-trucks, drum-trucks, pallet-jacks, carts-and-trucks, shelving, safety-supplies, nitrile-gloves, janitorial-supplies, b2b-ecommerce, b2b-prices, procurement, purchasing, part-number-lookup, manufacturer-part-number, catalog-matching, unspsc, quantity-breaks, volume-pricing, case-price, unit-price, ltl-freight, map-pricing, price-monitoring, price-tracking, product-data, us-retail, usd, cad, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/globalindustrial-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api
---

# Global Industrial API - Industrial and MRO Prices, Quantity Breaks, Lead Times, Clearance

Read Global Industrial (globalindustrial.com, the US industrial-equipment and MRO supplier; Global Industrial Canada at globalindustrial.ca): keyword, item number and part number search, category listings grouped by product group, brand listings, the clearance section, and one product with its quantity breaks, specs and documents. www.globalindustrial.com (USD) and www.globalindustrial.ca (`market` ca, CAD, English), as shown to a visitor who is not signed in.

**The job this skill is for: what an industrial or MRO item costs at Global Industrial today, per selling unit and per piece, and how fast it ships.** Every item carries the price of one selling unit, the pieces in it (`package_quantity`) and the price per piece (`unit_price`), plus the site's quantity breaks where it gives them. On 2026-11-28 a case of Ammex GWRBN industrial-grade textured nitrile gloves (XXL, 100 per box, 10 boxes per case) read $339.50 a case and $33.95 a box, shipping within 1 business day. The Wesco Dispenser Truck 240083 for poly and fiber drums read $399.95, shipping in 15 business days by truck (LTL) freight.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Pack price and piece price, apart.** `price` is one selling unit as listed, `package_quantity` the pieces in it, `unit_price` the price per piece; `quantity_breaks` are the site's volume prices, counted in selling units.
- **MAP items show no price.** Where the manufacturer's minimum advertised price policy applies, Global Industrial shows "See price in cart" instead of a price: `map_pricing` and `price_in_cart` are true and the price fields are null; `map_price` is the advertised minimum as given.
- **msrp is not on the page.** `msrp` is the manufacturer's suggested retail price as Global Industrial records it; the page does not print it and it can sit below the price (the glove case above: msrp 28.50 against $33.95 a box). Never present it as a list price or a saving.
- **Listings are capped at 42.** A search, brand or clearance listing returns up to 42 products and `total` is the full count; a leaf category lists products by product group, at most 10 per group, and `group` lists every product of one group. Results come in the site's default order: there is no sort and no paging.
- **No reviews, questions or history.** `rating` and `review_count` are the site's summary; review text and questions are not returned. Stock is a flag and a shipping text, not a count. Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Global Industrial publishes no public developer API for its catalog or prices. Prices, lead times and specs are shown on globalindustrial.com, and this skill reads those public pages with one Scavio key.

See also: Zoro `zoro-api` and MSC Industrial Supply `msc-industrial-api` (US industrial and MRO supply), Staples `staples-ink-prices-api`, Tractor Supply `tractor-supply-prices-api`, Home Depot `home-depot-product-data`, Harbor Freight `harbor-freight-api`.

## When to trigger

Use this skill when the user asks to:
- Price an industrial, MRO or facility item at Global Industrial: price per selling unit, price per piece, quantity breaks, was price and savings
- Search globalindustrial.com by keyword ("nitrile gloves", "drum truck", "pallet jack"), by Global Industrial item number (`652508`) or by manufacturer part number (`240083`), optionally for one brand
- Match a catalog by part number: item number, manufacturer part number, distributor part number and UNSPSC code
- List a Global Industrial category (`/c/carts-trucks/hand_trucks/drum_trucks_cradles`) or department (`/t/carts-trucks`), one product group of it, or one brand's products (`Wesco`, `Valley Craft`)
- Read the clearance section, overall or for one clearance category or brand
- Read one product: availability text, lead time, LTL freight, hazardous and non-returnable flags, specs with units, manuals and spec sheets
- Price the same item in Global Industrial Canada (CAD)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api) - email or Google, no card required.
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
| `POST /api/v1/globalindustrial/search` | Keywords, an item number or a part number, optionally one brand: up to 42 products with total, or the category or product the site sends the keyword to (`landed_on`, `redirected_to`), with facets | 1 |
| `POST /api/v1/globalindustrial/category` | A category by path: a leaf category's products by product group (at most 10 per group, `group` for all of one group), or a broader category's subcategories; breadcrumbs and facets | 1 |
| `POST /api/v1/globalindustrial/brand` | One brand's products, up to 42, with the brand's full product count and its count per top-level category | 1 |
| `POST /api/v1/globalindustrial/product` | One product by link, slug, item number or manufacturer part number: prices, quantity breaks, availability, lead time, flags, specs with units, manuals and spec sheets | 1 |
| `POST /api/v1/globalindustrial/clearance` | The clearance section: clearance count per category and the page's featured products, or up to 42 clearance products of one clearance category or brand | 1 |

Every answer carries `store` (globalindustrial), `market` (us, ca), `host`, `country`, `currency` (USD, CAD) and `language`, and most carry `notes`.

## Prices: pack price, piece price, quantity breaks and MAP

| Field | Meaning |
|---|---|
| `price` | One selling unit as listed, in USD or CAD ($339.50 for the glove case below) |
| `package_quantity` | Pieces in one selling unit (10 boxes) |
| `unit_price` | The price per piece ($33.95 a box) |
| `quantity_breaks[]` | The site's volume prices: `{qty_start, qty_end, unit_price, package_price}`, quantities in selling units |
| `price_type` | regular, promotional or clearance |
| `was_price`, `savings_percent` | The price before a promotion or clearance, and the saving the site shows |
| `clearance_price`, `sale_price` | The clearance or sale price where the site gives one |
| `map_pricing`, `price_in_cart`, `map_price` | A MAP item: "See price in cart" on the page, price fields null, `map_price` the advertised minimum as given |
| `call_for_price` | The site asks to call for a price |
| `msrp` | The manufacturer's suggested retail price as Global Industrial records it; not printed on the page and can sit below the price |
| `min_order_quantity`, `max_order_quantity` | Order limits where the site sets them (clearance items often carry a maximum) |

- Quote "Ammex GWRBN industrial nitrile gloves, XXL, case of 10 boxes of 100: $339.50 a case, $33.95 a box, on globalindustrial.com on 2026-11-28", with the date and which unit the price is for.
- Quote `quantity_breaks`, `was_price` and `savings_percent` exactly as given; never compute a break or a saving yourself, never present `msrp` as a list price, and never judge a price as a good deal. For a MAP item say the site shows the price in the cart; do not present `map_price` as the selling price.

## Workflow

1. **Find products.** `/search` with `query` (keywords, an item number or a manufacturer part number), optionally `brand`. Read `landed_on`: `search` (a listing), `category` (the site sent the keyword to a category: items are listed by product group) or `product` (the site opened one product).
2. **Browse.** `/category` with `path` (`items[].category_path`, `subcategories[].path`, a `/t/...` department), optionally `brand` or `group` (`groups[].group_id`) for every product of one group. `/brand` with `brand` as Global Industrial writes it (`items[].brand`).
3. **One product.** `/product` with `url` (`items[].url`, a `/p/...` path or `items[].slug`) or `item` (an item number or a manufacturer part number).
4. **Clearance.** `/clearance` with `{}` for the counts per clearance category and the featured products, then `category` (`categories[].id`, e.g. `PRIME30`) and / or `brand` for up to 42 clearance products.
5. **Canada.** Add `market` `ca` to any call for www.globalindustrial.ca in CAD.
6. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Description |
|---|---|
| `query` (required) | Keywords, a Global Industrial item number (`652508`) or a manufacturer part number (`240083`), 1-120 characters |
| `brand` | Limit to one brand as Global Industrial writes it (`Wesco`, `Global Industrial`, `Valley Craft`) |
| `market` | `us` (default, globalindustrial.com, USD) or `ca` (globalindustrial.ca, CAD, English) |

### Category (`/category`), brand (`/brand`) and clearance (`/clearance`)

| Parameter | Description |
|---|---|
| `path` (category, required) | A category path (`/c/carts-trucks/hand_trucks/drum_trucks_cradles`, as `subcategories[].path` or `items[].category_path` give it), a department path (`/t/carts-trucks`) or a link to one |
| `brand` (brand, required; category and clearance optional) | A brand as Global Industrial writes it; on a category or clearance, that brand's products only |
| `group` (category) | A product group of a leaf category (`groups[].group_id`, e.g. `42311`): every product of that group |
| `category` (clearance) | A clearance category id (`categories[].id`, e.g. `PRIME30` for Carts & Trucks) |
| `market` | `us` (default) or `ca` |

### Product (`/product`)

Send `url` (a product link, a `/p/<name>` path or `items[].slug`) or `item` (`items[].item_number` or a manufacturer part number), not both, with `market` optional.

## Examples

### One search item

Request `{"query": "nitrile gloves 6 mil"}` (1 credit): `landed_on` search, `total` 13, 13 items, facets such as `brand`, `attr_size`, `attr_material` and `price`. One item, abridged:

```json
{
  "position": 3,
  "item_number": "B2238667",
  "name": "Ammex® GWRBN Gloveworks Industrial Grade Textured Nitrile Gloves, Blue, XXL, 100/Box - Pkg Qty 10",
  "brand": "Ammex",
  "manufacturer_part_number": "GWRBN49100",
  "distributor_part_number": "GWRBN49100",
  "unspsc": "42132205",
  "product_group": { "group_id": 18355, "name": "Nitrile Gloves" },
  "category": "Disposable Gloves",
  "category_path": "/c/safety/gloves_sleeves/disposable_gloves",
  "currency": "USD",
  "price": 339.5,
  "price_type": "regular",
  "was_price": null,
  "msrp": 28.5,
  "map_pricing": false,
  "package_quantity": 10,
  "unit_price": 33.95,
  "quantity_breaks": [{ "qty_start": 1, "qty_end": 10000, "unit_price": 33.95, "package_price": 339.5 }],
  "in_stock": true,
  "availability": "Ships within 1 Business Day",
  "lead_time_days": 0,
  "ships_ltl_freight": false,
  "non_returnable": true
}
```

Here `msrp` (28.50) is below the price per box: it is the figure Global Industrial records, not a price the page shows. `{"query": "nitrile gloves"}` was sent by the site to the category Disposable Gloves (`landed_on` category, `redirected_to` `/c/safety/gloves_sleeves/disposable_gloves`): `total` 79 in 6 product groups (Nitrile Gloves 48, Vinyl Gloves 14, Latex Gloves 13, ...), 34 items at most 10 per group.

### One product

Request `{"url": "dispenser-truck-poly-drums"}` (1 credit), abridged:

```json
{
  "item_number": "652508",
  "name": "Wesco® Dispenser Truck 240083 for Poly & Fiber Drums",
  "brand": "Wesco",
  "manufacturer_part_number": "240083",
  "unspsc": "24101904",
  "product_group": { "group_id": 42372, "name": "Drum Trucks for Poly & Fiber Drums" },
  "category_path": "/c/carts-trucks/hand_trucks/drum_trucks_cradles",
  "currency": "USD",
  "price": 399.95,
  "price_type": "regular",
  "package_quantity": 1,
  "unit_price": 399.95,
  "in_stock": true,
  "availability": "Ships in 15 Business Days",
  "lead_time_days": 15,
  "ships_ltl_freight": true,
  "best_seller": true,
  "rating": 5,
  "review_count": 2,
  "launch_date": "2004-12-02"
}
```

The product also carried 3 `breadcrumbs` (Carts & Trucks > Hand Trucks > Drum Trucks & Cradles), 13 `specs` (Width 23-3/4 in, Depth 24-1/2 in, Height 58 in, Weight Capacity 1000 lbs, ...) and 1 document (Owner's Manual).

### Category, brand, clearance and Canada

- `/category` `{"path": "/c/carts-trucks/hand_trucks/drum_trucks_cradles"}`: a leaf category, `total` 162 in 11 product groups (4-Wheel Drum Trucks for Steel Drums 45, 2-Wheel Drum Trucks for Steel Drums 34, Drum Trucks for Poly & Fiber Drums 31, ...), 76 items; brand facet led by Valley Craft (106).
- `/brand` `{"brand": "Wesco"}`: `total` 438, 42 items, first the Wesco Spartan Jr. Aluminum 2-in-1 Hand Truck at $249.95; 369 of the brand's products in Carts & Trucks.
- `/clearance` `{"category": "PRIME30"}` (Carts & Trucks): `total` 65 in 9 clearance categories (Utility Carts 34, Cart & Truck Accessories 12, ...), 42 items, first the Interion Universal Dolly for Stacking Chairs at $115.95 clearance against $209.95. A Metro stainless wire shelf truck in the list carried `map_pricing` true, `price_in_cart` true and `price` null: the page shows "See price in cart".
- `/product` `{"url": "best-value-pallet-truck-pallet-jack-5500-lb-capacity-27-x-48", "market": "ca"}`: the Global Industrial Industrial Duty Manual Pallet Jack, 5500 lb capacity, CAD 409.95 promotional against CAD 515 (20 percent), ships within 1 business day by LTL freight, rated 5 over 399 reviews.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def gi(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/globalindustrial/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Search by keyword (1 credit)
hits = gi("search", {"query": "nitrile gloves 6 mil"})["data"]
for it in hits["items"][:5]:
    print(it["item_number"], it["name"], it["price"], it["package_quantity"], it["unit_price"], it["availability"])

# 2. Look a product up by manufacturer part number (1 credit)
item = gi("product", {"item": "240083"})["data"]
print(item["price"], item["lead_time_days"], item["ships_ltl_freight"], item["quantity_breaks"])

# 3. A product in Global Industrial Canada, in CAD (1 credit)
ca = gi("product", {"url": "best-value-pallet-truck-pallet-jack-5500-lb-capacity-27-x-48", "market": "ca"})["data"]
print(ca["currency"], ca["price"], ca["was_price"])

# Global Industrial prices change. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `market`, `host`, `country`, `currency` and `language`.

- **item fields** (listings and product) - `position`, `item_number`, `item_key`, `legacy_number`, `name`, `url`, `slug`, `image`, `brand`, `manufacturer_part_number`, `distributor_part_number`, `unspsc`, `product_group` {`group_id`, `name`}, `category`, `category_path`, `currency`, `price`, `price_type`, `was_price`, `savings_percent`, `msrp`, `clearance_price`, `sale_price`, `map_pricing`, `price_in_cart`, `map_price`, `call_for_price`, `package_quantity`, `unit_price`, `min_order_quantity`, `max_order_quantity`, `quantity_breaks[]` {`qty_start`, `qty_end`, `unit_price`, `package_price`}, `in_stock`, `availability`, `lead_time_days`, `ships_ltl_freight`, `free_shipping`, `hazardous`, `non_returnable`, `clearance`, `best_seller`, `new_arrival`, `rating`, `review_count`, `highlights[]` {`name`, `value`}, `variants` {`name`, `options[]` {`value`, `item_key`}}.
- **search** - `query`, `brand`, `landed_on` (search, category, product), `redirected_to`, `total`, `count`, `items[]`, `groups[]` {`group_id`, `name`, `count`, `shown`, `attributes`}, `subcategories[]` {`name`, `path`, `url`, `total`, `leaf`}, `category`, `facets[]` {`key`, `name`, `type`, `values`}, `notes`.
- **category** - `path`, `brand`, `group`, `redirected_to`, `category` {`name`, `path`, `url`, `leaf`, `breadcrumbs`}, `total`, `count`, `groups[]`, `items[]`, `subcategories[]`, `facets[]`, `filters_selected`, `notes`.
- **brand** - `brand`, `total`, `count`, `items[]`, `facets[]` (the brand's count per top-level category), `notes`.
- **product** - `requested`, the item fields, `summary`, `breadcrumbs[]` {`name`, `path`, `url`}, `images`, `specs[]` {`group`, `name`, `value`, `unit`}, `documents[]` {`type`, `title`, `url`}, `launch_date`, `notes`.
- **clearance** - `category`, `brand`, `total`, `count`, `categories[]` {`id`, `name`, `count`}, `sections[]` {`title`, `count`}, `items[]` (item fields plus `section`), `facets[]`, `filters_selected`, `notes`.

## Guardrails

- Name it "Global Industrial (globalindustrial.com, the US industrial-equipment and MRO supplier)" on first mention; "Global Industrial Canada (globalindustrial.ca)" for `market` ca. Accounts, carts, quotes and checkout are not read or made.
- Prices: quote `price` with what it is for (one selling unit of `package_quantity` pieces) and `unit_price` per piece, in USD or CAD, with the `fetched_at` date. Never present a case price as a piece price.
- MAP items: say the site shows the price in the cart ("See price in cart") under the manufacturer's minimum advertised price policy. Never present `map_price` as the price a buyer pays.
- msrp: say it is not shown on the page and can sit below the price. Never present it as a list price, a was price or a saving.
- Breaks and savings: quote `quantity_breaks`, `was_price` and `savings_percent` exactly as given; never compute them yourself.
- Stock: `in_stock`, `availability` and `lead_time_days` are the site's own flag and shipping text. Global Industrial shows no unit counts; never present any of them as a stock count.
- Listings: up to 42 products per listing (10 per product group in a leaf category); `total` is the full count. Say so when the user needs every product, and use `group` or narrower categories.
- Comparing Global Industrial with Zoro, MSC or another supplier: compare the same manufacturer part number, the same selling unit and the same date. Never call one supplier cheaper beyond the numbers shown.
- Images and copy: refer to products by `item_number` and manufacturer part number; do not republish Global Industrial's product photos or page copy, and keep any use descriptive.
- Not available: sorting, paging past 42, review text, questions, stock counts, account or contract pricing, shipping quotes, price history (poll and store), carts or checkout. This API cannot buy or request a quote.
- Terms: Scavio does not store Global Industrial data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Global Industrial's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, quantity breaks, lead times or specs. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "url or item is required"; "Pass url or item, not both."; "query must contain letters or digits."; "brand and group apply to a category (/c/...) path, not a department (/t/...)."; "path is a product link: use /api/v1/globalindustrial/product."; "category must be a clearance category id as a clearance answer lists it (categories[].id, e.g. PRIME30)."; a globalindustrial.ca link sent without `market` ca ("send market ca with it").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Global Industrial has no product <slug>.", "Global Industrial has no product with item or part number <item>.", "Global Industrial has no category <path>.", "Global Industrial lists no products for brand <brand> ...". A search with no products is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api).
- `502` and `503` mean Global Industrial data was temporarily unavailable ("Global Industrial is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- Calls usually take 5-60 seconds. Allow a client timeout of at least 180 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.107.0
npm install scavio@0.108.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.globalindustrial.search({ query: "nitrile gloves 6 mil" });
const { data: drums } = await scavio.globalindustrial.category({ path: "/c/carts-trucks/hand_trucks/drum_trucks_cradles", group: 42311 });
const { data: wesco } = await scavio.globalindustrial.brand({ brand: "Wesco" });
const { data: item } = await scavio.globalindustrial.product({ item: "652508" });
const { data: clearance } = await scavio.globalindustrial.clearance({ category: "PRIME30" });
const { data: canada } = await scavio.globalindustrial.product({ url: "best-value-pallet-truck-pallet-jack-5500-lb-capacity-27-x-48", market: "ca" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.globalindustrial.search(...)`, `category`, `brand`, `product` and `clearance`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_globalindustrial`, `get_globalindustrial_category`, `get_globalindustrial_brand`, `get_globalindustrial_product` and `get_globalindustrial_clearance`. Global Industrial is opt-in: add `globalindustrial` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.107.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,globalindustrial"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/globalindustrial-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api), [category](https://scavio.dev/docs/globalindustrial-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api), [brand](https://scavio.dev/docs/globalindustrial-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api), [product](https://scavio.dev/docs/globalindustrial-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api), [clearance](https://scavio.dev/docs/globalindustrial-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api). Platform page: [scavio.dev/globalindustrial-api](https://scavio.dev/globalindustrial-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=global-industrial-api).
