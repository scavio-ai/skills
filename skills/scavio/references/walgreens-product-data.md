# Walgreens Product Data API - Prices, Store Stock, Stores

Search Walgreens retail products (health, beauty, household, grocery; nothing pharmacy) with regular and sale price, unit price, promotion, coupon, rewards and rebate messages, rating and review count, up to 70 per page. Read one product with UPC, ingredients, warnings and its current offers. Find Walgreens and Duane Reade stores near a ZIP, and check live unit counts of one product at up to 20 stores in a single call. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find health, beauty, personal care or household items at Walgreens by keyword
- Check a Walgreens product's price, sale price, unit price, or the coupons and rewards on it
- Check whether nearby Walgreens stores have an item in stock, and how many units each has
- Find Walgreens or Duane Reade stores near a ZIP code or coordinates
- Read a product's ingredients, warnings or UPC
- List what is on sale or on clearance in a search
- Compare Walgreens prices with CVS or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Search, product and stores cost 2 credits each; stock costs 4.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/walgreens/search` | 2 | Up to 70 products per page: product id, SKU, UPC, name, brand, size, regular and sale price, multi-buy text, unit price, promotion, coupon, rewards and rebate messages, rating, review count, image, URL, ship / pickup / delivery availability, online stock status, clearance flag |
| `POST /api/v1/walgreens/product` | 2 | One product by id or URL: SKU, UPC, GTIN, name, brand, size, regular and sale price, savings, unit price, offers (rewards and rebates with dates), description, ingredients, warnings, rating, review count, categories, images, ship and pickup availability, FSA eligibility, clearance flag |
| `POST /api/v1/walgreens/stores` | 2 | Walgreens and Duane Reade stores near a ZIP or coordinates, nearest first: store number, name, brand, address, phone, coordinates, distance, opening and closing time, time zone and store page URL, paged |
| `POST /api/v1/walgreens/stock` | 4 | Live in-store stock of one product at up to 20 stores: per store the status (In Stock, Out of Stock, Not Available), unit count and `in_stock`. Unrecognized store numbers are listed in `unknown_store_ids` |

## Workflow

1. **Find the product:** call `/walgreens/search` with `query`. Each row has a `product_id`.
2. **One product in full:** call `/walgreens/product` with the `product_id` for offers, ingredients and warnings.
3. **Nearby stores:** call `/walgreens/stores` with the user's `zip`. Each row has a `store_number`.
4. **Who has it:** call `/walgreens/stock` with the `product_id` and up to 20 `store_ids` (the `store_number` values). One call covers every store.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-100), up to 70 results per page |
| `sort` | string | `relevance` | `relevance`, `top_sellers`, `price_low_to_high`, `price_high_to_low`, `unit_price_low_to_high`, `brand_name_asc`, `brand_name_desc`, `most_reviewed`, `highest_rated`, `most_viewed` or `newest_arrival` |
| `store_id` | string | - | Store number from `/stores`. Each row's `availability.text` then describes that store ("Not sold at your store") |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Walgreens product id, a search row's `product_id` (`"300452904"` or `"prod6345045"`), or a walgreens.com product URL |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code to search around |
| `latitude`, `longitude` | number | one of | Coordinates to search around, instead of `zip` |
| `radius` | number | 25 | Search radius in miles, 1-100 |
| `page` | integer | 1 | 1-based page (1-100) |
| `limit` | integer | 10 | Stores per page, 1-25 |

### Stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Product id or walgreens.com product URL |
| `store_ids` | string[] | required | 1-20 store numbers, the `store_number` values from `/stores` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/walgreens/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "300452904", "store_ids": ["15350", "15992", "249", "178", "1173"]}'
```

Captured response (Walgreens shampoo at five Chicago stores):

```json
{
  "data": {
    "product_id": "300452904",
    "article_id": "000000000012456764",
    "planogram": "40000735502",
    "count": 5,
    "in_stock_count": 5,
    "stores": [
      { "store_number": "15350", "status": "In Stock", "quantity": 3, "in_stock": true },
      { "store_number": "15992", "status": "In Stock", "quantity": 5, "in_stock": true },
      { "store_number": "249", "status": "In Stock", "quantity": 3, "in_stock": true },
      { "store_number": "178", "status": "In Stock", "quantity": 3, "in_stock": true },
      { "store_number": "1173", "status": "In Stock", "quantity": 1, "in_stock": true }
    ],
    "unknown_store_ids": []
  },
  "response_time": 2263,
  "credits_used": 4
}
```

A captured `/search` row for `{"query": "shampoo", "store_id": "15350"}` (image trimmed):

```json
{
  "position": 1,
  "product_id": "300452904",
  "sku_id": "400675110",
  "upc": "19560214708",
  "name": "Walgreens Shiny & Smooth Shampoo",
  "brand": "Walgreens",
  "product_name": "Shiny & Smooth Shampoo",
  "size": "33.8 fl oz",
  "product_type": "Shampoo",
  "price": 4.99,
  "sale_price": 3.74,
  "sale_text": null,
  "on_sale": true,
  "unit_price": null,
  "unit_price_size": null,
  "promotion": null,
  "coupon": null,
  "loyalty_message": "Earn $10 rewards on $30+ spent on select Walgreens brands*",
  "rebate": "Extra 15% off $35+ eligible items sitewide* with code NOV15 or 20% off $50+ eligible items sitewide* with code NOV20",
  "rating": 4,
  "review_count": 90,
  "url": "https://www.walgreens.com/store/c/walgreens-shiny-%26-smooth-shampoo/ID=300452904-product",
  "availability": { "ship": true, "pickup": false, "delivery": false, "text": "In stock but not available for pickup" },
  "online_stock_status": "In Stock",
  "clearance": false,
  "article_id": "000000000012456764",
  "planogram": "40000735502"
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def wag(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/walgreens/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find the product (2 credits)
row = wag("search", {"query": "shampoo", "sort": "top_sellers"})["products"][0]
print(row["name"], row["price"], "sale", row["sale_price"], row["promotion"], row["coupon"])

# 2. The 20 nearest stores (2 credits)
stores = wag("stores", {"zip": "60614", "limit": 20})["stores"]
by_number = {s["store_number"]: s for s in stores}

# 3. Units at all 20 in one call (4 credits)
stock = wag("stock", {"product_id": row["product_id"], "store_ids": list(by_number)})
for s in stock["stores"]:
    if s["in_stock"]:
        st = by_number[s["store_number"]]
        print(st["address"]["street"], st["distance_miles"], "mi:", s["quantity"], "units")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Walgreens answered.

- **search** - `query`, `page`, `sort`, `store_id`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `product_id`, `sku_id`, `upc`, `name`, `brand`, `product_name`, `size`, `product_type`, `price`, `sale_price`, `sale_text`, `on_sale`, `unit_price`, `unit_price_size`, `promotion`, `coupon`, `loyalty_message`, `rebate`, `rating`, `review_count`, `image`, `url`, `availability` {`ship`, `pickup`, `delivery`, `text`}, `online_stock_status`, `clearance`, `article_id`, `planogram`).
- **product** - `product_id`, `sku_id`, `upc`, `gtin`, `name`, `display_name`, `brand`, `size`, `product_type`, `walgreens_brand`, `price`, `sale_price`, `sale_text`, `on_sale`, `unit_price`, `unit_price_size`, `promotion`, `savings_amount`, `savings_percent`, `loyalty_message`, `rebate`, `offers[]` {`type`, `title`, `headline`, `details`, `description`, `link_text`, `start_date`, `end_date`}, `clearance`, `store_pricing`, `description`, `ingredients[]` {`group`, `type`, `ingredients[]`}, `warnings`, `rating`, `review_count`, `categories[]` {`id`, `name`, `url`}, `images[]`, `ship_available`, `pickup_available`, `ship_message`, `fsa_eligible`, `article_id`, `planogram`, `url`.
- **stores** - `zip`, `latitude`, `longitude`, `radius_miles`, `page`, `total_results`, `total_pages`, `has_more`, `count`, `stores[]` (`store_number`, `name`, `brand`, `address` {`street`, `city`, `state`, `zip`, `intersection`}, `phone`, `latitude`, `longitude`, `distance_miles`, `open_time`, `close_time`, `time_zone`, `temporarily_closed`, `url`).
- **stock** - `product_id`, `article_id`, `planogram`, `count`, `in_stock_count`, `stores[]` (`store_number`, `status`, `quantity`, `in_stock`), `unknown_store_ids[]`.

## Guardrails

- Prices are in dollars and national: `4.99` is $4.99 at every store. `store_pricing` is false on every product, and no endpoint takes a store for price, so never claim a store-specific price.
- `price` is the regular price; `sale_price` is the single-unit sale price. A multi-buy deal keeps its text in `sale_text` ("2/$12.00 or 1/$6.99"). `on_sale` means a sale price below the regular price.
- `promotion`, `coupon`, `loyalty_message` and `rebate` are the site's own text; quote them as written and do not compute a final price from them.
- `/stores` returns `store_number`; pass those values as `store_id` (search) and `store_ids` (stock).
- `/stock` quantities are live units at each store. `status` "Not Available" means the store does not carry the product, which is different from "Out of Stock". A store number Walgreens does not recognize lands in `unknown_store_ids`.
- Without `store_id` on search, `availability.text` reads "Store inventory unavailable". Use `/stock` for real counts.
- Retail only: prescriptions and pharmacy services are not covered.
- Never fabricate prices, stock or offers. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query` or `product_id`, an unknown `sort`, a ZIP that is not 5 digits, neither `zip` nor coordinates on `/stores`, `limit` above 25, or more than 20 `store_ids`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` or `/stock` means no such product, or Walgreens does not report store stock for it; use a `product_id` from search. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data).
- `502` means Walgreens is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.32.0
npm install scavio@0.32.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.walgreens.search({ query: "shampoo", sort: "price_low_to_high" });
const item = await scavio.walgreens.product({ product_id: found.products[0].product_id });
const { data: near } = await scavio.walgreens.stores({ zip: "60614", limit: 20 });
const stock = await scavio.walgreens.stock({
  product_id: found.products[0].product_id,
  store_ids: near.stores.map((s) => s.store_number),
});
```

MCP: the Scavio MCP server exposes all 4 endpoints as tools (`search_walgreens`, `get_walgreens_product`, `get_walgreens_stores`, `get_walgreens_stock`). Walgreens is opt-in: add `walgreens` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.30.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,walgreens"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/walgreens-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data), [product](https://scavio.dev/docs/walgreens-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data), [stores](https://scavio.dev/docs/walgreens-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data), [stock](https://scavio.dev/docs/walgreens-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data). Overview: [Walgreens API](https://scavio.dev/walgreens-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data).
