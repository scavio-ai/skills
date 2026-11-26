# Cult Beauty API - CultBeauty Prices, Discounts, Shades, Offers

Read Cult Beauty (cultbeauty.co.uk, the UK beauty retailer, with its international site cultbeauty.com; part of THG Beauty with Lookfantastic and Dermstore) on either site and in any of its 12 currencies: search, any list page, one product in full with every variant, search suggestions, the current offers, the brand directory and the category tree. Every answer comes as Cult Beauty's page shows it to a visitor without an account, in English. All 7 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Cult Beauty shows to any visitor and returns them as JSON for analysis. It uses no Cult Beauty account, no cart, no checkout, no code redemption and no rewards login.

**The job this skill is for: Cult Beauty prices, discounts and shades, per site and currency, read at a known time.** What a product costs on Cult Beauty now, Cult Beauty's RRP as it gives it, the percent off, and the offer it shows, for every shade or size, on cultbeauty.co.uk or cultbeauty.com, in the currency you ask for. Discounts move during an event, so the time of each reading matters. Captured 2026-11-26 during Black Friday, PIXI Glow Tonic 250ml (SKU `11200055`, barcode `885190821006`):

| Reading (2026-11-26, about an hour apart) | `market` | `currency` | Price | RRP | `discount_percent` | Offer |
|---|---|---|---|---|---|---|
| earlier | `gb` | GBP | 13.50 | 18 | 25 | 25% OFF |
| earlier | `gb` | USD | 17.82 | 23.76 | 25 | 25% OFF |
| earlier | `intl` | EUR | 15.23 | 20.30 | 25 | 25% OFF |
| later | `gb` | GBP | 12.60 | 18 | 30 | 30% OFF |
| later | `intl` | EUR | 14.21 | 20.30 | 30 | 30% OFF |

The same SKU read 12.60 GBP (RRP 18, 30% off) on lookfantastic.com the same day: Cult Beauty and Lookfantastic share SKUs, so `lookfantastic-api` reads the same `sku` there. Within one product the shades can carry different discounts: NARS Afterglow Lip Balm read 19.18 GBP (35% off an RRP of 29.50) on six shades and 20.65 GBP (30% off) on three. Read the variant and the time; never assume one discount for a brand, a product or a day.

Ten limits shape every answer, so say them plainly:
- **1 credit per call** on every endpoint. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **RRP as given, discount computed.** `rrp` is Cult Beauty's RRP exactly as it gives it. `discount_percent` is computed by Scavio from `price` and `rrp`, and only when the RRP is above the price; otherwise it is `null`. Cult Beauty's sale price is already in `price` ("Discount has been applied to the RRP").
- **Early-access and code prices are not in the data.** Some offers say "Must be logged into your account to redeem" (Black Friday early access) and some prices exist only in the basket. Those prices are not returned. A price after a stated rate is your own computation: label it "computed, not checked out".
- **Two sites, 12 currencies.** `market` `gb` (cultbeauty.co.uk, default, GBP) or `intl` (cultbeauty.com, EUR); each takes `currency` GBP, EUR, USD, AUD, CHF, AED, SAR, ILS, HKD, SGD, JPY or CNY. Each currency is the site's own price list, never converted by Scavio. Anything else is a `400`, not charged; every answer's currency is checked against the one asked.
- **Offers on the UK site only.** `/offers` reads cultbeauty.co.uk's voucher-codes page; cultbeauty.com has none, so `/offers` with `market` `intl` is a `400`, not charged. Product `offer` text is on both sites.
- **Mapped keywords resolve to a page.** Cult Beauty sends many keywords (a brand such as cerave, an ingredient such as vitamin c or retinol serum) to one of its pages instead of search results; `/search` then returns that page's products and says so in `resolved_from` {`type` (`brand`, `category`, `landing` or `product`), `path`, `listed_path`, `url`, `title`, `sku`} and in `notes`. Always check `resolved_from` before calling an answer "search results for q".
- **Variants carry their own price.** A product's `variants[]` (shades, sizes) each have their own `sku`, `price`, `rrp`, `discount_percent`, `in_stock`, `barcode` and `loyalty_points`. Asking for a product's own SKU returns the variant Cult Beauty selects for it, with a note. A list item's `price_from` is the lowest variant price when it is below the item's `price`.
- **Search pages are 40 at most.** `/search` takes `page_size` up to 40 (default 40); `/list` up to 200 (default 60). Paging reaches 10,000 positions.
- **10 latest reviews only.** `/product` returns `rating` and `review_count` (Cult Beauty's figures, per site: 4.51 from 509 on cultbeauty.co.uk and 4.46 from 492 on cultbeauty.com for the Glow Tonic) and `recent_reviews` [{`rating`, `date`, `text`}]: the 10 latest reviews the product page shows, no reviewer names. There is no review feed or review paging, and no Q&A.
- **No history.** Nothing is cached or kept: store each answer with its `fetched_at` for your own series.

Cult Beauty publishes no public API for its catalogue, prices, stock or reviews. Its affiliate programme runs on Awin, which offers product feeds to approved publishers; this skill reads the public product, list and offer pages with one Scavio key and needs no affiliate approval. Other vendors offer Cult Beauty data tools; this skill reads Cult Beauty's own public pages.

Cult Beauty, Lookfantastic and Dermstore make up THG plc's THG Beauty division, which THG reported at GBP 500.2m revenue for H1 2026 (THG plc interim results, Sep 10, 2026). THG reports the division, not Cult Beauty on its own. Quote this with its source, never from the samples.

See also: `lookfantastic-api` (Lookfantastic, 10 country sites, the same SKUs), `dermstore-skincare-prices-api` (Dermstore, US and Canada), `space-nk-api` (Space NK), `sephora-product-data` (Sephora) and `ulta-beauty-api` (Ulta Beauty). Same product and size only: match on the barcode where both sides return one, otherwise brand + name + size in both titles, each price with its retailer, site, currency and time.

## When to trigger

Use this skill when the user asks to:
- Read a Cult Beauty product's price, RRP, discount, stock, barcode and offer by SKU or link
- Compare every shade or size of one Cult Beauty product, each with its own price, discount and stock
- Read Cult Beauty prices in another currency (USD, EUR, AUD, CHF, AED, JPY ...) or on cultbeauty.com
- List Cult Beauty's current offers (Black Friday tiers, gifts with purchase) with their end times
- Search Cult Beauty by keyword or SKU, sorted by price, popularity, newest or discount, filtered by brand, skin type, concern, SPF content, key ingredient, formulation, product range, price, rating or discount
- List any Cult Beauty page: a brand, a category (Korean Beauty, Skincare), Black Friday or an offer tier
- Track a product's Cult Beauty discount through an event (read it at set times, store each answer)
- Put a Cult Beauty product next to the same product and size at Lookfantastic, Space NK, Sephora or Ulta
- Read a product's rating, review count and 10 latest reviews, ingredients and directions
- List Cult Beauty's brands or its category tree

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, search and suggestions took under 1 second, brands 1, offers 1.5, categories 4, product 5 and a Black Friday list with facets 6. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/cultbeauty/search` | Products for keywords or a SKU: price, RRP, discount, lowest variant price, stock, rating, review count and the offer per product; up to 40 per page, 7 sorts, filters, facets on request; `resolved_from` when Cult Beauty maps the keyword to a page | 1 |
| `POST /api/v1/cultbeauty/list` | The products of any list page by path or link (brand, category, Black Friday, an offer tier), same fields, sorts and filters as search, up to 200 per page | 1 |
| `POST /api/v1/cultbeauty/product` | One product by SKU or link: price, RRP, discount, barcode, every variant with its own price, stock and barcode, ingredients, directions, loyalty points, the offer, rating, review count, the 10 latest reviews | 1 |
| `POST /api/v1/cultbeauty/suggestions` | The search-box suggestions: suggested searches, corrections and up to 5 products with price | 1 |
| `POST /api/v1/cultbeauty/offers` | The current offers as cultbeauty.co.uk's voucher-codes page lists them: title, text, code, gift, spend threshold, end time, the offer's list path (`gb` only) | 1 |
| `POST /api/v1/cultbeauty/brands` | The A-Z brand directory of the site asked (289 brands on cultbeauty.co.uk, 265 on cultbeauty.com captured), optionally one letter | 1 |
| `POST /api/v1/cultbeauty/categories` | The category tree as the site navigation shows it (11 menus, 454 nodes on cultbeauty.co.uk captured) | 1 |

## Markets

Every endpoint takes `market` and `currency`, and every answer carries `market` {`market`, `site`, `language`, `currency`, `shipping_destination`}.

| `market` | Site | Default currency | Other currencies | Offers |
|---|---|---|---|---|
| `gb` (default; also `uk`, `co.uk`) | www.cultbeauty.co.uk, the UK site | GBP (ships to GB) | EUR (IE), USD, AUD, CHF, AED, SAR, ILS, HKD, SGD, JPY, CNY | yes |
| `intl` (also `international`, `com`) | www.cultbeauty.com, the international site | EUR (ships to MT) | GBP, USD, AUD, CHF, AED, SAR, ILS, HKD, SGD, JPY, CNY | no (`400`) |

- The site's host name works as `market` too (`cultbeauty.com`).
- Each currency pairs with the shipping destination Cult Beauty's selector gives it (`USD` ships to `US`, `AUD` to `AU`): `shipping_destination` in the answer says which.
- Both sites are in English. SKUs are the same on both; each site has its own brand directory (289 vs 265 brands) and its own navigation (Korean Beauty on the UK site reads Korean Skincare on cultbeauty.com).
- Captured 2026-11-26, CeraVe Resurfacing Retinol Serum 30ml read 17.63 GBP (RRP 23.50) on `gb` and 19.42 EUR (RRP 25.90) on `intl`, both 25% off. Show each price with its site and currency; never convert one into another.

## Prices, offers, variants and reviews

Every list item (search, list) carries:

| Field | Meaning |
|---|---|
| `price` | Cult Beauty's price for a visitor without an account, in the currency asked |
| `rrp` | Cult Beauty's RRP, as given |
| `discount_percent` | Computed by Scavio from `price` and `rrp`, only when the RRP is above the price; `null` otherwise |
| `price_from` | The lowest variant price when it is below `price` (PIXI Glow Tonic 250ml at 12.60 GBP read `price_from` 7, the 100ml); `null` otherwise |
| `in_stock` | Cult Beauty's online availability for the site, as given |
| `rating`, `review_count` | Cult Beauty's figures for the product on that site |
| `offer` | {`title`, `description`, `free_gift`, `url`}: Cult Beauty's promotion text for the product, as given; dates only inside the text |
| `variants_count`, `options` | How many variants and which option types (`Size`, `Shade`, `Option`) |

- **Offers per product:** a product's `offer` is the campaign Cult Beauty shows on it ("30% OFF": "Save 30% on selected products. Discount has been applied to the RRP. Offer valid for a limited time only"), or a label such as "NEW SHADE". Captured 2026-11-26 on the Black Friday list: Patrick Ta Major Headlines Blush & Balm Set - Vanilla Chai (Worth £59) at 33.60 GBP (RRP 48) and Sol de Janeiro Sol & Cheer Set (Worth £33.00) at 20.30 GBP (RRP 29), both "30% OFF".
- **Offers page (`/offers`, gb):** captured 2026-11-26: 9 offers, Black Friday "10% OFF" and "20% OFF" tiers ending 2026-11-26T16:30:00Z and "Early access" tiers (15% to 30% OFF, "Must be logged into your account to redeem") ending 2026-11-26T12:00:00Z, each with the list page of its products. Quote early-access tiers as account-only, as the text states.
- **Variants (product):** `variants[]` {`sku`, `name`, `option_type`, `option`, `shade_colour`, `price`, `rrp`, `discount_percent`, `in_stock`, `availability_message`, `preorder`, `max_per_order`, `loyalty_points`, `barcode`}. `shade_colour` is the shade's colour code as given (`#E997A3` for Stargaze). The product's own fields are those of the SKU asked for (or the variant Cult Beauty selects for a product SKU).
- **Stock:** Pat McGrath Labs Divine Skin The Essence Serum - Rose 001 100ml read `in_stock` `false` with "Sold out" at 60.75 GBP (RRP 81). Report it as the site's online availability at that time.
- **Barcode (product):** `barcode` is the EAN-13 or UPC Cult Beauty lists, as given; `null` when it lists none (sets and pre-release items).
- **Loyalty points:** `loyalty_points` as Cult Beauty shows them per product and variant (19 on the 19.18 GBP lip balm shade).
- **Reviews (product):** `rating`, `review_count` and `recent_reviews` (10 latest, `text` may be `null`). Report the counts and stars; quote a review's text only as that reviewer's own words.

## Workflow

1. **Find products.** `/search` with `q` (keywords or a SKU), `market`, and optionally `currency`, `sort`, filters and `page_size`. Check `resolved_from`: when set, the results are the products of the page Cult Beauty maps the keyword to. Each `items[].sku` is the input of `/product`.
2. **Read one product.** `/product` with `sku` (or `url`, an `items[].url` link): every shade or size with its own price, discount, stock and barcode, the offer, reviews.
3. **Across currencies and sites.** The same `/product` call with another `currency`, or with `market` `intl`. Show each price with its site, currency and time.
4. **Through an event.** Read the same SKUs at set times during a sale (1 credit each); `/offers` (gb) gives each tier's `ends`. Store every answer with `fetched_at`: that series is your record of when a discount changed.
5. **Read the offers.** `/offers` for the current offers with `gift`, `threshold` and `ends`; send an offer's `list_path` to `/list` (`path`, `market` `gb`) for the products it covers. Or `/brands` for a brand's `path`, then `/list`.
6. **Narrow a list.** `/search` or `/list` with `include_facets` `true` gives Cult Beauty's filter options with counts; a facet's `filter` names the input it maps to (`brand`, `skin_type`, `concern`, `spf`, `key_ingredient`, `formulation`, `range`, `min_price / max_price`, `min_discount / max_discount`, `min_rating`), or `filters` for any other facet (send `{"facet": facets[].facet, "value": options[].value}`). Send `options[].value` exactly.
7. **Compare retailers.** Read the same SKU on `lookfantastic-api`, or search the same brand and product on `space-nk-api`, `sephora-product-data` or `ulta-beauty-api`; keep a row only where the barcode matches, or brand, name and size all match, and show each price with its retailer and time.
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Every endpoint

| Parameter | Type | Default | Description |
|---|---|---|---|
| `market` | string | `gb` | `gb` (cultbeauty.co.uk) or `intl` (cultbeauty.com), or the host name. Anything else is a `400`, not charged |
| `currency` | string | `GBP` on gb, `EUR` on intl | GBP, EUR, USD, AUD, CHF, AED, SAR, ILS, HKD, SGD, JPY or CNY. Anything else is a `400`, not charged |

### Search (`/search`) and list (`/list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required (search) | Keywords or a Cult Beauty SKU (up to 200 chars). A keyword Cult Beauty maps to a page returns that page's products, with `resolved_from` |
| `path` | string | one of (list) | A list page path, as in its /c/ link: `/skin-care`, `/brands/cerave`, `/black-friday-cyber-monday`, `/skin-care/korean-skin-care`, an offer tier `/black-friday-cyber-monday/app/shop-all/20`. Paths come from `/categories`, `/brands` and `/offers` |
| `url` | string | one of (list) | A list page link, `https://www.cultbeauty.co.uk/c/<page>/` (or cultbeauty.com), instead of `path` |
| `page` | integer | 1 | Page; at most 10,000 positions (`page` x `page_size`) |
| `page_size` | integer | 40 (search), 60 (list) | 1-40 on search, 1-200 on list |
| `sort` | string | `relevance` | `relevance`, `popularity`, `price_low`, `price_high`, `name`, `newest`, `discount` (highest percent off first): Cult Beauty's sort menu |
| `brand` | string or list | none | Brand as Cult Beauty names it (`CeraVe`) |
| `skin_type` | string or list | none | `Dry`, `Oily`, `Sensitive` ... as Cult Beauty lists it |
| `concern` | string or list | none | `Anti-Ageing`, `Dry`, `Dullness` ... |
| `spf` | string or list | none | `No SPF`, `SPF 15+`, `SPF 30+` ... |
| `key_ingredient` | string or list | none | `Retinol`, `Hyaluronic Acid` ... |
| `formulation` | string or list | none | `Vegan`, `Alcohol Free` ... |
| `range` | string or list | none | A brand's product range as Cult Beauty lists it (`Advanced Snail 96`) |
| `filters` | list | none | Any other facet: up to 10 {`facet` (`facets[].facet`, e.g. `en_beauty_skinSubcategory_content`), `value` (one or a list of `options[].value`)} |
| `min_price`, `max_price` | number | none | Price range in the currency asked |
| `min_rating` | number | none | Lowest average stars (1-5); applied by Cult Beauty's own filter, a few items can show a rating just below it |
| `min_discount`, `max_discount` | number | none | Percent off Cult Beauty's RRP (0-100) |
| `include_facets` | boolean | false | Also return Cult Beauty's filter counts. Still 1 credit |

A filter list takes up to 10 values. An editorial page without a product list is listed through its shop-all page (`/black-friday-cyber-monday` lists `/black-friday-cyber-monday/shop-all`; `listed_path` and a note say so).

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | one of | A Cult Beauty SKU (`items[].sku` or `variants[].sku`, `11200055`); the same on both sites |
| `url` | string | one of | A product link, `https://www.cultbeauty.co.uk/p/<name>/<sku>/`; the site still comes from `market` |

### Suggestions, offers, brands, categories

`/suggestions` takes `q` (the text typed so far, up to 100 chars). `/offers` and `/categories` take only `market` and `currency` (`/offers` on `gb` only). `/brands` takes an optional `letter` (`A`-`Z`, or `0-9`).

## Examples

### One product with every shade

```bash
curl -X POST https://api.scavio.dev/api/v1/cultbeauty/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "12436381"}'
```

Captured `data` (2026-11-26; `variants` cut to 3 of 9, `recent_reviews` to 2 of 10, `subtitle`, `description`, `directions`, `ingredients`, `images`, `breadcrumbs` and `notes` dropped):

```json
{
  "market": { "market": "gb", "site": "www.cultbeauty.co.uk", "language": "en", "currency": "GBP", "shipping_destination": "GB" },
  "requested_sku": "12436381",
  "sku": "17661748",
  "product_sku": "12436381",
  "name": "NARS Afterglow Lip Balm - Triple X",
  "product_name": "NARS Afterglow Lip Balm 3g (Various Shades)",
  "brand": "NARS",
  "url": "https://www.cultbeauty.co.uk/p/nars-afterglow-lip-balm-3g-various-shades/12436381/",
  "price": 19.18,
  "rrp": 29.5,
  "discount_percent": 35,
  "currency": "GBP",
  "in_stock": true,
  "availability_message": "In stock | Usually dispatched within 24 hours",
  "barcode": "194251154718",
  "option_type": "Shade",
  "option": "Triple X",
  "variants": [
    { "sku": "17661748", "name": "NARS Afterglow Lip Balm - Triple X", "option_type": "Shade", "option": "Triple X", "shade_colour": "#FFFFFF", "price": 19.18, "rrp": 29.5, "discount_percent": 35, "in_stock": true, "availability_message": "In stock | Usually dispatched within 24 hours", "preorder": false, "max_per_order": null, "loyalty_points": 19, "barcode": "194251154718" },
    { "sku": "17661752", "name": "NARS Afterglow Lip Balm - Stargaze", "option_type": "Shade", "option": "Stargaze", "shade_colour": "#E997A3", "price": 19.18, "rrp": 29.5, "discount_percent": 35, "in_stock": true, "availability_message": "In stock | Usually dispatched within 24 hours", "preorder": false, "max_per_order": null, "loyalty_points": 19, "barcode": "194251154725" },
    { "sku": "17661756", "name": "NARS Afterglow Lip Balm - Orgasm", "option_type": "Shade", "option": "Orgasm", "shade_colour": "#E26675", "price": 20.65, "rrp": 29.5, "discount_percent": 30, "in_stock": true, "availability_message": "In stock | Usually dispatched within 24 hours", "preorder": false, "max_per_order": null, "loyalty_points": 21, "barcode": "194251154732" }
  ],
  "volume": null,
  "loyalty_points": 19,
  "max_per_order": null,
  "preorder": false,
  "offer": { "title": "NEW SHADE", "description": "New Shades at Cult Beauty!", "free_gift": null, "url": "https://www.cultbeauty.co.uk/c/auto-paps/new-brands/" },
  "rating": 4.61,
  "review_count": 1280,
  "recent_reviews": [
    { "rating": 5, "date": "2026-11-18", "text": "I absolutely love this lip balm! It feels incredibly comfortable, keeps my lips soft and hydrated, and gives them a beautiful natural shine. The texture is lovely, non-sticky and easy to apply. A perfect everyday lip essential! Adhesion the lip balm glides on smoothly and stays comfortably on my lips, leaving a lovely, even finish without feeling sticky." },
    { "rating": 5, "date": "2026-11-16", "text": "Genuinely my favourite lipstick! I wear this everyday! It’s truly hydrating and beautiful!" }
  ]
}
```

`12436381` is the product's SKU, so the answer is the shade Cult Beauty selects for it (Triple X), with a note; `variants` lists all 9 shades, six at 19.18 GBP (35% off) and three at 20.65 GBP (30% off), each with its own barcode. An unknown SKU is a charged `404`.

### The same SKU on cultbeauty.com

```bash
curl -X POST https://api.scavio.dev/api/v1/cultbeauty/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "11200055", "market": "intl"}'
```

Captured (2026-11-26): `market` {`market` `intl`, `site` `www.cultbeauty.com`, `language` `en`, `currency` `EUR`, `shipping_destination` `MT`}, PIXI Glow Tonic Glycolic Acid Toner 250ml, `price` 14.21, `rrp` 20.3, `discount_percent` 30, `barcode` `885190821006`, the 100ml variant at 8.96 EUR (RRP 12.80), `loyalty_points` 14, `offer` "30% OFF", `rating` 4.46 from `review_count` 492. About an hour earlier the same call read 15.23 EUR (25% off), and `market` `gb` with `currency` `USD` read 17.82 USD (RRP 23.76, 25% off, `shipping_destination` `US`).

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/cultbeauty/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "glow tonic", "page_size": 10}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 10, `url`, `image` and `notes` dropped):

```json
{
  "market": { "market": "gb", "site": "www.cultbeauty.co.uk", "language": "en", "currency": "GBP", "shipping_destination": "GB" },
  "query": "glow tonic",
  "resolved_from": null,
  "corrected_query": null,
  "total": 20,
  "total_pages": 2,
  "page": 1,
  "page_size": 10,
  "has_more": true,
  "count": 10,
  "sort": "relevance",
  "filters_applied": {},
  "items": [
    { "position": 1, "sku": "11200055", "name": "PIXI Glow Tonic 250ml (Worth £25.00)", "brand": "PIXI", "price": 12.6, "rrp": 18, "discount_percent": 30, "price_from": 7, "currency": "GBP", "in_stock": true, "rating": 4.51, "review_count": 509, "offer": { "title": "30% OFF", "description": "Save 30% on selected products. Discount has been applied to the RRP. Offer valid for a limited time only", "free_gift": null, "url": "https://www.cultbeauty.co.uk/auto-paps/pricing-campaign-30.list" }, "variants_count": 2, "options": ["Size"] },
    { "position": 2, "sku": "12708820", "name": "Medik8 Press & Glow, Daily PHA Exfoliating Facial Toner Refill 200ml", "brand": "Medik8", "price": 21.75, "rrp": 29, "discount_percent": 25, "price_from": null, "currency": "GBP", "in_stock": true, "rating": 4.84, "review_count": 1415, "offer": { "title": "25% OFF", "description": "Save 25% on selected products. Discount has been applied to the RRP. Offer valid for a limited time only", "free_gift": null, "url": "https://www.cultbeauty.co.uk/auto-paps/pricing-campaign-25.list" }, "variants_count": 2, "options": ["Size"] }
  ]
}
```

### Mapped keywords

- `/search` `{"q": "cerave"}`: `resolved_from` {`type` `landing`, `path` `/brands/cerave`, `listed_path` `/brands/cerave/shop-all`, `url` `https://www.cultbeauty.co.uk/c/brands/cerave/`, `title` "CeraVe | Dermatologist-Developed Skincare | Cult Beauty"}, `total` 48; first CeraVe Resurfacing Retinol Serum with Ceramides and Niacinamide for Blemish-Prone Skin 30ml at 17.63 GBP (RRP 23.50).
- `/search` `{"q": "retinol serum", "market": "intl"}`: `resolved_from` {`type` `category`, `path` `/skin-care/ingredients/retinol`}, `total` 201, first Paula's Choice Retinol Body Treatment (118ml) at 39 EUR with `discount_percent` `null`, then Medik8 Crystal Retinal 10 30ml at 82.50 EUR (RRP 110).
- `/search` `{"q": "vitamin c", "currency": "USD", "sort": "popularity"}`: resolved to `/skin-care/ingredients/vitamin-c`, `total` 367; first Huda Beauty Faux Filter Color Corrector 9ml at 24.02 USD (RRP 34.32). The ingredient page lists every product tagged with it, not only serums: say so when reporting.

### Offers with end times

```bash
curl -X POST https://api.scavio.dev/api/v1/cultbeauty/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-26; `offers` cut to 3 of 9, `notes` dropped):

```json
{
  "market": { "market": "gb", "site": "www.cultbeauty.co.uk", "language": "en", "currency": "GBP", "shipping_destination": "GB" },
  "count": 9,
  "offers": [
    {
      "title": "10% OFF",
      "description": "Don’t miss out on the chance to stock up on your favourite beauty essentials with our Black Friday 10% OFF savings. Discount has been applied to the RRP. T&Cs apply.",
      "code": null,
      "gift": null,
      "threshold": null,
      "ends": "2026-11-26T16:30:00.000Z",
      "url": "https://www.cultbeauty.co.uk/c/black-friday-cyber-monday/app/shop-all/10/",
      "list_path": "/black-friday-cyber-monday/app/shop-all/10"
    },
    {
      "title": "20% OFF",
      "description": "Don’t miss out on the chance to stock up on your favourite beauty essentials with our Black Friday 20% OFF savings. Discount has been applied to the RRP. T&Cs apply.",
      "code": null,
      "gift": null,
      "threshold": null,
      "ends": "2026-11-26T16:30:00.000Z",
      "url": "https://www.cultbeauty.co.uk/c/black-friday-cyber-monday/app/shop-all/20/",
      "list_path": "/black-friday-cyber-monday/app/shop-all/20"
    },
    {
      "title": "Early access - 25% OFF",
      "description": "Early Access - 25% OFF selected beauty. Discount has been applied to the RRP. Must be logged into your account to redeem. Valid for a limited time only.",
      "code": null,
      "gift": null,
      "threshold": null,
      "ends": "2026-11-26T12:00:00.000Z",
      "url": "https://www.cultbeauty.co.uk/c/black-friday-cyber-monday/app/shop-all/25/",
      "list_path": "/black-friday-cyber-monday/app/shop-all/25"
    }
  ]
}
```

`code`, `gift` and `threshold` are read from the offer text when it states them (`null` otherwise). `ends` is Cult Beauty's end time; there is no start date. Send `list_path` to `/list` (`market` `gb`) for the tier's products. The same call with `market` `intl` is a `400` (cultbeauty.com has no voucher-codes page), not charged.

### List, suggestions, brands, categories

- `/list` `{"path": "/black-friday-cyber-monday", "include_facets": true, "page_size": 10}`: listed through `/black-friday-cyber-monday/shop-all` (with a note), `total` 10,050, first the Patrick Ta set at 33.60 GBP (RRP 48). `facets` included Price (`cbeauty_GBP_price`, `min_price / max_price`: 15-30 GBP 4,062), Brand (`brand`), Average Reviews (`min_rating`: 4+ 4,708), Savings (`min_discount / max_discount`: 25% - 50% 9,330), and Skincare Product Type, Makeup Category, Haircare Category, Fragrance, Bath & Body and Wellness with `filter` `filters`: send those through `filters`.
- `/list` `{"path": "/skin-care", "concern": "Anti-Ageing", "min_rating": 4}`: `total` 112; first Medik8 Advanced Night Restore, Multi-Ceramide Night Cream 50ml at 46.50 GBP (RRP 62), Paula's Choice Skin Perfecting 2% BHA Exfoliating Toner 30ml at 9.10 GBP (RRP 13).
- `/suggestions` `{"q": "olaplex"}`: `terms` "olaplex", "olaplex no", "olaplex no 4", "olaplex no 5", "olaplex 7"; 5 `products`, first Olaplex Total Hair Repair Set (Worth £82) at 39.20 GBP (RRP 56).
- `/brands` `{}`: `total_brands` 289, each {`name`, `path`, `url`, `letter`} (`111SKIN` under `0-9`, `/brands/111skin`); 265 on `intl`.
- `/categories` `{}`: 11 menus (Black Friday `/black-friday-cyber-monday`, Christmas, New & Trending, Brands, Skincare `/skin-care`, Korean Beauty `/skin-care/korean-skin-care`, Makeup `/make-up`, Fragrance, Haircare, Bodycare & Wellness, Cult Conscious), `total_categories` 454. Seasonal menus change.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def cultbeauty(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/cultbeauty/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Every shade of one product (1 credit)
p = cultbeauty("product", {"sku": "12436381"})["data"]
for v in p["variants"]:
    print(v["option"], v["price"], v["rrp"], v["discount_percent"], v["in_stock"], v["barcode"])

# 2. One SKU per site and currency (1 credit each)
for body in ({"market": "gb"}, {"market": "gb", "currency": "USD"}, {"market": "intl"}):
    d = cultbeauty("product", {"sku": "11200055", **body})
    print(body, d["data"]["price"], d["data"]["currency"], d["data"]["discount_percent"], d["fetched_at"])

# 3. Current offers with end times (UK site, 1 credit)
for o in cultbeauty("offers", {})["data"]["offers"]:
    print(o["title"][:60], o["ends"], o["list_path"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`market`, `site`, `language`, `currency`, `shipping_destination`} and `notes`.

- **item** (search, list) - `position`, `sku`, `name`, `brand`, `url`, `image`, `price`, `rrp`, `discount_percent`, `price_from`, `currency`, `in_stock`, `rating`, `review_count`, `offer` {`title`, `description`, `free_gift`, `url`}, `variants_count`, `options`.
- **search** - `query`, `resolved_from` (or `null`), `corrected_query`, `total`, `total_pages`, `page`, `page_size`, `has_more`, `count`, `sort`, `filters_applied`, `items[]`, `facets` (with `include_facets`) [{`facet`, `filter`, `label`, `type`, `options` [{`value`, `label`, `count`} or {`label`, `from`, `to`, `count`}]}].
- **list** - `path`, `listed_path`, `url`, then as search from `total`.
- **product** - `requested_sku`, `sku`, `product_sku`, `name`, `product_name`, `brand`, `url`, `price`, `rrp`, `discount_percent`, `currency`, `in_stock`, `availability_message`, `barcode`, `option_type`, `option`, `variants[]`, `subtitle`, `description`, `key_benefits`, `directions`, `ingredients`, `at_a_glance`, `volume`, `faq`, `images`, `loyalty_points`, `max_per_order`, `preorder`, `offer`, `rating`, `review_count`, `recent_reviews[]` {`rating`, `date`, `text`}, `breadcrumbs`.
- **suggestions** - `query`, `count`, `terms[]`, `corrections[]`, `products[]` {`sku`, `name`, `url`, `image`, `price`, `rrp`, `discount_percent`, `currency`, `rating`, `review_count`}.
- **offers** - `count`, `offers[]` {`title`, `description`, `code`, `gift`, `threshold`, `ends`, `url`, `list_path`}.
- **brands** - `letter`, `total_brands`, `count`, `brands[]` {`name`, `path`, `url`, `letter`}.
- **categories** - `count`, `total_categories`, `categories[]` {`name`, `path`, `url`, `children[]`}.

## Guardrails

- Name it "Cult Beauty (cultbeauty.co.uk, the UK beauty retailer, with its international site cultbeauty.com)" on first mention, "Cult Beauty" after that, and name the site for every price.
- Prices: quote `price` with its currency, the site and the `fetched_at` time ("listed on cultbeauty.co.uk on Nov 26, 2026 at <fetched_at time> UTC"); during an event give the time, not only the date. `rrp` is "Cult Beauty's RRP, as it gives it"; `discount_percent` is "computed by Scavio from Cult Beauty's price and RRP". A computed price after a stated rate is your own arithmetic: label it computed and not checked out.
- Sites and currencies: every price belongs to one site and one currency. Never convert, average or merge them into one "Cult Beauty price".
- Offers: quote rate, gift, gift value and threshold exactly as Cult Beauty writes them, with `ends` and the capture time. Early-access tiers are account-only, as the text states. No countdowns, urgency or "real deal" / "fake discount" language.
- Comparisons: same product and size only (barcode where both sides return it, else brand + name + size), each price with its retailer, site, currency and time; show the numbers and their difference only. Never call a retailer or a price the cheapest, a deal, a bargain or a rip-off.
- Descriptive only: never say a product or seller is authentic, genuine, counterfeit, authorized or unauthorized, never give a legit or scam verdict on any retailer, and never make MAP claims or comment on Cult Beauty's pricing practices.
- No efficacy, SPF or medical claims. Report SPF content, concerns and ingredients as Cult Beauty labels them; quote review text only as that reviewer's own words.
- Reviews: counts, stars, dates and text as returned; no reviewer names are returned, never try to identify reviewers. Do not republish Cult Beauty product photos or descriptions at length; cite products by name, SKU and site instead.
- Names: use "Cult Beauty" only for cultbeauty.co.uk and cultbeauty.com; never treat lookalike domains or similarly named sites as Cult Beauty.
- Terms: Scavio does not collect or store Cult Beauty data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Cult Beauty's terms and conditions cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, RRPs, offers, end dates, SKUs, barcodes or reviews. Only return what the API returned, with the `fetched_at` time and the product `url`.
- Not available: a full review feed or review paging (only the 10 latest via product), Q&A, store pages, member or early-access prices, basket or checkout prices, code-applied prices, offers on cultbeauty.com, price history (store your own), offer start dates.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `market` other than `gb` or `intl`; a `currency` not among the 12 ("currency CAD is not offered on www.cultbeauty.co.uk (market gb): send one of GBP, EUR, USD ..."); `/offers` with `market` `intl` ("Offers are not available on www.cultbeauty.com: it has no voucher-codes page. Send market gb (www.cultbeauty.co.uk)."); search without `q`; list without `path` or `url`, or with both, a path that is not a list page (a product, search or account page), a link that is not a /c/ page of a Cult Beauty site; product without `sku` or `url`, or with both, a SKU that is not 5-10 digits, a link that is not a /p/ product link; `page` past 10,000 positions; `page_size` above 40 on search or 200 on list; an unknown `sort`; `min_price` above `max_price`; `min_discount` above `max_discount`; a range facet sent through `filters` (use `min_price` / `max_price`, `min_discount` / `max_discount` or `min_rating`); more than 10 values in a filter list or 10 `filters`; a `letter` that is not A-Z or 0-9.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Cult Beauty has no product with SKU <sku> on <site>.", "Cult Beauty has no list page at <path> on <site>.", "Cult Beauty's page <path> on <site> has no product list.". Take SKUs and paths from a previous answer, on the same site, rather than guessing them. A search with no matches is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api).
- `502` means Cult Beauty data was temporarily unavailable ("Cult Beauty is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Cult Beauty is busy ("Cult Beauty is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- A `/product` answer whose notes say the product page did not answer in time carries `rating`, `review_count`, `recent_reviews`, `offer` and `breadcrumbs` as `null` (the prices and variants are there): retry for the full answer.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.cultbeauty.search({ q: "glow tonic", currency: "USD" });
const { data: list } = await scavio.cultbeauty.list({ path: "/black-friday-cyber-monday", sort: "discount" });
const { data: product } = await scavio.cultbeauty.product({ sku: "12436381" });
const { data: offers } = await scavio.cultbeauty.offers();
const { data: brands } = await scavio.cultbeauty.brands({ letter: "N", market: "intl" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.cultbeauty.search(...)`, `list`, `product`, `suggestions`, `offers`, `brands` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_cultbeauty`, `get_cultbeauty_list`, `get_cultbeauty_product`, `get_cultbeauty_suggestions`, `get_cultbeauty_offers`, `get_cultbeauty_brands` and `get_cultbeauty_categories`. Cult Beauty is opt-in: add `cultbeauty` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,cultbeauty"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/cultbeauty-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api), [list](https://scavio.dev/docs/cultbeauty-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api), [product](https://scavio.dev/docs/cultbeauty-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api), [suggestions](https://scavio.dev/docs/cultbeauty-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api), [offers](https://scavio.dev/docs/cultbeauty-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api), [brands](https://scavio.dev/docs/cultbeauty-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api), [categories](https://scavio.dev/docs/cultbeauty-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api). Overview: [Cult Beauty API](https://scavio.dev/cultbeauty-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cult-beauty-api).
