# L.L.Bean API - Prices, Store Inventory, Sale, Fit Reviews, Canada + International

Read L.L.Bean (llbean.com, the US outdoor apparel and gear retailer): keyword search, category listings and the Sale category on the US, Canadian and international storefronts, one product with every SKU's price and stock, exact store units per SKU, the store directory, written reviews with fit data, L.L.Bean's own review summary, a delivery date to a ZIP, the department menu and search-box suggestions. Prices are what a visitor who is not signed in sees. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: what an L.L.Bean product costs today, per size range and color, and how many units a store has.** L.L.Bean prices by item (a size range such as Small or Medium, or Regular and Tall) and color, and sells many SKUs in store with exact counts. On 2026-11-27 the Boat and Tote, Zip-Top (product `37037`) read $44.95 Small, $49.95 Medium, $59.95 Large and $69.95 Extra-Large across 97 SKUs: 41 in stock, 32 on backorder and 24 sold out. Its Medium (item `112644`) had 506 units at store `0040`, 32 at `1350` and 74 at `2140` (Black, Regular: 69 units). The second job is the same product abroad: the Men's L.L.Bean Sweater Fleece Full-Zip Jacket (`120785`) read EUR 145 on the German storefront with the offer "15% OFF This Item!", and the Men's Fleece-Lined Flannel Shirt read C$159 on llbean.ca and GBP 110 for the United Kingdom. Pair it with `rei-api` or `dicks-sporting-goods-api` for the same category at other outdoor retailers.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **Never member or card prices.** Prices are what L.L.Bean shows a visitor who is not signed in. L.L.Bean Rewards and L.L.Bean Mastercard prices are never returned; never present a price as a member price.
- **Three markets, not every endpoint in each.** `market` `us` (www.llbean.com, USD, the default), `ca` (www.llbean.ca, CAD, English) or `intl` with a `country` (global.llbean.com, local currency). Search, category, deals and product serve all three; suggestions serve us and ca; categories, store stock, stores, reviews, review summary and delivery estimate serve the US storefront only.
- **Unit counts are US only.** The US product carries every SKU with its stock flag, and store stock gives exact units per SKU per store. The Canadian and international product shows the variant on the page with a price per color and no unit counts.
- **A sale price is reported only below the full price.** The site can list a sale price above the full price; then `sale_price` is null. Sale items carry no end dates.
- **Backorder dates are as given.** `status` and `backorder_date` are the site's text; many look like placeholders (several SKUs show the same date, such as December 30 or 31, 2026).
- **Prices are national.** The same in every store and online on a storefront; store stock has no per-store price.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

L.L.Bean has no public API for its catalog, prices or inventory. Prices, stock and reviews are shown on its storefronts for each product, and this skill reads those public pages with one Scavio key.

See also: REI gear prices and store pickup `rei-api`; Dick's Sporting Goods `dicks-sporting-goods-api`; Nordstrom `nordstrom-product-data`; Zappos footwear and size stock `zappos-api`.

## When to trigger

Use this skill when the user asks to:
- Price an L.L.Bean product (Boat and Tote, Bean Boots, fleece, flannel) per size range and color, with the full price, sale price and percent saved
- Check how many units of an L.L.Bean SKU a store has, for up to 20 stores or every store, or whether a SKU is in stock, on backorder (and until when) or sold out
- Search llbean.com, llbean.ca or the international storefront by keyword, or list a category, sorted by price, best selling, newest or top rated and filtered by color, size, gender, brand, sale, price, % off, width, material or shoe size
- List the L.L.Bean Sale category, optionally 20% to 70% off and up
- Compare one L.L.Bean product's price in the US, Canada and an international country (United Kingdom, Germany, France, Netherlands, Australia, Mexico, Switzerland, Sweden, China, Brazil, India, Singapore)
- Find L.L.Bean stores and outlets near a ZIP, a point or a city, with store pickup flags and this week's hours
- Read L.L.Bean reviews with fit, size purchased, height and weight, filtered by stars, height, weight or words; or L.L.Bean's own review summary
- Get the standard delivery date of an item to a US ZIP
- Read the L.L.Bean department menu or its search-box suggestions

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 1-10 seconds (in the captures: reviews 0.6, the department menu, product and deals 1.1, US search 1.5, a delivery estimate 1.5, store stock 2.2, stores 2.7, the review summary 3, international search 4.8, Canadian search 8.2). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/llbean/search` | Keyword search, 48 per page, 6 sorts, facet filters; a keyword the site sends to a category comes back with `redirected_to` | us, ca, intl | 1 |
| `POST /api/v1/llbean/category` | One category by id, sorted and filtered like search | us, ca, intl | 1 |
| `POST /api/v1/llbean/deals` | The Sale category (id 32), sorted and filtered like search; on us also by % Off | us, ca, intl | 1 |
| `POST /api/v1/llbean/categories` | The department menu (11 departments, about 570 nodes), or one department with its children | us | 1 |
| `POST /api/v1/llbean/product` | One product: on us every item, color and SKU with price, full price, sale price, percent saved and stock; on ca and intl the variant shown with a price per color | us, ca, intl | 1 |
| `POST /api/v1/llbean/store-stock` | Exact units per SKU per store for one item, at up to 20 stores or every store | us | 1 |
| `POST /api/v1/llbean/stores` | Stores near a ZIP, a point or a city, by id, or all, with hours and pickup flags | us | 1 |
| `POST /api/v1/llbean/reviews` | Written reviews with fit data, 4 sorts, up to 100 per page, filtered by stars, height, weight or words; no reviewer names | us | 1 |
| `POST /api/v1/llbean/review-summary` | L.L.Bean's own summary of a product's reviews, with its disclaimer | us | 1 |
| `POST /api/v1/llbean/delivery-estimate` | The standard delivery date of one item to a US ZIP | us | 1 |
| `POST /api/v1/llbean/suggestions` | Search-box suggestions (on ca also popular searches, products and categories) | us, ca | 1 |

Every answer carries `market`, `country`, `host`, `currency` and `language` (en-US, en-CA or en). An endpoint asked for a market it does not serve is an unbilled `400`.

## Prices and stock

US search, category and deal items carry `price` (the current lowest), `full_price` and `full_price_max`, `sale_price` and `sale_price_max` (set only when below the full price), `on_sale`, `stock` (`in_stock` or `backorder`), `stock_text` (a backorder date as given), `new_arrival`, `features` and `colors[]` {`name`, `family`, `on_sale`}. Canadian and international items carry `price`, `price_max` (a range), `list_price` (the was price, when higher), `currency`, `price_text` (as shown: `C$ 138 - C$ 179`), `on_sale`, `promotion` (the storefront's own offer text, `15% OFF This Item!`) and `colors` (names).

The US product has `items[]` (one per size range or fit: Small, Medium, Regular, Tall) with `colors[]` {`color`, `price`, `full_price`, `sale_price`, `percent_saved`, `sold_out`}, and `skus[]` {`sku`, `item_id`, `item`, `color`, `size`, `width`, `stock` (`in_stock`, `backorder`, `out_of_stock`), `status` (`In Stock`, `Limited Quantities`, `Sold Out` or a backorder date), `backorder_date`, `price`, `full_price`, `sale_price`, `percent_saved`}, with `sku_count`, `in_stock_count`, `backorder_count` and `out_of_stock_count`.

- Quote "Boat and Tote, Zip-Top, Medium: $49.95 at llbean.com on 2026-11-27", with the item, the color where it matters, the market and the date.
- `promotion` on ca and intl is the storefront's offer text; never subtract it from the price yourself.
- Report L.L.Bean's prices, flags and counts as given and the arithmetic only. Never judge a price as a good deal and never describe how often a SKU is in stock.

## Workflow

1. **Find the product.** `/search` with `query` (`fleece jacket`) or `/category` with `category_id` (from `/categories`; 474 is US Footwear, 32 is Sale everywhere). Each US item's `product_id` is the input of product, reviews and review summary; its `item_id` is one item of that product. If the answer has `redirected_to`, the keyword opened that category and the listing is the category's, with your sort, page and filters applied.
2. **Prices per item and color.** `/product` with `product_id` (and `market`). On us, read `skus[]` for each SKU's stock and price.
3. **Store units.** `/stores` near a ZIP for `store_id`s, then `/store-stock` with an `item_id` from `items[].item_id` (not the product id), `store_ids` (up to 20) or `all_stores` true, and `product_id` to label each SKU with its color, size and price. `inventory_online` false on a store means the site shows no stock for it.
4. **Abroad.** The same `product_id` usually works on ca and intl: `/product` with `market` `intl` and `country` `de`. Category ids differ from the US site in places.
5. **Reviews.** `/reviews` with `product_id`, `sort`, `page`, `limit`, and `filters` {`rating`, `height`, `weight`, `text`} (height and weight values from `stats.context`, such as `5ft10in` or `170180Lbs`). `/review-summary` for L.L.Bean's own summary.
6. **Delivery.** `/delivery-estimate` with `item_id` and `zip`.
7. **Watching prices or stock:** there is no history. Poll the same products or items on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required on search | Keywords, 1-200 chars |
| `category_id` | string or integer | required on category | A category id: `categories[].category_id` (us) or the number in a storefront link's `/llb/shop/<id>` |
| `market` | string | `us` | `us`, `ca` or `intl` |
| `country` | string | none | With `market` `intl`: `gb`, `de`, `fr`, `nl`, `au`, `mx`, `ch`, `se`, `cn`, `br`, `in`, `sg` (each in its own currency: GBP, EUR, AUD, MXN, CHF, SEK, CNY, BRL, INR, SGD). Korea, New Zealand and Japan are served the US site: use `us` |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`, `best_selling`, `newest`, `top_rated` |
| `page` | integer | 1 | 1-200, 48 per page; `total_pages` reports the last one |
| `filters` | object | none | Up to 8 keys, `{key: value or [values]}` (values of one key are OR-ed, up to 10). Keys: `color`, `size`, `brand`, `gender`, and on us `sale`, `price`, `discount`, `width`, `department`, `category`, `material`, `shoe_size`, `features`, `new`; or any `facets[].key` of an answer, with values exactly as `facets[].values[].value` (`{"price": "0 TO 30"}` on us, `{"color": "Black"}` on ca and intl) |
| `min_discount` | integer | none | Deals on us only: `20`, `30`, `40`, `50`, `60` or `70` (N% & Up) |

### Product (`/product`)

`product_id` (required, digits, `37037`), `market`, `country` as above.

### Categories (`/categories`)

`category_id` (optional): one department or category with its children; without it, the whole menu. US only.

### Store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string or integer | required | An item id from product `items[].item_id` (`112644`, the Medium of the Boat and Tote), not the product id |
| `product_id` | string or integer | none | The item's product: labels each SKU with its color, size and price (same 1 credit) |
| `store_ids` | array | one of the two | Up to 20 store ids (`stores[].store_id`, `0040` or `40`) |
| `all_stores` | boolean | one of the two | true: every store |

### Stores (`/stores`)

One of: `zip` (5-digit US ZIP, ordered by distance), `latitude` + `longitude` (with optional `radius` 1-500 miles, default 100), `city` + `state` (2-letter code), `store_ids`, or `all_stores` true. `limit` 1-75 stores (default 10 near a place).

### Reviews (`/reviews`), review summary (`/review-summary`), delivery estimate (`/delivery-estimate`), suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string or integer | required | Reviews and review summary |
| `sort` | string | `newest` | Reviews: `newest`, `helpful`, `rating_desc`, `rating_asc` |
| `page` | integer | 1 | Reviews: 1-500 |
| `limit` | integer | 20 | Reviews per page, 1-100 |
| `filters` | object | none | Reviews: `rating` (1-5), `height`, `weight` (values from `stats.context`), `text` (words in the review) |
| `item_id`, `zip` | string | required | Delivery estimate: an item id and a US ZIP |
| `query` | string | required | Suggestions: what has been typed so far, 1-100 chars; `market` `us` or `ca` |

## Examples

### Product with every SKU (US)

```bash
curl -X POST https://api.scavio.dev/api/v1/llbean/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "37037"}'
```

Captured `data` (2026-11-27; specs, notes, 3 of 4 items, 11 of 12 colors and 96 of 97 SKUs dropped):

```json
{
  "market": "us",
  "country": null,
  "host": "www.llbean.com",
  "currency": "USD",
  "language": "en-US",
  "product_id": "37037",
  "name": "Boat and Tote®, Zip-Top",
  "url": "https://www.llbean.com/llb/shop/37037?page=boat-and-tote-bag-zip-top",
  "rating": 4.8,
  "review_count": 9735,
  "items": [
    {
      "item_id": "112644",
      "name": "Medium",
      "colors": [
        { "color": "Black", "price": 49.95, "full_price": 49.95, "sale_price": null, "percent_saved": null, "sold_out": false }
      ],
      "sku_count": 24
    }
  ],
  "sku_count": 97,
  "in_stock_count": 41,
  "backorder_count": 32,
  "out_of_stock_count": 24,
  "skus": [
    {
      "sku": "0YL5710002",
      "item_id": "112643",
      "item": "Small",
      "color": "Black",
      "size": "Long",
      "width": null,
      "stock": "backorder",
      "status": "Wednesday, February 3, 2027",
      "backorder_date": "Wednesday, February 3, 2027",
      "price": 44.95,
      "full_price": 44.95,
      "sale_price": null,
      "percent_saved": null
    }
  ]
}
```

The items were Small ($44.95, `112643`), Medium ($49.95), Large ($59.95, `112645`) and Extra-Large ($69.95, `112646`). The German storefront `{"product_id": "120785", "market": "intl", "country": "de"}` answered the Men's Sweater Fleece Full-Zip Jacket at `price` 145, `price_text` "€ 145", `promotions` ["15% OFF This Item!"], 6 colors at EUR 145, `items` Regular and Tall, and `attributes.size` (Small, Medium, ...); no unit counts exist on that storefront. An unknown product is a charged `404`: "No L.L.Bean product with this id."

### Store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/llbean/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "112644", "product_id": "37037", "store_ids": ["0040", "1350", "2140"]}'
```

Captured `data` (2026-11-27; 1 of 24 SKUs shown, notes dropped):

```json
{
  "market": "us",
  "item_id": "112644",
  "product_id": "37037",
  "store_ids": ["0040", "1350", "2140"],
  "sku_count": 24,
  "store_count": 3,
  "stores": [
    { "store_id": "0040", "units": 506, "skus_in_stock": 13 },
    { "store_id": "1350", "units": 32, "skus_in_stock": 7 },
    { "store_id": "2140", "units": 74, "skus_in_stock": 9 }
  ],
  "skus": [
    {
      "sku": "0YL5807001",
      "item": "Medium",
      "color": "Regatta Blue",
      "size": "Regular",
      "width": null,
      "price": 49.95,
      "full_price": 49.95,
      "sale_price": null,
      "status": "out_of_stock",
      "units": 0,
      "stores": [
        { "store_id": "0040", "units": 0, "status": "out_of_stock" },
        { "store_id": "1350", "units": 0, "status": "out_of_stock" }
      ]
    }
  ],
  "unlisted_sku_count": 94
}
```

`units` is the site's exact available quantity per SKU per store for store pickup, as given (Medium Black Regular: 69; Blue Regular: 77; Red Long: 6). A store that does not carry a SKU is not listed for it, and SKUs the product page no longer offers are left out (`unlisted_sku_count`). An unknown item is a charged `404`: "No L.L.Bean item with this id (item_id is product items[].item_id, not the product id)."

### Search on three storefronts

```bash
curl -X POST https://api.scavio.dev/api/v1/llbean/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "fleece jacket", "market": "ca"}'
```

Captured `data.items[0]` (2026-11-27; `total` 73, 2 pages of 48, 15 facets):

```json
{
  "position": 1,
  "product_id": "90568",
  "name": "Men's Fleece-Lined Flannel Shirt, Traditional Fit, Plaid",
  "url": "https://www.llbean.ca/llb/shop/90568.html?page=fleece-lined-flannel-shirt-with-pocket-plaid-mens-regular",
  "price": 159,
  "price_max": null,
  "list_price": null,
  "currency": "CAD",
  "price_text": "C$ 159",
  "on_sale": false,
  "promotion": "15% OFF This Item!",
  "rating": 4.7,
  "review_count": 2152,
  "colors": ["Thyme", "Chalk Blue", "..."]
}
```

The same query with `market` `intl` and `country` `gb` read the same shirt at GBP 110 (`price_text` "£ 110"). On us it answered 24 products on one page, the first the Kids' Mountain Classic Fleece Anorak at $59.95 (`item_id` 528059, `stock` in_stock, `new_arrival` true), with facets Department, Category, ... and `redirected_to` null. A keyword with no results is a charged `404`: "No L.L.Bean results for this query."

### Category, deals, stores, reviews, summary, delivery, suggestions

- `/category` `{"category_id": "474", "sort": "price_asc"}`: Footwear, `total` 439, 10 pages; first the L.L.Bean Footwear Charms, Fun Pack at $12.95, then the Adults' Cresta Wool Lightweight Hiking Socks at $13.99 (`full_price` 16.95, `on_sale` true); facets Gender, Shoe Size and 9 more. An unknown id is a charged `404`: "No L.L.Bean category with this id (a product id is not a category; see categories)."
- `/deals` `{"min_discount": 40}`: Sale (32), `filters_applied` {`DISCOUNT_PCT`: "40% & Up"}, `total` 204, 5 pages; the Women's Mountain Classic Tee at $19.99 against $34.95, the Midweight Cotton Slub Rollneck Pullover at $34.99 against $59.95 (8,401 reviews). Sale items carry no end dates.
- `/categories` `{"category_id": "474"}`: Footwear with Women's, Men's and Kids' and their children (Boots, Hiking Boots & Shoes, Casual), `count` 50.
- `/stores` `{"zip": "04032"}`: 5 stores by distance; the Freeport Outlet Store (`0080`, `type` Outlet, Village Station, 0.13 miles, `inventory_online` false, opened 1989-06-30, Friday 2026-11-27 06:00-22:00) and the Home Store (`0860`, Retail, L.L.Bean Flagship Campus, `store_pickup` true). Store phone numbers are public business contact data.
- `/reviews` `{"product_id": "120785", "limit": 10}`: `total` 1,400 written reviews, 140 pages; `stats` {`average_rating` 4.67, `total_reviews` 4,402, `ratings_only_count` 3,002, `recommended_count` 1,024}, the fit slider average 3.07 between Too Small and Too Large, and `context` histograms of size purchased, height and weight. Each review has `rating`, `title` ("Great as usual"), `text`, `submitted_at`, `verified_purchaser`, `fit` [{`label` Fit, `value_label` True to size}], `size_purchased` Medium, `size_range` Regular, `height` 5'9", `weight` 140-150 lbs and `item_id`; `upcs` lists the UPCs of the items on the page. No reviewer names, nicknames or locations: a title that carries the reviewer's name comes back null.
- `/review-summary` `{"product_id": "37037"}`: L.L.Bean's own summary text, its `disclaimer` as given and `created_at` 2026-08-05. A product without one is a charged `404`: "No L.L.Bean review summary for this product."
- `/delivery-estimate` `{"item_id": "112644", "zip": "10001"}`: `standard_delivery_date` "Sat, November 28" (as given, no year).
- `/suggestions` `{"query": "fle"}`: 10 suggestions (fleece, fleece women, ...). On ca: `suggestions`, `popular_searches`, `products` [{`product_id`, `name`}] and `categories`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def llbean(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/llbean/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Every item of a product with its price per color (1 credit)
p = llbean("product", {"product_id": "37037"})["data"]
for it in p["items"]:
    print(it["item_id"], it["name"], it["colors"][0]["price"])

# 2. Stores near a ZIP, then exact units of one item at those stores (2 credits)
stores = llbean("stores", {"zip": "04032"})["data"]["stores"]
ids = [s["store_id"] for s in stores if s["inventory_online"]]
stock = llbean("store-stock", {"item_id": "112644", "product_id": "37037", "store_ids": ids})["data"]
for s in stock["stores"]:
    print(s["store_id"], s["units"], s["skus_in_stock"])

# 3. The same product in Canada and the United Kingdom (2 credits)
for body in ({"market": "ca"}, {"market": "intl", "country": "gb"}):
    d = llbean("product", {"product_id": "120785", **body})["data"]
    print(d["market"], d["country"], d["currency"], d["price"], d.get("promotions"))

# Prices and units change: store each answer with fetched_at and run this on a
# schedule; that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `market`, `country`, `host`, `currency`, `language` and `notes`.

- **search / category / deals** - `query` (search), `category_id` and `url` (category, deals), `min_discount` (deals), `sort`, `filters_applied`, `redirected_to` (search), `page`, `page_size` (48), `total`, `total_pages`, `has_more`, `count`, `items[]` (US: {`position`, `product_id`, `name`, `url`, `image`, `item_id`, `price`, `full_price`, `full_price_max`, `sale_price`, `sale_price_max`, `on_sale`, `rating`, `review_count`, `stock`, `stock_text`, `new_arrival`, `features`, `colors[]` {`name`, `family`, `on_sale`, `swatch_image`}}; ca and intl: {`position`, `product_id`, `name`, `url`, `image`, `price`, `price_max`, `list_price`, `currency`, `price_text`, `on_sale`, `promotion`, `rating`, `review_count`, `colors`}), `facets[]` {`key`, `label`, `values[]` {`value`, `count`}}.
- **categories** - `category_id`, `count`, `categories[]` {`category_id`, `name`, `slug`, `url`, `children[]`}.
- **product** - US: `product_id`, `name`, `url`, `rating`, `review_count`, `specs[]` {`component`, `specs`}, `materials`, `size_fit`, `items[]` {`item_id`, `name`, `colors[]` {`color`, `price`, `full_price`, `sale_price`, `percent_saved`, `sold_out`}, `sku_count`}, `sku_count`, `in_stock_count`, `backorder_count`, `out_of_stock_count`, `skus[]` (as above). ca and intl: `product_id`, `name`, `brand`, `url`, `image`, `price`, `list_price`, `price_text`, `availability`, `promotions`, `colors[]` {`id`, `name`, `price`, `price_text`, `selectable`}, `items[]` {`id`, `name`, `selectable`}, `attributes` {`size`, `width`}.
- **store-stock** - `item_id`, `product_id`, `store_ids`, `sku_count`, `store_count`, `stores[]` {`store_id`, `units`, `skus_in_stock`}, `skus[]` {`sku`, `item`, `color`, `size`, `width`, `price`, `full_price`, `sale_price`, `status`, `units`, `stores[]` {`store_id`, `units`, `status`}}, `unlisted_sku_count`.
- **stores** - `location`, `count`, `stores[]` {`store_id`, `name`, `shopping_center`, `type`, `address` {`line1`, `line2`, `city`, `state`, `postal_code`}, `phone`, `latitude`, `longitude`, `distance_miles`, `time_zone`, `opened`, `open`, `inventory_online`, `store_pickup`, `curbside_pickup`, `url`, `hours[]` {`date`, `day`, `open`, `close`}}.
- **reviews** - `product_id`, `sort`, `filters_applied`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `verified_purchaser`, `syndicated`, `helpful_votes`, `unhelpful_votes`, `item_id`, `fit[]` {`id`, `label`, `value`, `value_label`, `min_label`, `max_label`}, `size_purchased`, `size_range`, `height`, `weight`, `used_for`, `brand_responses`}, `stats` {`average_rating`, `total_reviews`, `ratings_only_count`, `recommended_count`, `not_recommended_count`, `rating_distribution[]`, `fit[]`, `context[]`}, `upcs[]` {`item_id`, `upcs`}.
- **review-summary** - `product_id`, `summary`, `disclaimer`, `created_at`.
- **delivery-estimate** - `item_id`, `zip`, `standard_delivery_date`.
- **suggestions** - `query`, `count`, `suggestions`, `popular_searches`, `products[]` {`product_id`, `name`}, `categories[]` {`category_id`, `name`, `parent`}.

## Guardrails

- Name it "L.L.Bean (llbean.com, the US outdoor apparel and gear retailer)" on first mention, and name the storefront (llbean.ca, or global.llbean.com for a country) when the answer is not US.
- Prices: quote the item, color, market, currency and `fetched_at` date. Never call any price a member, L.L.Bean Rewards or Mastercard price; those are never returned.
- Offers: `promotion` and `promotions` are the storefront's text as given; never compute a price after them.
- Stock: quote `units` as the store's count at the time of the call and backorder dates as the site's text. Never promise a unit will still be there.
- Reviews: no reviewer names are returned. Quote a review as "an L.L.Bean customer review". The review summary is L.L.Bean's own text; quote it with its disclaimer.
- Not available: member or card prices, unit counts or store stock outside the US, sale end dates, price history (poll and store), carts or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store L.L.Bean data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. L.L.Bean's terms of use restrict automated access or commercial use of its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, SKUs, product, item or store ids, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "market ca is not served on this endpoint: it is available for us."; "market intl needs a country: one of gb, de, fr, nl, au, mx, ch, se, cn, br, in, sg."; "country goes with market intl (us is www.llbean.com, ca is www.llbean.ca)."; "product_id must be an L.L.Bean product id: digits, e.g. 37037 (items[].product_id)."; "item_id is required (an L.L.Bean item id from product items[].item_id, e.g. 112644)."; "Send store_ids or all_stores, not both."; "Send one of: zip, latitude + longitude, city + state, store_ids, or all_stores: true."; "zip must be a 5-digit US ZIP code, e.g. 04032."; "min_discount is a US filter: the Canadian and international Sale pages have no % Off filter."; "filters: at most 8 facets."; a filter key that is not a facet; a review filter other than rating, height, weight or text; a `sort`, `page` or `limit` outside its range. An invalid ZIP on the delivery estimate is an unbilled `400` too.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No L.L.Bean product with this id.", "No L.L.Bean category with this id (a product id is not a category; see categories).", "No L.L.Bean results for this query.", "No L.L.Bean item with this id (item_id is product items[].item_id, not the product id).", "No L.L.Bean review summary for this product.", "L.L.Bean gave no delivery estimate for this item and ZIP.". On ca and intl: "No L.L.Bean product with this id on the Canadian storefront." (or international). Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api).
- `502` means L.L.Bean data was temporarily unavailable ("L.L.Bean is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.101.0
npm install scavio@0.102.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.llbean.search({ query: "fleece jacket", market: "intl", country: "gb" });
const { data: boots } = await scavio.llbean.category({ category_id: "474", sort: "price_asc" });
const { data: tree } = await scavio.llbean.categories({ category_id: "474" });
const { data: tote } = await scavio.llbean.product({ product_id: "37037" });
const { data: units } = await scavio.llbean.storeStock({ item_id: "112644", product_id: "37037", store_ids: ["0040", "1350"] });
const { data: near } = await scavio.llbean.stores({ zip: "04032" });
const { data: reviews } = await scavio.llbean.reviews({ product_id: "120785", filters: { rating: 5 } });
const { data: summary } = await scavio.llbean.reviewSummary({ product_id: "37037" });
const { data: eta } = await scavio.llbean.deliveryEstimate({ item_id: "112644", zip: "10001" });
const { data: typed } = await scavio.llbean.suggestions({ query: "fle" });
const { data: sale } = await scavio.llbean.deals({ min_discount: 40 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.llbean.search(...)`, `category`, `categories`, `product`, `store_stock`, `stores`, `reviews`, `review_summary`, `delivery_estimate`, `suggestions` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_llbean`, `get_llbean_category`, `get_llbean_categories`, `get_llbean_product`, `get_llbean_store_stock`, `get_llbean_stores`, `get_llbean_reviews`, `get_llbean_review_summary`, `get_llbean_delivery_estimate`, `get_llbean_suggestions` and `get_llbean_deals`. L.L.Bean is opt-in: add `llbean` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.101.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,llbean"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/llbean-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [category](https://scavio.dev/docs/llbean-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [categories](https://scavio.dev/docs/llbean-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [product](https://scavio.dev/docs/llbean-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [store stock](https://scavio.dev/docs/llbean-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [stores](https://scavio.dev/docs/llbean-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [reviews](https://scavio.dev/docs/llbean-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [review summary](https://scavio.dev/docs/llbean-review-summary?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [delivery estimate](https://scavio.dev/docs/llbean-delivery-estimate?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [suggestions](https://scavio.dev/docs/llbean-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api), [deals](https://scavio.dev/docs/llbean-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api). Overview: [L.L.Bean API](https://scavio.dev/llbean-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=llbean-api).
