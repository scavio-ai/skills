# Estante Virtual API - Used and New Book Prices by ISBN, Copies by Sebo, Shipping by CEP, Seller Reviews

Read Estante Virtual (estantevirtual.com.br, Brazil's used and new book marketplace, part of Magalu): keyword search, ISBN lookup, category and list pages, one book with its lowest-priced copies and reviews, every copy of a book on sale, one copy in full, shipping to a CEP, a sebo's page, its catalogue and its buyer reviews, and the sebo directory. www.estantevirtual.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in.

**The job this skill is for: what a book costs on Estante Virtual today, copy by copy, and what one copy costs delivered.** Estante Virtual is a marketplace of sebos (Brazil's second-hand bookshops) and booksellers; every copy is one seller's listing at its own fixed price. On 2026-11-27 the ISBN 9788535914849 (1984, George Orwell, Companhia das Letras) grouped 198 used and 62 new copies: the lowest used at R$ 18 from Sebo do Menino, the lowest new at R$ 21.90. That new copy cost R$ 19.34 to ship to CEP 01310-100 in 9 days (the Correios printed-matter rate), and its seller offered free shipping on orders from R$ 200.

Seven limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint, except copies with sellers.** `/copies` with `sellers: true` reads each copy's seller with one extra call per copy and costs ceil((1 + copies) / 5), counted on the copies the page returned (the balance must cover a full `page_size` page): 10 copies = 3 credits, 50 = 11. `credits_used` in the response is the truth. A not-found (`404`) is charged 1 credit; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Listings are slow.** Search, ISBN, category, list and a seller's catalogue usually take 3-30 seconds and can take about 70 seconds when the site is busy (in the captures: 9.1 and 8.6 seconds). Book, copy and seller pages usually take 4-25 seconds; `/copies` 2-10 seconds, 10-60 with `sellers: true` (27.6 seconds in the capture). Allow a client timeout of at least 180 seconds.
- **Book, listing and copy are different things.** A book (`kind` book, `book_id` ending in `-BK`, e.g. `017-4778-000-BK`) is every copy grouped under one ISBN. A one-copy listing the site did not group (`kind` listing) has a `copy_id` instead (`1IH-4767-000`). There is no work level: other editions of a title are separate books side by side.
- **Pages stop at 238.** Search and category list 44 a page, pages 1-238; narrow with filters to reach the rest. Lists show 42 a page, a seller's catalogue 40, the directory 30, seller reviews 10.
- **Fixed prices, no was price, no Pix.** Used books sell at the seller's fixed price: there is no was price, no Pix price and no coupon. Installments are returned as the site gives them.
- **Seller per copy only on request.** The `/copies` list carries no seller; send `sellers: true` (it costs more, see above) or read one copy with `/copy`.
- **City and state, never people.** A seller is its shop name, `seller_type` (`private` or `business`, as its registration says), city and state. No street address, ZIP, document number, phone or email is returned (they are removed from the seller's description). Reviews carry no reviewer names.

Estante Virtual has no public API for its books, copies or sebos. They are shown on estantevirtual.com.br to any visitor, and this skill reads those public pages with one Scavio key.

See also: ThriftBooks `thriftbooks-api`, Barnes & Noble `barnes-and-noble-api` (books outside Brazil); Enjoei `enjoei-api` (Brazil second-hand marketplace); Mercado Libre `mercadolibre-product-data` (Brazil marketplace); Brazilian retail: Magazine Luiza `magalu-magazine-luiza-api`.

## When to trigger

Use this skill when the user asks to:
- Search Estante Virtual by title, author or ISBN keywords (in Portuguese: "dom casmurro", "machado de assis"), sorted by relevance, price, newest, best sellers or price plus shipping
- Look up a book by ISBN-10 or ISBN-13 and see how many used and new copies are on sale and the lowest price
- Filter Estante Virtual books by used or new, author, publisher, printing year, seller city, seller, category, language, rating or a BRL price range
- Browse one Estante Virtual category (literatura brasileira, filosofia, livros raros) or list page (Black Friday, livros baratos, saldao de livros, livros com frete gratis, lancamentos)
- Read one book: the lowest-priced used and new copy with its seller, rating, recommendation percent and reviews
- List every used or new copy of a book by price, with the seller's condition notes, invoice flag and installments, optionally with each copy's seller
- Price the shipping of one copy to a Brazilian CEP, with delivery dates and the seller's free-shipping threshold
- Check a sebo before buying: shop name, city and state, member since, shipping methods, rating, review count, newest reviews
- Browse a sebo's catalogue (optionally by keyword) or its buyer reviews (positive or negative)
- List the sebos and booksellers of a state or city

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit (copies with sellers a little more), so 50 credits cover about 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/estantevirtual/search` | Title, author or ISBN keywords: 44 books per page with total and pages, lowest price, used and new copy counts, badges, rating; the site's facets with counts | 1 |
| `POST /api/v1/estantevirtual/isbn` | The book for an ISBN-10 or ISBN-13 (check digit verified), plus the single copies with that ISBN the site did not group | 1 |
| `POST /api/v1/estantevirtual/book` | One book: lowest price used and new, the lowest-priced used and new copy with its seller, rating, recommendation percent, histogram and every review the page shows | 1 |
| `POST /api/v1/estantevirtual/copies` | Every used or new copy of a book, up to 50 a page, by price: condition notes, invoice flag, price, installments; each copy's seller with `sellers: true` | 1; with `sellers` ceil((1 + copies) / 5) |
| `POST /api/v1/estantevirtual/copy` | One seller's copy: condition, condition notes, price, installments, free-shipping flag, seller, weight and dimensions | 1 |
| `POST /api/v1/estantevirtual/shipping` | The delivery quote for one copy to a CEP: cost, service, dates, and the seller's free-shipping threshold | 1 |
| `POST /api/v1/estantevirtual/seller` | A sebo or bookseller by id: shop name, private or business, city, state, member since, shipping methods, rating, newest reviews, catalogue total and 40 books | 1 |
| `POST /api/v1/estantevirtual/seller-books` | A sebo's catalogue, 40 per page, optionally searched by keyword and sorted by price | 1 |
| `POST /api/v1/estantevirtual/seller-reviews` | A sebo's buyer reviews, 10 per page, newest first, all, positive or negative | 1 |
| `POST /api/v1/estantevirtual/sellers` | The sebo and bookseller directory for Brazil, a state or a city, 30 per page, with the city and state counts | 1 |
| `POST /api/v1/estantevirtual/category` | One category by slug, sorted and filtered like search | 1 |
| `POST /api/v1/estantevirtual/list` | A list page of the site (black-friday by default), 42 per page in the site's order | 1 |

Brazil only: there is no `country` parameter. Every answer carries `store` (estantevirtual), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR), and most carry `notes`.

## Prices: lowest price, copies, installments and shipping

| Field | Meaning |
|---|---|
| `lowest_price` (listings) | The lowest copy price of the book in BRL (R$ 10 on the first Dom Casmurro below) |
| `copies` (listings) | `{used, new}`: how many copies of each condition are on sale (81 used, 22 new) |
| `lowest_price` (book) | `{used, new}`: the lowest price per condition (R$ 18 and R$ 21.90) |
| `lowest_priced_used`, `lowest_priced_new` (book) | The cheapest copy per condition with `copy_id`, `price`, `seller` {`id`, `name`}, year, publisher, `has_invoice`, `condition_notes`, `installment`, `url` |
| `price` (copies, copy) | That one copy's fixed price in BRL |
| `installment` | `{count, amount, total, interest_free}` as the site gives it (`total` can be null on lists) |
| `has_invoice` | Whether the seller issues an invoice (nota fiscal) for the copy |
| `condition_notes` | The seller's own description of a used copy (marks, wear, edition) |
| `badges` | The card's labels as written (`Black Ev`, `Só Aqui`) |
| `options[].cost` (shipping) | The cost to ship this one copy to the CEP, with `min_days` / `max_days` and dates |
| `free_shipping_threshold` (shipping) | `{min_order, missing, reached}`: the seller's free-shipping promotion (spend `min_order` in one cart) |

- Quote "1984, George Orwell, Companhia das Letras 2009, used: R$ 18 from Sebo do Menino on estantevirtual.com.br on 2026-11-27", with the condition, the edition, the shop name and the date.
- Shipping is per copy and per seller. Never add shipping to a price for a cart, and never apply a free-shipping threshold yourself. Report Estante Virtual's prices and the arithmetic only, and never judge a copy as a good deal.

## Workflow

1. **Find a book.** `/isbn` with `isbn` when you have one (`9788535914849`); otherwise `/search` with `query` (`dom casmurro`), `/category` with `category_slug` or `/list` with `slug`. A `kind` book's `book_id` is the input of `/book` and `/copies`; a `kind` listing's `copy_id` is the input of `/copy`.
2. **Narrow.** Read `facets` and send values back: `condition` (`used` / `new`), `author`, `publisher`, `city`, `category` as shortcuts, or `filters` `{key: value or [values]}` with `facets[].key` and `facets[].values[].value` (`ano-de-publicacao`, `idioma`, `sebos-e-livreiros`, `promocoes`, `_avaliacao`, ...); plus `price_min` / `price_max` in BRL.
3. **Next pages.** Send `page` 2, 3, ... with the same query and filters; `has_more` false means the last page.
4. **One book, then its copies.** `/book` with `book_id` for the cheapest used and new copy and the reviews; `/copies` with `book_id`, `condition` and `page_size` (up to 50) for every copy by price. Add `sellers: true` to get each copy's seller (more credits), or read one copy with `/copy`.
5. **Delivered cost.** `/shipping` with `copy_id` and `cep` for the quote to that CEP.
6. **The seller.** `/seller` with `seller_id` (`seller.id` of a copy, `sellers[].seller_id`) for the shop page; `/seller-books` for its catalogue; `/seller-reviews` for its reviews. `/sellers` with `state` (and `city`) lists the sebos of a region.
7. **Watching prices:** there is no history. Poll the same books and copies on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`) and category (`/category`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Title, author or ISBN keywords in Portuguese, 1-160 characters |
| `category_slug` (category, required) | A category slug or link: `antropologia`, `artes`, `auto-ajuda`, `biografias`, `ciencia-politica`, `comunicacao`, `direito`, `engenharia`, `filosofia`, `historia-do-brasil`, `historia-geral`, `infanto-juvenis`, `literatura-brasileira`, `literatura-estrangeira`, `livros-raros`, `medicina`, `psicologia`, `ensino-de-idiomas` (the site's menu), or a `categoria` facet value |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `newest`, `best_sellers`, `price_plus_shipping` |
| `condition` | `used` or `new` (books with copies of that condition) |
| `author`, `publisher`, `city`, `category` | Facet values as the site writes them (`machado-de-assis`, `companhia-das-letras`, `sao-paulo`, `literatura-brasileira`) |
| `filters` | `{key: value or [values]}` with the facet keys `tipo-de-livro`, `autor`, `editora`, `ano-de-publicacao`, `cidade`, `sebos-e-livreiros`, `promocoes`, `categoria`, `idioma`, `_avaliacao`, `compra-corporativa`; up to 12 values |
| `price_min`, `price_max` | Price range in BRL, 0-100000 |
| `page` | 1-238 (44 per page) |

A search with no books returns an empty `200` (charged). A query that is an ISBN gets a note pointing to `/isbn`.

### ISBN (`/isbn`)

`isbn`: an ISBN-10 or ISBN-13, 10-17 characters, dashes and spaces allowed. The check digit is verified first, so a typo is a `400` and not charged.

### Book (`/book`) and copies (`/copies`)

| Parameter | Description |
|---|---|
| `book_id` or `url` | One of: the book id (`items[].book_id`, `017-4778-000-BK`) or a book link `https://www.estantevirtual.com.br/livro/<title>-<book id>` |
| `condition` (copies) | `used` (default) or `new` |
| `sort` (copies) | `price_asc` (default) or `price_desc` |
| `page`, `page_size` (copies) | Page 1-500; 1-50 copies per page (default 10) |
| `sellers` (copies) | `true` adds each copy's seller: ceil((1 + copies) / 5) credits; default false (1 credit) |
| `year`, `publisher`, `city` (copies) | Printing year (`2009`), publisher and seller-city facet values |
| `filters` (copies) | `{key: value or [values]}`: `ano-de-publicacao`, `editora`, `cidade`, `sebos-e-livreiros`, `_preco` (min-max in cents) |

### Copy (`/copy`) and shipping (`/shipping`)

Send exactly one of `copy_id` (`GME-2437-000`: `items[].copy_id` of copies, `lowest_priced_used.copy_id` of a book, `copy_id` of a one-copy listing) or `url` (a copy link). `/shipping` also takes `cep`, a Brazilian CEP of 8 digits (`01310-100` or `01310100`).

### Seller (`/seller`), seller books (`/seller-books`) and seller reviews (`/seller-reviews`)

| Parameter | Description |
|---|---|
| `seller_id` | The seller id, digits (`1002276`): `sellers[].seller_id`, `copies[].seller.id`, a copy's `seller.id` |
| `name` (seller, optional) | The seller's `name_slug` (`sempre-brasil-livros`) |
| `query` (seller-books) | Keywords inside the seller's catalogue (`orwell`) |
| `sort` (seller-books) | `price_asc` or `price_desc` (default: the site's order) |
| `page` | seller-books 1-250 (40 per page); seller-reviews 1-1000 (10 per page) |
| `rating` (seller-reviews) | `positive` (3 to 5 stars) or `negative` (0 to 2), as the site's filters |

### Sellers (`/sellers`) and list (`/list`)

`/sellers` takes `state` (a UF, `SP`; leave out for the whole country), `city` (a city of that state, written as the site writes it with accents: `São Paulo`, see `cities[]`) and `page` 1-250. `/list` takes `slug` (`black-friday` by default, `livros-baratos`, `saldao-de-livros`, `livros-frete-gratis`, `lancamentos` or another list of the site, or its link) and `page` 1-250.

## Examples

### One search item

Request `{"query": "dom casmurro"}` (1 credit): `total` 3915, `total_pages` 89, 44 items, and 12 facets (used 3,576 and new 2,189 under `tipo-de-livro`, then author, publisher, year, city, seller, price, promotions, category, language, rating and corporate purchase). One item:

```json
{
  "position": 1,
  "kind": "book",
  "book_id": "067-5676-000-BK",
  "copy_id": null,
  "title": "Dom Casmurro",
  "author": "ASSIS, MACHADO DE",
  "publisher": "MARTIN CLARET",
  "year": 2010,
  "isbn": "9788572322645",
  "book_language": "Português",
  "url": "https://www.estantevirtual.com.br/livro/dom-casmurro-067-5676-000-BK",
  "lowest_price": 10,
  "copies": { "used": 81, "new": 22 },
  "department": null,
  "badges": [],
  "rating": null,
  "review_count": 0
}
```

### ISBN lookup

Request `{"isbn": "9788535914849"}` (1 credit): `isbn13` 9788535914849, `isbn10` 8535914846, `book` {`book_id` 017-4778-000-BK, 1984, George Orwell, Companhia das Letras, 2009, `lowest_price` 18, `copies` {`used` 198, `new` 62}}, and `listing_count` 43 single copies the site did not group, the first a 28th reprint at R$ 27 (`kind` listing, `copy_id` 1IH-4767-000, badge `Black Ev`).

### One book

Request `{"book_id": "017-4778-000-BK"}` (1 credit), abridged:

```json
{
  "book_id": "017-4778-000-BK",
  "title": "1984",
  "author": "George Orwell",
  "publisher": "Companhia das Letras",
  "year": 2009,
  "isbn": "9788535914849",
  "available": true,
  "lowest_price": { "used": 18, "new": 21.9 },
  "lowest_priced_used": {
    "copy_id": "TYV-2152-000",
    "price": 18,
    "seller": { "id": "1001559", "name": "Sebo do Menino" },
    "year": 2009,
    "has_invoice": true,
    "installment": { "count": 1, "amount": 18, "total": 18, "interest_free": true }
  },
  "lowest_priced_new": {
    "copy_id": "GME-2437-000",
    "price": 21.9,
    "seller": { "id": "1006809", "name": "Esse Livro Já Foi Dela" },
    "has_invoice": false
  },
  "rating": 5,
  "review_count": 12,
  "percent_recommended": 92,
  "reviews": [
    { "review_id": "20813736", "rating": 5, "text": "Mais um livro em melhor estado do que a descrição da venda! Ótimo custo-benefício", "date": "2026-05-14T16:03:46.843", "recommends": false, "photo_count": 0 }
  ]
}
```

The book also carried `histogram` (12 five-star reviews, 100 percent) and 12 reviews in all. There is no synopsis.

### Copies, one copy and shipping

- `/copies` `{"book_id": "017-4778-000-BK"}`: `condition` used, `sort` price_asc, `total` 198, `total_pages` 20, 10 a page; first `TYV-2152-000` at R$ 18 with `has_invoice` true and the seller's notes ("Livro usado, em bom estado de conservação geral ... Livre de grifos"), then `EMN-6036-000` at R$ 18 (2019 printing). `sellers_included` false: no seller on the list.
- `/copy` `{"copy_id": "GME-2437-000"}`: new, R$ 21.90, `free_shipping` false, `seller` {`id` 1006809, `name` "Esse Livro Já Foi Dela", `name_slug` esse-livro-ja-foi-dela}, `weight_grams` 554, `dimensions_cm` {23, 18, 5}, `quantity` 1.
- `/shipping` `{"copy_id": "GME-2437-000", "cep": "01310-100"}`:

```json
{
  "copy_id": "GME-2437-000",
  "cep": "01310100",
  "price": 21.9,
  "count": 1,
  "options": [
    { "type": "IMPRESSO_MODICO", "service": "IMPRESSO_MODICO", "seller_id": "1006809", "cost": 19.34, "free": false, "min_days": 9, "max_days": 9, "min_date": "2026-12-10", "max_date": "2026-12-10" }
  ],
  "free_shipping_threshold": { "min_order": 200, "missing": 178.1, "reached": false }
}
```

`IMPRESSO_MODICO` is the Correios printed-matter rate: the lowest-cost option the seller offers to that CEP.

### A sebo, its catalogue and its reviews

- `/seller` `{"seller_id": "1002276"}`: `name` Sempre Brasil Livros, `seller_type` private, `member_since` 2008-11-20, `city` São Vicente, `state` SP, 3 shipping methods (Impresso Modico, Correios, ...), `rating` 4.92 over 38 reviews (22 with a comment), `percent_recommended` 100, `catalogue_total` 2992 and 40 books, first a 1989 Marco Zero title at R$ 18.89.
- `/seller-books` `{"seller_id": "1002276", "query": "orwell"}`: `total` 3, first Nas Sombras de 1984 (Hemus, used) at R$ 23.90, then A Revolução dos Bichos (Globo 2003) at R$ 10.
- `/seller-reviews` `{"seller_id": "1002276"}`: `total_filtered` 38, `total_pages` 4, 10 a page, newest `{"rating": 5, "text": null, "date": "2026-11-20T08:38:09.206", "recommends": true}`. Many reviews carry a rating with `text` null.

### Directory, category and list

- `/sellers` `{"state": "SP", "city": "São Paulo"}`: `total` 1258, 42 pages of 30, e.g. Nova Cultura (rating 5), Sebo Raiz Cultural (4.75), Ellivros, each with `member_since`, `free_shipping`, `rating`, `percent_recommended`, city and state; `cities[]` with the site's counts (São Paulo 1,244).
- `/category` `{"category_slug": "literatura-brasileira"}`: `total` 840564, capped at 238 pages; first Amor é prosa, sexo é poesia (Objetiva 2004) from R$ 10, 542 used and 6 new copies, badge `Só Aqui`.
- `/list` `{}` (black-friday): title "Black Friday | Descontos Imperdíveis em Todos os Livros", `total` 399, 10 pages of 42; first Pai rico, pai pobre (Alta Books 2017) from R$ 18, 93 used and 96 new copies.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ev(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/estantevirtual/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. The book for an ISBN (1 credit)
book = ev("isbn", {"isbn": "978-85-359-1484-9"})["data"]["book"]
print(book["title"], book["lowest_price"], book["copies"])

# 2. The 10 cheapest used copies, with each copy's seller (ceil((1 + 10) / 5) = 3 credits)
copies = ev("copies", {"book_id": book["book_id"], "condition": "used", "page_size": 10, "sellers": True})["data"]
for c in copies["items"]:
    print(c["copy_id"], c["price"], c["has_invoice"], (c.get("seller") or {}).get("name"))

# 3. Shipping the cheapest copy to a CEP, then its seller (1 credit each)
first = copies["items"][0]
quote = ev("shipping", {"copy_id": first["copy_id"], "cep": "01310-100"})["data"]
print(quote["options"][0]["cost"], quote["options"][0]["max_days"], quote["free_shipping_threshold"])
if first.get("seller"):
    shop = ev("seller", {"seller_id": first["seller"]["id"]})["data"]
    print(shop["name"], shop["city"], shop["state"], shop["rating"], shop["review_count"])

# Copies sell one by one. Store each answer with fetched_at and run this on a
# schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency` and `language`.

- **search / category / list** - `query` (search), `category_slug` and `url` (category), `slug` and `url` (list), `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `title`, `items[]` {`position`, `kind` (book or listing), `book_id`, `copy_id`, `title`, `author`, `publisher`, `year`, `isbn`, `book_language`, `url`, `image`, `lowest_price`, `copies` {`used`, `new`}, `department`, `badges`, `rating`, `review_count`}, `facets[]` {`key`, `name`, `values[]` {`value`, `label`, `count`}, `min`, `max`} (search and category), `filters_echoed`, `sort`, `filters_applied` (search and category), `notes`.
- **isbn** - `isbn13`, `isbn10`, `book` (one item as above, or null), `listing_count`, `listings[]` (items of `kind` listing), `notes`.
- **book** - `book_id`, `title`, `author`, `publisher`, `year`, `isbn`, `url`, `image`, `available`, `currency`, `lowest_price` {`used`, `new`}, `lowest_priced_used` and `lowest_priced_new` {`copy_id`, `price`, `seller` {`id`, `name`}, `year`, `publisher`, `has_invoice`, `condition_notes`, `installment`, `url`}, `rating`, `review_count`, `percent_recommended`, `histogram[]` {`stars`, `count`, `percent`}, `reviews[]` {`review_id`, `rating`, `text`, `date`, `recommends`, `photo_count`}, `notes`.
- **copies** - `book_id`, `condition`, `sort`, `sellers_included`, `filters_applied`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `copy_id`, `book_id`, `title`, `author`, `publisher`, `year`, `isbn`, `book_language`, `condition`, `has_invoice`, `condition_notes`, `price`, `installment` {`count`, `amount`, `total`, `interest_free`}, `department`, `image`, `available`, `url`, `badges`, plus `seller` {`id`, `name`} and `weight_grams` with `sellers: true`}, `facets`, `notes`.
- **copy** - the copy fields above plus `free_shipping`, `seller` {`id`, `name`, `name_slug`}, `weight_grams`, `dimensions_cm` {`height`, `width`, `depth`}, `quantity` (always 1), `notes`.
- **shipping** - `copy_id`, `cep`, `seller` {`id`, `name`}, `price`, `currency`, `count`, `options[]` {`type`, `service`, `seller_id`, `cost`, `free`, `min_days`, `max_days`, `min_date`, `max_date`}, `free_shipping_threshold` {`min_order`, `missing`, `reached`}, `notes`.
- **seller** - `seller_id`, `name` (the shop name), `name_slug`, `seller_type` (private or business), `official_store`, `active`, `member_since`, `city`, `state`, `description` (phone numbers and emails removed), `shipping_methods[]` {`code`, `name`}, `url`, `rating`, `review_count`, `reviews_with_comment`, `percent_recommended`, `histogram`, `reviews[]` {`rating`, `text`, `date`, `recommends`}, `catalogue_total`, `books[]` (copy items), `notes`.
- **seller-books** - `seller_id`, `query`, `sort`, `page`, `page_size` (40), `total`, `total_pages`, `has_more`, `count`, `items[]` (copy items), `notes`.
- **seller-reviews** - `seller_id`, `page`, `page_size` (10), `total_pages`, `has_more`, `rating_filter`, `total_filtered`, `count`, `reviews[]` {`rating`, `text`, `date`, `recommends`}, `notes`.
- **sellers** - `state`, `city`, `page`, `page_size` (30), `total`, `total_pages`, `has_more`, `count`, `sellers[]` {`position`, `seller_id`, `name`, `active`, `member_since`, `city`, `state`, `free_shipping`, `rating`, `percent_recommended`, `url`}, `cities[]` and `states[]` {`value`, `count`}, `notes`.

## Guardrails

- Name it "Estante Virtual (estantevirtual.com.br, Brazil's used and new book marketplace, part of Magalu)" on first mention. Estante Virtual accounts, carts and checkout are not read or made.
- Prices: quote `price` (or `lowest_price`) with the condition, the edition (publisher and year), the shop name and the `fetched_at` date, in BRL (R$). Prices are what a visitor who is not signed in sees. There is no was price, Pix price or coupon: never invent a discount.
- Installments: quote `installment` as given. Never compute an installment yourself.
- Books and editions: a `book_id` is one ISBN, not the work. Never add up copies of different editions as one book, and never present one edition's lowest price as the price of the title.
- Shipping: `/shipping` quotes one copy from one seller to one CEP. Never sum shipping across sellers, and never assume the free-shipping threshold is reached.
- Sellers: refer to a seller by its shop name and id only, with city and state. No address, document number or contact is returned; never try to find out who is behind a shop (a `private` seller is an individual), and use seller data to judge a seller before a purchase, not to profile or contact a person.
- Reviews: no reviewer names are returned. Quote a review as "an Estante Virtual buyer review" with its rating and date; never try to identify a reviewer.
- Comparing Estante Virtual with ThriftBooks, Mercado Libre or a bookstore: compare the same ISBN, condition and date. Never call one site cheaper beyond the numbers shown.
- Images and copy: do not republish cover images, the site's marks or sellers' descriptions; refer to books and copies by `book_id`, `copy_id` and `url` instead.
- Not available: search suggestions, questions to the seller, physical stores, a was price, a Pix price, coupons, a book synopsis, price history (poll and store), account data, cart or checkout. This API cannot buy or message a seller.
- Terms: Scavio does not store Estante Virtual data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Estante Virtual's terms of use cover how its site, marks and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, copies, sellers, ratings or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "book_id or url is required"; "Pass book_id or url, not both."; "book_id must be an Estante Virtual book id, e.g. 017-4778-000-BK (items[].book_id)."; "<id> is a one-copy listing, not a book: use /api/v1/estantevirtual/copy with copy_id <id>."; "copy_id must be an Estante Virtual copy id, e.g. GME-2437-000 (copies[].copy_id)."; "seller_id must be an Estante Virtual seller id (digits, ...)"; "cep must be a Brazilian CEP of 8 digits, e.g. 01310-100."; an ISBN with a wrong check digit; "state must be a Brazilian state code (UF), e.g. SP or RJ."; "city needs its state (e.g. state SP, city São Paulo)."; "At most 12 filter values per call.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "Estante Virtual has no book with ISBN <isbn>.", "Estante Virtual has no book <id>.", "Estante Virtual has no copy <id>.", "Estante Virtual has no delivery for copy <id> to CEP <cep>.", "Estante Virtual has no seller <id>.", "Estante Virtual has no category <slug>.", "Estante Virtual has no list <slug>.". A search with no books is an empty `200`; a copy list with no copies is an empty `200` with a note; an unknown seller's catalogue is empty.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api).
- `502` and `503` mean Estante Virtual data was temporarily unavailable ("Estante Virtual is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.104.0
npm install scavio@0.105.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.estantevirtual.search({ query: "dom casmurro", condition: "used", sort: "price_asc" });
const { data: byIsbn } = await scavio.estantevirtual.isbn({ isbn: "9788535914849" });
const { data: book } = await scavio.estantevirtual.book({ book_id: "017-4778-000-BK" });
const { data: copies } = await scavio.estantevirtual.copies({ book_id: "017-4778-000-BK", condition: "used", page_size: 20 });
const { data: copy } = await scavio.estantevirtual.copy({ copy_id: "GME-2437-000" });
const { data: quote } = await scavio.estantevirtual.shipping({ copy_id: "GME-2437-000", cep: "01310-100" });
const { data: sebo } = await scavio.estantevirtual.seller({ seller_id: "1002276" });
const { data: catalogue } = await scavio.estantevirtual.sellerBooks({ seller_id: "1002276", query: "orwell" });
const { data: reviews } = await scavio.estantevirtual.sellerReviews({ seller_id: "1002276", rating: "negative" });
const { data: sebos } = await scavio.estantevirtual.sellers({ state: "SP", city: "São Paulo" });
const { data: category } = await scavio.estantevirtual.category({ category_slug: "literatura-brasileira" });
const { data: blackFriday } = await scavio.estantevirtual.list({ slug: "black-friday" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.estantevirtual.search(...)`, `isbn`, `book`, `copies`, `copy`, `shipping`, `seller`, `seller_books`, `seller_reviews`, `sellers`, `category` and `list`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 12 endpoints as tools: `search_estantevirtual`, `get_estantevirtual_isbn`, `get_estantevirtual_book`, `get_estantevirtual_copies`, `get_estantevirtual_copy`, `get_estantevirtual_shipping`, `get_estantevirtual_seller`, `get_estantevirtual_seller_books`, `get_estantevirtual_seller_reviews`, `get_estantevirtual_sellers`, `get_estantevirtual_category` and `get_estantevirtual_list`. Estante Virtual is opt-in: add `estantevirtual` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.104.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,estantevirtual"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/estantevirtual-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [isbn](https://scavio.dev/docs/estantevirtual-isbn?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [book](https://scavio.dev/docs/estantevirtual-book?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [copies](https://scavio.dev/docs/estantevirtual-copies?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [copy](https://scavio.dev/docs/estantevirtual-copy?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [shipping](https://scavio.dev/docs/estantevirtual-shipping?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [seller](https://scavio.dev/docs/estantevirtual-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [seller books](https://scavio.dev/docs/estantevirtual-seller-books?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [seller reviews](https://scavio.dev/docs/estantevirtual-seller-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [sellers](https://scavio.dev/docs/estantevirtual-sellers?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [category](https://scavio.dev/docs/estantevirtual-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api), [list](https://scavio.dev/docs/estantevirtual-list?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api). Platform page: [scavio.dev/estantevirtual-api](https://scavio.dev/estantevirtual-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=estante-virtual-api).
