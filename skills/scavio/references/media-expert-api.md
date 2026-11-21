# Media Expert API - Black Week Prices, Omnibus Low, Store Stock

Read Media Expert's online store (mediaexpert.pl, Poland's consumer-electronics and home-appliance chain, prices in PLN): keyword search, category, brand, outlet, promotion and marketplace-seller lists, one product in full, store stock near a Polish city or postcode, stores, reviews, the category tree, the brand directory and search suggestions. All 13 endpoints return structured JSON at 1 to 3 credits per call, billed on what each call actually costs.

**The job this skill is for: Media Expert Black Week prices.** For any Media Expert product, the `price`, the `old_price` (the struck-through price), the `omnibus_lowest_30d` (the lowest price of the last 30 days that Media Expert shows next to a promotion, under the EU Omnibus Directive) and the `code_price` (the price with a discount code, with the `code` and its `valid_from` / `valid_to` dates), plus Media Expert's stock indicator and the pickup-in-1-hour flag at the stores nearest a Polish city, town or postcode, on a dated read.

Seven limits shape every answer, so say them plainly:
- **Credits are the actual cost of each call: 1 to 3.** Sorted and lazily loaded lists cost 3, a fully loaded list page 1; store-stock and categories cost 2. `credits_used` on every answer says what was charged. See Credits.
- **Store stock is Media Expert's stock indicator, not a unit count.** `stock_level` is a bucket (seen: 0, 2, 9, 20; 0 = none on the shelf). Never report "20 in stock" or "2 units". Report the bucket, `in_stock`, `collect_in_1h` and, for a store without it on the shelf, `order_to_store_day`.
- **Store stock takes the product id, never the offer id.** `items[].product_id` (up to 8 digits, `8128227`) is the input; `items[].offer_id` (9-10 digits, `2151746557`) answers `400` before anything is charged.
- **Marketplace items have no store stock.** Media Expert also sells marketplace sellers' offers (`seller.marketplace: true`, shipped by the seller). Store stock for one is a charged `400`, and reviews for one are a charged `404` (marketplace offers carry no Media Expert product code).
- **Lists are 30 per page by default (5, 10, 15, 20, 30 or 50), up to 100 pages**, and Media Expert stops counting a broad search at 5,000 (`total_capped: true`). Never call one page, or `total`, "all products". The price sorts are Media Expert's own order: they follow promotional and code prices, so they are approximate against `price`.
- **Reviews: Media Expert's own reviews, up to 100 per page, every review reachable**, 6 sorts, a star range and a verified-purchase filter, with `verified_purchase` and `incentivized` ("Opinia z akcji promocyjnej": the review came from a Media Expert promotional campaign) flags. No reviewer names.
- **Poland only, data in Polish.** One store (mediaexpert.pl), PLN, no `country` input. Names, specifications, labels, store names and review texts come back in Polish as Media Expert writes them: translate them for the user, never alter the values.

Media Expert has no public product, price or stock API. Approved marketplace sellers get an API key for their own offers in the Mirakl seller panel, and Media Expert's affiliate programme gives publishers tracking links, not a data feed. This skill reads the public mediaexpert.pl pages instead, with one Scavio key.

See also: for Allegro (Poland's largest marketplace) use `allegro-api`; for OLX Poland classifieds use `olx-api`; for UK store stock use `argos-stock-checker-api`; for US electronics use `best-buy-product-data` or `micro-center-api`; for prices across retailers use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Read Media Expert Black Week or Black Friday prices: the price, the old price, the Omnibus 30-day low and the code price with its code and dates, for one product, a search, a category, a brand or a promotion list
- Compare a Media Expert promotion against the lowest price of the last 30 days that Media Expert shows next to it
- Check whether a Media Expert product is on the shelf at the stores near a Polish city, town or postcode, and which ones can hand it over within an hour
- Read Media Expert's Black Weeks promotion lists and the products on one list
- Read Media Expert outlet groups and outlet prices
- Read a Media Expert marketplace seller's rating, shipping terms and offers
- Read Media Expert reviews sorted by newest, most helpful or rating, only 1-2 star reviews, or only reviews confirmed by purchase
- Find Media Expert stores in a city with opening hours, or the full store list
- Resolve category paths, brand slugs, filter values and search suggestions before a search

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 to 3 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, store-stock took under 1 second, reviews 2, suggestions 1, categories 2, stores 3, product 4, seller 4, search, category and brand 5, brands 6, outlet 7 and promotions 8. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/mediaexpert/search` | Products for a keyword, 30 per page, with the four prices, availability, seller, rating and the facets to filter by. Many single words are redirected by Media Expert to a category page (`redirected_to`) | 1 when Media Expert answers with a full category page and no sort; 3 otherwise |
| `POST /api/v1/mediaexpert/product` | One product by id or link: EANs, description, specifications, variants, delivery labels, instalment line, seller with rating, rating summary, related products | 1 |
| `POST /api/v1/mediaexpert/store-stock` | One product's stock indicator at the up to 40 Media Expert stores and pickup points nearest a Polish city, town or postcode, nearest first | 2 |
| `POST /api/v1/mediaexpert/stores` | Every Media Expert store (637 in the capture), the stores of one city, or one store's page, with address, hours and services | 1 |
| `POST /api/v1/mediaexpert/reviews` | One product's reviews by `sku`, `product_id` or link, up to 100 per page, with verified-purchase and promotional-campaign flags | 1 |
| `POST /api/v1/mediaexpert/category` | One category's products by path, with filters, sort and paging | 1 unsorted, 3 sorted or lazy |
| `POST /api/v1/mediaexpert/categories` | The category tree, or one category's subtree, with product and child counts | 2 |
| `POST /api/v1/mediaexpert/brands` | The brand directory (15,875 brands in the capture), by name text or first letter | 1 |
| `POST /api/v1/mediaexpert/brand` | One brand's products, optionally inside a category | 1 unsorted, 3 sorted or lazy |
| `POST /api/v1/mediaexpert/promotions` | The promotion lists Media Expert links (Black Weeks included), or one list's products | 1 for the lists; 1 or 3 for one list's products |
| `POST /api/v1/mediaexpert/outlet` | The outlet's groups, or one outlet group's subgroups or products | 1 unsorted, 3 sorted or lazy |
| `POST /api/v1/mediaexpert/seller` | A marketplace seller's rating, shipping terms and categories, and its offers | 1 unsorted, 3 sorted or lazy |
| `POST /api/v1/mediaexpert/suggestions` | Media Expert's search suggestions for a partial query, with search counts and category links | 1 |

## Credits

Billed on what each call actually costs, 1 to 3 credits; `credits_used` on every answer reports it, so read it rather than assuming.
- **1 credit:** product, stores, reviews (by `sku`, `product_id` or link), brands, suggestions, the promotion lists, and any list page Media Expert serves in full without a sort (the `telewizor` search redirected to the TV category, the `pralki` category, the `amica` brand, the outlet root and the `autobi` seller all cost 1 in the captures).
- **2 credits:** store-stock and categories.
- **3 credits:** any sorted list (`sort` other than `relevance`: Media Expert loads sorted lists lazily, so the rest of the page takes one more lookup), and a search or list page Media Expert loads lazily even without a sort (a search that is not redirected to a category, such as `air fryer`; some deeper pages).
- A not-found is charged what it spent: an unknown product is a `404` at 1 credit, an unknown product on store-stock a `404` at 2. A marketplace item on store-stock is a `400` charged 2 (it can only be detected after the stock call). Every other `400`, the offer id on store-stock included, is refused before anything is charged. Upstream failures (`502`, `503`) are not charged.
- To keep a crawl cheap: page lists without a sort and re-sort the rows yourself; look reviews up by `sku` (the list items carry it).

## Market

One store: mediaexpert.pl (Poland), Polish, prices in PLN as numbers (`4199`, `3399.99`). There is no `country` input and no other language. Locations for store-stock are Polish cities and towns in any case, with or without Polish accents (`Warszawa`, `Kraków`, `Krakow`, `Sanok`), or a postcode as two digits, a hyphen and three digits (`00-950`). Media Expert's operator is TERG S.A., a family-controlled Polish company; it reported 618 Media Expert stores at the end of March 2026 (dlahandlu.pl), and the site's store list held 637 entries on 2026-11-21.

## Prices: the Black Week fields

Every list item and product carries:

| Field | Meaning |
|---|---|
| `price` | The listed price, PLN |
| `old_price` | Media Expert's struck-through price, as shown (`null` when the page shows none) |
| `omnibus_lowest_30d` | The lowest price of the last 30 days that Media Expert shows next to a promotion under the EU Omnibus Directive ("Najniższa cena z 30 dni przed obniżką"), as shown. `null` when the page shows none: it appears next to a reduction or code price, not on every product |
| `code_price` | `{price, code, valid_from, valid_to}`: the price with a discount code, the code to enter and its validity window (ISO with the Polish offset), or `null` |
| `discount_shown` | `{amount, percent}`: Media Expert's own discount figure, where it shows one |
| `discount_percent` | Computed by Scavio: from `old_price` to `price`, or with a code price from `price` to the code price (the lowest price you can pay) |

- Report how the prices relate descriptively, from the numbers: "the code price is 1,000 zł below the 30-day low Media Expert shows". Never call a discount fake, real or misleading, and never call a price "the lowest price" on your own authority: `omnibus_lowest_30d` is Media Expert's figure.
- `discount_shown` and `discount_percent` can differ because they measure from different prices. In the `telewizor` capture the LG 65QNED72B6B read `price` 3399.99, `omnibus_lowest_30d` 2999 and `code_price` 1999 (code `R1911-251126`, valid to 2026-11-25): Media Expert showed 1,000 zł / 33% (the gap from the 30-day low to the code price), while `discount_percent` read 41 (from the listed price). Quote which one you use.
- Code prices have dates: quote `valid_to` with every code price and re-read after it passes. In the same capture the TCL 98A400 read `price` 9999, `omnibus_lowest_30d` 9999 and `code_price` 5999 with code `ME2111-061226` valid 2026-11-21 to 2026-12-06.
- Other promotions are list filters, not price fields: the `promotions` facet carries Media Expert's own promotion names (`Cena z kodem` = price with a code, `Black Weeks`, cashback and multi-buy offers such as "Drugi -30% lub piąty za 1 zł!" = second one 30% off or the fifth for 1 zł). Filter with their `filter` values; never compute a multi-buy price.
- `installments` on a product is the instalment line the page shows (`monthly`, `months`, `interest_rate`), not a credit offer or its terms. There are no checkout prices.
- Media Expert's own Black Friday page (captured 2026-11-21) says Black Friday at Media Expert starts early with Black Weeks and that the traditional date is 27 November; its dated code offers ran to 01.12.2026. Quote dates from `code_price.valid_to` and the lists, not from memory.

## Store stock

`/mediaexpert/store-stock` takes `product_id` (items[].product_id), `location` (a Polish city, town or postcode) and optionally `limit` (1-40 stores, default 40).

- The answer: `product_id`, `location`, `count`, `in_stock_count`, `collect_in_1h_count` and `stores[]`, nearest first: `store_id`, `name`, `code`, `type` (`store`, or `pickup_point`: a Media Expert pickup point, "Punkt Odbioru Towaru"), `address` {`street`, `house_number`, `apartment`, `postcode`, `city`, `province`}, `phone`, `latitude`, `longitude`, `distance_km`, `hours`, `stock_level`, `in_stock`, `collect_in_1h`, `button_label`, `order_to_store_day`, `display_unit`, `availability`, `availability_label`.
- `stock_level` is Media Expert's stock indicator, a bucket and not a unit count (seen: 0, 2, 9, 20; 0 = none on the shelf). Report it as "Media Expert's indicator reads 20", never as "20 in stock".
- `collect_in_1h` is Media Expert's "Odbierz za godzinę" (collect in an hour): the store can have it ready within an hour. `button_label` is the button the page shows (`Odbierz za godzinę`, or `Do koszyka` = add to basket).
- `order_to_store_day` is set where the product is not on the shelf: the day an order reaches that store, as Media Expert words it (`w poniedziałek` = on Monday). Translate it; never turn it into a date.
- `display_unit` is Media Expert's display-model flag as given.
- The 40 stores are the nearest ones, not every store in a city: in a small town the list reaches far out. In the capture, Warszawa returned 40 stores from 4.58 to 42.08 km, Sanok 40 from 0.49 to 114.38 km.
- The product page's own `delivery.collect_in_1h` and the list items' `in_store` are page-level flags: use store-stock for availability at a store. In the capture the iPhone 17 product page read `delivery.collect_in_1h: false` while 39 of the 40 Warsaw-area stores read `collect_in_1h: true`, and a marketplace item in a seller list read `in_store: true`.

## Workflow

1. **Find the product:** `/mediaexpert/search` with `query` (Polish terms work best: `telewizor`, `pralka`, `iphone 17`), or `/mediaexpert/category` with a `category` path from `/mediaexpert/categories`. Each item has `product_id`, `sku`, `ean`, the four price fields and `seller.marketplace`.
2. **Narrow:** send `filters` with `facets[].values[].filter` values from an earlier answer (`promocje_cena-z-kodem`, `promocje_black-weeks`, `samsung`, `pojemnosc-kg_od-10-kg`). Several filters narrow together. There is no price-range filter: filter by price on your side.
3. **Black Weeks:** `/mediaexpert/promotions` with `{"black_weeks": true}` for the lists, then `{"list": "<lists[].list>"}` for one list's products.
4. **One product in full:** `/mediaexpert/product` with `product_id` or `url`: specifications, variants (each colour or memory size has its own `product_id`: check stock per variant), delivery labels, the seller and its rating.
5. **Stock near a place:** `/mediaexpert/store-stock` with the `product_id` and a `location`; call it once per city (2 credits each). Skip marketplace items (`seller.marketplace: true`).
6. **Reviews:** `/mediaexpert/reviews` with the item's `sku` (1 credit), `sort`, `rating_min` / `rating_max`, `verified` and `limit` up to 100.
7. **Watching prices or stock:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at` time; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`), outlet (`/outlet`), seller (`/seller`), promotion list (`/promotions` with `list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Search text (1-200 chars). Polish works best |
| `category_id` | string or integer | none | Search only: narrow to one category id (`categories[].category_id`) |
| `category` | string | category: required | A category path (`categories[].path`, `breadcrumbs[].path`, e.g. `agd/pralki-i-suszarki/pralki`) or its mediaexpert.pl link. Brand: only the brand inside this category. Outlet: an outlet group path (`subcategories[].path`); without it, the outlet's groups |
| `brand` | string | brand: required | `brands[].slug` (`samsung`, `amica`) or its mediaexpert.pl link |
| `seller` | string | seller: required | A marketplace seller: `items[].seller.slug` (`autobi`) or its mediaexpert.pl/sprzedawca-marketplace/... link |
| `list` | string | promotions: one of | A promotion list: `lists[].list` (`32975-logitech-black-weeks-czas-na-nowy-poziom-sprzetu`) or its mediaexpert.pl/lista,... link |
| `filters` | string or array | none | Category, brand and outlet: up to 10 `facets[].values[].filter` values (brand, promotions, Top Hit, instalments, energy class, specifications, marketplace seller). Facets whose `filter` is `null` (availability, rating) cannot be sent |
| `sort` | string | `relevance` | `relevance` (Media Expert's own order), `price_asc`, `price_desc` (Media Expert's price order: approximate, re-sort the page for a strict order), `rating`, `newest`, `name_asc`, `name_desc`, `brand_asc`, `brand_desc`, `discount`. Any sort costs 3 credits |
| `page` | integer | 1 | 1-100; `total_pages` says how deep the list goes |
| `limit` | integer | 30 | Products per page: 5, 10, 15, 20, 30 or 50 |

### Promotion lists (`/promotions` without `list`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `black_weeks` | boolean | false | Only Black Weeks / Black Friday lists |
| `query` | string | none | Only lists whose name or reference contains this text |

`sort`, `page` and `limit` apply to one list only (send `list`).

### Product (`/product`) and store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string or integer | product: one of; store-stock: required | `items[].product_id`, up to 8 digits (`8128227`). An offer id (`items[].offer_id`, 9-10 digits) answers `400` |
| `url` | string | product: one of | A mediaexpert.pl product link. Send exactly one of `product_id`, `url` |
| `location` | string | store-stock: required | A Polish city or town (`Warszawa`, `Kraków`, `Sanok`) or a postcode (`00-950`) |
| `limit` | integer | 40 | Store-stock: stores, nearest first, 1-40 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | one of | Media Expert's product code: `items[].sku` (`709727`) |
| `product_id` / `url` | | one of | The product id or link (the product page names the sku). Send exactly one of `sku`, `product_id`, `url` |
| `sort` | string | `most_helpful` | `most_helpful` (Media Expert's own order), `least_helpful`, `newest`, `oldest`, `highest_rating`, `lowest_rating` |
| `rating_min` / `rating_max` | integer | 1 / 5 | A star range. With a range, Media Expert gives no total: `total` is `null` and `has_more` means a full page came back |
| `verified` | boolean | false | Only reviews Media Expert marks as confirmed by purchase |
| `page` | integer | 1 | Every review is reachable: `page * limit` up to `total` |
| `limit` | integer | 10 | 1-100 per page |

### Stores (`/stores`), categories (`/categories`), brands (`/brands`), suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `city` | string | stores: optional | Only the stores in this city, as Media Expert writes it (case and accents do not matter). Without `city` or `store`: every store |
| `store` | string | stores: optional | One store's page: `stores[].store` (`warszawa/al-jerozolimskie-148`) or its mediaexpert.pl/sklepy/... link. Not with `city` |
| `category` / `category_id` | string / integer | categories: optional | Start the tree at this path (`agd`) or id (`12900`), not both |
| `depth` | integer | 2 (3 from a category) | Categories: levels, 1-6. `child_count` says what lies below a cut |
| `query` | string | brands: optional; suggestions: required | Brands whose name contains this text / what the shopper has typed so far |
| `letter` | string | none | Brands starting with this letter or digit |
| `page`, `limit` | integer | 1, 100 | Brands: 1-1,000 per page |
| `limit` | integer | 8 | Suggestions: 1-10 |

## Examples

### Store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/mediaexpert/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "8128227", "location": "Warszawa"}'
```

Captured `data` (2026-11-21, 2 credits; 3 of 40 stores shown, `latitude`, `longitude` and all but Monday's `hours` dropped):

```json
{
  "product_id": 8128227,
  "location": "Warszawa",
  "count": 40,
  "in_stock_count": 39,
  "collect_in_1h_count": 39,
  "stores": [
    {
      "store_id": 2033,
      "name": "Media Expert Warszawa, Al. Jerozolimskie 148",
      "code": "S1062",
      "type": "store",
      "address": { "street": "Al.Jerozolimskie", "house_number": "148", "apartment": null, "postcode": "02-326", "city": "Warszawa", "province": "mazowieckie" },
      "phone": "884 228 605",
      "distance_km": 4.58,
      "hours": [{ "day": "monday", "open": "10:00", "close": "21:00" }],
      "stock_level": 20,
      "in_stock": true,
      "collect_in_1h": true,
      "button_label": "Odbierz za godzinę",
      "order_to_store_day": null,
      "display_unit": false,
      "availability": "available",
      "availability_label": "Dostępny"
    },
    {
      "store_id": 1552,
      "name": "Media Expert Warszawa, Ul Połczyńska 121",
      "code": "S752",
      "type": "store",
      "address": { "street": "Połczyńska", "house_number": "121", "apartment": null, "postcode": "01-303", "city": "Warszawa", "province": "mazowieckie" },
      "phone": "608 481 098",
      "distance_km": 9.12,
      "stock_level": 2,
      "in_stock": true,
      "collect_in_1h": true,
      "button_label": "Odbierz za godzinę",
      "order_to_store_day": null,
      "display_unit": false,
      "availability": "available",
      "availability_label": "Dostępny"
    },
    {
      "store_id": 1300,
      "name": "Punkt Odbioru Towaru Media Expert Otwock, ul. Kupiecka 2",
      "code": "S668",
      "type": "pickup_point",
      "address": { "street": "Kupiecka", "house_number": "2", "apartment": null, "postcode": "05-400", "city": "Otwock", "province": "mazowieckie" },
      "phone": "22 112 24 85",
      "distance_km": 21.63,
      "stock_level": 0,
      "in_stock": false,
      "collect_in_1h": false,
      "button_label": "Do koszyka",
      "order_to_store_day": "w poniedziałek",
      "display_unit": false,
      "availability": "available",
      "availability_label": "Dostępny"
    }
  ]
}
```

Read it as: for the iPhone 17 256 GB in black (8128227), the 40 nearest locations ran from 4.58 to 42.08 km; 39 had it on the shelf and could have it ready within an hour. Media Expert's indicator read 20 at 15 of them, 9 at 18, 2 at 6 and 0 at 1, the Otwock pickup point, where an order would arrive "w poniedziałek" (on Monday). Near Sanok, a small town, the same product returned 40 locations from 0.49 km (the Sanok pickup point, indicator 0, order arrives on Monday) and 2.16 km (the Sanok store, indicator 2, ready within an hour) out to 114.38 km.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/mediaexpert/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "telewizor"}'
```

Captured `data` (2026-11-21, 1 credit: Media Expert redirected the search to its TV category; 2 of 30 items shown, `image` and `facets` omitted):

```json
{
  "query": "telewizor",
  "category_id": null,
  "redirected_to": { "type": "list", "path": "telewizory-i-rtv/telewizory", "url": "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory" },
  "sort": "relevance",
  "page": 1,
  "page_size": 30,
  "total": 1017,
  "total_capped": false,
  "total_pages": 34,
  "has_more": true,
  "count": 30,
  "currency": "PLN",
  "items": [
    {
      "product_id": 13166987,
      "offer_id": 2155201335,
      "sku": "2142551",
      "ean": "8806096732038",
      "name": "Telewizor LG 65QNED72B6B 65\" MINILED 4K WebOS TV HDMI 2.1",
      "brand": "LG",
      "model": "65QNED72B6B.AEU",
      "url": "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory/telewizor-lg-65qned72b6b-65-miniled-4k-webos-tv",
      "price": 3399.99,
      "old_price": null,
      "omnibus_lowest_30d": 2999,
      "code_price": { "price": 1999, "code": "R1911-251126", "valid_from": "2026-11-19T00:00:00+01:00", "valid_to": "2026-11-25T23:59:00+01:00" },
      "discount_percent": 41,
      "discount_shown": { "amount": 1000, "percent": 33 },
      "currency": "PLN",
      "availability": "available",
      "availability_label": "Dostępny od ręki",
      "rating": null,
      "review_count": 0,
      "seller": { "id": "0", "name": "Media Expert", "slug": null, "marketplace": false },
      "in_store": true,
      "energy_class": "E",
      "warranty_months": 24,
      "top_product": true,
      "outlet": null,
      "category": { "category_id": 12798, "name": "Telewizory", "path": "telewizory-i-rtv/telewizory" },
      "labels": ["Darmowa dostawa"]
    },
    {
      "product_id": 9696414,
      "offer_id": 2153018122,
      "sku": "2119701",
      "ean": "6942351433790",
      "name": "Telewizor HISENSE 65U77SE 65\" QD-Mini LED 4K 144 Hz VRR VIDAA Dolby Atmos Dolby Vision HDMI 2.1",
      "brand": "HISENSE",
      "model": "65U77SE",
      "url": "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory/telewizor-hisense-65u77se-65-qd-mini-led-4k-144hz-vrr-vidaa-dolby-atmos-dolby-vision-hdmi-2-1",
      "price": 3999.99,
      "old_price": 4499,
      "omnibus_lowest_30d": 4099,
      "code_price": null,
      "discount_percent": 11,
      "discount_shown": null,
      "currency": "PLN",
      "availability": "available",
      "availability_label": "Dostępny od ręki",
      "rating": null,
      "review_count": 0,
      "seller": { "id": "0", "name": "Media Expert", "slug": null, "marketplace": false },
      "in_store": true,
      "energy_class": "E",
      "warranty_months": 24,
      "top_product": true,
      "outlet": null,
      "category": { "category_id": 12798, "name": "Telewizory", "path": "telewizory-i-rtv/telewizory" },
      "labels": ["Darmowa dostawa"]
    }
  ]
}
```

On this page 17 of the 30 TVs carried `omnibus_lowest_30d`, 13 a `code_price` and 4 an `old_price`. The Hisense 65U77SE shows the other pattern: a struck-through price of 4,499 zł above a 30-day low of 4,099 zł, with the price at 3,999.99 zł. `availability_label` "Dostępny od ręki" means available right away; `labels` "Darmowa dostawa" means free delivery. The answer carried 42 facets, among them `promotions` (`Cena z kodem` 184, `Black Weeks` 1, `70 zł rabatu za wydane 500 zł` 349), `producer` (the brands: `HISENSE` 146, `LG` 98) and TV-specific ones such as screen size and refresh rate. `/category` with `{"category": "agd/pralki-i-suszarki/pralki"}` (washing machines) returned 626 products in 21 pages (1 credit), 25 of the first 30 with a code price, the first a Hisense WF5I1045BWQ at 2,999.99 zł with a 30-day low of 2,999 zł and a code price of 2,799.99 zł (code `RW2210-301126`).

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/mediaexpert/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "8128227"}'
```

Captured `data` (2026-11-21, 1 credit; trimmed: `description`, `images`, `key_attributes`, `specifications`, `breadcrumbs`, `related`, two of the four `labels` and the feature averages dropped):

```json
{
  "requested": "8128227",
  "product_id": 8128227,
  "offer_id": 2151746557,
  "sku": "2095223",
  "ean": "0195950643459",
  "name": "Smartfon APPLE iPhone 17 5G 256GB 6.3\" 120Hz Czarny",
  "brand": "APPLE",
  "model": "IPHONE 17",
  "url": "https://www.mediaexpert.pl/smartfony-i-zegarki/smartfony/smartfon-apple-iphone-17-5g-black-256gb",
  "price": 4199,
  "old_price": 4399,
  "omnibus_lowest_30d": 4399,
  "code_price": null,
  "discount_percent": 5,
  "discount_shown": { "amount": 200, "percent": 5 },
  "currency": "PLN",
  "availability": "available",
  "availability_label": "Dostępny od ręki",
  "rating": 4.9,
  "review_count": 216,
  "seller": { "id": "0", "name": "Media Expert", "slug": null, "marketplace": false, "url": null, "rating": null },
  "in_store": true,
  "energy_class": "A",
  "warranty_months": 24,
  "top_product": false,
  "outlet": false,
  "category": { "category_id": 13170, "name": "Smartfony", "path": "smartfony-i-zegarki/smartfony" },
  "labels": ["Darmowa dostawa", "Zanim zwrócisz urządzenie, przywróć je do ustawień fabrycznych."],
  "marketplace": false,
  "eans": ["0195950643459", "2995463198426"],
  "variants": [
    { "name": "Kolor", "options": [{ "value": "Czarny", "product_id": 8128227 }, { "value": "Biały", "product_id": 8128271 }, { "value": "Gołębi", "product_id": 8128219 }, { "value": "Lawendowy", "product_id": 8128215 }, { "value": "Szałwia", "product_id": 8128207 }] },
    { "name": "Pamięć", "options": [{ "value": "256", "product_id": 8128227 }, { "value": "512", "product_id": 8128211 }] }
  ],
  "delivery": { "delivery_label": "w poniedziałek", "store_pickup_label": "w poniedziałek", "parcel_locker_label": "2026-11-23", "collect_in_1h": false, "delivery_info": "Dostępny", "min_shipping_price": null },
  "installments": { "monthly": 419.9, "months": 10, "interest_rate": 0, "currency": "PLN" },
  "preorder": false,
  "renewed": false,
  "product_set": false,
  "first_listed_at": "2025-09-09 21:13:20",
  "rating_summary": { "average": 4.87, "recommendations": 212, "verified_purchases": 195 }
}
```

The struck-through price (4,399 zł) equalled the 30-day low here, and Media Expert showed 200 zł / 5% off. `variants` are colour (`Kolor`: black, white, dove blue, lavender, sage) and memory (`Pamięć`), each option with its own `product_id`. `delivery` labels are Media Expert's words ("w poniedziałek" = on Monday). `rating_summary.features` held six averages, such as `Wydajność` (performance) 4.94 and `Czas pracy na baterii` (battery life) 4.68. A **marketplace** product carries `marketplace: true` and `seller` {`id`, `name`, `slug`, `marketplace`, `url`, `rating` {`total`, `recommended`, `not_recommended`, `recommended_percent`}}.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/mediaexpert/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "709727", "sort": "newest"}'
```

Captured `data` (2026-11-21, 1 credit; 1 of 10 reviews shown, its `feature_ratings` trimmed to 2 of 7):

```json
{
  "sku": "709727",
  "product_id": null,
  "sort": "newest",
  "rating_min": 1,
  "rating_max": 5,
  "verified_only": false,
  "page": 1,
  "limit": 10,
  "total": 658,
  "total_pages": 66,
  "has_more": true,
  "count": 10,
  "average_rating": 4.89,
  "recommendations": 647,
  "verified_purchases": 565,
  "features": [],
  "reviews": [
    {
      "id": "01M7CR7RGZTX2FJ2YS0J3XJ2QQ",
      "rating": 4.6,
      "title": "Zadowolona klientka",
      "text": "Różnorodność programów pozwala dobrać łatwo i wygodnie tryb prania, ładnie i cicho pierze. Mam dostęp do krótkiego cyklu i na tym mi zależało ponieważ ubrania na długim cyklu bardzo się spierają i niszczą a w tym przypadku mogę tego uniknąć i mogę użytkować ubrania dłużej i wyglądać jak w nowych przez dłuższy czas.",
      "created_at": "2026-11-14 11:04:21",
      "verified_purchase": true,
      "incentivized": false,
      "incentive_label": null,
      "feature_ratings": [{ "name": "Pojemność", "rating": 5 }, { "name": "Jakość prania", "rating": 5 }],
      "helpful_yes": 0,
      "helpful_no": 0,
      "store_reply_count": 0
    }
  ]
}
```

On this page all 10 reviews were confirmed by purchase and 1 was flagged `incentivized` with `incentive_label` "Opinia z akcji promocyjnej" (a review from a Media Expert promotional campaign). A review `rating` can be a decimal (4.6 here): it is the rating Media Expert shows for that review, next to the reviewer's per-feature stars in `feature_ratings`. Translate the Polish text for the user (this one praises the choice of programmes, quiet washing and the short cycle); never alter the quoted text. `store_reply_count` is how many replies the store posted, not their text.

### Stores, categories, brands, promotions, outlet, seller and suggestions

- `/stores` with `{"city": "Kraków"}`: 9 of `total_stores` 637, such as `krakow/stary-trakt-wegrzce-4` (postcode 32-086) with `hours` by weekday, `closed_today`, `next_open_day` and `services`. `hours` is Media Expert's weekly schedule; `closed_today` and `next_open_day` are its calendar. In the Saturday 2026-11-21 capture `next_open_day` read 2026-11-23, the Monday, although `hours` lists Sunday hours: Poland restricts Sunday trading, so check `next_open_day` before telling a shopper a store is open on a Sunday. `{"store": "warszawa/al-jerozolimskie-148"}` returns one store's page with `phone`, `events` and `alerts` too. No stock here: use store-stock.
- `/categories` (no input, 2 credits): 23 top-level nodes and 464 nodes at depth 2. The first node, `Promocje`, links the promotions page (`product_count` 0); the departments run from `TV, Audio i RTV`, `AGD` (large appliances) and `Smartfony i zegarki` to `Outlet`. `path` is the input of `/category`.
- `/brands` with `{"query": "sams"}`: 5 matches of 15,875 brands (`samsung`, `samsonite` ...) plus Media Expert's `featured` brands. `slug` is the input of `/brand`; `{"brand": "amica"}` returned 724 products in 25 pages.
- `/promotions` with `{"black_weeks": true}`: 3 Black Weeks lists of the 20 the promotions page linked, such as `32975-logitech-black-weeks-czas-na-nowy-poziom-sprzetu` ("Zyskaj rabat przy zakupie kierownicy w promocji": a discount on a steering wheel bought on promotion). Send `list` for its products.
- `/outlet` (no input): 14 outlet groups (3,396 products), such as `outlet/outlet-agd` (243) and `outlet/outlet-smatrfony-i-telefony` (493). On outlet products `old_price` is the price before the outlet price.
- `/seller` with `{"seller": "autobi"}`: AUTOBI, a marketplace seller with `min_shipping_price` 14.9, `delivery_info` "Wysyłka w 2 dni robocze" (ships in 2 working days) and 189,551 offers (`total_capped: true`, 100 pages of 30 reachable). Its `rating` read `total` 0: a seller with no ratings yet reads 0, not `null`, so say "no ratings yet", never "0% recommended". Its items carry `availability: "advance"` with "Marketplace - Wysyłka w 2 dni robocze".
- `/suggestions` with `{"query": "pral"}`: 8 phrases from `pralka` (65,119 searches, Media Expert's count) down to `pralka i suszarka`, and 7 category links such as `agd/pralki-i-suszarki/pralki`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def me(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/mediaexpert/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. The code prices in a category, page by page, unsorted (1 or 3 credits per page: read credits_used)
rows, page = [], 1
while page <= 3:  # raise the cap and follow has_more for the whole list
    res = me("category", {"category": "agd/pralki-i-suszarki/pralki", "filters": ["promocje_cena-z-kodem"], "page": page})
    d = res["data"]
    for i in d["items"]:
        cp = i["code_price"] or {}
        rows.append((res["fetched_at"], i["product_id"], i["name"], i["price"], i["old_price"],
                     i["omnibus_lowest_30d"], cp.get("price"), cp.get("code"), cp.get("valid_to"), i["seller"]["marketplace"]))
    if not d["has_more"]:
        break
    page += 1
print(len(rows), "items,", sum(1 for r in rows if r[6] is not None and r[5] is not None and r[6] < r[5]), "with a code price below the 30-day low shown")

# 2. One product's stock indicator near three places (2 credits each; never for marketplace items)
for place in ("Warszawa", "Kraków", "Sanok"):
    d = me("store-stock", {"product_id": "8128227", "location": place, "limit": 10})["data"]
    for s in d["stores"]:
        print(place, s["name"], s["type"], s["distance_km"], "indicator", s["stock_level"], "1h" if s["collect_in_1h"] else s["order_to_store_day"])

# 3. Only 1-2 star reviews confirmed by purchase, 100 per page (1 credit per page)
low = me("reviews", {"sku": "709727", "rating_max": 2, "verified": True, "limit": 100})["data"]
for rv in low["reviews"]:
    print(rv["rating"], rv["created_at"], rv["incentivized"], rv["text"][:80])

# Store each answer with fetched_at and run this on a schedule: that stored series is
# your price and stock history (Media Expert shows only the 30-day low).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached.

- **item** (search, category, brand, outlet, seller, promotion list) - `product_id`, `offer_id`, `sku`, `ean`, `name`, `brand`, `model`, `url`, `image`, `price`, `old_price`, `omnibus_lowest_30d`, `code_price` {`price`, `code`, `valid_from`, `valid_to`}, `discount_percent`, `discount_shown` {`amount`, `percent`}, `currency` (PLN), `availability` (`available`, `preorder`, `not_available`, or `advance` for marketplace shipping), `availability_label` (as shown), `rating`, `review_count`, `seller` {`id`, `name`, `slug`, `marketplace`}, `in_store`, `energy_class`, `warranty_months`, `top_product`, `outlet`, `category` {`category_id`, `name`, `path`}, `labels` (Media Expert's notes under the price, on full list pages and products).
- **lists** (category, brand, outlet, promotion list) - `kind` (`products`, or `subcategories` for a parent page: `subcategories[]` {`category_id`, `name`, `path`, `url`, `product_count`}), `title`, `breadcrumbs`, `sort`, `page`, `page_size`, `total` (Media Expert's count, stopping at 5,000 for broad searches), `total_capped`, `total_pages` (up to 100), `has_more`, `count`, `currency`, `items[]`, `facets[]` {`code`, `name`, `values[]` {`name`, `count`, `filter`}}. Search adds `query`, `category_id`, `redirected_to` {`type`, `path`, `url`}. Category, brand and outlet echo their inputs (`category`, `brand`, `filters`); a promotion list adds `list`, `list_id`, `url`.
- **product** - the item fields plus `requested`, `marketplace`, `eans`, `description` (plain text), `images`, `key_attributes[]` {`name`, `values`}, `specifications[]` {`group`, `attributes[]` {`name`, `values`}}, `variants[]` {`name`, `options[]` {`value`, `product_id`}}, `delivery` {`delivery_label`, `store_pickup_label`, `parcel_locker_label`, `collect_in_1h`, `delivery_info`, `min_shipping_price`}, `installments` {`monthly`, `months`, `interest_rate`, `currency`}, `seller` (+ `url`, `rating`), `preorder`, `renewed`, `product_set`, `first_listed_at`, `rating_summary` {`average`, `recommendations`, `verified_purchases`, `features[]` {`name`, `average`}}, `breadcrumbs`, `related[]` {`product_id`, `name`, `url`, `image`}.
- **store-stock** - `product_id`, `location`, `count`, `in_stock_count`, `collect_in_1h_count`, `stores[]` (see Store stock).
- **stores** - `city`, `total_stores`, `count`, `stores[]` {`store_id`, `store`, `url`, `address` {`street`, `house_number`, `apartment`, `postcode`, `city`}, `latitude`, `longitude`, `hours[]` {`day`, `open`, `close`}, `closed_today`, `next_open_day`, `services`}. One store: the same fields plus `phone`, `events`, `alerts`.
- **reviews** - `sku`, `product_id`, `sort`, `rating_min`, `rating_max`, `verified_only`, `page`, `limit`, `total`, `total_pages`, `has_more`, `count`, `average_rating`, `recommendations`, `verified_purchases`, `features[]` {`name`, `average`}, `reviews[]` {`id`, `rating`, `title`, `text`, `created_at`, `verified_purchase`, `incentivized`, `incentive_label`, `feature_ratings[]` {`name`, `rating`}, `helpful_yes`, `helpful_no`, `store_reply_count`}.
- **categories** - `category`, `depth`, `count`, `node_count`, `categories[]` {`category_id`, `name`, `path`, `url`, `product_count`, `child_count`, `children`}.
- **brands** - `query`, `letter`, `total_brands`, `matches`, `page`, `limit`, `has_more`, `count`, `featured[]`, `brands[]` {`brand_id`, `name`, `slug`, `url`}.
- **promotion lists** - `query`, `black_weeks`, `total_lists`, `count`, `lists[]` {`list`, `list_id`, `name`, `url`, `black_weeks`}.
- **seller** - `seller` {`seller_id`, `name`, `slug`, `url`, `rating` {`total`, `recommended`, `not_recommended`, `recommended_percent`}, `min_shipping_price`, `delivery_info`, `categories[]` {`category_id`, `name`, `product_count`}} and the list fields with its offers.
- **suggestions** - `query`, `count`, `suggestions[]` {`phrase`, `searches`, `average_results`}, `categories[]` {`name`, `path`, `url`}.

## Guardrails

- Store stock is Media Expert's stock indicator per store, never a unit count. Report it as what Media Expert showed at `fetched_at` for the nearest stores the answer returned (up to 40), never as every store in a city or as guaranteed stock.
- Prices: quote `price`, `old_price`, `omnibus_lowest_30d` and `code_price` as Media Expert shows them, with the code's `valid_to`. `omnibus_lowest_30d` is the lowest price of the last 30 days that Media Expert shows next to a promotion (EU Omnibus Directive). Describe how the prices relate from the numbers; never call a discount fake, real or misleading, and never call a price the lowest on your own authority. Say which discount figure you quote (`discount_shown` is Media Expert's, `discount_percent` is computed by Scavio).
- Lists: 30 per page by default, up to 100 pages; never call one page "all products" or present `total` as what was returned. When `total_capped` is true say "5,000 or more". Price sorts are approximate: re-sort the page for a strict order.
- Sellers: `seller.marketplace: true` items are sold and shipped by a marketplace seller, never stocked in Media Expert stores. Never invent a seller name or rating.
- Reviews: no reviewer names or identities are returned; never try to identify a reviewer. Flag `incentivized` reviews (from a Media Expert promotional campaign) and say whether a review is a confirmed purchase.
- Polish data: translate names, labels and review texts for the user and keep the original values in quotes and outputs.
- Not available: Q&A (Media Expert has none), leaflets, price history (poll and store), unit counts, checkout prices, credit or instalment terms beyond the line the page shows, other countries or languages. This API cannot reserve, add to basket or buy.
- Terms: Scavio does not collect or store Media Expert data: each call fetches the public Media Expert page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Media Expert's terms of service cover how its service may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Media Expert product photos or logos; link products by `url` instead.
- Never fabricate prices, codes, stock indicators, stores, reviews or ratings. Only return what the API returned, with the currency, the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged (with one exception below): an offer id (9-10 digits) where a product id is expected, a product id over 8 digits, a `url` that is not a mediaexpert.pl link, both or neither of `product_id` / `url` (or `sku` / `product_id` / `url` on reviews, `city` / `store` on stores, `category` / `category_id` on categories), a `location` that is neither a Polish place name nor an `NN-NNN` postcode, a `limit` that is not a Media Expert page size (5, 10, 15, 20, 30, 50), a `page` above 100, an unknown `sort`, `rating_min` above `rating_max`, more than 10 `filters` or a value that is not a filter, `sort` / `page` / `limit` on the promotion lists without `list`, `query` / `black_weeks` with `list`.
- The exception: store-stock for a marketplace item answers `400` ("This product is sold and shipped by a marketplace seller: Media Expert stores do not stock it ...") and is charged 2 credits, because it is only known after the stock call. Check `seller.marketplace` first.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged what it spent: "No Media Expert product with this id or link (or the product is no longer listed on mediaexpert.pl).", "No Media Expert stock answer for this product id (send items[].product_id, not the offer id).", "This offer has no Media Expert product code (marketplace offers carry none), so Media Expert holds no reviews for it.", and the same for an unknown store, category path, brand, promotion list or seller. Take ids, paths and slugs from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api).
- `502` means Media Expert data was temporarily unavailable ("Media Expert is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Media Expert is busy ("Media Expert is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.73.0
npm install scavio@0.74.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.mediaexpert.search({ query: "telewizor" });
const { data: product } = await scavio.mediaexpert.product({ product_id: "8128227" });
const { data: stock } = await scavio.mediaexpert.storeStock({ product_id: "8128227", location: "Warszawa" });
const { data: stores } = await scavio.mediaexpert.stores({ city: "Kraków" });
const { data: reviews } = await scavio.mediaexpert.reviews({ sku: "709727", sort: "newest", limit: 100 });
const { data: washers } = await scavio.mediaexpert.category({ category: "agd/pralki-i-suszarki/pralki", filters: ["promocje_cena-z-kodem"] });
const { data: tree } = await scavio.mediaexpert.categories();
const { data: brands } = await scavio.mediaexpert.brands({ query: "sams" });
const { data: amica } = await scavio.mediaexpert.brand({ brand: "amica" });
const { data: lists } = await scavio.mediaexpert.promotions({ black_weeks: true });
const { data: outlet } = await scavio.mediaexpert.outlet();
const { data: seller } = await scavio.mediaexpert.seller({ seller: "autobi" });
const { data: typed } = await scavio.mediaexpert.suggestions({ query: "pral" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.mediaexpert.search(...)`, `product`, `store_stock`, `stores`, `reviews`, `category`, `categories`, `brands`, `brand`, `promotions`, `outlet`, `seller` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 13 endpoints as tools: `search_mediaexpert`, `get_mediaexpert_product`, `get_mediaexpert_store_stock`, `get_mediaexpert_stores`, `get_mediaexpert_reviews`, `get_mediaexpert_category`, `get_mediaexpert_categories`, `get_mediaexpert_brands`, `get_mediaexpert_brand`, `get_mediaexpert_promotions`, `get_mediaexpert_outlet`, `get_mediaexpert_seller` and `get_mediaexpert_suggestions`. Media Expert is opt-in: add `mediaexpert` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.73.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,mediaexpert"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/mediaexpert-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [product](https://scavio.dev/docs/mediaexpert-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [store stock](https://scavio.dev/docs/mediaexpert-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [stores](https://scavio.dev/docs/mediaexpert-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [reviews](https://scavio.dev/docs/mediaexpert-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [category](https://scavio.dev/docs/mediaexpert-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [categories](https://scavio.dev/docs/mediaexpert-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [brands](https://scavio.dev/docs/mediaexpert-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [brand](https://scavio.dev/docs/mediaexpert-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [promotions](https://scavio.dev/docs/mediaexpert-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [outlet](https://scavio.dev/docs/mediaexpert-outlet?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [seller](https://scavio.dev/docs/mediaexpert-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api), [suggestions](https://scavio.dev/docs/mediaexpert-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api). Overview: [Media Expert API](https://scavio.dev/mediaexpert-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=media-expert-api).
