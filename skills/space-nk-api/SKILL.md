---
name: space-nk-api
description: Space NK API for Space NK (spacenk.com, the London-based luxury beauty retailer, owned by Ulta Beauty) - the same product priced on Space NK's four sites in their own currencies, uk (GBP), ie (EUR), nl (EUR, Dutch copy) and au (AUD), with the struck-through list price next to a reduced price as Space NK shows it (Charlotte Tilbury Airbrush Flawless Foundation read 30 GBP (list 40) on uk, 34.50 EUR (list 46) on ie and nl and 59 AUD (list 78) on au on Nov 26, 2026); keyword search, any category (black-friday is the Black Friday list) and any brand, 36 products a page with total and pages, Space NK's ten sorts and a brand filter, with discount badge, gift badges, rating, review count and the online stock count of the shade or size shown; one product with EAN, every shade or size and its availability, ingredients, how to use, key benefits, size and Space NK's promotions on it; customer reviews up to 100 a page with four sorts, a star filter, text search, the rating distribution and syndicated reviews flagged (no names); the gifts with purchase on the uk and ie offers pages with brand, gift, condition, spend threshold and the page's end line; Space NK's UK stores nearest a postcode or point for one product with hours, Click and Collect answer and the in-store flag; the A-Z brand directory and search suggestions. 9 endpoints, 1 credit per call (a listing with full=true up to 5). Not available - the US market, a price filter, store stock counts, price history, cart or checkout.
version: 1.0.0
tags: spacenk, space-nk, space-nk-api, spacenk-api, spacenk-com, space-nk-prices, space-nk-uk, space-nk-ireland, space-nk-netherlands, space-nk-australia, space-nk-black-friday, space-nk-offers, space-nk-gift-with-purchase, space-nk-reviews, space-nk-stores, space-nk-click-and-collect, space-nk-brands, space-nk-product-data, ulta-beauty, luxury-beauty, beauty-prices, skincare-prices, makeup-prices, foundation-shades, charlotte-tilbury, augustinus-bader, medik8, shades, ean, gbp, eur, aud, uk-retail, price-comparison, price-monitoring, product-search, product-data, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/spacenk-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api
---

# Space NK API - SpaceNK Prices by Market, Offers, Shades, Reviews

Read Space NK (spacenk.com, the London-based luxury beauty retailer, owned by Ulta Beauty): keyword search, any category or brand, one product with every shade or size, customer reviews, the gifts with purchase on the offers page, the UK stores near a postcode for one product, the brand directory and search suggestions. Every answer is what Space NK's public pages show a visitor without an account at the moment of the call, on one of four sites in its own currency: uk (GBP), ie (EUR), nl (EUR, Dutch copy) and au (AUD). All 9 endpoints cost 1 credit; a listing with `full: true` costs up to 5.

**Read-only data.** This skill reads the public pages Space NK shows to any visitor and returns them as JSON for analysis. It uses no Space NK account, no loyalty login, no bag and no checkout.

**The job this skill is for: one Space NK product priced on each Space NK site, in that site's own currency.** Space NK prices each site itself; the numbers are not currency conversions of each other. Captured 2026-11-26 with `/product` (one call per market, 1 credit each) and from search, category and brand listings:

| Product (product id) | uk (GBP) | ie (EUR) | nl (EUR) | au (AUD) |
|---|---|---|---|---|
| Charlotte Tilbury Airbrush Flawless Foundation (MUK200057800; shade 1 COOL, UK200057805, on uk and ie) | 30, list 40 | 34.50, list 46 | 34.50, list 46 | 59, list 78 |
| Medik8 Exo-PDRN Prismatic+ (MUK200064210) | 59.25, list 79 | 68.25, list 91 | 68.25, list 91 | not captured |
| Augustinus Bader The Vitamin C Serum (MUK200058870) | 217.50, list 290 | not captured | not captured | 425, list 565 |
| Milk Makeup RISE Mascara (MUK200036010) | 18.20, list 26 | not captured | not captured | 36, list 51 |

All four showed a reduced price on the capture date (`list_price` is the price Space NK shows struck through). The product id is the same on every site, so send the same `product_id` with each `market`. Put each price with its market, currency, the product id (and the shade or size id when one was read) and the date. Never convert one market's price and present it as another market's price.

Ten limits shape every answer, so say them plainly:
- **Credits.** Every endpoint costs 1 credit. A listing (search, category, brand) with `full: true` costs up to 5: Space NK's page holds 36 products, the first 12 come in full and the other 24 as ids in `more_product_ids`, and `full: true` fills those 24 too. `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **36 a page, 12 in full by default.** Without `full`, `items` holds 12 products and `more_product_ids` the page's other 24 product ids. Read one with `/product`, or send `full: true` (up to 5 credits). Products that did not load in full stay in `more_product_ids` and are not billed.
- **Prices are per market.** `market` picks the site: `uk` (default, GBP), `ie` (EUR), `nl` (EUR, Dutch product copy and messages) or `au` (AUD). Report the market and currency with every price.
- **No US market.** `us`, `de` and `ca` are refused (`400`): Space NK's US, German and Canadian paths show the UK store in GBP, not prices of their own.
- **No price filter.** `min_price` and `max_price` are refused (`400`): Space NK's site ignores them. Use `sort` `price_low_to_high` or `price_high_to_low`.
- **stock_count is online stock for one shade or size.** On a tile it is the stock of the shade or size the tile shows (`sku`); on `/product` it is given for a shade or size (send its `variants[].id`), `null` on a master product with several shades. It is not store stock.
- **Stores are UK only and show a flag, not counts.** `/stores` needs a `product_id` and a UK postcode or point. `in_store_available` is Space NK's in-store flag for that product (it read `false` at every store in the captures); `click_collect_label` is its Click and Collect answer as worded. Space NK shows no unit counts per store.
- **Reviews take the product id only.** `/reviews` needs the product id starting with M (`MUK200057800`, `items[].product_id` or `/product`'s `master_id`); a shade or size id is a `400`. The reviews are one English pool shown on every market.
- **Offers are uk and ie only.** The nl and au offers pages show the UK offers in GBP, so `/offers` refuses them (`400`). Each offer is a brand gift with purchase as Space NK words it; Space NK shows no per-offer dates, only the page's own line in `validity` (`null` when the page shows none, as on ie in the capture).
- **What is not there.** No US market, no price filter, no store stock counts, no review names or photos, no price history (store your own answers with `fetched_at`), no bag or checkout.

Space NK publishes no public API for its catalog, prices or stores. What exists is an affiliate programme for publishers, not a product data API. This skill reads Space NK's own public pages with one Scavio key.

See also: `sephora-product-data` (Sephora US and Canada prices, shades and offers), `ulta-beauty-api` (Ulta Beauty prices and reviews), `dermstore-skincare-prices-api` (Dermstore US and Canada skincare prices and offers), `lookfantastic-api` (Lookfantastic prices across its country sites) and `cult-beauty-api` (Cult Beauty prices and offers). Same product only: match brand, product name and size (and the shade for makeup), show each price with its retailer, market, currency and date.

## When to trigger

Use this skill when the user asks to:
- Price one Space NK product on the UK, Irish, Dutch and Australian sites, each in its own currency
- Search Space NK or read a category or brand, sorted by price, discount, best sellers, rating or newest, with discount and gift badges
- Read Space NK's Black Friday list (`category_id` `black-friday`) sorted by discount
- Read one Space NK product with EAN, every shade or size and its availability, ingredients, size and Space NK's promotions on it
- Read Space NK customer reviews with the rating distribution, filtered by stars or text
- List the gifts with purchase on Space NK's offers page with their spend thresholds
- Find the Space NK stores near a UK postcode for one product, with hours and Click and Collect
- List Space NK's brands A-Z or read its search suggestions

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 credit (a listing with `full: true` up to 5), so 50 credits cover 50 product, review or listing calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, products and reviews answered in about 1-2 seconds, stores 1-3, offers 2-4, brands 1-6, listings 2-7 and a full listing about 8. An unknown product id can take about a minute before its `502`. Set a client timeout of at least 240 seconds and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/spacenk/search` | Products for keywords: price, list price, discount badge, gift badges, rating, review count, online stock of the shade shown; total, pages; ten sorts, brand filter | 1; up to 5 with `full: true` |
| `POST /api/v1/spacenk/category` | One category by id (`black-friday`, `skincare-treatment-serum`, `makeup-complexion-foundation` ...), as search | 1; up to 5 with `full: true` |
| `POST /api/v1/spacenk/brand` | One brand's products by brand id (`brands[].id`), as search | 1; up to 5 with `full: true` |
| `POST /api/v1/spacenk/brands` | Every brand A-Z (or one letter) with its id for `/brand` and its name for the brand filter | 1 |
| `POST /api/v1/spacenk/product` | One product by product id or shade / size id: EAN, price, list price, availability, online stock, size, descriptions, key benefits, how to use, ingredients, rating, images, every shade or size, promotions, badges | 1 |
| `POST /api/v1/spacenk/reviews` | Customer reviews of one product: rating, title, text, date, recommended, syndicated source, helpful votes, skin context; rating distribution; four sorts, stars, text search | 1 |
| `POST /api/v1/spacenk/suggestions` | Space NK's suggestions for what a shopper typed: brands, categories, article ids and products | 1 |
| `POST /api/v1/spacenk/stores` | Space NK's UK stores nearest a postcode or point for one product: address, phone, hours, distance, in-store flag, Click and Collect | 1 |
| `POST /api/v1/spacenk/offers` | The gifts with purchase on the offers page (uk or ie): brand, gift, condition, spend threshold, the page's end line | 1 |

## Markets

Every answer carries `market` {`code`, `country`, `name`, `language`, `currency`}.

| `market` | Site | Currency | Language |
|---|---|---|---|
| `uk` (default; `gb` also accepted) | United Kingdom | GBP | en |
| `ie` | Ireland | EUR | en |
| `nl` | Netherlands | EUR | nl (Dutch names, descriptions and messages such as "Op voorraad") |
| `au` | Australia | AUD | en |

Not offered (`400`): `us` ("Space NK's US path shows UK prices in GBP, not US prices"), `de` and `ca` (their paths show the UK store in GBP). `/stores` is uk only; `/offers` is uk or ie. Reviews are the same English pool on every market.

## Prices, shades, stock and offers

| Field | Meaning |
|---|---|
| `price` | Space NK's price on that market's site, in `currency` |
| `list_price` | The price Space NK shows struck through next to a reduced price (equal to `price`, or `null`, when nothing is reduced) |
| `on_sale` (tiles) | Whether the tile shows a reduced price |
| `discount_badge`, `promo_badges` (tiles) | Space NK's own badges as shown ("25% OFF", "FREE GIFT") |
| `badges` (tiles) | Space NK's tile badges as worded ("446 sold this week", "Trending this week", "new formulation") |
| `stock_count` | Online stock Space NK reports for one shade or size (the tile's `sku`, or the variant read on `/product`); `null` on a master product with several shades. Not store stock |
| `product_id`, `sku` (tiles) | The product id (starts with M, `MUK200057800`) and the shade or size the tile shows (`UK200057805`) |
| `type`, `master_id` (product) | `master` (the product with all its shades / sizes) or `variant` (one shade / size); a single-size product comes back as `variant` |
| `variants[]` (product) | Every shade or size: `id` (send it as `product_id`), `name` ("1 COOL"), `in_stock`, `availability`, `in_stock_date`, `swatch_colour` |
| `variant_counts` (product) | Shades or sizes in stock, on preorder and not available (`{"in_stock": 43, "preorder": 0, "not_available": 1}`) |
| `promotions[]` (product) | Space NK's promotions on the product as worded (free delivery, free samples, a gift with purchase), with no dates |
| `in_store_available` (stores) | Space NK's in-store flag for the product at the store, not a count |
| `spend_threshold` (offers) | The spend in the condition, `{amount, currency}`, `null` when the condition is not a spend ("When you buy 2 or more Aesop Products") |

- **Percent off:** compute it from `price` and `list_price` and label it computed (30 against 40 is 25% off, computed), or quote `discount_badge` as Space NK shows it.
- **Shades:** for makeup, compare the same shade (`variants[].id`) across markets; a master answer's `price` is the product's price as Space NK shows it on the product page.

## Workflow

1. **Find the products.** `/search` with `query` (and `brand` to narrow), `/category` with a `category_id`, or `/brand` with a `brand_id` from `/brands`. Note each `product_id`, `sku`, `name`, `brand`.
2. **Read the rest of the page.** The 24 ids in `more_product_ids`: send `full: true` on the listing (up to 5 credits), or `/product` for the ones you need.
3. **Price per market.** `/product` with the same `product_id` and each `market` (`uk`, `ie`, `nl`, `au`), 1 credit each; for makeup send the shade's `variants[].id`. Read `price`, `list_price`, `currency`, `availability`.
4. **Offers.** `/offers` for `uk` or `ie`: each brand's gift, condition and spend threshold, and the page's `validity` line.
5. **Reviews.** `/reviews` with the M product id; `stars: [1, 2]` for the critical ones, `search` for a word.
6. **Stores.** `/stores` with the `product_id` and a UK `postcode` (or `latitude` + `longitude`): hours, Click and Collect, the in-store flag.
7. **Report.** Each price with its market, currency, product (and shade) id and the capture date; a percent off labelled computed or the badge as shown.
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`), category (`/category`) and brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required (search) | Keywords or a brand, up to 200 chars |
| `category_id` | string | required (category) | A Space NK category id (`black-friday`, `skincare-treatment-serum`, `makeup-complexion-foundation`) |
| `brand_id` | string | required (brand) | A brand id from `/brands` (`brands[].id`: `medik8`, `Charlotte Tilbury`) |
| `brand` | string or list | none | Search and category only: up to 10 brand names as Space NK shows them (`items[].brand` or `brands[].name`: `Medik8`). On `/brand` it is a `400` |
| `page` | integer | 1 | 1-300; 36 products a page. A page past the last returns no products |
| `sort` | string | `relevance` | `relevance`, `best_sellers`, `new`, `our_favourites`, `price_high_to_low`, `price_low_to_high`, `rating`, `most_viewed`, `discount`, `brand` (Space NK's own orders) |
| `full` | boolean | false | Fill all 36 products in full (up to 5 credits) |
| `market` | string | `uk` | `uk`, `ie`, `nl`, `au` |
| `min_price`, `max_price` | - | - | Not offered (`400`): use a price sort |

### Product (`/product`), reviews (`/reviews`), stores (`/stores`)

| Endpoint | Parameters |
|---|---|
| `/product` | `product_id` (required: a product id `MUK200057800` or a shade / size id `UK200057805`), `market` |
| `/reviews` | `product_id` (required, the M product id), `page` (default 1), `page_size` 1-100 (default 20; up to 10,000 reviews deep), `sort` (`newest` default, `most_helpful`, `highest_rating`, `lowest_rating`), `stars` (one or a list, 1-5), `search` (text, up to 100 chars), `market`. `skin_type` is a `400`: read each review's `context.skin_type` |
| `/stores` | `product_id` (required), `postcode` (a full UK postcode, `W1D 1BS`) or `latitude` + `longitude` (a point in the UK), `limit` 1-20 (default 10), `market` (uk only) |

### Brands, suggestions, offers

| Endpoint | Parameters |
|---|---|
| `/brands` | `letter` (one of A-Z or `#`), `market` |
| `/suggestions` | `query` (required, up to 100 chars), `market` |
| `/offers` | `market`: `uk` (default) or `ie` |

## Examples

### One product on the Australian site

```bash
curl -X POST https://api.scavio.dev/api/v1/spacenk/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "MUK200057800", "market": "au"}'
```

Captured `data` (2026-11-26; `url`, `images`, `description`, `short_description`, `how_to_use`, `ingredients`, `key_benefits` and `notes` dropped, `variants` cut to 2 of 44):

```json
{
  "market": {"code": "au", "country": "AU", "name": "Australia", "language": "en", "currency": "AUD"},
  "requested_id": "MUK200057800",
  "product_id": "MUK200057800",
  "master_id": "MUK200057800",
  "type": "master",
  "ean": "5056446654937",
  "name": "Airbrush Flawless Foundation",
  "brand": "Charlotte Tilbury",
  "price": 59,
  "list_price": 78,
  "currency": "AUD",
  "price_text": "AU$ 59.00",
  "list_price_text": "AU$ 78.00",
  "in_stock": true,
  "availability": "IN_STOCK",
  "availability_message": "In Stock",
  "stock_count": null,
  "orderable": true,
  "button": "ADD_TO_BAG",
  "size": {"quantity": 30, "unit": null},
  "rating": 4.461,
  "review_count": 269,
  "variant_attribute": "color",
  "variant_counts": {"in_stock": 43, "preorder": 0, "not_available": 1},
  "variants": [
    {"id": "UK200057805", "attribute": "color", "name": "1 COOL", "in_stock": true, "availability": "IN_STOCK", "in_stock_date": null, "selectable": true, "selected": false, "swatch_colour": "#FAE4CD"},
    {"id": "UK200057795", "attribute": "color", "name": "1 NEUTRAL", "in_stock": true, "availability": "IN_STOCK", "in_stock_date": null, "selectable": true, "selected": false, "swatch_colour": "#F7DDC4"}
  ],
  "promotions": [],
  "badges": {"offers": ["25% OFF"], "gift": [], "trade": ["new formulation", "125 sold today", "Trending this week"]},
  "category_path": "makeup/complexion/foundation",
  "restricted_shipping": false,
  "hazmat": false,
  "coming_soon": null
}
```

The same `product_id` on `nl` read 34.50 EUR (list 46) with Dutch copy ("Op voorraad"). The shade `UK200057805` read 30 GBP (list 40) on `uk` and 34.50 EUR (list 46) on `ie`, each with `stock_count` 21.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/spacenk/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "vitamin c"}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 12, `more_product_ids` to 2 of 24, `url`, `image` and `notes` dropped):

```json
{
  "market": {"code": "uk", "country": "GB", "name": "United Kingdom", "language": "en", "currency": "GBP"},
  "query": "vitamin c",
  "page": 1,
  "page_size": 36,
  "sort": "relevance",
  "full": false,
  "total": 367,
  "total_pages": 11,
  "has_more": true,
  "count": 12,
  "items": [
    {"product_id": "MUK200058870", "sku": "UK200058870", "name": "The Vitamin C Serum", "brand": "Augustinus Bader", "price": 217.5, "list_price": 290, "currency": "GBP", "on_sale": true, "discount_badge": "25% OFF", "promo_badges": ["25% OFF"], "badges": [], "rating": 4.65, "review_count": 364, "in_stock": true, "availability": "IN_STOCK", "stock_count": 111},
    {"product_id": "MUK200035172", "sku": "UK200035172", "name": "Vitamin C + Lactic 15% Vitamin C Firm & Bright Serum", "brand": "Dr. Dennis Gross", "price": 65.25, "list_price": 87, "currency": "GBP", "on_sale": true, "discount_badge": "25% OFF", "promo_badges": ["FREE GIFT", "25% OFF"], "badges": [], "rating": 3.94, "review_count": 170, "in_stock": true, "availability": "IN_STOCK", "stock_count": 79}
  ],
  "more_product_ids": ["...", "..."]
}
```

With `"brand": "Medik8"` the same query returned 11 Medik8 products (`brand_filter` ["Medik8"]). With `"query": "foundation", "full": true` all 36 products came in full, `more_product_ids` empty, for 5 credits.

### Black Friday by discount

```bash
curl -X POST https://api.scavio.dev/api/v1/spacenk/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "black-friday", "sort": "discount"}'
```

Captured (2026-11-26): `total` 7607 over 212 pages; first By Terry Hyaluronic Hydra Foundation SPF30 at 39.75 GBP (list 53, "25% OFF", "Free Gift", `stock_count` 27), Milk Makeup RISE Mascara at 18.20 (list 26, "30% OFF") and VIEVE Sunset Blush at 20.25 (list 27, `stock_count` 2).

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/spacenk/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "MUK200057800", "page_size": 10}'
```

Captured `data` (2026-11-26; `reviews` cut to 2 of 10, texts shortened, `notes` dropped):

```json
{
  "product_id": "MUK200057800",
  "page": 1,
  "page_size": 10,
  "sort": "newest",
  "total": 269,
  "total_pages": 27,
  "has_more": true,
  "count": 10,
  "rating_distribution": {"1": 6, "2": 14, "3": 14, "4": 51, "5": 184},
  "reviews": [
    {"id": "186587214", "rating": 5, "title": "Love this foundation", "text": "I have worn this founation for years, ...", "submitted_at": "2026-11-19T11:10:18.000+00:00", "recommended": true, "syndicated": false, "syndication_source": null, "helpful_votes": 20, "unhelpful_votes": 10, "context": {"skin_type": "Normal / Balanced", "best_use": "Illuminating", "skin_tone": "Very Fair"}, "tags": []},
    {"id": "1237305019", "rating": 5, "title": "Great, and easy to blend in", "text": "This is my second purchase for the same foundation ...", "submitted_at": "2026-11-18T14:40:51.000+00:00", "recommended": null, "syndicated": true, "syndication_source": {"name": "charlottetilbury.com", "url": "https://www.charlottetilbury.com/us/product/airbrush-flawless-foundation-shade-9-warm"}, "helpful_votes": 0, "unhelpful_votes": 0, "context": null, "tags": []}
  ]
}
```

`{"product_id": "MUK200058870", "stars": [1, 2], "market": "ie"}` returned the 6 one- and two-star reviews of The Vitamin C Serum (distribution 3, 3, 22, 62, 274). Report a syndicated review with its source.

### Stores near a postcode

```bash
curl -X POST https://api.scavio.dev/api/v1/spacenk/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "MUK200064992", "postcode": "W1D 1BS", "limit": 5}'
```

Captured (2026-11-26): 5 stores, nearest first: Oxford Circus (S0121, 216 Oxford Street, London W1C 1DA) at 0.3 miles, Monday-Saturday 09:30 - 21:00, Sunday 12:00 - 18:00, then Covent Garden (S0110, 5-7 Neal Street) at 0.43 miles; each `in_store_available` false, `click_collect_label` "Click & Collect not available today". Near `M1 1AE` with `limit` 20, Arndale (0.48 miles) and Trafford (4.9 miles) read "Click & Collect from Monday 7th December".

### Offers, brands, suggestions

- `/offers` `{}`: `title` "Promotions & Offers", `validity` "Online, on the app & in-store. Ends 30th November at 11.45pm (GMT). T&Cs and exclusions apply.", 70 offers, for example About Face "Full Size Line Artist in Shade Call Me Crazy (Full Size)" "When you spend £40 on About Face" (`spend_threshold` 40 GBP) and Aesop "Mouthwash Beaker" "When you buy 2 or more Aesop Products" (`spend_threshold` null). `{"market": "ie"}`: 47 offers in EUR (Paula's Choice "When you spend €40 on Paula's Choice"), `validity` null.
- `/brands` `{"letter": "C"}`: `total` 245 brands, 15 under C, each with `id` for `/brand` and `name` for the brand filter (`{"id": "Chantecail", "name": "Chantecaille"}`, `{"id": "Charlotte Tilbury", "name": "Charlotte Tilbury"}`, `{"id": "clomana-beauty", "name": "Clomana Beauty"}`). Brand ids are Space NK's own: send `brands[].id` as given.
- `/brand` `{"brand_id": "medik8"}`: 71 products over 2 pages.
- `/suggestions` `{"query": "charlotte"}`: 2 brands, 10 categories (Charlotte Tilbury Gift Sets, Charlotte Tilbury Foundations ...), 10 article ids and 6 products, first Charlotte's Hollywood Beauty Wonderland at 127.50 GBP (list 170, "446 sold this week").

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def spacenk(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/spacenk/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. One product priced on each Space NK site (1 credit each)
for market in ["uk", "ie", "nl", "au"]:
    p = spacenk("product", {"product_id": "MUK200057800", "market": market})["data"]
    print(market, p["name"], p["price"], p["list_price"], p["currency"], p["availability"])

# 2. Black Friday by discount, the whole page in full (up to 5 credits)
d = spacenk("category", {"category_id": "black-friday", "sort": "discount", "full": True})["data"]
for i in d["items"]:
    print(i["brand"], i["name"], i["price"], i["list_price"], i["discount_badge"])

# 3. Gifts with purchase on the UK offers page (1 credit)
o = spacenk("offers", {"market": "uk"})["data"]
print(o["validity"])
for g in o["offers"]:
    print(g["brand"], g["gift"], g["condition"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`code`, `country`, `name`, `language`, `currency`}; most carry `notes`.

- **tile** (search, category, brand, suggestions products) - `product_id`, `sku`, `name`, `brand`, `url`, `image`, `price`, `list_price`, `currency`, `on_sale`, `discount_badge`, `promo_badges`, `badges`, `rating`, `review_count`, `in_stock`, `availability`, `stock_count`.
- **search / category / brand** - `query` / `category_id` / `brand_id`, `page`, `page_size` (36), `sort`, `brand_filter` (when sent), `full`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `more_product_ids[]`, `notes`.
- **brands** - `letter`, `total`, `count`, `brands[]` {`id`, `name`, `url`, `letter`}.
- **product** - `requested_id`, `product_id`, `master_id`, `type`, `ean`, `name`, `brand`, `url`, `price`, `list_price`, `currency`, `price_text`, `list_price_text`, `in_stock`, `availability`, `availability_message`, `stock_count`, `orderable`, `button` (`ADD_TO_BAG` or `NOTIFY_ME`), `min_order_quantity`, `max_order_quantity`, `size` {`quantity`, `unit`}, `short_description`, `description`, `key_benefits`, `how_to_use`, `kit_contents`, `ingredients`, `rating`, `review_count`, `images`, `variant_attribute` (`color` or `size`), `variant_counts`, `variants[]` {`id`, `attribute`, `name`, `in_stock`, `availability`, `in_stock_date`, `selectable`, `selected`, `swatch_colour`}, `promotions[]` {`id`, `name`, `callout`, `details`, `type`, `gift_product_id`}, `badges` {`offers`, `gift`, `trade`}, `category_path`, `skin_suitability`, `restricted_shipping`, `hazmat`, `coming_soon`.
- **reviews** - `product_id`, `page`, `page_size`, `sort`, `stars`, `search`, `total`, `total_pages`, `has_more`, `count`, `rating_distribution` {"1".."5"}, `reviews[]` {`id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `syndicated`, `syndication_source` {`name`, `url`}, `helpful_votes`, `unhelpful_votes`, `context` {`skin_type`, `skin_tone`, `best_use`, `sensitive_skin`}, `tags`}.
- **suggestions** - `query`, `count`, `brands[]` {`name`, `url`}, `categories[]` {`name`, `url`}, `articles[]` (editorial article ids), `products[]` (tiles).
- **stores** - `product_id`, `location` {`postcode`} or {`latitude`, `longitude`}, `count`, `stores[]` {`store_id`, `name`, `address`, `city`, `region`, `postcode`, `country`, `latitude`, `longitude`, `phone`, `opening_hours[]` {`day`, `hours`}, `distance_miles`, `in_store_available`, `click_collect_available`, `click_collect_label`, `express_available`}.
- **offers** - `title`, `validity`, `terms_url`, `count`, `offers[]` {`brand`, `gift`, `condition`, `spend_threshold` {`amount`, `currency`}, `brand_url`, `image`}.

## Guardrails

- Name it "Space NK (spacenk.com, the London-based luxury beauty retailer)" on first mention, "Space NK" after that.
- Prices: quote each with its market, currency, the product (and shade) id and the `fetched_at` date ("listed on spacenk.com's UK site at 30 GBP, list 40, on Nov 26, 2026"). Never present one market's price as another's, and never convert currencies and call the result Space NK's price.
- Percent off: computed from `price` and `list_price` and labelled computed, or Space NK's `discount_badge` quoted as shown.
- Stock: `stock_count` is online stock for one shade or size; `in_store_available` is a flag. Never report either as a store's unit count.
- Offers: quote the gift, condition and `validity` as Space NK words them; Space NK shows no per-offer dates.
- Reviews: no reviewer names, locations or photos are returned; never attribute a review to a person. Report syndicated reviews with their `syndication_source`.
- Descriptive only: no commentary on Space NK's business, ownership, pricing practices or policies.
- Do not republish Space NK product photos, descriptions or logos. Write spacenk.com as plain text and cite product names, product ids and capture dates rather than linking Space NK pages.
- Terms: Scavio does not collect or store Space NK data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no bag and no checkout. Space NK's website terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, list prices, badges, shades, stock, offers, stores or reviews. Only return what the API returned, with the `fetched_at` time.
- Not available: the US, German or Canadian market, a price filter, store stock counts, review names or photos, price history (store your own), bag or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `query`; `market` `us`, `de` or `ca` ("market us is not offered: Space NK's US path shows UK prices in GBP, not US prices."); `min_price` or `max_price` ("A price filter is not offered: Space NK's site ignores it. Use sort price_low_to_high or price_high_to_low."); `brand` on `/brand`; more than 10 brands, or brands joined by `|`; a `product_id` that is not a Space NK id; `/reviews` with a shade or size id ("product_id must be the product id ... starting with M"), with `skin_type`, or past 10,000 reviews; `/stores` without a postcode or point, with both, with a postcode that is not a full UK postcode, or with a market other than uk; `/offers` with `nl` or `au`. `/stores` with a product Space NK does not sell is also a `400` ("Space NK could not look up stores for product ... near this location.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged (1 credit): "Space NK has no category <id> (category ids look like black-friday, skincare-treatment-serum, makeup-complexion-foundation).", "Space NK has no brand <id> (send brands[].id from the brands endpoint, e.g. medik8 or Charlotte Tilbury).", "Space NK has no product <id>.". Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api).
- `502` means Space NK data was temporarily unavailable ("Space NK is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds. An id Space NK does not answer for is also an uncharged `502` after up to about a minute ("Space NK did not return product <id>. Check product_id ...; if it is right, try again."): check the id before retrying.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- `/reviews` with `total` 0 is a `200`: the product has no reviews (or none with these stars or text), or the id is not a Space NK product.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: results } = await scavio.spacenk.search({ query: "vitamin c", brand: "Medik8" });
const { data: product } = await scavio.spacenk.product({ product_id: "MUK200057800", market: "au" });
const { data: reviews } = await scavio.spacenk.reviews({ product_id: "MUK200057800", stars: [1, 2] });
const { data: offers } = await scavio.spacenk.offers({ market: "uk" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.spacenk.search(...)`, `category`, `brand`, `brands`, `product`, `reviews`, `suggestions`, `stores` and `offers`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_spacenk`, `get_spacenk_category`, `get_spacenk_brand`, `get_spacenk_brands`, `get_spacenk_product`, `get_spacenk_reviews`, `get_spacenk_suggestions`, `get_spacenk_stores` and `get_spacenk_offers`. Space NK is opt-in: add `spacenk` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,spacenk"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/spacenk-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [category](https://scavio.dev/docs/spacenk-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [brand](https://scavio.dev/docs/spacenk-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [brands](https://scavio.dev/docs/spacenk-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [product](https://scavio.dev/docs/spacenk-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [reviews](https://scavio.dev/docs/spacenk-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [suggestions](https://scavio.dev/docs/spacenk-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [stores](https://scavio.dev/docs/spacenk-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api), [offers](https://scavio.dev/docs/spacenk-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api). Overview: [Space NK API](https://scavio.dev/spacenk-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=space-nk-api).
