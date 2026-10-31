# Sam's Club Product Data API - Club Prices, Instant Savings, Stock, Reviews

Search Sam's Club, read one item's club shelf price, Instant Savings, stock and aisle at the club you choose, find clubs near a ZIP, list every Instant Savings item and any category (clearance included), and page member reviews. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find bulk or warehouse-club items at Sam's Club by keyword
- Check what an item costs at a specific Sam's Club, and whether that club has it in stock and in which aisle
- List Sam's Club Instant Savings, with each offer's amount, end date and purchase limit
- Browse Sam's Club clearance or any Sam's Club category
- Read Sam's Club member reviews or the rating breakdown for an item
- Find Sam's Club locations near a ZIP code
- Compare Sam's Club prices with Costco, Walmart or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Sam's Club endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/samsclub/search` | 1 | Up to 45 results per page: `item_id`, price, was-price, savings, unit price, Instant Savings, rating, review count, stock, pickup/delivery/shipping availability and aisle |
| `POST /api/v1/samsclub/product` | 1 | One item: online price and `club_price`, Instant Savings, member and order limits, rating histogram, UPC, model, specifications, and fulfillment per method with stock status, quantity and aisle. Optional `club_id` |
| `POST /api/v1/samsclub/clubs` | 1 | Clubs near a ZIP within 100 miles, nearest first: `club_id`, name, address, coordinates, distance, phone, hours, services and whether it is temporarily closed |
| `POST /api/v1/samsclub/savings` | 1 | Every Instant Savings item, paged: price, was-price, savings, and each offer's amount, end date and limit |
| `POST /api/v1/samsclub/category` | 1 | Products in a category, paged, same fields as search. Clearance is category `1150109` |
| `POST /api/v1/samsclub/reviews` | 1 | 10 reviews per page with rating, title, text, author, date, verified purchase and helpful votes, plus the average, total, star breakdown and the top positive and negative review |

## Workflow

The club is what you need to get right.

- **Listings (search, savings, category) are priced and stocked at a nearby club Sam's Club picks by location.** Which club it used comes back in `data.club`. Nothing you send changes it, so treat listing prices and stock as that club's, and say which club.
- **For a specific club, use product with `club_id`.** That call returns the chosen club's `club_price`, `in_stock_at_club` and `aisle`, and echoes the club in `club.club_id`.

1. **Find the club:** call `/samsclub/clubs` with the user's `zip`. Each row has a `club_id`.
2. **Find the item:** call `/samsclub/search` with `query` (or `/samsclub/category`, or `/samsclub/savings`). Each row has an `item_id`.
3. **Price and stock at that club:** call `/samsclub/product` with `item_id` and `club_id`.
4. **Reviews (optional):** call `/samsclub/reviews` with the `item_id`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-100), up to 45 results per page |
| `sort` | string | site order | `relevance`, `price_low`, `price_high` or `top_selling` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | The number at the end of a samsclub.com/ip/ URL, or `item_id` from search |
| `club_id` | string | - | Club number from `/clubs`, e.g. `"6372"`. Prices and stock become that club's |

### Clubs (`/clubs`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | 5-digit US ZIP |
| `limit` | integer | 10 | Clubs to return within 100 miles, nearest first, 1-20 |

### Savings (`/savings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | 1 | 1-based page (1-100), up to 45 items per page |
| `sort` | string | site order | `relevance`, `price_low`, `price_high` or `top_selling` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | The number at the end of a samsclub.com /browse/ or /cp/ URL. Clearance is `1150109` |
| `page` | integer | 1 | 1-based page (1-100) |
| `sort` | string | site order | `relevance`, `price_low`, `price_high` or `top_selling` |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Sam's Club item id |
| `page` | integer | 1 | 1-based page (1-100), 10 reviews per page |
| `sort` | string | - | `newest`, `oldest`, `highest`, `lowest` or `most_helpful` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/samsclub/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "15325822107", "club_id": "6372"}'
```

Captured response (club 6372, Dallas; trimmed: descriptions, images, specifications and 2 of 3 fulfillment options removed):

```json
{
  "data": {
    "item_id": "15325822107",
    "title": "Marathon Automated Hardwound Paper Towel Dispenser, Black",
    "url": "https://www.samsclub.com/ip/Marathon-Automated-Hardwound-Paper-Towel-Dispenser-Black/15325822107",
    "brand": "Marathon",
    "model": "6405099",
    "upc": "042000640503",
    "currency": "USD",
    "price": 47.46,
    "was_price": null,
    "savings_amount": null,
    "unit_price": null,
    "club_price": { "price": 47.46, "was_price": null, "savings_amount": null, "unit_price": null },
    "instant_savings": null,
    "member_limit": 10,
    "order_limit": 12,
    "rating": 4.6349,
    "review_count": 241,
    "availability_status": "IN_STOCK",
    "club": { "club_id": "6372", "city": "Dallas", "state": "TX", "zipcode": "75231" },
    "in_stock_at_club": false,
    "aisle": null,
    "fulfillment": {
      "pickup": false,
      "delivery": false,
      "shipping": true,
      "options": [
        {
          "method": "shipping",
          "available": true,
          "availability_status": "IN_STOCK",
          "available_quantity": 8,
          "max_order_quantity": 12,
          "location": "Dallas, 75231",
          "aisle": null,
          "estimated_date": "2026-11-03T22:59:00.000Z",
          "fee": null
        }
      ]
    }
  },
  "response_time": 20119,
  "credits_used": 1
}
```

Here the item ships (`available_quantity: 8`, which means 8 or more) but the Dallas club does not have it on the shelf (`in_stock_at_club: false`).

A captured `/savings` row (club picked by location, Los Angeles 6626):

```json
{
  "item_id": "81162002218",
  "title": "Fairlife Nutrition Plan 30g Protein Shake, Chocolate, 11.5 fl. oz., 12 pk.",
  "price": 21.28,
  "was_price": 26.78,
  "savings_amount": 5.5,
  "unit_price": "19.4 ¢/fl oz",
  "out_of_stock": false,
  "availability_status": "In stock",
  "fulfillment": { "pickup": true, "delivery": true, "shipping": true },
  "instant_savings": {
    "promotion_id": "0ee5f674-10b3-438e-b968-db3a5a0fc64f",
    "title": "Instant Savings",
    "message": "$5.50 off",
    "amount": 5.5,
    "end_date": "Nov 09",
    "limit": 5,
    "limit_text": "Limit 5"
  }
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def sams(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/samsclub/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. The user's club
club = sams("clubs", {"zip": "75201", "limit": 1})["clubs"][0]

# 2. Find the item (listing prices are for the club in found["club"])
found = sams("search", {"query": "paper towels"})
item_id = found["products"][0]["item_id"]

# 3. Price, shelf stock and aisle at the user's club
p = sams("product", {"item_id": item_id, "club_id": club["club_id"]})
print(club["name"], p["club_price"]["price"], "on shelf:", p["in_stock_at_club"], "aisle:", p["aisle"])

# Clearance at the location-picked club
clearance = sams("category", {"category_id": "1150109", "sort": "price_low"})
print(clearance["club"], clearance["total_results"], "clearance items")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Sam's Club answered.

- **search / savings / category** - `query` (search) or `category_id` and `category_name` (category), `title`, `club` {`club_id`, `city`, `state`, `zipcode`}, `page`, `sort`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `item_id`, `title`, `url`, `image`, `price`, `was_price`, `savings_amount`, `unit_price`, `currency`, `rating`, `review_count`, `sponsored`, `out_of_stock`, `availability_status`, `fulfillment` {`pickup`, `delivery`, `shipping`}, `aisle`, `instant_savings` {`promotion_id`, `title`, `message`, `amount`, `end_date`, `limit`, `limit_text`}, `badge`, `section`).
- **product** - `item_id`, `product_id`, `title`, `url`, `brand`, `model`, `upc`, `manufacturer_product_id`, `product_type`, `image`, `images[]`, `currency`, `price`, `was_price`, `savings_amount`, `unit_price`, `club_price` {same four}, `channel_prices[]` {`channel`, `store_front`, `price`, `was_price`, `savings_amount`, `unit_price`}, `instant_savings`, `member_limit`, `order_limit`, `rating`, `review_count`, `rating_breakdown` {`1`..`5`}, `recommended_percentage`, `availability_status`, `club`, `in_stock_at_club`, `aisle`, `fulfillment` {`pickup`, `delivery`, `shipping`, `options[]` {`method`, `available`, `availability_status`, `available_quantity`, `max_order_quantity`, `location`, `aisle`, `estimated_date`, `fee`}}, `specifications[]`, `short_description`, `long_description`, `warranty`, `category_path[]`.
- **clubs** - `zip`, `count`, `clubs[]` (`club_id`, `name`, `address` {`line1`, `city`, `state`, `zipcode`, `county`, `country`}, `latitude`, `longitude`, `distance_miles`, `phone`, `time_zone`, `hours` {`monday_friday`, `saturday`, `sunday`: {`open`, `close`, `closed`}}, `services[]`, `temporarily_closed`).
- **reviews** - `item_id`, `page`, `sort`, `average_rating`, `total_review_count`, `reviews_with_text_count`, `recommended_percentage`, `rating_breakdown`, `count`, `reviews[]` (`review_id`, `rating`, `title`, `text`, `author`, `author_location`, `submitted_at`, `verified_purchase`, `helpful_count`, `unhelpful_count`, `photos[]`), `top_positive_review`, `top_negative_review`.

## Guardrails

- Prices are in dollars: `47.46` is $47.46.
- Listing prices and stock (search, savings, category) belong to the club in `data.club`, not to the user's club. For the user's club, call product with `club_id` and quote `club_price` and `in_stock_at_club`.
- `available_quantity` is capped at 8 by Sam's Club: `8` means 8 or more. Never report it as an exact count.
- `instant_savings.end_date` is the site's own short text (`"Nov 09"`); quote it as given.
- A category with nothing on its shelf returns an empty `products[]`; that is an answer, not an error.
- Never fabricate prices, stock or offers. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (a non-numeric `item_id`, `club_id` or `category_id`, an unknown `sort`, a ZIP that is not 5 digits).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` or `/reviews` means Sam's Club has no such item; re-run the search for a fresh `item_id`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data).
- `502` means Sam's Club is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.31.0
npm install scavio@0.31.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.samsClub.clubs({ zip: "75201", limit: 1 });
const found = await scavio.samsClub.search({ query: "paper towels" });
const item = await scavio.samsClub.product({ item_id: found.data.products[0].item_id, club_id: near.clubs[0].club_id });
const savings = await scavio.samsClub.savings({ sort: "top_selling" });
const clearance = await scavio.samsClub.category({ category_id: "1150109" });
```

MCP: the Scavio MCP server exposes all 6 endpoints as tools (`search_sams_club`, `get_sams_club_product`, `get_sams_club_clubs`, `get_sams_club_savings`, `get_sams_club_category`, `get_sams_club_reviews`). Sam's Club is opt-in: add `samsclub` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.29.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,samsclub"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/samsclub-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data), [product](https://scavio.dev/docs/samsclub-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data), [clubs](https://scavio.dev/docs/samsclub-clubs?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data), [savings](https://scavio.dev/docs/samsclub-savings?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data), [category](https://scavio.dev/docs/samsclub-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data), [reviews](https://scavio.dev/docs/samsclub-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data). Overview: [Sam's Club API](https://scavio.dev/samsclub-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data).
