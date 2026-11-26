---
name: goodreads-api
description: Goodreads API for Goodreads (goodreads.com, Amazon's book community, one global English site) - how readers rate a book, as Goodreads shows it (Dune read 4.29 from 1,732,454 ratings, 907,135 of them 5 stars and 26,357 1 star, with 90,953 reviews in 54 languages and a $9.99 Kindle price as Goodreads gave it) with the full star distribution, review counts per language, genres, series, awards, places, characters, ISBN-10, ISBN-13 and ASIN; one book by id, link or ISBN; reader reviews 30 per page in Goodreads' own sorts (popular, newest, oldest) with star, language and this-edition filters, up to 4 pages (120 reviews) per call, without reviewer names; book, Listopia list and quote search, 20 per page; type-ahead book suggestions; an author's page with bio, followers and top books, and every book of an author 30 per page in 5 sorts; a series in reading order; every edition of a work 10 per page in 6 sorts; a Listopia list 100 books per page in vote order with score and votes, the lists that contain a book, and list search; quotes by words, tag or book with like counts; a genre's 50 most shelved books or this week's most read; new releases by genre or month. 14 endpoints, 1 credit per call. English site, USD Kindle prices. No reviewer names or profiles, no user shelves, no reviews past 4 pages from one view, no Choice Awards.
version: 1.0.0
tags: goodreads, goodreads-com, goodreads-api, goodreads-books, goodreads-ratings, goodreads-reviews, goodreads-book-reviews, goodreads-search, goodreads-isbn, goodreads-author, goodreads-series, goodreads-editions, goodreads-lists, goodreads-listopia, goodreads-quotes, goodreads-genres, goodreads-new-releases, goodreads-most-read, book-data, book-ratings, book-reviews, book-metadata, isbn-lookup, isbn-13, asin, book-search, author-data, book-series, book-editions, reading-lists, book-quotes, new-book-releases, publishing, book-market-research, reader-sentiment, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 150
    throttle: 1
    homepage: https://scavio.dev/goodreads-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api
---

# Goodreads API - Book Ratings, Reviews, Authors, Lists

Read Goodreads (goodreads.com, Amazon's book community): one book in full with its rating, star distribution, review counts per language, genres, series, awards and identifiers; reader reviews with Goodreads' own sorts and filters; book, list and quote search and type-ahead suggestions; authors and their books; series and editions; Listopia lists; quotes; genres; and new releases. Every answer is what Goodreads' public pages show a visitor without an account at the moment of the call. All 14 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Goodreads shows to any visitor and returns them as JSON for analysis. It uses no Goodreads account, no shelves, no ratings or reviews of its own, no friend or group feature and no purchase link.

**The job this skill is for: how readers rate and review a book, next to the book's own facts.** `/book` returns Goodreads' average rating, the count behind it, the full 1-5 star distribution, the review counts per review language and the first 30 reviews in Goodreads' popular order, all in one call; `/reviews` reads up to 120 more of one view, sorted and filtered. Captured 2026-11-26 (1 credit per call):

| Book (request) | `rating`, `ratings_count` | 5 stars / 1 star (`rating_distribution`) | `reviews_count` / `reviews_total` | Review languages | `kindle.price` (as Goodreads gives it) |
|---|---|---|---|---|---|
| Dune, Frank Herbert (`book_id` 44767458) | 4.29, 1,732,454 | 907,135 / 26,357 | 91,243 / 90,953 | 54 | 9.99 USD |
| Project Hail Mary, Andy Weir (`book_id` 54493401) | 4.51, 1,952,255 | 1,217,140 / 9,049 | 267,088 / 266,503 | 53 | 14.99 USD |
| Onyx Storm, Rebecca Yarros (`book_id` 209439446) | 4.22, 2,016,940 | 956,030 / 18,268 | 226,261 / 225,771 | 49 | 14.99 USD |
| Atomic Habits, James Clear (`isbn` 9780735211292, book 59910150) | 4.3, 1,451,154 | 737,722 / 15,479 | 84,823 / 84,575 | 57 | 12.99 USD |

The rating and counts are Goodreads' figures for the work across its editions, as its book page shows them. Quote each with the book, the count behind it and the capture date. A 1-star review view is not the 1-star rating count: `/reviews` with `stars: 1` on Atomic Habits counted 1,145 reviews in its view, while its `rating_distribution` counts 15,479 1-star ratings: the two measure different things, so quote each with its label. For the same title on a store use `amazon-product-data` (matched on ISBN or ASIN).

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent; a 4-page review read is still 1 credit. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Two review counts.** `reviews_count` is the count on Goodreads' book statistics (91,243 for Dune) and `reviews_total` the count on its review list (90,953). Quote each with its label.
- **Up to 4 review pages per call.** `/reviews` reads 30 reviews a page, `pages` 1 to 4 (up to 120 reviews of one view). Goodreads has no jump to a deeper page, so a call always starts from the first page of the view; narrow with `sort`, `stars`, `language` or `edition_only` to reach other reviews. `pages_read` says how many pages came back.
- **Sorted and filtered reviews are slower.** The default view (popular, one page, no filter) answered in about 3 to 5 seconds in the captures; a sort, a filter or more than one page opens the review page and reads what it shows: 13 to 31 seconds in the captures, up to about 2 minutes. Set a client timeout of at least 150 seconds.
- **No reviewer names.** Reviews carry `review_id`, `rating`, dates, `text`, `spoiler`, `recommend_for`, `likes` and `comments`. Reviewer names, avatars and profile links are never returned, and profile links are cut out of review text. Lists come without their creator.
- **Search has no sort and no field filter.** `/search` is Goodreads' own search box: 20 results a page in Goodreads' order, `total_text` as Goodreads words it ("over 111k") and `total` only when Goodreads gives an exact count. An ISBN query finds that edition.
- **Kindle prices as Goodreads gives them.** `kindle` {`price`, `currency` (USD), `kindle_unlimited`, `prime_reading`} and `kindle_price` in search are the Kindle price Goodreads prints on its page; Goodreads is one English site and shows USD.
- **Genres show one page.** `/genre` returns the first 50 books of the genre's shelf, most shelved first (`shelved_books` is the shelf's size, capped by Goodreads at 100,000), or `list: "most_read"` for the books most read this week. New releases by month return the first 15 Goodreads shows on its page.
- **Paging per endpoint.** Search, list search and quotes by words 20 a page; author books, book lists and quotes by tag or book 30; editions 10; a list 100. `has_more` says whether another page exists. Search, author books, list search and quotes go to page 100; editions, lists and book lists to page 1,000.
- **What is not there.** No reviewer names or profiles, no user shelves or reading challenges, no friends, groups or discussions, no questions and answers text (counts only), no Choice Awards pages, no reviews past 4 pages of one view, no purchase or price history.

Goodreads retired its official API (no new developer keys since 2020). This skill reads Goodreads' public pages with one Scavio key.

See also: `amazon-product-data` (the same book on Amazon by ASIN or ISBN: price, offers and reviews), `google-search-api` (where a title is discussed on the web) and `reddit-search-api` (reader threads). Same book only: match on ISBN, ASIN or exact title and author, and name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Read a book on Goodreads by title, Goodreads id, link or ISBN: average rating, ratings count, 1-5 star distribution, review counts per language, genres, series, awards, places, characters, page count, publisher, dates, ISBN-10, ISBN-13 and ASIN
- Pull Goodreads reader reviews for a book, sorted popular, newest or oldest, filtered by stars, review language or this edition only
- Search Goodreads books, Listopia lists or quotes, or get type-ahead book suggestions for a partial title, author or ISBN
- Read an author's Goodreads page (bio, born, website, genres, followers, rating, top books, series) or list every book by an author, sorted by year, title, rating or pages
- List a series in reading order, or every edition of a book with publisher, format, ISBN and per-edition rating
- Read a Listopia list with ranks, scores and votes, find the lists a book is on, or search lists by title
- Find quotes by words, tag or book with like counts
- See a genre's most shelved books or this week's most read, and new releases by genre or month

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example 25 books: one book page and one sorted review read each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 0.9-1.7 seconds, search 2.3-4.7, a book 4-8, an author 1.4-7.4, series, editions and author books 1.7-4.5, lists and list search 2-7, book lists 1.7-17, quotes 4.7-5.4, genres and new releases 2.3-9.2, default reviews 2.9-4.5 and sorted, filtered or multi-page reviews 10-31. Set a client timeout of at least 150 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/goodreads/search` | Books (title, author or ISBN), Listopia lists or quotes, 20 per page: rating, ratings and reviews counts, editions count, series, Kindle price, description; lists with books count, voters and top books; quotes with likes | 1 |
| `POST /api/v1/goodreads/book` | One book by id, link or ISBN: rating, star distribution, review counts and languages, genres, series, format, pages, publisher, dates, ISBN, ASIN, awards, places, characters, Kindle price, author profile and the first 30 reviews (no names) | 1 |
| `POST /api/v1/goodreads/reviews` | Reader reviews of one book, 30 per page, up to 4 pages per call: popular, newest or oldest, filtered by stars, language or this edition (no names) | 1 |
| `POST /api/v1/goodreads/suggestions` | The books Goodreads suggests as a reader types a title, author or ISBN | 1 |
| `POST /api/v1/goodreads/author` | One author: born, died, website, genres, influences, bio, rating, ratings and reviews counts, works count, followers, top books, series | 1 |
| `POST /api/v1/goodreads/author-books` | Every book of one author, 30 per page, in 5 sorts | 1 |
| `POST /api/v1/goodreads/series` | One series with every book in reading order (Book 1, Book 2.5 ...) | 1 |
| `POST /api/v1/goodreads/editions` | Every edition of one work, 10 per page, in 6 sorts: publisher, format, pages, ISBN-13, ISBN-10, ASIN, language, per-edition rating | 1 |
| `POST /api/v1/goodreads/list` | One Listopia list, 100 books per page in vote order, with score and votes | 1 |
| `POST /api/v1/goodreads/book-lists` | The Listopia lists that contain one book, with the book's rank on each | 1 |
| `POST /api/v1/goodreads/list-search` | Listopia lists whose title matches, 20 per page, with their top books | 1 |
| `POST /api/v1/goodreads/quotes` | Quotes by search words, by tag or from one book, with tags and likes | 1 |
| `POST /api/v1/goodreads/genre` | A genre's first 50 most shelved books, or the books most read this week in it | 1 |
| `POST /api/v1/goodreads/new-releases` | New releases by genre, or a month's most popular releases across every genre (the first 15) | 1 |

## Market

One global English site, www.goodreads.com. There is no `country`, `language` or `currency` input on the site itself; Kindle prices come in USD as Goodreads shows them. Review text stays in the language the reader wrote it in, and `/reviews` filters by review language (`language`: en, es, fr, de, zh-TW ... as `review_languages` lists them).

## Ratings and review fields

| Field | Meaning |
|---|---|
| `rating`, `ratings_count` | Goodreads' average rating (0-5) and the number of ratings behind it, for the work across its editions |
| `rating_distribution` | {`1`..`5`}: how many readers gave each star count |
| `reviews_count` | The review count on Goodreads' book statistics |
| `reviews_total`, `reviews_shown` | The review list's count, and how many reviews came back on the book answer (30) |
| `review_languages[]` | {`language`, `count`}: reviews per review language, the values `/reviews` takes as `language` |
| `reviews[]` | {`review_id`, `rating` (1-5, `null` when the reader gave no stars), `created_at`, `updated_at`, `text` (plain text), `spoiler`, `recommend_for`, `likes`, `comments`} |
| `total` (reviews) | The count Goodreads gives for the view asked (sort, stars, language, edition) |
| `kindle` | {`price`, `currency` (USD), `price_text`, `kindle_unlimited`, `prime_reading`} as Goodreads shows it |
| `awards[]` | {`name`, `category`, `designation` (winner, nominee), `year`, `url`} |
| `quotes_count`, `questions_count`, `discussions_count` | Goodreads' counts; the texts are not returned except quotes (`/quotes` with `work_id`) |

- **Work and edition.** `book_id` is one edition; `work_id` groups every edition of the book (the input of `/editions` and `/quotes`). `/reviews` covers every edition unless `edition_only: true`.
- **Changes over time:** ratings and counts change as readers add them. Any change you compute between two captures, label as computed with both `fetched_at` dates.

## Workflow

1. **Find the book.** `/suggestions` (`{"query": "sanderson"}`) or `/search` (`{"query": "dune"}`) returns `book_id`, `work_id` and the author's `author_id`; an ISBN goes straight to `/book` with `isbn`.
2. **The book.** `/book` with `book_id`: note `rating`, `ratings_count`, `rating_distribution`, `review_languages`, `series[].series_id` and `work_id`.
3. **More reviews.** `/reviews` with `book_id` plus `sort`, `stars`, `language`, `edition_only` and `pages` (1-4). Check `total`, `pages_read` and `has_more`.
4. **Around the book.** `/editions` with `work_id`, `/series` with `series_id`, `/book-lists` with `book_id`, `/quotes` with `work_id`, `/author` and `/author-books` with `author_id`.
5. **Discovery.** `/genre` with a genre slug (`genres[].slug` of a book), `/new-releases` with `genre` or `month`, `/list` with a `list_id` from `/list-search` or `/book-lists`.
6. **Report.** Each rating with its count and the `fetched_at` date; each review quoted as Goodreads shows it with its stars and date, never with a reviewer's name; Kindle prices as "the Kindle price Goodreads shows".
7. **Over time:** store each answer with its `fetched_at`; ratings, counts, lists and the week's most read change as Goodreads updates them, and that stored set is your record.

## Parameters

### Search (`/search`) and suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search text, 1-200 characters: a title, an author, a phrase or an ISBN (an ISBN finds that edition). Suggestions: 1-100 characters |
| `type` | string | `books` | `/search` only: `books`, `lists` or `quotes` (Goodreads' own search tabs) |
| `page` | integer | 1 | `/search` only: 1-100, 20 per page |

### Book (`/book`) and reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `book_id` | string or integer | one of | A Goodreads book id (`44767458`), or the id with its slug (`44767458-dune`) |
| `url` | string | one of | A goodreads.com book link |
| `isbn` | string | one of | `/book` only: an ISBN-13 or ISBN-10, checksum verified (`9780735211292`): the edition with it |
| `sort` | string | `popular` | `/reviews` only: `popular`, `newest` or `oldest` |
| `stars` | integer | none | `/reviews` only: reviews with this many stars, 1-5 |
| `language` | string | none | `/reviews` only: reviews in this language as `review_languages` lists it (`en`, `es`, `fr`, `de`, `zh-TW` ...) |
| `edition_only` | boolean | false | `/reviews` only: reviews of this edition only (default: every edition of the work) |
| `pages` | integer | 1 | `/reviews` only: pages of 30 to read in this call, 1-4 (up to 120 reviews of the view) |

### Authors, series, editions, lists, quotes, genres, new releases

| Endpoint | Parameters |
|---|---|
| `/author` | one of `author_id` (`38550`; `author.author_id` of any answer) or `url` (a goodreads.com author link) |
| `/author-books` | one of `author_id` or `url`; `sort` `popularity` (default), `original_publication_year`, `title`, `average_rating` or `number_of_pages`; `page` 1-100 (30 per page) |
| `/series` | one of `series_id` (`49075`; `series[].series_id` of a book answer) or `url` |
| `/editions` | one of `work_id` (`3634639`; `work_id` of a book answer) or `url` (a goodreads.com work editions link); `sort` `title`, `original_date_published`, `date_published`, `avg_rating`, `num_ratings` or `format` (default Goodreads' own order); `page` 1-1,000 (10 per page) |
| `/list` | one of `list_id` (`1`) or `url` (a goodreads.com list link); `page` 1-1,000 (100 per page) |
| `/book-lists` | one of `book_id` or `url` (a goodreads.com book link); `page` 1-1,000 (30 per page) |
| `/list-search` | `query` (1-200 characters: words in a list's title); `page` 1-100 (20 per page) |
| `/quotes` | one of `query` (words, an author or a book title), `tag` (`love`; `tags[]` of a quote) or `work_id` (quotes from one book); `page` 1-100 (20 per page for `query`, 30 for `tag` and `work_id`) |
| `/genre` | `genre` (required: a genre as its link writes it, `fantasy`, `science-fiction`, `young-adult`, `historical-fiction`; `genres[].slug` of a book); `list` `popular` (default: the first 50 of the genre's shelf, most shelved first) or `most_read` (the books most read this week in the genre). No `page`: Goodreads shows visitors one page of a genre |
| `/new-releases` | one of `genre` (new releases Goodreads tags with it) or `month` (`YYYY-MM`, 2007-01 to 12 months from now: the month's most popular releases across every genre, the first 15) |

## Examples

### One book with its ratings

```bash
curl -X POST https://api.scavio.dev/api/v1/goodreads/book \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"book_id": "44767458"}'
```

Captured `data` (2026-11-26; `description` and the author `bio` shortened, `review_languages` cut to 2 of 54, `genres` to 2 of 10, `awards` to 2 of 3, `reviews` to 1 of 30 and its text shortened; `places`, `characters`, `cover_url`, `author_profile.photo_url`, `authors` and `notes` dropped):

```json
{
  "site": "goodreads.com",
  "requested": {"book_id": "44767458"},
  "book_id": "44767458",
  "work_id": "3634639",
  "url": "https://www.goodreads.com/book/show/44767458-dune",
  "title": "Dune",
  "title_complete": "Dune (Dune, #1)",
  "original_title": "Dune",
  "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world ...",
  "author": {"author_id": "58", "name": "Frank Herbert", "role": "Author", "url": "https://www.goodreads.com/author/show/58.Frank_Herbert", "goodreads_author": false},
  "author_profile": {"bio": "Franklin Patrick Herbert Jr. was an American science fiction author best known for the 1965 novel Dune and its five sequels. ...", "works_count": 652, "followers": 17750},
  "rating": 4.29,
  "ratings_count": 1732454,
  "rating_distribution": {"1": 26357, "2": 56413, "3": 208040, "4": 534509, "5": 907135},
  "reviews_count": 91243,
  "review_languages": [
    {"language": "en", "count": 76378},
    {"language": "es", "count": 4004}
  ],
  "genres": [
    {"name": "Science Fiction", "slug": "science-fiction", "url": "https://www.goodreads.com/genres/science-fiction"},
    {"name": "Fiction", "slug": "fiction", "url": "https://www.goodreads.com/genres/fiction"}
  ],
  "series": [
    {"series_id": "45935", "title": "Dune", "position": "1", "url": "https://www.goodreads.com/series/45935-dune"},
    {"series_id": "106170", "title": "Dune Universe", "position": "14", "url": "https://www.goodreads.com/series/106170-dune-universe"}
  ],
  "format": "Hardcover",
  "pages": 658,
  "publisher": "Ace",
  "published": "2019-10-01",
  "first_published": "1965-06-01",
  "language": "English",
  "isbn": "059309932X",
  "isbn13": "9780593099322",
  "asin": "059309932X",
  "awards": [
    {"name": "Hugo Award", "category": "Best Novel", "designation": "winner", "year": 1966, "url": "https://www.goodreads.com/award/show/9-hugo-award"},
    {"name": "Nebula Award", "category": "Best Novel", "designation": "winner", "year": 1965, "url": "https://www.goodreads.com/award/show/23-nebula-award"}
  ],
  "kindle": {"price": 9.99, "currency": "USD", "price_text": "9.99", "kindle_unlimited": false, "prime_reading": false},
  "quotes_count": 1462,
  "questions_count": 78,
  "discussions_count": 408,
  "editions_url": "https://www.goodreads.com/work/editions/3634639",
  "reviews_total": 90953,
  "reviews_shown": 30,
  "reviews": [
    {"review_id": "amzn1.gr.review:goodreads.v1.tAVEsTgQ5jOonEbHrH_0cA", "rating": 5, "created_at": "2011-03-23T06:09:53.000Z", "updated_at": "2021-09-10T12:38:15.987Z", "text": "In my head, the purpose of this review is very clear. It is to convince YOU to read this book. ...", "spoiler": false, "recommend_for": null, "likes": 3102, "comments": 118}
  ]
}
```

### Reviews with a star filter

```bash
curl -X POST https://api.scavio.dev/api/v1/goodreads/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"book_id": "59910150", "stars": 1}'
```

Captured `data` (2026-11-26; `reviews` cut to 1 of 30 and its text shortened):

```json
{
  "site": "goodreads.com",
  "book": {"book_id": "59910150", "work_id": "62221762", "title": "Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones", "author": "James Clear", "url": "https://www.goodreads.com/book/show/59910150-atomic-habits"},
  "sort": "popular",
  "stars": 1,
  "language": null,
  "edition_only": false,
  "pages_requested": 1,
  "pages_read": 1,
  "page_size": 30,
  "total": 1145,
  "has_more": true,
  "count": 30,
  "reviews": [
    {"review_id": "amzn1.gr.review:goodreads.v1.d91botVxmi45XGryp9YeOQ", "rating": 1, "created_at": "2019-01-26T19:31:39.572Z", "updated_at": "2026-11-16T22:47:53.182Z", "text": "Reading this book feels like reading a homework assignment. ...", "spoiler": false, "recommend_for": null, "likes": 458, "comments": 31}
  ]
}
```

Other captured views: Onyx Storm `newest` in Spanish (`language: "es"`) counted 9,342 reviews; Project Hail Mary `oldest` with `pages: 3` returned 90 reviews of 266,506 in 30.9 seconds; The Alchemist with `edition_only: true` counted 69,137. The default view (no sort, filter or extra page) also returns `rating`, `ratings_count`, `rating_distribution`, `reviews_count` and `review_languages`.

### Search books

```bash
curl -X POST https://api.scavio.dev/api/v1/goodreads/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dune"}'
```

Captured `data` (2026-11-26; `results` cut to 1 of 20, `cover_url` dropped, `description` shortened):

```json
{
  "site": "goodreads.com",
  "query": "dune",
  "type": "books",
  "page": 1,
  "page_size": 20,
  "total": null,
  "total_text": "over 111k",
  "has_more": true,
  "count": 20,
  "results": [
    {
      "position": 1,
      "book_id": "44767458",
      "work_id": "3634639",
      "title": "Dune",
      "url": "https://www.goodreads.com/book/show/44767458-dune",
      "author": {"author_id": "58", "name": "Frank Herbert", "url": "https://www.goodreads.com/author/show/58.Frank_Herbert", "goodreads_author": false},
      "other_authors": [],
      "rating": 4.29,
      "ratings_count": 1732454,
      "reviews_count": 91243,
      "editions_count": 524,
      "published": "2019-10-01",
      "series": [{"series_id": "45935", "title": "Dune", "position": "1", "url": "https://www.goodreads.com/series/45935-dune"}],
      "kindle_price": 9.99,
      "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides ..."
    }
  ]
}
```

`{"query": "courage", "type": "quotes"}` returned 20 quotes of "over 34.7k", each with `quote_id`, `text`, `author`, `book_title`, `likes` (rounded as the search shows it: 34900) and `likes_text` ("34.9k likes").

### A series, editions and lists

```bash
curl -X POST https://api.scavio.dev/api/v1/goodreads/series \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"series_id": "49075"}'
```

Captured (2026-11-26): The Stormlight Archive, `primary_works` 5, `total_works` 27, `count` 27; `books[]` in reading order with `label` "Book 1" (The Way of Kings, 4.66 from 739,918 ratings, 1,007 pages, 2010), "Book 2" (Words of Radiance, 4.76 from 542,716), "Book 2.1", "Book 2.5" (Edgedancer), "Book 3" (Oathbringer) ...

`/editions` with `{"work_id": "3634639", "sort": "num_ratings"}` counted 524 editions of Dune (10 per page); the first, the 2019 Ace Deluxe Edition hardcover (ISBN-13 9780593099322, 658 pages), read 4.34 from 897,707 ratings, the second the 2006 Hodder & Stoughton paperback 4.21 from 568,436. `/book-lists` with `{"book_id": "44767458"}` placed Dune "59th out of 80,324 books" on Best Books Ever (299,523 voters) and "2nd out of 8,923 books" on Best Science Fiction & Fantasy Books. `/list` with `{"list_id": "1"}` returned Best Books Ever (80,344 books, 299,515 voters, created May 13th, 2008), 100 a page, rank 1 The Hunger Games (score 4,591,785, 46,656 votes).

### Authors, quotes, genres and new releases

`/author` with `{"author_id": "38550"}`: Brandon Sanderson, a Goodreads Author since January 2010, 4.39 from 10,073,402 ratings, 825,233 reviews, 464 works, 299,148 followers, 10 top books and 5 series. `/author-books` with `{"author_id": "38550", "sort": "original_publication_year"}`: 30 a page, `has_more` true. `/quotes` with `{"work_id": "3634639"}`: 1,462 Dune quotes, the first with 17,117 likes and 5 tags. `/genre` with `{"genre": "fantasy"}`: the first 50 of a shelf Goodreads counts at 100,000 (its cap), rank 1 with 91,113 shelvings. `/new-releases` with `{"month": "2026-11"}`: the first 15 of November 2026, rank 1 Peculiar Stars (Rebecca Yarros, `count` 121,794, 4.7 from 24,299 ratings), rank 2 The Last King of Faerie (Cassandra Clare, `count` 94,206).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def goodreads(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/goodreads/{endpoint}", headers=HEADERS, json=body, timeout=150)
    r.raise_for_status()
    return r.json()

# The book by ISBN (1 credit)
b = goodreads("book", {"isbn": "9780735211292"})["data"]
print(b["title"], b["rating"], b["ratings_count"], b["rating_distribution"])
for lang in b["review_languages"][:5]:
    print("  ", lang["language"], lang["count"])

# The newest 1-star reviews, two pages (1 credit)
r = goodreads("reviews", {"book_id": b["book_id"], "stars": 1, "sort": "newest", "pages": 2})["data"]
print("view total", r["total"], "read", r["count"], "pages", r["pages_read"])
for rev in r["reviews"][:3]:
    print(rev["created_at"][:10], rev["rating"], rev["likes"], rev["text"][:80])

# Every edition, most rated first (1 credit)
e = goodreads("editions", {"work_id": b["work_id"], "sort": "num_ratings"})["data"]
for ed in e["editions"]:
    print(ed["isbn13"], ed["format"], ed["publisher"], ed["rating"], ed["ratings_count"])

# Store each answer with fetched_at: that stored set is your record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `site` ("goodreads.com"); book, reviews, genre and new-release answers can carry `notes`.

- **book card** (search, suggestions, author, author books, series, list, genre, new releases) - `book_id`, `work_id`, `title`, `url`, `cover_url`, `author` {`author_id`, `name`, `url`, `goodreads_author`}, `rating`, `ratings_count`, plus per endpoint: `position`, `other_authors`, `reviews_count`, `editions_count`, `published`, `published_year`, `series`, `kindle_price`, `description` (search); `title_bare`, `pages` (suggestions, series); `label`, `position` (series); `rank`, `score`, `votes` (list); `shelved_count` (genre popular); `rank`, `count` (new releases by month).
- **book** - `requested`, `book_id`, `work_id`, `url`, `title`, `title_complete`, `original_title`, `description`, `cover_url`, `author`, `authors[]` {`author_id`, `name`, `role`, `url`, `goodreads_author`}, `author_profile` {`bio`, `photo_url`, `works_count`, `followers`}, `rating`, `ratings_count`, `rating_distribution`, `reviews_count`, `review_languages[]`, `genres[]` {`name`, `slug`, `url`}, `series[]` {`series_id`, `title`, `position`, `url`}, `format`, `pages`, `publisher`, `published`, `first_published`, `language`, `isbn`, `isbn13`, `asin`, `awards[]`, `places[]` {`name`, `country`, `year`, `url`}, `characters[]` {`name`, `url`}, `kindle`, `quotes_count`, `questions_count`, `discussions_count`, `editions_url`, `reviews_total`, `reviews_shown`, `reviews[]`, `notes`.
- **reviews** - `book` {`book_id`, `work_id`, `title`, `author`, `url`}, `sort`, `stars`, `language`, `edition_only`, `pages_requested`, `pages_read`, `page_size`, `total`, `has_more`, `count`, `reviews[]`; the default view adds `rating`, `ratings_count`, `rating_distribution`, `reviews_count`, `review_languages`.
- **search** - `query`, `type`, `page`, `page_size`, `total`, `total_text`, `has_more`, `count`, `results[]`: book cards, or lists {`position`, `list_id`, `title`, `url`, `books_count`, `voters`, `sponsored`, `top_books`}, or quotes {`position`, `quote_id`, `text`, `author`, `author_quotes_url`, `book_title`, `likes`, `likes_text`, `url`}.
- **author** - `author_id`, `name`, `url`, `goodreads_author`, `photo_url`, `born` {`date`, `place`}, `died`, `website`, `genres[]`, `influences[]`, `member_since`, `bio`, `rating`, `ratings_count`, `reviews_count`, `works_count`, `followers`, `top_books[]`, `series[]` {`series_id`, `title`, `url`}. **author books** - `author_id`, `author`, `sort`, `page`, `page_size`, `has_more`, `count`, `books[]`.
- **series** - `series_id`, `url`, `title`, `primary_works`, `total_works`, `description`, `count`, `books[]`. **editions** - `work_id`, `title`, `author`, `first_published`, `book_url`, `sort`, `page`, `page_size`, `total`, `has_more`, `count`, `editions[]` {`book_id`, `title`, `url`, `cover_url`, `published`, `publisher`, `format`, `edition`, `pages`, `isbn13`, `isbn10`, `asin`, `language`, `authors`, `rating`, `ratings_count`}.
- **list** - `list_id`, `url`, `title`, `description`, `books_count`, `voters`, `created`, `tags`, `page`, `page_size`, `has_more`, `count`, `books[]`. **book lists** - `book_id`, `title`, `page`, `page_size`, `has_more`, `count`, `lists[]` {`list_id`, `title`, `url`, `rank`, `rank_text`, `books_count`, `voters`}. **list search** - `query`, `page`, `page_size`, `total`, `total_text`, `has_more`, `count`, `lists[]` {`position`, `list_id`, `title`, `url`, `books_count`, `voters`, `sponsored`, `top_books[]`}.
- **quotes** - `query`, `tag`, `work_id`, `title`, `page`, `page_size`, `total`, `has_more`, `count`, `quotes[]` {`quote_id`, `text`, `author`, `book` {`title`, `work_id`, `quotes_url`}, `tags`, `likes`, `url`}.
- **genre** - `genre`, `list`, `title`, `shelved_books` (popular), `count`, `books[]` (most_read: `position`, `book_id`, `title`, `url`, `cover_url`), `notes`. **new releases** - `genre`, `month`, `list_name` or `title`, `has_more` (month), `count`, `books[]` (genre: `position`, `book_id`, `title`, `url`, `cover_url`; month: `rank`, `count`, book card, `reviews_count`, `description`), `notes`.

## Guardrails

- Name it "Goodreads (goodreads.com, Amazon's book community)" on first mention, "Goodreads" after that.
- Ratings: quote each with its count and date ("4.29 from 1,732,454 ratings on Goodreads, Dune, fetched Nov 26, 2026"). Say which review count you quote (`reviews_count` or `reviews_total`, or a view's `total`). Any share or change you compute, label as computed.
- Reviews: no reviewer is named or identified; quote review text as Goodreads shows it, with its stars and date, and say how many of the view's `total` were read. Respect `spoiler: true` and say a review is marked as a spoiler before quoting it.
- Authors are public creators and may be named as book metadata; do not add personal details beyond what their Goodreads page shows.
- Kindle prices: "the Kindle price Goodreads shows (USD)", with the date; never a store's current price.
- Descriptive only: no commentary on Goodreads' business, its ranking of lists or its policies.
- Do not republish Goodreads review text, descriptions, covers or quotes in bulk. Write goodreads.com as plain text and cite book ids, work ids, list ids and capture dates rather than linking Goodreads pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account. Goodreads' terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate ratings, counts, reviews, ISBNs, ids or quotes. Return what the API returned, with the `fetched_at` time.
- Not available: reviewer names or profiles, user shelves, friends, groups, discussion and question texts, Choice Awards, reviews past 4 pages of one view, price history, purchases.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: `/book` without exactly one of `book_id`, `url` or `isbn` ("send one of book_id, url or isbn"); an ISBN that fails its checksum ("isbn must be a valid ISBN-10 or ISBN-13 (e.g. 9780593099322)."); an id that is not digits or a goodreads.com link ("book_id must be a Goodreads id (digits, e.g. 44767458) or its goodreads.com link.", "url must be a Goodreads id or a goodreads.com link."); `/reviews` without exactly one of `book_id` or `url`, `stars` outside 1-5, `pages` outside 1-4, a `language` that is not a language code ("language must be a language code as Goodreads lists it (e.g. en, es, fr, zh-TW)."); a `sort`, `type` or `list` outside its list; `page` past its maximum ("page must be an integer from 1 to 100."); `/quotes` without exactly one of `query`, `tag` or `work_id` ("send one of query, tag or work_id."); `/genre` with a `page` ("page: Goodreads shows one page of a genre (the first 50 of the shelf, or the week's most read)."); `/new-releases` without exactly one of `genre` or `month` ("send one of genre or month."), a month that is not `YYYY-MM` ("month must be YYYY-MM (e.g. 2026-11).") or outside its window ("month must be YYYY-MM between 2007-01 and 12 months from now.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Goodreads has no book 999999999999.", "Goodreads has no book with ISBN ...", "Goodreads has no author ...", "Goodreads has no series ...", "Goodreads has no work ... (work_id: book work_id).", "Goodreads has no list ...", "Goodreads has no genre ...", "Goodreads has no release list for ...", and "Goodreads lists no reviews in language cy for book 59910150 (review_languages on a plain reviews call lists them).". Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api).
- `502` means Goodreads data was temporarily unavailable ("Goodreads is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Goodreads is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: book } = await scavio.goodreads.book({ isbn: "9780735211292" });
const { data: reviews } = await scavio.goodreads.reviews({ book_id: "59910150", stars: 1, pages: 2 });
const { data: results } = await scavio.goodreads.search({ query: "dune" });
const { data: author } = await scavio.goodreads.author({ author_id: "38550" });
const { data: books } = await scavio.goodreads.authorBooks({ author_id: "38550", sort: "original_publication_year" });
const { data: editions } = await scavio.goodreads.editions({ work_id: "3634639", sort: "num_ratings" });
const { data: lists } = await scavio.goodreads.bookLists({ book_id: "44767458" });
const { data: found } = await scavio.goodreads.listSearch({ query: "fantasy" });
const { data: releases } = await scavio.goodreads.newReleases({ month: "2026-11" });
```

The other methods are `suggestions`, `series`, `list`, `quotes` and `genre`. In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.goodreads.search(...)`, `book`, `reviews`, `suggestions`, `author`, `author_books`, `series`, `editions`, `list`, `book_lists`, `list_search`, `quotes`, `genre` and `new_releases`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 14 endpoints as tools: `search_goodreads`, `get_goodreads_book`, `get_goodreads_reviews`, `get_goodreads_suggestions`, `get_goodreads_author`, `get_goodreads_author_books`, `get_goodreads_series`, `get_goodreads_editions`, `get_goodreads_list`, `get_goodreads_book_lists`, `search_goodreads_lists`, `get_goodreads_quotes`, `get_goodreads_genre` and `get_goodreads_new_releases`. Goodreads is opt-in: add `goodreads` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,goodreads"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/goodreads-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [book](https://scavio.dev/docs/goodreads-book?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [reviews](https://scavio.dev/docs/goodreads-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [suggestions](https://scavio.dev/docs/goodreads-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [author](https://scavio.dev/docs/goodreads-author?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [author books](https://scavio.dev/docs/goodreads-author-books?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [series](https://scavio.dev/docs/goodreads-series?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [editions](https://scavio.dev/docs/goodreads-editions?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [list](https://scavio.dev/docs/goodreads-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [book lists](https://scavio.dev/docs/goodreads-book-lists?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [list search](https://scavio.dev/docs/goodreads-list-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [quotes](https://scavio.dev/docs/goodreads-quotes?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [genre](https://scavio.dev/docs/goodreads-genre?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api), [new releases](https://scavio.dev/docs/goodreads-new-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api). Overview: [Goodreads API](https://scavio.dev/goodreads-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=goodreads-api).
