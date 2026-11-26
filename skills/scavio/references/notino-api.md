# Notino API - Perfume Prices, 30-Day Low, 27 Storefronts

Read Notino (notino.com, the Brno-based online perfume and cosmetics store with 27 country shops across Europe) on any of its 27 storefronts: keyword search, any category, any brand, promo lists such as Black Friday, one product in full with every size or shade, customer reviews, search suggestions, the brand directory, and Notino's stores and pickup points with their hours. Every answer is the storefront's public page as a visitor without an account sees it, in that storefront's language and currency. All 10 endpoints return structured JSON, 1 credit per call on most.

**Read-only data.** This skill reads the public pages Notino shows to any visitor and returns them as JSON for analysis. It uses no Notino account, no loyalty login, no cart and no checkout.

**The job this skill is for: one perfume or cosmetic priced across Notino's storefronts, next to Notino's own 30-day low.** Every storefront has its own prices, also inside the euro zone, and EU price rules have Notino show the lowest price of the last 30 days beside each variant (`lowest_price_30d`). Captured 2026-11-26 with `/product` (one call per storefront, 1 credit each, 2 on notino.co.uk), DIOR Sauvage Eau de Parfum 200 ml (order code `CHD13588`, EAN `3348901428545`):

| Storefront (`market`) | Currency | `price` | `lowest_price_30d` | `stock_level` | `pickup_store_count` |
|---|---|---|---|---|---|
| notino.de (`de`) | EUR | 180 | 170 | more_than_20 | 0 |
| notino.at (`at`) | EUR | 204 | 170 | more_than_20 | 0 |
| notino.fr (`fr`) | EUR | 198 | 174.2 | more_than_20 | 0 |
| notino.it (`it`) | EUR | 200 | 177.2 | more_than_20 | 0 |
| notino.be (`be`) | EUR | 221 | 185 | more_than_20 | 0 |
| notino.nl (`nl`) | EUR | 226 | 202 | more_than_20 | 0 |
| notino.sk (`sk`) | EUR | 219 | 185.3 | more_than_20 | 0 |
| notino.gr (`gr`) | EUR | 249 | 225 | more_than_5 | 0 |
| notino.si (`si`) | EUR | 255 | 189 | more_than_20 | 0 |
| notino.hr (`hr`) | EUR | 255.6 | 240 | more_than_20 | 0 |
| notino.bg (`bg`) | EUR | 179 | 170 | more_than_5 | 0 |
| notino.ch (`ch`) | CHF | 190 | 168.6 | more_than_20 | 0 |
| notino.co.uk (`gb`) | GBP | 217.6 | 183 | more_than_20 | 0 |
| notino.cz (`cz`) | CZK | 5100 | 4350 | more_than_20 | 3 |
| notino.pl (`pl`) | PLN | 805 | 805 | more_than_20 | 3 |
| notino.hu (`hu`) | HUF | 92500 | 76900 | more_than_20 | 1 |
| notino.ro (`ro`) | RON | 1190 | 1050 | more_than_5 | 1 |
| notino.ua (`ua`) | UAH | 7200 | 7200 | more_than_20 | 0 |

The same order code and EAN on every storefront; the euro-zone storefronts captured ran from 179 (bg) to 255.6 (hr) EUR for the same bottle on the same day. Quote each price with its storefront, never one storefront's price as Notino's price.

Ten limits shape every answer, so say them plainly:
- **Credits depend on the storefront and the list.** 1 credit per call, 2 on notino.co.uk (`gb`). A category, brand or promo list beyond page 1, sorted or filtered is 3 credits (4 on `gb`): Notino's page 1 is read for the list's own ids, then the wanted page, both billed. Search is 1 (2 on `gb`) with any page, sort or filter, except when Notino answers the term with a brand or category page that drops them: then that page is read with them, 3 (4 on `gb`). Reviews: 1 credit (2 on `gb` for the newest 8; by `order_code` 1, 4 on `gb`). `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are per storefront.** `market` (default `de`) picks the storefront, its language and currency (EUR, GBP, CZK, HUF, PLN, RON, UAH, DKK, SEK, CHF). A product or listing link picks its own storefront; a link from one storefront with another `market` is a `400` ("prices, ids and links differ per storefront").
- **30-day low and RRP as Notino shows them.** `lowest_price_30d` is the lowest price of the last 30 days Notino shows under EU price rules, per variant. `rrp` is the recommended retail price only where the storefront shows one (`rrp_type` `recommended` on notino.es); it is `null` elsewhere, and listings rarely carry one. A percent off is your own computation from the two figures shown: label it computed.
- **Voucher codes are on listings.** Search, category, brand and promo items carry `deal` {`voucher_code`, `discount_percent`, `discounted_price` ...}: Notino's code and the price with it as Notino shows it (Garnier Vitamin C Serum 11.9 EUR, code `black` 20% off, `discounted_price` 9.52 on notino.de). The product page carries no code. A promo list's `terms` give the code's dates as Notino writes them.
- **Search redirects.** Notino sends brand names and some category words to a brand or category page: `redirected_to` {`page_type`, `path`, `url`} says so and the list is that page's (`dior` on notino.de went to the DIOR brand page, 218 products). Check `redirected_to` before calling an answer "search results".
- **Relevance stops near 500.** Sorted by relevance Notino stops a search list near 500 products (`total_capped` true); any other sort lists the full set.
- **Sponsored items stay in place.** `sponsored` true marks a paid placement Notino mixes into the list; it is kept where Notino puts it. Flag it rather than counting it as a ranking.
- **Stock is a word, not a count.** `stock_level` is Notino's stock word (`more_than_20`, `more_than_5`, `less_than_5`, `last_1` ... `last_5`, `out_of_stock`). `pickup_store_count` is how many Notino stores hold the variant; per-store stock is not offered.
- **Stores in 8 markets.** `/stores` and `/store` answer for `cz` (default), `sk`, `pl`, `at`, `hu`, `ro`, `bg`, `hr`: stores and pickup points by city (`city` filter, accents and case ignored), with opening hours. There is no postcode search. Other storefronts are a `400`.
- **What is not there.** No per-store stock, no postcode store search, no member, loyalty or cart prices, no price history (store your own answers with `fetched_at`; `lowest_price_30d` is Notino's own figure), no reviewer names or identity, no cart or checkout.

Notino publishes no public API for its catalogue, prices or reviews. Its Creator and Affiliate Program runs through the CJ affiliate network for approved publishers; this skill reads Notino's public pages with one Scavio key and needs no affiliate approval. Other vendors offer Notino data tools; this skill reads Notino's own public pages.

Notino was founded in 2004 in Brno, Czech Republic, and its about page states 115,000 unique products from 1,800 brands and shops in 27 countries (notino.ie about page, read Nov 26, 2026). Quote company figures with their source, never from the samples.

See also: for the same product at other retailers use `douglas-beauty-api` (Douglas, 15 European markets), `lookfantastic-api` (Lookfantastic), `sephora-product-data` (Sephora), `ulta-beauty-api` (Ulta Beauty), `amazon-product-data` (Amazon) and `allegro-api` (Allegro, Poland). Same product and size only: match on EAN where both sides return one (Notino returns `ean` per variant), otherwise brand + product name + size in both titles, each price with its seller, storefront and date.

## When to trigger

Use this skill when the user asks to:
- Price one perfume or cosmetic (by link or order code) on several Notino storefronts, each in its own currency
- Read a Notino product's price, 30-day low, RRP, EAN, order code, stock level, gift campaigns and delivery dates for every size or shade
- Find the storefronts that sell a product (`alternate_sites`) and compare them
- Search Notino by keyword, or list a category or a brand, sorted by bestseller, price, rating or newest, filtered by Notino's facets (brand, type of goods, skin type, gender, offers, free delivery, new, rating)
- List Notino's Black Friday or another promo page with its terms and each item's voucher code and discounted price
- Read Notino customer reviews of a product, sorted or filtered by stars, with counts per storefront and translations
- List Notino's brands, its search suggestions, or its stores and pickup points with opening hours in Czechia, Slovakia, Poland, Austria, Hungary, Romania, Bulgaria or Croatia

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit, so 50 credits price one product on 27 storefronts with credits to spare.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1-3 seconds, product 1-7 (notino.bg 20, notino.co.uk 26), search 2-10 (notino.co.uk 24), brands 2-5, stores 2-4, store 4-6, the newest reviews 1-6, a paged or sorted list 14-48, and deeper review pages 10-41. Deeper review views can take up to about 4 minutes: set a client timeout of at least 250 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/notino/search` | Products for search text: price, unit price, stock level, rating, deal (voucher code, discounted price), sponsored flag, variants; total, pages, facets, price range; `redirected_to` | 1 (2 on gb); 3 (4 on gb) when redirected with page, sort or filters |
| `POST /api/v1/notino/product` | One product by link or order code with every variant: price, 30-day low, RRP, EAN, order code, stock, store count, gift campaigns, deliveries, other storefronts | 1 (2 on gb) |
| `POST /api/v1/notino/reviews` | Reviews of one product, 8 a page, with rating buckets, counts per storefront, translations | 1 (2 on gb for the newest 8) |
| `POST /api/v1/notino/category` | One category by path, with page, sort and filters | 1 (2 on gb); paged, sorted or filtered 3 (4 on gb) |
| `POST /api/v1/notino/brand` | One brand's products, with page, sort and filters | 1 (2 on gb); paged, sorted or filtered 3 (4 on gb) |
| `POST /api/v1/notino/promo` | A promo list (default Black Friday) with the banner's terms; every item with its deal | 1 (2 on gb); paged, sorted or filtered 3 (4 on gb) |
| `POST /api/v1/notino/brands` | The storefront's brand directory: name, slug, featured, letter | 1 (2 on gb) |
| `POST /api/v1/notino/suggestions` | Notino's suggestions for a partial query: collections, brands, products | 1 (2 on gb) |
| `POST /api/v1/notino/stores` | Notino stores and pickup points in one of 8 markets, by city, with hours and coordinates | 1 |
| `POST /api/v1/notino/store` | One store: services, 7 days of opening hours from today, address, phone, email | 1 |

## Markets

| Code | Storefront | Language | Currency | Stores |
|---|---|---|---|---|
| `de` (default) | notino.de | de-DE | EUR | |
| `at` | notino.at | de-AT | EUR | yes |
| `ch` | notino.ch | de-CH (German) | CHF | |
| `cz` | notino.cz | cs-CZ | CZK | yes (stores default) |
| `sk` | notino.sk | sk-SK | EUR | yes |
| `pl` | notino.pl | pl-PL | PLN | yes |
| `hu` | notino.hu | hu-HU | HUF | yes |
| `ro` | notino.ro | ro-RO | RON | yes |
| `bg` | notino.bg | bg-BG | EUR | yes |
| `hr` | notino.hr | hr-HR | EUR | yes |
| `si` | notino.si | sl-SI | EUR | |
| `ua` | notino.ua | uk-UA | UAH | |
| `fr` | notino.fr | fr-FR | EUR | |
| `be` | notino.be | fr-BE (French) | EUR | |
| `nl` | notino.nl | nl-NL | EUR | |
| `it` | notino.it | it-IT | EUR | |
| `es` | notino.es | es-ES | EUR | |
| `pt` | notino.pt | pt-PT | EUR | |
| `gr` | notino.gr | el-GR | EUR | |
| `gb` (`uk`) | notino.co.uk | en-GB | GBP | (2 credits per call) |
| `ie` | notino.ie | en-IE | EUR | |
| `dk` | notino.dk | da-DK | DKK | |
| `se` | notino.se | sv-SE | SEK | |
| `fi` | notino.fi | fi-FI | EUR | |
| `lt` | notino.lt | lt-LT | EUR | |
| `lv` | notino.lv | lv-LV | EUR | |
| `ee` | notino.ee | et-EE | EUR | |

Every answer carries `market`, `shop`, `language` and `currency`. Names, labels and review texts are in the storefront's language as Notino writes them (a 200 ml label reads "200 мл" on notino.ua); field names are English.

## Prices and variant fields

| Field | Meaning |
|---|---|
| `price`, `currency` | The variant's price on the storefront, with VAT (`vat_percent`) |
| `lowest_price_30d` | The lowest price of the last 30 days Notino shows beside the variant |
| `rrp`, `rrp_type` | The recommended retail price where the storefront shows one (`recommended`); `null` elsewhere |
| `anchor_price` | A reference price Notino shows, as given (`null` when none) |
| `unit_price` | {`value`, `unit`, `per_amount`}: 900 per 1 l for 180 EUR for 200 ml |
| `order_code`, `product_code`, `ean` | Notino's order code (the input of `order_code`), its product code and the EAN |
| `availability` | {`state` (`CanBeBought`, `ShowWatchdog`), `can_buy`, `stock_level`, `in_stock`, `max_order_quantity`, `pickup_store_count`} |
| `deal` (lists) | {`reason` (`on_sale`, `clearance`), `voucher_code`, `discount_value`, `discount_type`, `discount_percent`, `discounted_price`, `voucher_not_for_cheapest`, `basket_condition`, `free_delivery`, `tags`, `campaign_ids`} or `null` |
| `gift_campaigns` (product) | {`campaign_id`, `type` (`special`, `try_it_first`), `text` (as Notino words it, e.g. a basket threshold), `image`, `variant_ids`} |

- **Ids:** `variant_id` is one size or shade (`/p-<variant id>/` links pick it); `order_code` (`CHD13588`) is the same across storefronts in the captures; `master_id` and `catalog_master_id` group the product.
- **Code prices:** `discounted_price` is Notino's own figure on a listing. A code price you work out yourself (a basket condition, a cart total) is computed: label it so, never "checked out".

## Workflow

1. **Find the product.** `/search` with `query` and `market`, `/brand` with a slug from `/brands` (`dior`, `cerave`), or `/category` with a path (`/hautseren/`). Note the item `url` and `product_code`.
2. **Read it in full.** `/product` with the `url` (or an `order_code` from `variants[]` and a `market`). Read each variant's `label`, `price`, `lowest_price_30d`, `rrp`, `ean`, `order_code` and `availability`.
3. **Other storefronts.** `alternate_sites[]` lists the same product's link on the other storefronts: call `/product` with each `url` (1 credit each, 2 on notino.co.uk). Match the variant on `ean` or `order_code`.
4. **Voucher codes.** `/promo` (default Black Friday) or the listing the product sits in: `items[].deal` gives the code and `discounted_price`; `terms` give the dates as Notino writes them.
5. **Reviews.** `/reviews` with the product `url`; page 1 newest is the quick view, other pages, sorts and star filters are slower.
6. **Report.** Each price with its storefront, currency and `fetched_at` date, the 30-day low beside it, an RRP only where the storefront shows one, a percent off labelled computed.
7. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`) and promo (`/promo`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required (search) | Search text, up to 200 chars (the storefront's own language matches best) |
| `category` | string | required (category) | A category path (`/hautseren/`, from `breadcrumbs[].url` or Category facets) or its link |
| `brand` | string | required (brand) | A brand slug (`brands[].slug`: `dior`, `cerave`) or its link |
| `promo` | string | `black-friday` | Promo only: a promo page path or link |
| `market` | string | `de` | One of the 27 storefronts (a link picks its own) |
| `page` | integer | 1 | Page of 24, 1 to 500; `total_pages` says how deep a list goes |
| `sort` | string | `relevance` | `relevance`, `bestseller`, `price_asc`, `price_desc`, `top_rated`, `newest` |
| `filters` | list | none | Up to 10 filter ids from `facets[].values[].id` (`[100004]` offers); ids of one group widen, of different groups narrow, as on the site |

### Product (`/product`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | A Notino product link or path (`/<brand>/<product>/`, or `/<brand>/<product>/p-<variant id>/` for one size or shade) |
| `order_code` | string | one of | A Notino order code (`variants[].order_code`, e.g. `CHD7138`) |
| `market` | string | `de` | The storefront for an order code or a path |
| `sort` | string | `newest` | Reviews only: `newest`, `oldest`, `highest_rating`, `lowest_rating`, `most_helpful` |
| `rating` | integer | none | Reviews only: 1-5 stars |
| `page` | integer | 1 | Reviews only: page of 8, 1 to 8 per view |

### Brands, suggestions, stores, store

| Endpoint | Parameters |
|---|---|
| `/brands` | `market`; `query` (name contains), `letter` (one letter or digit), `featured_only` (the brands the directory highlights), `page`, `limit` 1-500 (default 500) |
| `/suggestions` | `query` (what the shopper typed), `market` |
| `/stores` | `market` (`cz` default, `sk`, `pl`, `at`, `hu`, `ro`, `bg`, `hr`), `city` |
| `/store` | `store` (`stores[].store`, e.g. `florentinum-praha`, or the store's link), `market` |

## Examples

### One product with every size

```bash
curl -X POST https://api.scavio.dev/api/v1/notino/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/p-15676582/"}'
```

Captured `data` (2026-11-26; `sub_name`, `url`, `description`, `fragrance_notes`, `breadcrumbs`, `gift_campaigns`, `related_product_ids` and `reviews_url` dropped, `deliveries` cut to 1 of 2, `alternate_sites` to 2, `variants` to 1 of 4 with `url`, `colors`, `images`, `characteristics`, text fields and `gift_campaign_ids` dropped):

```json
{
  "market": "de",
  "shop": "notino.de",
  "language": "de-DE",
  "currency": "EUR",
  "requested": "15676582",
  "selected_variant_id": 15676582,
  "master_id": 15676518,
  "catalog_master_id": 361339,
  "master_product_code": "CHDSVGM_AEDP10",
  "name": "Sauvage",
  "brand": {"brand_id": 150, "name": "DIOR", "url": "https://www.notino.de/dior/", "manufacturer": "LVMH"},
  "annotation": "Eau de Parfum nachfüllbar für Herren",
  "collection": "Sauvage",
  "gender": "man",
  "is_perfume": true,
  "category": {"kind": "Fragrances", "category": "Perfumes", "subcategory": "Men’s perfumes", "type": "Eaux de Parfum"},
  "rating": {"average": 4.8, "count": 77, "text_reviews": 54, "translated_reviews": 0},
  "variant_count": 4,
  "variants": [
    {"variant_id": 15971107, "catalog_id": 763862, "name": "Sauvage", "variant_name": "Eau de Parfum für Herren", "label": "200 ml", "order_code": "CHD13588", "product_code": "CHDSVGM_AEDP25", "ean": "3348901428545", "price": 180, "currency": "EUR", "vat_percent": 19, "rrp": null, "rrp_type": null, "anchor_price": null, "lowest_price_30d": 170, "unit_price": {"value": 900, "unit": "l", "per_amount": 1}, "amount": {"value": 200, "unit": "ml"}, "availability": {"state": "CanBeBought", "can_buy": true, "stock_level": "more_than_20", "in_stock": true, "max_order_quantity": 3, "pickup_store_count": 0}}
  ],
  "deliveries": [{"name": "DHL", "type": "transport", "price": 3.9, "free_shipping": true, "date": "2026-12-01", "date_from": null, "date_to": null, "order_by_time": "18:00:00"}],
  "alternate_sites": [{"market": "bg", "locale": "bg-BG", "url": "https://www.notino.bg/dior/sauvage-parfjumna-voda-za-mzhe/"}, {"market": "cz", "locale": "cs-CZ", "url": "https://www.notino.cz/dior/sauvage-parfemovana-voda-pro-muze/"}]
}
```

The 4 variants read 200 ml 180 (30-day low 170), 100 ml 120 (115.2), 60 ml 85.5 (82.5) and 30 ml 72.5 (69.5) EUR. A `special` gift campaign read "Sie erhalten ein Geschenk zur Bestellung dieser Marke über 125 €. Gültig solange der Vorrat reicht." (a gift with an order of the brand over 125 EUR, while stocks last). On notino.es, `{"url": "https://www.notino.es/estee-lauder/advanced-night-repair-synchronized-multi-recovery-complex-serum-de-noche-antiarrugas/"}` read 75 ml at 134 EUR with `rrp` 179 (`rrp_type` recommended) and a 30-day low of 134.

### Search with voucher deals

```bash
curl -X POST https://api.scavio.dev/api/v1/notino/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "vitamin c serum", "market": "de"}'
```

Captured `data` (2026-11-26; `items` cut to 1 of 24, `url`, `image` and `facets` dropped):

```json
{
  "market": "de",
  "shop": "notino.de",
  "language": "de-DE",
  "currency": "EUR",
  "query": "vitamin c serum",
  "redirected_to": null,
  "page_type": "Category",
  "title": "Suchergebnisse",
  "sort": "relevance",
  "page": 1,
  "page_size": 24,
  "total": 499,
  "total_pages": 21,
  "has_more": true,
  "count": 24,
  "items": [
    {"product_id": 16281126, "master_id": 16103488, "name": "Vitamin C Serum", "sub_name": null, "brand": "Garnier", "annotation": "Aufhellendes Serum mit Vitamin C", "price": 11.9, "currency": "EUR", "rrp": null, "unit_price": {"value": 396.67, "unit": "l", "per_amount": 1}, "stock_level": "more_than_20", "in_stock": true, "product_code": "GARSKNW_KFSR01", "master_product_code": "GARSUPW_KSER01", "rating": 4.7, "review_count": 30, "is_new": false, "sponsored": false, "free_delivery": false, "deal": {"reason": null, "voucher_code": "black", "discount_value": 20, "discount_type": "relative", "discount_percent": 20, "discounted_price": 9.52, "basket_condition": null, "free_delivery": false, "voucher_not_for_cheapest": false, "tags": ["blackfriday"], "campaign_ids": [69465, 75873]}, "variant_count": 2, "variants": [{"variant_id": 16277945, "label": "30 ml", "colors": []}, {"variant_id": 16281126, "label": "30 ml", "colors": []}], "category": {"category": "Skin", "subcategory": "Skin Care", "type": "Skin Serums", "kind": "Cosmetics and other needs"}}
  ],
  "price_range": {"min": 0.9, "max": 347},
  "selected_filters": [],
  "total_capped": true,
  "note": "Sorted by relevance Notino stops the list near 500 products; any other sort lists the full set."
}
```

`{"query": "dior", "market": "de", "page": 2}` was answered with the DIOR brand page (`redirected_to` {`page_type` Brand, `path` /dior/}), 218 products over 10 pages, for 3 credits.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/notino/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "/dior/sauvage-eau-de-parfum-fuer-herren/", "market": "de"}'
```

Captured `data` (2026-11-26; `reviews` cut to 1 of 8, `shops` to 1 of 3, `variants` to 1 of 4):

```json
{
  "market": "de",
  "shop": "notino.de",
  "language": "de-DE",
  "currency": "EUR",
  "sort": "newest",
  "rating": null,
  "page": 1,
  "page_size": 8,
  "master_product_id": "361339",
  "average_rating": 4.8,
  "rating_count": 77,
  "total": 54,
  "total_pages": 7,
  "has_more": true,
  "count": 8,
  "reviews": [
    {"review_id": 5110105, "rating": 5, "title": "Super", "text": "Parfüm war eine Geschenk", "created_at": "2026-11-15T11:38:01.2549793Z", "likes": 0, "dislikes": 0, "verified_purchase": true, "author_type": "verified", "variant_id": 6870556, "from_shop": null, "translated": false, "source_language": null, "original_title": null, "original_text": null, "partner_domain": null, "image_count": 0}
  ],
  "rating_buckets": {"1": 1, "2": 0, "3": 2, "4": 2, "5": 49},
  "content_counts": {"verified": 10, "with_images": 0},
  "shops": [{"shop": "notino.de", "market": "de", "count": 25}],
  "variants": [{"variant_catalog_id": 361339, "count": 2}],
  "aspects": null
}
```

Page 2 of the same product took 25 seconds; `"sort": "lowest_rating"` on a Clinique mascara 31 seconds and `"rating": 3` on Sauvage 41 seconds, 1 credit each. On deeper views `average_rating` and `rating_count` can be `null` while `rating_buckets` stay filled.

### Promo, category, brand, brands, suggestions, stores, store

- `/promo` `{"market": "de"}`: Black Friday, `total` 12000 over 500 pages, `terms` "Der Rabatt gilt vom 23.11. bis zum 29.11.2026 für mit dem Code black gekennzeichnete Produkte. ..." (the discount applies Nov 23 to Nov 29, 2026 to products marked with the code black); first Afnan Supremacy Collector's Edition 100 ml at 48 with `deal` code black, 20%, `discounted_price` 38.4. `{"market": "cz", "page": 2, "sort": "bestseller"}` cost 3 credits.
- `/category` `{"category": "/hautseren/", "market": "de"}`: 2,549 products over 107 pages; first The Ordinary Niacinamide 10% + Zinc 1% at 4.8. `{"category": "hautseren", "market": "de", "page": 3, "sort": "price_asc"}` cost 3 credits.
- `/brand` `{"brand": "cerave", "market": "de"}`: 44 products; first CeraVe Skin Renewing Peptide Cream at 27.9 with code black. On `gb`: 71 products, 2 credits.
- `/brands` `{"market": "de", "query": "dior"}`: `total_brands` 1765, 1 match {`name` DIOR, `slug` dior, `featured` true}.
- `/suggestions` `{"market": "de", "query": "dior sa"}`: 15 suggestions in sections Kollektion (DIOR Sauvage, DIOR Eau Sauvage ...) and Marke (DIOR, Jil Sander), and 5 products.
- `/stores` `{"market": "cz"}`: 7 stores in Brno, Ostrava and Praha, each with address, coordinates, opening hours and `open_now`; `{"market": "pl"}` 11 stores in 7 cities.
- `/store` `{"market": "cz", "store": "florentinum-praha"}`: Parfumerie Praha – Florentinum, Na Florenci 2116/15, 110 00, `services` card payment, complaints, direct sale and order pickup, 7 days of hours from today (Thursday 8:00-20:00), phone 530 514 014, email info@notino.cz.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def notino(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/notino/{endpoint}", headers=HEADERS, json=body, timeout=250)
    r.raise_for_status()
    return r.json()

# One product, then the same product on every other storefront (1 credit each, 2 on gb)
first = notino("product", {"url": "https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/"})["data"]
EAN = "3348901428545"  # the 200 ml bottle
for site in [{"market": first["market"], "url": first["url"]}] + first["alternate_sites"]:
    p = first if site["market"] == first["market"] else notino("product", {"url": site["url"]})["data"]
    for v in p["variants"]:
        if v["ean"] == EAN:
            print(p["shop"], p["currency"], v["price"], v["lowest_price_30d"], v["availability"]["stock_level"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market`, `shop`, `language` and `currency`.

- **item** (search, category, brand, promo) - `product_id`, `master_id`, `url`, `name`, `sub_name`, `brand`, `annotation`, `image`, `price`, `currency`, `rrp`, `unit_price`, `stock_level`, `in_stock`, `product_code`, `master_product_code`, `rating`, `review_count`, `is_new`, `sponsored`, `free_delivery`, `deal`, `variant_count`, `variants[]` {`variant_id`, `label`, `colors`}, `category` {`category`, `subcategory`, `type`, `kind`}.
- **list** - `page_type` (Category, Brand, Promo), `title`, `breadcrumbs[]` {`name`, `url`}, `sort`, `page`, `page_size` (24), `total`, `total_pages`, `has_more`, `count`, `items[]`, `facets[]` {`group`, `type`, `multi_choice`, `values[]` {`id`, `name`, `count`, `selected`, `color`}}, `price_range` {`min`, `max`}, `selected_filters`, `note`; plus `query`, `redirected_to` and `total_capped` (search), `path` and `url` (category, brand, promo), `terms` (promo).
- **product** - `requested`, `selected_variant_id`, `master_id`, `catalog_master_id`, `master_product_code`, `name`, `brand` {`brand_id`, `name`, `url`, `manufacturer`}, `annotation`, `sub_name`, `collection`, `url`, `gender`, `is_perfume`, `description`, `fragrance_notes[]` {`note`, `values`}, `breadcrumbs`, `category`, `rating` {`average`, `count`, `text_reviews`, `translated_reviews`}, `variant_count`, `variants[]` {`variant_id`, `catalog_id`, `name`, `variant_name`, `label`, `order_code`, `product_code`, `ean`, `url`, `price`, `currency`, `vat_percent`, `rrp`, `rrp_type`, `anchor_price`, `lowest_price_30d`, `unit_price`, `amount` {`value`, `unit`}, `availability`, `colors`, `images`, `characteristics[]` {`name`, `values`}, `ingredients`, `instructions`, `warnings`, `manufacturer_importer`, `gift_campaign_ids`}, `gift_campaigns[]`, `deliveries[]` {`name`, `type`, `price`, `free_shipping`, `date`, `date_from`, `date_to`, `order_by_time`}, `alternate_sites[]` {`market`, `locale`, `url`}, `related_product_ids`, `reviews_url`.
- **reviews** - `sort`, `rating`, `page`, `page_size` (8), `product_url`, `reviews_url`, `master_product_id`, `average_rating`, `rating_count`, `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `created_at`, `likes`, `dislikes`, `verified_purchase`, `author_type`, `variant_id`, `from_shop`, `translated`, `source_language`, `original_title`, `original_text`, `partner_domain`, `image_count`}, `rating_buckets` {5..1}, `content_counts`, `shops[]` {`shop`, `market`, `count`}, `variants[]` {`variant_catalog_id`, `count`}, `aspects[]` {`aspect`, `average`} (on review-tab views, else `null`), `view` (`review_page` for the newest 8, `review_tab` for other pages, sorts and star filters).
- **brands** - `query`, `letter`, `featured_only`, `total_brands`, `matches`, `page`, `limit`, `has_more`, `count`, `brands[]` {`name`, `slug`, `url`, `featured`, `letter`}.
- **suggestions** - `query`, `count`, `sections[]` {`section`, `items[]` {`text`, `kind`, `url`}}, `products[]` {`name`, `description`, `product_code`, `url`, `image`}.
- **stores** - `city`, `cities`, `total_stores`, `count`, `stores[]` {`store`, `url`, `name`, `place`, `city_group`, `address` {`street`, `city`, `postcode`, `country`}, `latitude`, `longitude`, `opening_hours[]` {`days`, `opens`, `closes`}, `open_now`, `status_changes_at`, `image`}.
- **store** - `store`, `url`, `name`, `description`, `open_now`, `status_changes_at`, `services` {`card_payment`, `complaints`, `direct_sale`, `order_pickup`, `dermo_shop`}, `opening_hours[]` {`day`, `open`, `today`, `public_holiday`, `times[]` {`start`, `end`}}, `address`, `latitude`, `longitude`, `map_url`, `phone`, `email`, `images`.

## Guardrails

- Name it "Notino (notino.com, the Brno-based online perfume and cosmetics store with 27 country shops)" on first mention, "Notino" after that.
- Prices: quote each with its storefront, currency and the `fetched_at` date ("listed on notino.de on Nov 26, 2026, VAT included"). Prices differ by storefront, also inside the euro zone; never present one storefront's price as Notino's price everywhere.
- 30-day low and RRP: quote `lowest_price_30d` and `rrp` as Notino shows them, beside the price. A percent off from them is computed; label it so.
- Codes: quote `voucher_code` and `discounted_price` as the listing shows them, with the promo `terms` as Notino words them. A code price you work out yourself is computed, never checked out.
- Stock: report `stock_level` as Notino's word and `pickup_store_count` as a store count; never turn either into a unit count.
- Reviews: quote titles, texts, ratings and dates as given, noting `translated` reviews and the storefront they came from; no reviewer names or identity are returned.
- Stores: a store's address, hours, phone and email are Notino's public business details; quote them as given.
- Descriptive only: no commentary on Notino's business, pricing practices or policies. Quote company figures only with their source and date.
- Do not republish Notino product photos, descriptions or logos. Write notino.de (or the storefront's domain) as plain text and cite product names, order codes, EANs, storefronts and capture dates rather than linking Notino pages.
- Terms: Scavio does not collect or store Notino data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no cart and no checkout. Notino's terms and conditions cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, 30-day lows, RRPs, codes, EANs, order codes, stock levels, stores or reviews. Only return what the API returned, with the `fetched_at` time.
- Not available: per-store stock, postcode store search, member or cart prices, price history (store your own), reviewer identity, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `query`; product or reviews without a `url` or `order_code`, or with both ("send one of url or order_code"); an `order_code` that is not 3 to 16 letters and digits; a link that is not a Notino product link; a link from one storefront with another `market` ("... is a notino.pl link but market is de: send market pl"); a `market` that is not a storefront; `page` above 500 (reviews above 8); more than 10 `filters` or an id not from `facets`; `/stores` or `/store` on a storefront without stores ("Notino has stores and pickup points in cz, sk, pl, at, hu, ro, bg, hr; ...").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Notino product at this link on notino.de (the product may not be sold in this storefront).", "Nothing was found for this search on notino.de.", "No Notino category page at <path> on notino.de ...", "No Notino store <store> on notino.cz (send stores[].store).". Take links, order codes, paths and store names from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api).
- `502` means Notino data was temporarily unavailable ("Notino is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Notino is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- A slow answer on a deeper review page (other pages, sorts, star filters) is expected: it can take up to about 4 minutes. Keep the client timeout at 250 seconds or more rather than retrying early.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: product } = await scavio.notino.product({ url: "https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/" });
const { data: results } = await scavio.notino.search({ query: "vitamin c serum", market: "de", sort: "price_asc" });
const { data: promo } = await scavio.notino.promo({ market: "pl" });
const { data: stores } = await scavio.notino.stores({ market: "cz", city: "Praha" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.notino.search(...)`, `product`, `reviews`, `category`, `brand`, `promo`, `brands`, `suggestions`, `stores` and `store`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_notino`, `get_notino_product`, `get_notino_reviews`, `get_notino_category`, `get_notino_brand`, `get_notino_promo`, `get_notino_brands`, `get_notino_suggestions`, `get_notino_stores` and `get_notino_store`. Notino is opt-in: add `notino` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,notino"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/notino-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [product](https://scavio.dev/docs/notino-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [reviews](https://scavio.dev/docs/notino-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [category](https://scavio.dev/docs/notino-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [brand](https://scavio.dev/docs/notino-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [promo](https://scavio.dev/docs/notino-promo?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [brands](https://scavio.dev/docs/notino-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [suggestions](https://scavio.dev/docs/notino-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api), [stores](https://scavio.dev/docs/notino-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api) and [store](https://scavio.dev/docs/notino-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api). Overview: [scavio.dev/notino-api](https://scavio.dev/notino-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=notino-api).
