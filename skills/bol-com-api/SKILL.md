---
name: bol-com-api
description: "bol.com API for bol.com competitor prices and marketplace data in the Netherlands and Belgium, in euros, on three storefronts: nl-nl (Dutch), be-nl (Dutch) and be-fr (French; bol's own texts in French, review topics in Dutch, review texts bol's translation). One product by bol product id, link or EAN / GTIN with the buy box (price, seller, reference price with its type: the supplier's recommended price or bol's most-shown price of the last 90 days, discount, shipping cost, delivery promise), the offer count, the cheapest new, fastest new and cheapest second-hand offers, refurbished offers by grade, specifications, category path, rating distribution, bol's AI review topics and the first 10 reviews (pooled across the product family, no reviewer names); the 10 lowest-priced offers on one product with price, condition (refurbished grade, second-hand state), shipping cost, delivery date and the seller's rating out of 10, plus counts by condition for all its offers, for price comparison and price monitoring; keyword search (pages 1 to 10, sorted by relevance, popularity, price, rating or most wished for, filtered by price, condition, deals, Select deals, delivery, brand and any facet, sponsored items flagged); category, brand, seller and promotion (Black Friday list, day deal) listings, pages 1 to 500, sorted by popularity, price, rating or most wished for; a seller's public profile with rating out of 10, up to four sub-ratings, positive percent, review counts, product count and the EU trader data bol publishes (company, city, country, registration and VAT number, no street address); today's deals. Product, EAN, category, seller and offer ids are shared across storefronts; prices and offers can differ between the Netherlands and Belgium. 9 endpoints, 2 credits each, product by EAN 4. No price history or 30-day lowest price, no review paging beyond the first 10, no search suggestions. bol's own APIs need an account: the Retailer API is for registered bol sellers, the Marketing Catalog API for registered affiliates."
version: 1.0.0
tags: bol, bol-com, bolcom, bol-com-api, bolcom-api, bol-com-prices, bol-com-price-monitoring, bol-com-competitor-prices, bol-com-buy-box, bol-com-offers, bol-com-sellers, bol-com-seller-ratings, bol-com-reviews, bol-com-ean, bol-com-deals, bol-com-black-friday, bol-com-netherlands, bol-com-belgium, dutch-marketplace, netherlands-ecommerce, belgium-ecommerce, benelux, marketplace, price-comparison, price-monitoring, competitor-prices, repricing, buy-box, ean-lookup, seller-data, product-reviews, multi-country, europe, product-search, product-data, category-browse, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/docs/bolcom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api
---

# bol.com API - Prices, Offers, Sellers, NL and BE

Read bol.com, the marketplace of the Netherlands and Belgium, on its three storefronts: Netherlands in Dutch (`nl-nl`), Belgium in Dutch (`be-nl`) and Belgium in French (`be-fr`), all in euros. Look up one product by bol product id, link or EAN; list its 10 lowest-priced offers; search by keyword or browse a category, a brand, a seller's range or a bol promotion; read a seller's public profile; and read today's deals. All 9 endpoints return structured JSON and cost 2 credits per call; a product lookup by EAN costs 4.

**The job this skill is for: bol.com competitor prices.** `/product` gives the buy box (the offer bol shows first: price, seller, the reference price bol shows next to it and its type, shipping cost, delivery promise), `offer_count`, and the cheapest new, fastest new, cheapest second-hand and per-grade refurbished offers. `/offers` lists the 10 lowest-priced offers on the same product, lowest price first: price, condition (with the refurbished grade or second-hand state), shipping cost, delivery date and the seller's rating, with counts by condition for all its offers (`has_more` when bol has more; there is no paging). Product ids, EANs and seller ids are shared across storefronts, so the same id prices the product in the Netherlands and in Belgium.

bol has two official APIs, both behind an account: the Retailer API for registered bol sellers (free; its competing-offers call covers an EAN the seller works with, for the seller's own sales) and the Marketing Catalog API for registered affiliates (the best offer, ratings and search, to send traffic to bol). This skill needs neither account, which suits teams that do not sell on bol, or that track bol next to other marketplaces.

See also: for Amazon.nl and Amazon.com.be use `amazon-product-data` with the `nl` or `be` marketplace; for the cross-merchant view of one product use `google-shopping-api`; for every seller's price on other European marketplaces use `allegro-api` (Poland, Czechia, Slovakia, Hungary) or `trendyol-api`.

## When to trigger

Use this skill when the user asks to:
- Check competitor prices for a product on bol.com: who holds the buy box, at what price, and the lowest-priced competing offers
- Look up a bol.com product by EAN / GTIN (barcode) and get its price and offers
- Compare a product's price and offers between bol.com Netherlands and bol.com Belgium
- Read the reference price bol shows next to a price (the supplier's recommended price, or bol's most-shown price of the last 90 days) and the discount against it
- Find refurbished or second-hand offers for a product on bol.com, by grade
- Search bol.com or browse a category, a brand, a seller's range or a Black Friday / day-deal promotion, sorted and filtered
- Check a bol.com seller before buying or as a competitor: rating out of 10, sub-ratings, review counts, product count, company name, city, country and VAT number
- Read a bol.com product's specifications, rating distribution, the first 10 reviews and bol's AI review topics
- See today's bol.com deals

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits (a product lookup by EAN 4), so the free credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls take 2 to 10 seconds; a busy moment can take longer. Set a client timeout of at least 240 seconds and send one call at a time (a busy moment answers `503` with `Retry-After`).

| Endpoint | Storefronts | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/bolcom/search` | `nl-nl`, `be-nl`, `be-fr` | 2 | Products for a keyword, about 24 to 30 per page up to page 10, sorted and filtered, sponsored items flagged, with facets |
| `POST /api/v1/bolcom/product` | `nl-nl`, `be-nl`, `be-fr` | 2 (4 by `ean`) | One product by `product_id`, `url` or `ean`: buy box, offer counts, cheapest and fastest offers, refurbished grades, specifications, category path, rating distribution, bol's AI review topics and the first 10 reviews |
| `POST /api/v1/bolcom/offers` | `nl-nl`, `be-nl`, `be-fr` | 2 | The 10 lowest-priced offers on one product: price, reference price, condition, shipping cost, delivery date, seller with rating; counts by condition for all offers |
| `POST /api/v1/bolcom/seller` | `nl-nl`, `be-nl`, `be-fr` | 2 | A seller's public profile: rating out of 10 with up to 4 sub-ratings, positive percent, review counts, product count, EU trader data |
| `POST /api/v1/bolcom/seller-products` | `nl-nl`, `be-nl`, `be-fr` | 2 | The products a seller sells, pages 1 to 500, sorted (each with its buy box, which can be another seller's) |
| `POST /api/v1/bolcom/category` | `nl-nl`, `be-nl`, `be-fr` | 2 | Products in one category, pages 1 to 500, sorted and filtered like search |
| `POST /api/v1/bolcom/brand` | `nl-nl`, `be-nl`, `be-fr` | 2 | Products of one brand, pages 1 to 500, sorted |
| `POST /api/v1/bolcom/deals` | `nl-nl`, `be-nl`, `be-fr` | 2 | Today's day deal (linked on the storefront asked) and the first deal products of a few categories |
| `POST /api/v1/bolcom/campaign` | `nl-nl`, `be-nl`, `be-fr` | 2 | The products of one bol promotion (a Black Friday list, the day deal), pages 1 to 500, sorted |

A not-found (an unknown product, seller, category, brand or an ended campaign) is charged for what the call spent (2, or 4 when an EAN search answered a product with another EAN); a failed call is not charged.

## Storefronts

Every endpoint takes `country` and `language`:

| `country` | `language` | `storefront` | Site | Language | Currency |
|---|---|---|---|---|---|
| `nl` (default) | `nl` (default) | `nl-nl` | bol.com Netherlands | Dutch | EUR |
| `be` | `nl` (default) | `be-nl` | bol.com Belgium | Dutch | EUR |
| `be` | `fr` | `be-fr` | bol.com Belgium | French | EUR |

- Every answer echoes `country`, `language`, `storefront` and `currency` (`EUR`).
- `language: "fr"` works only with `country: "be"`; `nl` + `fr` answers `400` before anything is charged. Any other `country` or `language` answers `400`.
- Product ids, EANs, category ids, seller ids and offer ids are the same on every storefront. Prices, offers and stock can differ between the Netherlands and Belgium, and fewer sellers ship to Belgium: the build measured the iPhone 17 256GB with 10 offers on `nl-nl` and 6 on `be-nl` (2026-11-17).
- A `url` carries its storefront; `country` / `language` sent with it win (ids are shared, so a Dutch link can be read on `be-fr`).
- On `be-fr` bol's own texts are French, some partner titles and attribute values stay Dutch, review texts are bol's own translation from Dutch (`is_translated: true`), and the review topics stay Dutch. bol shows no seller description on `be-fr`.

## Workflow

1. **Competitor prices for one product:** `/product` (by `product_id`, `url` or `ean`) for the buy box, `offer_count`, `cheapest_new`, `fastest_new`, `cheapest_second_hand` and `refurbished`; then `/offers` with the same `product_id` for the 10 lowest-priced offers and the counts of all offers by condition. The offers list does not mark the buy box: match `offers[].offer_id` against the product's `buy_box.offer_id`. 4 credits (6 by EAN).
2. **Netherlands vs Belgium:** run the same `product_id` with `country: "nl"` and `country: "be"`. Compare prices, offer counts and who holds the buy box; say which storefront each figure came from.
3. **From a barcode:** `/product` with `ean` (8, 12, 13 or 14 digits). It is a search plus the product page, so it costs 4 credits; the answer carries `requested_ean` and the product's own `ean`. Once you have `product_id`, use it (2 credits).
4. **Find products:** `/search` with `query` (Dutch or French keywords match best; an EAN as `query` also finds that product). Search stops at page 10. List items carry no EAN: call `/product` for it. For deeper lists use `/category` (up to `max_page`, at most 500; for example 69 pages for earphones on `be-fr`), `/brand` or `/campaign`.
5. **Filter by brand:** take the brand's value id from the `Merk` / `Marque` facet of a search answer and send it as `brand_facet_id` on `/search` or `/category`. It is a different id from `brand.brand_id`, which feeds `/brand`.
6. **Seller check:** `seller_id` from an offer (`offer.seller_id` on list items, `seller.seller_id` on offers and the buy box) feeds `/seller` and `/seller-products`. `seller_id` `"0"` is bol itself (`sold_by_bol: true`): it has no seller profile.
7. **Promotions:** `/deals` gives today's day deal with its `campaign_id`; offer `labels[]` carry `campaign_id`s too (for example a Black Friday label). `/campaign` with that id lists every product in the promotion; each item's `offer` is its buy box, which does not always carry the campaign's label.

## Parameters

### Storefront (every endpoint)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `nl` | `nl` or `be` |
| `language` | string | `nl` | `nl` or `fr` (`fr` only with `be`) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, up to 200 characters |
| `page` | integer | 1 | 1 to 10 (bol.com search stops at page 10, about 280 results; higher answers `400`) |
| `sort` | string | `relevance` | `relevance`, `popularity`, `price_asc`, `price_desc`, `rating`, `wishlist` (most wished for). No newest sort |
| `category_id` | string | none | Search within one category (from the category facet or a product's `category_path`) |
| `price_min` / `price_max` | number | none | Euros |
| `condition` | string or list | all | One or more of `new`, `refurbished`, `second_hand`: keeps products that have an offer in that condition |
| `deals_only` | boolean | false | Only products on a deal |
| `select_deals` | boolean | false | Only bol Select member deals |
| `delivery` | string or list | none | One or more of `today`, `tomorrow`, `evening`, `sunday`, `free_shipping` |
| `brand_facet_id` | string | none | A brand value id from the brand facet of an earlier answer (`facets[].values[].id` of `Merk` / `Marque`, e.g. `4294862300` Apple). Not a `brand_id` |
| `facets` | list | none | Up to 10 facet value ids from `facets[].values[].id` of an earlier answer (any facet); ids bol did not apply come back in `filters_ignored` |

### Product (`/product`)

Send exactly one of:

| Parameter | Type | Description |
|---|---|---|
| `product_id` | string | A bol product id, 16 digits, as a **string** (`"9300000239314960"`): a JSON number that long loses digits, and a number that is not a safe integer answers `400` |
| `url` | string | A bol.com product link (`https://www.bol.com/nl/nl/p/<slug>/<product id>/`) or its price overview link |
| `ean` | string | An EAN / GTIN of 8, 12, 13 or 14 digits. 4 credits |

### Offers (`/offers`)

Exactly one of `product_id` (string) or `url` (a product or price overview link).

### Seller (`/seller`)

Exactly one of `seller_id` (digits, `"1770745"`) or `url` (the seller's bol.com page or product-list link). `"0"` (bol itself) answers `400`.

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | required | A bol category id (`"8440"` earphones; the same id on every storefront) |
| `page` | integer | 1 | 1 to `max_page` of the answer (bol lists at most 500 pages; above 500 answers `400`) |
| `sort` | string | `popularity` | `popularity`, `price_asc`, `price_desc`, `rating`, `wishlist`. `relevance` is not offered on listing pages (`400`) |

Plus the search filters `price_min`, `price_max`, `condition`, `deals_only`, `select_deals`, `delivery`, `brand_facet_id` and `facets` (not `category_id`).

### Seller products (`/seller-products`), brand (`/brand`), campaign (`/campaign`)

Exactly one of the id (`seller_id`, `brand_id` such as `"5070005"` Apple, `campaign_id` such as `"555136"`) or `url`, plus `page` and `sort` (default `popularity`, no `relevance`). These three take page and sort only: a filter answers `400`.

### Deals (`/deals`)

`country` and `language` only.

## Examples

### Product (buy box, offers summary, reviews)

```bash
curl -X POST https://api.scavio.dev/api/v1/bolcom/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "9300000239314960"}'
```

Captured `data` (nl-nl, 2026-11-17; `description`, `specifications` (68 rows), `images` (25), 4 of 5 `review_topics`, 9 of 10 reviews and the notes dropped, the review text cut):

```json
{
  "product_id": "9300000239314960",
  "ean": "0195950543742",
  "title": "Apple Airpods Pro 3 - In-ear koptelefoon - USB-C",
  "subtitle": null,
  "url": "https://www.bol.com/nl/nl/p/apple-airpods-pro-3-in-ear-koptelefoon-usb-c/9300000239314960/",
  "brand": { "brand_id": "5070005", "name": "Apple" },
  "category_path": [
    { "category_id": "3136", "name": "Elektronica" },
    { "category_id": "10714", "name": "Audio & Hifi" },
    { "category_id": "64498", "name": "Audio voor jou" },
    { "category_id": "76364", "name": "Oordopjes & Accessoires" },
    { "category_id": "8440", "name": "Oordopjes" }
  ],
  "buy_box": {
    "offer_id": "6a4792a5-9727-4bb1-a207-e1751a99508a",
    "price": 208.95,
    "reference_price": 249,
    "reference_price_type": "rrp",
    "discount_percent": 16,
    "discount_shown": false,
    "condition": "new",
    "seller": { "seller_id": "0", "name": "bol", "sold_by_bol": true },
    "shipping_cost": 0,
    "delivery_text": "Op voorraad. Voor 23:59 uur besteld, morgen in huis",
    "delivery_date": "2026-11-18",
    "delivered_within_48h": true,
    "low_stock": false,
    "labels": [{ "text": "Max 2 per klant", "campaign_id": "578257", "mechanism": null }]
  },
  "offer_count": 3,
  "cheapest_new": { "price": 208.95 },
  "fastest_new": { "price": 208.95, "delivery_text": "Op voorraad. Voor 23:59 uur besteld, morgen in huis", "delivery_date": "2026-11-18" },
  "cheapest_second_hand": null,
  "refurbished": [],
  "energy_label": null,
  "video": null,
  "series": [{ "series_id": "9700000000002133", "name": "Apple AirPods" }],
  "rating": { "average": 4.4, "count": 402, "distribution": { "1": 33, "2": 21, "3": 19, "4": 24, "5": 305 } },
  "review_topics": [
    {
      "topic": "geluidskwaliteit",
      "review_count": 162,
      "positive": 154,
      "neutral": 0,
      "negative": 8,
      "summary": "De overgrote meerderheid van de gebruikers prijst de geluidskwaliteit, helderheid en diepe basweergave. Enkele reviewers vinden het geluid echter tegenvallen of merken af en toe ruis of storingen op."
    }
  ],
  "review_summary": null,
  "reviews": [
    {
      "review_id": "e4abc1e9-ec51-4fe7-a5fa-7af66c93a188",
      "rating": 3,
      "title": "Beperkte evolutie tov Pro 2",
      "text": "Het is even wennen aan de nieuwe pasvorm. ...",
      "pros": ["Toegenomen bas/lage tonen (als je er van houdt)", "Zitten iets steviger in mijn(!) oren"],
      "cons": ["Evolutie tov pro2 te beperkt", "Modderige bas (sounds like bose)"],
      "verified": true,
      "is_translated": false,
      "refurbished_purchase": false,
      "date": "2025-12-28T11:25:11.642Z",
      "helpful_count": 63,
      "not_helpful_count": 6,
      "product_id": "9300000239314960"
    }
  ],
  "more_reviews": true,
  "country": "nl",
  "language": "nl",
  "storefront": "nl-nl",
  "currency": "EUR"
}
```

bol itself (`seller_id` `"0"`, `sold_by_bol: true`) holds the buy box here at 208.95 EUR against the supplier's recommended price of 249 (`reference_price_type` `rrp`); `discount_percent` 16 is computed against it because bol did not show it struck through (`discount_shown: false`). Reviews are pooled across the product family: only 3 of the 10 reviews in this answer carry this `product_id`, the other 7 were written for two related product ids, and `rating` counts the pool. `review_topics` are bol's own AI-generated summaries; `review_summary` (bol's AI recap) is often null.

### Offers (the 10 lowest-priced)

```bash
curl -X POST https://api.scavio.dev/api/v1/bolcom/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "9300000240171936"}'
```

Captured `data` (nl-nl, 2026-11-17; 3 of the 10 offers returned, the notes dropped):

```json
{
  "product_id": "9300000240171936",
  "title": "Apple iPhone 17 - 256GB - Black",
  "url": "https://www.bol.com/nl/nl/p/apple-iphone-17-256gb-zwart/9300000240171936/",
  "counts": { "new": 8, "refurbished": 3, "second_hand": 0 },
  "offers": [
    {
      "offer_id": "0f298674-b156-4768-aae0-91a80602a427",
      "price": 766,
      "reference_price": null,
      "reference_price_type": null,
      "discount_percent": null,
      "discount_shown": false,
      "condition": "refurbished",
      "refurbished_grade": "B",
      "seller": { "seller_id": "1849943", "name": "Alloccaz", "sold_by_bol": false, "rating": 8.6, "top_seller": false },
      "shipping_cost": 0,
      "delivery_text": "Uiterlijk 24 november in huis",
      "delivery_date": "2026-11-24",
      "delivered_within_48h": false,
      "low_stock": false,
      "labels": []
    },
    {
      "offer_id": "4484d8ba-b7d2-4f71-bd94-182f88421e7e",
      "price": 945,
      "reference_price": 1119,
      "reference_price_type": "rrp",
      "discount_percent": 16,
      "discount_shown": false,
      "condition": "new",
      "seller": { "seller_id": "1756174", "name": "EZShop NL", "sold_by_bol": false, "rating": 9.1, "top_seller": false },
      "shipping_cost": 0,
      "delivery_text": "Op voorraad. Voor 23:59 uur besteld, donderdag in huis",
      "delivery_date": "2026-11-19",
      "delivered_within_48h": true,
      "low_stock": false,
      "labels": []
    },
    {
      "offer_id": "5b18086f-cff1-496c-9be5-60f89a150cab",
      "price": 1029,
      "reference_price": 1119,
      "reference_price_type": "rrp",
      "discount_percent": 8,
      "discount_shown": false,
      "condition": "new",
      "seller": { "seller_id": "1823883", "name": "Smartphonehoekje.nl", "sold_by_bol": false, "rating": 9, "top_seller": false },
      "shipping_cost": 0,
      "delivery_text": "Op voorraad. Voor 23:59 uur besteld, morgen in huis",
      "delivery_date": "2026-11-18",
      "delivered_within_48h": true,
      "low_stock": false,
      "labels": []
    }
  ],
  "has_more": true,
  "count": 10,
  "country": "nl",
  "language": "nl",
  "storefront": "nl-nl",
  "currency": "EUR"
}
```

`offers` are the 10 lowest-priced offers, lowest price first as bol orders them, all conditions mixed: here 3 refurbished offers (from 766 EUR, grade B) before 7 new ones (945 to 1029 EUR, three sellers at 945). `counts` covers all of the product's offers (8 new + 3 refurbished = 11), and `has_more` is true because bol has more than the 10 returned: the higher-priced one is not returned, and there is no paging. `rating` is the seller's score out of 10 (the seller's positive percentage is on `/seller`). The list has no buy-box flag: the product answer's `buy_box.offer_id` names it.

### Product by EAN (Belgium, French)

```bash
curl -X POST https://api.scavio.dev/api/v1/bolcom/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "4242005483976", "country": "be", "language": "fr"}'
```

Captured `data` (be-fr, 2026-11-17, 4 credits; selected fields):

```json
{
  "product_id": "9300000184950577",
  "ean": "4242005483976",
  "requested_ean": "4242005483976",
  "title": "Bosch BGB41BA1 Série 4 - Aspirateur avec sac - Zwart",
  "brand": { "brand_id": "7573353", "name": "Bosch" },
  "buy_box": {
    "offer_id": "3f0dbb65-ebd3-44dd-8817-9b353e4437d7",
    "price": 109,
    "reference_price": 149.99,
    "reference_price_type": "rrp",
    "discount_percent": 27,
    "discount_shown": false,
    "condition": "new",
    "seller": { "seller_id": "0", "name": "bol", "sold_by_bol": true },
    "shipping_cost": 0,
    "delivery_text": "En stock. Commandé avant 23:59 heure, livré demain",
    "delivery_date": "2026-11-18",
    "delivered_within_48h": true,
    "low_stock": false,
    "labels": [{ "text": "Offre Black Friday", "campaign_id": "555140", "mechanism": "price_off" }]
  },
  "offer_count": 1,
  "rating": { "average": 4.2, "count": 27, "distribution": { "1": 2, "2": 0, "3": 3, "4": 8, "5": 14 } },
  "country": "be",
  "language": "fr",
  "storefront": "be-fr",
  "currency": "EUR"
}
```

The title is French with a Dutch colour word left in ("Zwart"), as bol shows it. All 10 reviews of this answer are bol's translation (`is_translated: true`), while `review_topics` stay Dutch (`zuigkracht`). The buy box carries a Black Friday label whose `campaign_id` `555140` feeds `/campaign`.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/bolcom/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "airpods"}'
```

Captured `data` (nl-nl, 2026-11-17; 2 of 28 items, 2 of 11 facets with 1 to 3 values each, and the notes shown in part):

```json
{
  "query": "airpods",
  "items": [
    {
      "product_id": "9300000242114670",
      "title": "Accezz Echt Leren Case - Hoesje geschikt voor AirPods Pro 3 - Cognac",
      "url": "https://www.bol.com/nl/nl/p/accezz-echt-leren-case-hoesje-geschikt-voor-airpods-pro-3-cognac/9300000242114670/",
      "brand": { "brand_id": "15058295", "name": "Accezz" },
      "category": "Hoesje voor oordopjes",
      "rating": { "average": 3.7, "count": 9 },
      "offer": {
        "offer_id": "5de89b18-7ff0-4d91-8ff6-ce52897a6d84",
        "price": 16.99,
        "reference_price": 26.99,
        "reference_price_type": "most_shown_price",
        "discount_percent": 37,
        "discount_shown": false,
        "condition": "new",
        "seller_id": "829931",
        "seller_name": "Smartphonehoesjes.nl",
        "sold_by_bol": false,
        "delivery_text": "Op voorraad. Voor 21:00 uur besteld, morgen in huis",
        "delivery_date": "2026-11-18",
        "delivered_within_48h": true,
        "low_stock": false,
        "labels": [{ "text": "in prijs verlaagd", "campaign_id": "325524", "mechanism": "reguliere_prijsverlaging" }]
      },
      "energy_label": null,
      "image": "https://media.s-bol.com/WVGZVAW3EGkx/58DwwQX/550x491.jpg",
      "family_id": "9300000231124918",
      "sponsored": true
    },
    {
      "product_id": "9300000386682752",
      "title": "Apple AirPods 5 - reguliere oplaadcase",
      "url": "https://www.bol.com/nl/nl/p/apple-airpods-5-reguliere-oplaadcase/9300000386682752/",
      "brand": { "brand_id": "5070005", "name": "Apple" },
      "category": "Oordopjes",
      "rating": { "average": 4.9, "count": 12 },
      "offer": {
        "offer_id": "0a4828e4-8f9f-4dff-a289-b620fe970b44",
        "price": 136.95,
        "reference_price": 149,
        "reference_price_type": "rrp",
        "discount_percent": 8,
        "discount_shown": false,
        "condition": "new",
        "seller_id": "0",
        "seller_name": "bol",
        "sold_by_bol": true,
        "delivery_text": "Op voorraad. Voor 23:59 uur besteld, morgen in huis",
        "delivery_date": "2026-11-18",
        "delivered_within_48h": true,
        "low_stock": false,
        "labels": [
          { "text": "Black Friday deal", "campaign_id": "561354", "mechanism": "price_off" },
          { "text": "Max 4 per klant", "campaign_id": "578260", "mechanism": null },
          { "text": "Bekijk alle nieuwe electronica producten", "campaign_id": "516350", "mechanism": null }
        ]
      },
      "energy_label": null,
      "image": "https://media.s-bol.com/Y3yy73OnNgqp/z6prPzr/550x517.jpg",
      "family_id": "9300000364785902",
      "sponsored": false
    }
  ],
  "count": 28,
  "sponsored_count": 6,
  "total": 3776,
  "page": 1,
  "max_page": 10,
  "has_more": true,
  "sort": "relevance",
  "sorts_offered": ["relevance", "popularity", "price_asc", "price_desc", "rating", "wishlist"],
  "facets": [
    {
      "id": "4842",
      "name": "Merk",
      "type": "values",
      "values": [{ "id": "4294862300", "name": "Apple", "count": 27, "applied": false }]
    },
    {
      "id": "14032",
      "name": "Conditie",
      "type": "values",
      "values": [
        { "id": "14033", "name": "Nieuw", "count": 7939, "applied": false },
        { "id": "72659", "name": "Refurbished", "count": 2, "applied": false },
        { "id": "1426", "name": "Tweedehands", "count": 3, "applied": false }
      ]
    }
  ],
  "notes": [
    "sponsored items are paid placements bol mixes into the list.",
    "List items carry no EAN (product has it). bol search stops at page 10 (about 280 results)."
  ],
  "dominant_category": { "category_id": "76364", "name": "Oordopjes & Accessoires" },
  "country": "nl",
  "language": "nl",
  "storefront": "nl-nl",
  "currency": "EUR"
}
```

`most_shown_price` is bol's most-shown non-promotional price over the last 90 days ("in prijs verlaagd", price lowered); `rrp` is the supplier's recommended price. The Apple brand facet value id is `4294862300` (for `brand_facet_id`), while the items' `brand.brand_id` is `5070005` (for `/brand`): two id spaces. `total` is bol's own count; search pages stop at 10 whatever `total` says.

### Seller

```bash
curl -X POST https://api.scavio.dev/api/v1/bolcom/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_id": "1770745"}'
```

Captured `data` (nl-nl, 2026-11-17; `url`, `description` and the notes dropped):

```json
{
  "seller": {
    "seller_id": "1770745",
    "name": "Clevertronic",
    "active_since": "2023-11-30T08:18:28",
    "rating": 8.8,
    "rating_details": { "product_info": 9.5, "delivery_time": 9.3, "shipping": 9.6, "service": 9.7 },
    "rating_method": "recent_reviews",
    "reviews_used_for_rating": 49,
    "positive_percent": 97.8,
    "top_seller": false,
    "reviews": { "positive": 568, "neutral": 47, "negative": 22, "total": 637 },
    "product_count": 21,
    "business": {
      "company_name": "TELBLUE COMÉRCIO INTERNACIONAL",
      "city": "Braga",
      "country": "PT",
      "registration_number": "517515113",
      "vat_number": "PT517515113",
      "country_of_origin": "PT"
    }
  },
  "country": "nl",
  "language": "nl",
  "storefront": "nl-nl",
  "currency": "EUR"
}
```

`rating` (out of 10) is computed over the reviews `rating_method` names, as bol states per seller (`recent_reviews`: the last 3 months, `reviews_used_for_rating` 49 here; `all_reviews`: all of the seller's reviews), and `positive_percent` is bol's positive percentage over those reviews; `rating_details` carries up to four sub-ratings (some sellers have fewer), while `reviews` counts every review by sentiment, all time. `business` is the trader data bol publishes under EU rules; no street address is returned, and review texts are not returned.

### Other endpoints (captured 2026-11-17)

- `/seller-products` with `{"seller_id": "1767374", "country": "be"}` (be-nl): `seller` `{"seller_id": "1767374", "name": "FlowCart"}`, 24 items, `total` 187, `max_page` 8, `sort` `popularity`. Each item's `offer` is that product's buy box, which can be another seller's; items can add `cheapest_refurbished` (with `refurbished_grade`) or `cheapest_second_hand`.
- `/category` with `{"category_id": "8440", "country": "be", "language": "fr"}` (be-fr): `category` `{"category_id": "8440", "name": "Écouteurs", ...}` with `breadcrumbs`, 28 items (6 sponsored), `total` 1650, `max_page` 69, 15 facets.
- `/brand` with `{"brand_id": "5070005"}` (nl-nl): `brand` `{"brand_id": "5070005", "name": "Apple", "premium_brand": true}`, 24 items, `total` 2035, `max_page` 85.
- `/campaign` with `{"campaign_id": "555136"}` (nl-nl): `campaign` `{"campaign_id": "555136", "name": "Deals op steel- en robotstofzuigers", "description": "Ontdek alle Black Friday deals op steel- en robotstofzuigers van o.a. Dyson, Roborock, Rowenta, Dreame en Bosch.", "type": "discount", "ends_at": "2026-12-01T00:00:00.000+01:00"}` (a Black Friday list of stick and robot vacuums), 24 items, `total` 156, `max_page` 7.
- `/deals` with `{"country": "be"}` (be-nl): `day_deal` "Little Live Pets & Beyblade" with `campaign_id` `556789`, `url` `https://www.bol.com/be/nl/ra/dagdeal-op-little-live-pets---beyblade/556789/` (the day deal on the storefront asked) and `ends_at` `2026-11-18T00:00:00.000+01:00`; 4 `category_deals` (Speelgoed, Elektronica, Boeken, Persoonlijke verzorging) with 14 products; 8 `more_deal_category_ids`. Deal products carry `seller_id` only (`seller_name` null).

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bol(endpoint, body, timeout=240):
    r = requests.post(f"{BASE}/api/v1/bolcom/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

# Competitor prices for one product in the Netherlands and Belgium (8 credits)
product_id = "9300000240171936"  # a string: 16 digits
captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
for country in ("nl", "be"):
    product = bol("product", {"product_id": product_id, "country": country})
    offers = bol("offers", {"product_id": product_id, "country": country})
    bb = product["buy_box"] or {}
    seller = (bb.get("seller") or {}).get("name")
    print(captured_at, product["storefront"], "buy box", bb.get("price"), seller, "counts", offers["counts"])
    for o in offers["offers"]:
        mark = "*" if o["offer_id"] == bb.get("offer_id") else " "
        grade = o.get("refurbished_grade") or o.get("second_hand_state") or ""
        print(mark, o["price"], "+", o["shipping_cost"], o["condition"], grade,
              o["seller"]["name"], o["seller"].get("rating"), o["delivery_date"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live. Every answer carries `country`, `language`, `storefront`, `currency` (`EUR`) and `notes`.

- **Offer** (list items, buy box, offers) - `offer_id`, `price`, `reference_price`, `reference_price_type` (`rrp`: the supplier's recommended price, bol's "Adviesprijs" / "Prix conseillé"; `most_shown_price`: bol's most-shown non-promotional price over the last 90 days), `discount_percent` (bol's own percentage when `discount_shown` is true, else computed against the reference price), `discount_shown` (bol shows the reference struck through), `condition` (`new`, `refurbished` with `refurbished_grade` A / B / C, `second_hand` with `second_hand_state` and `condition_note` when given), `delivery_text` (bol's delivery promise in the storefront language), `delivery_date`, `delivered_within_48h`, `low_stock`, `labels[]` {`text`, `campaign_id`, `mechanism`}. List items and deals add `seller_id`, `seller_name`, `sold_by_bol`; the buy box and offers carry `seller` {`seller_id`, `name`, `sold_by_bol`, and for partners `rating` (out of 10), `top_seller`, sometimes `top_quality_seller`} and `shipping_cost`.
- **Listing answer** (search, category, brand, seller-products, campaign) - `items[]`, `count`, `sponsored_count`, `total` (bol's count), `page`, `max_page`, `has_more`, `sort`, `sorts_offered`, `filters` and `filters_ignored` (when sent), `facets[]` {`id`, `name`, `type` (`category`, `values`, `range`), `values[]` {`id`, `name`, `count`, `applied`} or `unit`, `min`, `max`, `applied_min`, `applied_max`}, `notes`. Search adds `query` and `dominant_category`; category adds `category` {`category_id`, `name`, `url`, `breadcrumbs`}; brand adds `brand` {`brand_id`, `name`, `premium_brand`}; seller-products adds `seller` {`seller_id`, `name`}; campaign adds `campaign` {`campaign_id`, `name`, `description`, `type`, `ends_at`}.
- **List item** - `product_id`, `title`, `url`, `brand` {`brand_id`, `name`}, `category` (name), `rating` {`average`, `count`}, `offer` (the buy box), `cheapest_second_hand` and `cheapest_refurbished` when bol shows them, `energy_label` {`class`, `description`}, `image`, `family_id`, `sponsored`. No EAN.
- **product** - `product_id`, `ean`, `title`, `subtitle`, `url`, `brand`, `description` (plain text), `specifications[]` {`group`, `name`, `key`, `value`}, `category_path[]` {`category_id`, `name`}, `buy_box`, `offer_count`, `cheapest_new` {`price`}, `fastest_new` {`price`, `delivery_text`, `delivery_date`}, `cheapest_second_hand`, `refurbished[]` {`grade`, `grade_name`, `offer_count`, `cheapest`}, `energy_label`, `images[]`, `video` {`url`, `poster`}, `series[]`, `rating` {`average`, `count`, `distribution` 1-5}, `review_topics[]` {`topic`, `review_count`, `positive`, `neutral`, `negative`, `summary`}, `review_summary`, `reviews[]` (first 10: `review_id`, `rating`, `title`, `text`, `pros`, `cons`, `verified`, `is_translated`, `refurbished_purchase`, `date`, `helpful_count`, `not_helpful_count`, `product_id`), `more_reviews`; `requested_ean` when looked up by EAN.
- **offers** - `product_id`, `title`, `url`, `counts` {`new`, `refurbished`, `second_hand`} (all of the product's offers), `offers[]` (up to 10, lowest price first), `has_more` (bol has more than the 10 returned; no paging), `count`.
- **seller** - `seller` {`seller_id`, `name`, `url`, `active_since`, `description`, `rating`, `rating_details` {`product_info`, `delivery_time`, `shipping`, `service`}, `rating_method`, `reviews_used_for_rating`, `positive_percent`, `top_seller`, `reviews` {`positive`, `neutral`, `negative`, `total`}, `product_count`, `business` {`company_name`, `city`, `country`, `registration_number`, `vat_number`, `country_of_origin`}}.
- **deals** - `day_deal` {`title`, `campaign_id`, `url` (on the storefront asked), `ends_at`, `highlighted_product` {`product_id`, `title`, `url`, `image`}}, `category_deals[]` {`category_id`, `category_name`, `products[]` {`product_id`, `title`, `url`, `image`, `offer`}}, `more_deal_category_ids`, `count`.

## Guardrails

- Competitor prices: the buy box is the offer bol shows first, not always the lowest price; compare `buy_box` with `cheapest_new` and the `/offers` list (the 10 lowest-priced; when `has_more` is true, say the higher-priced offers were not read), and add `shipping_cost` when comparing sellers. Say which storefront, product id and time each price comes from.
- `/offers` mixes conditions (refurbished offers often come first, being cheaper). Never compare a refurbished or second-hand price with a new price as if they were the same product state.
- `reference_price` is a reference bol shows, not a past price paid: name its type (`rrp` = recommended retail price, `most_shown_price` = bol's most-shown price of the last 90 days). There is no price history and no 30-day lowest price: poll and store if the user needs a history.
- Search depth is fixed: pages 1 to 10 (about 280 results). Sorting by anything but relevance can narrow bol's result set (the build measured nintendo switch at 6,655 results by relevance, 30 by price), and price sorts follow bol's own ordering, so small inversions against the buy-box price occur: sort yourself when strict order matters. Never claim to have read every result or to know a market's size from `total`.
- Listing pages (category, brand, seller-products, campaign) run pages 1 to 500, default to `popularity` and do not offer `relevance`; brand, seller-products and campaign take no filters.
- `brand_facet_id` and `brand_id` are different id spaces; never send one as the other.
- `product_id` is a 16-digit string. Never send it as a JSON number.
- Reviews: the first 10 as bol shows them, pooled across the product family; filter by `reviews[].product_id` before attributing a review to a product, and treat `rating` as the pool's rating. No review paging, sorting or star filter. `review_topics` and `review_summary` are bol's AI summaries: label them as bol's. On `be-fr`, review texts are bol's translation and `review_topics` stay Dutch as bol serves them.
- `seller_id` `"0"` is bol itself; it has no seller profile or seller product list.
- Not available, so do not offer them: price history, 30-day lowest price, search suggestions, review paging beyond the first 10, seller review texts, pickup points, bol Select member prices, a structured variant selector, buying, or anything that changes an offer.
- People: reviews never carry reviewer names, ages or locations; do not try to identify reviewers. Seller `business` data is the trader information bol publishes; use it to judge a seller, not to contact or profile a person.
- Terms: bol.com's copyright notice says the site is for customers' own or internal use and may not be reproduced or made available on a network without bol's prior written permission; bol's affiliate API may be used only to send traffic to bol, and its Retailer API only for a seller's own sales. This is not legal advice; read the current terms for your use case. Do not republish bol product photos, seller logos or bol marks; link products by `url` instead.
- Never fabricate prices, ids, ratings or reviews. Only return what the API returned, with the `storefront`, `currency` and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `nl` / `be`, a `language` other than `nl` / `fr`, `fr` with `nl` ("French is available on be (storefront be-fr); nl is Dutch only."), a search `page` above 10 ("page must be 1 to 10: bol.com search stops at page 10 (about 280 results)."), a listing `page` above 500, `relevance` on a listing page, a filter on brand, seller-products or campaign ("... is not available on brand (page and sort only)."), `price_min` above `price_max`, more than 10 `facets`, an EAN that is not 8, 12, 13 or 14 digits, a long `product_id` sent as a JSON number ("product_id must be sent as a string (too long for a JSON number)."), `seller_id` `0`, not exactly one of the id fields and `url`, or a link that is not a bol.com link of the right kind.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged for what the call spent: "bol.com has no product ... on nl-nl.", "No bol.com product carries EAN ... on be-fr.", "bol.com has no seller ...", "bol.com has no category ...", "bol.com has no brand ...", "bol.com has no running campaign ... on nl-nl." (campaigns end). Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api).
- `502` means bol.com data was temporarily unavailable ("bol.com is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means bol.com is busy ("bol.com is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- A page past the last one answers `200` with no items and a note; it is charged like any page.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.66.0
npm install scavio@0.67.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: product } = await scavio.bolcom.product({ product_id: "9300000239314960" });
const { data: byEan } = await scavio.bolcom.product({ ean: "4242005483976", country: "be", language: "fr" });
const { data: offers } = await scavio.bolcom.offers({ product_id: "9300000240171936" });
const { data: results } = await scavio.bolcom.search({ query: "airpods", sort: "popularity" });
const { data: seller } = await scavio.bolcom.seller({ seller_id: "1770745" });
const { data: range } = await scavio.bolcom.sellerProducts({ seller_id: "1767374", country: "be" });
const { data: earphones } = await scavio.bolcom.category({ category_id: "8440", deals_only: true });
const { data: apple } = await scavio.bolcom.brand({ brand_id: "5070005" });
const { data: deals } = await scavio.bolcom.deals({ country: "nl" });
const { data: blackFriday } = await scavio.bolcom.campaign({ campaign_id: "555136" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.bolcom.search(...)`, `product`, `offers`, `seller`, `seller_products`, `category`, `brand`, `deals` and `campaign`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_bolcom`, `get_bolcom_product`, `get_bolcom_offers`, `get_bolcom_seller`, `get_bolcom_seller_products`, `get_bolcom_category`, `get_bolcom_brand`, `get_bolcom_deals` and `get_bolcom_campaign`. bol.com is opt-in: add `bolcom` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.66.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bolcom"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bolcom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [product](https://scavio.dev/docs/bolcom-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [offers](https://scavio.dev/docs/bolcom-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [seller](https://scavio.dev/docs/bolcom-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [seller products](https://scavio.dev/docs/bolcom-seller-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [category](https://scavio.dev/docs/bolcom-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [brand](https://scavio.dev/docs/bolcom-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [deals](https://scavio.dev/docs/bolcom-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api), [campaign](https://scavio.dev/docs/bolcom-campaign?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api). Overview: [bol.com API](https://scavio.dev/bolcom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=bol-com-api).
