---
name: barnes-and-noble-api
description: Barnes & Noble API for Barnes & Noble (barnesandnoble.com, the US bookseller) - what a book costs at Barnes & Noble today and whether the Barnes & Noble stores near you have it for pickup, as barnesandnoble.com shows it to a visitor (on 2026-11-27 Project Hail Mary by Andy Weir, EAN 9780593135204, read $32 in hardcover with a 4.6 rating from 287 ratings, and the page linked 6 formats with their own EAN and price - paperback $22, Large Print $31, eBook $14.99, the Deluxe Edition $37 against $40 and the Audio CD at $49.99 not available for sale; The Hunger Games paperback, EAN 9780439023528, showed available for pickup at all 28 stores near Chicago ZIP 60611, State Street 0.73 miles away first) with the price, the struck-through original price, on-sale flag, the site's badges ($3 OFF, 50% Off, Best Seller), the member offer text as the page writes it (never a member price), publisher, imprint, publication date, pages, dimensions, series, audience age, run time, online stock flags and a short overview excerpt; keyword, title, author, series or ISBN search, the 24 results the site shows with its total (3,101 for project hail mary), in its 7 sorts and filtered by format, availability, price band, subject, age and language; one title by EAN, ISBN-13 or ISBN-10; store pickup flags for one EAN at the stores near a ZIP, a city or a store number; stores near a ZIP, a city or a point with hours, dated holiday hours (Thanksgiving closed, Black Friday 9 AM to 10 PM at Fifth Avenue) and cafe, toys and games, vinyl and used-book flags; one store in full; the Bestsellers page, Bestselling Books, The New York Times Best Sellers (11 lists such as Hardcover Fiction and Paperback Nonfiction) and B&N Stores Bestsellers; one collection (Mystery & Thriller, New Releases, Kids ages 3-5) sorted and filtered like search; the header navigation (9 departments, 238 links); the deals pages (Black Friday and Cyber Monday with 21 deal shelves and 165 titles, Coupons & Deals, kids, eBook and audiobook deals); search-box title and subject suggestions. US only, USD. 10 endpoints, 1 credit per call. No member prices, no review text, no results past the first 24, no unit counts at stores, no deal end dates, no price history, cart or checkout.
version: 1.0.0
tags: barnes-and-noble, barnesandnoble, barnesandnoble-com, barnes-and-noble-api, barnes-noble-api, bn-api, barnes-and-noble-prices, barnes-and-noble-book-prices, barnes-and-noble-search, barnes-and-noble-isbn, barnes-and-noble-isbn-lookup, barnes-and-noble-store-availability, barnes-and-noble-store-pickup, barnes-and-noble-stores, barnes-and-noble-store-hours, barnes-and-noble-bestsellers, barnes-and-noble-deals, barnes-and-noble-black-friday, barnes-and-noble-coupons, bn-exclusive, nyt-best-sellers, new-york-times-best-sellers, book-prices, book-data, book-metadata, isbn-lookup, isbn-13, ean, book-search, bestseller-lists, new-releases, ebook-prices, audiobook-prices, book-deals, bookstore, bookstore-locator, store-availability, store-pickup, publishing, book-market-research, price-monitoring, us-retail, usd, agents, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/barnesandnoble-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api
---

# Barnes & Noble API - Book Prices, Store Availability, Bestsellers, Deals

Read Barnes & Noble (barnesandnoble.com, the US bookseller): keyword, author, series and ISBN search, one title in full by EAN, ISBN-13 or ISBN-10 with every format the page links, store pickup flags for one title at the Barnes & Noble stores near a ZIP, a city or a store number, the stores near a ZIP, a city or a point, one store with hours and holiday hours, the bestseller lists, one collection, the header navigation, the deals pages and search-box suggestions. www.barnesandnoble.com only (US, USD, English), as shown to a visitor who is not signed in. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Barnes & Noble book prices and Barnes & Noble store pickup.** What a book costs at barnesandnoble.com today in each format, whether it is on sale, and which Barnes & Noble stores near a ZIP show it available for pickup. On 2026-11-27 Project Hail Mary (EAN `9780593135204`, hardcover) read $32, 4.6 stars from 287 ratings, with 6 `formats` each carrying its own EAN and price: paperback `9780593135228` $22, Large Print $31, eBook $14.99, the Deluxe Edition `9798217374274` $37 against an `original_price` of $40 (`on_sale` true, badge "$3 OFF") and the Audio CD at $49.99 with `available_for_sale` false. `/store-availability` for The Hunger Games paperback (`9780439023528`) near ZIP 60611 listed 28 stores, all `available` (State Street, Chicago, 0.73 miles, first); Project Hail Mary near "Austin, TX" was available at 11 of 16. The second job is lists: the Bestsellers page, The New York Times Best Sellers (11 lists in one answer) and the Black Friday and Cyber Monday deals page (21 deal shelves, 165 titles, "50% Off Hardcover Fiction" first). Pair it with `goodreads-api` for how readers rate the same book and `thriftbooks-api` for used copies (match on ISBN-13).

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **The first 24 results only.** Search and collections answer the 24 results the site shows on its first page, with the site's `total` for the whole list (`has_more` true when there are more). There is no `page` parameter: narrow the list with `sort` and `filters`.
- **No member prices.** Prices are what barnesandnoble.com shows a visitor who is not signed in. `member_offers` is the member offer text the page shows, as given ("Premium Members save an extra 10%." on the Sunrise on the Reaping audiobook): quote it as Barnes & Noble's offer text, never compute a member price from it. Badges such as "Bonus $10 Reward" are the site's own text.
- **Store pickup is a flag per store, never a unit count.** `eligible` and `available` are Barnes & Noble's own pickup flags for that EAN at each store. Never write how many copies a store has. Prices are national: a store charges the price `product` shows.
- **The overview is a short excerpt.** `overview` is at most 300 characters of the page's publisher copy, cut at a word and ending with "..." (`overview_truncated` says when it was cut). Never quote more than that excerpt, and never present it as the book's text. No book excerpts, sample pages or review text are returned.
- **Ratings come from product.** `rating` and `rating_count` are empty in lists (the site does not fill them there); `/product` carries them. No review text is available.
- **Formats are EANs.** Hardcover, paperback, eBook, audiobook, Large Print and B&N Exclusive editions each have their own EAN and price (`formats[]`). Barnes & Noble digital titles use 2940 EANs (`2940191864129` for an audiobook). `/store-availability` takes one EAN, so pick the format first.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. The deals pages give no end date per deal. Poll and store your own series.

Barnes & Noble has no public API for reading its catalog, prices or store pickup. Prices and store pickup are shown on barnesandnoble.com for the title and place you pick, and this skill reads those public pages with one Scavio key.

See also: how readers rate the same book `goodreads-api`; used copies and prices per condition `thriftbooks-api`; the same ISBN at Amazon `amazon-product-data`; prices across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Price a book at Barnes & Noble in hardcover, paperback, eBook, audiobook, Large Print or a B&N Exclusive edition, with the struck-through price and the site's sale badges
- Look up a book by ISBN-13, ISBN-10 or EAN: publisher, imprint, publication date, pages, dimensions, series, audience age, rating and every format the page links
- Check whether the Barnes & Noble stores near a ZIP, a city or a given store show one title available for pickup
- Search barnesandnoble.com by title, author, series, ISBN or subject, sorted by bestselling, newest, oldest, price or title, or filtered by format, availability, price band, subject, age or language
- Read the Barnes & Noble Bestsellers page, Bestselling Books, The New York Times Best Sellers lists or B&N Stores Bestsellers
- List a Barnes & Noble collection (Mystery & Thriller, New Releases, Kids ages 3-5) or the departments and links of the site's navigation
- Read the Barnes & Noble Black Friday and Cyber Monday deals, Coupons & Deals, kids' book deals, eBook or audiobook deals
- Find the Barnes & Noble stores near a ZIP, a city or a point with hours, holiday hours and cafe, toys and games, vinyl or used-book flags, or one store in full
- Get the search box's title and subject suggestions for a partial query

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Search, product, store availability, stores, store and suggestions usually take 2-15 seconds; bestsellers, category, categories and deals read large pages and usually take 8-35 seconds. Allow a client timeout of at least 90 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/barnesandnoble/search` | Keywords (title, author, series, ISBN): the first 24 results with the site's total, price, original price, on-sale flag, format, series, publication date, sales rank, availability, badges, and facets with counts | 1 |
| `POST /api/v1/barnesandnoble/product` | One title by EAN, ISBN-13 or ISBN-10: publisher, imprint, publication date, pages, dimensions, language, series, audience age, run time, price, original price, online stock flags, rating, member offer text, badges, collections, categories, a short overview excerpt and every format with its EAN and price | 1 |
| `POST /api/v1/barnesandnoble/store-availability` | One EAN's pickup flags (eligible, available) at the stores near a ZIP, a city and state or a store number (usually 16-50 stores, nearest first), with each store's address, phone, hours and distance | 1 |
| `POST /api/v1/barnesandnoble/stores` | The stores near a ZIP, a city and state or a point, nearest first, with hours by day, holiday hours, services and coordinates | 1 |
| `POST /api/v1/barnesandnoble/store` | One store by id: the stores fields plus the company name and the holiday hours line | 1 |
| `POST /api/v1/barnesandnoble/suggestions` | The search box's suggestions for a partial query: up to 10 titles (search item fields) and subject topics with their collection path | 1 |
| `POST /api/v1/barnesandnoble/bestsellers` | The Bestsellers page, Bestselling Books, The New York Times Best Sellers or B&N Stores Bestsellers, ranked | 1 |
| `POST /api/v1/barnesandnoble/category` | One collection by path or link, sorted and filtered like search, with breadcrumbs (or the page's shelves) | 1 |
| `POST /api/v1/barnesandnoble/categories` | The header navigation: departments, their groups and links, each with the collection path category takes | 1 |
| `POST /api/v1/barnesandnoble/deals` | A deals page (Black Friday and Cyber Monday, Coupons & Deals, kids, eBooks, audiobooks) as deal shelves of titles with sale and original prices | 1 |

`country` is `us` (the default and the only market). Anything else is an unbilled `400`.

## Prices: price, original price, sale badges and member offer text

Every listed title carries:

| Field | Meaning |
|---|---|
| `price` | What Barnes & Noble charges now, in USD |
| `original_price` | The struck-through price when the site shows one ($40 on the Project Hail Mary Deluxe Edition at $37) |
| `on_sale` | True when the site shows a struck-through price |
| `badges` | The site's own badges as given: "$3 OFF", "50% Off", "30% off", "Best Seller", "Bonus $10 Reward" |
| `availability` | Online availability as given: `IN_STOCK`, `OUT_OF_STOCK`, `PREORDER` ... (lists) |
| `available_for_sale`, `inventory` | Product: whether the format can be bought, and the page's online stock flags {`in_stock`, `preorder`, `backorder`} |
| `member_offers` | Product: the member offer text the page shows, as given; never a price |
| `sales_rank` | The site's own sales rank for the title (null when the site gives none) |

- Quote "$37 at barnesandnoble.com on 2026-11-27 (Deluxe Edition hardcover, original price $40, badge $3 OFF)", with the date and the format.
- Quote one format's price from `formats[]` when the user names a format, not the requested EAN's price.
- Report the site's badges, the member offer text and the arithmetic only. Never compute a member price, never judge a discount, and never describe how often a title is on sale.

## Workflow

1. **Find the title.** `/search` with `query` (`project hail mary`, an author, a series or an ISBN), or `/bestsellers`, `/category` (a `path` from `categories`, `suggestions` topics or `breadcrumbs`) or `/deals`. Each item's `ean` is the input of product and store-availability.
2. **Read it in full.** `/product` with `ean` (or `isbn`, an ISBN-10 or ISBN-13, dashes allowed): every format the page links in `formats[]`, each with its own `ean` and `price`.
3. **Pick the format.** Match the user's format (hardcover, paperback, eBook, audiobook) in `formats[]` and take its `ean`.
4. **Pickup near a place.** `/store-availability` with `ean` and `near` (a ZIP `60611`, a city and state `"Austin, TX"` or a store number `2234`). Read `available` per store and `available_count`.
5. **Narrow a list.** `sort` and `filters` (`format`, `availability`, `price`, `subject`, `age`, `language`; values exactly as an earlier answer gives them in `facets[].values[].value`, a value or a list, at most 10 values in all). There is no paging: the answer is always the first 24.
6. **Stores.** `/stores` with `near` (ZIP or city and state) or `latitude` + `longitude`; `/store` with `store_id` for one store with its holiday hours line.
7. **Watching prices or pickup:** there is no history. Poll the same EANs on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords: title, author, series, ISBN or subject, 1-200 chars |
| `path` | string | category: one of | A collection path (`books/mystery-thrillers`, `books/kids/ages-3-5`): `categories[].path`, `topics[].path`, `breadcrumbs[].path`; a leading `/collections/` is accepted |
| `url` | string | category: one of | A barnesandnoble.com/collections/ link instead of `path` (not both); its query string is not read (send `sort` and `filters`) |
| `sort` | string | `relevance` | The site's sort menu: `relevance` (Top Matches), `bestselling`, `newest`, `oldest`, `price_asc`, `price_desc`, `title` (A to Z). `price_asc` puts free eBooks first |
| `filters` | object | none | {`format`, `availability`, `price`, `subject`, `age`, `language`}: a value or a list of values each, at most 10 in all |
| `country` | string | `us` | `us` only |

Filter values: `format` as the site names it (`Hardcover`, `Paperback`, `eBook`, `Audiobook`, `BN Exclusive`, `Large Print`, `Audio CD` ...); `availability` `in_stock`, `preorder` or `ships_in_1_2_days`; `price` `under_5`, `5_10`, `10_15`, `15_25`, `25_50` or `over_50` (the site's bands Under $5 to Over $50); `subject` (`Fiction`, `Kids`, `Social Sciences` ...), `age` (`0 - 2 Years`, `3 - 5 Years` ...) and `language` (`English`, `Spanish` ...) as `facets[].values[].value` gives them.

### Product (`/product`) and store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ean` | string or integer | one of | The EAN / ISBN-13 (`9780593135204`; `items[].ean`, `formats[].ean`; 978, 979 or the site's 2940 digital EANs), or an ISBN-10 (converted to its 978 EAN). Check digits are verified |
| `isbn` | string or integer | one of | Instead of `ean` (not both): an ISBN-10 or ISBN-13, dashes allowed (`0439023521`, `978-1-668-00217-9`) |
| `near` | string | store-availability: required | A US ZIP code (`60611`), a city and state (`"Austin, TX"`) or a Barnes & Noble store number (`2234`) |
| `country` | string | `us` | `us` only |

### Stores (`/stores`), store (`/store`), suggestions (`/suggestions`), bestsellers (`/bestsellers`), categories (`/categories`), deals (`/deals`)

`/stores` takes `near` (a US ZIP code or `"City, ST"`) or `latitude` + `longitude` together (not both). `/store` takes `store_id` (required, digits, `2234` for Fifth Avenue; `stores[].store_id`). `/suggestions` takes `query` (1-100 chars). `/bestsellers` takes `list`: `top` (default, the Bestsellers page), `books` (Bestselling Books), `nyt` (The New York Times Best Sellers) or `stores` (B&N Stores Bestsellers: hardcover fiction and nonfiction). `/categories` takes no parameter besides `country`. `/deals` takes `type`: `black_friday` (default, the Black Friday and Cyber Monday deals page while the site runs it), `coupons` (Coupons & Deals), `kids` (Book Deals for Kids), `ebooks` or `audiobooks`.

## Examples

### Store pickup flags for one title near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/barnesandnoble/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "9780439023528", "near": "60611"}'
```

Captured `data` (2026-11-27; 2 of 28 stores shown):

```json
{
  "country": "us",
  "currency": "USD",
  "ean": "9780439023528",
  "near": "60611",
  "near_type": "zip",
  "count": 28,
  "available_count": 28,
  "stores": [
    {
      "store_id": "3610",
      "name": "State Street",
      "address": { "street": "150 N State Street", "location_name": null, "city": "Chicago", "state": "IL", "zip": "60601" },
      "phone": "708-967-3324",
      "hours": "Sun 10-7, Mon-Sat 9-8",
      "distance_miles": 0.73,
      "ean": "9780439023528",
      "eligible": true,
      "available": true
    },
    {
      "store_id": "3464",
      "name": "Diversey Parkway",
      "address": { "street": "651 West Diversey Parkway", "location_name": null, "city": "Chicago", "state": "IL", "zip": "60614" },
      "phone": "872-270-0776",
      "hours": "Sun 11-7, Mon-Sat 10-9",
      "distance_miles": 2.88,
      "ean": "9780439023528",
      "eligible": true,
      "available": true
    }
  ],
  "notes": [
    "eligible and available are Barnes & Noble's own pickup flags for this EAN at each store (available: the store shows it in stock for pickup), not unit counts.",
    "Prices are national: a store charges the price product shows."
  ]
}
```

The other 26 stores ran from Wicker Park (3.03 miles) to Bayshore (88.12 miles), all `available`. `{"ean": "9780593135204", "near": "Austin, TX"}` (Project Hail Mary, hardcover) answered 16 stores, 11 available (Sunset Valley 5.19 miles first; the other 5, Southpark Meadows among them, `eligible` but not `available`); `{"isbn": "978-1-668-00217-9", "near": "2234"}` answered 50 stores from Fifth Avenue outward, none available.

### One title with its formats

```bash
curl -X POST https://api.scavio.dev/api/v1/barnesandnoble/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "9780593135204"}'
```

Captured `data` (2026-11-27; `collections`, `categories`, `image`, `images`, `url`, `overview` and `notes` dropped; `formats` cut to 4 of 6):

```json
{
  "country": "us",
  "currency": "USD",
  "requested_ean": "9780593135204",
  "ean": "9780593135204",
  "work_id": "1137456421",
  "title": "Project Hail Mary",
  "contributors": [{ "name": "Andy Weir", "role": "Author" }],
  "format": "Hardcover",
  "parent_format": "Hardcover",
  "edition": null,
  "publisher": "Random House Publishing Group",
  "imprint": "Ballantine Books",
  "publication_date": "2021-05-04",
  "pages": 496,
  "dimensions": { "height": 9.4, "width": 6.2, "depth": 1.7 },
  "language": "English",
  "series": null,
  "audience_age": null,
  "run_time": null,
  "sales_rank": null,
  "price": 32,
  "original_price": null,
  "on_sale": false,
  "available_for_sale": true,
  "inventory": { "in_stock": true, "preorder": false, "backorder": false },
  "rating": 4.6,
  "rating_scale_max": 5,
  "rating_count": 287,
  "member_offers": [],
  "badges": [],
  "overview_truncated": true,
  "formats": [
    { "format": "Paperback", "ean": "9780593135228", "title": "Project Hail Mary", "price": 22, "original_price": null, "on_sale": false, "available_for_sale": true, "requested": false },
    { "format": "Hardcover", "ean": "9780593135204", "title": "Project Hail Mary", "price": 32, "original_price": null, "on_sale": false, "available_for_sale": true, "requested": true },
    { "format": "eBook", "ean": "9780593135211", "title": "Project Hail Mary", "price": 14.99, "original_price": null, "on_sale": false, "available_for_sale": true, "requested": false },
    { "format": "Special", "ean": "9798217374274", "title": "Project Hail Mary (Deluxe Edition): A Novel", "price": 37, "original_price": 40, "on_sale": true, "available_for_sale": true, "requested": false }
  ]
}
```

The other two formats were Large Print (`9780593395561`, $31) and Audio CD (`9798228844506`, $49.99, `available_for_sale` false). `overview` held a 300-character excerpt of the publisher's copy ending with "...". `{"isbn": "0439023521"}` answered The Hunger Games paperback (`9780439023528`, Scholastic Press, 384 pages) at $14.99 with 4.8 stars from 7,737 ratings, `series` {`title` Hunger Games Series, `number` 1} and `audience_age` {`from` 13, `to` 17}. `{"ean": "2940191864129"}` (the Sunrise on the Reaping audiobook, Unabridged) read $23.99 against $29.99, badges "20% off" and "Best Seller", `run_time` "46086" and `member_offers` ["Premium Members save an extra 10%."]. An unknown EAN is a charged `404`: "Barnes & Noble has no product with EAN 9780000000002."

### Search, bestsellers, category, deals, stores, store, suggestions, categories

- `/search` `{"query": "project hail mary"}`: `total` 3,101, the first 24 with `has_more` true; the first item the Deluxe Edition (`9798217374274`, `format` Special, `format_detail` Hardcover) at $37 against $40 with badges "$3 OFF" and "Best Seller", `sales_rank` 248, then the paperback $22 (`sales_rank` 26) and the hardcover $32. Barnes & Noble also lists music and film: the score on CD and vinyl, the Blu-ray and the DVD came back in the same 24. `facets` held availability (IN_STOCK 3,075, PREORDER 26), format (eBook 1,638, Paperback 936, Hardcover 302, Audiobook 169), subject, age, price band and language with counts. `{"query": "hunger games", "sort": "bestselling", "filters": {"format": "Paperback"}}` answered 1,124 results.
- `/bestsellers` `{}`: the Bestsellers page, `total` 180,416, the first 24 ranked; rank 1 A Court of Splintered Harmony (A Court of Thorns and Roses Series #6) hardcover at $32 with badges "Bonus $10 Reward" and "Best Seller"; rank 3 Fight or Flight (Diary of a Wimpy Kid #21) at $7.99 against $15.99 ("50% Off"). `{"list": "nyt"}` answered `items` [] and `lists` of 11 New York Times lists (Hardcover Fiction 15, Hardcover Nonfiction 15, Paperback Fiction 15, Paperback Nonfiction 15, Advice, How-To & Miscellaneous 10, ... Audio Nonfiction 15), 131 titles in all; `{"list": "stores"}` the B&N Stores Bestsellers (66 titles).
- `/category` `{"path": "books/mystery-thrillers"}`: "Best Mystery & Thriller Books", `total` 188,000, breadcrumbs Home > Books > Mystery & Thrillers; The French Illusion: A Novel hardcover at $17.50 against $35 ("50% Off"). An unknown collection is a charged `404`: "Barnes & Noble has no collection <path>."
- `/deals` `{}`: "Black Friday and Cyber Monday Deals", 21 deal shelves and 165 titles: "50% Off Hardcover Fiction" (13), "50% Off Hardcover Nonfiction" (11), "50% Off Select Paperbacks" (15), "Buy One, Get One 50% Off Collectible Editions" (14), ... "30% Off Thousands of CDs" (14). `{"type": "coupons"}` 3 shelves ("30% Off Hardcover Bestsellers"); `{"type": "kids"}` 10 shelves and 114 titles; `{"type": "ebooks"}` 4 shelves; `{"type": "audiobooks"}` 1 shelf of 13. No end dates per deal. A deals page the site does not run is a charged `404`: "Barnes & Noble has no <type> deals page right now."
- `/stores` `{"near": "10001"}`: 44 stores nearest first, Union Square (0.81 miles) and Fifth Avenue (0.94 miles) first, each with `services` {`cafe`, `toys_games`, `vinyl`, `used_books`, `electronics`}. `{"near": "Austin, TX"}` 6 stores; `{"latitude": 34.0522, "longitude": -118.2437}` 30.
- `/store` `{"store_id": "2234"}`: Fifth Avenue, 555 Fifth Avenue, New York, NY 10017, opened 2005-10-07, "9-9 Every Day", `holiday_hours` Thanksgiving 2026-11-26 Closed and Black Friday 2026-11-27 "9:00 AM - 10:00 PM", `holiday_hours_text` "Thanksgiving: Closed | Black Friday: 9:00 AM - 10:00 PM", cafe, toys and games and vinyl. An unknown store is a charged `404`: "Barnes & Noble has no store <id>."
- `/suggestions` `{"query": "hunger"}`: `total` 5,710, 10 titles (the Hunger Games 5-Book Box Set (Deluxe Edition) at $89.95 first) and 5 topics (Fiction `books/general-fiction`, Kids `books/kids`, ...). The answer carries no keyword completions.
- `/categories` `{}`: 9 departments (Bestsellers, Holiday Gift Guide, Books, Kids & Teens, What to Read, New, eBooks & NOOK, Toys, Games & Gifts, Music & Movies), 52 groups, 238 links; Books > All Fiction > Mystery & Thriller links `books/mystery-thrillers`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bn(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/barnesandnoble/{endpoint}", headers=HEADERS, json=body, timeout=90)
    r.raise_for_status()
    return r.json()

# 1. The New York Times Best Sellers, list by list (1 credit)
nyt = bn("bestsellers", {"list": "nyt"})["data"]
for l in nyt["lists"]:
    for i in l["items"][:3]:
        print(l["heading"], i["rank"], i["ean"], i["title"], i["price"], i["original_price"])

# 2. One title: every format with its own EAN and price (1 credit)
p = bn("product", {"isbn": "0439023521"})["data"]
for f in p["formats"]:
    print(f["format"], f["ean"], f["price"], f["original_price"], f["available_for_sale"])

# 3. Pickup flags for the paperback near a ZIP (1 credit). Flags, not unit counts.
pb = next(f for f in p["formats"] if f["format"] == "Paperback")
stock = bn("store-availability", {"ean": pb["ean"], "near": "60611"})["data"]
for s in stock["stores"][:10]:
    print(s["name"], s["distance_miles"], s["eligible"], s["available"])

# Prices and pickup flags can change between calls. Store each answer with
# fetched_at and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `country` (`us`), `currency` (`USD`) and `notes`.

- **item** (search, category, suggestions products, bestsellers) - `position`, `ean`, `work_id`, `title`, `contributors[]` {`name`, `role`}, `format`, `format_detail`, `edition`, `series` {`title`, `number`}, `publication_date`, `sales_rank`, `price`, `original_price`, `on_sale`, `currency`, `availability`, `rating`, `rating_count` (empty in lists), `badges`, `image`, `url`. Bestsellers items add `rank`.
- **lists** (search, category) - `sort`, `sort_label`, `filters`, `total`, `count`, `page_size` (24), `has_more`, `items[]`, `facets[]` {`filter`, `title`, `values[]` {`value`, `label`, `count`}}. Search adds `query`; category adds `path`, `url`, `title`, `breadcrumbs[]` {`name`, `url`, `path`} and `shelves[]` {`heading`, `group`, `link`, `link_path`, `count`, `items`} (a collection page that shows shelves instead of a product list answers `items` [] and its shelves).
- **product** - `requested_ean`, `ean`, `work_id`, `title`, `contributors`, `format`, `parent_format`, `edition`, `publisher`, `imprint`, `publication_date`, `pages`, `dimensions` {`height`, `width`, `depth`}, `language`, `series`, `audience_age` {`from`, `to`}, `run_time`, `sales_rank`, `price`, `original_price`, `on_sale`, `available_for_sale`, `inventory` {`in_stock`, `preorder`, `backorder`}, `rating`, `rating_scale_max`, `rating_count`, `member_offers`, `badges`, `collections[]` {`name`, `url`, `path`}, `categories[]` {`name`, `url`, `path`}, `image`, `images`, `url`, `overview` (at most 300 characters), `overview_truncated`, `formats[]` {`format`, `ean`, `title`, `price`, `original_price`, `on_sale`, `available_for_sale`, `requested`}.
- **store-availability** - `ean`, `near`, `near_type` (`zip`, `city`, `store`), `count`, `available_count`, `stores[]` {`store_id`, `name`, `address` {`street`, `location_name`, `city`, `state`, `zip`}, `phone`, `hours`, `distance_miles`, `ean`, `eligible`, `available`}.
- **stores** - `near`, `latitude`, `longitude`, `count`, `stores[]` {`store_id`, `name`, `address`, `phone`, `latitude`, `longitude`, `distance_miles`, `time_zone`, `hours`, `hours_by_day[]` {`day`, `open`, `close`, `text`}, `holiday_hours[]` {`name`, `date`, `open`, `close`, `text`}, `services` {`cafe`, `toys_games`, `vinyl`, `used_books`, `electronics`}, `open_date`, `events_count`, `url`}. Hours are as the store page writes them (open and close without AM / PM: 9:00 to 8:00 is 9 AM to 8 PM; `text` is the page's own wording).
- **store** - the stores fields plus `corp_name` and `holiday_hours_text`.
- **suggestions** - `query`, `total`, `count`, `products[]` (item fields), `topics[]` {`label`, `path`, `url`}.
- **bestsellers** - `list`, `title`, `url`, `total`, `count`, `items[]` (item fields with `rank`), `lists[]` {`heading`, `link`, `link_path`, `count`, `items[]` {`rank`, `ean`, `title`, `format`, `contributors`, `price`, `original_price`, `on_sale`, `available_for_sale`, `image`}} (a list page that shows its titles as separate lists; `items` is then empty).
- **categories** - `count`, `group_count`, `link_count`, `departments[]` {`name`, `url`, `path`, `groups[]` {`name`, `url`, `path`, `links[]` {`name`, `url`, `path`}}}. `path` is null for a page that is not a collection.
- **deals** - `type`, `title`, `url`, `count`, `item_count`, `sections[]` {`heading`, `group`, `link`, `link_path`, `count`, `items[]` {`ean`, `title`, `format`, `contributors`, `price`, `original_price`, `on_sale`, `available_for_sale`, `image`}}.

## Guardrails

- Name it "Barnes & Noble (barnesandnoble.com, the US bookseller)" on first mention. Barnes & Noble member accounts are not read.
- Prices: quote `price` with `original_price` and the site's badges, the format and EAN, and the `fetched_at` date. Prices are what a visitor who is not signed in sees; never call any price a member price.
- `member_offers` is offer text as the page writes it: quote it as given, never turn it into a price.
- Store pickup: report `eligible` and `available` per store as Barnes & Noble gave them at the moment of the call; Scavio makes no promise of their accuracy. Never state or estimate a unit count, and never promise pickup.
- Overview: never quote more than the excerpt `overview` returns, and label it as the publisher's copy from the page. No book text, sample pages or review text are available.
- Comparing Barnes & Noble with Amazon, ThriftBooks or Goodreads: compare only the same EAN / ISBN-13 and format, each with its date. B&N Exclusive editions have no same item elsewhere: label them as different products. Never call one retailer cheaper beyond the numbers shown.
- Not available: member prices, review text, results past the first 24 (no paging), unit counts at stores, deal end dates, price history (poll and store), cart or checkout. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not store Barnes & Noble data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Barnes & Noble's terms of use restrict automated access or commercial use of its site; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish cover images, overview copy or logos; link titles by `url` instead.
- Never fabricate prices, EANs, store ids, hours, pickup flags, ranks, dates or ratings. Only return what the API returned, with the `fetched_at` time and the title `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "ean or isbn is required", "Send ean or isbn, not both.", an EAN or ISBN whose check digit fails ("ean must be a valid EAN / ISBN-13 (e.g. 9780593135204) or ISBN-10 (e.g. 0439023521); check digits are verified."), a `near` that is not a ZIP, a city and state or a store number ("near must be a US ZIP code (10001), a city and state ("Austin, TX") or a Barnes & Noble store number (2234)."), "near (a ZIP code or a city and state) or latitude and longitude is required.", "Send latitude and longitude together.", "Send near, or latitude and longitude, not both.", a `store_id` that is not digits ("store_id must be a Barnes & Noble store id (digits, e.g. 2234; stores lists them)."), "path or url is required", "Send path or url, not both.", a `url` that is not a barnesandnoble.com collection link, an unknown filter ("filters.<key> is not a filter; use format, availability, price, subject, age, language."), "filters.availability must be in_stock, preorder or ships_in_1_2_days.", a price band that is not one of the site's, "At most 10 filter values in all.", an unknown `sort`, `list` or `type`, and "country must be us (default): Barnes & Noble (barnesandnoble.com) serves the United States only."
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Barnes & Noble has no product with EAN <ean>.", "Barnes & Noble has no store check for EAN <ean>.", "Barnes & Noble has no store <id>.", "Barnes & Noble has no collection <path>.", "Barnes & Noble has no <type> deals page right now.", "Barnes & Noble has no search page for this query.", "Barnes & Noble has no suggestions for this query.". Take EANs, store ids and paths from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api).
- `502` means Barnes & Noble data was temporarily unavailable ("Barnes & Noble is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Barnes & Noble is busy ("Barnes & Noble is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- A `200` with an empty list is an answer: "Barnes & Noble lists no store near this place." or "Barnes & Noble found nothing for this request (with these filters)." in `notes`.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.100.0
npm install scavio@0.101.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.barnesandnoble.search({ query: "hunger games", sort: "bestselling", filters: { format: "Paperback" } });
const { data: book } = await scavio.barnesandnoble.product({ isbn: "0439023521" });
const { data: pickup } = await scavio.barnesandnoble.storeAvailability({ ean: "9780439023528", near: "60611" });
const { data: near } = await scavio.barnesandnoble.stores({ near: "10001" });
const { data: fifthAve } = await scavio.barnesandnoble.store({ store_id: "2234" });
const { data: typed } = await scavio.barnesandnoble.suggestions({ query: "hunger" });
const { data: nyt } = await scavio.barnesandnoble.bestsellers({ list: "nyt" });
const { data: mystery } = await scavio.barnesandnoble.category({ path: "books/mystery-thrillers", sort: "newest" });
const { data: nav } = await scavio.barnesandnoble.categories({});
const { data: deals } = await scavio.barnesandnoble.deals({ type: "black_friday" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.barnesandnoble.search(...)`, `product`, `store_availability`, `stores`, `store`, `suggestions`, `bestsellers`, `category`, `categories` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_barnesandnoble`, `get_barnesandnoble_product`, `get_barnesandnoble_store_availability`, `get_barnesandnoble_stores`, `get_barnesandnoble_store`, `get_barnesandnoble_suggestions`, `get_barnesandnoble_bestsellers`, `get_barnesandnoble_category`, `get_barnesandnoble_categories` and `get_barnesandnoble_deals`. Barnes & Noble is opt-in: add `barnesandnoble` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.100.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,barnesandnoble"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/barnesandnoble-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [product](https://scavio.dev/docs/barnesandnoble-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [store availability](https://scavio.dev/docs/barnesandnoble-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [stores](https://scavio.dev/docs/barnesandnoble-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [store](https://scavio.dev/docs/barnesandnoble-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [suggestions](https://scavio.dev/docs/barnesandnoble-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [bestsellers](https://scavio.dev/docs/barnesandnoble-bestsellers?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [category](https://scavio.dev/docs/barnesandnoble-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [categories](https://scavio.dev/docs/barnesandnoble-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api), [deals](https://scavio.dev/docs/barnesandnoble-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api). Overview: [Barnes & Noble API](https://scavio.dev/barnesandnoble-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=barnes-and-noble-api).
