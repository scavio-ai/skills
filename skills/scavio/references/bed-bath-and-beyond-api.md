# Bed Bath & Beyond API - Prices, Online Stock, Doorbusters, Reviews

Read Bed Bath & Beyond (bedbathandbeyond.com, the US online home goods store): keyword search, category listings and the department menu, one product with every option's price and online stock, a delivery estimate to a ZIP, customer reviews and questions, the stores of the Bed Bath & Beyond family and the deals page and deal lists. US only (en-US, USD). Every endpoint returns structured JSON at 1 credit per call; search, category and deal lists are 2.

**The job this skill is for: what a home goods product and each of its options costs at bedbathandbeyond.com today, and how many are in online stock.** Bed Bath & Beyond prices every option (size and color) on its own, with a compare price and the sale window. On 2026-11-27 the Superior Egyptian Cotton 6 Piece Towel Set (product `5296998`) read "Sale Starts at" $63.98 against an MSRP of $157.50 (59% off), with 26 of its 49 options in stock; the Ash Grey 6-Piece Set (option `94445783`) read $74.25 against a was price of $93.99, on sale from 2026-11-25 to 2026-12-07, with 97 units on hand, and the Black set $68.84 with 1,423 on hand. Delivered to New York ZIP 10001 it read Standard, FREE, Mon, Nov. 30. The second job is the deals: the deals page carried the countdown "Black Friday Sale ends in" to 2026-11-30T05:00Z and the Doorbusters list read 1,133 products. Pair it with `wayfair-api` or `williams-sonoma-api` for the same category at other home stores, and `amazon-product-data` for the same item at Amazon (match on brand and MPN).

Eight limits shape every answer, so say them plainly:
- **1 or 2 credits per call.** Search, category and the deal lists are 2; the deals page, product, delivery estimate, reviews, questions, stores and the department menu are 1 (a product is occasionally 2 when it needs a second lookup). `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **Online stock only.** `qty_on_hand` per option is the online stock. Bed Bath & Beyond publishes no store stock and no store prices; the stores endpoint is a directory.
- **Out-of-stock options are left out.** The site lists in-stock options only: `option_count` counts those listed and `original_option_count` all of them (26 of 49). A product no longer sold answers `in_stock` false with no options, not a 404.
- **Promo codes are badges, never applied.** `promo` (`30% Off Code CYBER30`) is the badge the page shows; the price is never computed after it.
- **Sale ends as given.** `sale_ends` on listings and `sale_end` on options are the site's values; some read far in the future (`05-Oct-2027 16:35:00`) and look like placeholders.
- **Sponsored tiles are kept apart.** `items` are the organic results; `sponsored_items` are the site's sponsored tiles, marked `sponsored` true.
- **Lists stop at page 84.** Page size varies (about 48-81 products). The price filter is not offered on keyword lists: use `/category` with `price_min` and `price_max`.
- **No history, no UPCs.** Everything is the page at the moment of the call; Scavio keeps nothing. No UPC or GTIN is published. Poll and store your own series.

Bed Bath & Beyond has no public API for its catalog, prices or stock. Prices, stock and reviews are shown on bedbathandbeyond.com for each product, and this skill reads those public pages with one Scavio key.

See also: Wayfair `wayfair-api`; Williams-Sonoma, Pottery Barn and West Elm `williams-sonoma-api`; Target `target-product-data`; Walmart `walmart-product-data`; Amazon `amazon-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a Bed Bath & Beyond product and each of its options (size, color), with the compare price (MSRP or was), savings, percent off and the sale window
- Check how many units of an option are in online stock, its purchase limit and whether it is on backorder
- Search bedbathandbeyond.com by keyword, or list a category (Bedding Sets, Sofas & Couches, Rugs), sorted by best selling, on sale, price, rating or newest and filtered by attribute (color, size), price range, rating, brand, promotion, fast delivery or expedited shipping
- List the Bed Bath & Beyond deals: the deals page countdown and Doorbusters, or the Black Friday, On Sale, Doorbusters and Holiday Brand Deals lists
- Get the delivery date and shipping charge of one option, for a quantity, to a US ZIP
- Read Bed Bath & Beyond customer reviews (newest, most helpful, highest, lowest, by stars, by text) or customer questions and answers
- Find Bed Bath & Beyond, The Container Store or Kirkland's stores near a ZIP, a point or in a state, with hours
- Read the Bed Bath & Beyond department menu

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit (search, category and deal lists 2), so 50 credits cover 25 to 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 2-30 seconds (in the captures: questions 1.7, product 2.7, stores 2.8, the deals page 3, a delivery estimate 3.2, reviews 3.4, the department menu 4.2, search 6.1, a category 7.3, the Doorbusters list 11, a sorted search 28). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/bedbathbeyond/search` | Keyword search (or a facet link from an earlier answer): organic items and sponsored tiles apart, facets, matching categories, related searches | 2 |
| `POST /api/v1/bedbathbeyond/category` | One category's list with sorts and attribute, price range, rating, brand, promotion and delivery filters; breadcrumbs and child categories | 2 |
| `POST /api/v1/bedbathbeyond/categories` | The department menu: 13 departments, their groups and links with slug and category id | 1 |
| `POST /api/v1/bedbathbeyond/product` | One product: lead price and label, compare price, savings, rating histogram, specs, taxonomy and every in-stock option with price, sale window and exact online stock | 1 (occasionally 2) |
| `POST /api/v1/bedbathbeyond/delivery-estimate` | Delivery date and shipping charge of one option, for a quantity, to a US ZIP | 1 |
| `POST /api/v1/bedbathbeyond/reviews` | Customer reviews in 4 sorts, with a star filter and text search; no reviewer names | 1 |
| `POST /api/v1/bedbathbeyond/questions` | Customer questions and answers, 20 per page; no screen names | 1 |
| `POST /api/v1/bedbathbeyond/stores` | The 333 stores of the Bed Bath & Beyond family near a ZIP or a point, in a state, by banner, with hours and services | 1 |
| `POST /api/v1/bedbathbeyond/deals` | The deals page (countdown and product grids, 1 credit) or one deal list (2 credits) | 1 or 2 |

Every answer carries `market` (us), `host`, `language` (en-US) and `currency` (USD).

## Prices and stock

List items (`items[]`, `sponsored_items[]`) carry `price`, `price_max` (a range across options), `price_text` (when the site hides the price), `price_type` (`sale`, `standard`), `base_price`, `compare_price`, `compare_type` (`msrp`, `was`, `compare_at`), `discount_percent`, `discount_amount`, `on_sale`, `sale_ends` (as given), `promo` (the badge, `30% Off Code CYBER30`), `label` (`Best Seller`, `High Satisfaction`, `Top Rated`), `rating`, `review_count`, `option_count`, `fast_delivery`, `club_o_rewards` (the Club O Rewards amount shown) and `sponsored`.

The product carries `price` with `price_label` (`Sale Starts at`), `compare_price` with `compare_label` (`MSRP`, `Was`), `savings`, `savings_percent`, `price_min`, `price_max`, and `options[]` {`option_id`, `description`, `attributes` {`Color`, `Size`}, `price`, `compare_price`, `compare_type`, `savings`, `savings_percent`, `on_sale`, `sale_start`, `sale_end`, `qty_on_hand` (exact online stock), `max_quantity`, `in_stock`, `backorder`, `sub_sku`}.

- Quote "Superior Egyptian Cotton 6 Piece Towel Set, Ash Grey 6-Piece Set: $74.25 at bedbathandbeyond.com on 2026-11-27 (was $93.99, sale ends 2026-12-07)", with the option and date.
- A compare price is the site's own (MSRP, was or compare at); say which type it is.
- Report the site's prices, compare prices, badges and counts as given and the arithmetic only. Never subtract a promo code, never judge a price as a good deal and never describe how often an option is in stock.

## Workflow

1. **Find the product.** `/search` with `query` (`bath towels`); or `/categories` then `/category` with a link's `slug` and `category_id` (or its `url`). Each item's `product_id` is the input of product, reviews and questions. If the answer has `redirected_to` {`type` category}, the keyword opened that category; {`type` product} means one product page.
2. **Narrow a list.** On search, send back a `facets[].values[].url` as `facet_url` (a color, a brand, On Sale). On category, use `attributes` (facet id to value ids, `{"2415": ["2913"]}`), `price_min` + `price_max`, `rating`, `brand`, `promotion`, `fast_delivery`, `expedited`.
3. **Options and stock.** `/product` with `product_id` or `url`: read `options[]` for each option's price, sale window and `qty_on_hand`.
4. **Delivery.** `/delivery-estimate` with an `option_id` from `options[]`, `zip` and `quantity`.
5. **Reviews and questions.** `/reviews` with `product_id`, `sort`, `rating`, `search`, `page`, `page_size`; `/questions` with `product_id` and `page`.
6. **Deals.** `/deals` without `type` for the deals page (countdown, Doorbusters grid and `deal_lists`), or with `type` `black_friday`, `on_sale`, `doorbusters` or `holiday_brand_deals` for a full sortable list.
7. **Watching prices or stock:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of the two | Keywords, 1-150 chars |
| `facet_url` | string | one of the two | A `facets[].values[].url` from a search answer (a filtered keyword list); price filter links are refused |
| `sort` | string | `best_match` | `best_match`, `on_sale`, `best_selling`, `price_asc`, `price_desc`, `rating`, `newest` |
| `include_out_of_stock` | boolean | false | Also list out-of-stock products |
| `page` | integer | 1 | 1-84 |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `slug` + `category_id` | string | one of the two | The path after /c/ (`bedding/bedding-sets`) and the category id (`276`), from `/categories`, breadcrumbs or child categories |
| `url` | string | one of the two | A bedbathandbeyond.com `/c/` link instead; its filters are kept |
| `sort` | string | `best_selling` | `best_selling`, `on_sale`, `price_asc`, `price_desc`, `rating`, `newest` (the site's own keys are accepted too) |
| `page` | integer | 1 | 1-84 |
| `attributes` | object | none | Up to 8 facets: facet id to 1-10 value ids (`facets[].id`, `facets[].values[].id`) |
| `price_min`, `price_max` | number | none | Price range in USD, sent together |
| `rating` | integer | none | 1-4: this many stars and up |
| `brand`, `promotion` | string or array | none | Up to 10 names as the Brand and Sales and Promotions facets list them (`on sale`, `top rated`, `best selling`, `new products`) |
| `fast_delivery`, `expedited`, `include_out_of_stock` | boolean | false | Fast Delivery only, Expedited Shipping Available only, include out-of-stock |

### Categories (`/categories`)

No parameters: the whole menu.

### Product (`/product`), reviews (`/reviews`), questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` or `url` | string | required (one) | The digits before /product.html (`5296998`), or a bedbathandbeyond.com product link |
| `sort` | string | `newest` | Reviews: `newest`, `most_helpful`, `highest`, `lowest` |
| `rating` | integer | none | Reviews: exactly this many stars (1-5) |
| `search` | string | none | Reviews containing this text |
| `page` | integer | 1 | Reviews and questions (20 per page) |
| `page_size` | integer | 10 | Reviews per page, 1-50 |

### Delivery estimate (`/delivery-estimate`)

`option_id` (required, `options[].option_id`, `94445783`), `zip` (required, a US ZIP), `quantity` (1-99, default 1).

### Stores (`/stores`)

One of `zip` (placed at its Census center), `state` (2-letter code: every store in the state) or `latitude` + `longitude`; `radius` 1-500 miles (default 50) with zip or a point; `banner` `bed_bath_beyond` (the co-branded Bed Bath & Beyond / The Container Store stores), `kirklands` or `container_store` (every store carrying The Container Store). Without a place: all 333.

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `page` | `page` (the deals page, 1 credit), or a list: `black_friday`, `on_sale`, `doorbusters`, `holiday_brand_deals` (2 credits) |
| `sort` | string | the list's order | Lists only: as search |
| `page` | integer | 1 | Lists only: 1-84 |
| `include_out_of_stock` | boolean | false | Lists only |

## Examples

### Product with every option

```bash
curl -X POST https://api.scavio.dev/api/v1/bedbathbeyond/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "5296998"}'
```

Captured `data` (2026-11-27; breadcrumbs, specs, images, notes and 24 of 26 options dropped):

```json
{
  "requested_id": "5296998",
  "product_id": "5296998",
  "name": "Superior Egyptian Cotton 6 Piece Towel Set Ultra Plush & Absorbent Bath, Hand & Face Towels, Heavyweight Spa Quality",
  "brand": "Superior",
  "brand_id": "31912",
  "mpn": "Madeline 6 PC TOWEL SET",
  "sku": "13108204",
  "url": "https://www.bedbathandbeyond.com/Bedding-Bath/Superior-Egyptian-Cotton-900-GSM-Luxurious-Absorbent-6-piece-Towel-Set/5296998/product.html",
  "in_stock": true,
  "online": true,
  "discontinued": false,
  "price": 63.98,
  "price_label": "Sale Starts at",
  "compare_price": 157.5,
  "compare_label": "MSRP",
  "savings": 93.52,
  "savings_percent": 59,
  "price_min": 63.98,
  "price_max": 74.25,
  "on_sale": true,
  "rating": 4.5,
  "review_count": 5165,
  "rating_histogram": { "1": 241, "2": 157, "3": 244, "4": 681, "5": 3842 },
  "free_shipping": true,
  "freight": false,
  "country_of_origin": "India",
  "first_onsite_date": "2010-10-12",
  "label": "Best Seller",
  "taxonomy": { "store": "Bedding", "department": "Bath Linens", "category": "Towels", "subcategory": "Bath Towels" },
  "option_count": 26,
  "original_option_count": 49,
  "options": [
    {
      "option_id": "94445783",
      "description": "6-Piece Set - Ash Grey",
      "attributes": { "Color": "Ash Grey", "Size": "6-Piece Set" },
      "price": 74.25,
      "compare_price": 93.99,
      "compare_type": "was",
      "savings": 19.74,
      "savings_percent": 21,
      "on_sale": true,
      "sale_start": "2026-11-25T22:00-07:00",
      "sale_end": "2026-12-07T01:00-07:00",
      "qty_on_hand": 97,
      "max_quantity": 20,
      "in_stock": true,
      "backorder": false,
      "sub_sku": "000-048"
    },
    {
      "option_id": "7240384",
      "description": "6-Piece Set - Black",
      "attributes": { "Color": "Black", "Size": "6-Piece Set" },
      "price": 68.84,
      "compare_price": 164.5,
      "compare_type": "msrp",
      "savings": 95.66,
      "savings_percent": 58,
      "on_sale": true,
      "sale_start": "2026-11-25T22:00-07:00",
      "sale_end": "2026-12-07T01:00-07:00",
      "qty_on_hand": 1423,
      "max_quantity": 20,
      "in_stock": true,
      "backorder": false,
      "sub_sku": "000-000"
    }
  ]
}
```

The two options carry different compare types (was and MSRP): quote each with its own. `notes` said "26 of 49 options are listed: the site leaves out-of-stock options out." An unknown product is a charged `404`: "Bed Bath & Beyond has no product <id>."

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/bedbathbeyond/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "bath towels"}'
```

Captured `data.items[0]` (2026-11-27; `total` 7,835, 84 pages, `count` 48, `sponsored_count` 17; url dropped):

```json
{
  "position": 1,
  "product_id": "5296998",
  "name": "Superior Egyptian Cotton 6 Piece Towel Set Ultra Plush & Absorbent Bath, Hand & Face Towels, Heavyweight Spa Quality",
  "price": 63.98,
  "price_max": 74.25,
  "price_text": null,
  "price_type": "sale",
  "base_price": 80.99,
  "compare_price": 157.5,
  "compare_type": "msrp",
  "discount_percent": 59,
  "discount_amount": 93.52,
  "on_sale": true,
  "sale_ends": "05-Oct-2027 16:35:00",
  "promo": "30% Off Code CYBER30",
  "label": "Best Seller",
  "rating": 4.52,
  "review_count": 3737,
  "option_count": 26,
  "fast_delivery": false,
  "club_o_rewards": 3.2,
  "sponsored": false
}
```

`promo` is the badge with a code; the price is not reduced by it. `sale_ends` 2027 is the site's value as given. The second result was the Authentic Hotel and Spa Turkish Cotton Bath Towels (Set of 4) at $58.82, MSRP $141.99. `{"query": "table lamp", "sort": "price_asc"}` read 12,501 results with `matching_categories` (Lighting 11,478, Home Improvement 1,918, ...). A search with no results is a charged `404`: "Bed Bath & Beyond found nothing for this search."

### Category, menu, delivery, reviews, questions, stores, deals

- `/category` `{"slug": "bedding/bedding-sets", "category_id": "276", "sort": "price_asc"}`: Bedding Sets, `total` 4,548, 76 pages of 81; first a 3 Piece Solid Duvet Cover & Sham Covers Set at $16.71 to $29.69 (`price_type` sale, `base_price` 22.89); `child_categories` Comforters and Sets (2,647), Duvet Covers and Sets (1,678), ...; 15 facets (Delivery, Expedited Shipping, ...). An unknown category is a charged `404`: "Bed Bath & Beyond has no category <id> at <slug>."
- `/categories` `{}`: 13 departments and 541 links (Furniture > Living Room Furniture > Sofas & Couches `24464`; Rugs > Rugs By Size > 3' x 5', `filtered` true).
- `/delivery-estimate` `{"option_id": "94445783", "zip": "10001"}`: `in_stock` true, `can_ship` true, `ship_charge_total` 0, `ground_days` 3, `two_day` true, options [{`level` GROUND, `name` Standard, `charge_text` FREE, `estimated_date` 2026-11-30, `estimate_text` "Mon, Nov. 30"}]. An unknown option is a charged `404`: "Bed Bath & Beyond has no product option <id>."
- `/reviews` `{"product_id": "5296998", "sort": "most_helpful"}`: `total` 5,165, 517 pages, `average_rating` 4.5, `media_count` 57, the histogram; each review with `rating`, `title` ("fell apart upon washing"), `text`, `submitted_at`, `helpful_votes` (133), `verified_purchase`, `rewards_received`, `recommended`, `locale` and `media`. No reviewer names or locations.
- `/questions` `{"product_id": "10216253"}`: 159 questions, 693 answers, 8 pages of 20; each with `text`, `asked_at`, `answer_count` and `answers`. No screen names.
- `/stores` `{"zip": "75201"}`: `total_stores` 333, 16 within 50 miles of Dallas; first Bed Bath & Beyond / The Container Store - Dallas Northwest Hwy (5.5 miles, `brands` Bed Bath & Beyond and The Container Store, hours Monday-Thursday 10am-8pm, Sunday 11am-6pm). Store phone numbers are public business contact data. No store stock or store prices exist.
- `/deals` `{}`: `event` {`text` "Black Friday Sale ends in", `ends_at` 2026-11-30T05:00:00.000Z}, the DOORBUSTERS section (12 items: a KYVOS Mallory modular sectional at $131.47 against an MSRP of $259, 206 on hand; a Beautyrest Black Luxury Foam Pillow at $79.29 against a was price of $121.99) and `deal_lists`. `{"type": "doorbusters"}` (2 credits): `total` 1,133, 19 pages, 54 organic items and 16 sponsored tiles; a Shark Navigator Lift Away Deluxe Upright Vacuum at $124.99 (`base_price` 201.49, `sale_ends` 03-Dec-2026 05:00:00).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bbb(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bedbathbeyond/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Search, organic results only (2 credits)
hits = bbb("search", {"query": "bath towels"})["data"]
first = hits["items"][0]
print(first["name"], first["price"], first["compare_type"], first["compare_price"], first["promo"])

# 2. Every in-stock option with its price and online stock (1 credit)
p = bbb("product", {"product_id": first["product_id"]})["data"]
print(p["option_count"], "of", p["original_option_count"], "options in stock")
for o in p["options"]:
    print(o["description"], o["price"], o["compare_type"], o["compare_price"], o["qty_on_hand"], o["sale_end"])

# 3. Delivery date of the first option to a ZIP (1 credit)
eta = bbb("delivery-estimate", {"option_id": p["options"][0]["option_id"], "zip": "10001"})["data"]
print([(x["name"], x["charge_text"], x["estimate_text"]) for x in eta["options"]])

# Prices and stock change: store each answer with fetched_at and run this on a
# schedule; that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `market`, `host`, `language`, `currency` and `notes`.

- **search / category / deal lists** - `query`, `sort`, `include_out_of_stock` (search); `category` {`id`, `slug`, `name`, `url`}, `requested_filters`, `selected_facets[]` {`group`, `name`, `id`, `remove_url`}, `breadcrumbs`, `child_categories[]` {`id`, `name`, `count`, `slug`, `url`} (category); `type`, `name` (deal lists); then `total`, `page`, `total_pages`, `has_more`, `sort_applied`, `count`, `items[]` and `sponsored_items[]` (as above, with `position`, `product_id`, `name`, `url`, `image`), `sponsored_count`, `facets[]` {`id`, `name`, `multi_select`, `values[]` {`name`, `id`, `count`, `selected`, `url`}}, `related_searches`, `matching_categories` and `redirected_to` (search).
- **categories** - `count`, `link_count`, `departments[]` {`name`, `url`, `category_id`, `slug`, `filtered`, `groups[]` {`name`, `url`, `category_id`, `slug`, `filtered`, `links[]` {`name`, `url`, `category_id`, `slug`, `filtered`}}}.
- **product** - `requested_id`, `product_id`, `name`, `brand`, `brand_id`, `mpn`, `sku`, `sold_by`, `url`, `in_stock`, `online`, `discontinued`, `status_code`, `price`, `price_label`, `compare_price`, `compare_label`, `savings`, `savings_percent`, `price_min`, `price_max`, `on_sale`, `rating`, `review_count`, `rating_histogram`, `free_shipping`, `freight`, `international_shippable`, `country_of_origin`, `first_onsite_date`, `label`, `breadcrumbs`, `taxonomy`, `specs[]` {`group`, `name`, `values`}, `images`, `option_count`, `original_option_count`, `options[]` (as above, plus `image`).
- **delivery-estimate** - `requested_option_id`, `requested_quantity`, `product_id`, `option_id`, `zip`, `quantity`, `in_stock`, `can_ship`, `ship_charge_total`, `ground_days`, `one_day`, `two_day`, `holiday`, `pre_release`, `options[]` {`level`, `name`, `charge`, `charge_text`, `estimated_date`, `estimate_type`, `estimate_text`, `freight`}, `errors[]` {`type`, `message`}.
- **reviews** - `product_id`, `sort`, `rating_filter`, `search`, `page`, `page_size`, `total_pages`, `total`, `total_matching`, `average_rating`, `rating_count`, `media_count`, `rating_histogram`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `helpful_votes`, `unhelpful_votes`, `verified_purchase`, `rewards_received`, `recommended`, `locale`, `variation_id`, `media[]` {`type`, `url`, `thumbnail`}}.
- **questions** - `product_id`, `page`, `page_size`, `total_pages`, `total_questions`, `total_answers`, `has_more`, `count`, `questions[]` {`question_id`, `text`, `asked_at`, `type`, `answer_count`, `answers[]` {`answer_id`, `text`, `answered_at`}}.
- **stores** - `zip`, `state`, `latitude`, `longitude`, `radius_miles`, `banner`, `total_stores`, `count`, `stores[]` {`name`, `banner`, `brands`, `address` {`street`, `city`, `state`, `zip`, `full`}, `phone`, `latitude`, `longitude`, `time_zone`, `hours` {`monday_thursday`, `friday`, `saturday`, `sunday`}, `services`, `service_callout`, `distance_miles`}.
- **deals (page)** - `type`, `event` {`text`, `ends_at`}, `count`, `sections[]` {`name`, `items[]` {`position`, `product_id`, `option_id`, `name`, `url`, `image`, `price`, `compare_price`, `compare_type`, `savings`, `savings_percent`, `on_sale`, `sale_end`, `qty_on_hand`, `option_count`, `rating`, `review_count`}}, `deal_lists[]` {`type`, `name`}.

## Guardrails

- Name it "Bed Bath & Beyond (bedbathandbeyond.com, the US online home goods store)" on first mention.
- Prices: quote the option, `price`, the compare price with its type (MSRP, was, compare at) and the `fetched_at` date. Never compute a price after a promo code, and never call a compare price a former selling price unless its type is `was`.
- Sale windows: quote `sale_end` and `sale_ends` as the site's values; some look like placeholders.
- Stock: `qty_on_hand` is online stock at the time of the call. Never describe it as store stock, and never promise a unit will still be there.
- Sponsored tiles: keep `sponsored_items` apart from organic results; never rank them as search results.
- Reviews and questions: no reviewer or asker names are returned. Quote a review as "a Bed Bath & Beyond customer review".
- Not available: store stock, store prices, UPCs or GTINs, results past page 84, price history (poll and store), carts or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Bed Bath & Beyond data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Bed Bath & Beyond's terms of use restrict automated access or commercial use of its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, quantities, product or option ids, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "send one of query (keywords) or facet_url (a facets[].values[].url from a search answer)."; "price filter links are not accepted: the site drops prices from their tiles. Use category with price_min and price_max."; "send slug and category_id (categories[].slug / category_id, e.g. bedding/bedding-sets and 276), or a category url."; "send price_min and price_max together (USD)."; "attributes takes at most 8 facets."; "send one of product_id (digits, e.g. 5296998) or url (a bedbathandbeyond.com product link)."; "option_id must be product's options[].option_id (digits, e.g. 94445783)."; "zip must be a 5-digit US ZIP code, e.g. 10001."; "send one of zip, state, or latitude and longitude."; "state must be a 2-letter US state code, e.g. TX."; "sort, page and include_out_of_stock go with a deal list type (black_friday, on_sale, doorbusters, holiday_brand_deals), not with type page."; a `sort`, `page`, `rating` or `page_size` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Bed Bath & Beyond found nothing for this search.", "Bed Bath & Beyond has no category <id> at <slug>.", "Bed Bath & Beyond has no product <id>.", "Bed Bath & Beyond has no product option <id>.", "Bed Bath & Beyond has no reviews for product <id>.", "Bed Bath & Beyond has no product <id> (or no questions for it).", "Bed Bath & Beyond shows no <list> list right now.". Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api).
- `502` means Bed Bath & Beyond data was temporarily unavailable ("Bed Bath & Beyond is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.101.0
npm install scavio@0.102.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.bedbathbeyond.search({ query: "bath towels", sort: "best_selling" });
const { data: list } = await scavio.bedbathbeyond.category({ slug: "bedding/bedding-sets", category_id: "276", price_min: 20, price_max: 60 });
const { data: menu } = await scavio.bedbathbeyond.categories({});
const { data: towels } = await scavio.bedbathbeyond.product({ product_id: "5296998" });
const { data: eta } = await scavio.bedbathbeyond.deliveryEstimate({ option_id: "94445783", zip: "10001", quantity: 2 });
const { data: reviews } = await scavio.bedbathbeyond.reviews({ product_id: "5296998", sort: "lowest" });
const { data: qa } = await scavio.bedbathbeyond.questions({ product_id: "10216253" });
const { data: near } = await scavio.bedbathbeyond.stores({ zip: "75201", banner: "kirklands" });
const { data: deals } = await scavio.bedbathbeyond.deals({ type: "doorbusters", sort: "price_asc" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.bedbathbeyond.search(...)`, `category`, `categories`, `product`, `delivery_estimate`, `reviews`, `questions`, `stores` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_bedbathbeyond`, `get_bedbathbeyond_category`, `get_bedbathbeyond_categories`, `get_bedbathbeyond_product`, `get_bedbathbeyond_delivery_estimate`, `get_bedbathbeyond_reviews`, `get_bedbathbeyond_questions`, `get_bedbathbeyond_stores` and `get_bedbathbeyond_deals`. Bed Bath & Beyond is opt-in: add `bedbathbeyond` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.101.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bedbathbeyond"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bedbathbeyond-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [category](https://scavio.dev/docs/bedbathbeyond-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [categories](https://scavio.dev/docs/bedbathbeyond-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [product](https://scavio.dev/docs/bedbathbeyond-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [delivery estimate](https://scavio.dev/docs/bedbathbeyond-delivery-estimate?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [reviews](https://scavio.dev/docs/bedbathbeyond-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [questions](https://scavio.dev/docs/bedbathbeyond-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [stores](https://scavio.dev/docs/bedbathbeyond-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api), [deals](https://scavio.dev/docs/bedbathbeyond-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api). Overview: [Bed Bath & Beyond API](https://scavio.dev/bedbathbeyond-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=bed-bath-and-beyond-api).
