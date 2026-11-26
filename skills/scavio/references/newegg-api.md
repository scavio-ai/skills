# Newegg API - PC Part Prices, Seller Offers, Reviews, Deals

Read Newegg (newegg.com, the US computer and electronics store; newegg.ca in Canada and the Newegg Global storefronts): keyword search, category listings, one item in full with Newegg's price, struck-through list price, instant rebate, lowest price in 30 days, promo code and stock, every seller's offer on an item, reviews, Shell Shocker and Black Friday deals, a marketplace seller's store and its items, the department tree and search-box suggestions. www.newegg.com (USD) for all 10 endpoints, www.newegg.ca (CAD) for 9, and the Newegg Global storefronts (uk, au, nz, jp, ph, sg, kr, th, mx; local currency, English) for search, category, product and reviews. Every endpoint returns structured JSON at 2 credits per call.

**The job this skill is for: Newegg prices on PC parts, and who else sells the same item.** What a CPU, graphics card, SSD or laptop costs on newegg.com today, how Newegg builds that price, and which marketplace sellers offer it for less or more. On 2026-11-26 the AMD Ryzen 7 9800X3D (item `19-113-877`, UPC 730143315289) read `price` $439.99 = `list_price` $506.99 - `instant_rebate` $67, with Newegg's own `lowest_price_30_days` $369.99, a "Black Friday Deal" badge ending 2026-11-28, `stock` 1 and `quantity_limit` 1, and a separate promo "+ $70 off w/ promo code BFF36" (`promo.code_discount` 70) that applies at checkout and is never taken off `price`. `/offers` on the same item listed 28 offers on 2 pages (26 new from $418.99, 2 used from $449.99); the lowest new one, $418.99, was the marketplace seller PlatinumMicro (4.5 stars from 7,249 seller reviews, Top Rated, 4 days delivery), with Newegg's own unit second at $439.99. On newegg.ca the same item read $549.99 CAD (list $799.99, rebate $250). Pair it with `amazon-product-data`, `best-buy-product-data`, `micro-center-api` and `walmart-product-data` for the same part (match on UPC or MPN).

Nine limits shape every answer, so say them plainly:
- **2 credits per call.** Every endpoint is 2 credits. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **`price` is after the instant rebate, never after a promo code.** `list_price` is the price Newegg shows struck through, `instant_rebate` the amount taken off, `price` what is left ($506.99 - $67 = $439.99). A promo code (`promo.code`, `promo.code_discount`) applies at checkout: report it apart and never subtract it from `price`.
- **The 30-day low is Newegg's own.** `lowest_price_30_days` and `is_lowest_price_30_days` are Newegg's figures as given. Quote them as Newegg's; Scavio does not keep a price series.
- **Buy-box swap: the requested item and the served item can differ.** When Newegg's own unit of an item is unavailable, the product page serves a marketplace offer instead: the answer then has `buy_box_changed` `true`, `requested_item` (what you asked for) and `served_item` (the marketplace item number, starting `9SI`), and every price, stock and seller field describes `served_item`. A note says so. Always check `buy_box_changed` before quoting a product price as Newegg's.
- **Marketplace sellers are labelled.** `seller.name` is "Newegg" on items Newegg sells; marketplace items (item numbers starting `9SI`) carry the seller's store name, `url_key` and `marketplace` `true`. `shipped_by_newegg` says who ships. `/offers` lists every seller's offer on one item, Newegg's own included.
- **Storefronts and currencies.** `country` `us` (default, USD), `ca` (CAD) or a Newegg Global storefront: `uk` GBP, `au` AUD, `nz` NZD, `jp` JPY, `ph` PHP, `sg` SGD, `kr` KRW, `th` THB, `mx` MXN. The Global storefronts carry part of Newegg's catalog in English, with international shipping in `shipping.charge` (the GIGABYTE WindForce RTX 5070, `14-932-777`, read £791.53 plus £50.54 shipping on uk, $899.99 on us and $1,249.99 CAD on ca). Report each in its own currency; never convert or call one storefront cheaper.
- **Category and seller ids are per storefront.** The GPU category is `100007709` on us, `100007708` on ca and `101582767` on uk; the seller TECH-EDGE is `1066805289` on us and `1066805290` on ca. Take ids from an answer of the same storefront: another storefront's id answers no items.
- **Reviews need two ids from the product.** `/reviews` takes `group_id` and `subcategory_id` from `review_params` of a product or search answer. Reviews are one pool across Newegg's storefronts and across an item's variants.
- **No history, no live checkout price.** The price is the product page's price at the moment of the call; Scavio runs no cart or checkout price check and keeps nothing. Poll and store your own series.

Newegg has no public API for reading its catalog, prices or offers: developer.newegg.com is the Marketplace seller API (item, price and inventory feeds that need seller credentials), and the affiliate programme runs through a third-party affiliate network (links, not a price API). Prices and offers are shown on newegg.com, newegg.ca and the Global storefronts, and this skill reads those public pages with one Scavio key.

Newegg Commerce, Inc. (NASDAQ: NEGG) reported net sales of $1.444B for fiscal 2025 in its Form 20-F filed 2026-04-28; it sells online only (newegg.com, newegg.ca, the Newegg Global storefronts, Newegg Business). Quote these with their source, never from the samples.

See also: for the same part at Amazon use `amazon-product-data`; at Best Buy `best-buy-product-data`; at Micro Center `micro-center-api`; at Walmart `walmart-product-data`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Price a CPU, graphics card, SSD, RAM kit, motherboard, monitor or laptop on Newegg, with the struck-through list price, the instant rebate and Newegg's lowest price in 30 days
- See every seller's offer on one Newegg item, new or used, with seller ratings, shipping and delivery days, and the lowest offer per condition
- Check whether Newegg itself sells an item or a marketplace seller does, and whether the product page swapped to a marketplace offer
- Search Newegg by keyword, sorted by price, best selling, rating or most reviews, or filtered by sold by Newegg, in stock, new, used, recertified, open box, lowest price in 30 days, 40 percent off, a brand or a spec
- List a Newegg category (GPUs, desktop CPUs, gaming laptops) or the department tree
- Read today's Shell Shocker deals with the countdown end, or the Black Friday store, for all categories or one
- Read Newegg reviews (25 per page, by stars, verified owners only, newest or most helpful) with pros and cons
- Read a marketplace seller's store rating, positive percent, about text and return policy, and list the items that seller sells
- Compare one item on newegg.com, newegg.ca and a Newegg Global storefront, each in its own currency
- Get Newegg's search-box suggestions for a partial query

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits, so 50 credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, offers, reviews, seller and suggestions took 1-4 seconds, search, category and deals 1-5, a product 2-12 and up to 43 on one US item. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/newegg/search` | Keywords: 36 to 60 items per page with total, list price, price, instant rebate, 30-day low, promo, badges, seller, stock, facets and this storefront's category ids | us, ca, Global | 2 |
| `POST /api/v1/newegg/category` | One category's items (category id), with keywords, filters and sorts as search, the category's spec facets and breadcrumbs | us, ca, Global | 2 |
| `POST /api/v1/newegg/categories` | The newegg.com department tree with category ids (17 departments, 1,055 categories captured) | us | 2 |
| `POST /api/v1/newegg/product` | One item by item number: prices, rebate, 30-day low, promo code and expiry, badges, stock and quantity limit, seller, UPC, MPN, specs, warranty, variants, review summary, the reviews and questions on the page, requested vs served item | us, ca, Global | 2 |
| `POST /api/v1/newegg/offers` | Every seller's offer on one item, by condition, with offer counts and the lowest price per condition, seller ratings and delivery days | us, ca | 2 |
| `POST /api/v1/newegg/reviews` | Reviews of one item, 25 per page, with stars, pros, cons, verified-owner marks and manufacturer replies; no reviewer names | us, ca, Global | 2 |
| `POST /api/v1/newegg/deals` | Shell Shocker (daily deals, with the countdown end) or the Black Friday store, optionally one category | us, ca | 2 |
| `POST /api/v1/newegg/seller` | A marketplace seller's store: name, seller id, rating, review count, positive percent, about text, return policy | us, ca | 2 |
| `POST /api/v1/newegg/seller-products` | The items one marketplace seller lists, with keywords, filters and sorts as search | us, ca | 2 |
| `POST /api/v1/newegg/suggestions` | Search-box keyword suggestions and the products shown for what has been typed | us, ca | 2 |

`country` is `us` (default, www.newegg.com, USD), `ca` (www.newegg.ca, CAD) or a Newegg Global storefront (`uk`, `au`, `nz`, `jp`, `ph`, `sg`, `kr`, `th`, `mx`). An endpoint asked for a market it does not serve is a `400`, not charged: "offers is served on country us, ca (the Newegg Global storefronts have no other-sellers list); uk is not one of them."

## Prices: list price, instant rebate, 30-day low, promo codes

Every priced item carries:

| Field | Meaning |
|---|---|
| `list_price` | The price Newegg shows struck through |
| `instant_rebate` | The amount Newegg takes off `list_price` |
| `price` | The price shown after `instant_rebate` ($506.99 - $67 = $439.99 on `19-113-877`) |
| `original_price` | Product: Newegg's original unit price as given ($479 on `19-113-877`) |
| `lowest_price_30_days`, `is_lowest_price_30_days` | Newegg's own lowest price in 30 days and its own flag, as given |
| `black_friday_save_percent` | Product: the save percent Newegg shows on a Black Friday item (27 on `19-113-877`) |
| `promo` {`text`, `code`, `code_discount`} | Newegg's promo text and code ("+ $70 off w/ promo code BFF36", `BFF36`, 70); applies at checkout, never taken off `price` |
| `promo_expires_at` | Product: the promo's expiry as Newegg gives it (2026-11-28T23:59:59-08:00) |
| `badges` | Lists: badge titles ("Black Friday Deal"); product: [{`title`, `starts_at`, `ends_at`}] |
| `shipping` {`charge`, `free`} | `free` is `true` where Newegg marks free shipping, `null` where a listing states a 0 charge without that mark; Global storefronts put international shipping in `charge` |
| `currency` | The storefront's currency (USD, CAD, GBP, AUD, NZD, JPY, PHP, SGD, KRW, THB, MXN) |

- **Quote the arithmetic.** "$439.99 at newegg.com on 2026-11-26 ($506.99 struck through, $67 instant rebate)". A promo code goes on its own line: "a further $70 with code BFF36 at checkout, as Newegg states it, until 2026-11-28". Never compute or quote an after-code price as Newegg's price.
- **Combos.** A listing cell can be a combo (`type` `combo`) with `combo_id`, `list_price`, `combo_discount`, `price` and its `items`; report the combo price as a combo, not as one item's price.
- Report Newegg's labels and figures only. Never judge a list price, a rebate, a 30-day low or a deal deadline, and never describe how often an item is on sale.

## Workflow

1. **Find the item.** `/search` with `query` (`rtx 5070`, `ryzen 7 9800x3d`), or `/category` with a `category_id` from `/categories` (us) or from a listing's `categories[]` and `breadcrumbs[]` (every storefront). Each item's `item_number` is the input of product and offers, and its `review_params` the input of reviews.
2. **Read it in full.** `/product` with `item_number` (`19-113-877`, `N82E16819113877`, a marketplace `9SI...` number, or an other-form number such as `2WC-000C-0JJ10`; an `R` suffix is an open-box unit). Check `buy_box_changed`: when `true`, `served_item` is a marketplace offer and every price describes it.
3. **Every seller.** `/offers` with `item_number` (us, ca): `tabs` give each condition's offer count and lowest price on page 1 in price order; `offers[]` give each seller's price, shipping, condition, seller rating and delivery days. `condition` `new` or `used` narrows it; `page_size` up to 20.
4. **One seller.** `/seller` with the store key (`items[].seller.url_key` or `offers[].seller.url_key`, such as `TECH-EDGE`) gives the store rating and `seller_id`; `/seller-products` with that `seller_id` lists its items. The `seller_id` differs per storefront: call `/seller` on the same `country`.
5. **Reviews.** `/reviews` with `item_number`, `group_id` and `subcategory_id` (from `review_params`), then `sort`, `rating`, `verified_only` and `page` (25 per page).
6. **Deals.** `/deals` with `type` `shell_shocker` (default) or `black_friday`, optionally `category_id` from the answer's `categories[]`. `ends_at` is the Shell Shocker countdown end for the whole event; a single deal's end is on the product (`promo_expires_at`, `badges[].ends_at`).
7. **Narrow a list.** `sort` and `filters` (named filters or facet ids from `facets[].options[].id`, up to 10), `page` (1-100). A page past the last answers no items.
8. **Other storefronts.** Send `country` on search, category, product and reviews for the Global storefronts; ca also serves offers, deals, seller, seller-products and suggestions.
9. **Watching prices:** there is no history. Poll the same items on a schedule and store each answer with its `fetched_at` and storefront; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), seller products (`/seller-products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords, 1-200 chars. Category and seller-products: keywords within the list |
| `category_id` | string | category: required | A category id of this storefront (digits, `100007709`): `categories[].category_id` of categories (us) or of a listing, `breadcrumbs[].category_id`, or a category link's `N=` |
| `seller_id` | string | seller-products: required | The seller's listing id (digits, `1066805289`): `seller_id` of the seller answer |
| `filters` | array | none | Up to 10: `sold_by_newegg`, `in_stock`, `new`, `recertified`, `used`, `open_box`, `lowest_price_30_days`, `40_percent_off`, or a facet id from `facets[].options[].id` (brands, specs, price bands) |
| `sort` | string | `featured` | `featured` (the site's order), `price_asc`, `price_desc`, `best_selling`, `top_rated`, `most_reviews` |
| `page` | integer | 1 | 1-100; 36 to 60 items per page as the site lists them |
| `country` | string | `us` | Search and category: `us`, `ca` or a Global storefront; seller-products: `us` or `ca` |

### Product (`/product`) and offers (`/offers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string | required | `N82E16819113877` or `19-113-877` (Newegg's own; `R` suffix = open box), `9SIA2W0KDW5195` (a marketplace item) or `0D9-000E-00346` (other product numbers in `items[].item_number`) |
| `country` | string | `us` | Product: `us`, `ca` or a Global storefront; offers: `us` or `ca` |
| `condition` | string | `all` | Offers: `all`, `new` or `used` |
| `sort` | string | `price` | Offers: `price` (low to high) or `seller_rating` |
| `page` | integer | 1 | Offers: 1-50 |
| `page_size` | integer | 20 | Offers per page, 1-20 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_number` | string | required | The item number |
| `group_id` | integer | required | `review_params.group_id` of the product or search answer (196668433 on `19-113-877`) |
| `subcategory_id` | integer | required | `review_params.subcategory_id` (343 on `19-113-877`) |
| `sort` | string | `most_helpful` | `most_helpful`, `newest`, `highest_rated`, `lowest_rated` |
| `rating` | integer | none | Only reviews with this many stars (1-5) |
| `verified_only` | boolean | false | Verified owners' reviews only |
| `page` | integer | 1 | 1-400, 25 reviews per page |
| `country` | string | `us` | Any storefront; the pool is shared |

### Deals (`/deals`), seller (`/seller`), categories (`/categories`), suggestions (`/suggestions`)

`/deals` takes `type` (`shell_shocker` default, or `black_friday`), an optional `category_id`, `page` and `country` (`us` or `ca`). `/seller` takes `seller` (required, the store key such as `TECH-EDGE`: `items[].seller.url_key`, or the part after /Seller-Store/ in a store link) and `country` (`us` or `ca`). `/categories` takes `country` `us` only. `/suggestions` takes `query` (1-100 chars, what has been typed) and `country` (`us` or `ca`).

## Examples

### One item with its rebate, 30-day low, promo code and stock

```bash
curl -X POST https://api.scavio.dev/api/v1/newegg/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "N82E16819113877"}'
```

Captured `data` (2026-11-26; `bullets`, `specs`, `warranty`, `images`, `variants`, `combo_builder`, `package_options`, `breadcrumbs`, `reviews` and `questions` dropped, `notes` cut to 2 of 4):

```json
{
  "country": "us",
  "storefront": "www.newegg.com",
  "currency": "USD",
  "item_number": "19-113-877",
  "buy_box_changed": false,
  "requested_item": "19-113-877",
  "served_item": "19-113-877",
  "parent_item": null,
  "title": "AMD Ryzen 7 9800X3D - Ryzen 7 9000 Series Zen 5 8-Core 5.2 GHz - Socket AM5 120W - AMD Radeon Graphics Desktop Processor - 100-100001084WOF",
  "brand": "AMD",
  "model": "100-100001084WOF",
  "mpn": "100-100001084WOF",
  "upc": "730143315289",
  "url": "https://www.newegg.com/p/N82E16819113877",
  "list_price": 506.99,
  "original_price": 479,
  "price": 439.99,
  "instant_rebate": 67,
  "lowest_price_30_days": 369.99,
  "is_lowest_price_30_days": true,
  "black_friday_save_percent": 27,
  "promo": { "text": "+ $70 off w/ promo code BFF36, limited offer", "code": "BFF36", "code_discount": 70 },
  "promo_expires_at": "2026-11-28T23:59:59-08:00",
  "shell_shocker": false,
  "badges": [{ "title": "Black Friday Deal", "starts_at": "2026-11-19T00:00:00", "ends_at": "2026-11-28T23:59:59" }],
  "in_stock": true,
  "stock": 1,
  "quantity_limit": 1,
  "shipping": { "charge": 0, "free": true },
  "ship_from_country": "United States",
  "seller": { "name": "Newegg", "url_key": null, "marketplace": false, "rating": null, "review_count": null, "top_rated": false },
  "shipped_by_newegg": true,
  "open_box": false,
  "refurbished": false,
  "rating": 4.8,
  "review_count": 749,
  "review_params": { "group_id": 196668433, "subcategory_id": 343 },
  "category": "Desktop CPU Processor",
  "review_summary": { "total": 316, "stars": { "1": 23, "2": 4, "3": 1, "4": 22, "5": 699 } },
  "notes": [
    "list_price is the price Newegg shows struck through, price the price shown after any instant_rebate; a promo code discount (promo.code, promo.code_discount) applies at checkout and is never taken off price. lowest_price_30_days and is_lowest_price_30_days are Newegg's own figures as given. Money is rounded to the currency's digits.",
    "shipping.free is true where Newegg marks free shipping; null where the listing states a 0 charge without that mark."
  ]
}
```

$506.99 - $67 = $439.99, the price Newegg shows. The $70 BFF36 code is Newegg's checkout promo, reported apart. `variants.items[]` list the sibling CPUs with their own item numbers (Ryzen 7 9850X3D `19-113-934`, Ryzen 7 7800X3D `19-113-793`, ...); `reviews` holds the up to 8 reviews the page shows. With `"country": "ca"` the same item read $549.99 CAD, `list_price` $799.99, `instant_rebate` $250, `lowest_price_30_days` $539.99. `{"item_number": "N82E16899999999"}` answered a charged `404`: "Newegg has no product 99-999-999 on this storefront."

### Every seller's offer on one item

```bash
curl -X POST https://api.scavio.dev/api/v1/newegg/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_number": "19-113-877"}'
```

Captured `data` (2026-11-26; 2 of 20 offers shown, `notes` cut to 1 of 2):

```json
{
  "country": "us",
  "storefront": "www.newegg.com",
  "currency": "USD",
  "item_number": "19-113-877",
  "condition": "all",
  "sort": "price",
  "page": 1,
  "page_size": 20,
  "total": 28,
  "pages": 2,
  "count": 20,
  "tabs": [
    { "condition": "new", "count": 26, "lowest_price": 418.99, "lowest_price_item": "9SIA2W0KDW5195" },
    { "condition": "used", "count": 2, "lowest_price": 449.99, "lowest_price_item": "9SIC3U3KNS1228" }
  ],
  "offers": [
    {
      "item_number": "9SIA2W0KDW5195",
      "url": "https://www.newegg.com/p/9SIA2W0KDW5195",
      "price": 418.99,
      "list_price": 418.99,
      "instant_rebate": 0,
      "shipping": { "charge": 0, "free": true },
      "condition": "new",
      "in_stock": true,
      "seller": { "name": "PlatinumMicro", "url_key": "PlatinumMicro", "marketplace": true, "rating": 4.5, "review_count": 7249, "rating_12_months": 4.5, "review_count_12_months": 127, "top_rated": true },
      "shipped_by_newegg": false,
      "ship_from_country": "United States",
      "delivery_days": { "fastest": 4, "slowest": 4 }
    },
    {
      "item_number": "19-113-877",
      "url": "https://www.newegg.com/p/N82E16819113877",
      "price": 439.99,
      "list_price": 506.99,
      "instant_rebate": 67,
      "shipping": { "charge": 0, "free": true },
      "condition": "new",
      "in_stock": true,
      "seller": { "name": "Newegg", "url_key": null, "marketplace": false, "rating": null, "review_count": null, "rating_12_months": null, "review_count_12_months": null, "top_rated": false },
      "shipped_by_newegg": true,
      "ship_from_country": "United States",
      "delivery_days": null
    }
  ],
  "notes": [
    "Every seller's offer on the item, Newegg's own included (seller.name Newegg). price is the offer price after its instant rebate. tabs give each condition's offer count and lowest price as Newegg lists them (Newegg gives them with page 1 in price order; other pages and the seller_rating order answer tabs [])."
  ]
}
```

Each offer is its own item number: a marketplace offer is a `9SI...` item, readable with `/product`. Label marketplace offers as the seller's, with its rating. On `ca` the same item listed 6 offers, Newegg's own first at $549.99 CAD. An item no other seller offers answers `total` 0; open-box units are separate items (`R` suffix): search with the `open_box` filter.

### Search, category, categories, reviews, deals, seller, seller products and suggestions

- `/search` `{"query": "rtx 5070"}`: `total` 4,556, 42 items on page 1; the first, an MSI Vector 16 HX gaming laptop (`2WC-000C-0JJ10`), read $1,599 against a $1,999 list price with a $400 instant rebate and a "Black Friday Deal" badge; the GIGABYTE WindForce GeForce RTX 5070 (`14-932-777`) $899.99 ($964.99 list, $65 rebate, 30-day low $869.99). Each item carries `review_params` for `/reviews`. On `ca` the same query read `total` 279 and the WindForce card $1,249.99 CAD; on `uk` `total` 43 and £791.53 plus £50.54 shipping (`shipping.free` `false`).
- `/category` `{"category_id": "100007709", "filters": ["in_stock"]}` (GPUs / Video Graphics Cards): `total` 5,016, 36 per page, 37 spec facets (GPU series, memory, brand, ...); the first item was a marketplace listing (`9SIBKFRMAW1497`, Halfmoon Tech Store, $599.99). On `ca` use `100007708` (1,963 items); on `uk` `101582767` (83 items).
- `/categories`: 17 departments and 1,055 categories, such as Components & Storage > Core Component > CPU / Processor > Desktop CPU Processor `100007671`. Entries without a `category_id` are links Newegg sets (guides, promotions).
- `/reviews` `{"item_number": "19-113-877", "group_id": 196668433, "subcategory_id": 343}`: `total` 316, 13 pages of 25, `stars` {5: 699, 4: 22, 3: 1, 2: 4, 1: 23}; the first review (most helpful) was 5 stars, "Absolute Beast", `verified_owner` `true`, 70 of 72 found it helpful, with its `pros` and `cons`. No reviewer names. Newegg's `stars` counts and `total` are given as Newegg gives them (the item's `review_count` read 749).
- `/deals` `{}` (Shell Shocker): 38 items, `ends_at` 2026-11-27T08:00:00.000Z; `{"type": "black_friday", "category_id": "100006519"}` (Components & Storage): `total` 903, 60 per page. On `ca` Shell Shocker listed 15 items.
- `/seller` `{"seller": "TECH-EDGE"}`: TECH EDGE Store, `seller_id` 1066805289, `rating` 4.7 from 83 reviews, `positive_percent` 93.98, its `about` text and `return_policy`. An unknown store answered a charged `404`: "Newegg has no seller store No-Such-Store-Zq9."
- `/seller-products` `{"seller_id": "1066805289"}`: `total` 2,216, 36 per page, every item a marketplace `9SI...` number (an AMD Ryzen 7 9800X3D listing at $559.99), with brand facets and the seller's categories.
- `/suggestions` `{"query": "rtx 5"}`: 10 suggestions (rtx 5090, rtx 5080, rtx 5070 ti, ...) and 4 products with item number, rating and promo text.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def newegg(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/newegg/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. In-stock cards for a query, lowest price first (2 credits)
hits = newegg("search", {"query": "rtx 5070", "filters": ["in_stock"], "sort": "price_asc"})["data"]
for i in hits["items"][:5]:
    print(i["item_number"], i["title"][:60], i["price"], i["list_price"], i["seller"]["name"])

# 2. One item: how Newegg builds the price (2 credits)
p = newegg("product", {"item_number": "19-113-877"})["data"]
if p["buy_box_changed"]:
    print("Newegg's own unit is unavailable; the page serves", p["served_item"], "from", p["seller"]["name"])
print(p["list_price"], "-", p["instant_rebate"], "=", p["price"], "| 30-day low", p["lowest_price_30_days"])
if p["promo"] and p["promo"]["code"]:
    # A checkout code: report it apart, never subtract it from price.
    print("promo", p["promo"]["code"], p["promo"]["code_discount"], "until", p["promo_expires_at"])

# 3. Every seller's offer on it (2 credits)
offers = newegg("offers", {"item_number": "19-113-877"})["data"]
for t in offers["tabs"]:
    print(t["condition"], t["count"], "from", t["lowest_price"])
for o in offers["offers"][:5]:
    print(o["price"], o["condition"], o["seller"]["name"], o["seller"]["marketplace"], o["delivery_days"])

# Prices change between calls. Store each answer with fetched_at and run this
# on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Listing, product, offers and deals `data` carry `country`, `storefront` and `currency`; every `data` carries `notes`.

- **item** (search, category, deals, seller-products) - `type` (`item` or `combo`), `item_number`, `product_number`, `title`, `brand`, `model`, `url`, `list_price`, `price`, `instant_rebate`, `lowest_price_30_days`, `is_lowest_price_30_days`, `shipping` {`charge`, `free`}, `promo` {`text`, `code`, `code_discount`}, `badges`, `rating`, `review_count`, `seller` {`name`, `url_key`, `marketplace`}, `shipped_by_newegg`, `ship_from_country`, `in_stock`, `open_box`, `refurbished`, `sponsored`, `best_selling_rank`, `category`, `image`, `review_params` {`group_id`, `subcategory_id`}, `group`; combos: `combo_id`, `title`, `url`, `list_price`, `combo_discount`, `price`, `items`.
- **lists** - search: `query`, `sort`, `filters`, `page`, `total`, `count`, `items[]`, `facets[]` {`name`, `type`, `options[]` {`id`, `name`, `selected`}}, `categories[]` {`name`, `category_id`, `children`}, `breadcrumbs`; category adds `category_id`, `query`; seller-products `seller_id`, `query`; deals `type`, `category_id`, `page`, `total`, `count`, `ends_at`, `items[]`, `categories[]`.
- **categories** - `department_count`, `category_count`, `categories[]` {`name`, `category_id`, `link`, `children`}.
- **product** - `item_number`, `buy_box_changed`, `requested_item`, `served_item`, `parent_item`, `title`, `brand`, `model`, `mpn`, `upc`, `url`, `currency`, `list_price`, `original_price`, `price`, `instant_rebate`, `lowest_price_30_days`, `is_lowest_price_30_days`, `black_friday_save_percent`, `promo`, `promo_expires_at`, `shell_shocker`, `badges[]` {`title`, `starts_at`, `ends_at`}, `in_stock`, `stock`, `quantity_limit`, `shipping`, `ship_from_country`, `seller` {`name`, `url_key`, `marketplace`, `rating`, `review_count`, `top_rated`}, `shipped_by_newegg`, `open_box`, `refurbished`, `rating`, `review_count`, `review_params`, `category`, `breadcrumbs[]` {`name`, `category_id`}, `bullets`, `specs[]` {`group`, `specs[]` {`name`, `value`}}, `warranty`, `images`, `variants` {`options`, `items[]` {`item_number`, `options`, `active`}}, `combo_builder`, `package_options`, `review_summary` {`total`, `stars`}, `reviews` (up to 8, no reviewer names), `questions[]` {`question`, `date`, `upvotes`, `answer_count`, `answers[]` {`answer`, `best_answer`, `upvotes`, `date`}}.
- **offers** - `item_number`, `condition`, `sort`, `page`, `page_size`, `total`, `pages`, `count`, `tabs[]` {`condition`, `count`, `lowest_price`, `lowest_price_item`}, `offers[]` {`item_number`, `url`, `price`, `list_price`, `instant_rebate`, `shipping`, `condition`, `in_stock`, `seller` {`name`, `url_key`, `marketplace`, `rating`, `review_count`, `rating_12_months`, `review_count_12_months`, `top_rated`}, `shipped_by_newegg`, `ship_from_country`, `delivery_days` {`fastest`, `slowest`}}.
- **reviews** - `item_number`, `sort`, `rating`, `verified_only`, `page`, `per_page`, `total`, `pages`, `count`, `stars` {5..1}, `reviews[]` {`rating`, `title`, `text`, `pros`, `cons`, `date`, `verified_owner`, `helpful_votes`, `total_votes`, `item_number`, `item_title`, `language`, `manufacturer_reply`}.
- **seller** - `seller`, `name`, `seller_id`, `rating`, `review_count`, `positive_percent`, `about`, `return_policy`.
- **suggestions** - `query`, `count`, `suggestions`, `product_count`, `products[]` {`item_number`, `title`, `url`, `promo_text`, `rating`, `review_count`, `image`}.

## Guardrails

- Name it "Newegg (newegg.com, the US computer and electronics store)" on first mention, and name the storefront (newegg.com, newegg.ca, or the Newegg Global storefront for a country) with every price. Newegg Business and Newegg accounts are not read.
- Prices: quote `price` with `list_price` and `instant_rebate`, the currency, the storefront and the `fetched_at` date. A promo code is Newegg's checkout offer: report the code, its amount and expiry apart and never subtract it.
- Buy-box swap: when `buy_box_changed` is `true`, say that Newegg's own unit of the requested item is unavailable and that the price shown is the marketplace offer `served_item` from the named seller.
- Sellers: label marketplace offers with the seller's store name and rating; marketplace store names are public business data. Never call a seller reliable or unreliable beyond its ratings as given.
- Comparing Newegg with Amazon, Best Buy, Micro Center or Walmart: compare only the same item (same UPC or MPN), each with its date, and label marketplace sellers as such. Never call one retailer cheaper beyond the numbers shown.
- Report Newegg's labels and figures (list price, instant rebate, 30-day low, badges, Shell Shocker end, promo expiry) as given. Never judge a price, a discount or a deal deadline.
- Stock: `in_stock`, `stock` and `quantity_limit` as Newegg reported them at the moment of the call; Scavio makes no promise of their accuracy. Never promise delivery.
- Reviews: no reviewer names are returned. `verified_owner` is Newegg's own mark.
- Not available: price history (poll and store), a live price check at checkout, Newegg Business prices, offers, deals, sellers or suggestions on the Global storefronts, the department tree outside us, cart, ordering or checkout. This API cannot add to cart or buy.
- Terms: Scavio does not collect or store Newegg data: each call fetches the public Newegg page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Newegg's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Newegg product photos or logos; link items by `url` instead.
- Never fabricate prices, item numbers, sellers, ratings, stock, dates or promo codes. Only return what the API returned, with the `fetched_at` time, the storefront and the item `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` the endpoint does not serve ("offers is served on country us, ca (the Newegg Global storefronts have no other-sellers list); uk is not one of them."); an `item_number` that is not a Newegg item number; a `category_id` or `seller_id` that is not digits; a `seller` that is not a store key; `filters` that are neither a filter name nor a facet id ("filters: ... is not a filter name (sold_by_newegg, in_stock, new, recertified, used, open_box, lowest_price_30_days, 40_percent_off) or a facet id (digits, facets[].options[].id of an answer).") or more than 10; reviews without `group_id` and `subcategory_id` ("group_id and subcategory_id are required: take review_params.group_id and review_params.subcategory_id from the product (or search) answer for this item."); a `page` outside its range; an unknown `sort`, `type` or `condition`. A review request Newegg refuses answers "Newegg refused this review request. Check item_number, group_id and subcategory_id (review_params of the product answer for this item)."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Newegg has no product <item> on this storefront.", "Newegg has no item <item>.", "Newegg has no reviews for <item>.", "Newegg has no seller store <seller>.", "No Newegg category has this id.", "No Newegg seller has this listing id.", "This Newegg deal event has no page.", "This search has no results page.". Take item numbers, category ids, seller keys and review params from a previous answer of the same storefront rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api).
- `502` means Newegg data was temporarily unavailable ("Newegg is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Newegg is busy ("Newegg is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.newegg.search({ query: "rtx 5070", filters: ["in_stock"], sort: "price_asc" });
const { data: item } = await scavio.newegg.product({ item_number: "19-113-877" });
const { data: offers } = await scavio.newegg.offers({ item_number: "19-113-877", condition: "new" });
const { data: reviews } = await scavio.newegg.reviews({ item_number: "19-113-877", group_id: 196668433, subcategory_id: 343 });
const { data: gpus } = await scavio.newegg.category({ category_id: "100007709" });
const { data: tree } = await scavio.newegg.categories();
const { data: deals } = await scavio.newegg.deals({ type: "shell_shocker" });
const { data: seller } = await scavio.newegg.seller({ seller: "TECH-EDGE" });
const { data: listed } = await scavio.newegg.sellerProducts({ seller_id: "1066805289" });
const { data: typed } = await scavio.newegg.suggestions({ query: "rtx 5" });
const { data: canada } = await scavio.newegg.product({ item_number: "19-113-877", country: "ca" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.newegg.search(...)`, `category`, `categories`, `product`, `offers`, `reviews`, `deals`, `seller`, `seller_products` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_newegg`, `get_newegg_category`, `get_newegg_categories`, `get_newegg_product`, `get_newegg_offers`, `get_newegg_reviews`, `get_newegg_deals`, `get_newegg_seller`, `get_newegg_seller_products` and `get_newegg_suggestions`. Newegg is opt-in: add `newegg` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,newegg"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/newegg-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [category](https://scavio.dev/docs/newegg-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [categories](https://scavio.dev/docs/newegg-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [product](https://scavio.dev/docs/newegg-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [offers](https://scavio.dev/docs/newegg-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [reviews](https://scavio.dev/docs/newegg-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [deals](https://scavio.dev/docs/newegg-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [seller](https://scavio.dev/docs/newegg-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [seller products](https://scavio.dev/docs/newegg-seller-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api), [suggestions](https://scavio.dev/docs/newegg-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api). Overview: [Newegg API](https://scavio.dev/newegg-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=newegg-api).
