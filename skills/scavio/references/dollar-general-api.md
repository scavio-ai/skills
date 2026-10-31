# Dollar General API - Store Prices, Stock, Deals, Coupons

Search Dollar General and read products at the store you choose: that store's price, original price and units on hand, with digital coupons attached. One store-locator call returns a product's unit count at up to 25 nearby stores. List what is on sale or on clearance at a store, and page the current digital coupons. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find household, grocery, health or beauty items at Dollar General by keyword
- Check what an item costs at a specific Dollar General store, and how many are on the shelf
- Find which Dollar General stores near a ZIP have a product in stock, and how many units each has
- List what is on sale or on clearance at a Dollar General store
- List Dollar General digital coupons, or the coupons that apply to a product
- Look up a Dollar General product by UPC
- Compare Dollar General prices with other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Dollar General endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/dollargeneral/search` | 1 | 24 results per page at one store: price, original price, `available_quantity` (units on hand at that store), rating, review count, categories, digital coupons, UPC and URL |
| `POST /api/v1/dollargeneral/product` | 1 | One product by UPC at one store: price, original price, units on hand, `nearby_stores_with_stock`, rating, SKU, brand, description, highlights, images, categories and coupons |
| `POST /api/v1/dollargeneral/stores` | 1 | Up to 25 stores near a ZIP or coordinates, nearest first: `store_id`, address, phone, coordinates, distance, hours, services. With `upc`, each store's unit count of that product |
| `POST /api/v1/dollargeneral/deals` | 1 | Items `on_sale` or on `clearance`, priced and stocked at one store, 24 per page |
| `POST /api/v1/dollargeneral/coupons` | 1 | Current digital coupons, 30 per page: offer id and code, summary, brand, value, offer type, category, minimum quantity, start and expiration dates |

## Workflow

Every price and unit count belongs to one store, so pin the store first.

1. **Pick the store:** call `/dollargeneral/stores` with the user's `zip` (or `latitude` and `longitude`). Each row has a `store_id`.
2. **Search at that store:** call `/dollargeneral/search` with `query` and `store_id`. Each row has a `upc`.
3. **One product in full:** call `/dollargeneral/product` with the `upc` and `store_id`.
4. **Who has it nearby:** call `/dollargeneral/stores` with the `zip` and the `upc`. One call returns the unit count at up to 25 nearby stores.
5. **Deals and coupons:** call `/dollargeneral/deals` with `store_id` and `type`, and `/dollargeneral/coupons` (not store-scoped).

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `store_id` | string | required | Store number from `/stores`, e.g. `"12629"` |
| `page` | integer | 1 | 1-based page (1-100), 24 results per page |
| `sort` | string | `recommended` | `recommended`, `price_low`, `price_high` or `rating` |
| `in_stock_only` | boolean | false | Only products with units on hand at the store |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `upc` | string | required | Product UPC, the `upc` of a search result (6-14 digits, leading zeros optional) |
| `store_id` | string | required | Store number |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code to search around |
| `latitude`, `longitude` | number | one of | Coordinates to search around, instead of `zip` |
| `radius` | number | 25 | Search radius in miles, 1-100 |
| `upc` | string | - | Product UPC; every store also gets its unit count of that product |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | Store number |
| `type` | string | required | `on_sale` (everything on sale) or `clearance` (the clearance event) |
| `page` | integer | 1 | 1-based page (1-100), 24 per page |
| `sort` | string | `recommended` | `recommended`, `price_low`, `price_high` or `rating` |

### Coupons (`/coupons`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | 1 | 1-based page (1-50), 30 coupons per page |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/dollargeneral/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "75203", "upc": "030772156629"}'
```

Captured response (Bounty paper towels near Dallas 75203; trimmed to 2 of 25 stores):

```json
{
  "data": {
    "zip": "75203",
    "latitude": 32.744,
    "longitude": -96.802,
    "radius_miles": 25,
    "upc": "030772156629",
    "total_results": 117,
    "count": 25,
    "stores": [
      {
        "store_id": "12629",
        "address": "2919 Cedar Crest Blvd",
        "city": "Dallas",
        "state": "TX",
        "zip": "75203-4011",
        "latitude": 32.741674,
        "longitude": -96.788919,
        "phone": "6822731392",
        "distance_miles": 0.8,
        "hours": { "monday": "08:00-20:00", "tuesday": "08:00-20:00", "wednesday": "08:00-20:00", "thursday": "08:00-20:00", "friday": "08:00-20:00", "saturday": "08:00-20:00", "sunday": "08:00-20:00" },
        "services": ["Rug Doctor", "DG Delivery", "NCI", "Fresh Produce"],
        "quantity": 3,
        "in_stock": true,
        "inventory_status": 3,
        "is_sellable": true,
        "pickup_eligible": false,
        "delivery_eligible": true
      },
      {
        "store_id": "19292",
        "address": "655 W Illinois Ave Ste 254",
        "city": "Dallas",
        "state": "TX",
        "zip": "75224-1814",
        "latitude": 32.722557,
        "longitude": -96.83183,
        "phone": "4692502773",
        "distance_miles": 2.3,
        "hours": { "monday": "08:00-22:00", "tuesday": "08:00-22:00", "wednesday": "08:00-22:00", "thursday": "08:00-22:00", "friday": "08:00-22:00", "saturday": "08:00-22:00", "sunday": "08:00-22:00" },
        "services": ["Amerigas", "DG Delivery", "NCI", "Alcohol", "Beer", "Wine"],
        "quantity": 4,
        "in_stock": true,
        "inventory_status": 3,
        "is_sellable": true,
        "pickup_eligible": false,
        "delivery_eligible": true
      }
    ]
  },
  "response_time": 6114,
  "credits_used": 1
}
```

A captured `/product` answer for the same UPC at store 12629 (description, images, categories and coupons trimmed):

```json
{
  "upc": "030772156629",
  "sku": "36158202",
  "store_id": "12629",
  "title": "Bounty Paper Towels Select-A-Size White, 6 Double Plus Rolls, 103 Sheets Per Roll",
  "brand": "Bounty",
  "price": 14.95,
  "original_price": 16.75,
  "available_quantity": 3,
  "in_stock": true,
  "stock_status": 3,
  "is_sellable": true,
  "nearby_stores_with_stock": 20,
  "rating": 4.5,
  "review_count": 5680,
  "unit_size": "305",
  "unit_of_measure": "sq feet",
  "url": "https://www.dollargeneral.com/p/bounty-paper-towels-select-a-size-white-6-double-plus-rolls-103-sheets-per-roll/030772156629"
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def dg(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/dollargeneral/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. The user's store
store = dg("stores", {"zip": "75203"})["stores"][0]
sid = store["store_id"]

# 2. Search at that store
row = dg("search", {"query": "paper towels", "store_id": sid})["products"][0]
print(row["title"][:60], row["price"], "on hand:", row["available_quantity"])

# 3. Unit count at every nearby store in one call
for s in dg("stores", {"zip": "75203", "upc": row["upc"]})["stores"]:
    if s["in_stock"]:
        print(s["store_id"], s["address"], s["distance_miles"], "mi:", s["quantity"], "units")

# 4. Clearance in stock at this store (the listing covers the whole chain)
clr = dg("deals", {"store_id": sid, "type": "clearance"})["products"]
print([p["title"][:40] for p in clr if p["available_quantity"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Dollar General answered.

- **search / deals** - `query` (search) or `type` and `category` (deals), `store_id`, `page`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `upc`, `sku`, `title`, `image`, `price`, `original_price`, `available_quantity`, `in_stock`, `inventory_status`, `is_sellable`, `rating`, `review_count`, `categories[]`, `coupons[]`, `offers[]`, `url`).
- **product** - `upc`, `sku`, `store_id`, `title`, `brand`, `price`, `original_price`, `available_quantity`, `in_stock`, `stock_status`, `is_sellable`, `nearby_stores_with_stock`, `rating`, `review_count`, `unit_size`, `unit_of_measure`, `description`, `highlights[]`, `images[]`, `category_hierarchy[]`, `categories[]`, `coupons[]`, `offers[]`, `url`.
- **stores** - `zip`, `latitude`, `longitude`, `radius_miles`, `upc`, `total_results`, `count`, `stores[]` (`store_id`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `phone`, `distance_miles`, `hours` {`monday`..`sunday`: `"08:00-20:00"`}, `services[]`, and with `upc`: `quantity`, `in_stock`, `inventory_status`, `is_sellable`, `pickup_eligible`, `delivery_eligible`).
- **coupons** - `page`, `total_results`, `total_pages`, `count`, `coupons[]` (`offer_id`, `offer_code`, `summary`, `description`, `brand`, `value`, `category`, `min_quantity`, `is_manufacturer_coupon`, `expiration_date`, `image`, `company`, `offer_type`, `start_date`, `disclaimer`). The same coupon shape is attached to products in `coupons[]`.

## Guardrails

- Prices are in dollars: `14.95` is $14.95.
- `available_quantity` (search, deals, product) and `quantity` (stores) are units on hand at that store. `inventory_status` / `stock_status` are the site's raw codes; use the counts and `in_stock` when answering.
- The deals listing and its `total_results` cover the whole chain, so out-of-stock items are included. Only `available_quantity > 0` means the item is at that store.
- Clearance items carry the current price only: `original_price` equals `price` there, so do not report a discount for them.
- Dollar General returns `rating` and `review_count` only; there is no review text endpoint.
- A coupon's `offer_type` can be `AmountOff` or `Cashback`; say which, and quote `expiration_date`.
- Never fabricate prices, stock or coupons. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `store_id`, a UPC that is not numeric, neither `zip` nor coordinates on `/stores`, an unknown ZIP, or a `type` other than `on_sale` or `clearance`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means an unknown UPC or store number; check both. Not charged. A search at an unknown store answers with 0 results instead.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api).
- `502` means Dollar General is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.31.0
npm install scavio@0.31.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.dollarGeneral.stores({ zip: "75203" });
const store_id = near.stores[0].store_id;
const found = await scavio.dollarGeneral.search({ query: "paper towels", store_id });
const nearby = await scavio.dollarGeneral.stores({ zip: "75203", upc: found.data.products[0].upc });
const coupons = await scavio.dollarGeneral.coupons({ page: 1 });
```

MCP: the Scavio MCP server exposes all 5 endpoints as tools (`search_dollar_general`, `get_dollar_general_product`, `get_dollar_general_stores`, `get_dollar_general_deals`, `get_dollar_general_coupons`). Dollar General is opt-in: add `dollargeneral` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.29.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,dollargeneral"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/dollargeneral-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api), [product](https://scavio.dev/docs/dollargeneral-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api), [stores](https://scavio.dev/docs/dollargeneral-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api), [deals](https://scavio.dev/docs/dollargeneral-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api), [coupons](https://scavio.dev/docs/dollargeneral-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api). Overview: [Dollar General API](https://scavio.dev/dollargeneral-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api).
