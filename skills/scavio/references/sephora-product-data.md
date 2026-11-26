# Sephora Product Data API - US and Canada Prices, Shades, Offers, Stores

Two markets on the same endpoints, chosen with `country`:

- `country: "us"` (the default) - sephora.com, in USD. Unchanged by Canada: a body without `country` works exactly as before.
- `country: "ca"` - Sephora Canada (sephora.com/ca, Sephora's Canadian store: 152 stores per its store list on Nov 25, 2026), in CAD, in English or French. Search, category and product take it, and Canada adds six endpoints of its own: brand, brands, suggestions, offers, stores and store. See [Sephora Canada](#sephora-canada-country-ca) below.

Sephora publishes no public product, price or store API for Canada; an affiliate creator storefront gives links, not a product feed.

The rest of this section and the US sections below describe sephora.com. Search Sephora (sephora.com, US) and list any category: price, list and sale price, value price for sets, rating, review count, extra colors and bestseller, new, exclusive and limited-edition flags, 60 products per page. Read one product with every shade or size it offers, each with its own price, stock and ingredients, plus Sephora's own summary of what reviews say and pro and con sentiment counts. All endpoints return structured JSON.

See also: `ulta-beauty-api` for Ulta Beauty prices and store pickup stock; `dermstore-skincare-prices-api` for Dermstore skincare prices in USD or CAD. For Canadian beauty prices at other retailers, see [Pairs well with](#pairs-well-with).

## When to trigger

Use this skill when the user asks to:
- Find makeup, skincare, hair care or fragrance at Sephora by keyword
- List the products in a Sephora category (lipstick, face serum, foundation) with prices and ratings
- Check a Sephora product's price, sale price, and which shades or sizes are in stock
- Compare shades of one product: shade name, description, size, price, swatch
- Summarize what Sephora's own review summary says about a product, and its pro and con counts
- Read a product's ingredients or suggested usage
- Find what is on sale, new or Sephora-exclusive in a search or category
- Compare Sephora prices with other retailers, or monitor them
- Get Sephora Canada prices in CAD (The Ordinary, Dior, Rare Beauty, Supergoop and other brands) with the sale price and which shades are in stock, in English or French
- List one brand's products at Sephora Canada, or the full Sephora Canada brand directory
- Read the current Sephora Canada beauty offers with their end dates, promo codes, spend thresholds and who they apply to
- List the Sephora stores in Canada or in one province, or read one store's address, phone, hours, holiday hours and services
- Pull Sephora Canada search box suggestions for keyword research
- Compare one beauty product's Sephora Canada price with Dermstore, Amazon.ca or Walmart.ca

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. US search and category cost 1 credit per call, product 2. Sephora Canada calls cost 1 credit, product and offers 2.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Monthly plans work out cheaper per credit when usage is steady (Hobby is $15 a
month for 3,000 credits; Growth works out to $1 per 1,000 credits).

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. The cost depends on `country`: the **US** costs are unchanged (search and category 1 credit, product 2), and a **Sephora Canada** call costs 1 credit, product and offers 2. Most calls take 2-10 seconds; some (a product page, the Canada store list) have taken 30-50 seconds. Allow a client timeout of at least 60 seconds.

| Endpoint | US credits | Canada credits | What it returns |
|---|---|---|---|
| `POST /api/v1/sephora/search` | 1 | 1 | 60 products per page: product id, sku id, brand, name, URL, image, price, list and sale price, value price for sets, price range, rating, review count, extra colors, sale scope, bestseller, new, exclusive, online-only, limited-edition and sponsored flags. US: with `zip`, same-day delivery eligibility. Plus category facets and related searches. Canada adds filters, facets, `has_more`, an app-exclusive flag and the brand redirect for a brand keyword |
| `POST /api/v1/sephora/category` | 1 | 1 | 60 products per page of one category in the same shape as search, plus the category id, name and URL, total products, parent category, subcategories with product counts and breadcrumbs. Canada adds sorts and filters |
| `POST /api/v1/sephora/product` | 2 | 2 | One product: name, brand, rating, review count, loves count, price range, description, suggested usage, category, breadcrumbs, Sephora's review summary with pro and con sentiment counts, and every shade or size the page offers with sku id, shade, size, price, list and sale price, in stock, only-few-left, ingredients, images, swatch, pickup and same-day eligibility. Canada adds the 10 latest reviews (no reviewer names), `currency` and `availability` per SKU |
| `POST /api/v1/sephora/brand` | -- | 1 | Canada only: one brand's products in the listing shape, with the brand's id, name and description and its categories with product counts |
| `POST /api/v1/sephora/brands` | -- | 1 | Canada only: every brand in the Sephora Canada A-Z directory (268 in the capture) with id, name, `seo_name`, link and letter |
| `POST /api/v1/sephora/suggestions` | -- | 1 | Canada only: the search box suggestions for a partial term, suggested terms plus products with rating and review count |
| `POST /api/v1/sephora/offers` | -- | 2 | Canada only: the current offers on the beauty offers page (26 in the capture) with section, title, description, eligibility, app-only flag, spend threshold, promo code, end date, legal copy and link |
| `POST /api/v1/sephora/stores` | -- | 1 | Canada only: the Canadian stores on Sephora's store list (152 on Nov 25, 2026), optionally one province, with the count per province and each store's name, city, mall, province and slug |
| `POST /api/v1/sephora/store` | -- | 1 | Canada only: one store by slug with address, phone, latitude / longitude, time zone, weekly hours, dated holiday hours, curbside hours and services |

## Workflow (US)

1. **Find products:** call `/sephora/search` with `query`, or `/sephora/category` with a category name such as `lipstick`. Each row has a `url` and a `product_id`.
2. **One product in full:** call `/sephora/product` with the row's `url` (faster) or its `product_id`.
3. **Shades and stock:** read `skus[]` on the product answer. Each shade or size has its own `price`, `in_stock` and `only_few_left`.
4. **What reviews say:** read `review_summary` and `review_sentiments[]` on the same answer. sephora.com has no review text endpoint.

## Parameters (US)

Every endpoint above also takes `country` (`us`, the default, or `ca`: see [Sephora Canada](#sephora-canada-country-ca) for the Canada parameters). The Canada-only fields (`filters`, `include_facets`, `language`, and `sort` on category) do nothing on a US call.

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `page` | integer | 1 | 1-based page (1-100), 60 products per page |
| `sort` | string | `relevance` | `relevance`, `best_selling`, `rating`, `price_low`, `price_high` or `newest` |
| `zip` | string | - | US ZIP code. When set, each product carries `same_day_eligible` for same-day delivery to that ZIP |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | The name in a sephora.com/shop/ URL (`lipstick`, `face-serum`, `makeup-cosmetics`), or the full `https://www.sephora.com/shop/...` URL |
| `page` | integer | 1 | 1-based page (1-100), 60 products per page |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | sephora.com product URL, the `url` of a search or category row. Preferred: it answers faster |
| `product_id` | string | one of | Sephora product id like `P510799`, used when `url` is not given |

## Sephora Canada (`country: "ca"`)

Send `country: "ca"` on search, category or product, or call one of the six Canada-only endpoints (`brand`, `brands`, `suggestions`, `offers`, `stores`, `store`; `country` defaults to `ca` there and `ca` is its only value). Sephora Canada is sephora.com/ca, Sephora's Canadian store: 152 stores per its store list on Nov 25, 2026. Every Canada call costs **1 credit**, except product and offers at **2**. Prices are in Canadian dollars (CAD), as Sephora Canada gives them. `language` is `en` (default) or `fr`: product and SKU ids and CAD prices are the same, names, descriptions, facet values and the review summary come back in French, and links open sephora.com/ca/fr.

### Same ids as the US, prices in CAD

- **Product and SKU ids are shared with sephora.com.** `P428500` is the same product in both markets, so a US `product_id` or a US product link works with `country: "ca"` and returns the Canadian price. Never convert a USD price to CAD yourself: call Canada for the CAD price.
- **French prices are parsed.** On the French pages Sephora Canada writes prices as `33,00 $`; `price`, `list_price` and `sale_price` are numbers (`33`) in both languages. `price_text` stays as the page shows it (`124,00 $` in French, `$42.00` in English).
- **Sale price and stock per SKU.** `skus[]` on `/product` carries `price`, `list_price`, `sale_price`, `on_sale`, `in_stock`, `only_few_left` and `availability` per shade or size. These are Sephora Canada's online flags, not a store's shelf.
- **Reviews.** `/product` returns `latest_reviews[]`: the 10 latest reviews the product page shows, with id, date, rating, title and text, and no reviewer names. `review_summary` is `{text, source}`: Sephora's own AI-generated summary of customer reviews, labelled as Sephora's.
- **Offers carry an end date, never a start date.** `end_date` is as Sephora Canada gives it (ISO 8601 with offset, e.g. `2026-11-30T23:59:00.000-08:00`) and is null when the offer states none. An offer that only starts later says so in its `description` text.

### Canada parameters

| Endpoint | Parameters |
|---|---|
| `/search` | `country: "ca"`, `query` (required, 1-200 chars), `page` (1-100, 60 per page), `sort` (`relevance`, `best_selling`, `rating`, `price_low`, `price_high`, `newest`), `filters`, `include_facets`, `language`. `zip` is sephora.com only (a `400` with `ca`) |
| `/category` | `country: "ca"`, `category` (the name in a `/shop/<name>` link: `lipstick`, `face-serum`, `makeup-cosmetics`, or the link), plus every listing parameter of search |
| `/product` | `country: "ca"`, `url` (any Sephora product link, Canadian `/ca/en` or `/ca/fr`, or the US one) or `product_id` (e.g. `P428500`), `language` (a `/ca/fr` link reads French) |
| `/brand` | `brand` (the name in a `/brand/<name>` link, e.g. `the-ordinary`, `dior`, `rare-beauty-by-selena-gomez`, a `seo_name` from `/brands`, or the link), plus every listing parameter of search |
| `/brands` | `language` |
| `/suggestions` | `query` (required, 1-100 chars: what the shopper has typed), `language` |
| `/offers` | `language` |
| `/stores` | `province` (optional: `AB`, `BC`, `MB`, `NB`, `NL`, `NS`, `NT`, `NU`, `ON`, `PE`, `QC`, `SK`, `YT`), `language` |
| `/store` | `store` (required: a `slug` from `/stores`, e.g. `toronto-eaton-centre`, or the store's link), `language` |

`filters` on search, category and brand: `brand` (as the Brand facet shows it, e.g. `The Ordinary`), `on_sale`, `new`, `clean` (Clean at Sephora), `rating` (1-4: that many stars and up), `min_price` and `max_price` (CAD), and `facets` (up to 10 `{facet, value}` pairs taken from a response's `facets[]`, which `include_facets: true` returns). `filters` can also be a plain array of `{facet, value}`. Several filters all apply together. An unknown filter name is a `400`, never silently dropped.

### Canada workflow

1. **Find products:** `/search` with `country: "ca"` and `query`, `/category` with a category name, or `/brand` with a brand name (take it from `/brands`). Read `products[].product_id`, `url`, `price`, `list_price`, `sale_price`, `on_sale`. A brand keyword on `/search` (e.g. `the ordinary`) answers with that brand's products and `redirect: {type: "brand", url}`.
2. **Narrow the listing:** pass `filters` (`on_sale: true` for what is on sale, `brand`, `min_price` / `max_price`) and a `sort`. Send `include_facets: true` once to get the facet values you can filter on. `filters_applied` echoes what was applied.
3. **One product in full:** `/product` with `country: "ca"` and the row's `url` or `product_id`. Read `skus[]` for the CAD price, sale price and stock of each shade or size, `review_summary` and `review_sentiments[]` for Sephora's summary, and `latest_reviews[]`.
4. **Offers:** `/offers` for the current beauty offers; read `end_date`, `promo_code`, `threshold`, `eligibility` and `app_only`.
5. **Stores:** `/stores` (optionally with `province`) for the list and a `slug`, then `/store` with that slug for the address, phone, hours, holiday hours and services.
6. **Price tracking:** call `/product` (or a listing) on a schedule and store the prices yourself; compare `price` and `sale_price` across runs.

### Canada traps

- **`list_price` can be null on a listing row.** When a product's sizes are priced differently, `list_price` is null and `price` is the low end; read `price_range` and `price_text`, or the exact SKU price from `/product`.
- **`sale_scope`.** `full` means every shade is on sale, `partial` some shades. Read each SKU's `on_sale` and `sale_price` before saying a given shade is on sale.
- **Online stock, not store stock.** `in_stock`, `only_few_left` and `availability` are Sephora Canada's online flags. `pickup_eligible` and `same_day_eligible` are national eligibility flags, not a store's stock. Never say a store has an item.
- **`upc` is always null for Canada.** Sephora Canada's pages carry no UPC or GTIN. Match products across retailers by brand, name and size, and say the match is by name.
- **Reviews are the latest 10, not all of them.** `review_count` is the product's total; `latest_reviews[]` holds at most 10. Never claim to have read every review, and never sort or filter them by star rating: that is not available. Review text is as given, including incentive notes such as "[I received this product in exchange for my honest review]". Quote a review as that reviewer's words with its date and rating, never as a fact.
- **The AI summary is Sephora's.** Present `review_summary.text` as "Sephora's AI-generated summary of reviews says ...", never as your own finding or as a fact about the product.
- **Offers.** `app_only: true` means the offer's eligibility is the Sephora app only (in the capture, "Black Friday Preview: 50% OFF∆", whose description says it starts 11/26 at 6pm PT). `eligibility[]` is as given (`Online`, `In Store`, `Apps`, `Rouge`, `VIB`, `Insider`). `threshold` and `legal_copy` are Sephora's own text; quote them, do not reword the conditions. Offers carry no product prices or member prices.
- **Stores.** The store list is Sephora's own list. `/stores` has no postal code or distance search: filter by `province`, or match the city yourself. Store contact details (address, phone) are public business data; show them as returned. `phone` is digits only (`4165957227`).
- **Hours.** `hours` is the weekly pattern as the page shows it (`10:00AM-09:00PM`); `holiday_hours[]` holds dated exceptions with `closed: true` on closed days. Read the dated entry for the day the user asks about first.
- **Not-found is charged.** An unknown product, category, brand or store is a charged `404`, as in the US. A refused input (`400`) and an upstream failure (`502`) are not charged.
- Not available for Canada: stock per store, a store finder by postal code, full review paging, review sorts and the star filter, UPC (Sephora Canada does not show it), Beauty Insider member prices, cart / checkout, price history (poll and store it yourself).

### Pairs well with

For Canadian beauty prices across retailers: `dermstore-skincare-prices-api` with `country: "ca"` (Dermstore's own CAD prices), `amazon-product-data` with `country: "ca"` (Amazon.ca) and `walmart-product-data` with `domain: "ca"` (Walmart.ca). Each reads the retailer's own site and price. Match products by brand, name and size (Sephora Canada has no UPC), and show each price with its currency and retailer.

### Canada examples

#### Product in CAD (2 credits)

```bash
curl -X POST https://api.scavio.dev/api/v1/sephora/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "ca", "product_id": "P428500"}'
```

Captured `data` (Dior Sauvage Eau de Parfum; description, suggested usage, category, breadcrumbs, `current_sku`, 3 of 5 `skus[]` and 9 of 10 `latest_reviews[]` trimmed, SKU images and ingredients left out):

```json
{
  "product_id": "P428500",
  "requested_product_id": "P428500",
  "name": "Sauvage Eau de Parfum",
  "brand": "DIOR",
  "url": "https://www.sephora.com/ca/en/product/sauvage-eau-de-parfum-P428500",
  "language": "en",
  "currency": "CAD",
  "rating": 4.5799,
  "review_count": 914,
  "loves_count": 103550,
  "price_min": 128,
  "price_max": 300,
  "upc": null,
  "review_summary": {
    "text": "Reviews frequently praise the style, with many also noting strong longevity and a clearly masculinity-leaning character. A smaller share of feedback suggests some reservations around uniqueness, while a few comments mention the scent and perceived similarity to other fragrances.",
    "source": "Sephora's own AI-generated summary of customer reviews, as shown on the product page"
  },
  "review_sentiments": [
    { "sentiment": "Longevity", "type": "pros", "count": 80 },
    { "sentiment": "Masculinity", "type": "pros", "count": 58 },
    { "sentiment": "Scent", "type": "cons", "count": 5 },
    { "sentiment": "Similarity", "type": "cons", "count": 5 },
    { "sentiment": "Style", "type": "pros", "count": 93 },
    { "sentiment": "Uniqueness", "type": "cons", "count": 6 }
  ],
  "variation_type": "Size + Concentration + Formulation",
  "sku_count": 5,
  "skus": [
    {
      "sku_id": "2038131",
      "variation_type": "Size + Concentration + Formulation",
      "variation_value": "3.4 oz / 100 ml",
      "variation_description": null,
      "size": "3.4 oz / 100 ml",
      "price": 200,
      "list_price": 200,
      "sale_price": null,
      "on_sale": false,
      "in_stock": true,
      "only_few_left": false,
      "availability": "in_stock",
      "is_new": false,
      "is_limited_edition": false,
      "is_sephora_exclusive": false,
      "is_online_only": false,
      "pickup_eligible": true,
      "same_day_eligible": true,
      "max_purchase_quantity": 10,
      "highlights": ["Woody & Earthy Scent"],
      "url": "https://www.sephora.com/ca/en/product/sauvage-eau-de-parfum-P428500?skuId=2038131"
    },
    {
      "sku_id": "2038123",
      "variation_type": "Size + Concentration + Formulation",
      "variation_value": "2.0 oz / 60 ml",
      "variation_description": null,
      "size": "2.0 oz / 60 ml",
      "price": 150,
      "list_price": 150,
      "sale_price": null,
      "on_sale": false,
      "in_stock": true,
      "only_few_left": false,
      "availability": "in_stock",
      "is_new": false,
      "is_limited_edition": false,
      "is_sephora_exclusive": false,
      "is_online_only": false,
      "pickup_eligible": true,
      "same_day_eligible": true,
      "max_purchase_quantity": 10,
      "highlights": ["Woody & Earthy Scent"],
      "url": "https://www.sephora.com/ca/en/product/sauvage-eau-de-parfum-P428500?skuId=2038123"
    }
  ],
  "latest_reviews": [
    {
      "id": "421685629",
      "date": "2026-11-24",
      "rating": 5,
      "title": null,
      "text": "This scent provides a very masculine profile with a more earthy smell to it, with a hint of musk. For me, I've received many compliments and it will last me all day, which is such a benefit!"
    }
  ],
  "market": { "country": "ca", "currency": "CAD", "language": "en", "site": "sephora.com/ca" }
}
```

With `"language": "fr"` the same call reads the French page: the captured Rare Beauty by Selena Gomez lip oil (`P505568`) came back as "Huile teintée pour les lèvres Soft Pinch", 8 shades at `price` 33 (CAD, written `33,00 $` on the page), with a French `review_summary.text`.

#### A sale row in CAD (search, 1 credit)

`{"country": "ca", "query": "lip oil"}` returned 109 results; 14 of the 60 rows on page 1 were on sale. One captured row (image left out):

```json
{
  "position": 4,
  "product_id": "P483060",
  "sku_id": "2583938",
  "brand": "Clarins",
  "name": "Lip Comfort Hydrating Oil",
  "url": "https://www.sephora.com/ca/en/product/clarins-lip-comfort-oil-P483060?skuId=2583938",
  "price": 31.5,
  "list_price": 42,
  "sale_price": 31.5,
  "value_price": null,
  "price_range": null,
  "price_text": "$42.00",
  "rating": 4.2991,
  "review_count": 1829,
  "more_colors": 7,
  "on_sale": true,
  "sale_scope": "full",
  "is_bestseller": false,
  "is_new": false,
  "is_sephora_exclusive": false,
  "is_online_only": false,
  "is_limited_edition": false,
  "is_app_exclusive": false,
  "sponsored": false
}
```

Here `price_text` is the list price as the row shows it; `price` and `sale_price` are the sale price. Report it as "31.50 CAD, list 42.00 CAD", as Sephora Canada gives it.

#### Offers with end dates (2 credits)

`{}` on `/api/v1/sephora/offers` returned 26 offers and `note`. Three captured offers (the last two trimmed to their main fields):

```json
[
  {
    "id": "beautyoffers_offerbanner_merchsale_program_sephoracollection_cyber1126_FY264959_ca_rwd_promo_112326",
    "section": "Shop the Best Deals of the Year",
    "title": "30% OFF∆ Sephora Collection",
    "description": "Enjoy 30% off all Sephora Collection products from 11/23 through 11/30.",
    "eligibility": ["Online", "In Store"],
    "app_only": false,
    "threshold": null,
    "promo_code": null,
    "promo_id": null,
    "end_date": "2026-11-30T23:59:00.000-08:00",
    "legal_copy": "∆Available on in-stock merchandise only.",
    "action_label": "Shop Sale",
    "url": "https://www.sephora.com/ca/en/brand/sephora-collection"
  },
  {
    "section": "Shop the Best Deals of the Year",
    "title": "FREE* Sample Bag",
    "eligibility": ["Rouge", "VIB", "Insider", "Online"],
    "app_only": false,
    "threshold": "Free with $95 min. spend.*",
    "promo_code": "grabmybag",
    "end_date": null
  },
  {
    "section": "Shop the Best Deals of the Year",
    "title": "Black Friday Preview: 50% OFF∆",
    "description": "Half off select gifts starts 11/26 at 6pm PT. See the best deals early––only on the app.",
    "eligibility": ["Apps"],
    "app_only": true,
    "threshold": null,
    "promo_code": null,
    "end_date": null
  }
]
```

`note` in the capture: "Sephora Canada gives each offer an end date (end_date, as given) when it has one, and no start date."

#### Stores and one store (1 credit each)

`/api/v1/sephora/stores` with `{}` returned `total_stores` 152 and `province_counts` `{"AB": 22, "BC": 22, "MB": 5, "NB": 3, "NL": 1, "NS": 4, "ON": 64, "PE": 1, "QC": 26, "SK": 4}`. One row:

```json
{ "name": "Toronto, Eaton Centre", "city": "Toronto", "location": "Eaton Centre", "province": "ON", "province_name": "Ontario", "slug": "toronto-eaton-centre", "url": "https://www.sephora.com/ca/en/happening/stores/toronto-eaton-centre" }
```

`/api/v1/sephora/store` with `{"store": "toronto-eaton-centre"}` (4 of 6 `holiday_hours[]` trimmed):

```json
{
  "store": {
    "store_id": "0500",
    "slug": "toronto-eaton-centre",
    "name": "EATON CENTRE",
    "type": "SEPHORA",
    "address": { "line1": "220 YONGE ST", "line2": "SPC 3-131", "city": "TORONTO", "province": "ON", "postal_code": "M5B 2H1", "country": "CA" },
    "phone": "4165957227",
    "latitude": 43.65353,
    "longitude": -79.38014,
    "time_zone": "America/Toronto",
    "hours": {
      "monday": "10:00AM-09:00PM",
      "tuesday": "10:00AM-09:00PM",
      "wednesday": "10:00AM-09:00PM",
      "thursday": "10:00AM-09:00PM",
      "friday": "10:00AM-09:00PM",
      "saturday": "10:00AM-09:00PM",
      "sunday": "11:00AM-07:00PM"
    },
    "holiday_hours": [
      { "start_date": "2026-11-27", "end_date": "2026-11-27", "hours": "08:00AM-10:00PM", "closed": false, "reason": "HOLIDAY" },
      { "start_date": "2026-12-25", "end_date": "2026-12-25", "hours": null, "closed": true, "reason": "HOLIDAY" }
    ],
    "curbside_hours": null,
    "services": { "buy_online_pick_up": true, "in_store_pickup": true, "curbside": false, "beauty_services": true, "store_events": true },
    "message": null,
    "url": "https://www.sephora.com/ca/en/happening/stores/toronto-eaton-centre"
  },
  "language": "en",
  "market": { "country": "ca", "currency": "CAD", "language": "en", "site": "sephora.com/ca" }
}
```

#### Brand, brands and suggestions (1 credit each)

`/api/v1/sephora/brand` with `{"brand": "the-ordinary"}` returned `brand` `{"brand_id": "6234", "name": "The Ordinary", "seo_name": "the-ordinary", "url": "https://www.sephora.com/ca/en/brand/the-ordinary", "description": "Clinical Formulations with Integrity."}`, 7 `categories[]` (e.g. `{"category_id": "cat150006", "name": "Skincare", "product_count": 63, "url": "https://www.sephora.com/ca/en/brand/the-ordinary/skincare"}`), `total_results` 67 over 2 pages and 60 `products[]` in the listing shape. `/brands` returned `count` 268 rows like `{"brand_id": "6317", "name": "Rare Beauty by Selena Gomez", "seo_name": "rare-beauty-by-selena-gomez", "url": "https://www.sephora.com/ca/en/brand/rare-beauty-by-selena-gomez", "letter": "R"}`. `/suggestions` with `{"query": "lip"}` returned `terms` `["lip liner", "lip balm", "lip gloss"]` and 6 `products[]` such as `{"product_id": "P455936", "sku_id": "2968907", "name": "Lip Butter Balm Treatment for Hydration + Nourishing Shine", "brand": "Summer Fridays", "rating": 4.294, "review_count": 18316, "image": "https://www.sephora.com/productimages/sku/s2968907-main-zoom.jpg", "url": "https://www.sephora.com/ca/en/product/P455936"}`.

## Examples (US)

```bash
curl -X POST https://api.scavio.dev/api/v1/sephora/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.sephora.com/product/mac-cosmetics-m-a-cximal-silky-matte-lipstick-P510799"}'
```

Captured response (MAC lipstick; description, breadcrumbs and 31 `skus[]` trimmed, `current_sku` without images and ingredients):

```json
{
  "data": {
    "product_id": "P510799",
    "name": "M·A·Cximal Silky Matte 12HR Wear Lipstick",
    "brand": "MAC Cosmetics",
    "url": "https://www.sephora.com/product/mac-cosmetics-m-a-cximal-silky-matte-lipstick-P510799",
    "rating": 4.5879,
    "review_count": 774,
    "loves_count": 316704,
    "price_min": 16,
    "price_max": 25,
    "review_summary": "Reviews generally reflect favorable impressions of the pigment, texture, and finish, with these features often mentioned positively. Some customers note mild concerns about dryness, transfer, and formula change, though these are less frequently discussed.",
    "review_sentiments": [
      { "sentiment": "Dryness", "type": "cons", "count": 21 },
      { "sentiment": "Finish", "type": "pros", "count": 34 },
      { "sentiment": "Formula Change", "type": "cons", "count": 11 },
      { "sentiment": "Pigment", "type": "pros", "count": 88 },
      { "sentiment": "Texture", "type": "pros", "count": 54 },
      { "sentiment": "Transfer", "type": "cons", "count": 12 }
    ],
    "variation_type": "Color",
    "current_sku": {
      "sku_id": "2764421",
      "variation_type": "Color",
      "variation_value": "Honeylove",
      "variation_description": "light beige toned rose",
      "size": "0.12 oz",
      "price": 25,
      "list_price": 25,
      "sale_price": null,
      "on_sale": false,
      "in_stock": true,
      "only_few_left": false,
      "is_new": false,
      "is_limited_edition": false,
      "is_sephora_exclusive": false,
      "is_online_only": false,
      "pickup_eligible": true,
      "same_day_eligible": true,
      "max_purchase_quantity": 10,
      "highlights": ["Matte Finish"],
      "swatch": "https://www.sephora.com/productimages/sku/s2764421+sw.jpg",
      "url": "https://www.sephora.com/product/mac-cosmetics-m-a-cximal-silky-matte-lipstick-P510799?skuId=2764421"
    },
    "sku_count": 31
  },
  "response_time": 3465,
  "credits_used": 2
}
```

A captured `/search` row for `{"query": "lipstick", "zip": "10001"}`, a product on sale (image trimmed):

```json
{
  "position": 30,
  "product_id": "P501583",
  "sku_id": "2599041",
  "brand": "NARS",
  "name": "Powermatte Long-Lasting Lipstick",
  "url": "https://www.sephora.com/product/nars-powermatte-lipstick-P501583?skuId=2599041",
  "price": 18,
  "list_price": 36,
  "sale_price": 18,
  "value_price": null,
  "price_range": null,
  "price_text": "$36.00",
  "rating": 4.3106,
  "review_count": 367,
  "more_colors": 7,
  "on_sale": true,
  "sale_scope": "full",
  "is_bestseller": false,
  "is_new": false,
  "is_sephora_exclusive": true,
  "is_online_only": false,
  "is_limited_edition": false,
  "sponsored": false,
  "same_day_eligible": true
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def sephora(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/sephora/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. What is on sale in a category (1 credit)
cat = sephora("category", {"category": "lipstick"})
for p in cat["products"]:
    if p["on_sale"]:
        print(p["brand"], p["name"][:40], p["price"], "was", p["list_price"])

# 2. One product: shades in stock and Sephora's review summary (2 credits)
item = sephora("product", {"url": cat["products"][0]["url"]})
print(item["name"], item["rating"], item["review_count"], "reviews")
print("Sephora's review summary:", item["review_summary"])
for s in item["review_sentiments"]:
    print(s["type"], s["sentiment"], s["count"])
print([s["variation_value"] for s in item["skus"] if s["in_stock"]])

# 3. The same product at Sephora Canada, in CAD (2 credits)
ca = sephora("product", {"country": "ca", "product_id": item["product_id"]})
for s in ca["skus"]:
    print(s["variation_value"], s["price"], ca["currency"], "sale" if s["on_sale"] else "", "in stock" if s["in_stock"] else "out of stock")

# 4. Sephora Canada offers that end on a date (2 credits)
for o in sephora("offers", {"country": "ca"})["offers"]:
    if o["end_date"]:
        print(o["title"], "ends", o["end_date"], o["promo_code"] or "")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Sephora answered.

- **search** (US) - `query`, `page`, `sort`, `zip`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `product_id`, `sku_id`, `brand`, `name`, `url`, `image`, `price`, `list_price`, `sale_price`, `value_price`, `price_range` {`min`, `max`}, `price_text`, `rating`, `review_count`, `more_colors`, `on_sale`, `sale_scope`, `is_bestseller`, `is_new`, `is_sephora_exclusive`, `is_online_only`, `is_limited_edition`, `sponsored`, `same_day_eligible`), `categories[]` {`category_id`, `name`, `product_count`}, `related_searches[]`.
- **category** (US) - `category` {`category_id`, `name`, `seo_name`, `url`, `page_type`}, `page`, `total_results`, `total_pages`, `count`, `parent_category` {`category_id`, `name`, `url`}, `subcategories[]` {`category_id`, `name`, `url`, `product_count`}, `breadcrumbs[]` {`name`, `url`}, `products[]` (the search product shape).
- **product** (US) - `product_id`, `name`, `brand`, `brand_url`, `url`, `rating`, `review_count`, `loves_count`, `price_min`, `price_max`, `description`, `suggested_usage`, `category` {`category_id`, `name`, `url`}, `breadcrumbs[]`, `review_summary`, `review_sentiments[]` {`sentiment`, `type` (`pros` or `cons`), `count`}, `variation_type`, `current_sku`, `sku_count`, `skus[]` (`sku_id`, `variation_type`, `variation_value`, `variation_description`, `size`, `price`, `list_price`, `sale_price`, `on_sale`, `in_stock`, `only_few_left`, `is_new`, `is_limited_edition`, `is_sephora_exclusive`, `is_online_only`, `pickup_eligible`, `same_day_eligible`, `max_purchase_quantity`, `highlights[]`, `ingredients`, `image`, `images[]`, `swatch`, `url`).
- **Canada listing** (search, category, brand with `country: "ca"`) - `language`, `page`, `sort`, `filters_applied[]`, `total_results`, `total_pages`, `has_more`, `count`, `products[]` (the US row without `same_day_eligible`, plus `is_app_exclusive`; `list_price` null when sizes are priced differently), `facets[]` {`facet`, `type`, `values[]` {`value`, `name`, `count`, `selected`}} (with `include_facets`), `market` {`country`, `currency`, `language`, `site`}. Search adds `query`, `redirect` {`type`, `url`} (null unless a brand or category keyword), `categories[]` and `related_searches[]`; category adds `category`, `parent_category`, `subcategories[]` and `breadcrumbs[]`; brand adds `brand` {`brand_id`, `name`, `seo_name`, `url`, `description`} and `categories[]` {`category_id`, `name`, `product_count`, `url`}.
- **Canada product** - the US product shape plus `requested_product_id`, `language`, `currency`, `upc` (always null), `review_summary` as {`text`, `source`}, `latest_reviews[]` {`id`, `date`, `rating`, `title`, `text`}, `availability` per SKU, and `market`.
- **brands** - `language`, `count`, `brands[]` {`brand_id`, `name`, `seo_name`, `url`, `letter`}.
- **suggestions** - `query`, `language`, `count`, `terms[]`, `products[]` {`product_id`, `sku_id`, `name`, `brand`, `rating`, `review_count`, `image`, `url`}.
- **offers** - `language`, `count`, `offers[]` {`id`, `section`, `title`, `description`, `eligibility[]`, `app_only`, `threshold`, `promo_code`, `promo_id`, `end_date`, `legal_copy`, `action_label`, `url`}, `note`.
- **stores** - `language`, `province`, `total_stores`, `province_counts` {code: count}, `count`, `stores[]` {`name`, `city`, `location`, `province`, `province_name`, `slug`, `url`}, `market`.
- **store** - `store` {`store_id`, `slug`, `name`, `type`, `address` {`line1`, `line2`, `city`, `province`, `postal_code`, `country`}, `phone`, `latitude`, `longitude`, `time_zone`, `hours` {`monday` .. `sunday`}, `holiday_hours[]` {`start_date`, `end_date`, `hours`, `closed`, `reason`}, `curbside_hours`, `services` {`buy_online_pick_up`, `in_store_pickup`, `curbside`, `beauty_services`, `store_events`}, `message`, `url`}, `language`, `market`.

## Guardrails

- These guardrails are for sephora.com unless they say Canada; the Canada-specific ones are in [Canada traps](#canada-traps). Never mix the two markets in one answer without labelling each price with its market and currency.
- US prices are in US dollars: `25` is $25.00. With `country: "ca"` prices are in Canadian dollars as Sephora Canada gives them; say CAD. `price` is what the shopper pays now: the sale price when there is one, else the list price.
- On a listing row whose sizes are priced differently, `price` and `list_price` are the low end (Canada: `list_price` is null); `price_range` holds both ends and `price_text` the range as shown ("$16.00 - $25.00"). Quote the range, or read the exact shade's price from `/product`.
- `value_price` is the stated value of a set's contents, not a price anyone pays.
- `sale_scope` is `full` (every shade on sale) or `partial` (some shades). On a partial sale the product page can leave the sale shades out, so `skus[]` is what the page offers, not necessarily every shade; `more_colors` on the listing row is the site's own count.
- `same_day_eligible` on US listings is only set when a `zip` was sent; it is `null` otherwise and always `null` on `/category`.
- `review_summary` and `review_sentiments` are Sephora's own AI-generated summary of its reviews. Label them as Sephora's and never present them as a fact about the product. sephora.com has no review text endpoint; with `country: "ca"`, `latest_reviews[]` holds the 10 latest reviews only.
- Report prices, sale prices and offers as Sephora gives them. Do not call a price low, high, good or bad, and do not say whether an offer is worth taking. Make no claims about what a product does for skin or hair: quote the product's name and description as given if asked.
- Store-level stock is not available in either market; `pickup_eligible` only says the shade can be picked up somewhere.
- This API reads public product data for research and price monitoring. It does not add to cart, check out or apply promo codes.
- Never fabricate prices, shades, stock, offer dates or reviews. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, an unknown `sort`, a ZIP that is not 5 digits, a `category` that is not a sephora.com/shop/ name, or a `product_id` not like `P510799`).
- For Canada, `400` also covers `zip` with `country: "ca"`, a `language` other than `en` or `fr`, an unknown filter name, `filters.rating` outside 1-4, `min_price` above `max_price`, more than 10 filters, a facet value not taken from `facets[]`, a `brand` or `category` that is not a Sephora name or link, a `province` that is not a Canadian province or territory code, a `store` that is not a store slug or link, and neither `url` nor `product_id`. Not charged.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/category` means no such category; use the name from a sephora.com/shop/ URL. `404` on `/product` means no such product; re-run the search for a fresh `url`. With `country: "ca"` an unknown brand or store is a `404` too. A not-found is a paid answer in both markets (1 credit, product 2), so do not retry the same input.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data).
- `502` or `503` means Sephora is temporarily unavailable. It is not charged; retry after a few seconds.
- A nonsense query is not empty: Sephora falls back to loosely related products, so check that results match before answering.

## SDKs

```bash
pip install scavio==0.93.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.sephora.search(query="lipstick", sort="best_selling", zip="10001")
item = client.sephora.product(url=found["data"]["products"][0]["url"])

# Sephora Canada: country="ca" on search, category and product (product 2 credits)
ca = client.sephora.search(query="lip oil", country="ca", filters={"on_sale": True})
ca_item = client.sephora.product(product_id="P428500", country="ca", language="fr")
lips = client.sephora.category(category="lipstick", country="ca", sort="price_low")

# Canada only (country defaults to "ca")
brand = client.sephora.brand(brand="the-ordinary")
brands = client.sephora.brands()
ideas = client.sephora.suggestions(query="lip")
offers = client.sephora.offers()  # 2 credits
stores = client.sephora.stores(province="QC")
store = client.sephora.store(store="toronto-eaton-centre")
```

```bash
npm install scavio@0.94.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.sephora.search({ query: "lipstick", sort: "best_selling", zip: "10001" });
const lips = await scavio.sephora.category({ category: "lipstick", page: 2 });
const item = await scavio.sephora.product({ url: found.products[0].url });

// Sephora Canada
const { data: caItem } = await scavio.sephora.product({ country: "ca", product_id: "P428500" });
const { data: brand } = await scavio.sephora.brand({ brand: "the-ordinary", filters: { on_sale: true } });
const { data: brands } = await scavio.sephora.brands();
const { data: ideas } = await scavio.sephora.suggestions({ query: "lip" });
const { data: offers } = await scavio.sephora.offers();
const { data: stores } = await scavio.sephora.stores({ province: "ON" });
const { data: store } = await scavio.sephora.store({ store: "toronto-eaton-centre" });
```

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_sephora`, `get_sephora_category`, `get_sephora_product`, and the Sephora Canada only `get_sephora_brand`, `get_sephora_brands`, `get_sephora_suggestions`, `get_sephora_offers`, `get_sephora_stores` and `get_sephora_store`. Pass `country: "ca"` to the first three for Sephora Canada. Sephora is opt-in: add `sephora` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.93.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,sephora"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/sephora-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [category](https://scavio.dev/docs/sephora-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [product](https://scavio.dev/docs/sephora-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data) (each covers `country: "us"` and `country: "ca"`), and Sephora Canada only: [brand](https://scavio.dev/docs/sephora-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [brands](https://scavio.dev/docs/sephora-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [suggestions](https://scavio.dev/docs/sephora-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [offers](https://scavio.dev/docs/sephora-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [stores](https://scavio.dev/docs/sephora-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data), [store](https://scavio.dev/docs/sephora-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data). Overview: [Sephora API](https://scavio.dev/sephora-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data).
