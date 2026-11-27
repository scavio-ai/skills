---
name: thriftbooks-api
description: ThriftBooks API for ThriftBooks (thriftbooks.com, the US online used-book seller; USD) - what a used or new book costs at ThriftBooks today in each condition, as its pages show it to a visitor who is not signed in (on 2026-11-27 The Hunger Games, work 246187, read 4 formats from $7.19 to $34.59 - Paperback New $12.74 (list $14.99, 499 copies), Very Good $34.59, Good $16.79, Acceptable $7.19, Hardcover New $17.90 (500 or more copies), Good $9.29 with no dust jacket, Acceptable $15.09 ex-library, Audio CD New $31.82, Library Binding New $24.95), one row per format and condition (New, Like New, Very Good, Good, Acceptable) with price, list price, quantity, edition and copy ids, ISBN and EAN, ex-library, no-dust-jacket and no-CD flags, ThriftBooks Deals, promotion text, ReadingRewards bonus points and days to ship; an ISBN-10 or ISBN-13 lookup that returns the matched work and edition with that table (9780593135204, Project Hail Mary hardcover, New $23.92, list $32); keyword or whole-catalog search with the bestsellers, ThriftBooks Deals and New Releases presets, filtered by format, condition, language, genre, price, collectible, signed, first edition and large print, in the site's 7 sorts, up to 50 works per page and 10,000 results deep, each work with its price range, the copy the result puts up for sale, list price, copies available, edition count, series and rating; one edition with publisher, release date, pages, age and grade range, lowest new and used price, a short overview excerpt and its copies; every copy of an edition for sale; every edition of a work, 25 per page, in 5 sorts with format and condition filters; customer reviews 10 per page with rating, headline, text, date and verified purchase (no reviewer names); search-box title and author suggestions. 8 endpoints, 1 credit per call. US storefront only, USD. A New quantity of 500 means 500 or more. No member or cart prices, no price history, no sold prices, no checkout.
version: 1.0.0
tags: thriftbooks, thriftbooks-com, thriftbooks-api, thriftbooks-prices, thriftbooks-used-books, thriftbooks-isbn, thriftbooks-isbn-lookup, thriftbooks-search, thriftbooks-editions, thriftbooks-copies, thriftbooks-conditions, thriftbooks-deals, thriftbooks-bestsellers, thriftbooks-new-releases, thriftbooks-reviews, thriftbooks-readingrewards, used-books, used-book-prices, book-prices, book-condition, like-new, very-good, ex-library, isbn-lookup, isbn-13, isbn-10, ean, book-editions, book-search, book-data, book-metadata, bestsellers, book-reviews, textbooks, collectible-books, signed-books, first-editions, book-resale, bookselling, price-monitoring, price-comparison, us-retail, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/thriftbooks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api
---

# ThriftBooks API - Used Book Prices by Condition, ISBN Lookup, Editions

Read ThriftBooks (thriftbooks.com, the US online used-book seller): keyword or whole-catalog search with the bestsellers, ThriftBooks Deals and New Releases presets, an ISBN lookup, the format x condition price table of a work, one edition in full, every copy of an edition for sale, every edition of a work, customer reviews and search-box suggestions. www.thriftbooks.com only (US storefront, USD, English), as shown to a visitor who is not signed in. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: what a book costs at ThriftBooks in each condition.** A used book has no single price: ThriftBooks prices every format and condition separately, and this skill returns that table. On 2026-11-27 The Hunger Games (work `246187`) read 4 formats from $7.19 to $34.59: Paperback New $12.74 (list $14.99, 499 copies), Very Good $34.59, Good $16.79 and Acceptable $7.19; Hardcover New $17.90 (500 copies, which means 500 or more), Good $9.29 (one copy, `no_dust_jacket` true) and Acceptable $15.09 (`ex_library` true); Audio CD New $31.82; Library Binding New $24.95 (60 days to ship). The second job is ISBN lookup: `/isbn` with `9780593135204` matched Project Hail Mary (work `26830049`, hardcover edition `49364660`) and returned the whole work's table, the matched hardcover New at $23.92 against a $32 list price. Pair it with `goodreads-api` for the reader ratings of the same book and `barnes-and-noble-api` or `amazon-product-data` for new-book prices elsewhere (match on ISBN-13).

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit, suggestions included. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **Prices are per format and condition.** `/work` and `/isbn` give one row per format (Hardcover, Paperback, Audio CD, Library Binding, ...) and condition (New, Like New, Very Good, Good, Acceptable). Quote the row the user means, never the work's `low_price` as "the price".
- **A New quantity of 500 means 500 or more.** 500 is the most ThriftBooks shows for a New copy. `available_copies` on search counts copies across editions, so a total of 500 or more is a lower bound too (one bestseller read 501).
- **Read `in_stock` first.** A row with `in_stock` false has `price` null and no copy for sale now; such a row can still carry the `edition_id` and `copy_id` of a copy in another format (the Hunger Games Audio CD Very Good row pointed at a paperback copy). Never use the ids of an out-of-stock row.
- **The overview is a short excerpt.** `/edition` `description` is the start of the overview the page shows, cut to about 300 characters. Never quote more of a book's overview than that excerpt, and do not reproduce an `/editions` `edition_description` in full.
- **Search does not match ISBNs.** An ISBN sent as a search `query` is a `400` that points to `/isbn`.
- **US storefront only, no member prices.** Prices are ThriftBooks' own in USD as a visitor who is not signed in sees them: no member, cart or coupon prices. `loyalty_bonus_points` are the ReadingRewards bonus points ThriftBooks shows on a copy to any visitor; account balances are not available.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Used copies sell one at a time, so a row can change between calls. Poll and store your own series.

ThriftBooks has no public API for its catalog, prices or copies. Prices and copies are shown on thriftbooks.com for each book, and this skill reads those public pages with one Scavio key.

See also: for reader ratings, reviews and editions of the same book use `goodreads-api`; new-book prices and store pickup at Barnes & Noble `barnes-and-noble-api`; at Amazon `amazon-product-data`; used and sold listings on eBay `ebay-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a used book at ThriftBooks in a given condition (Like New, Very Good, Good, Acceptable) or new, for one format or every format
- Look a book up by ISBN-10 or ISBN-13 and get its ThriftBooks work, edition and condition prices
- Search thriftbooks.com by title, author or subject, sorted by popularity, relevance, bestsellers, title or publication date, or filtered by format, condition, language, genre, price, collectible, signed, first edition or large print
- List ThriftBooks bestsellers, ThriftBooks Deals or New Releases, overall or within a genre or price band
- Read one edition: publisher, release date, pages, language, age and grade range, list price, lowest new and used price, and its copies
- List every copy of one edition for sale, with condition, price, quantity and ex-library, no-dust-jacket or no-CD flags
- List every edition of a work (hardcover, paperback, mass market, library binding, audio) with each edition's lowest price, sorted by bestselling, date or price
- Read ThriftBooks customer reviews of a book, 10 per page
- Get ThriftBooks' search-box title and author suggestions for a partial query

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. Calls usually take 1-10 seconds (in the captures: an edition 0.5, suggestions 0.9, editions 1.2, a work 1.4, copies and reviews 2, search 2.7-3.9, an ISBN lookup 8.2). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/thriftbooks/search` | Keywords or the whole catalog, with the bestsellers, deals and new_releases presets: up to 50 works per page with total, each with price range, the copy the result puts up for sale, list price, copies available, edition count, series, rating; facets with the ids filters take | 1 |
| `POST /api/v1/thriftbooks/isbn` | An ISBN-10 or ISBN-13: the matched work and edition, then the work's format x condition price table with the matched edition's rows marked | 1 |
| `POST /api/v1/thriftbooks/work` | One work by id: for each format, the price, list price, quantity and copy details of each condition | 1 |
| `POST /api/v1/thriftbooks/edition` | One edition by id: title, authors, format, ISBN, publisher, release date, pages, language, age and grade range, list price, lowest new and used price, a short overview excerpt, its copies | 1 |
| `POST /api/v1/thriftbooks/copies` | Every copy of one edition for sale, one row per condition and copy type | 1 |
| `POST /api/v1/thriftbooks/editions` | Every edition of one work, 25 per page, filtered by format and condition, in 5 sorts, each with its copies | 1 |
| `POST /api/v1/thriftbooks/reviews` | Customer reviews of one work, 10 per page, in the site's order; no reviewer names | 1 |
| `POST /api/v1/thriftbooks/suggestions` | ThriftBooks' search-box title and author suggestions for a partial query | 1 |

US only: there is no `country` parameter. Every answer carries `store` (thriftbooks), `host`, `country` (us), `currency` (USD) and `language` (en).

## Prices: format, condition, list price and quantity

Every row of the `/work` and `/isbn` table (`formats[].conditions[]`) carries:

| Field | Meaning |
|---|---|
| `condition`, `condition_id` | New (1), Like New (2), Very Good (4), Good (3), Acceptable (5) |
| `in_stock` | A copy in this format and condition is for sale now; false means `price` null |
| `price` | ThriftBooks' price for that copy, USD |
| `list_price` | The list price ThriftBooks shows for the edition (null on some used rows) |
| `quantity` | Copies for sale; a New quantity of 500 means 500 or more |
| `edition_id`, `copy_id`, `isbn`, `ean`, `format_id` | The edition and copy behind the row (ignore them when `in_stock` is false) |
| `ex_library`, `no_dust_jacket`, `no_cd` | ThriftBooks' copy-type flags |
| `thrift_deal`, `promotion` | ThriftBooks Deals flag and the promotion text as given |
| `loyalty_bonus_points` | ReadingRewards bonus points shown on the copy |
| `shipping_surcharge`, `est_days_to_ship`, `ship_country_restriction` | Shipping details as given (Library Binding New on The Hunger Games: 60 days) |

Each format (`formats[]`) adds `format`, `format_id`, `in_stock`, `low_price`, `high_price` and `default_edition` {`edition_id`, `isbn`, `ean`}; the table adds `format_count`, `in_stock`, `low_price` and `high_price` across all formats.

- Quote "Paperback, Acceptable: $7.19 at thriftbooks.com on 2026-11-27 (list $14.99)", with format, condition and date.
- On search, `low_price` and `high_price` are the price range ThriftBooks gives for the work across editions and conditions, and `buy_now` is the copy the result puts up for sale (its condition, format and edition): it is not necessarily the lowest copy.
- Report ThriftBooks' prices, list prices and flags and the arithmetic only. Never judge a price as a good deal and never describe how often a book is in stock.

## Workflow

1. **Find the work.** With an ISBN, `/isbn` (it returns `work_id`, `edition_id` and the full price table in one call). Otherwise `/search` with `query` (`project hail mary`) or a `list` preset; each item's `work_id` is the input of work, editions and reviews, and `buy_now.edition_id` an input of edition and copies.
2. **Prices by condition.** `/work` with `work_id`: read `formats[].conditions[]`, keeping rows with `in_stock` true.
3. **One edition.** `/edition` with `edition_id` (from `/isbn`, `conditions[].edition_id`, `default_edition.edition_id` or `/editions`) for publisher, pages, release date and its copies; `/copies` for the copies alone.
4. **Every edition.** `/editions` with `work_id`, narrowed by `format` and `condition`, sorted by `price_asc` to find the lowest-priced edition; `in_stock_only` false lists editions with no copy now.
5. **Narrow a search.** `format`, `condition`, `language` (names or ids), `genre` (ids from `facets.genres[].id`), `min_price` and `max_price` (whole dollars), and the flags `deals`, `new_releases`, `collectible`, `signed`, `first_edition`, `large_print`, `include_out_of_stock`. `page` x `page_size` stays within 10,000.
6. **Reviews.** `/reviews` with `work_id` and `page`; `has_next` says whether another page exists.
7. **Watching prices:** there is no history. Poll the same works or editions on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | none | Keywords (title, author, subject), 1-200 chars. Leave out to browse the whole catalog with a list or filters. An ISBN is a `400` |
| `list` | string | none | `bestsellers` (the site's bestseller order), `deals` (ThriftBooks Deals) or `new_releases`; combines with query and filters |
| `sort` | string | `most_popular` | `most_popular`, `relevance` (top matches), `bestsellers`, `title_asc`, `title_desc`, `newest`, `oldest` (publication date); `bestsellers` is the default with `list` bestsellers |
| `page` | integer | 1 | 1-1000; `page` x `page_size` must be at most 10,000 |
| `page_size` | integer | 25 | 1-50 works per page |
| `format` | string, integer or array | none | Up to 10: `paperback`, `hardcover`, `mass_market_paperback`, `library_binding`, `audio_cd`, `mp3_cd`, `audio_cassette`, `perfect_paperback`, `board_book`, `comic`, `dvd`, `blu_ray`, `4k_ultra_hd`, or a `format_id` an answer lists |
| `condition` | string or array | none | Up to 10: `new`, `like_new`, `very_good`, `good`, `acceptable` |
| `language` | string, integer or array | none | Up to 10: `english`, `spanish`, `french`, `german`, `italian`, `chinese`, `russian`, `portuguese`, `polish`, `japanese`, `dutch`, `turkish`, `korean`, `greek`, or an id from `facets.languages` |
| `genre` | integer or array | none | Genre ids from `facets.genres[].id` or `facets.age_ranges[].id` (13207 Fiction, 15013 Science Fiction & Fantasy) |
| `min_price`, `max_price` | integer | none | Whole US dollars, 0-10000 |
| `deals`, `new_releases`, `collectible`, `signed`, `first_edition`, `large_print` | boolean | false | Only works with that flag |
| `include_out_of_stock` | boolean | false | Also list works with no copy for sale now |

### ISBN (`/isbn`), work (`/work`), edition (`/edition`), copies (`/copies`)

`/isbn` takes `isbn` (required, ISBN-10 or ISBN-13, dashes and spaces allowed; the check digit is verified, so a typo is an unbilled `400`; an ISBN-10 is converted to ISBN-13). `/work` takes `work_id` (required, `246187`). `/edition` and `/copies` take `edition_id` (required, `49364660`). Ids are digits, as a string or an integer.

### Editions (`/editions`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `work_id` | string or integer | required | A ThriftBooks work id |
| `format`, `condition` | as search | none | Editions: filter by format and condition |
| `sort` | string | `bestselling` | Editions: `bestselling`, `newest`, `oldest`, `price_asc`, `price_desc` |
| `in_stock_only` | boolean | true | Editions: false lists every edition, with or without a copy now |
| `page` | integer | 1 | 1-1000; editions 25 per page (`total_pages`), reviews 10 per page (`has_next`) |

### Suggestions (`/suggestions`)

`query` (required, 1-100 chars): title and author completions as given.

## Examples

### Price table of a work by ISBN

```bash
curl -X POST https://api.scavio.dev/api/v1/thriftbooks/isbn \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"isbn": "9780593135204"}'
```

Captured `data` (2026-11-27; 1 of 4 formats shown and 2 of its 5 condition rows; `notes` and the per-row `image` dropped):

```json
{
  "store": "thriftbooks",
  "host": "www.thriftbooks.com",
  "country": "us",
  "currency": "USD",
  "language": "en",
  "isbn": "9780593135204",
  "isbn13": "9780593135204",
  "isbn10": "0593135202",
  "work_id": 26830049,
  "edition_id": 49364660,
  "format_count": 4,
  "in_stock": true,
  "low_price": 17.25,
  "high_price": 23.92,
  "formats": [
    {
      "format": "Hardcover",
      "format_id": 45,
      "in_stock": true,
      "low_price": 23.92,
      "high_price": 23.92,
      "default_edition": { "edition_id": 49364660, "isbn": "0593135202", "ean": "9780593135204" },
      "conditions": [
        {
          "condition": "New",
          "condition_id": 1,
          "in_stock": true,
          "price": 23.92,
          "list_price": 32,
          "quantity": 500,
          "edition_id": 49364660,
          "copy_id": 44733346,
          "format_id": 45,
          "isbn": "0593135202",
          "ean": "9780593135204",
          "ex_library": false,
          "no_dust_jacket": false,
          "no_cd": false,
          "thrift_deal": false,
          "promotion": null,
          "loyalty_bonus_points": 0,
          "shipping_surcharge": null,
          "est_days_to_ship": 1,
          "ship_country_restriction": false,
          "requested_edition": true
        },
        {
          "condition": "Like New",
          "condition_id": 2,
          "in_stock": false,
          "price": null,
          "list_price": null,
          "quantity": 0,
          "edition_id": null,
          "copy_id": null,
          "format_id": 45,
          "isbn": null,
          "ean": null,
          "ex_library": null,
          "no_dust_jacket": null,
          "no_cd": null,
          "thrift_deal": false,
          "promotion": null,
          "loyalty_bonus_points": 0,
          "shipping_surcharge": null,
          "est_days_to_ship": null,
          "ship_country_restriction": false,
          "requested_edition": false
        }
      ]
    }
  ]
}
```

The other formats were Paperback (New $17.25, list $22, quantity 499, edition `65269440`), MP3 CD and Audio CD, both with no copy in stock. `quantity` 500 on the hardcover means 500 or more. `requested_edition` marks the rows of the edition ThriftBooks matched to the ISBN; send `edition_id` to `/edition` or `/copies` for that edition alone. An ISBN ThriftBooks does not carry is a charged `404`: "ThriftBooks has no book with ISBN <isbn>." (the ISBN as sent).

### Used prices by condition for a work

```bash
curl -X POST https://api.scavio.dev/api/v1/thriftbooks/work \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"work_id": 246187}'
```

The Hunger Games (2026-11-27), `format_count` 4, `low_price` 7.19, `high_price` 34.59; the in-stock rows:

| Format | Condition | Price | List price | Quantity | Copy flags |
|---|---|---|---|---|---|
| Hardcover | New | 17.90 | 22.99 | 500 (500 or more) | |
| Hardcover | Good | 9.29 | 22.99 | 1 | `no_dust_jacket` |
| Hardcover | Acceptable | 15.09 | 22.99 | 2 | `ex_library` |
| Paperback | New | 12.74 | 14.99 | 499 | |
| Paperback | Very Good | 34.59 | null | 1 | |
| Paperback | Good | 16.79 | null | 2 | |
| Paperback | Acceptable | 7.19 | 12.99 | 2 | |
| Audio CD | New | 31.82 | 44.99 | 3 | |
| Library Binding | New | 24.95 | 33.35 | 500 (500 or more) | `est_days_to_ship` 60 |

Like New was out of stock in every format. A condition is not a price ladder: the Hardcover Good copy without a dust jacket ($9.29) sat below the ex-library Acceptable copy ($15.09). An unknown work is a charged `404`: "No ThriftBooks work has id 999999999."

### One search result

```bash
curl -X POST https://api.scavio.dev/api/v1/thriftbooks/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "project hail mary", "page_size": 10}'
```

Captured `data.items[0]` (2026-11-27; `total` 3, 1 page; facets for genres, age ranges, product types, formats, conditions and languages):

```json
{
  "position": 1,
  "work_id": 26830049,
  "title": "Project Hail Mary",
  "authors": [{ "id": 1407958, "name": "Andy Weir" }],
  "series": [],
  "in_stock": true,
  "buy_now": {
    "price": 29.99,
    "condition": "New",
    "condition_id": 1,
    "format": "Hardcover",
    "format_id": 45,
    "edition_id": 75399220,
    "copy_id": 88636777,
    "isbn": "B0GTD7TC9V",
    "publisher": "Random House Publishing Group",
    "release_date": "2026-12-01",
    "ex_library": false,
    "no_dust_jacket": false,
    "no_cd": false
  },
  "low_price": 17.25,
  "high_price": 29.99,
  "list_price": 40,
  "available_copies": 500,
  "edition_count": 27,
  "collectible_count": 0,
  "collectible_low_price": null,
  "thrift_deal": false,
  "backorder": false,
  "book_language": "English",
  "rating": null,
  "review_count": 0,
  "image": "https://i.thriftbooks.com/api/imagehandler/l/A29B3859612BC53E622F6673C8CCB30DC7531A58.jpeg",
  "edition_image": "https://i.thriftbooks.com/api/imagehandler/l/DBBD04F2C92B97FE34A095B9617AA788A4823EE0.jpeg"
}
```

`buy_now` here is a new hardcover edition at $29.99, while the work's `low_price` is $17.25 (the New paperback): quote the copy the user means. `isbn` is as ThriftBooks lists it; an edition without an ISBN can carry another catalog code there (`B0GTD7TC9V`). The other two results were the Spanish deluxe edition and a Spanish box set. `{"list": "bestsellers", "page_size": 10}` answered the whole catalog in bestseller order (`total` 11,593,338): House of Flame and Shadow first (`buy_now` Acceptable $11.59, range $11.09-$66.34, series Crescent City 3), then A Court of Splintered Harmony and Dog Man: A Sprinkle in Time.

### Edition, copies, editions, reviews and suggestions

- `/edition` `{"edition_id": 49364660}`: Project Hail Mary, Hardcover, ISBN 0593135202 / 9780593135204, Random House Publishing Group, 2021-05-04, 496 pages, English, `list_price` 32, `lowest_new_price` 23.92, `lowest_used_price` null, `has_used_copies` false, `available_copies` 500, one copy (New, $23.92, quantity 500), and `description` (the start of the overview, about 300 characters). An unknown edition is a charged `404`: "No ThriftBooks edition has id 999999999."
- `/copies` `{"edition_id": 4587405}` (The Hunger Games hardcover, 2008): `count` 1, a Good copy at $9.29, quantity 1, `no_dust_jacket` true. An empty list means no copy is in stock (or no edition has the id).
- `/editions` `{"work_id": 246187}`: `total` 33 in-stock editions, 2 pages of 25; the first, the 2010 Scholastic paperback (`5277544`, list $14.99), had one Acceptable copy at $5.29 and `others_watching` 515; `top_formats` Paperback, Hardcover, Mass Market Paperback, Library Binding, Audio CD, Board book, Tankobon Hardcover, MP3 CD. An empty list means no edition matches (or no work has the id).
- `/reviews` `{"work_id": 26830049}`: 10 reviews, `has_next` true, each with `review_id`, `rating`, `headline` ("Great read"), `text`, `date`, `verified_purchase`, `likes` and `dislikes`. No reviewer names.
- `/suggestions` `{"query": "hunger"}`: The Hunger Games, Hunger Games Series 1-5, The Hunger Games 4 Book Box Set, A Hunger Like No Other, Hunger: A Novel, and an author name (6).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def thriftbooks(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/thriftbooks/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. ISBN to the work's price table (1 credit)
book = thriftbooks("isbn", {"isbn": "9780439023528"})["data"]

# 2. Every in-stock row: format, condition, price, quantity (500 means 500 or more)
for f in book["formats"]:
    for c in f["conditions"]:
        if c["in_stock"]:
            qty = "500+" if c["quantity"] >= 500 else c["quantity"]
            print(f["format"], c["condition"], c["price"], c["list_price"], qty, c["ex_library"], c["no_dust_jacket"])

# 3. Lowest-priced paperback editions of the same work (1 credit)
eds = thriftbooks("editions", {"work_id": book["work_id"], "format": "paperback", "sort": "price_asc"})["data"]
for e in eds["editions"][:5]:
    print(e["edition_id"], e["publisher"], e["release_date"], e["low_price"])

# Used copies sell one at a time. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency`, `language` and `notes`.

- **search** - `query`, `list`, `sort`, `page`, `page_size`, `total`, `total_pages`, `did_you_mean`, `applied_filters` {`format_ids`, `condition_ids`, `language_ids`, `genre_ids`, `min_price`, `max_price`, `deals`, `new_releases`, `collectible`, `signed`, `first_edition`, `large_print`, `include_out_of_stock`}, `count`, `items[]` {`position`, `work_id`, `title`, `authors[]` {`id`, `name`}, `series[]` {`id`, `name`, `number`}, `in_stock`, `buy_now` {`price`, `condition`, `condition_id`, `format`, `format_id`, `edition_id`, `copy_id`, `isbn`, `publisher`, `release_date`, `ex_library`, `no_dust_jacket`, `no_cd`}, `low_price`, `high_price`, `list_price`, `available_copies`, `edition_count`, `collectible_count`, `collectible_low_price`, `thrift_deal`, `backorder`, `book_language`, `rating`, `review_count`, `image`, `edition_image`}, `facets` {`genres`, `age_ranges`, `product_types` [{`id`, `name`, `count`, `selected`}], `formats`, `conditions`, `languages` [{`id`, `name`, `selected`}]}.
- **isbn / work** - (`isbn`, `isbn13`, `isbn10`, `edition_id` on isbn), `work_id`, `format_count`, `in_stock`, `low_price`, `high_price`, `formats[]` {`format`, `format_id`, `in_stock`, `low_price`, `high_price`, `default_edition` {`edition_id`, `isbn`, `ean`}, `conditions[]` {`condition`, `condition_id`, `in_stock`, `price`, `list_price`, `quantity`, `edition_id`, `copy_id`, `format_id`, `isbn`, `ean`, `ex_library`, `no_dust_jacket`, `no_cd`, `thrift_deal`, `promotion`, `loyalty_bonus_points`, `shipping_surcharge`, `est_days_to_ship`, `ship_country_restriction`, `image`, `requested_edition` (isbn)}}.
- **edition** - `edition_id`, `title`, `authors` (as given), `format`, `isbn`, `isbn13`, `upc`, `publisher`, `release_date`, `pages`, `book_language`, `large_print`, `age_range`, `grade_range`, `list_price`, `in_stock`, `buy_now` {`price`, `condition`, `copy_id`}, `low_price`, `high_price`, `lowest_new_price`, `lowest_used_price`, `has_new_copies`, `has_used_copies`, `available_copies`, `backorder`, `thriftbooks_sales_rank`, `description` (a short overview excerpt), `image`, `copies[]` (as copies).
- **copies** - `edition_id`, `count`, `copies[]` {`copy_id`, `edition_id`, `condition`, `condition_id`, `price`, `quantity`, `ex_library`, `no_dust_jacket`, `no_cd`, `backorder`}.
- **editions** - `work_id`, `sort`, `in_stock_only`, `applied_filters` {`format_ids`, `condition_ids`}, `page`, `per_page`, `total`, `total_pages`, `count`, `editions[]` {`edition_id`, `title`, `edition_description`, `authors[]` {`id`, `name`}, `format`, `isbn`, `ean`, `upc`, `publisher`, `release_date`, `pages`, `book_language`, `large_print`, `age_range`, `grade_range`, `list_price`, `in_stock`, `low_price`, `others_watching`, `image`, `copies[]` (as copies, plus `thrift_deal`)}, `top_formats[]` {`format`, `format_id`}.
- **reviews** - `work_id`, `page`, `per_page`, `has_next`, `count`, `reviews[]` {`review_id`, `rating`, `headline`, `text`, `date`, `verified_purchase`, `likes`, `dislikes`}.
- **suggestions** - `query`, `count`, `suggestions[]` (strings).

## Guardrails

- Name it "ThriftBooks (thriftbooks.com, the US online used-book seller)" on first mention. ThriftBooks accounts and ReadingRewards balances are not read.
- Prices: quote the format, the condition, `price`, `list_price` where given and the `fetched_at` date. Prices are what a visitor who is not signed in sees on the US storefront; never call any price a member price.
- Quantities: a New `quantity` of 500, and an `available_copies` of 500 or more, are lower bounds: write "500 or more", never "500". Never promise that a copy will still be there; used copies sell one at a time.
- Out-of-stock rows: when `in_stock` is false, the row has no price; never quote its ids or a price for it.
- Overviews: quote at most the short `description` excerpt `/edition` returns, and never reproduce an `/editions` `edition_description` in full. Do not republish ThriftBooks images; link books by work or edition id instead.
- Comparing ThriftBooks with Barnes & Noble, Amazon or eBay: compare the same edition (same ISBN-13) and condition, each with its date. A used copy and a new copy are different products. Never call one seller cheaper beyond the numbers shown.
- Reviews: no reviewer names or ids are returned. Quote a review as "a ThriftBooks customer review".
- Not available: member or cart prices, price history (poll and store), sold prices, buyback quotes, account data, wish lists, cart or checkout. This API cannot reserve or buy a copy.
- Terms: Scavio does not store ThriftBooks data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. ThriftBooks' terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, quantities, ISBNs, work, edition or copy ids, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: an ISBN sent as a search query ("query is an ISBN: ThriftBooks search does not match ISBNs. Send it to /api/v1/thriftbooks/isbn instead."); a search past the site's depth ("ThriftBooks pages a search up to 10000 results: page x page_size must be at most 10000. Narrow the search with filters."); "max_price must be at least min_price."; an invalid ISBN ("isbn must be a valid ISBN-10 or ISBN-13 (check digit included), e.g. 9780593135204 or 0439023521."); an id that is not digits ("work_id must be a ThriftBooks id: digits only, e.g. 26830049."); an unknown format, condition or language name ("is not one of ... (or send the numeric id an answer lists)."); more than 10 filter values; "query is required" on suggestions; a `sort`, `list`, `page` or `page_size` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "ThriftBooks has no book with ISBN <isbn>.", "No ThriftBooks work has id <id>.", "No ThriftBooks edition has id <id>.", "Nothing was found for this search.", "No suggestions were found.". `/copies` and `/editions` answer an empty list instead of a 404. Take work and edition ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api).
- `502` means ThriftBooks data was temporarily unavailable ("ThriftBooks is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.100.0
npm install scavio@0.101.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.thriftbooks.search({ query: "project hail mary", condition: ["like_new", "very_good"] });
const { data: best } = await scavio.thriftbooks.search({ list: "bestsellers", genre: [13207] });
const { data: book } = await scavio.thriftbooks.isbn({ isbn: "9780593135204" });
const { data: table } = await scavio.thriftbooks.work({ work_id: "246187" });
const { data: edition } = await scavio.thriftbooks.edition({ edition_id: "49364660" });
const { data: copies } = await scavio.thriftbooks.copies({ edition_id: "4587405" });
const { data: eds } = await scavio.thriftbooks.editions({ work_id: "246187", sort: "price_asc" });
const { data: reviews } = await scavio.thriftbooks.reviews({ work_id: "26830049", page: 2 });
const { data: typed } = await scavio.thriftbooks.suggestions({ query: "hunger" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.thriftbooks.search(...)`, `isbn`, `work`, `edition`, `copies`, `editions`, `reviews` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_thriftbooks`, `get_thriftbooks_isbn`, `get_thriftbooks_work`, `get_thriftbooks_edition`, `get_thriftbooks_copies`, `get_thriftbooks_editions`, `get_thriftbooks_reviews` and `get_thriftbooks_suggestions`. ThriftBooks is opt-in: add `thriftbooks` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.100.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,thriftbooks"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/thriftbooks-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [isbn](https://scavio.dev/docs/thriftbooks-isbn?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [work](https://scavio.dev/docs/thriftbooks-work?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [edition](https://scavio.dev/docs/thriftbooks-edition?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [copies](https://scavio.dev/docs/thriftbooks-copies?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [editions](https://scavio.dev/docs/thriftbooks-editions?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [reviews](https://scavio.dev/docs/thriftbooks-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api), [suggestions](https://scavio.dev/docs/thriftbooks-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api). Overview: [ThriftBooks API](https://scavio.dev/thriftbooks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=thriftbooks-api).
