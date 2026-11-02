# PetSmart Product Data API - Prices, Autoship, Store Stock, Deals

Search PetSmart pet food and supplies with the national price, list and sale price, price range across sizes, rating, review count, promotion text and how many PetSmart stores stock each item, up to 40 per page. Read one product with every size and flavor: SKU, UPC, sale price and its end date, the Autoship discount with first-order and recurring price, and the ship, pickup and same-day options. Find the 12 stores nearest a ZIP with hours and services, get live unit counts for up to 20 SKUs at one store or for 20 store and SKU pairs, and list the Sale section with its current sale events. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find dog, cat, fish, bird, reptile or small-pet products at PetSmart by keyword
- Check a PetSmart product's price, sale price, or the price of each size and flavor
- Check the Autoship price of a PetSmart product, first order and recurring
- Check how many units a PetSmart store has of an item, or which nearby store has it
- Find PetSmart stores near a ZIP code, with hours and services (grooming, PetsHotel, training)
- List what is on sale at PetSmart, for one pet or one sale event
- Compare PetSmart prices with Petco, Chewy or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All PetSmart endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/petsmart/search` | 1 | Up to 40 products per page: SKU, web style id, name, brand, UPC, price, original and sale price, price range across sizes, rating, review count, image, size, variation summary, category, pets, promotions, `stores_in_stock` (how many stores stock it), pickup and Autoship eligibility, URL. With `store_id`, only items in stock at that store |
| `POST /api/v1/petsmart/product` | 1 | One product by web style id, SKU or URL, with every variant (size and flavor): SKU, UPC, price, original and sale price, sale end date, Autoship discount with first-order and recurring price, ship-to-home stock, pickup and same-day options, images, promotions. Plus brand, rating, review count, categories, description and option lists |
| `POST /api/v1/petsmart/stores` | 1 | The 12 stores nearest a US ZIP: store number, name, address, phone, coordinates, distance, time zone, the next 7 days of hours and services. With `sku`, each store also carries its unit count of that SKU |
| `POST /api/v1/petsmart/store-stock` | 1 | Up to 20 SKUs at ONE store: units for in-store pickup there, units to ship to home, and a nearby alternate store with its count when the store has none. Plus the store's address, page URL and pickup options |
| `POST /api/v1/petsmart/availability` | 1 | Up to 20 store and SKU pairs, mixed freely (many stores, many SKUs): `quantity` and `in_stock` per pair |
| `POST /api/v1/petsmart/deals` | 1 | The Sale section, up to 40 per page, in the search row shape, plus the current sale events with approximate product counts. Filter by pet, sale event, keywords or store |

## Workflow

1. **Find the product:** call `/petsmart/search` with `query`. Each row has a `sku` (one size or flavor) and a `web_style_id` (the whole product).
2. **Every size and its price:** call `/petsmart/product` with the `web_style_id` (or a `sku` or the product `url`). Each `variants[]` row has its own `sku`, price and Autoship block.
3. **Nearby stores:** call `/petsmart/stores` with the user's `zip`. Pass one `sku` too and each store carries its unit count of it, so one call answers "which store near me has this".
4. **Many SKUs at one store:** call `/petsmart/store-stock` with `store_id` and up to 20 `skus` (for example every variant of a product).
5. **Many stores at once, or a mix:** call `/petsmart/availability` with up to 20 `{store_id, sku}` pairs.
6. **What is on sale:** call `/petsmart/deals`, optionally with `pet`. Its `events[]` names the running sale events; pass one back as `event` to list only that sale.

`store-stock` vs `availability`: `store-stock` is one store and many SKUs, and adds ship-to-home stock, an alternate nearby store, and the store's details; an unknown store number there is a `404`. `availability` takes any mix of stores and SKUs but returns only `quantity` and `in_stock`, and an unknown store or SKU reads `0`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-100) |
| `limit` | integer | 40 | Results per page, 1-40 |
| `store_id` | string | - | PetSmart store number from `/stores`. Lists only products in stock at that store; each row then carries `in_stock_at_store` |
| `sort` | string | `relevance` | `relevance`, `best_sellers`, `price_low`, `price_high`, `top_rated` or `new_arrivals` |

### Product (`/product`)

Pass exactly one of the three.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `web_style_id` | string | one of | The number at the end of a product URL (`...-570.html`), a search row's `web_style_id`. One id covers every size and flavor |
| `sku` | string | one of | One size or flavor, a search row's `sku` (4-9 digits). Returns the whole product it belongs to, with `requested_sku` set |
| `url` | string | one of | A petsmart.com product page URL |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP code (5 digits or ZIP+4) |
| `radius` | integer | 30 | Search radius in miles, 1-100 |
| `sku` | string | - | A SKU. Each store then carries `quantity` and `in_stock` for it |

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | PetSmart store number from `/stores` |
| `skus` | string[] | required | 1-20 SKUs, for example every `variants[].sku` of a product |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pairs` | object[] | required | 1-20 `{ "store_id": "1658", "sku": "5252900" }` pairs, stores and SKUs mixed freely |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pet` | string | - | `dog`, `cat`, `fish`, `small_pet`, `reptile` or `bird` |
| `event` | string | - | One sale event, by its exact name from the `events[]` of a previous deals answer (`"Sale > November > Dog Sale"`). Events change with the season |
| `query` | string | - | Keywords to search within the sale |
| `page` | integer | 1 | 1-based page (1-100) |
| `limit` | integer | 40 | Results per page, 1-40 |
| `store_id` | string | - | Only products in stock at this store |
| `sort` | string | `relevance` | Same values as search |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/petsmart/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pairs": [{"store_id": "1658", "sku": "5252900"}, {"store_id": "2528", "sku": "5252900"}]}'
```

Captured response (a 30 lb bag of Purina Pro Plan dry dog food at two Chicago-area stores):

```json
{
  "data": {
    "count": 2,
    "in_stock_count": 2,
    "results": [
      { "store_id": "1658", "sku": "5252900", "quantity": 8, "in_stock": true },
      { "store_id": "2528", "sku": "5252900", "quantity": 4, "in_stock": true }
    ]
  },
  "response_time": 3257,
  "credits_used": 1
}
```

A captured `/store-stock` item for `{"store_id": "1658", "skus": ["5252900", ...]}`:

```json
{
  "sku": "5252900",
  "store_quantity": 8,
  "in_stock_at_store": true,
  "ship_to_home_quantity": 9816,
  "ship_to_home_in_stock": true,
  "alt_store_id": null,
  "alt_store_quantity": null
}
```

A captured `/product` variant for `{"web_style_id": "36648"}`, the 4 lb size on sale (images and promotions trimmed):

```json
{
  "sku": "5339374",
  "name": "Purina Pro Plan Sensitive Skin and Stomach Dry Dog Food Adult Salmon & Rice Formula Digestive Health",
  "upc": "038100100757",
  "options": { "flavor": "Salmon & Rice", "size": "4 Lb" },
  "price": 20.68,
  "original_price": 21.99,
  "sale_price": 20.68,
  "sale_valid_until": "9999-12-31T07:00:00.000Z",
  "on_sale": true,
  "autoship": null,
  "ship_to_home": { "in_stock": true, "one_time": true, "autoship": true, "max_quantity": 500 },
  "store_pickup": { "one_time": true, "autoship": true, "max_quantity": 500 },
  "same_day_delivery": { "one_time": true, "autoship": true, "max_quantity": 500 },
  "is_live_pet": false,
  "treats_points": 10
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def petsmart(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/petsmart/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find the product (1 credit)
row = petsmart("search", {"query": "dog food", "sort": "best_sellers", "limit": 10})["products"][0]
print(row["name"], row["price"], "in", row["stores_in_stock"], "stores")

# 2. Every size, with sale and Autoship prices (1 credit)
product = petsmart("product", {"web_style_id": row["web_style_id"]})
for v in product["variants"]:
    auto = v["autoship"] or {}
    print(v["options"].get("size"), v["price"], "sale" if v["on_sale"] else "", auto.get("first_order_price"))

# 3. Stores near a ZIP with their count of one SKU (1 credit)
stores = petsmart("stores", {"zip": "60601", "sku": row["sku"]})["stores"]
for s in stores:
    print(s["name"], s["distance_miles"], "mi:", s["quantity"], "units")

# 4. Every size at the nearest store in one call (1 credit)
skus = [v["sku"] for v in product["variants"]][:20]
for it in petsmart("store-stock", {"store_id": stores[0]["store_id"], "skus": skus})["items"]:
    print(it["sku"], it["store_quantity"], it["alt_store_id"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when PetSmart answered.

- **search** - `query`, `store_id`, `sort`, `page`, `limit`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `sku`, `web_style_id`, `name`, `brand`, `upc`, `price`, `original_price`, `sale_price`, `on_sale`, `price_range` {`min`, `max`}, `rating`, `review_count`, `image`, `size`, `variations[]`, `category`, `pets[]`, `stores_in_stock`, `in_stock_at_store` (only with `store_id`), `pickup_eligible`, `in_store_only`, `online_only`, `autoship_eligible`, `promotions[]` {`text`, `start`, `end`}, `url`).
- **product** - `web_style_id`, `default_sku`, `requested_sku`, `name`, `brand`, `brand_url`, `rating`, `review_count`, `primary_category`, `categories[]`, `description`, `price_range` {`min`, `max`}, `options` {option: [values]}, `variant_count`, `variants[]` (`sku`, `name`, `upc`, `options` {option: value}, `price`, `original_price`, `sale_price`, `sale_valid_until`, `on_sale`, `autoship` {`discount`, `first_order_price`, `recurring_price`} or null, `ship_to_home` {`in_stock`, `one_time`, `autoship`, `max_quantity`}, `store_pickup` {`one_time`, `autoship`, `max_quantity`}, `same_day_delivery` {same}, `images[]`, `promotions[]` {`text`, `type`, `start`, `end`}, `is_live_pet`, `treats_points`), `url`.
- **stores** - `zip`, `radius_miles`, `sku`, `count`, `stores_in_stock` (only with `sku`), `stores[]` (`store_id`, `name`, `address`, `address2`, `city`, `state`, `zip`, `phone`, `latitude`, `longitude`, `distance_miles`, `time_zone`, `google_place_id`, `opening_date`, `hours[]` {`date`, `day`, `closed`, `open`, `close`}, `services[]`, and with `sku`: `quantity`, `in_stock`).
- **store-stock** - `store_id`, `store` {`name`, `address`, `address2`, `city`, `state`, `zip`, `phone`, `url`, `offers_pickup`, `offers_curbside_pickup`}, `count`, `in_stock_count`, `items[]` (`sku`, `store_quantity`, `in_stock_at_store`, `ship_to_home_quantity`, `ship_to_home_in_stock`, `alt_store_id`, `alt_store_quantity`).
- **availability** - `count`, `in_stock_count`, `results[]` (`store_id`, `sku`, `quantity`, `in_stock`).
- **deals** - `pet`, `event`, `query`, `store_id`, `sort`, `page`, `limit`, `total_results`, `total_pages`, `count`, `products[]` (the search row shape), `events[]` {`name`, `product_count`}.

## Guardrails

- Prices are in dollars and national: `77.99` is $77.99 at every store and online. No endpoint returns a store-specific price, so never claim one.
- `price` is what the item sells for now, `original_price` the list price, `sale_price` the reduced price or `null`. `on_sale` means `sale_price` is below `original_price`. A `sale_valid_until` of `9999-12-31` means the sale has no announced end date.
- Autoship is per variant: `autoship.first_order_price` is the first Autoship order and `recurring_price` every order after it, with PetSmart's `discount` label. `autoship` is `null` when no Autoship offer is running for that variant, even if `autoship_eligible` is true; quote the one-time price then.
- Stock is per store and live: `quantity` and `store_quantity` are units at that store. `stores_in_stock` on a search row is how many stores carry the item, not a unit count.
- `store-stock` covers one store and adds ship-to-home stock and an alternate store (`alt_store_id`, `alt_store_quantity`) when that store has none; an unknown store number is a `404`. `availability` mixes stores and SKUs, but an unknown store or SKU reads `0`, the same as out of stock, so check the store number from `/stores` before telling the user an item is out of stock.
- `ship_to_home_quantity` is the online warehouse (chain-wide), not the store.
- The Sale section also holds points, Autoship and free-delivery promotions, so most `/deals` rows are not price cuts: use `on_sale` to find the rows whose price is actually reduced. `promotions[].text` is the site's own wording; quote it as written and do not compute a final price from it.
- Without `store_id`, search and deals list every product regardless of local stock.
- `/stores` returns at most the 12 nearest stores; an unknown ZIP returns an empty list, not an error.
- Never fabricate prices, stock or promotions. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, none or more than one of `web_style_id` / `sku` / `url`, a non-PetSmart URL, a ZIP that is not 5 digits, an unknown `sort` or `pet`, `limit` above 40, or more than 20 `skus` or `pairs`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product or SKU; on `/store-stock` it means an unknown store number (find one with `/stores`). Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data).
- `502` or `503` means PetSmart is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.33.0
npm install scavio@0.33.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.petsmart.search({ query: "dog food", sort: "best_sellers" });
const { data: item } = await scavio.petsmart.product({ web_style_id: found.products[0].web_style_id });
const { data: near } = await scavio.petsmart.stores({ zip: "60601", sku: found.products[0].sku });
const stock = await scavio.petsmart.storeStock({
  store_id: near.stores[0].store_id,
  skus: item.variants.map((v) => v.sku),
});
const deals = await scavio.petsmart.deals({ pet: "cat" });
```

MCP: the Scavio MCP server exposes all 6 endpoints as tools (`search_petsmart`, `get_petsmart_product`, `get_petsmart_stores`, `get_petsmart_store_stock`, `get_petsmart_availability`, `get_petsmart_deals`). PetSmart is opt-in: add `petsmart` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.31.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,petsmart"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/petsmart-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data), [product](https://scavio.dev/docs/petsmart-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data), [stores](https://scavio.dev/docs/petsmart-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data), [store stock](https://scavio.dev/docs/petsmart-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data), [availability](https://scavio.dev/docs/petsmart-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data), [deals](https://scavio.dev/docs/petsmart-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data). Overview: [PetSmart API](https://scavio.dev/petsmart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data).
