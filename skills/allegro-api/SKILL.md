---
name: allegro-api
description: "Allegro API for allegro.pl, Poland's largest marketplace, plus allegro.cz (CZK), allegro.sk (EUR) and allegro.hu (HUF): search by keyword or browse a category, 60 organic offers per page plus sponsored slots, with price, price incl. delivery, condition, auction state, discount and the EU 30-day lowest price shown on a discount, sold count (\"x people bought\"), Allegro Smart!, the seller (super seller, positive feedback percent, business or private) and the placement (regular, promoted, sponsored), sorted by price, price with delivery, popularity, ending soonest or newest and filtered by price, new or used, buy now or auction, Smart! and the deals zone (Black Weeks); read one offer in full with every parameter, GTIN, delivery methods and prices, stock, returns, warranty and auction bids; read one catalog product with its lowest price, offer count, buy-box offer, star distribution, review aspects and the first 20 reviews; list every seller's offer for one product for price comparison and price monitoring; read a seller's offers and categories and the seller's buyer ratings, super-seller status and member-since date. Data comes in the site's language. 7 endpoints, 2 credits each. No price history, no bidding or checkout. Allegro no longer grants access to its public offer search (GET /offers/listing)."
version: 1.0.0
tags: allegro, allegro-api, allegro-pl, allegro-price-monitoring, allegro-price-tracker, allegro-scraper, allegro-offers, allegro-offers-listing-alternative, allegro-product-data, allegro-sellers, allegro-seller-ratings, allegro-sold-count, allegro-black-weeks, allegro-czech, allegro-slovakia, allegro-hungary, polish-marketplace, poland-ecommerce, central-europe, cee-ecommerce, marketplace, price-comparison, price-monitoring, competitor-prices, repricing, buy-box, omnibus-price, 30-day-lowest-price, auctions, sponsored-offers, seller-data, product-reviews, multi-country, europe, product-search, product-data, category-browse, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/docs/allegro-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api
---

# Allegro API - Offers, Every Seller's Price, Sellers, Sold Counts

Read Allegro marketplace data from allegro.pl, and from Allegro's Czech, Slovak and Hungarian sites: search by keyword or browse a category, 60 organic offers per page plus the sponsored slots, each with the price, the price including delivery where the page shows it, condition, auction state, discount and the EU 30-day lowest price, how many people bought it recently, the Allegro Smart! flag, the seller (super seller, positive feedback percent, business or private) and where it was placed (regular, promoted, sponsored). Read one offer in full: every parameter, GTIN, the seller's description, delivery methods with prices and estimates, stock, returns, warranty and, on an auction, the current price, minimum next bid and end time. Read one catalog product with its lowest price, offer count, the buy-box offer, the star distribution, review aspects and the first 20 reviews, then list every seller's offer for that product, sortable by price or price with delivery. Read a seller's offers and the categories they sell in, and a seller's buyer ratings with the super-seller flag and member-since date. All 7 endpoints return structured JSON and cost 2 credits each.

Data comes in the site's language exactly as Allegro writes it: Polish titles, conditions, parameters, delivery methods and reviews on allegro.pl ("Nowy", "Używany", "dostawa jutro – kup do 14:00", "17 osób kupiło ostatnio"), Czech on allegro.cz, Slovak on allegro.sk, Hungarian on allegro.hu. Quote those values as returned; translate them for the user only in your own words around the data, never inside it.

Allegro's REST API is built for sellers: it reads and manages your own offers and orders after you register an application and log in as an Allegro user (OAuth). Allegro no longer grants access to its public offer search (`GET /offers/listing`) and has suspended verification for it: its own method list says "access to the resource is no longer possible. Verification has been suspended for business reasons", and Allegro staff wrote on GitHub (October 12, 2026) that the resource "is no longer available as part of Allegro's public API; as a result, access to it is no longer granted." This skill reads public Allegro pages with one Scavio key instead.

See also: for eBay listings and sold comps use `ebay-product-data`; for second-hand fashion on Vinted (including vinted.pl) use `vinted-api`; for Amazon's Polish marketplace use `amazon-product-data` with the `pl` marketplace; for Latin American marketplaces use `mercadolibre-product-data`.

## When to trigger

Use this skill when the user asks to:
- Monitor Allegro prices: track a product's or a list of offers' price, price with delivery, discount and stock over time (Allegro price monitoring, repricing input)
- Compare every seller's price for one product on Allegro: who sells it, at what price and price with delivery, in what condition, with Smart! or not, and who holds the buy box
- Search allegro.pl (or allegro.cz, allegro.sk, allegro.hu) for a product and get prices in PLN (CZK, EUR, HUF), sorted by price, price with delivery, popularity or newest
- Check what a discount is really worth: the EU 30-day lowest price Allegro shows next to a discount, for example during Black Weeks
- See how many people bought an offer or product recently (sold counts) to size demand or find best sellers in a category
- Find auctions ending soon and read an auction's current price, minimum next bid and end time (monitoring only, no bidding)
- Read a seller's catalog on Allegro: their offers, the categories they sell in, business or private, and their buyer ratings, super-seller status and member-since date
- Track which offers Allegro shows as sponsored or promoted for a keyword
- Read a product's star distribution, review aspects and the first reviews on its product page
- Replace `GET /offers/listing` for a project Allegro no longer grants access to

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits, so the free credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
On Growth, 1,000 credits cost $1, so 1,000 Allegro calls cost $2.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In testing, allegro.pl calls answered in 4 to 28 seconds, allegro.cz in 8 to 43, and allegro.sk and allegro.hu in 7 to 57 seconds, with one allegro.sk call at 86 seconds after an automatic retry. Set a client timeout of at least 120 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/allegro/search` | 2 | A keyword search page: 60 organic offers plus sponsored slots, each with `offer_id`, `product_id`, `title`, `url`, `price`, `currency`, `price_with_delivery`, `condition`, `is_auction`, `discount_percent`, `lowest_price_30d`, `seller`, `rating`, `sold_count`, `smart`, `offers_count`, `placement`, `is_sponsored`, `source`. Plus `total` (exact), `total_pages` (at most 100), `applied_filters` and `facets` |
| `POST /api/v1/allegro/offer` | 2 | One offer (one seller's listing, `/oferta/`) by `offer_id` or `url`: price, original price and 30-day lowest price on a discount, price with delivery, stock, sold count, auction state, every parameter, GTIN, brand, description, images, breadcrumb, delivery methods with price and estimate, handling time, returns, warranty, and the seller with feedback counts and, for business sellers, the company name |
| `POST /api/v1/allegro/product` | 2 | One catalog product (`/produkt/`) by `product_id` or `url`: brand, GTIN, parameters, images, breadcrumb, description, `lowest_price` and `offer_count`, the cheapest and fastest highlights, the buy-box `featured_offer`, sold count, rating with 1-5 star distribution, review aspects and the first 20 reviews |
| `POST /api/v1/allegro/product-offers` | 2 | Every seller's offer for one catalog product, 60 per page: price, `price_with_delivery`, condition, seller with feedback percent and count, Smart!, stock where shown, `is_featured` (the buy box) and the search item fields |
| `POST /api/v1/allegro/seller` | 2 | One seller's offers by `login` (the search grid, with search, sorts and filters) plus the seller's `id`, `login`, `is_business` and `url`, `is_active_seller` and the `categories` they sell in with offer counts and a `slug` |
| `POST /api/v1/allegro/seller-feedback` | 2 | One seller's buyer ratings, 20 per page, newest first: a `summary` (recommended / not recommended counts, positive percent, excluded and removed ratings, `member_since`, `super_seller`) and each rating with recommended yes / no, comment, reasons, date, the offers rated and whether it was excluded from the score |
| `POST /api/v1/allegro/category` | 2 | One category's offers by `category_id` or `url`, with the same sorts and filters as search and an optional `query`, plus the category's name, breadcrumb, subcategories or sibling categories with offer counts |

## Markets

Every endpoint takes `country` (default `pl`) and works on all four sites.

| `country` | Site | Currency | Language | pl-only filters |
|---|---|---|---|---|
| `pl` | allegro.pl | PLN | Polish (`pl`) | `buying_format` and `deals` work here |
| `cz` | allegro.cz | CZK | Czech (`cs`) | `buying_format` and `deals` return `400` |
| `sk` | allegro.sk | EUR | Slovak (`sk`) | `buying_format` and `deals` return `400` |
| `hu` | allegro.hu | HUF | Hungarian (`hu`) | `buying_format` and `deals` return `400` |

A `url` from any of the four sites sets the market by itself; if you also send a different `country`, the call returns `400`. Category ids are shared: `491` was laptops on all four sites in testing (Laptopy, Notebooky, Laptopok). Allegro Lokalnie is not a separate source: Allegro Lokalnie offers that allegro.pl mixes into its own results come back flagged `source: "allegro_lokalnie"`.

## Offer vs product

This is the distinction that matters most on Allegro:

- An **offer** is one seller's listing. Its id is a number (`offer_id`, 8-14 digits, e.g. `18801787032`), its page is `/oferta/<slug>-<id>`. Read it with `/allegro/offer`.
- A **product** is a catalog entry that groups the offers of many sellers for the same item. Its id is a uuid (`product_id`, e.g. `90d08230-e02a-4210-913d-d417453321b8`), its page is `/produkt/<slug>-<uuid>`. Read it with `/allegro/product`; list every seller's offer for it with `/allegro/product-offers`.

Search items carry both ids when the offer is linked to a catalog product (`product_id` is `null` otherwise). An item `url` can be either `/oferta/<id>` or a product link with `?offerId=<id>`; both are accepted by `/allegro/offer`. `offers_count` on a search item and `product_offers_count` on an offer say how many offers the product has.

## Workflow

1. **Find offers:** call `/allegro/search` with `query` (or `/allegro/category` with a `category_id`), add `sort` and filters. `applied_filters` echoes the filters the call sent.
2. **Price comparison for one product:** take `product_id` from a search item or an offer, call `/allegro/product` for `lowest_price`, `offer_count` and the buy-box `featured_offer`, then `/allegro/product-offers` with `sort: "price_low_to_high"` (or `price_with_delivery_low_to_high`) and walk `page` up to `total_pages` for every seller's price.
3. **One offer in full:** call `/allegro/offer` with the `offer_id` for parameters, GTIN, delivery prices, stock, returns, warranty and the seller's company name (business sellers).
4. **Price monitoring:** poll `/allegro/offer` for a fixed list of offer ids, or `/allegro/product-offers` for a product, on a schedule; store `price`, `price_with_delivery`, `discount_percent`, `lowest_price_30d`, `stock` and the time per run; compare runs yourself. There is no price history endpoint.
5. **Judge a seller:** `seller.login` from any item feeds `/allegro/seller-feedback` (super-seller flag, positive percent, member since, recent ratings) and `/allegro/seller` (their offers and categories; narrow with a `categories[].slug` in `category`).

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars), in any language. Misspellings are not corrected |
| `country` | string | `pl` | `pl`, `cz`, `sk` or `hu` |
| `category_id` | string or integer | all | Search inside one category: an id (`491`) or its slug (`laptopy-491`), from `category.id` or `breadcrumb[].id` of an offer |
| `page` | integer | 1 | 1-100. 60 organic offers per page; sponsored slots come on top |
| `sort` | string | `relevance` | `relevance`, `price_low_to_high`, `price_high_to_low`, `price_with_delivery_low_to_high`, `price_with_delivery_high_to_low`, `popularity`, `ending_soonest` (auctions first to end) or `newest` |
| `min_price` / `max_price` | number | none | Price range in the site's currency. `min_price` must not be above `max_price` |
| `condition` | string | all | `new` or `used` (the site's single "used" value; "for renovation" is not included) |
| `buying_format` | string | all | pl only: `buy_now` (fixed price) or `auction` |
| `smart` | boolean | false | Only offers with Allegro Smart! |
| `deals` | boolean | false | pl only: only offers in Allegro's deals and promotions zone, which includes seasonal campaign deals such as Black Weeks while they run |

### Offer (`/offer`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `offer_id` | string or integer | one of | An offer number (8-14 digits): `items[].offer_id` of a search, category or seller answer |
| `url` | string | one of | An offer link (`allegro.pl/oferta/...`) or a product link with `?offerId=`, on any of the four sites. Send `offer_id` or `url`, not both |
| `country` | string | `pl` | Used with `offer_id`; a `url` sets its own market |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A catalog product id (uuid): `items[].product_id` of a search or `product_id` of an offer |
| `url` | string | one of | A product link (`allegro.pl/produkt/...`, any of the four sites). Send `product_id` or `url`, not both |
| `country` | string | `pl` | As on offer |

### Product offers (`/product-offers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` / `country` | | | As on product |
| `page` | integer | 1 | 1-100, 60 offers per page |
| `sort` | string | `relevance` | `relevance`, `price_low_to_high`, `price_high_to_low`, `price_with_delivery_low_to_high`, `price_with_delivery_high_to_low` or `popularity` |
| `min_price` / `max_price`, `condition`, `smart` | | | As on search. `buying_format` and `deals` are not accepted here (`400`) |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `login` | string | required | A seller login: `items[].seller.login` of a search or `seller.login` of an offer (e.g. `Yupilo_pl`) |
| `country` | string | `pl` | As on search |
| `query` | string | none | Search within the seller's offers |
| `category` | string | none | One of the seller's categories: a `categories[].slug` of a previous seller answer (e.g. `komputery`), not a category id |
| `page`, `sort`, `min_price` / `max_price`, `condition`, `buying_format`, `smart`, `deals` | | | As on search |

### Seller feedback (`/seller-feedback`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `login` | string | required | As on seller |
| `country` | string | `pl` | As on search |
| `page` | integer | 1 | 1-500, 20 ratings per page, newest first |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string or integer | one of | A category id (`491`) or its slug (`laptopy-491`): `breadcrumb[].id` of an offer or `subcategories[].id` of a category answer |
| `url` | string | one of | A category link (`allegro.pl/kategoria/...`, any of the four sites). Send `category_id` or `url`, not both |
| `country` | string | `pl` | As on search |
| `query` | string | none | Search within the category |
| `page`, `sort` and every search filter | | | As on search |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "laptop"}'
```

Captured `data` (69 of 73 items and 32 of 33 facets trimmed):

```json
{
  "query": "laptop",
  "category_id": null,
  "sort": "relevance",
  "applied_filters": {},
  "total": 1173947,
  "total_pages": 100,
  "page": 1,
  "page_size": 60,
  "count": 73,
  "items": [
    {
      "offer_id": "19018116806",
      "product_id": "53528933-d4b9-4b98-8a80-9d2061ecf278",
      "title": "Laptop HP Omnibook 3 16 \" AMD Ryzen 5 16 GB / 512 GB srebrny",
      "url": "https://allegro.pl/oferta/19018116806",
      "image": "https://a.allegroimg.com/s720/11de86/1c275065476082038f0c29d0f8f8/HP-OMNIBOOK-3-16-Ryzen-5-230-16GB-SSD512-IPS-WiFi-7-Win11",
      "price": 2499,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": null,
      "free_delivery": false,
      "delivery_text": "dostawa jutro – kup do 14:00",
      "condition": null,
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": 10,
      "lowest_price_30d": 2799,
      "seller": {"id": "24801306", "login": "ogit_pl", "super_seller": true, "positive_feedback_percent": 99.4, "positive_feedback_count": null, "is_business": true},
      "rating": null,
      "rating_count": null,
      "sold_count": 17,
      "sold_label": "17 osób kupiło ostatnio",
      "smart": true,
      "offers_count": 1,
      "stock": null,
      "placement": "sponsored",
      "is_sponsored": true,
      "source": "allegro"
    },
    {
      "offer_id": "17118603300",
      "product_id": "880fe6be-3992-4532-97f2-8fd88c55889a",
      "title": "Laptop Lenovo V15 G4 15,6 \" AMD Ryzen 5 16 GB / 512 GB czarny",
      "url": "https://allegro.pl/produkt/laptop-lenovo-v15-g4-15-6-amd-ryzen-5-16-gb-512-gb-czarny-880fe6be-3992-4532-97f2-8fd88c55889a?offerId=17118603300",
      "image": "https://a.allegroimg.com/s720/111a49/76af06114cf8980f1b9fd504edd4/LENOVO-V15-G4-RYZEN-5-7520U-16GB-SSD512-FHD-Win11",
      "price": 2499,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": null,
      "free_delivery": false,
      "delivery_text": "dostawa jutro – kup do 14:00",
      "condition": null,
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": null,
      "lowest_price_30d": null,
      "seller": {"id": "24801306", "login": "ogit_pl", "super_seller": true, "positive_feedback_percent": 99.4, "positive_feedback_count": null, "is_business": true},
      "rating": 4.83,
      "rating_count": 114,
      "sold_count": 41,
      "sold_label": "41 osób kupiło ostatnio",
      "smart": true,
      "offers_count": 2,
      "stock": null,
      "placement": "promoted",
      "is_sponsored": false,
      "source": "allegro"
    },
    {
      "offer_id": "18358298114",
      "product_id": "2d0a1707-2a9c-4630-a6dd-9ebcfe8333a8",
      "title": "Laptop HP ProBook x360 11,6\" 8 GB RAM 128 GB SSD Windows 11 niebieski",
      "url": "https://allegro.pl/produkt/laptop-hp-probook-x360-11-6-8-gb-ram-128-gb-ssd-windows-11-niebieski-2d0a1707-2a9c-4630-a6dd-9ebcfe8333a8?offerId=18358298114",
      "image": "https://a.allegroimg.com/s720/117d61/f56585604b32bd19e3ed35109a32/Laptop-HP-11-X360-2w1-8-128GB-SSD-Win11-DOTYK-6-godzin-PRACY-NA-BATERII",
      "price": 588.78,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": null,
      "free_delivery": false,
      "delivery_text": "dostawa jutro – kup do 14:30",
      "condition": "Powystawowy",
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": null,
      "lowest_price_30d": null,
      "seller": {"id": "69710181", "login": "LobiCom", "super_seller": true, "positive_feedback_percent": 98.5, "positive_feedback_count": null, "is_business": true},
      "rating": null,
      "rating_count": null,
      "sold_count": 109,
      "sold_label": "109 osób kupiło ostatnio",
      "smart": true,
      "offers_count": 1,
      "stock": null,
      "placement": "regular",
      "is_sponsored": false,
      "source": "allegro"
    },
    {
      "offer_id": "1095101825",
      "product_id": null,
      "title": "LENOVO Thinkpad T470 14\" Touch FHD, i5-7300U, 16GB RAM, SSD 512GB+128GB",
      "url": "https://allegrolokalnie.pl/oferta/lenovo-thinkpad-t470-14-touch-fhd-i57300u-16gb-ram-ssd-512gb-128gb?rep=1095101825",
      "image": "https://a.allegroimg.com/s720/1e3e0c/2842ddeb437181198ebc762b6fae/LENOVO-Thinkpad-T470-14-Touch-FHD-i5-7300U-16GB-RAM-SSD-512GB-128GB",
      "price": 675,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": null,
      "free_delivery": false,
      "delivery_text": null,
      "condition": "Używany",
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": 25,
      "lowest_price_30d": 900,
      "seller": {"id": "44910", "login": "polo08", "super_seller": false, "positive_feedback_percent": null, "positive_feedback_count": null, "is_business": false},
      "rating": null,
      "rating_count": null,
      "sold_count": null,
      "sold_label": null,
      "smart": true,
      "offers_count": null,
      "stock": 1,
      "placement": "promoted",
      "is_sponsored": false,
      "source": "allegro_lokalnie"
    }
  ],
  "facets": [
    {
      "id": "offerType",
      "label": "Rodzaj oferty",
      "values": [
        {"label": "kup teraz", "param": "offerTypeBuyNow", "value": "1", "count": 10000, "count_label": "9999+", "selected": false},
        {"label": "licytacje", "param": "offerTypeAuction", "value": "2", "count": 848, "count_label": "848", "selected": false},
        {"label": "ogłoszenia", "param": "offerTypeAdvert", "value": "3", "count": 4, "count_label": "4", "selected": false}
      ]
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

Read the items as: the first is a sponsored slot (`is_sponsored: true`) at 2,499.00 PLN, 10% off, and Allegro shows 2,799.00 PLN as the lowest price of the 30 days before that discount (`lowest_price_30d`). The second is in Allegro's promoted block (`placement: "promoted"`): on this relevance search 60 of the 73 items were promoted, 12 were sponsored and 1 was regular, so on page 1 "promoted" is the normal placement, not an exception. The fourth comes from Allegro Lokalnie (`source: "allegro_lokalnie"`, an `allegrolokalnie.pl` URL, `product_id: null`); it cannot be read with `/allegro/offer`. `sold_count: 17` is the number of people who bought recently as Allegro shows it ("17 osób kupiło ostatnio"), not a lifetime total. `price_with_delivery` is `null` on every keyword-search tile in this capture; take it from `/allegro/product-offers`, `/allegro/seller` or `/allegro/offer`. `total` is exact (1,173,947 matches) while `total_pages` stops at 100. A facet `count` with a `count_label` ending in `+` ("9999+") is a floor, not an exact number.

### Offer

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/offer \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"offer_id": "18801787032"}'
```

Captured `data` (39 of 43 parameters, 13 of 14 images, 34 of 36 delivery methods and most of the description trimmed):

```json
{
  "offer_id": "18801787032",
  "product_id": "42a995a2-04ad-4a0e-9047-d24b2400cbe0",
  "title": "Laptop Acer Aspire Lite 15,6 FHD Celeron N4500 8GB SSD256GB Intel Graphics",
  "url": "https://allegro.pl/oferta/laptop-acer-aspire-lite-15-6-fhd-celeron-n4500-8gb-ssd256gb-intel-graphics-18801787032",
  "product_url": "https://allegro.pl/produkt/laptop-acer-aspire-lite-15-6-fhd-celeron-n4500-8gb-ssd256gb-intel-graphics-42a995a2-04ad-4a0e-9047-d24b2400cbe0",
  "status": "active",
  "condition": "Nowy",
  "price": 1357.02,
  "currency": "PLN",
  "buy_now": true,
  "buy_now_price": null,
  "original_price": 1399,
  "lowest_price_30d": 1399,
  "lowest_price_30d_note": "Najniższa cena oferty z 30 dni przed obniżką, obowiązuje do 30.11.2026 lub wyczerpania zapasów",
  "discount_percent": 3,
  "discount_amount": 41.98,
  "price_with_delivery": 1367.51,
  "stock": 42,
  "stock_label": "z 42 sztuk",
  "sold_count": 3,
  "sold_label": "3 osoby kupiły 3 sztuki",
  "is_auction": false,
  "auction": null,
  "parameters": [
    {"name": "Stan", "value": "Nowy"},
    {"name": "Faktura", "value": "Wystawiam fakturę VAT"},
    {"name": "Kod producenta", "value": "NX.DHFEX.001-8G-S256-NOS"},
    {"name": "Marka", "value": "Acer"}
  ],
  "gtin": null,
  "brand": "Acer",
  "description": "Laptop Acer Aspire Lite 15\nPoznaj Aspire Lite 15 – laptopa, który stawia na prostotę bez kompromisów. Zaprojektowany z m...",
  "images": ["https://a.allegroimg.com/original/11ed6a/2acc11c54d59a95c78be2bc159c4/Laptop-Acer-Aspire-Lite-15-6-FHD-Celeron-N4500-8GB-SSD256GB-Intel-Graphics"],
  "breadcrumb": [
    {"id": "42540aec-367a-4e5e-b411-17c09b08e41f", "name": "Elektronika", "url": "https://allegro.pl/dzial/elektronika"},
    {"id": "2", "name": "Komputery", "url": "https://allegro.pl/kategoria/komputery"},
    {"id": "491", "name": "Laptopy", "url": "https://allegro.pl/kategoria/laptopy-491"}
  ],
  "category": {"id": "491", "name": "Laptopy"},
  "delivery": [
    {"method": "Allegro One Box, Allegro One", "group": "Odbiór w punkcie", "price": 10.49, "currency": "PLN", "eta_text": "sob. 14 lis. w punkcie"},
    {"method": "Kurier, InPost", "group": "Na adres", "price": 12.49, "currency": "PLN", "eta_text": "pon. 16 lis. u Ciebie"}
  ],
  "handling_time": "24 godziny",
  "returns": {"days": 14, "label": "Masz 14 dni na odstąpienie od umowy."},
  "warranty": {"label": "Produkt jest objęty gwarancją producenta/dystrybutora przez 24 miesiące od zakupu.", "period": "24 miesiące", "type": "producenta/dystrybutora"},
  "seller": {
    "id": "12846481",
    "login": "REMEDIAL",
    "super_seller": true,
    "positive_feedback_percent": 98.9,
    "positive_count": 2852,
    "negative_count": 33,
    "is_business": true,
    "company_name": "REMEDIAL SPÓŁKA CYWILNA R. SZYMAŃSKI, Ł. SZYMAŃSKI"
  },
  "rating": 5,
  "rating_count": 1,
  "product_offers_count": 2,
  "smart": true,
  "country": "pl",
  "language": "pl"
}
```

The offer is discounted: `price` 1,357.02 PLN, `discount_percent` 3, and `original_price` equals `lowest_price_30d` (1,399.00 PLN), because the "original" price Allegro shows next to a discount is the EU 30-day lowest price; `lowest_price_30d_note` is Allegro's own disclosure text. `price_with_delivery` (1,367.51) is the price plus the cheapest delivery (10.49). `sold_count: 3` counts buyers; `sold_label` says 3 people bought 3 units. `company_name` is returned for business sellers only; addresses and tax ids are not returned. On an auction, `is_auction` is `true`, `price` is the current price, `buy_now_price` the optional buy-now price, `auction` holds `current_price`, `min_next_bid`, `bid_step`, `ends_at` and `has_bids`, and `sold_count` is `null` (the bid status is in `auction.bids_label`). There is no bid history.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "90d08230-e02a-4210-913d-d417453321b8"}'
```

Captured `data` (9 of 12 parameters, 6 of 7 images, 3 of 5 aspects, 18 of 20 reviews and most of the description trimmed):

```json
{
  "product_id": "90d08230-e02a-4210-913d-d417453321b8",
  "title": "LEGO City Kalendarz adwentowy na 2026 rok, prezent dla 5-latka 60510",
  "url": "https://allegro.pl/produkt/lego-city-kalendarz-adwentowy-na-2026-rok-prezent-dla-5-latka-60510-90d08230-e02a-4210-913d-d417453321b8",
  "brand": "LEGO",
  "gtin": "5702018056783",
  "parameters": [{"name": "Stan", "value": "Nowy"}, {"name": "Faktura", "value": "Wystawiam fakturę VAT"}, {"name": "Stan opakowania", "value": "oryginalne"}],
  "images": ["https://a.allegroimg.com/original/117a18/79ac1579432da28a006aca479f56"],
  "breadcrumb": [
    {"id": "11763", "name": "Dziecko", "url": "https://allegro.pl/dzial/dziecko"},
    {"id": "11818", "name": "Zabawki", "url": "https://allegro.pl/kategoria/zabawki-11818"},
    {"id": "11823", "name": "Klocki", "url": "https://allegro.pl/kategoria/zabawki-klocki-11823"},
    {"id": "17865", "name": "LEGO", "url": "https://allegro.pl/kategoria/klocki-lego-17865"},
    {"id": "305637", "name": "Kalendarze adwentowe", "url": "https://allegro.pl/kategoria/lego-kalendarze-adwentowe-305637"}
  ],
  "category": {"id": "305637", "name": "Kalendarze adwentowe"},
  "description": "LEGO City 60510 Kalendarz adwentowy na 2026 rok\nRozpocznij odliczanie do świąt dzięki Kalendarzowi a...",
  "currency": "PLN",
  "lowest_price": 67.82,
  "offer_count": 406,
  "offer_highlights": [
    {"label": "NAJTANIEJ", "subtitle": "Stan: Nowy", "price": 67.82, "currency": "PLN", "kind": "cheapest"},
    {"label": "NAJSZYBCIEJ", "subtitle": "dostawa dzisiaj do wybranych miast", "price": 97.49, "currency": "PLN", "kind": "fastest"}
  ],
  "featured_offer": {
    "offer_id": "18968708171",
    "url": "https://allegro.pl/oferta/lego-city-60510-kalendarz-adwentowy-na-2026-rok-18968708171",
    "price": 99.9,
    "currency": "PLN",
    "original_price": null,
    "lowest_price_30d": null,
    "discount_percent": null,
    "price_with_delivery": 110.39,
    "condition": "Nowy",
    "is_auction": false,
    "smart": true,
    "stock": 32,
    "sold_count": 105,
    "sold_label": "105 osób kupiło 119 sztuk",
    "seller": {
      "id": "107124968",
      "login": "MONS22",
      "super_seller": true,
      "positive_feedback_percent": 99.5,
      "positive_count": 1420,
      "negative_count": 7,
      "is_business": true,
      "company_name": "MONS Sławomir Kwintal"
    }
  },
  "sold_count": 10482,
  "sold_label": "10 482 osoby kupiły ostatnio",
  "rating": {
    "average": 4.95,
    "count": 173,
    "distribution": [
      {"stars": 5, "count": 167, "percent": 96},
      {"stars": 4, "count": 4, "percent": 2},
      {"stars": 3, "count": 2, "percent": 1},
      {"stars": 2, "count": 0, "percent": 0},
      {"stars": 1, "count": 0, "percent": 0}
    ]
  },
  "aspects": [
    {"label": "Bawialność", "sentiment": "positive", "mentions": 3, "positive": 3, "negative": 0, "neutral": 0},
    {"label": "Jakość wykonania", "sentiment": "neutral", "mentions": 3, "positive": 2, "negative": 1, "neutral": 0}
  ],
  "review_count": 26,
  "reviews": [
    {
      "id": "6af1c7d21c8314acefeeae22",
      "rating": 5,
      "text": "Wygląda świetnie. Zawartość, jak to przy kalendarzu adwentowym będzie można ocenić 24 grudnia.",
      "pros": null,
      "cons": null,
      "author": "b...y",
      "created_at": "2026-11-09T13:17:06.486Z",
      "helpful_count": 0,
      "not_helpful_count": 0,
      "images": [],
      "language": "pl-PL",
      "is_best": true,
      "seller_login": "MONS22"
    },
    {
      "id": "6aef0f5f2aef611f760d11c4",
      "rating": 5,
      "text": "Jak zawsze super produkt. Chodz klockoglowi wiedza ze jakość plastiku jest slabsza - ale to już sprawy ekologii.",
      "pros": null,
      "cons": null,
      "author": "d...l",
      "created_at": "2026-11-07T11:45:35.673Z",
      "helpful_count": 0,
      "not_helpful_count": 0,
      "images": [],
      "language": "pl-PL",
      "is_best": false,
      "seller_login": "Allegro"
    }
  ],
  "reviews_note": "first 20 reviews as shown on the product page",
  "country": "pl",
  "language": "pl"
}
```

The product has 406 offers; the cheapest is 67.82 PLN (`lowest_price`, also the "NAJTANIEJ" highlight), while the buy-box `featured_offer` is 99.90 PLN. There is no highest price: use `/allegro/product-offers` sorted `price_high_to_low` for that. `reviews` holds the first 20 reviews as shown on the product page (`reviews_note`), not the full history; `review_count` (26) and `rating.count` (173) are different counts, so quote the one you mean. `author` is masked by Allegro ("b...y"). Reviews have `is_best` and `images` but no verified-purchase flag.

### Product offers (every seller's price)

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/product-offers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "90d08230-e02a-4210-913d-d417453321b8"}'
```

Captured `data` (58 of 61 offers and every facet trimmed):

```json
{
  "product_id": "90d08230-e02a-4210-913d-d417453321b8",
  "title": "LEGO City Kalendarz adwentowy na 2026 rok, prezent dla 5-latka 60510",
  "sort": "relevance",
  "applied_filters": {},
  "total": 407,
  "total_pages": 7,
  "page": 1,
  "page_size": 60,
  "count": 61,
  "facets": [],
  "offers": [
    {
      "offer_id": "18894409301",
      "product_id": "90d08230-e02a-4210-913d-d417453321b8",
      "title": "LEGO 60510 City Kalendarz adwentowy na 2026 rok",
      "url": "https://allegro.pl/produkt/lego-city-kalendarz-adwentowy-na-2026-rok-prezent-dla-5-latka-60510-90d08230-e02a-4210-913d-d417453321b8?offerId=18894409301",
      "image": "https://a.allegroimg.com/s720/1142ba/e9a3eb3049649c4870fc0a923fa4/LEGO-60510-City-Kalendarz-adwentowy-na-2026-rok",
      "price": 84.99,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": 84.99,
      "free_delivery": true,
      "delivery_text": "dostawa jutro – kup do 15:00",
      "condition": "Nowy",
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": null,
      "lowest_price_30d": null,
      "seller": {"id": "6879039", "login": "ELECTROpl", "super_seller": true, "positive_feedback_percent": 98.3, "positive_feedback_count": 146114, "is_business": true},
      "rating": 4.95,
      "rating_count": 173,
      "sold_count": null,
      "sold_label": null,
      "smart": true,
      "offers_count": null,
      "stock": 0,
      "is_sponsored": false,
      "source": "allegro",
      "placement": "featured",
      "is_featured": true
    },
    {
      "offer_id": "18855202264",
      "product_id": "90d08230-e02a-4210-913d-d417453321b8",
      "title": "LEGO City 60510 Kalendarz adwentowy na 2026 rok, prezent dla 5-latka",
      "url": "https://allegro.pl/oferta/18855202264",
      "image": "https://a.allegroimg.com/s720/117a18/79ac1579432da28a006aca479f56/LEGO-City-60510-Kalendarz-adwentowy-na-2026-rok-prezent-dla-5-latka",
      "price": 99.99,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": 110.48,
      "free_delivery": false,
      "delivery_text": "dostawa jutro – kup do 17:00",
      "condition": "Nowy",
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": null,
      "lowest_price_30d": null,
      "seller": {"id": "1680", "login": "Allegro", "super_seller": true, "positive_feedback_percent": 98.9, "positive_feedback_count": 275457, "is_business": true},
      "rating": 4.95,
      "rating_count": 173,
      "sold_count": null,
      "sold_label": null,
      "smart": true,
      "offers_count": null,
      "stock": 482,
      "is_sponsored": true,
      "source": "allegro",
      "placement": "sponsored",
      "is_featured": false
    },
    {
      "offer_id": "18894409304",
      "product_id": "90d08230-e02a-4210-913d-d417453321b8",
      "title": "LEGO 60510 City Kalendarz adwentowy na 2026 rok",
      "url": "https://allegro.pl/produkt/lego-city-kalendarz-adwentowy-na-2026-rok-prezent-dla-5-latka-60510-90d08230-e02a-4210-913d-d417453321b8?offerId=18894409304",
      "image": "https://a.allegroimg.com/s720/1142ba/e9a3eb3049649c4870fc0a923fa4/LEGO-60510-City-Kalendarz-adwentowy-na-2026-rok",
      "price": 84.99,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": 84.99,
      "free_delivery": true,
      "delivery_text": "dostawa jutro – kup do 15:00",
      "condition": "Nowy",
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": null,
      "lowest_price_30d": null,
      "seller": {"id": "42388365", "login": "avans__pl", "super_seller": true, "positive_feedback_percent": 98.3, "positive_feedback_count": 164716, "is_business": true},
      "rating": 4.95,
      "rating_count": 173,
      "sold_count": null,
      "sold_label": null,
      "smart": true,
      "offers_count": null,
      "stock": 164,
      "is_sponsored": false,
      "source": "allegro",
      "placement": "regular",
      "is_featured": false
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

The first offer is the buy box (`is_featured: true`, `placement: "featured"`), then a sponsored slot, then Allegro's promoted block, then the regular offers. On this relevance sort the cheapest price on page 1 was 84.99 PLN, while `/allegro/product` reported a 67.82 PLN offer: to find the cheapest sellers, sort `price_low_to_high` or `price_with_delivery_low_to_high` and walk the pages. Sponsored slots are not sorted, and where the site shows promoted offers as their own block each block is in sort order, so sort the rows yourself before naming the cheapest. The buy-box offer changes over time: `/allegro/product` and `/allegro/product-offers` named different featured offers in captures taken a minute apart, so quote it from the call you are reporting.

### Seller

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"login": "Yupilo_pl"}'
```

Captured `data` (59 of 60 items and every facet trimmed):

```json
{
  "login": "Yupilo_pl",
  "seller": {
    "id": "102033445",
    "login": "Yupilo_pl",
    "is_business": true,
    "url": "https://allegro.pl/uzytkownik/Yupilo_pl",
    "feedback_note": "super seller status, feedback percent and counts: seller-feedback"
  },
  "is_active_seller": true,
  "query": null,
  "category": null,
  "categories": [
    {"id": "11763", "name": "Dziecko", "count": 1, "slug": "dziecko"},
    {"id": "2", "name": "Komputery", "count": 172, "slug": "komputery"},
    {"id": "4", "name": "Telefony i Akcesoria", "count": 1, "slug": "telefony-i-akcesoria"}
  ],
  "sort": "relevance",
  "applied_filters": {},
  "total": 174,
  "total_pages": 3,
  "page": 1,
  "page_size": 60,
  "count": 60,
  "items": [
    {
      "offer_id": "18624096238",
      "product_id": "128ec606-0cf4-4256-b37d-2c9d78065c78",
      "title": "Stacja Dock Dell WD15 USB-C PD 2 monitory HDMI DP LAN RJ-45 uniwersalna HUB",
      "url": "https://allegro.pl/produkt/stacja-dokujaca-dell-452-bccw-128ec606-0cf4-4256-b37d-2c9d78065c78?offerId=18624096238",
      "image": "https://a.allegroimg.com/s720/1122c2/d3ddca2c4c8391418965815d0b16/Stacja-Dock-Dell-WD15-USB-C-PD-2-monitory-HDMI-DP-LAN-RJ-45-uniwersalna-HUB",
      "price": 250,
      "currency": "PLN",
      "buy_now_price": null,
      "price_with_delivery": 260.49,
      "free_delivery": false,
      "delivery_text": "dostawa jutro – kup do 15:00",
      "condition": null,
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": null,
      "lowest_price_30d": null,
      "seller": {"id": "102033445", "login": "Yupilo_pl", "super_seller": true, "positive_feedback_percent": null, "positive_feedback_count": null, "is_business": true},
      "rating": 4.88,
      "rating_count": 24,
      "sold_count": 55,
      "sold_label": "55 osób kupiło ostatnio",
      "smart": true,
      "offers_count": 1,
      "stock": null,
      "placement": "promoted",
      "is_sponsored": false,
      "source": "allegro"
    }
  ],
  "facets": [],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

The seller summary here is `id`, `login`, `is_business` and `url` only: read the super-seller flag, positive percent and member-since date from `/allegro/seller-feedback`. The per-item `seller` block on this endpoint is not the authoritative score (it disagreed with the ratings page in testing). To narrow to one category pass `category: "komputery"` (a `slug`), not the id.

### Seller feedback

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/seller-feedback \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"login": "Yupilo_pl"}'
```

Captured `data` (18 of 20 ratings trimmed):

```json
{
  "login": "Yupilo_pl",
  "summary": {
    "recommended": 379,
    "recommended_unique": 372,
    "not_recommended": 1,
    "not_recommended_unique": 1,
    "positive_percent": 99.7,
    "received": 381,
    "excluded": 7,
    "removed": 1,
    "member_since": "2021-07-23",
    "super_seller": true
  },
  "total": 380,
  "total_pages": 19,
  "page": 1,
  "page_size": 20,
  "count": 20,
  "ratings": [
    {
      "id": "6af4140fc4f5197c35717e61",
      "recommended": true,
      "comment": null,
      "comment_language": null,
      "justifications": ["Miła obsługa", "Dostawa na czas", "Dostawa przed czasem", "Sprzedający szybko odpisuje", "Dobrze zabezpieczony produkt"],
      "created_at": "2026-11-11T07:06:55.480Z",
      "offers": [
        {
          "offer_id": "19066494124",
          "title": "Metalowy laptop HP EliteBook 14 G6 IPS 16 GB 256 GB LAN Windows 11 + Office",
          "url": "https://allegro.pl/oferta/metalowy-laptop-hp-elitebook-14-g6-ips-16-gb-256-gb-lan-windows-11-office-19066494124"
        }
      ],
      "excluded": false,
      "exclusion_reason": null
    },
    {
      "id": "6ae31e00cf5b2a3af2cd8f80",
      "recommended": true,
      "comment": null,
      "comment_language": null,
      "justifications": [],
      "created_at": "2026-10-29T10:20:48.354Z",
      "offers": [
        {
          "offer_id": "16515366041",
          "title": "ORYGINALNY ZASILACZ ŁADOWARKA DELL 130W 7.4mm 6.7A| do stacja dokująca WD15",
          "url": "https://allegro.pl/oferta/oryginalny-zasilacz-ladowarka-dell-130w-7-4mm-6-7a-do-stacja-dokujaca-wd15-16515366041"
        }
      ],
      "excluded": true,
      "exclusion_reason": "Kupujący ocenił już inny zakup u tego sprzedawcy, dokonany w krótkim odstępie czasu."
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

`positive_percent` is 99.7 with 379 recommended and 1 not recommended. `justifications` are the reasons the buyer ticked, in Polish ("Dostawa na czas" is on-time delivery). An `excluded: true` rating does not count toward the score and `exclusion_reason` says why in Allegro's words. No buyer identity is returned.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "491"}'
```

Captured `data` (all 73 items, 21 of 23 sibling categories and every facet trimmed):

```json
{
  "category": {
    "id": "491",
    "name": "Laptopy",
    "url": "https://allegro.pl/kategoria/laptopy-491",
    "breadcrumb": [{"id": "42540aec-367a-4e5e-b411-17c09b08e41f", "name": "Elektronika"}, {"id": "2", "name": "Komputery"}, {"id": "491", "name": "Laptopy"}],
    "subcategories": [],
    "sibling_categories": [
      {"id": "497", "name": "Akcesoria (Laptop, PC)", "count": 9999, "count_label": "9999+", "url": "https://allegro.pl/kategoria/akcesoria-laptop-pc-497"},
      {"id": "77801", "name": "Części do laptopów", "count": 9999, "count_label": "9999+", "url": "https://allegro.pl/kategoria/czesci-do-laptopow-77801"}
    ]
  },
  "query": null,
  "sort": "relevance",
  "applied_filters": {},
  "total": 109504,
  "total_pages": 100,
  "page": 1,
  "page_size": 60,
  "count": 73,
  "items": [],
  "facets": [],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

`items` and `facets` have the search shape. A leaf category has `subcategories: []` and lists `sibling_categories` instead; a sibling `count` of 9999 with `count_label` "9999+" means at least 9,999.

### Czech, Slovak and Hungarian sites

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "notebook", "country": "cz"}'
```

Captured `data` (71 of 72 items and every facet trimmed):

```json
{
  "query": "notebook",
  "category_id": null,
  "sort": "relevance",
  "applied_filters": {},
  "total": 330315,
  "total_pages": 100,
  "page": 1,
  "page_size": 60,
  "count": 72,
  "items": [
    {
      "offer_id": "16968129088",
      "product_id": "99bb3657-b1a1-4740-b0a0-fa925208c67f",
      "title": "Notebook Umax UMM230240 14,1\" Intel Celeron 4 GB / 128 GB šedý",
      "url": "https://allegro.cz/produkt/notebook-umax-umm230240-14-1-intel-celeron-4-gb-128-gb-sedy-99bb3657-b1a1-4740-b0a0-fa925208c67f?offerId=16968129088",
      "image": "https://a.allegroimg.com/s720/25652b/73e2691f4f1590cd801b095ee0f7/Umax-VisionBook-14WRx-seda-UMM230240",
      "price": 3385,
      "currency": "CZK",
      "buy_now_price": null,
      "price_with_delivery": null,
      "free_delivery": false,
      "delivery_text": "doručení zítra – kupte do 21:00",
      "condition": null,
      "is_auction": false,
      "auction_ends_in": null,
      "discount_percent": 19,
      "lowest_price_30d": 4213,
      "seller": {"id": "109981040", "login": "mall-cz", "super_seller": false, "positive_feedback_percent": 97.3, "positive_feedback_count": null, "is_business": true},
      "rating": 4.2,
      "rating_count": 25,
      "sold_count": 60,
      "sold_label": "60 lidí nedávno koupilo",
      "smart": true,
      "offers_count": 3,
      "stock": null,
      "placement": "regular",
      "is_sponsored": false,
      "source": "allegro"
    }
  ],
  "facets": [],
  "country": "cz",
  "language": "cs",
  "currency": "CZK"
}
```

```bash
curl -X POST https://api.scavio.dev/api/v1/allegro/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "3a659be2-34b3-4d9a-9a24-5c694f9ef447", "country": "hu"}'
```

Captured `data` (`url`, catalog fields, aspects and description trimmed):

```json
{
  "product_id": "3a659be2-34b3-4d9a-9a24-5c694f9ef447",
  "title": "Laptop ASUS TUF Gaming A15 (2021) 15,6 \" AMD Ryzen 7 16 GB / 1 GB szürke",
  "currency": "HUF",
  "lowest_price": 322480,
  "offer_count": 2,
  "offer_highlights": [
    {"label": "LEGOLCSÓBB", "subtitle": "Állapot: új", "price": 322480, "currency": "HUF", "kind": "cheapest"},
    {"label": "LEGGYORSABB", "subtitle": "szállítás nov. 17, K.", "price": 404990, "currency": "HUF", "kind": "fastest"}
  ],
  "featured_offer": {
    "offer_id": "18978193331",
    "url": "https://allegro.hu/ajanlat/asus-tuf-a15-ryzen-7-16gb-1tb-ssd-rtx-3050-18978193331",
    "price": 322480,
    "currency": "HUF",
    "original_price": null,
    "lowest_price_30d": null,
    "discount_percent": null,
    "price_with_delivery": 323270,
    "condition": "új",
    "is_auction": false,
    "smart": true,
    "stock": 32,
    "sold_count": null,
    "sold_label": null,
    "seller": {
      "id": "134370249",
      "login": "Europeer",
      "super_seller": false,
      "positive_feedback_percent": 92.4,
      "positive_count": 208,
      "negative_count": 17,
      "is_business": true,
      "company_name": "EUROPEER SZOLGÁLTATÓ KORLÁTOLT FELELŐSSÉGŰ TÁRSASÁG"
    }
  },
  "sold_count": null,
  "sold_label": null,
  "rating": null,
  "review_count": 0,
  "reviews": [],
  "country": "hu",
  "language": "hu"
}
```

Prices come in CZK, EUR or HUF and labels in Czech, Slovak or Hungarian. Unlike the search tiles, the cz, sk and hu offer pages carry no sold figure, so `sold_count` is `null` on `/allegro/offer` for those markets; a product with no ratings has `rating: null` and `reviews: []`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def allegro(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/allegro/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find the catalog product (2 credits)
found = allegro("search", {"query": "lego 60510", "sort": "popularity"})
item = next(i for i in found["items"] if i["product_id"] and not i["is_sponsored"])
pid = item["product_id"]

# 2. Product summary: lowest price, offer count, buy box (2 credits)
product = allegro("product", {"product_id": pid})
print(product["title"], product["lowest_price"], product["currency"], product["offer_count"], "offers")

# 3. Every seller's offer, cheapest with delivery first (2 credits per page)
rows, page = [], 1
while True:
    res = allegro("product-offers", {"product_id": pid, "sort": "price_with_delivery_low_to_high", "page": page})
    rows += res["offers"]
    if page >= res["total_pages"] or page >= 3:
        break
    page += 1
rows = [o for o in rows if o["price_with_delivery"] is not None]
rows.sort(key=lambda o: o["price_with_delivery"])
for o in rows[:10]:
    print(o["price"], o["price_with_delivery"], o["condition"], o["seller"]["login"],
          "buy box" if o["is_featured"] else "", "sponsored" if o["is_sponsored"] else "")

# 4. Check the cheapest seller (2 credits)
fb = allegro("seller-feedback", {"login": rows[0]["seller"]["login"]})
print(fb["summary"]["positive_percent"], fb["summary"]["super_seller"], fb["summary"]["member_since"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live.

- **listing item** (search, category, seller `items[]`; product-offers `offers[]` adds `is_featured`) - `offer_id`, `product_id`, `title`, `url`, `image`, `price`, `currency`, `buy_now_price`, `price_with_delivery`, `free_delivery`, `delivery_text`, `condition`, `is_auction`, `auction_ends_in`, `discount_percent`, `lowest_price_30d`, `seller` {`id`, `login`, `super_seller`, `positive_feedback_percent`, `positive_feedback_count`, `is_business`}, `rating`, `rating_count`, `sold_count`, `sold_label`, `smart`, `offers_count`, `stock`, `placement` (`regular`, `promoted`, `sponsored`, `featured`), `is_sponsored`, `source` (`allegro`, `allegro_lokalnie`).
- **search** - `query`, `category_id`, `sort`, `applied_filters`, `total`, `total_pages`, `page`, `page_size` (60), `count`, `items[]`, `facets[]` {`id`, `label`, `values[]` {`label`, `param`, `value`, `count`, `count_label`, `selected`}}, `country`, `language`, `currency`.
- **offer** - `offer_id`, `product_id`, `title`, `url`, `product_url`, `status`, `condition`, `price`, `currency`, `buy_now`, `buy_now_price`, `original_price`, `lowest_price_30d`, `lowest_price_30d_note`, `discount_percent`, `discount_amount`, `price_with_delivery`, `stock`, `stock_label`, `sold_count`, `sold_label`, `is_auction`, `auction` {`current_price`, `min_next_bid`, `bid_step`, `ends_at`, `has_bids`, `bids_label`}, `parameters[]` {`name`, `value`}, `gtin`, `brand`, `description`, `images[]`, `breadcrumb[]`, `category`, `delivery[]` {`method`, `group`, `price`, `currency`, `eta_text`}, `handling_time`, `returns` {`days`, `label`}, `warranty` {`label`, `period`, `type`}, `seller` {`id`, `login`, `super_seller`, `positive_feedback_percent`, `positive_count`, `negative_count`, `is_business`, `company_name`}, `rating`, `rating_count`, `product_offers_count`, `smart`, `country`, `language`.
- **product** - `product_id`, `title`, `url`, `brand`, `gtin`, `parameters[]`, `images[]`, `breadcrumb[]`, `category`, `description`, `currency`, `lowest_price`, `offer_count`, `offer_highlights[]` {`label`, `subtitle`, `price`, `currency`, `kind`}, `featured_offer` {`offer_id`, `url`, `price`, `currency`, `original_price`, `lowest_price_30d`, `discount_percent`, `price_with_delivery`, `condition`, `is_auction`, `smart`, `stock`, `sold_count`, `sold_label`, `seller`}, `sold_count`, `sold_label`, `rating` {`average`, `count`, `distribution[]` {`stars`, `count`, `percent`}}, `aspects[]` {`label`, `sentiment`, `mentions`, `positive`, `negative`, `neutral`}, `review_count`, `reviews[]` {`id`, `rating`, `text`, `pros`, `cons`, `author`, `created_at`, `helpful_count`, `not_helpful_count`, `images[]`, `language`, `is_best`, `seller_login`}, `reviews_note`, `country`, `language`.
- **product-offers** - `product_id`, `title`, `sort`, `applied_filters`, `total`, `total_pages`, `page`, `page_size`, `count`, `facets[]`, `offers[]`, `country`, `language`, `currency`.
- **seller** - `login`, `seller` {`id`, `login`, `is_business`, `url`, `feedback_note`}, `is_active_seller`, `query`, `category`, `categories[]` {`id`, `name`, `count`, `slug`}, plus the search grid fields.
- **seller-feedback** - `login`, `summary` {`recommended`, `recommended_unique`, `not_recommended`, `not_recommended_unique`, `positive_percent`, `received`, `excluded`, `removed`, `member_since`, `super_seller`}, `total`, `total_pages`, `page`, `page_size` (20), `count`, `ratings[]` {`id`, `recommended`, `comment`, `comment_language`, `justifications[]`, `created_at`, `offers[]` {`offer_id`, `title`, `url`}, `excluded`, `exclusion_reason`}.
- **category** - `category` {`id`, `name`, `url`, `breadcrumb[]`, `subcategories[]`, `sibling_categories[]`}, `query`, plus the search grid fields.

## Guardrails

- Always give the currency (PLN, CZK, EUR, HUF) and the site. Never add up or compare prices across sites as if they were one market.
- Offer vs product: an `offer_id` (digits) is one seller's listing, a `product_id` (uuid) is a catalog product with many sellers. Do not send one where the other is expected.
- `lowest_price_30d` exists only where Allegro shows a discount: it is the lowest price of the 30 days before the discount (the EU price disclosure), shown with `discount_percent`. It is not a price history and it is `null` on undiscounted offers. For a real history, poll and store prices yourself.
- `price_with_delivery` is the price plus the cheapest delivery as the page shows it, and it is `null` where the page does not show it (every keyword-search tile in testing). Compare sellers on `/allegro/product-offers`, where it is filled.
- `sold_count` is the number of people who bought recently as Allegro displays it ("x people bought"), not units and not lifetime sales; `sold_label` is the site's text. It is `null` on auctions and on cz, sk and hu offer pages.
- Placement: `sponsored` (with `is_sponsored: true`) are paid ad slots and `promoted` is Allegro's promoted block; both can make up most of page 1. Report placement when the order of results matters, and never call the first result the cheapest or the best seller without sorting.
- Auctions: `price` is the current price; `auction_ends_in` on a search tile is the site's relative text ("24 minuty"); `auction.ends_at` on the offer is the exact time. There is no bid history, and this API cannot bid, snipe, buy or check out.
- Sellers: super-seller status, positive percent and member-since come from `/allegro/seller-feedback`. `is_business` separates business from private sellers; `company_name` is shown for business sellers only. Seller addresses, tax ids and contact details are not returned. Private sellers are individuals: use this to judge a seller, not to profile or contact a person.
- Reviews: the first 20 reviews shown on the product page, the star distribution and the aspects. Not the full review history, no verified-purchase flag, authors masked as Allegro shows them.
- Filters: only the parameters listed above are applied; `facets` are for reading counts and cannot be passed back as filters, and any other key in the body is ignored. `buying_format` and `deals` work on pl only. `applied_filters` echoes what the call sent; the site applied every filter in testing.
- Allegro Lokalnie offers inside pl results are flagged `source: "allegro_lokalnie"`; Allegro Lokalnie is not searched or read on its own.
- Not covered: search suggestions, bidding or buying, Allegro Smart! account data, seller sales revenue, price history, pickup-point locations, and Allegro's own Analytics data.
- Allegro's Terms & Conditions (section 10.10) say that downloading or using data available on Allegro requires Allegro's consent, and prohibit aggregating it, including by scraping, for use in another business. This is not legal advice; the user is responsible for checking the terms for their use case.
- Never fabricate prices, sold counts, stock, ratings or sellers. Only return what the API returned, with the offer or product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no `query` on search; neither or both of `offer_id` / `url`, `product_id` / `url` or `category_id` / `url`; an `offer_id` that is not 8-14 digits; a `product_id` that is not a uuid; a `url` that is not an Allegro offer, product or category link on allegro.pl, .cz, .sk or .hu (an Allegro Lokalnie link included); a `url` on one site with a different `country`; `buying_format` or `deals` on cz, sk or hu, or on `/product-offers`; a seller `category` that is not a slug; `min_price` above `max_price`; a `page` out of range; an unknown `sort`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such offer, product, category or seller (an unknown login included). Not-founds are charged (2 credits): take ids, logins and URLs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api).
- `502` means Allegro was temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Allegro is busy: wait the `Retry-After` seconds (5) and send it again. Not charged.

## SDKs

```bash
pip install scavio==0.51.0
npm install scavio@0.52.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.allegro.search({ query: "laptop", sort: "price_low_to_high", condition: "new" });
const { data: offer } = await scavio.allegro.offer({ offer_id: "18801787032" });
const { data: product } = await scavio.allegro.product({ product_id: "90d08230-e02a-4210-913d-d417453321b8" });
const { data: sellers } = await scavio.allegro.productOffers({ product_id: "90d08230-e02a-4210-913d-d417453321b8", sort: "price_with_delivery_low_to_high" });
const { data: shop } = await scavio.allegro.seller({ login: "Yupilo_pl", category: "komputery" });
const { data: ratings } = await scavio.allegro.sellerFeedback({ login: "Yupilo_pl" });
const { data: laptops } = await scavio.allegro.category({ category_id: "491", sort: "popularity" });
const { data: cz } = await scavio.allegro.search({ query: "notebook", country: "cz" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.allegro.search(...)`, `client.allegro.offer(...)`, `client.allegro.product(...)`, `client.allegro.product_offers(...)`, `client.allegro.seller(...)`, `client.allegro.seller_feedback(...)` and `client.allegro.category(...)`.

## MCP

The Scavio MCP server exposes all seven endpoints as tools: `search_allegro`, `get_allegro_offer`, `get_allegro_product`, `get_allegro_product_offers`, `get_allegro_seller`, `get_allegro_seller_feedback` and `get_allegro_category`. Allegro is opt-in: add `allegro` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.49.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,allegro"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/allegro-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api), [offer](https://scavio.dev/docs/allegro-offer?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api), [product](https://scavio.dev/docs/allegro-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api), [product offers](https://scavio.dev/docs/allegro-product-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api), [seller](https://scavio.dev/docs/allegro-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api), [seller feedback](https://scavio.dev/docs/allegro-seller-feedback?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api), [category](https://scavio.dev/docs/allegro-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api). Overview: [Allegro API](https://scavio.dev/allegro-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api).
