---
name: williams-sonoma-api
description: Williams-Sonoma API for the Williams-Sonoma, Inc. brands (Williams Sonoma, Pottery Barn, Pottery Barn Kids, Pottery Barn Teen, West Elm, Rejuvenation and Mark and Graham; US in USD, and the Canadian Williams Sonoma, Pottery Barn and West Elm sites in CAD for product) - what a piece costs on the brand's site today, per SKU, with the regular price, the sale or special price and the brand's own discount type (on 2026-11-27 the Pottery Barn Gabrielle Bergere Sofa (63") read $2,319 against a $2,899 regular price, and CAD 3,710 against CAD 4,638 on potterybarn.ca; the WUSTHOF Classic Chef's Knife at Williams Sonoma read $99 to $200 across its sizes and colors, 564 ratings at 4.81 stars), whether each SKU is on hand, back-ordered (with the date) or not available, its delivery services (standard, rush, white glove) and dimensions; the fabric configurator of a made-to-order Pottery Barn piece (the Gabrielle Sofa base SKU 4889446 lists 50 fabrics with fiber content, rub count and price tier, $1,999 to $2,899 across fabrics, a 27-51 production lead time as given); standard-delivery dates to a US ZIP per SKU with the holiday order cutoff (Christmas cutoffs 2026-12-17 and 2026-12-19 for two knife SKUs to 60611); the online stock ranges per SKU (401+, 1-10, 71-80 within 2 weeks), national; store pickup yes or no per SKU at up to 10 stores with the ship-to-store window; the stores of every brand near a ZIP or point with this week's hours; the stores showing one furniture piece on their floor; the category tree with the Sale and Black Friday listings; Pottery Barn category listings and Williams Sonoma or Pottery Barn keyword search, page 1 (20 products) with total, price range, regular price, sale price, limited-time-offer flag and max percent off; the day's most searched terms with counts; Williams Sonoma customer reviews newest first with the rating distribution, without reviewer names. 12 endpoints, 1 credit per call, 5 for search and category. Prices national (the same at every ZIP and store). No UPCs, unit counts per store, West Elm search, reviews on the other brands, page 2 of a listing, price history or checkout.
version: 1.0.0
tags: williams-sonoma, williams-sonoma-com, williams-sonoma-api, williams-sonoma-prices, williams-sonoma-sale, williams-sonoma-reviews, williams-sonoma-stores, williams-sonoma-inc, pottery-barn, potterybarn, pottery-barn-api, pottery-barn-prices, pottery-barn-sale, pottery-barn-kids, pottery-barn-teen, pbteen, west-elm, westelm, west-elm-api, west-elm-prices, rejuvenation, mark-and-graham, furniture-prices, home-furnishings, cookware-prices, kitchenware, sofa-prices, fabric-configurator, made-to-order-furniture, delivery-estimate, holiday-delivery-cutoff, online-stock, store-pickup, floor-samples, store-locator, popular-searches, black-friday-furniture, category-browse, product-search, product-reviews, sku-data, us-retail, canada, usd, cad, price-monitoring, competitor-research, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/williamssonoma-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api
---

# Williams-Sonoma API - Pottery Barn, West Elm Prices, Delivery Dates, Store Pickup

Read the Williams-Sonoma, Inc. brand sites (Williams Sonoma, Pottery Barn, Pottery Barn Kids, Pottery Barn Teen, West Elm, Rejuvenation and Mark and Graham) with one `brand` parameter: one product in full with every SKU's price, regular price, stock state and delivery services, the fabric configurator of a made-to-order piece, standard-delivery dates to a US ZIP, online stock ranges, store pickup per store, the stores near a ZIP or point, the stores showing a furniture piece on their floor, the category tree, category listings, keyword search, the day's most searched terms and Williams Sonoma customer reviews. US sites in USD; the Canadian Williams Sonoma, Pottery Barn and West Elm sites in CAD for product. Every endpoint returns structured JSON at 1 credit per call, 5 for search and category.

**The job this skill is for: Williams-Sonoma, Pottery Barn and West Elm prices, and when a piece can be in your home.** What a sofa, rug or knife costs on the brand's site today, per size and color, whether it is on sale, and the brand's own delivery dates, stock ranges and store pickup. On 2026-11-27 the Pottery Barn Gabrielle Bergere Sofa (63") (`gabrielle-upholstered-sofa`) read $2,319 against a $2,899 regular price (`discount_type` `special`), a `configured` made-to-order piece with configurator base SKU `4889446`, and the same sofa read CAD 3,710 against CAD 4,638 on potterybarn.ca. `/configurator` for `4889446` listed 50 fabrics (Performance Boucle, Ivory, 60% recycled poly, rub count 100,000, price tier F) with a $1,999 to $2,899 price range across fabrics and a production lead time of 27 to 51 as the configurator gives it. `/delivery-estimate` to ZIP 94103 dated the sofa SKU `10464436` 2027-02-26 to 2027-03-12 (`special_order`), and two Williams Sonoma knife SKUs to 60611 2026-12-02 to 2026-12-04 with a Christmas delivery of 2026-12-24 for orders before the published cutoff. `/floor-samples` found the sofa on the floor of 9 Pottery Barn stores within 200 miles of 94103, Village at Corte Madera (12.24 miles) first. The second job is the catalog itself: `/search` for "dutch oven" on Williams Sonoma read 212 products, the first a Le Creuset Signature Enameled Cast Iron Deep Round Oven, 6.5-Qt at $289.95 against $460 (`limited_time_offer`, 37% off). Pair it with `wayfair-api`, `ikea-api` and `ashley-furniture-api` for furniture, and `amazon-product-data` for the same branded cookware.

Eight limits shape every answer, so say them plainly:
- **1 credit per call, 5 for search and category.** Search and category listings are 5 credits; every other endpoint is 1. `credits_used` in the response is the truth. A not-found (`404`) is charged (5 on an unknown category path); a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Not every brand on every endpoint.** Product, delivery-estimate, stock, categories and popular-searches serve all 7 brands; store-pickup, stores and floor-samples the 6 brands with stores (Mark and Graham has none); configurator and category Pottery Barn only; search Williams Sonoma and Pottery Barn only (West Elm search is not served); reviews Williams Sonoma only (the other brands show no ratings or reviews). Anything else is an unbilled `400` naming what is available.
- **Canada is product only.** `market` `ca` reads williams-sonoma.ca, potterybarn.ca and westelm.ca on `/product`, in CAD and English. Every other endpoint is US only.
- **Prices are national.** The brand's online price in the market's currency, the same at every ZIP code and store. `price` is the SKU's current price, `regular_price` the brand's regular price, `discount_type` `sale` or `special` as the brand marks it. Personalization fees and surcharges are their own fields.
- **Stock is a state, a range or a yes / no, never a store count.** `/product` gives each SKU's online state (`on_hand`, `back_ordered` with `back_ordered_date`, `not_available`); `/stock` the brand's national online unit ranges as given (`1-10`, `71-80`, `401+`); `/store-pickup` `available_for_pickup` true or false per store. Never write how many a store has.
- **Listings are page 1.** Search and category return the 20 products of page 1 as the site shows them, with the brand's `total`, facets and sort options. Search comes in the site's relevance order; category takes one of the site's sorts.
- **Reviews are newest first, no filters.** Williams Sonoma reviews, page 1 holding 8 and pages 2-5 holding 30 each, newest to oldest; no sort or star filter (sending either is a `400`). No reviewer names, locations or photos.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

The Williams-Sonoma, Inc. brands have no public API for their catalog, prices, delivery dates or store pickup. Prices and delivery dates are shown on each brand's site, and this skill reads those public pages with one Scavio key.

See also: furniture and home at other retailers `wayfair-api`, `ikea-api`, `ashley-furniture-api`, `maisons-du-monde-api`; the same branded cookware at Amazon `amazon-product-data`, at Target `target-product-data`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Price a sofa, bed, rug, light, knife or pan at Williams Sonoma, Pottery Barn, Pottery Barn Kids, Pottery Barn Teen, West Elm, Rejuvenation or Mark and Graham, per size and color, with the regular price and the sale or special price
- Compare one product's US price with its price on williams-sonoma.ca, potterybarn.ca or westelm.ca
- List the fabrics of a made-to-order Pottery Barn piece with fiber content, rub count, price tier, the price range across fabrics and the production lead time
- Get the brand's standard-delivery dates to a US ZIP for a product or up to 20 SKUs, with the holiday order cutoff
- Read the online stock ranges per SKU (available now, within 2 weeks) and the delivery-region states for a ZIP
- Check whether up to 20 SKUs can be picked up at up to 10 stores, with the ship-to-store window
- Find the Williams Sonoma, Pottery Barn, West Elm, Rejuvenation, Pottery Barn Kids or Pottery Barn Teen stores near a ZIP or point with this week's hours
- Find the stores showing one furniture piece on their floor near a ZIP or point
- Read a brand's category tree, including its Sale and Black Friday listings, list a Pottery Barn category in the site's sorts, or search Williams Sonoma or Pottery Barn by keyword
- Read the day's most searched terms on a brand site, or Williams Sonoma customer reviews with the rating distribution

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

Without `SCAVIO_API_KEY` set, every call below answers `401`. The whole path from
nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit and search and category 5, so 50 credits cover 50 product or delivery calls, or 10 searches.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 1-20 seconds (product pages up to 50, search and category 15-60, reviews 25-60). Allow a client timeout of at least 150 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/williamssonoma/product` | One product by brand + product id or a product link, us or ca: price range, regular price, discount type, rating (Williams Sonoma), messages, dimensions, materials, configurator base SKUs and every SKU (price, regular price, stock state, ship mode, delivery services, pickup services, size) | 1 |
| `POST /api/v1/williamssonoma/configurator` | The fabric configurator of a made-to-order piece: price range across fabrics, production lead time, dimensions, every fabric with content, rub count and price tier | 1 |
| `POST /api/v1/williamssonoma/delivery-estimate` | Standard-delivery dates to a US ZIP for every SKU of a product or up to 20 SKUs, with the holiday order cutoff | 1 |
| `POST /api/v1/williamssonoma/stock` | Online stock ranges per SKU (available now, within 2 weeks), national, and the delivery-region states for a ZIP | 1 |
| `POST /api/v1/williamssonoma/store-pickup` | Pickup yes or no and the ship-to-store window for up to 20 SKUs at up to 10 stores | 1 |
| `POST /api/v1/williamssonoma/stores` | The stores of every brand (or the brands asked for) near a US ZIP or a point, by distance, with this week's hours | 1 |
| `POST /api/v1/williamssonoma/floor-samples` | The stores showing one furniture piece on their floor near a US ZIP or a point | 1 |
| `POST /api/v1/williamssonoma/categories` | A brand's top-level categories, or one category's full subtree with the paths category takes | 1 |
| `POST /api/v1/williamssonoma/category` | One Pottery Barn category listing by path or link, page 1 (20 products), in the site's sorts | 5 |
| `POST /api/v1/williamssonoma/search` | Williams Sonoma or Pottery Barn keyword search, page 1 (20 products) with total, facets and sort options | 5 |
| `POST /api/v1/williamssonoma/popular-searches` | The day's most searched terms on a brand site, with counts as given | 1 |
| `POST /api/v1/williamssonoma/reviews` | Williams Sonoma customer reviews, newest first, with the rating distribution; no reviewer names | 1 |

Every answer carries `brand`, `brand_name`, `market`, `currency`, `language` and `host`.

| `brand` | Site | Served on |
|---|---|---|
| `williams_sonoma` | williams-sonoma.com, williams-sonoma.ca | everything except configurator and category; ca on product |
| `pottery_barn` | potterybarn.com, potterybarn.ca | every endpoint except reviews; ca on product |
| `pottery_barn_kids` | potterybarnkids.com | product, delivery-estimate, stock, store-pickup, stores, floor-samples, categories, popular-searches |
| `pottery_barn_teen` | pbteen.com | the same as Pottery Barn Kids |
| `west_elm` | westelm.com, westelm.ca | the same as Pottery Barn Kids; ca on product |
| `rejuvenation` | rejuvenation.com | the same as Pottery Barn Kids |
| `mark_and_graham` | markandgraham.com | product, delivery-estimate, stock, categories, popular-searches (no stores) |

## Prices: price, regular price and discount type

Per product (`/product`): `price` {`min`, `max`, `regular_min`, `regular_max`, `discount_type`} across the SKUs, and `on_sale`. Per SKU:

| Field | Meaning |
|---|---|
| `price` | The SKU's current price on the brand's site, in the market's currency |
| `regular_price` | The brand's regular price for the SKU |
| `on_sale`, `discount_type` | Whether the SKU is reduced, and the brand's own type: `sale` or `special` |
| `personalization_price` | The brand's personalization price, apart from the price (17 on the WUSTHOF knife) |
| `surcharge` | A surcharge where the brand lists one, apart from the price |
| `stock`, `back_ordered_date` | `on_hand`, `back_ordered` (with the date) or `not_available` |
| `delivery_services`, `white_glove`, `pickup_services` | `standard`, `rush`, `white_glove`, `doorstep`, `room_of_choice`; store pickup services |

On listings (search, category): `price_min`, `price_max`, `regular_price_min`, `regular_price_max`, `sale_price_min`, `sale_price_max`, `price_type` (`regular`, `limited_time_offer`, `set_savings` or `clearance`, as the site marks it) and `max_discount_percent`.

- Quote "$2,319 at potterybarn.com on 2026-11-27 (regular price $2,899, special)", with the date and the brand.
- Quote a size or color's price from `skus[]`, not the product range, when the user names one.
- Report the brand's labels and the arithmetic only. Never judge a regular price or a discount, and never describe how often an item is on sale.
- A configured piece's `/configurator` price is the range across fabrics and options as the configurator gives it; the exact price for one fabric is set in the cart and is not returned.

## Workflow

1. **Find the product.** `/search` with `brand` (`williams_sonoma` or `pottery_barn`) and `query`, or `/categories` then `/category` (Pottery Barn) with a `path` from the tree. Each item's `product_id` is the input of product, delivery-estimate, stock, floor-samples and reviews. For other brands, take the product id from a product link (the part after /products/).
2. **Read it in full.** `/product` with `brand` and `product`, or a product `url` (brand and market are read from it): every SKU with options, price, regular price, stock state and delivery services. Add `market: "ca"` for the Canadian price (Williams Sonoma, Pottery Barn, West Elm).
3. **Made to order.** When `configurator_base_skus` is not empty (a `configured` Pottery Barn piece), call `/configurator` with one `base_sku` for its fabrics, price range and lead time.
4. **When it can arrive.** `/delivery-estimate` with the product (every SKU) or `skus` and a US `zip`: `earliest_date`, `latest_date` and the `holiday` cutoff when the brand publishes one.
5. **How many online.** `/stock` with the product (optionally `skus` and a `zip`): the national unit ranges and the region states for that ZIP.
6. **Pick up in a store.** `/stores` with a `zip` or `latitude` + `longitude` (optionally `brands`) for each store's `pickup_location_code`, then `/store-pickup` with `brand`, `skus` and `stores` (those codes).
7. **See it in person.** `/floor-samples` with a furniture product or `sku` and a `zip` or point: the stores showing it on their floor, nearest first; `radius_extended` true means the brand widened the radius to find one.
8. **What shoppers search.** `/popular-searches` with a `brand`: the day's top terms with their counts.
9. **Reviews.** `/reviews` with a Williams Sonoma `product` and `page` (1-5).
10. **Watching prices or dates:** there is no history. Poll the same SKUs on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Product (`/product`), configurator (`/configurator`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | required unless `url` | One of the 7 brand values above |
| `market` | string | `us` | `us`, or `ca` on product (Williams Sonoma, Pottery Barn, West Elm) |
| `product` | string | one of | The product id: the part after /products/ in a product link (`gabrielle-upholstered-sofa`, `wusthof-classic-chefs-knife`) |
| `url` | string | one of | A product link on the brand site, instead of `product` (not both) |
| `base_sku` | string | configurator: one of | A configurator base SKU (`4889446`, from product `configurator_base_skus`), instead of product / url |

### Delivery estimate (`/delivery-estimate`), stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand`, `product`, `url` | | | As on product (US only) |
| `skus` | string or array | none | Up to 20 SKU ids (product `skus[].sku`, e.g. `1468824`). Delivery: instead of product. Stock: limits the answer to these SKUs of the product |
| `zip` | string or integer | delivery: required; stock: `10001` | A US ZIP code. On stock it picks the delivery-region states; the unit ranges are national |

### Store pickup (`/store-pickup`), stores (`/stores`), floor samples (`/floor-samples`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | pickup: required; floor: required unless `url` | A brand with stores |
| `skus` | string or array | pickup: required | Up to 20 SKU ids |
| `stores` | string or array | pickup: required | Up to 10 store codes as `stores[].pickup_location_code` gives them (`ST:0859`) |
| `brands` | string or array | stores: every brand with stores | Up to 6 of `williams_sonoma`, `pottery_barn`, `pottery_barn_kids`, `pottery_barn_teen`, `west_elm`, `rejuvenation` |
| `zip` | string or integer | one of | A US ZIP code (placed at its Census centroid) |
| `latitude`, `longitude` | number | one of | A point, instead of zip (not both) |
| `radius` | integer | stores 25, floor 50 | Miles, 1-200 |
| `include_outlets` | boolean | `false` | Stores: include outlet stores |
| `product`, `url`, `sku` | string | floor: one of | The furniture piece by product id, link or one SKU id |

### Categories (`/categories`), category (`/category`), search (`/search`), popular searches (`/popular-searches`), reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | required | Categories and popular searches: any brand; category: `pottery_barn`; search: `williams_sonoma` or `pottery_barn`; reviews: `williams_sonoma` (or a product `url`) |
| `category` | string | none | Categories: a top-level category id (`furniture`, `sale`) for its full subtree; leave out for the top-level list |
| `path` | string | category: one of | A category path under /shop/ (`furniture/sofa`, `sale/exclusive-savings`): a tree `path` without /shop/ |
| `url` | string | category: one of | A category link on the brand site, instead of path |
| `sort` | string | `featured` | Category: `featured`, `price_asc`, `price_desc`, `newest`, `best_selling`. Search takes no sort; reviews answer `400` to any sort |
| `query` | string | search: required | Keywords, 1-100 chars |
| `product` | string | reviews: one of | A Williams Sonoma product id, or `url` |
| `page` | integer | 1 | Reviews: 1-5 (page 1 holds 8 reviews, every later page 30) |

## Examples

### Delivery dates to a ZIP, with the holiday cutoff

```bash
curl -X POST https://api.scavio.dev/api/v1/williamssonoma/delivery-estimate \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "williams_sonoma", "skus": ["1468824", "2600435"], "zip": "60611"}'
```

Captured `data` (2026-11-27; the second SKU and `brand_name`, `currency`, `language`, `host` dropped):

```json
{
  "brand": "williams_sonoma",
  "market": "us",
  "zip": "60611",
  "product_id": null,
  "requested_skus": ["1468824", "2600435"],
  "count": 2,
  "skus": [
    {
      "sku": "1468824",
      "ship_mode": "conveyable_mail_order",
      "availability": "in_stock_ready_to_ship",
      "special_order": false,
      "service_level": "standard",
      "earliest_date": "2026-12-02",
      "latest_date": "2026-12-04",
      "min_days": 6,
      "max_days": 8,
      "message": "arrive_by_holiday_estimate_available",
      "holiday": {
        "name": "CHRISTMAS",
        "order_cutoff": "2026-12-19 06:00:00",
        "delivery_dates": [
          { "earliest_date": "2026-12-24", "latest_date": "2026-12-24", "service_level": "standard", "cutoff": "2026-12-19T06:00:00" }
        ]
      }
    }
  ],
  "notes": [
    "Dates are the brand's own standard-delivery estimate to this ZIP code (YYYY-MM-DD), as given. holiday is the brand's holiday order cutoff when it publishes one."
  ]
}
```

SKU `2600435` read the same dates with two published cutoffs (2026-12-17 22:00 and 2026-12-19 06:00). `{"brand": "pottery_barn", "product": "gabrielle-upholstered-sofa", "zip": "94103"}` answered one SKU, `10464436`, `special_order`, 2027-02-26 to 2027-03-12 (92 to 106 days), `holiday` null.

### One product with its SKUs

```bash
curl -X POST https://api.scavio.dev/api/v1/williamssonoma/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "williams_sonoma", "product": "wusthof-classic-chefs-knife"}'
```

Captured `data` (2026-11-27; `skus` cut to 1 of 19, `breadcrumbs`, `notes` and the market fields dropped):

```json
{
  "brand": "williams_sonoma",
  "market": "us",
  "requested_product_id": "wusthof-classic-chefs-knife",
  "product_id": "wusthof-classic-chefs-knife",
  "name": "WÜSTHOF Classic Chef's Knife",
  "url": "https://www.williams-sonoma.com/products/wusthof-classic-chefs-knife/",
  "page_type": "simple",
  "available": true,
  "category_id": "cutlery-chef-knives",
  "price": { "min": 99, "max": 200, "regular_min": 135, "regular_max": 200, "discount_type": "special" },
  "on_sale": true,
  "rating": 4.8138,
  "review_count": 564,
  "flags": ["freeship", "memfreeship"],
  "messages": [],
  "dimensions": [
    { "section": null, "lines": ["6\" Chef's Knife: 6\" blade; 5\" handle; 5.8 oz.", "8\" Chef's Knife: 8\" blade; 5\" handle; 8.5 oz.", "10\" Chef's Knife: 10\" blade; 5 1/2\" handle; 9.8 oz.", "Made in Germany."] }
  ],
  "materials": ["high-carbon-stainless-steel"],
  "configurator_base_skus": [],
  "sku_count": 18,
  "skus_returned": 19,
  "skus": [
    {
      "sku": "338443",
      "name": "Wusthof Classic 6\" Chef Knife, Light Pink",
      "options": { "size": "6\"", "color": "Pink Himalayan Salt" },
      "price": 99,
      "regular_price": 135,
      "on_sale": true,
      "discount_type": "special",
      "personalization_price": 17,
      "surcharge": null,
      "stock": "on_hand",
      "back_ordered_date": null,
      "ship_mode": "separate_ship",
      "delivery_services": ["standard"],
      "white_glove": false,
      "pickup_services": [],
      "furniture": false,
      "direct_ship": true,
      "special_order": false,
      "materials": ["high-carbon-stainless-steel"],
      "width_in": null,
      "height_in": null,
      "depth_in": null
    }
  ]
}
```

SKU `1468824` (8", Wild Blueberry) read $170 at its regular price with `rush` and `standard` delivery and `pickup_internal`. `{"url": "https://www.williams-sonoma.ca/products/wusthof-classic-chefs-knife/"}` read CAD 139.95 to 289.95 over 9 SKUs. Pottery Barn and the other brands answer `rating` and `review_count` null (they show no ratings). An unknown product is a charged `404`: "No Williams Sonoma product no-such-product-xyz-123 on www.williams-sonoma.com. Check the product id (the part after /products/ in its link)."

### Configurator, stock, pickup, stores, floor samples, listings, popular searches and reviews

- `/configurator` `{"brand": "pottery_barn", "base_sku": "4889446"}`: Gabrielle Sofa, `price` {`min` 1999, `max` 2899, `discount_percent_max` 20, `discount_type` `special`}, `production_lead_time` {`min` 27, `max` 51}, `dimensions_in` 63 x 33 x 39, `fabric_count` 50, the first Performance Boucle, Ivory (`PBO-IVRY`, features Bestseller and Contract Grade, content "60% Recycled Poly, 35% Poly, 5% Linen", `rub_count` "100,000", `price_tier` F). A product with no configurator (an empty `configurator_base_skus`) is a charged `404`; configurator on any brand other than Pottery Barn is an unbilled `400`.
- `/stock` `{"brand": "williams_sonoma", "product": "wusthof-classic-chefs-knife", "skus": ["2600435", "6124527"]}`: `2600435` `available_now` "401+" (`available_now_max` null on an open range), `within_2_weeks` "401+"; `6124527` "1-10" now and "71-80" within 2 weeks; both `regional` `in_stock` for the default ZIP 10001. A made-to-order sofa answers `count` 0 (no online stock reported).
- `/store-pickup` `{"brand": "williams_sonoma", "skus": ["1468824", "2600435"], "stores": ["ST:0859", "ST:6016"]}`: `2600435` `available_for_pickup` true at both stores, `1468824` false at both, each with `ship_to_store` 2026-12-01 to 2026-12-08 (5 to 12 days). A made-to-order sofa SKU answered false with `ship_to_store` null.
- `/stores` `{"zip": "60611"}`: 10 stores within 25 miles, Williams Sonoma Lincoln Park (store 6016, `ST:6016`, 1550 N Fremont St, 2.16 miles, 8:00 AM - 8:00 PM) first, then Pottery Barn, West Elm and Rejuvenation Lincoln Park, West Elm and Pottery Barn Old Orchard, and the Oakbrook stores, each with `pickup`, `ship_to_store` and this week's hours.
- `/floor-samples` `{"brand": "pottery_barn", "product": "gabrielle-upholstered-sofa", "zip": "94103"}`: 9 Pottery Barn stores, `radius_miles` 200 with `radius_extended` true, Village at Corte Madera (12.24 miles), Broadway Plaza (Walnut Creek), CC Bishop Ranch (San Ramon), Stanford Shopping Center (Palo Alto) and on to San Luis Obispo (197.67 miles).
- `/categories` `{"brand": "pottery_barn"}`: the 24 top-level categories (New, Furniture, Outdoor, Bedding, ... Sale, PB Apartment, ...) with `child_count`; `{"brand": "pottery_barn", "category": "sale"}`: 56 entries under Sale, the first "Black Friday: Up to 70% off" at path `/shop/sale/exclusive-savings/`.
- `/category` `{"brand": "pottery_barn", "path": "sale/exclusive-savings"}`: `total` 7,871, the first a Cozy Pom Pom Sherpa Throw at $35 against $59 (`limited_time_offer`, 41% off); `{"path": "furniture/sofa", "sort": "price_asc"}` 429 products, the Josie Sofa (58"-82") first from $499. An unknown path is a charged `404` (5 credits): "No category /shop/<path>/ on www.potterybarn.com (categories lists the paths)."
- `/search` `{"brand": "pottery_barn", "query": "sofa"}`: `total` 1,912, the first York Slope Arm Deep Seat Slipcovered Sofa from $1,679 to $4,199 (40% off at most); `{"brand": "williams_sonoma", "query": "espresso machine"}` 207, the Breville Barista Express Espresso Machine at $499.95 against $699.95. The "dutch oven" search answered 26 facets and the site's 8 sort options.
- `/popular-searches` `{"brand": "williams_sonoma"}`: `date` 2026-11-25, 15 terms, le creuset (13,584), coffee maker (7,830), hot chocolate (6,393), ...
- `/reviews` `{"brand": "williams_sonoma", "product": "wusthof-classic-chefs-knife"}`: `total` 502 written reviews of `statistics.review_count` 564 (rating-only reviews counted there too), 18 pages, average 4.81, 521 five-star; the first, 5 stars, "Christmas Gift", `syndicated` from the knife maker's site. Page 2 of `shun-classic-chefs-knife` held 30 of 90.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def wsi(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/williamssonoma/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. One product, every SKU's price and stock state (1 credit)
p = wsi("product", {"brand": "pottery_barn", "product": "gabrielle-upholstered-sofa"})["data"]
print(p["name"], p["price"], p["configurator_base_skus"])
for s in p["skus"]:
    print(s["sku"], s["options"], s["price"], s["regular_price"], s["stock"])

# 2. Fabrics and lead time of the made-to-order piece (1 credit)
if p["configurator_base_skus"]:
    c = wsi("configurator", {"brand": "pottery_barn", "base_sku": p["configurator_base_skus"][0]})["data"]
    print(c["price"], c["production_lead_time"], c["fabric_count"])

# 3. Delivery dates to a ZIP (1 credit)
d = wsi("delivery-estimate", {"brand": "pottery_barn", "product": p["product_id"], "zip": "94103"})["data"]
for s in d["skus"]:
    print(s["sku"], s["availability"], s["earliest_date"], s["latest_date"])

# Prices and dates can change between calls. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Every `data` carries `brand`, `brand_name`, `market`, `currency`, `language`, `host` and `notes`.

- **product** - `requested_product_id`, `product_id`, `name`, `url`, `page_type` (`simple`, `complex`, `configured`, `guided`), `available`, `category_id`, `breadcrumbs[]` {`name`, `path`}, `price` {`min`, `max`, `regular_min`, `regular_max`, `discount_type`}, `on_sale`, `rating`, `review_count`, `flags`, `messages[]` {`text`, `starts_at`, `ends_at`}, `dimensions[]` {`section`, `lines`}, `materials`, `configurator_base_skus`, `sku_count`, `skus_returned`, `skus[]` {`sku`, `name`, `options`, `price`, `regular_price`, `on_sale`, `discount_type`, `personalization_price`, `surcharge`, `stock`, `back_ordered_date`, `ship_mode`, `delivery_services`, `white_glove`, `pickup_services`, `furniture`, `direct_ship`, `special_order`, `materials`, `width_in`, `height_in`, `depth_in`} (up to 500). No UPC.
- **configurator** - `requested_base_sku`, `product_id`, `base_sku`, `name`, `price` {`min`, `max`, `regular_min`, `regular_max`, `discount_percent_max`, `discount_type`, `currency`}, `production_lead_time` {`min`, `max`}, `dimensions_in` {`width`, `depth`, `height`}, `fabric_count`, `fabrics[]` {`id`, `name`, `color`, `fabric`, `features`, `content`, `rub_count`, `price_tier`}.
- **delivery-estimate** - `zip`, `product_id`, `requested_skus`, `count`, `skus[]` {`sku`, `ship_mode`, `availability`, `special_order`, `service_level`, `earliest_date`, `latest_date`, `min_days`, `max_days`, `message`, `holiday` {`name`, `order_cutoff`, `delivery_dates[]` {`earliest_date`, `latest_date`, `service_level`, `cutoff`}}}.
- **stock** - `product_id`, `zip`, `regions`, `count`, `skus[]` {`sku`, `available_now`, `available_now_min`, `available_now_max`, `within_2_weeks`, `regional`}.
- **store-pickup** - `requested_skus`, `requested_stores`, `count`, `skus[]` {`sku`, `ship_mode`, `stores[]` {`pickup_location_code`, `available_for_pickup`, `ship_to_store` {`earliest_date`, `latest_date`, `min_days`, `max_days`}}}.
- **stores** - `brands`, `zip`, `latitude`, `longitude`, `radius_miles`, `include_outlets`, `count`, `stores[]` {`store_number`, `pickup_location_code`, `name`, `brand`, `store_type`, `address` {`line1`, `line2`, `city`, `state`, `postal_code`, `country`}, `latitude`, `longitude`, `phone`, `distance_miles`, `pickup`, `ship_to_store`, `hours[]` {`day`, `hours`}}.
- **floor-samples** - `product`, `zip`, `latitude`, `longitude`, `radius_miles`, `radius_extended`, `count`, `stores[]` {`store_number`, `brand`, `name`, `address`, `phone`, `latitude`, `longitude`, `distance_miles`, `hours`}.
- **categories** - without `category`: `count`, `categories[]` {`id`, `name`, `type`, `path`, `child_count`}; with it: `category` {`id`, `name`, `type`, `path`}, `count`, `children[]` {`id`, `name`, `type`, `path`, `children`}.
- **search, category** - `query` or `path` and `sort`, `page` (1), `page_size`, `total`, `count`, `items[]` {`position`, `product_id`, `name`, `url`, `leader_sku`, `image`, `price_min`, `price_max`, `regular_price_min`, `regular_price_max`, `sale_price_min`, `sale_price_max`, `price_type`, `max_discount_percent`, `flags`, `more_swatches`}, `facets[]` {`name`, `label`, `type`, `options[]` {`value`, `label`, `count`}}, `sort_options[]` {`label`, `sort_by`, `order`, `selected`}, `related_searches`.
- **popular-searches** - `date`, `count`, `terms[]` {`rank`, `term`, `count`}.
- **reviews** - `product_id`, `page`, `offset`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `statistics` {`average_rating`, `review_count`, `recommended_count`, `not_recommended_count`, `rating_distribution[]` {`rating`, `count`}}, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `verified_purchaser`, `badges`, `syndicated`, `syndication_source`, `helpful_votes`, `unhelpful_votes`, `secondary_ratings`, `product_name`}.

## Guardrails

- Name the brand on first mention ("Pottery Barn (potterybarn.com, a Williams-Sonoma, Inc. brand)"). No brand account is read.
- Prices: quote the SKU's `price` with `regular_price` and `discount_type`, the brand, the market and the `fetched_at` date. Prices are national online prices; never present one as a store's price or a member price.
- Configurator prices are the range across fabrics as given; never present one end of the range as the price of a named fabric.
- Delivery dates, stock ranges and pickup flags are the brand's own at the moment of the call; Scavio makes no promise of their accuracy. Never state or estimate a store's unit count, and never promise a delivery date or pickup.
- Report the brand's labels (`discount_type`, `price_type`, messages, holiday cutoffs) and the arithmetic only. Never judge a regular price or a discount, and never describe how often an item is on sale.
- Comparing brands or retailers: compare only the same item, each with its date and market; label different products as different. Never call one retailer cheaper beyond the numbers shown.
- Reviews: no reviewer names, locations or photos are returned. Syndicated reviews were written on another site (`syndication_source`); say so when quoting one.
- Not available: UPCs, unit counts per store, prices at a chosen store (prices are national), West Elm search, category listings beyond Pottery Barn, reviews on brands other than Williams Sonoma, listings past page 1, Canada beyond product, price history (poll and store), registry, cart or checkout. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not store Williams-Sonoma, Inc. data: each call fetches the brand's public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. The Williams-Sonoma, Inc. brand terms of use restrict automated access to their sites and how their content may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish product photos or logos; refer to products by name and `product_id`.
- Never fabricate prices, SKU ids, product ids, store codes, hours, delivery dates, stock ranges or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, or a brand / market the endpoint does not serve, and it is not charged: "product or url is required", "brand is required (or a product url)", "Pass product or url, not both."; "<endpoint> is not available for this brand / market (<brand>, <market>). Available: ..."; a `product` that is not a product id ("product must be a product id: the part after /products/ in a product link (items[].product_id, e.g. wusthof-classic-chefs-knife)."); a `url` on another host ("url must be on one of: ..."), a `url` whose brand or market disagrees with `brand` or `market`; a `sku` that is not a SKU id ("skus must be a SKU id (digits, product skus[].sku, e.g. 1468824)."), more than 20 SKUs or 10 store codes, store codes not in `ST:0154` form; "Pass zip or latitude + longitude, not both.", "zip <zip> is not a known US ZIP code.", "latitude and longitude go together"; "Pass product (every SKU of the product) or skus, one of them." (delivery), "Pass base_sku, or product / url, not both." (configurator), "Pass product or sku, not both." (floor samples), "<brand> has no stores: ..." (stores); "path must be a category path under /shop/ ..."; a `category` that is not a top-level id; "reviews has no sort or star filter: the brand's review list runs newest to oldest."; an unknown `sort`, a `page` or `radius` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged (5 credits on category and search, 1 elsewhere): "No <brand> product <id> on <host>. Check the product id (the part after /products/ in its link).", "No configurator for base SKU <sku> on <host> (product configurator_base_skus lists them).", "Product <id> has no fabric configurator (its configurator_base_skus is empty: guided pieces list every fabric and size as SKUs in product).", "No delivery estimate for product <id>: check the product id.", "No pickup answer for SKU ... at ...: check the SKU ids and store codes.", "No <brand> product or SKU <id>." (floor samples), "No top-level category <id> (categories without category lists the ids).", "No category /shop/<path>/ on <host> (categories lists the paths).", "No popular search terms were published in the last 4 days.", "No Williams Sonoma product <id>." (reviews). Take product ids, SKU ids, base SKUs, store codes and paths from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api).
- `502` means the brand site was temporarily unavailable ("The Williams-Sonoma, Inc. site is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the site is busy ("The Williams-Sonoma, Inc. site is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.100.0
npm install scavio@0.101.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: sofa } = await scavio.williamssonoma.product({ brand: "pottery_barn", product: "gabrielle-upholstered-sofa" });
const { data: fabrics } = await scavio.williamssonoma.configurator({ brand: "pottery_barn", base_sku: "4889446" });
const { data: dates } = await scavio.williamssonoma.deliveryEstimate({ brand: "pottery_barn", product: "gabrielle-upholstered-sofa", zip: "94103" });
const { data: online } = await scavio.williamssonoma.stock({ brand: "williams_sonoma", product: "wusthof-classic-chefs-knife" });
const { data: pickup } = await scavio.williamssonoma.storePickup({ brand: "williams_sonoma", skus: ["2600435"], stores: ["ST:6016"] });
const { data: near } = await scavio.williamssonoma.stores({ zip: "60611" });
const { data: floor } = await scavio.williamssonoma.floorSamples({ brand: "pottery_barn", product: "gabrielle-upholstered-sofa", zip: "94103" });
const { data: tree } = await scavio.williamssonoma.categories({ brand: "pottery_barn", category: "sale" });
const { data: sale } = await scavio.williamssonoma.category({ brand: "pottery_barn", path: "sale/exclusive-savings" });
const { data: hits } = await scavio.williamssonoma.search({ brand: "williams_sonoma", query: "dutch oven" });
const { data: terms } = await scavio.williamssonoma.popularSearches({ brand: "williams_sonoma" });
const { data: reviews } = await scavio.williamssonoma.reviews({ brand: "williams_sonoma", product: "wusthof-classic-chefs-knife" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.williamssonoma.product(...)`, `configurator`, `delivery_estimate`, `stock`, `store_pickup`, `stores`, `floor_samples`, `categories`, `category`, `search`, `popular_searches` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `get_williamssonoma_product`, `get_williamssonoma_configurator`, `get_williamssonoma_delivery_estimate`, `get_williamssonoma_stock`, `get_williamssonoma_store_pickup`, `get_williamssonoma_stores`, `get_williamssonoma_floor_samples`, `get_williamssonoma_categories`, `get_williamssonoma_category`, `search_williamssonoma`, `get_williamssonoma_popular_searches` and `get_williamssonoma_reviews`. Williams-Sonoma is opt-in: add `williamssonoma` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.100.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,williamssonoma"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [product](https://scavio.dev/docs/williamssonoma-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [configurator](https://scavio.dev/docs/williamssonoma-configurator?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [delivery estimate](https://scavio.dev/docs/williamssonoma-delivery-estimate?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [stock](https://scavio.dev/docs/williamssonoma-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [store pickup](https://scavio.dev/docs/williamssonoma-store-pickup?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [stores](https://scavio.dev/docs/williamssonoma-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [floor samples](https://scavio.dev/docs/williamssonoma-floor-samples?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [categories](https://scavio.dev/docs/williamssonoma-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [category](https://scavio.dev/docs/williamssonoma-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [search](https://scavio.dev/docs/williamssonoma-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [popular searches](https://scavio.dev/docs/williamssonoma-popular-searches?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api), [reviews](https://scavio.dev/docs/williamssonoma-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api). Overview: [Williams-Sonoma API](https://scavio.dev/williamssonoma-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=williams-sonoma-api).
