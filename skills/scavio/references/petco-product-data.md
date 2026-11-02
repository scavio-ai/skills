# Petco Product Data API - Prices, Repeat Delivery, Store Stock

Search Petco products or list any petco.com category, 48 per page, with price, list price and Repeat Delivery (autoship) price, rating, review count, brand, fulfillment flags (pickup in store, same-day delivery, autoship, in-store only), deal groups and every size or flavor variation with its own prices. Read one product with every variant: UPC, price, autoship and first-autoship price, online quantity, ingredients, guaranteed analysis, directions and specifications. Find Petco stores near a ZIP, and check units on hand for up to 10 products at one store in a single call. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find dog food, cat food, treats, litter or other pet supplies at Petco by keyword
- List the products in a Petco category, or the items in a Petco deals group
- Check a Petco product's price, sale (list) price, or Repeat Delivery autoship price
- Compare the price of every size or flavor of one Petco product
- Read a pet food's ingredients, guaranteed analysis, feeding directions or UPC
- Find Petco stores near a ZIP code with their hours
- Check whether a Petco store has an item on hand, and how many units
- Compare Petco prices with PetSmart, Chewy or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Petco endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/petco/search` | 1 | 48 products per page: name, brand, part number, `cat_entry_id`, URL, price, list price, autoship price, rating, review count, fulfillment flags, deal group ids and every size or flavor variation with its own prices. Facets with counts and the categories the matches fall into |
| `POST /api/v1/petco/category` | 1 | The same 48-per-page listing for one petco.com category path (`dog/dog-food/dry-dog-food`) or deals group (`dry-dog-food-deals`) |
| `POST /api/v1/petco/product` | 1 | One product by part number or URL: brand, rating, review count, breadcrumbs, and every variant with `cat_entry_id`, part number, UPC, price, list price, autoship and first-autoship price, pickup price, online quantity and status, fulfillment flags, ingredients, guaranteed analysis, directions, specifications, dimensions and images |
| `POST /api/v1/petco/stores` | 1 | Up to 10 Petco stores nearest a ZIP: `store_id`, store number, name, address, phone, coordinates, distance, in-store pickup and opening hours per weekday |
| `POST /api/v1/petco/store-inventory` | 1 | Units on hand at one store for up to 10 products: `qty_available`, `alert_level` (GREEN, YELLOW, RED) and `in_stock` per `cat_entry_id` |

## Workflow

1. **Find the product:** call `/petco/search` with `query`, or `/petco/category` with a category `path`. Each row has a `part_number`, a `url`, a `cat_entry_id`, and `variations[]` with the same ids per size or flavor.
2. **One product in full:** call `/petco/product` with the row's `url` (faster) or `part_number`. Product and category calls can take 10-30 seconds; give them a 60-second timeout or longer.
3. **Nearby stores:** call `/petco/stores` with the user's `zip`. Each row has a `store_id`.
4. **Who has it:** call `/petco/store-inventory` with up to 10 `cat_entry_ids` and the `store_id` (or just a `zip`, which uses the nearest store). It takes `cat_entry_id` values, not part numbers.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars). A bare part number is rejected; look it up with `/product` |
| `page` | integer | 1 | 1-based page (1-100), 48 products per page |
| `sort` | string | `relevance` | `relevance`, `price`, `rating`, `top_sold`, `newest` or `name` |
| `sort_order` | string | per sort | `asc` or `desc`. Defaults to `asc` for `price` and `name`, `desc` for everything else |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | required | A petco.com category: its path (`dog/dog-food/dry-dog-food`), `/category/<path>`, or the full URL. A listing's `categories[].url` or `deal_group_ids` value works too |
| `page` | integer | 1 | 1-based page (1-100), 48 products per page |
| `sort` | string | `relevance` | Same values as search |
| `sort_order` | string | per sort | `asc` or `desc` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | Petco product page URL, `https://www.petco.com/product/<name>-<part number>` (a listing row's `url`). Answers faster than `part_number` |
| `part_number` | string | one of | Petco part number, 4-10 digits (a listing row's `part_number`) |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP code to search around |
| `limit` | integer | 5 | Stores to return, nearest first, 1-10 |

### Store inventory (`/store-inventory`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `cat_entry_ids` | string[] | required | 1-10 catalog entry ids: the `cat_entry_id` of a listing row, variation or product variant. NOT the part number |
| `store_id` | string | one of | Petco store id: the `store_id` from `/stores` (not the `store_number`) |
| `zip` | string | one of | US ZIP code; stock is read at the nearest store, returned as `store` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/petco/store-inventory \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"cat_entry_ids": ["6131012"], "store_id": "715931384"}'
```

Captured response (Purina Pro Plan 40 lb at the Union Square store, New York):

```json
{
  "data": {
    "store_id": "715931384",
    "zip": null,
    "store": null,
    "count": 1,
    "items": [
      { "cat_entry_id": "6131012", "qty_available": 9, "alert_level": "GREEN", "in_stock": true }
    ],
    "missing_cat_entry_ids": []
  },
  "response_time": 11769,
  "credits_used": 1
}
```

A captured `/search` row for `{"query": "dog food"}` (description, group ids and two variations trimmed):

```json
{
  "position": 1,
  "name": "Purina Pro Plan Sensitive Skin and Stomach Salmon and Rice Formula Dog Food, 40 lbs.",
  "product_name": "Purina Pro Plan Sensitive Skin and Stomach Salmon and Rice Formula Dog Food",
  "brand": "Purina Pro Plan",
  "part_number": "3748364",
  "cat_entry_id": "6131012",
  "parent_cat_entry_id": "2026049",
  "url": "https://www.petco.com/product/purina-pro-plan-sensitive-skin-and-stomach-salmon-and-rice-formula-dry-dog-food-40-lbs-3748364",
  "rating": 4.5378,
  "review_count": 6737,
  "price": 97.99,
  "list_price": 97.99,
  "autoship_price": 93.09,
  "fulfillment": { "pickup_in_store": true, "same_day_delivery": true, "autoship_eligible": true, "in_store_only": false },
  "is_rx_food": false,
  "taxonomy": "Consumables|Food|Household Pet",
  "deal_group_ids": [],
  "variations": [
    {
      "name": "Purina Pro Plan Sensitive Skin and Stomach Salmon and Rice Formula Dog Food, 30 lbs.",
      "part_number": "2579466",
      "cat_entry_id": "531503",
      "price": 77.99,
      "list_price": 80.99,
      "autoship_price": 74.09
    },
    {
      "name": "Purina Pro Plan Sensitive Skin and Stomach Salmon and Rice Formula Dog Food, 16 lbs.",
      "part_number": "2579440",
      "cat_entry_id": "531507",
      "price": 54.99,
      "list_price": 57.99,
      "autoship_price": 52.24
    }
  ]
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def petco(endpoint, body):
    # /product and /category can take 10-30 seconds; a generous timeout keeps them from failing early.
    r = requests.post(f"{BASE}/api/v1/petco/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Search: every size with one-time and autoship price
row = petco("search", {"query": "dog food", "sort": "top_sold"})["products"][0]
for v in row["variations"]:
    print(v["name"][-12:], v["price"], "was", v["list_price"], "autoship", v["autoship_price"])

# 2. The nearest stores
stores = petco("stores", {"zip": "10001", "limit": 10})["stores"]
by_id = {s["store_id"]: s for s in stores}

# 3. Units of every size at the nearest store, in one call (cat_entry_id, not part_number)
ids = [v["cat_entry_id"] for v in row["variations"]][:10]
stock = petco("store-inventory", {"cat_entry_ids": ids, "store_id": stores[0]["store_id"]})
for it in stock["items"]:
    print(it["cat_entry_id"], it["qty_available"], it["alert_level"])

# 4. One product in full
item = petco("product", {"url": row["url"]})
for v in item["variants"]:
    print(v["upc"], v["price"], "first autoship", v["first_autoship_price"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Petco answered.

- **search** - `query`, `page`, `sort`, `sort_order`, `total_results`, `total_pages`, `page_size`, `count`, `products[]` (`position`, `name`, `product_name`, `brand`, `part_number`, `cat_entry_id`, `parent_cat_entry_id`, `url`, `image`, `description`, `rating`, `review_count`, `price`, `list_price`, `autoship_price`, `fulfillment` {`pickup_in_store`, `same_day_delivery`, `autoship_eligible`, `in_store_only`}, `is_rx_food`, `taxonomy`, `deal_group_ids[]`, `group_ids[]`, `variations[]` {`name`, `part_number`, `cat_entry_id`, `url`, `image`, `price`, `list_price`, `autoship_price`}), `facets[]` {`name`, `display_name`, `options[]` {`value`, `display_name`, `count`, `selected`}}, `categories[]` {`group_id`, `name`, `count`, `url`}.
- **category** - `path`, `url`, `group_id`, `page`, `sort`, `sort_order`, `total_results`, `total_pages`, `page_size`, `count`, `products[]` (same as search), `facets[]`, `categories[]`.
- **product** - `part_number`, `cat_entry_id`, `parent_part_number`, `url`, `name`, `brand`, `brand_url`, `rating`, `review_count`, `answered_questions`, `breadcrumbs[]` {`name`, `url`}, `variant_count`, `variants[]` (`cat_entry_id`, `part_number`, `sku`, `upc`, `name`, `url`, `attributes[]` {`name`, `value`}, `price`, `list_price`, `autoship_price`, `first_autoship_price`, `pickup_price`, `online_quantity`, `inventory_status`, `is_discontinued`, `fulfillment` {`pickup_in_store`, `same_day_delivery`, `autoship_eligible`, `in_store_only`, `online_only`}, `is_rx`, `is_rx_food`, `pet_type`, `taxonomy`, `description`, `highlights[]`, `details[]` {`name`, `value`}, `ingredients`, `guaranteed_analysis`, `directions`, `specifications[]` {`group`, `rows[]` {`name`, `value`}}, `dimensions`, `warranty`, `thumbnail`, `images[]`).
- **stores** - `zip`, `latitude`, `longitude`, `limit`, `count`, `stores[]` (`store_id`, `store_number`, `name`, `store_type`, `address`, `address2`, `city`, `state`, `zip`, `phone`, `latitude`, `longitude`, `distance_miles`, `pickup_in_store`, `hours` {`monday`..`sunday`: {`open`, `close`}}).
- **store-inventory** - `store_id`, `zip`, `store` (the nearest store's row when called with `zip`, else `null`), `count`, `items[]` (`cat_entry_id`, `qty_available`, `alert_level`, `in_stock`), `missing_cat_entry_ids[]`.

## Guardrails

- Prices are in dollars and national: `97.99` is $97.99 at every store. `pickup_price` equals `price`, and no endpoint takes a store for price, so never claim a store-specific price. Stock is per store.
- `price` is the one-time purchase price; `list_price` is the was/compare price and equals `price` when not on sale. `autoship_price` is the Repeat Delivery price. `first_autoship_price` (product only) is the promo price of the first Repeat Delivery order; it is not the ongoing autoship price.
- `/store-inventory` takes `cat_entry_id` values from a listing row, variation or product variant, and the `store_id` from `/stores`. A part number or a `store_number` there does not work.
- One unknown `cat_entry_id` empties the whole stock answer and returns `404`. If a multi-id call 404s, retry the ids one at a time to find the bad one. A real id with no units still returns its row (`qty_available: 0`, `alert_level: "RED"`).
- Called with `zip`, store-inventory reads the single nearest store and returns it as `store`. Name the store when quoting stock.
- `/product` returns every variant; the top-level `part_number` and `cat_entry_id` are the variant that was asked for. Prices live on `variants[]`, not at the top level.
- Search and category rows show one variant's prices; `variations[]` has the price per size or flavor. Compare like-for-like sizes.
- `deal_group_ids` name the promotions a product is in (`dry-dog-food-deals`); pass one as a category `path` to list that deal group.
- Product and category calls can take 10-30 seconds. Use a 60-second timeout or longer per call.
- `is_rx` and `is_rx_food` flag prescription items and prescription diets; mention the flag when quoting one. Never fabricate prices or stock. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, a query that is a bare part number, a malformed category `path`, neither `url` nor `part_number`, a ZIP that is not 5 digits, `limit` above 10, more than 10 `cat_entry_ids`, or neither `store_id` nor `zip` on store-inventory).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such category or product, no Petco store near the ZIP, or no stock records for the ids at that store (check each is a `cat_entry_id` and the store a `store_id`). Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data).
- `502` means Petco is temporarily unavailable. It is not charged; retry after a few seconds. Product and category calls are slow (10-30 seconds), so allow at least a minute per call before treating one as failed.

## SDKs

```bash
pip install scavio==0.33.0
npm install scavio@0.33.0
```

```js
import { Scavio } from "scavio";

// reads SCAVIO_API_KEY; /product and /category can take 30 seconds, so raise the 30s default timeout
const scavio = new Scavio({ timeout: 90_000 });
const { data: found } = await scavio.petco.search({ query: "dog food", sort: "price" });
const { data: near } = await scavio.petco.stores({ zip: "10001" });
const stock = await scavio.petco.storeInventory({
  cat_entry_ids: found.products[0].variations.map((v) => v.cat_entry_id).slice(0, 10),
  store_id: near.stores[0].store_id,
});
const item = await scavio.petco.product({ url: found.products[0].url });
```

MCP: the Scavio MCP server exposes all 5 endpoints as tools (`search_petco`, `get_petco_category`, `get_petco_product`, `get_petco_stores`, `get_petco_store_inventory`). Petco is opt-in: add `petco` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.31.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,petco"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/petco-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data), [category](https://scavio.dev/docs/petco-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data), [product](https://scavio.dev/docs/petco-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data), [stores](https://scavio.dev/docs/petco-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data), [store inventory](https://scavio.dev/docs/petco-store-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data). Overview: [Petco API](https://scavio.dev/petco-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data).
