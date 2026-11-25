---
name: dermstore-skincare-prices-api
description: Dermstore API for Dermstore (dermstore.com, the US skincare and beauty retailer, shipping to the US and Canada) - skincare prices and offers by brand, a product's price next to Dermstore's RRP as Dermstore gives it, discount_percent computed by Scavio from the two, and the offer text Dermstore attaches to the product (in the Holiday Beauty Event captured 2026-11-25 EltaMD read "20% Off With Code JOY + $22 Gift", Medik8 "30% Off With Code JOY + Gift", while SkinCeuticals read "Earn 10% Back + $25 Gift", double points instead of a code, as Dermstore states it); US prices in USD or Dermstore's own Canadian dollar prices with country us or ca (EltaMD UV Clear SPF 46 1.7 fl. oz. read 46 USD and 65.78 CAD); Dermstore's current offers with the code, gift, spend threshold and END time it states (no start date exists); search by keyword or Dermstore SKU, up to 200 per page, 7 sorts and filters by brand, skin type, concern, SPF band, key ingredient, preference, gender, price, rating and discount, with Dermstore's facet counts on request, mapped keywords (sunscreen, a brand, an ingredient) resolved to the page Dermstore sends them to in resolved_from; any Dermstore list page by path (category, brand, sale, an offer page, gift sets, ingredient); one product with UPC, every shade, size or strength with its own price, stock and UPC, ingredients, directions, auto-replenish discounts, loyalty points, rating, review count and the 10 latest reviews (no names); search suggestions, the 235-brand directory and the category tree. 7 endpoints, 1 credit per call. No full review feed, Q&A, member (VIP) prices, cart or code-applied prices, price history or coupon start dates.
version: 1.0.0
tags: dermstore, dermstore-com, dermstore-api, dermstore-prices, dermstore-price-api, dermstore-product-data, dermstore-skincare, dermstore-skincare-prices, dermstore-offers, dermstore-coupon-codes, dermstore-black-friday, dermstore-holiday-beauty-event, dermstore-sale, dermstore-brands, dermstore-skinceuticals, dermstore-eltamd, dermstore-canada, dermstore-cad, dermstore-reviews, dermstore-ingredients, dermstore-upc, dermstore-auto-replenish, skincare, skincare-prices, skincare-price-api, skincare-price-comparison, professional-skincare, beauty, beauty-prices, sunscreen, retinol, shades, upc, variant-data, product-search, product-data, price-monitoring, price-comparison, us-retail, usd, cad, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/dermstore-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api
---

# Dermstore API - Skincare Prices, Offers, Product Data

Read Dermstore (dermstore.com, the US skincare and beauty retailer, shipping to the US and Canada) for the US (USD) or Canada (Dermstore's own CAD prices): search, any list page, one product in full with every variant, search suggestions, the current offers, the brand directory and the category tree. Every answer comes as Dermstore's page shows it to a visitor without an account. All 7 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Dermstore shows to any visitor and returns them as JSON for analysis. It uses no Dermstore account, no cart, no checkout, no code redemption and no rewards login.

**The job this skill is for: Dermstore skincare prices and offers by brand.** What a product costs on Dermstore today, Dermstore's RRP as it gives it, and which offer Dermstore attaches to it as labelled (a code rate, a gift with a spend threshold, or points), per product and per brand, in the US and in Canada, next to the same product and size at Sephora, Ulta and Amazon where that match is evidenced. Captured 2026-11-25, during Dermstore's Holiday Beauty Event: EltaMD UV Clear Broad-Spectrum SPF 46 (1.7 fl. oz.) (SKU `11370303`) read `price` 46 and `rrp` 46 USD with the offer "20% Off With Code JOY + $22 Gift"; the same SKU read 65.78 CAD with `country` `ca`. Medik8 read "30% Off With Code JOY + Gift" and La Roche-Posay "25% Off With Code JOY + Gift", while SkinCeuticals read "Earn 10% Back + $25 Gift": "Earn double points on SkinCeuticals", no code discount, as Dermstore states it. The code rates differ by brand, so read the offer per product or per brand, never assume one sitewide rate.

Ten limits shape every answer, so say them plainly:
- **1 credit per call** on every endpoint. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **RRP as given, discount computed.** `rrp` is Dermstore's RRP exactly as Dermstore gives it. `discount_percent` is computed by Scavio from `price` and `rrp`, and only when the RRP is above the price; otherwise it is `null`. During a code event the page price usually equals the RRP (every captured product read `discount_percent` `null`): the code discount is applied in Dermstore's cart and is not in `price`.
- **Code prices are arithmetic, not data.** A price after a code (46 USD less 20% with code JOY = 36.80 USD) is your own computation from the offer text: label it "computed, not checked out". Member (VIP) prices and cart-only discounts are not returned.
- **Offers have end times only.** `/offers` gives `ends` (Dermstore's stated end time, ISO 8601 UTC) and the offer text; Dermstore gives no start date. A product's `offer` carries its dates only inside its text. Quote `ends` and the text as given, side by side, when they read differently (the goop beauty offer read `ends` `2026-11-30T08:00:00.000Z` while its text said "ends 11/30/2026 11:59PM PT").
- **Mapped keywords resolve to a page.** Dermstore sends some keywords (a brand such as eltamd, an ingredient such as retinol, a category or landing such as sunscreen) to one of its pages instead of search results; `/search` then returns that page's products and says so in `resolved_from` {`type` (`brand`, `ingredient`, `category`, `landing` or `product`), `path`, `listed_path`, `url`, `title`, `sku`} and in `notes`. Always check `resolved_from` before calling an answer "search results for q".
- **Variants carry their own price.** A product's `variants[]` (shades, sizes, strengths) each have their own `sku`, `price`, `rrp`, `discount_percent`, `in_stock`, `upc` and `loyalty_points`. A list item's `price_from` is the lowest variant price when it is below the item's `price`. Compare the variant, never the product range.
- **Two markets.** `country` `us` (default, USD) or `ca` (CAD, Dermstore's own Canadian dollar prices, not converted by Scavio). Anything else is a `400`, not charged. Same catalogue, same SKUs.
- **10 latest reviews only.** `/product` returns `rating` and `review_count` (Dermstore's figures) and `recent_reviews` [{`rating`, `date`, `text`}]: the 10 latest reviews the product page shows, `text` can be `null`, no reviewer names. There is no review feed or review paging, and no Q&A.
- **UPC as Dermstore gives it.** `upc` is the barcode Dermstore lists; `null` when it lists none (sets and pre-release items). Use it to match the same product elsewhere where the other retailer returns a barcode.
- **No history.** Nothing is cached or kept: store each answer with its `fetched_at` for your own series.

Dermstore publishes no public API for its catalogue, prices, stock or reviews. Its affiliate programme runs on Awin, which Dermstore says offers product feeds to approved publishers; this skill reads the public product, list and offer pages with one Scavio key and needs no affiliate approval. Other vendors offer Dermstore data tools; this skill reads Dermstore's own public pages.

Dermstore was founded in 1999, and THG plc agreed to buy it from Target Corporation for $350m in cash (THG release, Dec 29, 2020), completing the acquisition in February 2021 (THG release, Feb 2, 2021). THG reports THG Beauty revenue, not Dermstore's. Quote these with their source, never from the samples.

See also: for the same product at other retailers use `sephora-product-data` (Sephora), `ulta-beauty-api` (Ulta Beauty) and `amazon-product-data` (Amazon). Same product and size only: match on UPC where both sides return one, otherwise brand + name + size in both titles, each price with its seller and date. Professional brands are often absent from those retailers (on 2026-11-25 Scavio's Ulta search returned no SkinCeuticals product, its Ulta and Sephora searches returned no EltaMD product, and Amazon's top 5 results had EltaMD but no SkinCeuticals product): report what each search returned on that date, never "only at Dermstore".

## When to trigger

Use this skill when the user asks to:
- Read a Dermstore product's price, RRP, discount, stock, UPC and offer by SKU or link
- Compare every shade, size or strength of one Dermstore product, each with its own price and stock
- Read the offer Dermstore attaches to each brand (code rate, gift with threshold, points) and its end time
- List Dermstore's current offers and codes (Black Friday, Holiday Beauty Event) with their end times
- Search Dermstore by keyword or SKU, sorted by price, popularity, newest or discount, filtered by brand, skin type, concern, SPF band, key ingredient, preference, price, rating or discount
- List any Dermstore page: a brand, a category, sale, an offer page, gift sets or an ingredient page
- Put Dermstore's US price next to its Canadian price for the same SKU
- Put a Dermstore product next to the same product and size at Sephora, Ulta or Amazon
- Read a product's rating, review count and 10 latest reviews, ingredients, directions and auto-replenish discounts
- List Dermstore's brands or its category tree

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, suggestions took under 1 second, brands, categories and offers about 2, search, list and product 2 to 7, and a mapped-keyword search 18. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/dermstore/search` | Products for keywords or a Dermstore SKU: price, RRP, discount, lowest variant price, stock, rating, review count and the offer per product; up to 200 per page, 7 sorts, filters, facets on request; `resolved_from` when Dermstore maps the keyword to a page | 1 |
| `POST /api/v1/dermstore/list` | The products of any Dermstore list page by path or link (brand, category, sale, offer page, gift sets, ingredient), same fields, sorts and filters as search | 1 |
| `POST /api/v1/dermstore/product` | One product by SKU or link: price, RRP, discount, UPC, every variant with its own price, stock and UPC, ingredients, directions, auto-replenish plans, loyalty points, the offer, HSA/FSA tag, rating, review count, the 10 latest reviews | 1 |
| `POST /api/v1/dermstore/suggestions` | Dermstore's search-box suggestions: suggested searches, corrections and up to 5 products with price | 1 |
| `POST /api/v1/dermstore/offers` | Dermstore's current offers as its coupon-codes page lists them: title, text, code, gift, spend threshold, end time, the offer's list path | 1 |
| `POST /api/v1/dermstore/brands` | Dermstore's A-Z brand directory (235 brands captured), optionally one letter | 1 |
| `POST /api/v1/dermstore/categories` | Dermstore's category tree as its site navigation shows it (11 menus, 229 nodes captured) | 1 |

## Markets

Every endpoint takes `country` and every answer carries `market` {`country`, `currency`, `shipping_destination`}.

| `country` | Currency | Ships to | Captured |
|---|---|---|---|
| `us` (default) | USD | US | EltaMD UV Clear SPF 46 (1.7 fl. oz.) 46, the Exclusive UV Clear SPF 46 Duo 88 |
| `ca` | CAD (Dermstore's own prices) | Canada | the same SKUs 65.78 and 125.84; SkinCeuticals C E Ferulic (1 fl. oz.) 264.55 |

Same catalogue and SKUs in both markets; the offer text read the same in both captures (with its amounts as Dermstore writes them, in dollars). In the captures the CAD price read about 1.43 times the USD price (65.78 / 46, 125.84 / 88: arithmetic). Show each price with its currency, never convert one into the other.

## Prices, offers, variants and reviews

Every list item (search, list) carries:

| Field | Meaning |
|---|---|
| `price` | Dermstore's price for a visitor without an account, in the market's currency |
| `rrp` | Dermstore's RRP, as Dermstore gives it |
| `discount_percent` | Computed by Scavio from `price` and `rrp`, only when the RRP is above the price; `null` otherwise |
| `price_from` | The lowest variant price when it is below `price` (EltaMD UV Clear SPF 46 (3.7 fl. oz.) at 78 USD read `price_from` 46); `null` otherwise |
| `in_stock` | Dermstore's online availability for the market, as given |
| `rating`, `review_count` | Dermstore's figures for the product |
| `offer` | {`title`, `description`, `free_gift`, `url`}: Dermstore's promotion text for the product, as given; dates only inside the text |
| `variants_count`, `options` | How many variants and which option types (`Size`, `Option`, shade) |

- **Offers per brand:** a product's `offer` is its brand's event offer. Captured 2026-11-25 (US): EltaMD "20% Off With Code JOY + $22 Gift" (gift "when you spend $115 or more on the brand"), Medik8 "30% Off With Code JOY + Gift" ($100 threshold), La Roche-Posay "25% Off With Code JOY + Gift" ($50), SkinCeuticals "Earn 10% Back + $25 Gift" (double points, $175). `/offers` listed 10 more, e.g. jane iredale 25% with code JOY, SkinMedica 20%, goop beauty 30%, Supergoop! 20%, Vacation 25%, Susanne Kaufmann 30%, Alpha-H 25%, Vichy 25%, and iS Clinical "Discount Applied at Cart" with `code` `null`. Quote each one in Dermstore's words with the capture date.
- **Gifts:** Dermstore's terms give one free gift per transaction, subject to availability; `free_gift` and `gift` carry the gift and the value as Dermstore writes it ("Worth $22.00", "($22 Value)").
- **Variants (product):** `variants[]` {`sku`, `name`, `option_type`, `option`, `shade_colour`, `price`, `rrp`, `discount_percent`, `in_stock`, `availability_message`, `upc`, `preorder`, `max_per_order`, `loyalty_points`}. The product's own fields are those of the SKU asked for.
- **Auto-replenish (product):** `auto_replenish[]` {`discount_first`, `discount_recurring`, `price_first`, `price_recurring`, `frequencies`}: Dermstore's subscribe-and-save plans, as given. Medik8 Crystal Retinal 20 read 30% off the first order (86.10 USD) and 15% recurring (104.55 USD) on 1, 2, 3, 6 months or 1 year.
- **Loyalty points (product):** `loyalty_points` per product and per variant, as Dermstore shows them (615 on a 123 USD product).
- **HSA/FSA (product):** `hsa_fsa` is Dermstore's eligibility tag as shown; never say anything about tax treatment.
- **Reviews (product):** `rating`, `review_count` and `recent_reviews` (10 latest, `text` may be `null`). Report the counts and stars; quote a review's text only as that reviewer's own words.

## Workflow

1. **Find products.** `/search` with `q` (keywords or a SKU), `country`, and optionally `sort`, filters and `page_size`. Check `resolved_from`: when set, the results are the products of the page Dermstore maps the keyword to. Each `items[].sku` is the input of `/product`.
2. **Read one product.** `/product` with `sku` (or `url`, an `items[].url` link): every variant with its own price, stock and UPC, the offer, auto-replenish, reviews.
3. **Read a brand's offer.** `/offers` for the current offers with `code`, `gift`, `threshold` and `ends`; send an offer's `list_path` to `/list` (`path`) for the products it covers. Or `/brands` for a brand's `path`, then `/list`.
4. **Narrow a list.** `/search` or `/list` with `include_facets` `true` gives Dermstore's filter options with counts; a facet's `filter` names the input it maps to (`skin_type`, `concern`, `spf`, `key_ingredient`, `preference`, `gender`, `min_price` / `max_price`, `min_rating`), `null` when there is no input for it. Send `options[].value` exactly (`Fragrance_Free`, `SPF 30+`).
5. **US vs Canada.** The same `/product` or `/search` call with `country` `ca`. Show both prices with their currency and date.
6. **Compare retailers.** Search the same brand and product on `sephora-product-data`, `ulta-beauty-api` or `amazon-product-data`; keep a row only where the UPC matches, or brand, name and size all match, and show each price with its seller and date. When a search returns no match, say so for that date.
7. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Every endpoint

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | `us` (USD) or `ca` (Dermstore's own CAD prices) |

### Search (`/search`) and list (`/list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required (search) | Keywords or a Dermstore SKU (up to 200 chars). A keyword Dermstore maps to a page returns that page's products, with `resolved_from` |
| `path` | string | one of (list) | A Dermstore list page path, as in its dermstore.com/c/ link: `/skin-care`, `/brands/eltamd`, `/sale`, `/shop/black-friday/30-off`, `/gift-sets`, `/ingredient/retinol`. Paths come from `/categories`, `/brands` and `/offers` |
| `url` | string | one of (list) | A Dermstore list page link, `https://www.dermstore.com/c/<page>/`, instead of `path` |
| `page` | integer | 1 | Page; at most 10,000 positions (`page` x `page_size`) |
| `page_size` | integer | 60 | 1-200 products per page |
| `sort` | string | `relevance` | `relevance`, `popularity`, `price_low`, `price_high`, `name`, `newest`, `discount` (highest percent off first): Dermstore's sort menu |
| `brand` | string or list | none | Brand as Dermstore names it (`EltaMD`) |
| `skin_type` | string or list | none | `Dry Skin`, `Oily Skin`, `Sensitive Skin` ... as Dermstore lists it |
| `concern` | string or list | none | `Aging`, `Sun Damage`, `Dehydration` ... |
| `spf` | string or list | none | `SPF 30+`, `SPF 50+`, `No SPF` ... |
| `key_ingredient` | string or list | none | `Retinol`, `Hyaluronic Acid`, `Niacinamide` ... |
| `preference` | string or list | none | `Clean`, `Vegan`, `Fragrance_Free` ... (exact facet values) |
| `gender` | string or list | none | As Dermstore lists it (`Unisex`) |
| `min_price`, `max_price` | number | none | Price range in the market's currency |
| `min_rating` | number | none | Lowest average stars (1-5); applied by Dermstore's own filter, a few items can show a rating just below it |
| `min_discount`, `max_discount` | number | none | Percent off Dermstore's RRP (0-100) |
| `include_facets` | boolean | false | Also return Dermstore's filter counts. Still 1 credit |

A list takes up to 10 values. An editorial page without a product list is listed through its view-all page (`listed_path`, with a note).

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | one of | A Dermstore SKU (`items[].sku` or `variants[].sku`, `11289609`) |
| `url` | string | one of | A Dermstore product link, `https://www.dermstore.com/p/<name>/<sku>/` |

### Suggestions, offers, brands, categories

`/suggestions` takes `q` (the text typed so far, up to 100 chars). `/offers` and `/categories` take only `country`. `/brands` takes an optional `letter` (`A`-`Z`, or `0-9`).

## Examples

### One product with its variants and offer

```bash
curl -X POST https://api.scavio.dev/api/v1/dermstore/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "13806521"}'
```

Captured `data` (2026-11-25; `variants` cut to 3 of 6, `recent_reviews` to 2 of 10, `description`, `directions`, `ingredients`, `images`, `breadcrumbs` and `notes` dropped):

```json
{
  "market": { "country": "us", "currency": "USD", "shipping_destination": "US" },
  "requested_sku": "13806521",
  "sku": "13806521",
  "name": "Medik8 Crystal Retinal 20 30ml",
  "brand": "Medik8",
  "url": "https://www.dermstore.com/p/medik8-crystal-retinal-20-30ml/13806521/",
  "price": 123,
  "rrp": 123,
  "discount_percent": null,
  "currency": "USD",
  "in_stock": true,
  "availability_message": "In stock | Usually dispatched within 24 hours",
  "upc": "818625025847",
  "option_type": "Option",
  "option": "Retinal 20",
  "variants": [
    { "sku": "12810716", "name": "Medik8 Crystal Retinal 1 Serum 30ml", "option_type": "Option", "option": "Retinal 1", "shade_colour": null, "price": 56, "rrp": 56, "discount_percent": null, "in_stock": true, "upc": "818625023379", "preorder": false, "max_per_order": null, "loyalty_points": 280 },
    { "sku": "13806521", "name": "Medik8 Crystal Retinal 20 30ml", "option_type": "Option", "option": "Retinal 20", "shade_colour": null, "price": 123, "rrp": 123, "discount_percent": null, "in_stock": true, "upc": "818625025847", "preorder": false, "max_per_order": null, "loyalty_points": 615 },
    { "sku": "15451254", "name": "Medik8 Crystal Retinal 24 30ml", "option_type": "Option", "option": "Retinal 24", "shade_colour": null, "price": 137, "rrp": 137, "discount_percent": null, "in_stock": true, "upc": "818625026899", "preorder": false, "max_per_order": null, "loyalty_points": 685 }
  ],
  "volume": "30ml",
  "auto_replenish": [
    { "discount_first": 30, "discount_recurring": 15, "price_first": 86.1, "price_recurring": 104.55, "frequencies": ["1 month", "2 months", "3 months", "6 months", "1 year"] },
    { "discount_first": 15, "discount_recurring": 15, "price_first": 104.55, "price_recurring": 104.55, "frequencies": ["4 months"] }
  ],
  "loyalty_points": 615,
  "offer": {
    "title": "30% Off With Code JOY + Gift",
    "description": "Enjoy 30% off Medik8 with code JOY. Plus, receive a Medik8 C-Tetra Advanced 4ml ($11 Value) when you spend $100 or more on the brand. Complimentary gift will be awarded at the cart, while supplies last. Holiday Beauty Event ends 11/30/2026 11:59PM PT.",
    "free_gift": "Medik8 C-Tetra Advanced 4ml (Worth $11.00)",
    "url": "https://www.dermstore.com/c/brands/medik8/view-all/"
  },
  "hsa_fsa": true,
  "rating": 4.74,
  "review_count": 19,
  "recent_reviews": [
    { "rating": 5, "date": "2026-11-16", "text": "My skin seems to be much softer after using this for several months" },
    { "rating": 5, "date": "2026-11-05", "text": "It has taken me a year of slowing increasing the strength to 20. This is my go to product. Doesn’t disappoint" }
  ]
}
```

The six strengths ran from 56 to 137 USD, each with its own UPC and points. `price` equals `rrp`, so `discount_percent` is `null`: the 30% is a code applied in Dermstore's cart (123 x 0.70 = 86.10 USD, computed, not checked out). An unknown SKU is a charged `404`.

### The same SKU in Canada

```bash
curl -X POST https://api.scavio.dev/api/v1/dermstore/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "11289609", "country": "ca"}'
```

Captured (2026-11-25): `market` {`country` `ca`, `currency` `CAD`}, SkinCeuticals C E Ferulic (1 fl. oz.) - New Patent-Pending Formula, `price` 264.55, `rrp` 264.55 CAD, `upc` `635494263008`, `max_per_order` 3, `loyalty_points` 1850, `auto_replenish` 5% first and recurring (251.32 CAD), `rating` 4.53 from `review_count` 13,455, and the offer "Earn 10% Back + $25 Gift": "Earn double points on SkinCeuticals. Double Points = 10% back in rewards to spend on future purchases at Dermstore.com . Participating products only. Plus, receive a SkinCeuticals A.G.E. Interrupter Ultra Serum 4ml ($25 Value) when you spend $175 or more on the brand." No code discount on this brand, as Dermstore states it.

`/search` `{"q": "uv clear spf 46"}` in both markets: `total` 74 each; EltaMD UV Clear Broad-Spectrum SPF 46 (1.7 fl. oz.) (SKU `11370303`) 46 USD / 65.78 CAD, the 3.7 fl. oz. (`16088535`) 78 USD / 111.54 CAD, the Exclusive UV Clear SPF 46 Broad-Spectrum Duo (`12538013`) 88 USD / 125.84 CAD, all with "20% Off With Code JOY + $22 Gift".

### A mapped keyword

```bash
curl -X POST https://api.scavio.dev/api/v1/dermstore/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "sunscreen", "page_size": 10}'
```

Captured (2026-11-25): `resolved_from` {`type` `landing`, `path` `/sunscreen`, `listed_path` `/sunscreen/view-all`, `url` `https://www.dermstore.com/c/sunscreen/`, `title` "SPF & Sunblock | Dermstore", `sku` `null`}, `total` 488, `total_pages` 49, and the note "Dermstore maps "sunscreen" to its landing page /sunscreen: the results are that page's products (resolved_from), as Dermstore's own search shows them." First three: the EltaMD duo at 88 USD, SkinCeuticals Future Mineral UV Defense SPF 50 (1.7 fl. oz.) at 60 USD ("Earn 10% Back + $25 Gift"), La Roche-Posay Anthelios Ultra Light Fluid SPF 60 (1.7 fl. oz.) at 35.99 USD ("25% Off With Code JOY + Gift").

### Offers with end times

```bash
curl -X POST https://api.scavio.dev/api/v1/dermstore/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-25; `offers` cut to 3 of 10, `notes` dropped):

```json
{
  "market": { "country": "us", "currency": "USD", "shipping_destination": "US" },
  "count": 10,
  "offers": [
    {
      "title": "SkinMedica Growth Factor Authority Set ($198 Value)",
      "description": "Enjoy 20% off SkinMedica with code JOY. Plus, receive a SkinMedica Growth Factor Authority Set ($198 Value) when you spend $300 or more on the brand. Complimentary gift will be awarded at the cart, while supplies last. Holiday Beauty Event ends 11/30/2026 11:59PM PT.",
      "code": "JOY",
      "gift": "SkinMedica Growth Factor Authority Set ($198 Value)",
      "threshold": "$300 or more on the brand",
      "ends": "2026-12-01T08:00:00.000Z",
      "url": "https://www.dermstore.com/c/brands/skinmedica/",
      "list_path": "/brands/skinmedica"
    },
    {
      "title": "iS Clinical Active Serum 3.75ml ($22 Value)",
      "description": "The Holiday Beauty Event | iS Clinical—Discount Applied at Cart. Valid on participating products only. Plus, receive an iS Clinical Active Serum 3.75ml ($22 Value) when you spend $125 or more on the brand. Complimentary gift will be awarded at the cart, while supplies last. Holiday Beauty Event ends 11/30/2026 11:59PM PT.",
      "code": null,
      "gift": "iS Clinical Active Serum 3.75ml ($22 Value)",
      "threshold": "$125 or more on the brand",
      "ends": "2026-12-01T08:00:00.000Z",
      "url": "https://www.dermstore.com/c/brands/is-clinical/",
      "list_path": "/brands/is-clinical"
    },
    {
      "title": "goop beauty Lift + Depuff Eye Masks 1pk ($5 Value)",
      "description": "Enjoy 30% off goop beauty with code JOY. Plus, receive a goop beauty Lift + Depuff Eye Masks 1pk ($5 Value) when you spend $100 or more on the brand. Complimentary gift will be awarded at the cart. Offer valid for a limited time only, while supplies last. Holiday Beauty Event ends 11/30/2026 11:59PM PT.",
      "code": "JOY",
      "gift": "goop beauty Lift + Depuff Eye Masks 1pk ($5 Value)",
      "threshold": "$100 or more on the brand",
      "ends": "2026-11-30T08:00:00.000Z",
      "url": "https://www.dermstore.com/c/brands/goop-beauty/view-all/",
      "list_path": "/brands/goop-beauty/view-all"
    }
  ]
}
```

`code`, `gift` and `threshold` are read from the offer text when it states them (`null` otherwise). `ends` is Dermstore's end time; there is no start date. Send `list_path` to `/list` for the brand's products.

### List, suggestions, brands, categories

- `/list` `{"path": "/brands/eltamd", "include_facets": true, "page_size": 10}`: `total` 55, `total_pages` 6; first EltaMD UV Skin Recovery Red Color Correcting Green Tint SPF 50 (1.7 fl. oz.) at 53 USD with `price_from` 51. `facets` included Skin Type (`skin_type`), Skincare Concern (`concern`: Sun Damage 29), SPF Content (`spf`: SPF 30+ 12, SPF 50+ 8), Key Ingredients (`key_ingredient`), Preferences (`preference`: Fragrance_Free 30), Gender (`gender`), Price (`min_price` / `max_price` ranges) and Average Reviews (`min_rating`), plus Skincare Product Type (Face Sunscreen 26) with `filter` `null`: no input for it.
- `/suggestions` `{"q": "eltamd"}`: `terms` "eltamd", "eltamd uv", "eltamd uv daily", "eltamd skin", "eltamd skin recovery"; 5 `products`, first EltaMD AM Restore Moisturizer (1.7 fl. oz.) at 51 USD.
- `/brands` `{}`: `total_brands` 235, each {`name`, `path`, `url`, `letter`} (`111SKIN` under `0-9`, `/brands/111skin`).
- `/categories` `{}`: 11 menus (Holiday Beauty Event `/shop/black-friday`, Brands, Bestsellers, Skin Care `/skin-care`, Beauty, HSA/FSA Shop, Sale & Offers `/sale`, Exclusives, New ...), `total_categories` 229. Seasonal menus change.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def dermstore(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/dermstore/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. A brand's products with the offer Dermstore attaches (1 credit)
eltamd = dermstore("list", {"path": "/brands/eltamd", "sort": "price_low", "page_size": 60})["data"]
for i in eltamd["items"][:5]:
    offer = (i["offer"] or {}).get("title")
    print(i["sku"], i["name"], i["price"], i["rrp"], i["discount_percent"], offer)

# 2. The same SKU in the US and Canada (1 credit each)
for country in ("us", "ca"):
    p = dermstore("product", {"sku": "11370303", "country": country})["data"]
    print(country, p["price"], p["currency"], p["upc"], [(v["option"], v["price"]) for v in p["variants"]])

# 3. Current offers with end times (1 credit)
for o in dermstore("offers", {})["data"]["offers"]:
    print(o["title"], o["code"], o["threshold"], o["ends"], o["list_path"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `currency`, `shipping_destination`} and `notes`.

- **item** (search, list) - `position`, `sku`, `name`, `brand`, `url`, `image`, `price`, `rrp`, `discount_percent`, `price_from`, `currency`, `in_stock`, `rating`, `review_count`, `offer` {`title`, `description`, `free_gift`, `url`}, `variants_count`, `options`.
- **search** - `query`, `resolved_from` (or `null`), `corrected_query`, `total`, `total_pages`, `page`, `page_size`, `has_more`, `count`, `sort`, `filters_applied`, `items[]`, `facets` (with `include_facets`) [{`filter`, `label`, `type`, `options` [{`value`, `label`, `count`} or {`label`, `from`, `to`, `count`}]}].
- **list** - `path`, `listed_path`, `url`, then as search from `total`.
- **product** - `requested_sku`, `sku`, `product_sku`, `name`, `product_name`, `brand`, `url`, `price`, `rrp`, `discount_percent`, `currency`, `in_stock`, `availability_message`, `upc`, `option_type`, `option`, `variants[]`, `subtitle`, `description`, `key_benefits`, `directions`, `ingredients`, `at_a_glance`, `volume`, `faq`, `images`, `offer`, `auto_replenish[]`, `loyalty_points`, `max_per_order`, `preorder`, `hsa_fsa`, `rating`, `review_count`, `recent_reviews[]` {`rating`, `date`, `text`}, `breadcrumbs`.
- **suggestions** - `query`, `count`, `terms[]`, `corrections[]`, `products[]` {`sku`, `name`, `url`, `image`, `price`, `rrp`, `discount_percent`, `currency`, `rating`, `review_count`}.
- **offers** - `count`, `offers[]` {`title`, `description`, `code`, `gift`, `threshold`, `ends`, `url`, `list_path`}.
- **brands** - `letter`, `total_brands`, `count`, `brands[]` {`name`, `path`, `url`, `letter`}.
- **categories** - `count`, `total_categories`, `categories[]` {`name`, `path`, `url`, `children[]`}.

## Guardrails

- Name it "Dermstore (dermstore.com, the US skincare and beauty retailer, shipping to the US and Canada)" on first mention, "Dermstore" after that.
- Prices: quote `price` with its currency, the market and the `fetched_at` date ("listed on dermstore.com on Nov 25, 2026, before tax"). `rrp` is "Dermstore's RRP, as Dermstore gives it"; `discount_percent` is "computed by Scavio from Dermstore's price and RRP". A code price is your own arithmetic: label it computed and not checked out.
- Offers: quote code, rate, gift, gift value and threshold exactly as Dermstore writes them, with `ends` and the capture date. No countdowns, urgency or "real deal" / "fake discount" language. SkinCeuticals and any other points offer: say points, as Dermstore states it, never a percent off.
- Comparisons: same product and size only (UPC where both sides return it, else brand + name + size), each price with its seller, currency and date; show the numbers and their difference only. Never call a retailer or a price the cheapest, a deal, a bargain or a rip-off. When another retailer's search shows no match, report that search's result on that date, never "only at Dermstore".
- Descriptive only: never say a product or seller is authentic, genuine, counterfeit, authorized or unauthorized, never give a legit or scam verdict on any retailer, and never make MAP claims. For SkinCeuticals' retailers use only the brand's own retailer list, if at all.
- No efficacy, SPF, medical or HSA/FSA tax claims. Report SPF bands, concerns, ingredients and the `hsa_fsa` tag as Dermstore labels them; quote review text only as that reviewer's own words.
- Reviews: counts, stars, dates and text as returned; no reviewer names are returned, never try to identify reviewers. Do not republish Dermstore product photos or descriptions at length; link products by `url` instead.
- Names: use "Dermstore" only for dermstore.com; never treat lookalike domains or similarly named sites as Dermstore.
- Terms: Scavio does not collect or store Dermstore data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Dermstore's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, RRPs, offers, codes, end dates, SKUs, UPCs or reviews. Only return what the API returned, with the `fetched_at` time and the product `url`.
- Not available: a full review feed or review paging (only the 10 latest via product), Q&A, member (VIP) prices, cart or checkout prices, code-applied prices, price history (store your own), coupon start dates.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` other than `us` or `ca`; search without `q`; list without `path` or `url`, or with both, a path that is not a Dermstore list page (a product, search or account page), a link that is not a dermstore.com/c/ page; product without `sku` or `url`, or with both, a SKU that is not digits, a link that is not a dermstore.com/p/ product link; `page` past 10,000 positions; `page_size` above 200; an unknown `sort`; `min_price` above `max_price`; `min_discount` above `max_discount`; more than 10 values in a filter list; a `letter` that is not A-Z or 0-9.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Dermstore has no product with SKU <sku>.", "Dermstore has no list page at <path>.", "Dermstore's page <path> has no product list.". Take SKUs and paths from a previous answer rather than guessing them. A search with no matches is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api).
- `502` means Dermstore data was temporarily unavailable ("Dermstore is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Dermstore is busy ("Dermstore is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.88.0
npm install scavio@0.89.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.dermstore.search({ q: "uv clear spf 46", country: "ca" });
const { data: brand } = await scavio.dermstore.list({ path: "/brands/eltamd", sort: "price_low" });
const { data: product } = await scavio.dermstore.product({ sku: "13806521" });
const { data: offers } = await scavio.dermstore.offers();
const { data: brands } = await scavio.dermstore.brands({ letter: "E" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.dermstore.search(...)`, `list`, `product`, `suggestions`, `offers`, `brands` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_dermstore`, `get_dermstore_list`, `get_dermstore_product`, `get_dermstore_suggestions`, `get_dermstore_offers`, `get_dermstore_brands` and `get_dermstore_categories`. Dermstore is opt-in: add `dermstore` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.88.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,dermstore"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/dermstore-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api), [list](https://scavio.dev/docs/dermstore-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api), [product](https://scavio.dev/docs/dermstore-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api), [suggestions](https://scavio.dev/docs/dermstore-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api), [offers](https://scavio.dev/docs/dermstore-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api), [brands](https://scavio.dev/docs/dermstore-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api), [categories](https://scavio.dev/docs/dermstore-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api). Overview: [Dermstore API](https://scavio.dev/dermstore-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dermstore-skincare-prices-api).
