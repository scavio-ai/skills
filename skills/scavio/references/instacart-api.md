# Instacart API - Grocery Prices by Store and ZIP, Price Compare

Read Instacart (instacart.com, the US and Canada grocery delivery and pickup marketplace; instacart.ca for Canada): every store serving a ZIP, search inside one store, one query across up to 10 stores, one product at one store, the same product priced at every store delivering to a ZIP, a store's departments and aisles, an aisle or collection, the store's sale items, its pickup locations, search suggestions and customer reviews. All 11 endpoints return structured JSON at 1 credit per call (search 3, cross-search 3-4).

**The job this skill is for: Instacart prices by store at a ZIP.** One product or a basket priced at every store delivering to a ZIP, each with that store's pricing label, and Instacart's delivery price next to the same store's in-store price where Instacart shows both. On 2026-11-23 at ZIP 10001 (New York), Instacart priced fairlife 2% Reduced-Fat Ultra-Filtered Milk (52 fl oz, product id `16408559`) at 153 of the 306 stores delivering there, from $5.49 (Key Food on sale from $7.99, Walgreens) to $12.59 (Grace's Marketplace); Wegmans read $6.39 with Wegmans' own label as Instacart showed it: "Our online prices remain about 15% above in-store prices."

Nine limits shape every answer, so say them plainly:
- **1 credit per call; search 3, cross-search 3-4.** search reserves 3 and charges 2 when the page sits inside the first answer Instacart gives (English); cross-search charges 3 for up to 5 stores and 4 for 6 to 10. `credits_used` reports the actual charge. A not-found (an unknown product id, a retailer not serving the ZIP, an unknown category slug, a ZIP Instacart does not recognise) is a `404` and is charged. A refused input (`400`) and an upstream failure (`502`, `503`) are not charged.
- **`zip` is required on every endpoint but reviews.** A 5-digit US ZIP (`10001`) or, with `country` `ca`, a Canadian postal code with or without the space (`M5V 2T6`, `H2X1Y4`). A ZIP with no Instacart service area answers `200` with an empty list and a note (on `/product`, a charged `404`).
- **Every price is for one store, one ZIP and one service type.** `priced_for` {`retailer_id`, `retailer_slug`, `retailer_name`, `service_type`, `shop_id`, `retailer_location_id`, `zip`, `pricing_label`} names it. Retailers set their own prices on Instacart, and the Instacart Help Center says some set prices that are different from their in-store prices. Report "$6.39 at Wegmans for delivery to 10001 on 2026-11-23", never a national price and never the store's shelf price.
- **`retailer` comes from `/retailers`.** A slug (`retailers[].slug`: `wegmans`, `jewel-osco`, `costco`) or id (`retailer_id`: `231`) of a store that serves that ZIP; anything else is a charged `404`.
- **`service_type` is `delivery` (default), `pickup` or `instore`.** `instore` returns Instacart's in-store prices for that store where Instacart shows them; a store without them is a charged `404`, and so is `pickup` at a store with no pickup at the ZIP. `/retailers` lists each store's `services`, `pickup_available` and `instore_available`: pick from those.
- **price-compare is the same product at every store, delivery prices.** One `product_id` (shared by every store on Instacart) priced at each store delivering to the ZIP, sorted low to high. It has no unit price and no stock: `/product` gives them per store.
- **cross-search is US only and prices at most 10 stores.** One query, `max_retailers` 1-10 stores in Instacart's order, `items_per_retailer` 1-20 products each, for delivery.
- **Two markets.** `country` `us` (instacart.com, USD, default) and `ca` (instacart.ca, CAD). `language` `fr` (Canada only) returns French names, aisles and price text as Instacart shows them in Quebec. Canada serves every endpoint except cross-search and reviews; suggestions are English only.
- **Not in any answer:** delivery and service fee amounts and order minimums as numbers (Instacart shows them at checkout), coupons, Instacart+ member prices, account, cart or order data, and price history (poll and store it). Reviews are US only and carry no reviewer names.

Instacart's own developer offering is not a price feed. Its Developer Platform is free with review but returns shopping links and a list of nearby retailers, not item prices; its Connect and Catalog APIs are for retailers managing their own storefronts. Item prices are shown on instacart.com per retailer and per store; this skill reads those public pages with one Scavio key.

Instacart works with more than 2,200 retail banners representing nearly 100,000 stores (Instacart, Oct 29, 2026) and handled 338.8 million orders worth $37.2 billion in gross transaction value in 2025 (Maplebear 10-K). On Oct 29, 2026 DoorDash agreed to acquire Instacart for $65.00 a share, about $17 billion in equity value; the companies expect the deal to close in the end of 2027 or the first half of 2028, subject to approvals (8-K). Quote these with their source, never from the samples.

See also: for shelf prices straight from a store, set beside an Instacart price, use `kroger-grocery-data`, `costco-product-data`, `aldi-grocery-data`, `whole-foods-grocery-data` or `heb-grocery-data`; for the Publix weekly ad and BOGO list use `publix-api`; for prices across online merchants use `google-shopping-api`; for Walmart grocery use `walmart-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price one grocery product at every store delivering to a US ZIP or Canadian postal code on Instacart, cheapest first
- Compare an Instacart delivery price with the same store's in-store price on Instacart, or measure a store's Instacart markup on given products
- List the stores on Instacart at a ZIP, with delivery and pickup ETA, Instacart's No markups label, EBT and services
- Search one store on Instacart by keyword, sorted by price, filtered to sale items or a brand, with unit prices and stock labels
- Run one search across several Instacart stores at a ZIP (a basket item at up to 10 stores)
- Read one product at one store: ingredients, allergen warnings, key nutrients, price and rating
- List a store's departments and aisles, or the products of one aisle or collection (for example Thanksgiving)
- Read a store's sale items on Instacart: sale price with the regular price, multi-buy offers
- Find a retailer's pickup locations near a ZIP with 7 days of hours
- Read Instacart customer reviews of a product (US), or Instacart's search suggestions
- Read Instacart Canada in CAD, in English or French

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit; search costs 3 (2 when the page sits inside Instacart's first answer) and cross-search 3 or 4.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, categories took 1-2 seconds, reviews, suggestions, category, deals, product and price-compare 2-4, cross-search 5, retailers and stores about 10, and search 12-13. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/instacart/retailers` | Every store serving the ZIP: slug and id (the `retailer` input), type, services, delivery and pickup ETA, `no_markups`, `accepts_ebt`, store labels | us, ca | 1 |
| `POST /api/v1/instacart/search` | One store at the ZIP: matching products with prices, `priced_for`, total and pages, brand filters; sort, on sale, brand, page, service type | us, ca | 3 (2 when the page sits in the first answer) |
| `POST /api/v1/instacart/cross-search` | One query across up to 10 stores delivering to a US ZIP, each with its first matching products priced | us only | 3 (1-5 stores), 4 (6-10) |
| `POST /api/v1/instacart/product` | One product at one store: ingredients, directions, warnings, key nutrients, images, the store's price block, rating summary | us, ca | 1 |
| `POST /api/v1/instacart/price-compare` | The same product priced at every store delivering to the ZIP, low to high, with sale and regular price and `no_markups` | us, ca | 1 |
| `POST /api/v1/instacart/categories` | One store's department and aisle tree (and collections such as Thanksgiving) with the slugs category takes | us, ca | 1 |
| `POST /api/v1/instacart/category` | The products of one department, aisle or collection of a store, paged, with `priced_for` | us, ca | 1 |
| `POST /api/v1/instacart/deals` | The store's Sales collection: sale price with the regular price, multi-buy offers; paged | us, ca | 1 |
| `POST /api/v1/instacart/stores` | One retailer's pickup locations near the ZIP, nearest first, with 7 days of hours for the 5 nearest | us, ca | 1 |
| `POST /api/v1/instacart/suggestions` | Instacart's suggestions for a partial query, for one store or every store at the ZIP | us, ca (English) | 1 |
| `POST /api/v1/instacart/reviews` | One product's customer reviews, 15 a page, with the rating summary on page 1, source and incentivized flag | us only | 1 |

## Markets

| `country` | Site | Language, currency | Endpoints |
|---|---|---|---|
| `us` (default) | www.instacart.com | English, USD | all 11 |
| `ca` | www.instacart.ca | English (default) or French (`language` `fr`), CAD | all but `/cross-search` and `/reviews`; `/suggestions` in English only |

- Every answer echoes `country`, `language`, `currency`, `zip` and `place` (Instacart's name for the ZIP, e.g. "New York, NY, USA"). A `country` outside us and ca, a market an endpoint does not serve, or `language` `fr` with `us` (or on suggestions) is a `400`, not charged.
- With `language` `fr`, names, aisles, deal badges, unit prices, `price_text` and the pricing label come back in French as Instacart shows them (`"price_text": "4,99 $"`, `"deal": "12 % de réduction"`); `price` stays a number (`4.99`). Translate for the user, never alter the values.
- In Canada, price-compare prices one product at every store serving a postal code and search searches one store; there is no cross-store search.

## Prices, pricing labels and service types

Every priced item (search, cross-search, product `item`, category, deals) carries:

| Field | Meaning |
|---|---|
| `price` / `price_text` | Instacart's price at the `priced_for` store, ZIP and service type; `price_text` as Instacart writes it |
| `was_price` | The regular price Instacart shows next to a sale price, or `null` |
| `discount_percent` | Computed by Scavio from `was_price`; `null` without one |
| `deal` / `promotions` | Instacart's offer badge and promotion texts ("15% off", "Buy 2, get 3 free", "Spend $18, save $2.50") |
| `unit_price` | As Instacart shows it ("$0.25/oz", "About $1.98 each", "0,25 $/100ml") |
| `loyalty_price` / `loyalty_label` | A loyalty-card price and its label, as Instacart shows it, or `null` |
| `in_stock`, `stock_level`, `stock_label` | Instacart's stock state (`inStock`, `highlyInStock`, `lowStock`) and label ("Many in stock", "Out of stock") |
| `dietary` | Instacart's dietary labels ("Organic", "Gluten-free", "Lactose-free") |
| `max_quantity` | The most Instacart lets one order add |

- **`pricing_label`** is the retailer's pricing statement as Instacart shows it under the store's logo, and it is the first thing to quote next to a price. Captured 2026-11-23: Jewel-Osco "Jewel-Osco sets the price of items on the Instacart marketplace. Item prices may vary from in-store prices in your area. Prices may be higher than in-store prices to cover the cost of personal shopping."; Wegmans "Our online prices remain about 15% above in-store prices. This includes our costs of shopping your order. There is also a $10 order minimum." (plus Instacart's charges text); Metro in Montreal, in French, that item prices are generally the same as in-store prices in your area. A Costco label reads "Prices are higher than your local warehouse." The label can mention fees or a minimum in words; Scavio returns no fee amounts.
- **`no_markups`** (retailers, cross-search, price-compare) marks the stores Instacart labels "No markups". At 10001, 83 of the 315 stores carried it; in the fairlife price-compare, 30 of the 153.
- **`service_type`**: `delivery` (default), `pickup` or `instore`. `instore` reads Instacart's in-store prices for that store and the in-store pricing statement. To put a delivery price next to an in-store price, call the same `product_id`, `retailer` and `zip` twice, once per service type, the same day.
- **Markup** is only ever a measured difference between two prices for the same product, store, ZIP and day: Instacart delivery against Instacart in-store, or against the store's own shelf price from a direct Scavio route (Kroger, Costco, ALDI, Whole Foods, H-E-B) when product and size match. Report the numbers and the date; never a reason, and never a markup for a store you did not measure.
- Fees and minimums: Instacart's Help Center says "The delivery fee varies based on the retailer, delivery window, and order total". Compare item prices; mention fees only in Instacart's words.
- Prices are what a signed-out shopper sees: no Instacart+ membership, no linked store membership, no coupons. Instacart ended its item price tests in December 2025 (Instacart's Pricing Principles, Jul 22, 2026); describe two prices that differ by store, ZIP or service type, never as a test or as personal pricing.

## Workflow

1. **Stores at the ZIP:** `/retailers` with `zip`. Keep `slug` (or `retailer_id`) for the stores you want; check `delivery_available`, `pickup_available`, `instore_available`.
2. **Find the product:** `/search` with `query`, `retailer` and `zip`. Keep `items[].product_id`: it is the same at every store on Instacart.
3. **Every store's price:** `/price-compare` with `product_id` and `zip` (1 credit for every store delivering there). Compare `size` first: two stores can list different sizes under similar names, but a `product_id` is one product.
4. **Detail and unit price at one store:** `/product` with `product_id`, `retailer`, `zip`.
5. **Delivery vs in-store:** `/product` (or `/search`) twice for the same store, `service_type` `delivery` then `instore`; quote both `pricing_label`s.
6. **A basket at several stores (US):** `/cross-search` per basket item with `max_retailers` up to 10, or `/price-compare` per product id once you have the ids.
7. **Browse:** `/categories` for slugs, then `/category` with `category` (`produce`, `fresh-fruits`, a collection slug such as `n-thanksgiving-79335`); `/deals` for the store's sale items.
8. **Pickup:** `/stores` with `retailer` and `zip` for locations and hours.
9. **Watching prices:** there is no history. Poll the same product ids at the same stores and ZIP on a schedule and store each answer with its `fetched_at` and `priced_for`; that stored series is the history.

## Parameters

### Retailers (`/retailers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP (`10001`) or, with `country` `ca`, a Canadian postal code (`M5V 2T6`, `M5V2T6`) |
| `country` | string | `us` | `us` or `ca` |
| `language` | string | `en` | `en`, or `fr` with `ca` |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-200 chars |
| `retailer` | string or integer | required | A slug or id from `/retailers` serving the ZIP (`jewel-osco`, `10`) |
| `zip` / `country` / `language` | | | As in retailers |
| `service_type` | string | `delivery` | `delivery`, `pickup` or `instore` |
| `sort` | string | `best_match` | `best_match` (Instacart's order), `price_asc`, `price_desc` |
| `on_sale` | boolean | false | Only the products Instacart marks on sale at this store |
| `brand_id` | string or integer | none | A `brand_filters[].brand_id` from an earlier search (`18514` = Chobani) |
| `page` | integer | 1 | 1-100; `total_pages` says how deep the list goes |
| `limit` | integer | 30 | Products per page, 1-60 |

### Cross-search (`/cross-search`, US)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-200 chars |
| `zip` | string | required | A US ZIP |
| `max_retailers` | integer | 5 | Stores to price, 1-10, in Instacart's order (3 credits up to 5, 4 above) |
| `items_per_retailer` | integer | 5 | Products per store, 1-20 |
| `country` | string | `us` | `us` only; `ca` is a `400` |

### Product (`/product`) and price-compare (`/price-compare`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string or integer | required | An Instacart product id (`items[].product_id`: `16408559`), an item id (`items_2683-16408559`) or an Instacart product link |
| `retailer` | string or integer | product: required unless the link names the store | A slug or id from `/retailers`. price-compare takes no retailer |
| `zip` / `country` / `language` | | | As in retailers. A link carries its market: send `country` only if it agrees |
| `service_type` | string | `delivery` | Product only: `delivery`, `pickup` or `instore`. price-compare is delivery |

### Categories (`/categories`), category (`/category`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `retailer` | string or integer | required | A slug or id from `/retailers` |
| `zip` / `country` / `language` | | | As in retailers |
| `category` | string | category: required | A slug from `/categories` (`categories[].slug` or `categories[].aisles[].slug`: `produce`, `fresh-fruits`) |
| `service_type` | string | `delivery` | Category and deals: `delivery`, `pickup` or `instore` |
| `page` / `limit` | integer | 1 / 30 | Category and deals: as in search |

### Stores (`/stores`), suggestions (`/suggestions`), reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `retailer` | string or integer | stores: required; suggestions: optional | Stores: whose pickup locations. Suggestions: that store's suggestions; without it, across every store serving the ZIP |
| `zip` / `country` / `language` | | | Stores and suggestions: as in retailers (suggestions `en` only) |
| `limit` | integer | 10 | Stores: 1-50 locations; hours come for the 5 nearest |
| `query` | string | suggestions: required | What the shopper has typed so far (`eg`), 1-100 chars |
| `product_id` | string or integer | reviews: required | As in product. Reviews take no `zip` |
| `page` | integer | 1 | Reviews: 15 a page, 1-100 |

## Examples

### Every store's price for one product

```bash
curl -X POST https://api.scavio.dev/api/v1/instacart/price-compare \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "16408559", "zip": "10001"}'
```

Captured `data` (2026-11-23, 1 credit; 3 of 153 rows shown, then the last):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "zip": "10001",
  "place": "New York, NY, USA",
  "product_id": "16408559",
  "service_type": "delivery",
  "stores_checked": 306,
  "count": 153,
  "prices": [
    {
      "retailer_id": "39",
      "retailer_slug": "key-food",
      "retailer_name": "Key Food",
      "shop_id": "595543",
      "retailer_location_id": "1962",
      "price": 5.49,
      "price_text": "$5.49",
      "currency": "USD",
      "was_price": 7.99,
      "discount_percent": 31,
      "price_reduction": 2.5,
      "on_sale": true,
      "no_markups": false,
      "url": "https://www.instacart.com/store/key-food/products/16408559"
    },
    {
      "retailer_id": "110",
      "retailer_slug": "vitelios-marketplace",
      "retailer_name": "Vitelio's Marketplace",
      "shop_id": "23979",
      "retailer_location_id": "31904",
      "price": 5.49,
      "price_text": "$5.49",
      "currency": "USD",
      "was_price": 7.99,
      "discount_percent": 31,
      "price_reduction": 2.5,
      "on_sale": true,
      "no_markups": true,
      "url": "https://www.instacart.com/store/vitelios-marketplace/products/16408559"
    },
    {
      "retailer_id": "151",
      "retailer_slug": "food-universe",
      "retailer_name": "Food Universe",
      "shop_id": "268029",
      "retailer_location_id": "1957",
      "price": 5.49,
      "price_text": "$5.49",
      "currency": "USD",
      "was_price": 8.79,
      "discount_percent": 38,
      "price_reduction": 3.3,
      "on_sale": true,
      "no_markups": false,
      "url": "https://www.instacart.com/store/food-universe/products/16408559"
    },
    {
      "retailer_id": "3540",
      "retailer_slug": "graces-marketplace-nyc",
      "retailer_name": "Grace's Marketplace",
      "shop_id": "524565",
      "retailer_location_id": "370198",
      "price": 12.59,
      "price_text": "$12.59",
      "currency": "USD",
      "was_price": null,
      "discount_percent": null,
      "price_reduction": null,
      "on_sale": false,
      "no_markups": false,
      "url": "https://www.instacart.com/store/graces-marketplace-nyc/products/16408559"
    }
  ],
  "note": "The same Instacart product priced at each store delivering to this ZIP, as Instacart shows it for delivery, sorted by price (low to high). Retailers set their Instacart prices, which can differ from their in-store prices; no_markups marks the stores Instacart labels 'No markups'. was_price is the regular price Instacart shows next to a sale price; discount_percent is computed by Scavio from it. Fees and coupons are not included."
}
```

`stores_checked` is the stores delivering to the ZIP; `count` is how many price the product (153 of 306 here). In the same answer Walgreens read $5.49, Target $5.99, BJ's and Wegmans $6.39, Food Bazaar $6.99 (on sale), Fairway $7.20, CVS $7.49 and ShopRite $7.71; 42 rows were on sale. A product priced nowhere at the ZIP answers `200` with an empty list and a note.

### Search one store

```bash
curl -X POST https://api.scavio.dev/api/v1/instacart/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "yogurt", "retailer": "jewel-osco", "zip": "60540", "limit": 10}'
```

Captured `data` (2026-11-23; 2 of 10 items and 3 of the brand filters shown, `image` dropped):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "zip": "60540",
  "place": "Naperville, IL, USA",
  "query": "yogurt",
  "sort": "best_match",
  "on_sale": false,
  "brand_id": null,
  "page": 1,
  "limit": 10,
  "priced_for": {
    "retailer_id": "10",
    "retailer_slug": "jewel-osco",
    "retailer_name": "Jewel-Osco",
    "service_type": "delivery",
    "shop_id": "1745",
    "retailer_location_id": "2683",
    "zip": "60540",
    "pricing_label": "Jewel-Osco sets the price of items on the Instacart marketplace. Item prices may vary from in-store prices in your area. Prices may be higher than in-store prices to cover the cost of personal shopping."
  },
  "total": 311,
  "total_pages": 32,
  "has_more": true,
  "count": 10,
  "items": [
    {
      "product_id": "54189",
      "item_id": "items_2683-54189",
      "name": "Stonyfield Organic Whole Milk Probiotic Yogurt, Plain, 32 oz. – Multi-Serving Yogurt; Supports Immunity & Digestive Health",
      "brand": "stonyfield organic",
      "brand_id": "45402",
      "size": "32 oz",
      "price": 7.99,
      "price_text": "$7.99",
      "currency": "USD",
      "was_price": null,
      "discount_percent": null,
      "deal": "Spend $18, save $2.50",
      "promotions": ["Spend $18, save $2.50"],
      "unit_price": "$0.25/oz",
      "loyalty_price": null,
      "loyalty_label": null,
      "in_stock": true,
      "stock_level": "inStock",
      "stock_label": null,
      "dietary": ["Organic", "Non-GMO", "Gluten-free"],
      "url": "https://www.instacart.com/store/jewel-osco/products/54189-stonyfield-organic-plain-whole-milk-probiotic-yogurt-32-oz",
      "max_quantity": 99
    },
    {
      "product_id": "17830663",
      "item_id": "items_2683-17830663",
      "name": "Lucerne Blended Plain Yogurt",
      "brand": "lucerne",
      "brand_id": "48795",
      "size": "32 oz",
      "price": 3.99,
      "price_text": "$3.99",
      "currency": "USD",
      "was_price": 4.69,
      "discount_percent": 15,
      "deal": "15% off",
      "promotions": [],
      "unit_price": "$0.12/oz",
      "loyalty_price": null,
      "loyalty_label": null,
      "in_stock": true,
      "stock_level": "inStock",
      "stock_label": null,
      "dietary": [],
      "url": "https://www.instacart.com/store/jewel-osco/products/17830663-lucern-dairy-farms-yogurt-plain-32-oz",
      "max_quantity": 99
    }
  ],
  "brand_filters": [
    { "brand_id": "18514", "name": "Chobani" },
    { "brand_id": "3402", "name": "Yoplait" },
    { "brand_id": "26658", "name": "Oikos" }
  ],
  "note": "Prices as Instacart shows them for this store, ZIP and service type (priced_for). Retailers set their Instacart prices, which can differ from the shelf price in the store; service_type instore shows Instacart's in-store prices. Delivery and service fees, order minimums and coupons are not included."
}
```

311 matches in 32 pages of 10. `brand_filters[].brand_id` goes back in as `brand_id`; `sort` `price_asc` with `on_sale` true lists the cheapest sale items first. The same store and ZIP with `service_type` `instore` returns Instacart's in-store prices for that store, where Instacart shows them.

### Canada in French

```bash
curl -X POST https://api.scavio.dev/api/v1/instacart/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "lait", "retailer": "metro", "zip": "H2X1Y4", "country": "ca", "language": "fr", "limit": 10}'
```

Captured `data` (2026-11-23; 1 of 10 items shown, `image` and the brand filters dropped, the pricing label cut):

```json
{
  "country": "ca",
  "language": "fr",
  "currency": "CAD",
  "zip": "H2X1Y4",
  "place": "Montreal, QC, Canada",
  "query": "lait",
  "priced_for": {
    "retailer_id": "2138",
    "retailer_slug": "metro",
    "retailer_name": "Metro",
    "service_type": "delivery",
    "shop_id": "450593",
    "retailer_location_id": "143534",
    "zip": "H2X1Y4",
    "pricing_label": "Metro fixe les prix des articles sur le marché Instacart. Les prix des articles sont généralement les mêmes que les prix en magasin dans votre région. ..."
  },
  "total": 139,
  "total_pages": 14,
  "has_more": true,
  "count": 10,
  "items": [
    {
      "product_id": "18497458",
      "item_id": "items_143534-18497458",
      "name": "Natrel finement filtré Lait Homogénéisé",
      "brand": "natrel finement filtré",
      "brand_id": "1122467",
      "size": "2 l",
      "price": 4.99,
      "price_text": "4,99 $",
      "currency": "CAD",
      "was_price": 5.69,
      "discount_percent": 12,
      "deal": "12 % de réduction",
      "promotions": [],
      "unit_price": "0,25 $/100ml",
      "loyalty_price": null,
      "loyalty_label": null,
      "in_stock": true,
      "stock_level": "inStock",
      "stock_label": null,
      "dietary": [],
      "url": "https://www.instacart.ca/store/metro/products/18497458-natrel-fine-filtered-homogenized-milk-2l",
      "max_quantity": 500
    }
  ]
}
```

(`sort`, `on_sale`, `brand_id`, `page`, `limit` and `note` dropped in this excerpt.) Natrel fine-filtered homogenized milk, 2 L, CAD 4.99 on sale from CAD 5.69 at Metro for delivery to Montreal H2X 1Y4; Metro's label says item prices are generally the same as in-store prices in your area. Instacart's best match put a peach drink first in this answer: read names, not positions.

### Product at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/instacart/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "16408559", "retailer": "wegmans", "zip": "10001"}'
```

Captured `data` (2026-11-23, 1 credit; `description`, `sections`, `images`, `note` and the item's `image` dropped, the pricing label cut):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "zip": "10001",
  "place": "New York, NY, USA",
  "product_id": "16408559",
  "priced_for": {
    "retailer_id": "231",
    "retailer_slug": "wegmans",
    "retailer_name": "Wegmans",
    "service_type": "delivery",
    "shop_id": "366100",
    "retailer_location_id": "162737",
    "zip": "10001",
    "pricing_label": "We keep our prices consistently low, every day, so you can save on the items your family uses most. Our online prices remain about 15% above in-store prices. This includes our costs of shopping your order. There is also a $10 order minimum. ..."
  },
  "available_at_store": true,
  "name": "Milk fairlife 2% Reduced-Fat Ultra-Filtered Milk Bottle",
  "size": "52 fl oz",
  "ingredients": "REDUCED FAT ULTRA-FILTERED MILK, LACTASE ENZYME, VITAMIN A PALMITATE, VITAMIN D3.",
  "directions": "Keep refrigerated. Consume within 14 days of opening.",
  "warnings": "Contains: milk.",
  "key_nutrients": [
    { "name": "Protein", "value": "13", "unit": "g" },
    { "name": "Sat Fat", "value": "3", "unit": "g" },
    { "name": "Sugar", "value": "6", "unit": "g" },
    { "name": "Sodium", "value": "120", "unit": "mg" },
    { "name": "Carbs", "value": "6", "unit": "g" }
  ],
  "brand": "fairlife",
  "item": {
    "product_id": "16408559",
    "item_id": "items_162737-16408559",
    "name": "fairlife 2% Reduced-Fat Ultra-Filtered Milk Bottle",
    "brand": "fairlife",
    "brand_id": "77065",
    "size": "52 fl oz",
    "price": 6.39,
    "price_text": "$6.39",
    "currency": "USD",
    "was_price": null,
    "discount_percent": null,
    "deal": null,
    "promotions": [],
    "unit_price": "$0.12/fl oz",
    "loyalty_price": null,
    "loyalty_label": null,
    "in_stock": true,
    "stock_level": "highlyInStock",
    "stock_label": "Many in stock",
    "dietary": ["2%", "Lactose-free"],
    "url": "https://www.instacart.com/store/wegmans/products/16408559-fairlife-2-reduced-fat-ultrafiltered-milk-lactose-free-52-fl-oz",
    "max_quantity": 20
  },
  "rating": {
    "average_rating": 4.8,
    "ratings_count": 2204,
    "distribution": [
      { "stars": 5, "count": 1851, "percent": 84 },
      { "stars": 4, "count": 246, "percent": 11 },
      { "stars": 3, "count": 47, "percent": 2 },
      { "stars": 2, "count": 23, "percent": 1 },
      { "stars": 1, "count": 37, "percent": 2 }
    ]
  },
  "url": "https://www.instacart.com/store/wegmans/products/16408559-fairlife-2-reduced-fat-ultrafiltered-milk-lactose-free-52-fl-oz"
}
```

$6.39 at Wegmans for delivery to 10001, the same price price-compare showed for Wegmans. `key_nutrients` are the nutrients Instacart lists, not a full nutrition panel; `warnings` carries allergens as given. `item` is `null` when Instacart shows the product but no price at that store. An id Instacart does not know is a charged `404`.

### Reviews (US)

```bash
curl -X POST https://api.scavio.dev/api/v1/instacart/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "16408559"}'
```

Captured `data` (2026-11-23, 1 credit; 1 of 15 reviews shown, the distribution and `note` dropped):

```json
{
  "country": "us",
  "product_id": "16408559",
  "page": 1,
  "page_size": 15,
  "order": "mostRelevant",
  "has_more": true,
  "rating": { "average_rating": 4.8, "ratings_count": 2204 },
  "count": 15,
  "reviews": [
    {
      "review_id": "2",
      "rating": 5,
      "title": "Love this milk!",
      "text": "I love this milk! I put ice in it and just love it. I drink a few gallons a month. I’ll have it with breakfast, lunch and dinner. I have always loved milk but it hurt my stomach but this milk does not. It is a staple in my house hold.",
      "reviewed_on": "October 30, 2026",
      "date": "2026-10-30",
      "source": "Fairlife",
      "incentivized": false
    }
  ]
}
```

`source` is the brand or site Instacart names for the review (on this page Fairlife, influenster.com and Meijer); `incentivized` marks the reviews Instacart notes were written as part of a promotion (7 of the 15 on page 1). Say how many are incentivized when you summarize. No reviewer name or identity is returned. Reviews are a product's, not a store's.

### Retailers, cross-search, categories, category, deals, stores and suggestions

- `/retailers` with `{"zip": "10001"}`: 315 stores, 83 with `no_markups` true, for example Wegmans (`wegmans`, `retailer_id` 231, delivery and pickup, "Delivery by 10:45pm", `accepts_ebt` true), Costco (`costco`, 5, delivery only), Target (`target-corp`, 648), Food Bazaar (`no_markups` true), CVS, Walgreens, Best Buy and The Home Depot. Instacart lists more than grocers: filter on `retailer_type` ("Grocery - Traditional", "Club/Warehouse Store", "Drugstore") or `categories` (`grocery`). `delivery_eta` and `pickup_eta` are Instacart's text; delivery fees and order minimums are not in the answer.
- `/cross-search` with `{"query": "milk", "zip": "10001", "max_retailers": 3}`: `retailers_matched` 50, three stores priced (Fairway, Food Bazaar, Wegmans) with 5 items each; Food Bazaar's first, Organic Valley Whole Milk 64 fl oz, read $5.99 against $8.49 (`discount_percent` 29); Fairway's first read `in_stock` false, "Out of stock". `matches` is how many items Instacart returned for that store (at most 20). Each group is one store's best matches, not the same product: use price-compare for one product at every store.
- `/categories` with `{"retailer": "wegmans", "zip": "10001"}`: 32 departments and collections with 241 aisles; the first a "Thanksgiving" collection (`n-thanksgiving-79335`), then Produce (`produce`: Fresh Fruits `fresh-fruits`, Fresh Vegetables, Herbs, ...).
- `/category` with `{"category": "produce", "retailer": "wegmans", "zip": "10001", "limit": 10}`: 469 products in 47 pages; Wegmans Organic Bananas, Bunch, $1.98 "About $1.98 each" (`size` "per lb").
- `/deals` with `{"retailer": "jewel-osco", "zip": "60540", "limit": 10}`: Jewel-Osco's Sales collection, 951 items; Chips Ahoy! and Oreo cookies at $6.99 with "Buy 2, get 3 free". Multi-buy offers come as `deal` text; `was_price` appears on straight price cuts. Coupons are not included.
- `/stores` with `{"retailer": "jewel-osco", "zip": "60540", "limit": 5}`: `total` 171, the nearest "Jewel-Osco - 1111" at 1227 S Naper Blvd, "Store 1.3mi away", with 7 dated days of hours (Thanksgiving 2026-11-26 "Open 6am - 4pm"). `phone` can be `null`. A retailer with no pickup near the ZIP answers `200` with an empty list and a note.
- `/suggestions` with `{"query": "eg", "retailer": "jewel-osco", "zip": "60540"}`: 10 suggestions, 9 search terms (eggs, egg noodles, eggplant, eggo, ...) and the collection "Dairy & Eggs". Without `retailer`, `scope` is `all_retailers`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def instacart(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/instacart/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. One product at every store delivering to a ZIP, cheapest first (1 credit)
res = instacart("price-compare", {"product_id": "16408559", "zip": "10001"})
d = res["data"]
print(res["fetched_at"], d["place"], "-", d["count"], "of", d["stores_checked"], "stores price it")
for p in d["prices"][:10]:
    print(p["retailer_name"], p["price"], "was", p["was_price"], "no markups" if p["no_markups"] else "")

# 2. Delivery next to in-store at one store that shows in-store prices (1 credit each)
stores = instacart("retailers", {"zip": "10001"})["data"]["retailers"]
store = next(r for r in stores if r["instore_available"] and r["delivery_available"])
for mode in ("delivery", "instore"):
    try:
        prod = instacart("product", {"product_id": "16408559", "retailer": store["slug"], "zip": "10001", "service_type": mode})["data"]
    except requests.HTTPError as e:
        # 404 (charged): this store does not carry the product, or shows no price in this mode
        print(mode, e.response.status_code, e.response.json().get("error"))
        continue
    item = prod["item"] or {}
    print(store["name"], mode, item.get("price"), item.get("unit_price"), "|", prod["priced_for"]["pricing_label"])

# Prices are for one store, ZIP and service type (priced_for). Store each answer with
# fetched_at and priced_for and run this on a schedule: that stored series is your
# price history (Instacart shows only the current price).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country`, `language`, `currency`, `zip` and `place` (reviews: `country` only).

- **item** (search, cross-search, category, deals, product `item`) - `product_id` (the input of product, price-compare and reviews; the same at every store), `item_id` (`items_<retailer_location_id>-<product_id>`), `name`, `brand`, `brand_id`, `size`, `price`, `price_text`, `currency`, `was_price`, `discount_percent`, `deal`, `promotions`, `unit_price`, `loyalty_price`, `loyalty_label`, `in_stock`, `stock_level`, `stock_label`, `dietary`, `image`, `url`, `max_quantity`.
- **priced_for** (search, product, category, deals) - `retailer_id`, `retailer_slug`, `retailer_name`, `service_type`, `shop_id`, `retailer_location_id`, `zip`, `pricing_label` (`null` when it cannot be read).
- **retailers** - `count`, `no_markups_count`, `retailers[]` {`retailer_id`, `slug`, `name`, `retailer_type`, `categories`, `logo`, `services`, `delivery_available`, `pickup_available`, `instore_available`, `delivery_eta`, `pickup_eta`, `no_markups`, `accepts_ebt`, `store_labels`, `alcohol_allowed`, `delivery_shop_id`, `pickup_shop_id`, `retailer_location_id`, `url`}, `note`.
- **search** - `query`, `sort`, `on_sale`, `brand_id`, `page`, `limit`, `priced_for`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `brand_filters[]` {`brand_id`, `name`}, `note`.
- **cross-search** - `query`, `service_type`, `max_retailers`, `items_per_retailer`, `retailers_matched`, `count`, `groups[]` {`retailer_id`, `retailer_slug`, `retailer_name`, `shop_id`, `retailer_location_id`, `no_markups`, `matches`, `count`, `items[]`}, `note`.
- **product** - `product_id`, `priced_for`, `available_at_store`, `name`, `size`, `brand`, `description`, `ingredients`, `directions`, `warnings`, `sections[]` {`title`, `text`}, `key_nutrients[]` {`name`, `value`, `unit`}, `images`, `item` (or `null`), `rating` {`average_rating`, `ratings_count`, `distribution[]` {`stars`, `count`, `percent`}}, `url`, `note`.
- **price-compare** - `product_id`, `service_type` (`delivery`), `stores_checked`, `count`, `prices[]` {`retailer_id`, `retailer_slug`, `retailer_name`, `shop_id`, `retailer_location_id`, `price`, `price_text`, `currency`, `was_price`, `discount_percent`, `price_reduction`, `on_sale`, `no_markups`, `url`} low to high, `note`.
- **categories** - `retailer_id`, `retailer_slug`, `retailer_name`, `count`, `aisle_count`, `categories[]` {`id`, `name`, `slug` (the input of category), `type` (`department` or `collection`), `image`, `aisles[]` {`id`, `name`, `slug`}}.
- **category / deals** - `category` (deals: `dynamic_collection-sales`), `title`, `page`, `limit`, `priced_for`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `note`.
- **stores** - `retailer`, `retailer_id`, `retailer_name`, `retailer_slug`, `total`, `count`, `stores[]` {`retailer_location_id`, `name`, `address` {`street`, `line2`, `postal_code`}, `latitude`, `longitude`, `distance`, `distance_text`, `phone`, `hours[]` {`date`, `hours`} (or `null` past the 5 nearest)}, `note`.
- **suggestions** - `query`, `scope` (`retailer` or `all_retailers`), `retailer_id`, `retailer_slug`, `retailer_name`, `count`, `suggestions[]` {`type` (`search_term`, `collection` or `retailer`), `text`, `search_term`, `category`, `retailer`, `image`}.
- **reviews** - `product_id`, `page`, `page_size` (15), `order`, `has_more`, `rating` (page 1), `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `reviewed_on`, `date`, `source`, `incentivized`}, `note`.

## Guardrails

- Name it "Instacart (instacart.com, the US and Canada grocery delivery and pickup marketplace)" on first mention.
- Prices: quote `price` with the `priced_for` store, the ZIP, the service type and the `fetched_at` date, and the store's `pricing_label` when the reader compares prices. Never call an Instacart delivery price the store's shelf price, never call a price national, and never carry one ZIP's or store's price to another.
- Markups: only a measured difference between two prices for the same product, store, ZIP and day, with both numbers shown. No reasons or motives, no claim that Instacart prices are personal or tested.
- Comparisons: match `product_id` and `size`, not names. Cross-search groups are each store's own best matches, not one product.
- Fees and memberships: no fee amounts, order minimums, coupons or Instacart+ prices are returned; never estimate them. Quote fee wording only from a `pricing_label` or Instacart's Help Center.
- Stock: `in_stock` and `stock_label` are what Instacart showed at the moment of the call; Scavio makes no promise of their accuracy.
- Reviews: say which `source` they come from and how many are `incentivized`. No reviewer names or identities are returned; never try to identify a reviewer.
- French data: translate French names, aisles, deal badges and labels for the user and keep the original values in quotes and outputs.
- Not available: delivery and service fee amounts, order minimums, coupons, Instacart+ member prices, account, cart, order or checkout data, price history (poll and store), cross-search and reviews in Canada, French suggestions. This API cannot add to cart, order or buy.
- Terms: Scavio does not collect or store Instacart data: each call fetches the public Instacart page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Instacart's terms cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Instacart product photos, logos or reviewer details; link products by `url` instead.
- Never fabricate prices, pricing labels, stores, stock, hours, ratings or reviews. Only return what the API returned, with the `fetched_at` time, the `priced_for` store and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a missing or malformed `zip` (a Canadian postal code without `country` `ca`, or the reverse), a missing `retailer` or `query`, a `country` outside us and ca, `ca` on cross-search or reviews, `language` `fr` with `us` or on suggestions, an unknown `sort` or `service_type`, `page` outside 1-100, `limit` outside 1-60, `max_retailers` outside 1-10, `items_per_retailer` outside 1-20, a malformed `product_id`, `brand_id` or `category`, a product link whose market disagrees with `country`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Instacart lists no <retailer> store serving ZIP <zip>. /api/v1/instacart/retailers lists the retailers that do.", "Instacart has no product <id> at <store> (<service_type>, <zip>). Check the id with search.", "<store> has no category <slug> on Instacart. /api/v1/instacart/categories lists the slugs.", "Instacart shows no in-store prices for <store> at ZIP <zip>: send service_type delivery or pickup.", "<store> offers pickup only at ZIP <zip> on Instacart: send service_type pickup.", "<store> offers no pickup at ZIP <zip> on Instacart: send service_type delivery.", "Instacart shows no sales for <store> at <zip>.", "Instacart does not recognise ZIP <zip>." Take slugs, ids and category slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api).
- `502` means Instacart data was temporarily unavailable ("Instacart is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Instacart is busy ("Instacart is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- A `200` with an empty list and a `note` is an answer, not an error: no service area at the ZIP, no store delivering there right now, a product priced at no store, or no pickup location near the ZIP.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.77.0
npm install scavio@0.78.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: stores } = await scavio.instacart.retailers({ zip: "10001" });
const { data: found } = await scavio.instacart.search({ query: "yogurt", retailer: "jewel-osco", zip: "60540" });
const { data: across } = await scavio.instacart.crossSearch({ query: "milk", zip: "10001", max_retailers: 3 });
const { data: product } = await scavio.instacart.product({ product_id: "16408559", retailer: "wegmans", zip: "10001" });
const { data: compare } = await scavio.instacart.priceCompare({ product_id: "16408559", zip: "10001" });
const { data: tree } = await scavio.instacart.categories({ retailer: "wegmans", zip: "10001" });
const { data: produce } = await scavio.instacart.category({ category: "produce", retailer: "wegmans", zip: "10001" });
const { data: deals } = await scavio.instacart.deals({ retailer: "jewel-osco", zip: "60540" });
const { data: pickup } = await scavio.instacart.stores({ retailer: "jewel-osco", zip: "60540" });
const { data: typed } = await scavio.instacart.suggestions({ query: "eg", zip: "60540" });
const { data: reviews } = await scavio.instacart.reviews({ product_id: "16408559" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.instacart.retailers(...)`, `search`, `cross_search`, `product`, `price_compare`, `categories`, `category`, `deals`, `stores`, `suggestions` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `get_instacart_retailers`, `search_instacart`, `get_instacart_cross_search`, `get_instacart_product`, `get_instacart_price_compare`, `get_instacart_categories`, `get_instacart_category`, `get_instacart_deals`, `get_instacart_stores`, `get_instacart_suggestions` and `get_instacart_reviews`. Instacart is opt-in: add `instacart` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.77.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,instacart"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [retailers](https://scavio.dev/docs/instacart-retailers?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [search](https://scavio.dev/docs/instacart-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [cross-search](https://scavio.dev/docs/instacart-cross-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [product](https://scavio.dev/docs/instacart-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [price compare](https://scavio.dev/docs/instacart-price-compare?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [categories](https://scavio.dev/docs/instacart-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [category](https://scavio.dev/docs/instacart-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [deals](https://scavio.dev/docs/instacart-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [stores](https://scavio.dev/docs/instacart-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [suggestions](https://scavio.dev/docs/instacart-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api), [reviews](https://scavio.dev/docs/instacart-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api). Overview: [Instacart API](https://scavio.dev/instacart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api).
