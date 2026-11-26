# Lookfantastic API - Look Fantastic Prices by Country, Offers, Shades

Read Lookfantastic (lookfantastic.com, the beauty retailer with 10 country sites, part of THG Beauty with Cult Beauty and Dermstore) on any of its 10 sites and, on lookfantastic.com, in any of its 22 currencies: search, any list page, one product in full with every variant, search suggestions, the current offers, the brand directory and the category tree. Every answer comes as the site's page shows it to a visitor without an account, in that site's language. All 7 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Lookfantastic shows to any visitor and returns them as JSON for analysis. It uses no Lookfantastic account, no cart, no checkout, no code redemption and no loyalty login.

**The job this skill is for: one beauty product's price on each Lookfantastic site and in each currency.** Lookfantastic keeps its own price list per site and per currency, so the same SKU reads differently from one country site to the next, and an RRP and a discount come with each. Captured 2026-11-26 with `/product` (`sku` `11200055`, PIXI Glow Tonic 250ml, barcode `885190821006`, 1 credit per site):

| `market` (site) | Price | RRP | `discount_percent` | Offer text, as the site gives it |
|---|---|---|---|---|
| `gb` (lookfantastic.com) | 12.60 GBP | 18 | 30 | Save 30% + Extra 5% off \| Use Code: EXTRA |
| `ie` (lookfantastic.ie) | 14.49 EUR | 20.70 | 30 | Save 30% + Extra 5% off \| Use Code: EXTRA |
| `de` (lookfantastic.de) | 14.49 EUR | 20.70 | 30 | 30% + Doppelte +Punkte |
| `fr`, `nl`, `at` | 14.49 EUR | 20.70 | 30 | Économisez -30% (fr), 30% + Dubbele +Punten (nl), -30% Rabatt (at) |
| `es`, `it` | 16.56 EUR | 20.70 | 20 | 20% de descuento (es), 20% di sconto (it) |
| `eu` (eu.lookfantastic.com) | 20.95 EUR | 20.95 | `null` | none |
| `pl` (lookfantastic.pl) | 66.15 PLN | 94.50 | 30 | 30% ZNIŻKI |

The same RRP (20.70 EUR) carried a 30% discount on six euro sites and a 20% discount on Spain and Italy, and the EU site priced it at its own RRP with no discount. The product's `rating` and `review_count` are per site too (4.7 from 724 reviews on lookfantastic.com, 4.91 from 11 on lookfantastic.fr, 5 from 4 on lookfantastic.pl). Read each site you report on; never assume one site's price or rating for another.

Ten limits shape every answer, so say them plainly:
- **1 credit per call** on every endpoint. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **RRP as given, discount computed.** `rrp` is Lookfantastic's RRP exactly as the site gives it. `discount_percent` is computed by Scavio from `price` and `rrp`, and only when the RRP is above the price; otherwise it is `null`. On Lookfantastic the page price usually carries the sale already ("Discount has been applied to the RRP").
- **Code prices are arithmetic, not data.** An extra code in the offer text ("Extra 5% off | Use Code: EXTRA") is applied in the site's basket and is not in `price`. A price after a code is your own computation: label it "computed, not checked out". Member prices and basket-only discounts are not returned.
- **One site, one currency, one price list.** `market` picks the site (`gb` default, `de`, `fr`, `es`, `it`, `nl`, `pl`, `at`, `ie`, `eu`) and `currency` the currency that site's own selector offers. Nothing is converted by Scavio. A currency the site does not offer is a `400`, not charged; every answer's currency is checked against the one asked.
- **Each site answers in its own language.** Titles, descriptions, offer text, availability text and categories come in the site's language (German on `de` and `at`, French on `fr` ...). Search with keywords in that language (`gesichtsreinigung` on `de`); facet names carry the site's language prefix (`en_` on lookfantastic.com, `de_` on lookfantastic.de).
- **Mapped keywords resolve to a page.** Lookfantastic sends many keywords (a brand such as cerave, a generic term such as face wash on the Irish site) to one of its pages instead of search results; `/search` then returns that page's products and says so in `resolved_from` {`type` (`brand`, `category`, `landing` or `product`), `path`, `listed_path`, `url`, `title`, `sku`} and in `notes`. Always check `resolved_from` before calling an answer "search results for q".
- **Variants carry their own price.** A product's `variants[]` (shades, sizes) each have their own `sku`, `price`, `rrp`, `discount_percent`, `in_stock`, `barcode` and `loyalty_points`. A list item's `price_from` is the lowest variant price when it is below the item's `price`. Compare the variant, never the product range.
- **Search pages are 40 at most.** `/search` takes `page_size` up to 40 (default 40); `/list` up to 200 (default 60). Paging reaches 10,000 positions.
- **10 latest reviews only.** `/product` returns `rating` and `review_count` (the site's figures) and `recent_reviews` [{`rating`, `date`, `text`}]: the 10 latest reviews the product page shows, no reviewer names. There is no review feed or review paging, and no Q&A.
- **No history.** Nothing is cached or kept: store each answer with its `fetched_at` for your own series.

Lookfantastic publishes no public API for its catalogue, prices, stock or reviews. Its affiliate programme runs on Awin, which offers product feeds to approved publishers; this skill reads the public product, list and offer pages with one Scavio key and needs no affiliate approval. Other vendors offer Lookfantastic data tools; this skill reads Lookfantastic's own public pages.

Lookfantastic, Cult Beauty and Dermstore make up THG plc's THG Beauty division, which THG reported at GBP 500.2m revenue for H1 2026 (THG plc interim results, Sep 10, 2026). THG reports the division, not Lookfantastic on its own. Quote this with its source, never from the samples.

See also: `cult-beauty-api` (Cult Beauty; Lookfantastic and Cult Beauty use the same SKUs, so the same `sku` reads on both: PIXI Glow Tonic 250ml was 12.60 GBP on each UK site on 2026-11-26), `dermstore-skincare-prices-api` (Dermstore, US and Canada), `space-nk-api` (Space NK), `sephora-product-data` (Sephora) and `ulta-beauty-api` (Ulta Beauty). Same product and size only: match on the barcode where both sides return one, otherwise brand + name + size in both titles, each price with its retailer, site, currency and date.

## When to trigger

Use this skill when the user asks to:
- Read a Lookfantastic product's price, RRP, discount, stock, barcode and offer by SKU or link, on one site or several
- Put one product's price on lookfantastic.com next to the German, French, Spanish, Italian, Dutch, Polish, Austrian, Irish and EU sites
- Read lookfantastic.com prices in another currency (USD, EUR, AUD, CAD, JPY, AED ...)
- Compare every shade or size of one product, each with its own price, stock and barcode
- List Lookfantastic's current offers (gift with purchase, spend thresholds, Black Friday) with their end times
- Search Lookfantastic by keyword or SKU, sorted by price, popularity, newest or discount, filtered by brand, skin type, concern, SPF band, key ingredient, formulation, price, rating or discount
- List any Lookfantastic page: a brand, a category, Black Friday or an offer page
- Put a Lookfantastic product next to the same product and size at Cult Beauty, Space NK, Sephora or Ulta
- Read a product's rating, review count and 10 latest reviews, ingredients and directions
- List Lookfantastic's brands or its category tree on any site

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (the same product on all 10 sites is 10 credits).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search and suggestions took about 2 seconds, list, categories and search on a site other than lookfantastic.com about 3, offers 5, brands 6 and product 7 to 8. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/lookfantastic/search` | Products for keywords or a SKU: price, RRP, discount, lowest variant price, stock, rating, review count and the offer per product; up to 40 per page, 7 sorts, filters, facets on request; `resolved_from` when the site maps the keyword to a page | 1 |
| `POST /api/v1/lookfantastic/list` | The products of any list page by path or link (brand, category, Black Friday, an offer page), same fields, sorts and filters as search, up to 200 per page | 1 |
| `POST /api/v1/lookfantastic/product` | One product by SKU or link: price, RRP, discount, barcode, every variant with its own price, stock and barcode, ingredients, directions, loyalty points, the offer, rating, review count, the 10 latest reviews | 1 |
| `POST /api/v1/lookfantastic/suggestions` | The search-box suggestions: suggested searches, corrections and up to 5 products with price | 1 |
| `POST /api/v1/lookfantastic/offers` | The current offers as the site's voucher-codes page lists them: title, text, code, gift, spend threshold, end time, the offer's list path | 1 |
| `POST /api/v1/lookfantastic/brands` | The A-Z brand directory of the site asked (415 brands on lookfantastic.com, 177 on .de, 168 on .fr, 189 on .pl captured), optionally one letter | 1 |
| `POST /api/v1/lookfantastic/categories` | The category tree as the site navigation shows it, in the site's language (13 menus and 574 nodes on lookfantastic.com captured) | 1 |

## Markets

Every endpoint takes `market` and `currency`, and every answer carries `market` {`market`, `site`, `language`, `currency`, `shipping_destination`}.

| `market` | Site | Language | `currency` |
|---|---|---|---|
| `gb` (default; also `uk`, `com`) | www.lookfantastic.com, the UK and international site | English | GBP (default), USD, EUR, AUD, CAD, CHF, SEK, DKK, NOK, JPY, KRW, HKD, SGD, AED, SAR, ILS, NZD, CNY, MYR, TWD, THB, IDR |
| `de` | www.lookfantastic.de | German | EUR |
| `fr` | www.lookfantastic.fr | French | EUR |
| `es` | www.lookfantastic.es | Spanish | EUR |
| `it` | www.lookfantastic.it | Italian | EUR |
| `nl` | www.lookfantastic.nl | Dutch | EUR |
| `pl` | www.lookfantastic.pl | Polish | PLN (default) or EUR |
| `at` | www.lookfantastic.at | German | EUR |
| `ie` | www.lookfantastic.ie | English | EUR |
| `eu` | eu.lookfantastic.com, the EU site | English | EUR (its own euro prices) |

- The site's host name works as `market` too (`lookfantastic.de`, `eu.lookfantastic.com`).
- Each currency on lookfantastic.com pairs with the shipping destination its own selector gives it (`USD` ships to `US`, `EUR` to `IE`, `JPY` to `JP`): `shipping_destination` in the answer says which.
- SKUs are the same on every site; prices, RRPs, ratings, review counts, offers and brand directories are each site's own (415 brands on lookfantastic.com, 177 on lookfantastic.de).
- `loyalty_points` was filled on lookfantastic.com (63 points on the 12.60 GBP Glow Tonic), lookfantastic.de and lookfantastic.nl (29 each), and `null` on the fr, es, it, at, ie, pl and eu sites in the captures.
- Show each price with its site and currency; never convert one into another.

## Prices, offers, variants and reviews

Every list item (search, list) carries:

| Field | Meaning |
|---|---|
| `price` | The site's price for a visitor without an account, in the currency asked |
| `rrp` | Lookfantastic's RRP on that site, as given |
| `discount_percent` | Computed by Scavio from `price` and `rrp`, only when the RRP is above the price; `null` otherwise |
| `price_from` | The lowest variant price when it is below `price` (PIXI Glow Tonic 250ml at 12.60 GBP read `price_from` 7, the 100ml); `null` otherwise |
| `in_stock` | The site's online availability, as given |
| `rating`, `review_count` | The site's figures for the product |
| `offer` | {`title`, `description`, `free_gift`, `url`}: the site's promotion text for the product, as given, in its language; dates only inside the text |
| `variants_count`, `options` | How many variants and which option types (`Size`, `Shade`) |

- **Offers per product:** a product's `offer` is the promotion the site shows on it. Captured 2026-11-26 on lookfantastic.com during Black Friday: CeraVe AM Facial Moisturising Lotion SPF50 52ml 11.90 GBP (RRP 17) "Save 30% + Extra 5% off | Use Code: EXTRA"; Estée Lauder Double Wear Longwear Matte Foundation 15ml Travel Size 15 GBP (RRP 20) "Save 25%"; Medik8 Travel Size Press & Glow Tonic 30ml 6.75 GBP (RRP 9) "Save 25%". On lookfantastic.de La Roche-Posay Toleriane Dermo Gesichtsreinigung 400 ml read 21.56 EUR (RRP 28.75) "-25% Rabatt", and The INKEY List's cleanser "20% + Doppelte +Punkte" (double points for the site's members, as the text states).
- **Offers page (`/offers`):** gifts with purchase and bundles with a threshold and an end time. Captured on lookfantastic.com: 7 offers, e.g. the Estée Lauder Holiday Blockbuster gift set "(Worth £454) for £92 when you spend £50 or more on the brand" ending 2026-12-31T23:59:00Z, a complimentary NARS palette at "£80 on the brand" ending 2026-11-30T23:59:00Z, Christmas crackers "2 for £40 or 3 for £60" ending 2027-01-31T23:59:00Z. lookfantastic.fr listed 1 offer; lookfantastic.de and lookfantastic.pl listed none at the capture (a `200` with `count` 0 and a note).
- **Variants (product):** `variants[]` {`sku`, `name`, `option_type`, `option`, `shade_colour`, `price`, `rrp`, `discount_percent`, `in_stock`, `availability_message`, `preorder`, `max_per_order`, `loyalty_points`, `barcode`}. Giorgio Armani Luminous Silk Foundation listed 33 shades in USD on lookfantastic.com (47.40 USD, RRP 67.70). The product's own fields are those of the SKU asked for.
- **Barcode (product):** `barcode` is the EAN-13 or UPC the site lists, as given; `null` when it lists none (sets and pre-release items). Use it to match the same product elsewhere where the other retailer returns a barcode.
- **Reviews (product):** `rating`, `review_count` and `recent_reviews` (10 latest, `text` may be `null`). Report the counts and stars; quote a review's text only as that reviewer's own words.

## Workflow

1. **Find products.** `/search` with `q` (keywords in the site's language, or a SKU), `market`, and optionally `currency`, `sort`, filters and `page_size`. Check `resolved_from`: when set, the results are the products of the page the site maps the keyword to. Each `items[].sku` is the input of `/product`.
2. **Read one product.** `/product` with `sku` (or `url`, an `items[].url` link): every variant with its own price, stock and barcode, the offer, reviews.
3. **Across sites.** The same `/product` call once per `market` (1 credit each). Put each price with its site, currency and RRP in one table, with the capture date.
4. **Across currencies.** On `gb`, the same call with `currency` (`USD`, `EUR`, `AUD` ...): the site's own price in that currency, not a conversion.
5. **Read the offers.** `/offers` for the current offers with `gift`, `threshold` and `ends`; send an offer's `list_path` to `/list` (`path`, same `market`) for the products it covers. Or `/brands` for a brand's `path`, then `/list`.
6. **Narrow a list.** `/search` or `/list` with `include_facets` `true` gives the site's filter options with counts; a facet's `filter` names the input it maps to (`brand`, `skin_type`, `concern`, `spf`, `key_ingredient`, `formulation`, `min_price / max_price`, `min_discount / max_discount`, `min_rating`), or `filters` for any other facet (send `{"facet": facets[].facet, "value": options[].value}`). Send `options[].value` exactly (`SPF 50+`, `Dry`).
7. **Compare retailers.** Read the same SKU on `cult-beauty-api`, or search the same brand and product on `space-nk-api`, `sephora-product-data` or `ulta-beauty-api`; keep a row only where the barcode matches, or brand, name and size all match, and show each price with its retailer and date.
8. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Every endpoint

| Parameter | Type | Default | Description |
|---|---|---|---|
| `market` | string | `gb` | The site: `gb`, `de`, `fr`, `es`, `it`, `nl`, `pl`, `at`, `ie` or `eu` (or its host name). Anything else is a `400`, not charged |
| `currency` | string | the site's own | One the site's selector offers: any of the 22 on `gb`, `PLN` or `EUR` on `pl`, `EUR` elsewhere. Anything else is a `400`, not charged |

### Search (`/search`) and list (`/list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required (search) | Keywords in the site's language, or a Lookfantastic SKU (up to 200 chars). A keyword the site maps to a page returns that page's products, with `resolved_from` |
| `path` | string | one of (list) | A list page path, as in its /c/ link: `/brands/cerave`, `/black-friday`, `/black-friday/extra`, `/health-beauty/face/skincare-products/moisturisers`. Paths come from `/categories`, `/brands` and `/offers` |
| `url` | string | one of (list) | A list page link, `https://www.lookfantastic.com/c/<page>/` (any of the 10 sites), instead of `path` |
| `page` | integer | 1 | Page; at most 10,000 positions (`page` x `page_size`) |
| `page_size` | integer | 40 (search), 60 (list) | 1-40 on search, 1-200 on list |
| `sort` | string | `relevance` | `relevance`, `popularity`, `price_low`, `price_high`, `name`, `newest`, `discount` (highest percent off first): the site's sort menu |
| `brand` | string or list | none | Brand as the site names it (`CeraVe`) |
| `skin_type` | string or list | none | `Dry`, `Oily`, `Sensitive` ... as the site lists it (in its language) |
| `concern` | string or list | none | `Anti-Ageing`, `Dry Skin`, `Breakouts & Blemishes` ... |
| `spf` | string or list | none | `SPF 30+`, `SPF 50+` ... |
| `key_ingredient` | string or list | none | `Retinol`, `Hyaluronic Acid`, `Niacinamide` ... |
| `formulation` | string or list | none | `Vegan`, `Fragrance Free`, `Dermatologist-Approved` ... |
| `filters` | list | none | Any other facet: up to 10 {`facet` (`facets[].facet`, e.g. `en_beauty_skinSubcategory_content`), `value` (one or a list of `options[].value`)} |
| `min_price`, `max_price` | number | none | Price range in the currency asked |
| `min_rating` | number | none | Lowest average stars (1-5); applied by the site's own filter, a few items can show a rating just below it |
| `min_discount`, `max_discount` | number | none | Percent off the site's RRP (0-100) |
| `include_facets` | boolean | false | Also return the site's filter counts. Still 1 credit |

A filter list takes up to 10 values. An editorial page without a product list is listed through its view-all page (`/black-friday` lists `/black-friday/view-all`; `listed_path` and a note say so).

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | one of | A Lookfantastic SKU (`items[].sku` or `variants[].sku`, `11200055`); the same on every site |
| `url` | string | one of | A product link, `https://www.lookfantastic.com/p/<name>/<sku>/`; the site still comes from `market` |

### Suggestions, offers, brands, categories

`/suggestions` takes `q` (the text typed so far, up to 100 chars). `/offers` and `/categories` take only `market` and `currency`. `/brands` takes an optional `letter` (`A`-`Z`, or `0-9`).

## Examples

### One product with its variants and offer

```bash
curl -X POST https://api.scavio.dev/api/v1/lookfantastic/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "11200055"}'
```

Captured `data` (2026-11-26; `recent_reviews` cut to 2 of 10, `subtitle`, `description`, `directions`, `ingredients`, `images`, `breadcrumbs` and `notes` dropped):

```json
{
  "market": { "market": "gb", "site": "www.lookfantastic.com", "language": "en", "currency": "GBP", "shipping_destination": "GB" },
  "requested_sku": "11200055",
  "sku": "11200055",
  "product_sku": "11200055",
  "name": "PIXI Glow Tonic 250ml (Worth £25.00)",
  "product_name": null,
  "brand": "PIXI",
  "url": "https://www.lookfantastic.com/p/pixi-glow-tonic-glycolic-acid-toner-250ml/11200055/",
  "price": 12.6,
  "rrp": 18,
  "discount_percent": 30,
  "currency": "GBP",
  "in_stock": true,
  "availability_message": "In stock | Usually dispatched within 24 hours",
  "barcode": "885190821006",
  "option_type": "Size",
  "option": "250ml",
  "variants": [
    { "sku": "11537217", "name": "PIXI Glow Tonic Glycolic Acid Toner 100ml", "option_type": "Size", "option": "100ml", "shade_colour": null, "price": 7, "rrp": 10, "discount_percent": 30, "in_stock": true, "availability_message": "In stock | Usually dispatched within 24 hours", "preorder": false, "max_per_order": null, "loyalty_points": 35, "barcode": "885190821020" },
    { "sku": "11200055", "name": "PIXI Glow Tonic 250ml (Worth £25.00)", "option_type": "Size", "option": "250ml", "shade_colour": null, "price": 12.6, "rrp": 18, "discount_percent": 30, "in_stock": true, "availability_message": "In stock | Usually dispatched within 24 hours", "preorder": false, "max_per_order": null, "loyalty_points": 63, "barcode": "885190821006" }
  ],
  "volume": null,
  "loyalty_points": 63,
  "max_per_order": null,
  "preorder": false,
  "offer": {
    "title": "Save 30% + Extra 5% off | Use Code: EXTRA",
    "description": "Today's Saving! Plus, enjoy an extra 5% off. Offer valid for a limited time only. Exclusions apply.",
    "free_gift": null,
    "url": "https://www.lookfantastic.com/c/black-friday/extra/v1/"
  },
  "rating": 4.7,
  "review_count": 724,
  "recent_reviews": [
    { "rating": 5, "date": "2026-11-20", "text": "Really makes your skin glow, use twice a day. Brilliant" },
    { "rating": 5, "date": "2026-10-21", "text": "I really like this toner and find it good value for money. I don’t think it’s out of this world but it does the job and is good money for the size!" }
  ]
}
```

The 30% is already in `price` (12.60 against 18). The extra 5% with code EXTRA is applied in the basket (12.60 x 0.95 = 11.97 GBP, computed, not checked out). An unknown SKU is a charged `404`.

### The same SKU on the French site

```bash
curl -X POST https://api.scavio.dev/api/v1/lookfantastic/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "11200055", "market": "fr"}'
```

Captured (2026-11-26): `market` {`market` `fr`, `site` `www.lookfantastic.fr`, `language` `fr`, `currency` `EUR`, `shipping_destination` `FR`}, `name` "Pixi Glow Tonic (250ml)", `price` 14.49, `rrp` 20.7, `discount_percent` 30, `barcode` `885190821006`, `availability_message` "Disponible | Expédié normalement sous 24h (jours ouvrables)", the 100ml variant at 8.05 EUR (RRP 11.50), `loyalty_points` `null`, `offer` "Économisez -30%" ("Économisez 30% sur votre commande. La réduction a été appliquée au prix de vente conseillé. Offre valable pour une durée limitée."), `rating` 4.91 from `review_count` 11, French description and directions.

The same call with `market` `es` read 16.56 EUR (20% off, "20% de descuento"), with `eu` 20.95 EUR and `discount_percent` `null`, with `pl` 66.15 PLN (RRP 94.50) and with `pl` plus `currency` `EUR` 14.49 EUR.

### Search on the German site

```bash
curl -X POST https://api.scavio.dev/api/v1/lookfantastic/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "gesichtsreinigung", "market": "de", "page_size": 10}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 10, `url`, `image` and `notes` dropped):

```json
{
  "market": { "market": "de", "site": "www.lookfantastic.de", "language": "de", "currency": "EUR", "shipping_destination": "DE" },
  "query": "gesichtsreinigung",
  "resolved_from": null,
  "corrected_query": null,
  "total": 79,
  "total_pages": 8,
  "page": 1,
  "page_size": 10,
  "has_more": true,
  "count": 10,
  "sort": "relevance",
  "filters_applied": {},
  "items": [
    { "position": 1, "sku": "12631146", "name": "La Roche-Posay Toleraine Dermo Gesichtsreinigung 400 ml", "brand": "La Roche-Posay", "price": 21.56, "rrp": 28.75, "discount_percent": 25, "price_from": null, "currency": "EUR", "in_stock": true, "rating": 4.7, "review_count": 705, "offer": { "title": "-25% Rabatt", "description": "Spare 25% auf deine Bestellung. Der Rabatt wurde auf den UVP angewendet. Das Angebot ist nur für eine begrenzte Zeit gültig.", "free_gift": null, "url": "https://www.lookfantastic.de/offers/pc-eu.list" }, "variants_count": 1, "options": ["Size"] },
    { "position": 2, "sku": "12916104", "name": "Kiehl's Ultra Gesichtsreinigung (Verschiedene Größen)", "brand": "Kiehl's Since 1851", "price": 13.8, "rrp": 17.25, "discount_percent": 20, "price_from": null, "currency": "EUR", "in_stock": true, "rating": 4.72, "review_count": 255, "offer": { "title": "-20% Rabatt", "description": "Spare 20% auf deine Bestellung. Der Rabatt wurde auf den UVP angewendet. Das Angebot ist nur für eine begrenzte Zeit gültig.", "free_gift": null, "url": "https://www.lookfantastic.de/offers/pc-eu.list" }, "variants_count": 2, "options": ["Size"] }
  ]
}
```

### A mapped keyword

```bash
curl -X POST https://api.scavio.dev/api/v1/lookfantastic/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "cerave", "currency": "USD"}'
```

Captured (2026-11-26): `resolved_from` {`type` `landing`, `path` `/brands/cerave`, `listed_path` `/brands/cerave/view-all`, `url` `https://www.lookfantastic.com/c/brands/cerave/`, `title` "CeraVe | LOOKFANTASTIC", `sku` `null`}, `total` 80, `market` {`currency` `USD`, `shipping_destination` `US`}; first CeraVe AM Facial Moisturising Lotion SPF50 for Normal to Dry Skin 52ml at 16.50 USD (RRP 23.50) "Save 30% + Extra 5% off | Use Code: EXTRA". The same product read 11.90 GBP (RRP 17) in GBP. On lookfantastic.ie, `face wash` resolved to the cleansers category (`type` `category`, `/health-beauty/face/cleansers`, 438 products).

### Offers with end times

```bash
curl -X POST https://api.scavio.dev/api/v1/lookfantastic/offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (2026-11-26; `offers` cut to 3 of 7, `notes` dropped):

```json
{
  "market": { "market": "gb", "site": "www.lookfantastic.com", "language": "en", "currency": "GBP", "shipping_destination": "GB" },
  "count": 7,
  "offers": [
    {
      "title": "Receive the Estée Lauder Holiday Blockbuster 8 Full-Sizes + More Gift Set (Worth £454) for £92 when you spend £50 or more on the brand",
      "description": "Receive the Estée Lauder Holiday Blockbuster 8 Full-Sizes + More Gift Set (Worth £454) for £92 when you spend £50 or more on the brand. Add the Estée Lauder Holiday Blockbuster 8 Full-Sizes + More Gift Set to basket. Offer valid for a limited time only, while stocks last. Exclusions apply.",
      "code": null,
      "gift": "the Estée Lauder Holiday Blockbuster 8 Full-Sizes + More Gift Set (Worth £454) for £92",
      "threshold": "£50 or more on the brand",
      "ends": "2026-12-31T23:59:00.000Z",
      "url": "https://www.lookfantastic.com/c/brands/estee-lauder/all/",
      "list_path": "/brands/estee-lauder/all"
    },
    {
      "title": "Receive a complimentary NARS Afterglow Tempting Eyeshadow Palette Lavender Haze when you spend £80 on the brand (after discount)",
      "description": "Receive a complimentary NARS Afterglow Tempting Eyeshadow Palette Lavender Haze when you spend £80 on the brand (after discount). Complimentary gift will be awarded at basket. Offer valid for a limited time only, while stocks last.",
      "code": null,
      "gift": "NARS Afterglow Tempting Eyeshadow Palette Lavender Haze",
      "threshold": "£80 on the brand",
      "ends": "2026-11-30T23:59:00.000Z",
      "url": "https://www.lookfantastic.com/c/brands/nars/view-all/",
      "list_path": "/brands/nars/view-all"
    },
    {
      "title": "Buy More, Save More on Crackers*",
      "description": "Buy more save more - Buy 2 Christmas Crackers for £40 or 3 Christmas Crackers for £60. *Offer applies to The LOOKFANTASTIC Christmas Cracker Collection.",
      "code": null,
      "gift": null,
      "threshold": null,
      "ends": "2027-01-31T23:59:00.000Z",
      "url": "https://www.lookfantastic.com/c/offers/beauty-box/lookfantastic-christmas-collection/crackers/",
      "list_path": "/offers/beauty-box/lookfantastic-christmas-collection/crackers"
    }
  ]
}
```

`code`, `gift` and `threshold` are read from the offer text when it states them (`null` otherwise). `ends` is the site's end time; there is no start date. `list_path` is `null` when the offer links a single product (the Lancôme Beauty Box offer); otherwise send it to `/list`.

### List, suggestions, brands, categories

- `/list` `{"path": "/brands/cerave", "include_facets": true, "page_size": 10}`: listed through `/brands/cerave/view-all` (with a note), `total` 80, `total_pages` 8; first CeraVe AM Facial Moisturising Lotion SPF50 52ml at 11.90 GBP (RRP 17), then the Moisturising Cream Pot 454g at 12.25 GBP with `price_from` 8.40. `facets` included Skin Type (`skin_type`: Dry 26), Skincare Concern (`concern`: Dry Skin 51), Suncare SPF (`spf`: SPF 30+ 7, SPF 50+ 5), Key Ingredients (`key_ingredient`), Formulation (`formulation`: Dermatologist-Approved 73), Price (`lfint_GBP_price`, `min_price / max_price`), Savings (`min_discount / max_discount`: 25% - 50% 78), Average Reviews (`min_rating`: 4+ 60), and Skincare Product Type (`en_beauty_skinSubcategory_content`: Moisturisers 32) with `filter` `filters`: send it through `filters`.
- `/list` `{"path": "/black-friday", "page_size": 10}`: `listed_path` `/black-friday/view-all`, `total` 13,665; first Estée Lauder Double Wear Longwear Matte Foundation SPF 10 15ml Travel Size at 15 GBP (RRP 20, 29 shades), La Roche-Posay Cicaplast Balm B5 100ml at 14.93 GBP (RRP 19.90), Silk'n Facial LED Mask 100 LEDS at 82.17 GBP (RRP 160, 49% computed). `/black-friday/extra` listed the 10,608 products carrying the extra code.
- `/suggestions` `{"q": "cerave"}`: `terms` "cerave", "cerave hydrating", "cerave invisible", "cerave blemish", "cerave moisturising"; 5 `products`, first CeraVe PM Facial Moisturising Lotion 52ml at 11.90 GBP (RRP 17).
- `/brands` `{}`: `total_brands` 415, each {`name`, `path`, `url`, `letter`} (`111SKIN` under `0-9`, `/brands/111skin`).
- `/categories` `{}`: 13 menus (Black Friday `/black-friday`, Christmas, Beauty Box, Brands, New In, Makeup `/health-beauty/make-up`, Hair, Skincare `/health-beauty/face`, Fragrance, Men's, Body, Luxury, Korean Beauty), `total_categories` 574. lookfantastic.de: 12 menus in German (Weihnachten, Marken, Hautpflege ...), 324 nodes. Seasonal menus change.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def lookfantastic(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/lookfantastic/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. One SKU on every site (1 credit each)
for market in ["gb", "ie", "de", "fr", "es", "it", "nl", "at", "pl", "eu"]:
    p = lookfantastic("product", {"sku": "11200055", "market": market})["data"]
    offer = (p["offer"] or {}).get("title")
    print(market, p["price"], p["rrp"], p["currency"], p["discount_percent"], p["rating"], p["review_count"], offer)

# 2. lookfantastic.com in another currency (1 credit)
usd = lookfantastic("product", {"sku": "11200055", "currency": "USD"})["data"]
print(usd["market"]["shipping_destination"], usd["price"], usd["currency"])

# 3. Current offers with end times (1 credit)
for o in lookfantastic("offers", {})["data"]["offers"]:
    print(o["title"][:80], o["threshold"], o["ends"], o["list_path"])

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

- Name it "Lookfantastic (lookfantastic.com, the beauty retailer with 10 country sites)" on first mention, "Lookfantastic" after that, and name the site for every price ("lookfantastic.de").
- Prices: quote `price` with its currency, the site and the `fetched_at` date ("listed on lookfantastic.fr on Nov 26, 2026"). `rrp` is "Lookfantastic's RRP, as the site gives it"; `discount_percent` is "computed by Scavio from the site's price and RRP". A code price is your own arithmetic: label it computed and not checked out.
- Sites and currencies: every price belongs to one site and one currency. Never convert, average or rank sites into one "Lookfantastic price"; show each one as read.
- Offers: quote code, rate, gift, gift value and threshold exactly as the site writes them, in its language, with `ends` and the capture date. No countdowns, urgency or "real deal" / "fake discount" language. A points offer ("Doppelte +Punkte") is points, as the site states it, never a percent off.
- Comparisons: same product and size only (barcode where both sides return it, else brand + name + size), each price with its retailer, site, currency and date; show the numbers and their difference only. Never call a retailer, a site or a price the cheapest, a deal, a bargain or a rip-off.
- Descriptive only: never say a product or seller is authentic, genuine, counterfeit, authorized or unauthorized, never give a legit or scam verdict on any retailer, and never make MAP claims or comment on Lookfantastic's pricing practices.
- No efficacy, SPF or medical claims. Report SPF bands, concerns and ingredients as the site labels them; quote review text only as that reviewer's own words.
- Reviews: counts, stars, dates and text as returned; no reviewer names are returned, never try to identify reviewers. Do not republish Lookfantastic product photos or descriptions at length; cite products by name, SKU and site instead.
- Names: use "Lookfantastic" only for the 10 sites in the Markets table; never treat lookalike domains or similarly named sites as Lookfantastic.
- Terms: Scavio does not collect or store Lookfantastic data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Lookfantastic's terms and conditions cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, RRPs, offers, codes, end dates, SKUs, barcodes or reviews. Only return what the API returned, with the `fetched_at` time and the product `url`.
- Not available: a full review feed or review paging (only the 10 latest via product), Q&A, store pages or store stock, member prices, basket or checkout prices, code-applied prices, price history (store your own), offer start dates.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `market` that is not one of the 10 sites; a `currency` the site does not offer ("currency PLN is not offered on www.lookfantastic.com (market gb): send one of GBP, USD, EUR ..."); search without `q`; list without `path` or `url`, or with both, a path that is not a list page (a product, search or account page), a link that is not a /c/ page of a Lookfantastic site; product without `sku` or `url`, or with both, a SKU that is not 5-10 digits, a link that is not a /p/ product link; `page` past 10,000 positions; `page_size` above 40 on search or 200 on list; an unknown `sort`; `min_price` above `max_price`; `min_discount` above `max_discount`; a range facet sent through `filters` (use `min_price` / `max_price`, `min_discount` / `max_discount` or `min_rating`); more than 10 values in a filter list or 10 `filters`; a `letter` that is not A-Z or 0-9.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Lookfantastic has no product with SKU <sku> on <site>.", "Lookfantastic has no list page at <path> on <site>.", "Lookfantastic's page <path> on <site> has no product list.". Take SKUs and paths from a previous answer, on the same site, rather than guessing them. A search with no matches is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api).
- `502` means Lookfantastic data was temporarily unavailable ("Lookfantastic is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Lookfantastic is busy ("Lookfantastic is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
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
const { data: hits } = await scavio.lookfantastic.search({ q: "gesichtsreinigung", market: "de" });
const { data: brand } = await scavio.lookfantastic.list({ path: "/brands/cerave", sort: "price_low" });
const { data: product } = await scavio.lookfantastic.product({ sku: "11200055", market: "fr" });
const { data: offers } = await scavio.lookfantastic.offers();
const { data: brands } = await scavio.lookfantastic.brands({ letter: "C" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.lookfantastic.search(...)`, `list`, `product`, `suggestions`, `offers`, `brands` and `categories`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 7 endpoints as tools: `search_lookfantastic`, `get_lookfantastic_list`, `get_lookfantastic_product`, `get_lookfantastic_suggestions`, `get_lookfantastic_offers`, `get_lookfantastic_brands` and `get_lookfantastic_categories`. Lookfantastic is opt-in: add `lookfantastic` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,lookfantastic"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/lookfantastic-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api), [list](https://scavio.dev/docs/lookfantastic-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api), [product](https://scavio.dev/docs/lookfantastic-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api), [suggestions](https://scavio.dev/docs/lookfantastic-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api), [offers](https://scavio.dev/docs/lookfantastic-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api), [brands](https://scavio.dev/docs/lookfantastic-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api), [categories](https://scavio.dev/docs/lookfantastic-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api). Overview: [Lookfantastic API](https://scavio.dev/lookfantastic-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lookfantastic-api).
