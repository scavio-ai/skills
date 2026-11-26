# Zappos API - Shoe Prices, Size Stock, Reviews, 6pm Outlet

Read Zappos (zappos.com, the US shoe and clothing store, an Amazon company) and 6pm (6pm.com, the Zappos outlet site): keyword or whole-catalog search with facets and sorts, one product with every color, size and width, its price, original price, percent off and the exact units in stock, UPC and ASIN per size, customer reviews with fit ratings, customer questions and answers, the lowest price Zappos gives per color, the category tree and search suggestions. Both sites are US stores in USD and English. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Zappos shoe prices and size stock.** What a shoe costs at zappos.com in each color, and how many pairs of each size and width Zappos has. On 2026-11-26 the Brooks Adrenaline GTS 25 (product `10002909`, women's) read 22 colors (`style_count`) and 512 sizes (`sku_count`), 114 of them in stock, `total_on_hand` 5,995. The color Grey/Blackened Pearl/Coral (style `6549810`) read $109.95 against an `original_price` of $155, `percent_off` 29, `on_hand` 1,547 across 64 size and width combinations, 50 of them in stock: size 8 B - Medium (stock `59742431`, UPC `195394665932`) 143 units, size 9.5 B - Medium 135, size 5 A - Narrow 1. Eleven of the 22 colors were out of stock and carried `price` null with the `price_note` "No price: the site shows no price for a color that is out of stock." Reviewers' fit answers: 78% "Felt true to size", 84% "Felt true to width", 54% "Excellent arch support". The second job is the outlet: `site` `6pm` reads the same catalog on 6pm.com, where prices and stock differ (a women's Brooks search on 6pm read 37 items, such as Cascadia 19 at $112.50 against $150, 25% off, 13 units).

Seven limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **Units are exact and warehouse-only.** `on_hand` is the number of units Zappos reports in stock: per size (`skus[].on_hand`), per color (`styles[].on_hand`), per product (`total_on_hand`) and per search item (all sizes of that color). Zappos sells online and has no stores: there is no store stock or store finder.
- **Out of stock means no price.** A color or a size that is out of stock has `price` null on the site; `original_price` can still be given and `price_note` says why. Never fill in a price for it.
- **zappos.com and 6pm are separate stores with the same ids.** Product, style and stock ids are the same on both, but prices and stock differ (the probe measured one style at $93.00 on Zappos and $105.00 on 6pm, and another out of stock on Zappos but $75.00 with 2 units on 6pm). Every answer names its `site` and `host`. Reviews, questions and lowest prices exist on zappos.com only: `site` `6pm` on them is a `400`, not charged.
- **The lowest price is Zappos' figure, without a period.** `/lowest-prices` gives the lowest price Zappos states for each color for its product page. Zappos does not say what period it covers and it can include colors out of stock now. Never call it a 30-day low or any dated low.
- **One value per facet.** Search filters take one value of each facet (Zappos matches one value of a facet at a time): run one search per value. Size and width need `gender` Men or Women.
- **No history.** Nothing is cached or kept: poll and store your own series.

Zappos has no public API. The keyed developer API it launched in 2010 is gone: developer.zappos.com now redirects to the zappos.com home page. Its affiliate program runs on the Rakuten Affiliate Network with links and banners; no data feed is described. Prices, sizes and units in stock are shown on zappos.com and 6pm.com to every visitor, and this skill reads those public pages with one Scavio key.

Zappos says it was founded in 1999 and that Zappos.com LLC is a subsidiary of Amazon.com, Inc. (zappos.com about page). Quote this with its source, never from the samples.

See also: for the same shoe (same UPC or ASIN) at Amazon use `amazon-product-data`; at Nike `nike-api`; at Foot Locker `foot-locker-api`; at Dick's Sporting Goods `dicks-sporting-goods-api`; at Nordstrom `nordstrom-product-data`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Price a shoe or a clothing item at Zappos or 6pm in every color, with the original price and percent off
- Check which sizes and widths of a shoe Zappos has in stock, and how many units of each
- Search zappos.com or 6pm.com by keyword, brand, gender, category, size, width, color, price band or sale, sorted by price, percent off, rating, newest or best sellers
- List what is on sale at Zappos or 6pm, by percent off
- Look up a Zappos product by a style id, a stock id (one size) or an ASIN, and read its UPC per size
- Read Zappos reviews with comfort, look, size, width and arch fit ratings, or how reviewers say a shoe fits
- Read the customer questions on a Zappos product, with Zappos staff answers flagged
- Read the lowest price Zappos gives for each color of a product
- Browse the Zappos department, category and subcategory tree with item counts, or pull search suggestions
- Compare one shoe at Zappos, 6pm and Amazon (with `amazon-product-data`, by ASIN or UPC)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, lowest prices answered in under 1 second, suggestions in about 1, search, product and questions in 2-3, reviews and categories in about 5. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Sites | Credits |
|---|---|---|---|
| `POST /api/v1/zappos/search` | Keywords or the whole catalog: up to 100 items per page with total, price, original price, percent off, units on hand for the color, rating, badges, and facets | zappos, 6pm | 1 |
| `POST /api/v1/zappos/product` | One product by product, style, stock id or ASIN: every color with its price and units, every size and width with exact units, UPC and ASIN, fit, review summary, description and size charts | zappos, 6pm | 1 |
| `POST /api/v1/zappos/reviews` | Reviews of one product, 25 per page, most helpful first or latest, with overall, comfort and look ratings and size, width and arch fit | zappos | 1 |
| `POST /api/v1/zappos/questions` | Every customer question on one product with its answers, Zappos staff answers flagged | zappos | 1 |
| `POST /api/v1/zappos/lowest-prices` | The lowest price Zappos gives for each color of one product | zappos | 1 |
| `POST /api/v1/zappos/categories` | One level of the department > category > subcategory tree with item counts and the facets to search it | zappos, 6pm | 1 |
| `POST /api/v1/zappos/suggestions` | Up to 10 search-box completions for a partial query | zappos, 6pm | 1 |

`site` is `zappos` (default, www.zappos.com) or `6pm` (www.6pm.com, the Zappos outlet site). Every answer carries `site`, `host`, `country` (`us`), `currency` (`USD`) and `language` (`en`).

## Prices, percent off and units

| Field | Meaning |
|---|---|
| `price` | The price as Zappos (or 6pm) shows it, USD. `null` for a color or size that is out of stock |
| `original_price` | The original price Zappos gives beside it; can be given when `price` is null |
| `percent_off` | The percent off as the site gives it (29 for $109.95 against $155; rounded, so do not multiply it back) |
| `on_sale`, `final_sale`, `is_new` | The site's own flags |
| `price_note` | Why `price` is null ("No price: the site shows no price for a color that is out of stock.") |
| `on_hand` | Units in stock as the site reports them: per size (`skus[]`), per color (`styles[]`), per product (`total_on_hand`), per search item (all sizes of that color) |
| `badges`, `promo_badges` | The site's badges ({`code` `BS`, `name` "Best Seller"}) |

- **Report the site and date:** "$109.95 at zappos.com on 2026-11-26, original price $155, 29% off". A 6pm price is a 6pm price: never carry it to zappos.com or the reverse.
- **Per size:** quote `skus[].on_hand` with its `size` and `width` ("size 8 B - Medium: 143 units"). Units change with every order: give the `fetched_at` time.
- **Lowest prices:** quote them as "the lowest price Zappos gives for this color", with no period. On product `10002909` six colors read a lowest price of $124.95, all of them out of stock on the product page that day, while every in-stock color read $109.95 on both: report each as given, never reconcile them.
- Report the labels and the arithmetic only. Never judge an original price or a discount, and never describe how often an item is on sale.

## Workflow

1. **Find the item.** `/search` with `query` (or none for the whole catalog) and `facets`. Each item's `product_id` is the input of every other endpoint; `style_id` (one color) and `stock_id` (one size of one color) also open a product.
2. **Read it in full.** `/product` with exactly one of `product_id`, `style_id`, `stock_id` or `asin`: every color (`styles[]`) and size (`styles[].skus[]`) with price, original price and exact units. A style, stock or ASIN lookup answers the whole product and names the match in `match`.
3. **Narrow a search.** `facets` with one value each: `brand`, `brand_id`, `gender`, `department`, `category`, `subcategory`, `color`, `price` (a band as listed: "$100 and Under"), `on_sale` (`true`), `size` and `width` (with `gender` Men or Women), or any `facets[].field` an answer lists (`txAttrFacet_Materials`, `hc_men_size`). Up to 12 facets.
4. **Sort and page.** `sort` (`relevance`, `price_asc`, `price_desc`, `percent_off`, `rating`, `newest`, `best_sellers`); `mode` `sale` for items on sale by percent off; `page` (1-2,000) and `limit` (1-100, default 50).
5. **Browse the tree.** `/categories` without parameters lists departments; with `department` its categories; with `category` its subcategories. Each entry's `facets` goes straight into search.
6. **Fit and questions.** `/reviews` with `product_id`, `page` and `sort` (`best` or `latest`); `/questions` with `product_id`. Both zappos.com only.
7. **Outlet.** Send `site` `6pm` on search, product, categories and suggestions; the same ids work on both sites.
8. **Watching prices or stock:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at` and `site`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `site` | string | `zappos` | `zappos` or `6pm` |
| `query` | string | none | Search keywords, 1-200 characters. Leave out to browse the whole catalog (narrowed by facets) |
| `facets` | object | none | {facet: one value}, up to 12. Names: `brand`, `brand_id` (`26` for Brooks), `gender` (Women, Men, Girls, Boys), `department` (Shoes), `category` (Boots), `subcategory` (Running Shoes), `color` (Black), `price` (a band as listed, "$100 and Under"; 6pm has its own bands), `on_sale` (`true`), `size` and `width` (with `gender` Men or Women: `{"gender": "Men", "size": "10", "width": "Wide"}`), or any `facets[].field` from an answer. Values are matched as the site writes them; an unknown value is an empty answer |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`, `percent_off`, `rating`, `newest`, `best_sellers` |
| `mode` | string | `all` | `all` or `sale` (items on sale, by percent off unless `sort` is set) |
| `page` | integer | 1 | 1-2,000. A page past the last one is an empty `items` list with the real `total` |
| `limit` | integer | 50 | Items per page, 1-100 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `site` | string | `zappos` | `zappos` or `6pm` |
| `product_id` | string | one of | A Zappos product id, 4-10 digits (`10002909`; the number after /product/ in a Zappos link) |
| `style_id` | string | one of | A style (one color) id (`6549810`, `items[].style_id`) |
| `stock_id` | string | one of | A stock id (one size of one color, `skus[].stock_id`, `60162981`) |
| `asin` | string | one of | An ASIN (`skus[].asin`, `B0F4JKCMQ2`) |

Send exactly one of `product_id`, `style_id`, `stock_id` or `asin`.

### Reviews (`/reviews`), questions (`/questions`), lowest prices (`/lowest-prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | A Zappos product id |
| `page` | integer | 1 | Reviews: 1-1,000, 25 reviews per page (`total_pages` says how many) |
| `sort` | string | `best` | Reviews: `best` (most helpful first) or `latest` |
| `site` | string | `zappos` | `zappos` only; `6pm` is a `400` that says so, not charged |

### Categories (`/categories`) and suggestions (`/suggestions`)

`/categories` takes `site`, an optional `department` (`Shoes`, a top-level `categories[].name`) and an optional `category` (`Sneakers & Athletic Shoes`, with `department` or alone). `/suggestions` takes `site` and `query` (1-100 characters, required).

## Examples

### One product with every color, size and unit count

```bash
curl -X POST https://api.scavio.dev/api/v1/zappos/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "10002909"}'
```

Captured `data` (2026-11-26; `review_summary` and `description` dropped, 2 of 22 styles shown, `attributes` cut to 3 of 16, `images` dropped, `skus` cut to 3 of 64, the second style cut to 8 fields):

```json
{
  "site": "zappos",
  "host": "www.zappos.com",
  "country": "us",
  "currency": "USD",
  "language": "en",
  "requested": { "product_id": "10002909" },
  "match": null,
  "product_id": "10002909",
  "name": "Adrenaline GTS 25",
  "brand": { "id": "26", "name": "Brooks" },
  "brand_product_name": "Brooks Adrenaline GTS 25",
  "product_type": "Shoes",
  "category": "Sneakers & Athletic Shoes",
  "subcategory": "Running Shoes",
  "genders": ["Women"],
  "url": "https://www.zappos.com/product/10002909",
  "rating": 5,
  "review_count": 1023,
  "fit": {
    "size": { "text": "Felt true to size", "percent": 78 },
    "width": { "text": "Felt true to width", "percent": 84 },
    "arch": { "text": "Excellent arch support", "percent": 54 }
  },
  "out_of_stock": false,
  "style_count": 22,
  "sku_count": 512,
  "in_stock_sku_count": 114,
  "total_on_hand": 5995,
  "styles": [
    {
      "style_id": "6549810",
      "color_id": "1107247",
      "color": "Grey/Blackened Pearl/Coral",
      "price": 109.95,
      "original_price": 155,
      "percent_off": 29,
      "price_note": null,
      "on_sale": true,
      "is_new": false,
      "final_sale": false,
      "launch_date": "2025-11-01T07:00:00.000Z",
      "on_hand": 1547,
      "in_stock": true,
      "badges": [{ "code": "BS", "name": "Best Seller" }],
      "promo_badges": [],
      "attributes": [
        { "name": "Activity", "value": "Running" },
        { "name": "Closures", "value": "Lace up" },
        { "name": "Running Footwear Cushioning", "value": "3-Maximum Cushioning" }
      ],
      "url": "https://www.zappos.com/product/10002909/color/1107247",
      "skus": [
        { "stock_id": "59742135", "size": "5", "width": "A - Narrow", "on_hand": 1, "price": 109.95, "original_price": 155, "upc": "195394665680", "asin": "B0DM3B248L" },
        { "stock_id": "59718700", "size": "5", "width": "B - Medium", "on_hand": 0, "price": null, "original_price": 155, "upc": "195394665697", "asin": "B0DM3LRRQP" },
        { "stock_id": "59742431", "size": "8", "width": "B - Medium", "on_hand": 143, "price": 109.95, "original_price": 155, "upc": "195394665932", "asin": "B0DM3FWZ5V" }
      ]
    },
    {
      "style_id": "6549827",
      "color": "Black/Cyber Pink/Iced Aqua",
      "price": null,
      "original_price": 155,
      "percent_off": null,
      "price_note": "No price: the site shows no price for a color that is out of stock.",
      "on_hand": 0,
      "in_stock": false
    }
  ],
  "notes": [
    "price is null for a color or a size that is out of stock: the site shows no price for it (original_price can still be given).",
    "on_hand is the exact number of units the site has in stock (warehouse stock: Zappos sells online and has no stores)."
  ]
}
```

Grey/Blackened Pearl/Coral: $109.95 against $155, 29% off as Zappos gives it (a rounded percent), 1,547 units, the most at size 8 B - Medium (143) and 9.5 B - Medium (135). `{"stock_id": "60162981"}` opens the same product with `match` naming that size; `{"asin": "B0F4JKCMQ2"}` likewise. An unknown id is a charged `404` ("No Zappos product has product_id <id>.").

### Search on the outlet

```bash
curl -X POST https://api.scavio.dev/api/v1/zappos/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"site": "6pm", "facets": {"brand": "Brooks", "gender": "Women"}, "limit": 10}'
```

Captured `data` (2026-11-26; 2 of 10 items shown with 10 of their fields, `facets` dropped):

```json
{
  "site": "6pm",
  "host": "www.6pm.com",
  "country": "us",
  "currency": "USD",
  "language": "en",
  "query": null,
  "mode": "all",
  "sort": "relevance",
  "page": 1,
  "limit": 10,
  "total": 37,
  "total_pages": 4,
  "searched_as": null,
  "applied_filters": { "gender": "Women", "brand": "Brooks" },
  "count": 10,
  "items": [
    {
      "product_id": "10003256",
      "style_id": "6551520",
      "name": "Luxe Tight",
      "brand": "Brooks",
      "price": 45,
      "original_price": 90,
      "percent_off": 50,
      "on_sale": true,
      "on_hand": 1,
      "badges": []
    },
    {
      "product_id": "10002914",
      "style_id": "6549909",
      "name": "Cascadia 19",
      "brand": "Brooks",
      "price": 112.5,
      "original_price": 150,
      "percent_off": 25,
      "on_sale": true,
      "on_hand": 13,
      "badges": []
    }
  ]
}
```

On zappos.com, `{"query": "running shoes", "limit": 10}` read `total` 7,142 and 715 pages at that limit, the first item adidas Terrex Agravic GTX 2 Trail Running Shoes at $160 with 16 units of that color, then ASICS Novablast 6 Tenka at $164.95 with 648. Its facets were Brand (191 values, adidas 329 items), Color (Black 1,751), Gender, Department, Sale and Price; send `facets[].field` and a `values[].value` back in `facets`. The 6pm facets had their own price bands ("$25 and Under", "$30 and Under", ...).

### Reviews with fit ratings

```bash
curl -X POST https://api.scavio.dev/api/v1/zappos/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "9984296"}'
```

Captured `data` (2026-11-26; 1 of 25 reviews shown, `text` shortened):

```json
{
  "site": "zappos",
  "host": "www.zappos.com",
  "country": "us",
  "currency": "USD",
  "language": "en",
  "product_id": "9984296",
  "name": "Bondi 9",
  "brand": "HOKA",
  "rating": 4,
  "total_reviews": 2558,
  "page": 1,
  "total_pages": 103,
  "sort": "best",
  "count": 25,
  "reviews": [
    {
      "id": "17511114",
      "overall_rating": 1,
      "comfort_rating": 2,
      "look_rating": 5,
      "size_fit": "Felt true to size",
      "width_fit": "Felt true to width",
      "arch_fit": "Moderate arch support",
      "text": "Initially I thought the Bondi 9 was perfection. I had a new pair of Bondi 7’s on when they arrived and it was like a “new and improved” version. ...",
      "date": "2025-02-24T05:55:02.000Z",
      "upvotes": 171,
      "verified_purchase": false,
      "incentivized": false,
      "customer_reward_review": true,
      "source": null,
      "other_shoes": null,
      "media": []
    }
  ],
  "per_page": 25
}
```

`{"product_id": "9984296", "page": 2, "sort": "latest"}` reads the next 25, newest first. No reviewer names, locations or bylines are returned.

### Questions, lowest prices, categories and suggestions

- `/questions` `{"product_id": "9405856"}` (UGG Classic Ultra Mini): `total` 33, all in one answer, `staff_answer_count` 11. Each question has `top_answer` and `answers`, each answer with `upvotes`, `best` and `is_staff` (a Zappos staff answer). No asker or answerer names.
- `/lowest-prices` `{"product_id": "10002909"}`: 20 styles, such as `6549810` $109.95 and `6549811` $124.95, with the note "The lowest price of each style (color) as Zappos gives it for its product page. Zappos does not state the period it covers; it can include colors that are out of stock now." A product with no lowest prices is a charged `404`.
- `/categories` `{"department": "Shoes"}`: `total` 63,603 items in 13 categories, Sneakers & Athletic Shoes 21,967, Boots 11,691, Sandals 10,686, Heels 8,609 down to Crib Shoes 33, each with `facets` {`department`, `category`} to send to search.
- `/suggestions` `{"query": "hoka bon"}`: 10 completions, "hoka bondi", "hoka bondi sr", "hoka bondi sr mens", "hoka bondi slip on", ...

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def zappos(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/zappos/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Women's Brooks running shoes on sale, biggest discount first (1 credit)
hits = zappos("search", {"facets": {"brand": "Brooks", "gender": "Women", "subcategory": "Running Shoes"}, "mode": "sale", "limit": 20})["data"]
for i in hits["items"][:5]:
    print(i["product_id"], i["name"], i["color"], i["price"], i["original_price"], i["percent_off"], i["on_hand"])

# 2. Every size of one shoe with exact units (1 credit)
p = zappos("product", {"product_id": "10002909"})["data"]
for s in p["styles"]:
    if not s["in_stock"]:
        print(s["color"], "out of stock:", s["price_note"])
        continue
    sizes = [(k["size"], k["width"], k["on_hand"]) for k in s["skus"] if k["on_hand"] > 0]
    print(s["color"], s["price"], s["original_price"], s["on_hand"], sizes[:5])

# 3. The same product on 6pm, the outlet (1 credit): prices and units differ
outlet = zappos("product", {"product_id": "10002909", "site": "6pm"})["data"]
print(outlet["site"], outlet["total_on_hand"])

# Prices and units change with every order. Store each answer with fetched_at
# and site, and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `site`, `host`, `country` (`us`), `currency` (`USD`) and `language` (`en`).

- **search** - `query`, `mode`, `sort`, `page`, `limit`, `total`, `total_pages`, `searched_as` (the term the site searched when it corrected the query), `applied_filters`, `count`, `items[]` {`position`, `product_id`, `style_id`, `color_id`, `name`, `brand`, `color`, `price`, `original_price`, `percent_off`, `on_sale`, `is_new`, `rating`, `review_count`, `on_hand`, `gender`, `product_type`, `badges[]` {`code`, `name`}, `promo_badges`, `image`, `url`}, `facets[]` {`field`, `name`, `group`, `values[]` {`value`, `name`, `count`, `selected`}}.
- **product** - `requested`, `match` {`style_id`, `stock_id`}, `product_id`, `name`, `brand` {`id`, `name`}, `brand_product_name`, `product_type`, `category`, `subcategory`, `genders`, `url`, `rating`, `review_count`, `fit` {`size`, `width`, `arch`: {`text`, `percent`}}, `review_summary` (`total_reviews`, `average_rating`, `overall_star_counts`, overall / comfort / look star percent, size / width / arch fit counts and percent, most and least helpful review without reviewer names), `description` {`bullets`, `measurements`, `size_charts`}, `out_of_stock`, `style_count`, `sku_count`, `in_stock_sku_count`, `total_on_hand`, `styles[]` {`style_id`, `color_id`, `color`, `price`, `original_price`, `percent_off`, `price_note`, `on_sale`, `is_new`, `final_sale`, `launch_date`, `on_hand`, `in_stock`, `badges`, `promo_badges`, `attributes[]` {`name`, `value`}, `images`, `url`, `skus[]` {`stock_id`, `size`, `width`, `on_hand`, `price`, `original_price`, `upc`, `asin`}}, `notes`.
- **reviews** - `product_id`, `name`, `brand`, `rating`, `total_reviews`, `page`, `total_pages`, `per_page`, `sort`, `count`, `reviews[]` {`id`, `overall_rating`, `comfort_rating`, `look_rating`, `size_fit`, `width_fit`, `arch_fit`, `text`, `date`, `upvotes`, `verified_purchase`, `incentivized`, `customer_reward_review`, `source`, `other_shoes`, `media[]` {`type`, `url`}}.
- **questions** - `product_id`, `total`, `count`, `staff_answer_count`, `questions[]` {`id`, `text`, `votes`, `answer_count`, `top_answer`, `answers[]` {`text`, `date`, `upvotes`, `best`, `is_staff`}}.
- **lowest-prices** - `product_id`, `count`, `styles[]` {`style_id`, `price`}, `note`.
- **categories** - `level`, `department`, `category`, `total`, `count`, `categories[]` {`name`, `count`, `level`, `facets`}.
- **suggestions** - `query`, `count`, `suggestions`.

## Guardrails

- Name it "Zappos (zappos.com, the US shoe and clothing store, an Amazon company)" or "6pm (6pm.com, the Zappos outlet site)" on first mention, matching `site`. Zappos accounts and VIP status are not read.
- Prices: quote `price` with `original_price` and `percent_off` as given, the site and the `fetched_at` date. Never carry a 6pm price to zappos.com or the reverse, and never fill in a price that is null.
- Lowest prices: "the lowest price Zappos gives for this color", with no period. Never call it a 30-day low, an all-time low or a price history.
- Stock: `on_hand` units as the site reported them at the moment of the call; Scavio makes no promise of their accuracy. They are warehouse units: never describe them as store stock, and never promise delivery.
- Comparing with Amazon or other retailers: compare only the same item (same UPC or ASIN, same size), each with its date and site. Never call one retailer cheaper beyond the numbers shown.
- Reviews and questions: no reviewer, asker or answerer names are returned. Fit percentages are reviewers' answers as Zappos gives them, not measurements.
- Not available: stores, store stock or store pickup (Zappos has no stores), reviews, questions or lowest prices on 6pm, more than one value per facet in one search, VIP or member prices, price history (poll and store), cart, checkout or ordering. This API cannot reserve or buy.
- Terms: Scavio does not collect or store Zappos data: each call fetches the public Zappos or 6pm page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Zappos' terms of use cover how its sites may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Zappos product photos or logos; link products by `url` instead.
- Never fabricate prices, units, sizes, ids, UPCs, ASINs, ratings or fit figures. Only return what the API returned, with the `fetched_at` time, the site and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "site must be zappos (zappos.com, the default) or 6pm (6pm.com, the Zappos outlet site)."; "6pm (6pm.com) has no reviews of its own: reviews come from zappos.com. Send site zappos (6pm uses the same product ids)." (likewise questions and lowest prices); "Send exactly one of product_id, style_id, stock_id (a size of one color) or asin."; "product_id must be a Zappos product id: 4 to 10 digits, e.g. 10002909."; "asin must be 10 letters and digits, e.g. B0F4JKCMQ2 (skus[].asin of a product answer)."; "facets.brand: one value per facet (Zappos matches one value of a facet at a time; run one search per value)."; "facets: at most 12 facets."; a `size` or `width` facet without `gender` Men or Women; a facet name that is not a Zappos facet; a `page`, `limit` or `sort` outside its range or list.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Zappos product has product_id <id>." (or style_id, stock_id, asin; "No 6pm product ..." on 6pm), "Zappos has no reviews page for product <id>.", "Zappos lists no lowest prices for product <id>.", "Zappos has no department \"<name>\".", "Zappos has no category \"<name>\" in <department>.", "Nothing was found for this search.". Take ids and category names from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api).
- `502` means Zappos data was temporarily unavailable ("Zappos is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.zappos.search({ query: "running shoes", sort: "best_sellers" });
const { data: outlet } = await scavio.zappos.search({ site: "6pm", facets: { brand: "Brooks", gender: "Women" } });
const { data: product } = await scavio.zappos.product({ product_id: "10002909" });
const { data: bySize } = await scavio.zappos.product({ stock_id: "60162981" });
const { data: reviews } = await scavio.zappos.reviews({ product_id: "9984296", sort: "latest" });
const { data: questions } = await scavio.zappos.questions({ product_id: "9405856" });
const { data: lows } = await scavio.zappos.lowestPrices({ product_id: "10002909" });
const { data: tree } = await scavio.zappos.categories({ department: "Shoes" });
const { data: suggest } = await scavio.zappos.suggestions({ query: "hoka bon" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.zappos.search(...)`, `product`, `reviews`, `questions`, `lowest_prices`, `categories` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_zappos`, `get_zappos_product`, `get_zappos_reviews`, `get_zappos_questions`, `get_zappos_lowest_prices`, `get_zappos_categories` and `get_zappos_suggestions`. Zappos is opt-in: add `zappos` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,zappos"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/zappos-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api), [product](https://scavio.dev/docs/zappos-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api), [reviews](https://scavio.dev/docs/zappos-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api), [questions](https://scavio.dev/docs/zappos-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api), [lowest prices](https://scavio.dev/docs/zappos-lowest-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api), [categories](https://scavio.dev/docs/zappos-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api), [suggestions](https://scavio.dev/docs/zappos-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api). Overview: [Zappos API](https://scavio.dev/zappos-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=zappos-api).
