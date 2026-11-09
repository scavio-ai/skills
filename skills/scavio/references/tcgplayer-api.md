# TCGplayer API - Card Market Prices, Price History, Listings, Sellers

Search TCGplayer (tcgplayer.com, the US marketplace, prices in USD) for single cards and sealed products across every game it carries (Pokemon, Magic: The Gathering, Yu-Gi-Oh!, One Piece, Lorcana and the rest of its 71 product lines), up to 50 per page, sorted by relevance, best match, best selling, name or market price, filtered by game, set, rarity and cards vs sealed: product id, name, URL, image, game, set, card number, rarity, market price, median price, lowest listing price, listing count and up to 3 featured listings, plus the filter facets with counts. Read one product by id or URL with its images (200, 400 and 1000 px), card text, the game's card attributes (Pokemon HP, stage, attacks, weakness; Magic mana value, type line, power and toughness; Yu-Gi-Oh! ATK and DEF...), listing and seller counts, and every SKU - one per condition x printing x language, such as Near Mint / Normal / English - with its market price and the low, high and count of the recent sales behind that market price. Page every live seller listing for a product, cheapest first, filtered by condition, printing, language, verified sellers or TCGplayer Direct, with the seller's rating, sales band, gold star and location. Pull up to a year of price history per SKU (market price, quantity sold, transaction count and the sale range per day, 3-day or week), the 5 most recent sales, a whole set's price guide (up to 500 rows per page, cards or sealed), every set of a game newest first, the list of games, search autocomplete, trending searches, and a seller's profile with 365 days of feedback summarized, their individual feedback rows and their catalogue with their own listings. All endpoints return structured JSON.

TCGplayer's own developer API is closed to new developers: its docs say "We are no longer granting new API access at this time." This skill reads the public marketplace data instead, with one Scavio key.

See also: for sold comps of graded cards and other collectibles on eBay use the `ebay-product-data` skill; for the cross-retailer price of sealed product at big-box stores use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Get the TCGplayer market price of a Pokemon, Magic, Yu-Gi-Oh!, One Piece or Lorcana card, by condition and printing (Near Mint vs Lightly Played, Holofoil vs Reverse Holofoil, 1st Edition vs Unlimited)
- Build a card price checker, a collection value tracker, a Discord price bot or a deck cost calculator on TCGplayer prices
- Pull TCGplayer price history or sales volume for a card over a month, quarter, half year or year
- See the last few sales of a card (the newest 5) with condition, price and shipping
- List every live TCGplayer listing for a card, cheapest first, with seller ratings, for repricing a store or finding the best buy
- Price a whole set at once (the set price guide), or sealed product such as booster boxes, ETBs and tins
- List the sets of a game newest first, or every game TCGplayer carries
- Research a TCGplayer seller: rating, sales band, feedback, and what they have listed
- Find what collectors are searching for right now (trending searches) or autocomplete a card name
- Replace the TCGplayer API for an app that never got a key, or whose key request went unanswered

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls take 1-5 seconds; allow a client timeout of at least 60 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/tcgplayer/search` | 1 | Cards and sealed products, up to 50 per page: product id, name, URL, image, game, set name, code and id, card number, rarity, product type, sealed and foil-only flags, release date, market price, median price, lowest price, lowest price with shipping, listing count and up to 3 featured live listings. Plus total results, `has_more`, `duplicates_removed` and the facets (game, set, rarity, product type, card type, condition, language, printing...) with counts |
| `POST /api/v1/tcgplayer/product` | 1 | One product by id or URL: images, game, set, card number, rarity, product type, release date, market, median and lowest price, listing and seller counts, card text, flavor text, card attributes, the details table, and `skus[]` (condition x printing x language) each with market price, lowest and highest recent sale price, the sale count behind the market price and when it was calculated |
| `POST /api/v1/tcgplayer/listings` | 1 | Live listings for one product, up to 50 per page, by price plus shipping or by price: listing id, price, shipping, total, quantity, condition, printing, language, listing type (`standard` or `custom`, with the custom title), photo count, and the seller (key, id, name, URL, rating percent, sales band, gold star, verified, Direct, programs, location). Plus total, `has_more` and condition / printing / language / listing type counts |
| `POST /api/v1/tcgplayer/price-history` | 1 | Up to a year of sales history per SKU: total quantity sold, transaction count, daily averages, and buckets (daily for `month`, 3-day for `quarter`, weekly for `semi_annual` and `annual`, newest first) with market price, quantity sold, transaction count and the low and high sale price with and without shipping. Totals across SKUs |
| `POST /api/v1/tcgplayer/sales` | 1 | The 5 most recent sales of one product, optionally only some conditions: date, condition, printing, language, quantity, price, shipping, total, title and listing type |
| `POST /api/v1/tcgplayer/games` | 1 | Every game (product line) on TCGplayer, 71 in the capture: game id, name, `url_name` and whether TCGplayer Direct carries it. No parameters |
| `POST /api/v1/tcgplayer/sets` | 1 | Every set of one game, newest release first: set id, name, `url_name`, abbreviation, release date, supplemental and active flags |
| `POST /api/v1/tcgplayer/price-guide` | 1 | One set's price guide, up to 500 rows per page, cards or sealed: one row per product per condition and printing with product id, name, URL, card number, rarity, market price and low price |
| `POST /api/v1/tcgplayer/suggestions` | 1 | The search box's autocomplete: suggested products (id, name, URL, set, game, score), matching sets and the games the matches come from with counts |
| `POST /api/v1/tcgplayer/trending` | 1 | Up to 10 trending search terms with a popularity score, overall or for Pokemon, Magic or Yu-Gi-Oh! |
| `POST /api/v1/tcgplayer/seller` | 1 | One seller by seller key: store name, URL, location, member since, lifetime sales band, completed sales rank, rating percent, gold star, Direct, Pro, VIP, certified hobby shop and WPN flags, shipping, store hours, games sold, social links, and the last 365 days of feedback summarized |
| `POST /api/v1/tcgplayer/seller-feedback` | 1 | One seller's buyer feedback from the last 365 days, newest first, up to 50 per page: date, rating, comment, the three checkboxes and the buyer's masked nickname |
| `POST /api/v1/tcgplayer/seller-products` | 1 | The products one seller has listed, in the search shape, with that seller's own listings of each |

## Workflow

1. **Find the product:** call `/tcgplayer/search` with `query` (and `game`, such as `pokemon`, `magic` or `yugioh`). Each row has a `product_id` and a `url`. `/tcgplayer/suggestions` is the cheap way to resolve a partial name to a product id.
2. **Price it by condition and printing:** call `/tcgplayer/product` with the `product_id` (or the tcgplayer.com `url`). Pick the `skus[]` row that matches the user's card (`condition`, `printing`, `language`) and quote its `market_price`.
3. **Volume and trend:** call `/tcgplayer/price-history` with the `product_id` and a `range`. Each SKU's `total_quantity_sold` and `buckets[]` give the sold volume and market price over time.
4. **Last sales:** `/tcgplayer/sales` gives the newest 5 sales, to show what the card actually went for this week. For anything beyond 5 sales use price history.
5. **Buy or reprice:** `/tcgplayer/listings` with the `product_id` and `condition` lists every live offer cheapest first; read `total_price` (price plus shipping) and the seller's `rating_percent`.
6. **Whole sets:** `/tcgplayer/games` gives each game's `url_name`; `/tcgplayer/sets` with that `game` gives each set's `set_id`; `/tcgplayer/price-guide` with the `set_id` prices the whole set, cards or sealed.
7. **Browse a set or a game:** `/tcgplayer/search` with only `game` (or `set`, a set's `url_name`), no `query`, and a `sort` such as `price_desc`.
8. **Sellers:** a listing's `seller.key` feeds `/tcgplayer/seller` (profile and feedback summary), `/tcgplayer/seller-feedback` (individual rows) and `/tcgplayer/seller-products` (their catalogue).
9. **What is hot:** `/tcgplayer/trending` with `game` returns the terms shoppers are searching now; feed one into `/tcgplayer/search`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Search keywords (up to 200 chars). Optional when `game` or `set` is given (browse the game or set) |
| `game` | string | all games | A game's `url_name` from `/games` (`pokemon`, `magic`, `yugioh`, `pokemon-japan`, `one-piece-card-game`, `lorcana-tcg`...) or a game facet's `url_value` |
| `set` | string | all sets | A set's `url_name` from `/sets` (`base-set`) or a set facet's `url_value` |
| `rarity` | string | all | One rarity as spelled in the rarity facet (`Common`, `Rare`, `Holo Rare`, `Secret Rare`...) |
| `product_type` | string | both | `cards` (single cards) or `sealed` (booster boxes, packs, decks, tins...) |
| `sort` | string | `relevance` | `relevance`, `best_match`, `best_selling`, `name_asc`, `price_asc` or `price_desc` (by market price) |
| `page` | integer | 1 | Results page, 1-based (1-200) |
| `limit` | integer | 24 | Products per page, 1-50 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | integer or string | one of | TCGplayer product id, the number after `/product/` in a tcgplayer.com URL (a search result's `product_id`, e.g. `219058`) |
| `url` | string | one of | A tcgplayer.com product URL (`https://www.tcgplayer.com/product/219058/...`), used when `product_id` is not given |

### Listings (`/listings`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` | | one of | As on `/product` |
| `condition` | array or string | all | `Near Mint`, `Lightly Played`, `Moderately Played`, `Heavily Played`, `Damaged`, `Unopened` (or `NM`, `LP`, `MP`, `HP`, `DM`, `U`). An array or a comma-separated string |
| `printing` | array or string | all | Printings as a product's `skus[].printing` spells them (`Normal`, `Foil`, `Holofoil`, `Reverse Holofoil`, `1st Edition`, `Unlimited`...) |
| `language` | array or string | all | `English`, `Japanese`, `French`, `German`, `Italian`, `Spanish`, `Portuguese`, `Korean`, `Chinese (S)`, `Chinese (T)`, `Russian` |
| `verified_sellers` | boolean | `false` | Only verified sellers |
| `direct_only` | boolean | `false` | Only TCGplayer Direct sellers |
| `sort` | string | `price_shipping` | `price_shipping` (cheapest price plus shipping first) or `price` (item price only) |
| `page` | integer | 1 | Page, 1-based (1-200) |
| `limit` | integer | 10 | Listings per page, 1-50 |

### Price history (`/price-history`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` | | one of | As on `/product` |
| `range` | string | `quarter` | `month` (daily buckets), `quarter` (3-day), `semi_annual` (weekly) or `annual` (weekly) |

### Sales (`/sales`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` | | one of | As on `/product` |
| `condition` | array or string | all | Only sales in these conditions, the same values as on `/listings` |

### Games (`/games`)

No parameters: send `{}`.

### Sets (`/sets`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `game` | string or integer | required | A game's `url_name` or `game_id` from `/games` (`pokemon`, `magic`, `yugioh`, or `3`, `1`, `2`) |

### Price guide (`/price-guide`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `set_id` | integer or string | required | A `set_id` from `/sets` (`604` is Pokemon Base Set) |
| `product_type` | string | `cards` | `cards` or `sealed` |
| `page` | integer | 1 | Page, 1-based (1-100) |
| `limit` | integer | 100 | Rows per page, 1-500. One row per card per condition and printing |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars). There is no game filter |

### Trending (`/trending`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `game` | string | `all` | `all`, `pokemon`, `magic` or `yugioh` |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller_key` | string | required | A seller key, a listing's `seller.key` (8 characters, e.g. `58f7acae`) |

### Seller feedback (`/seller-feedback`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller_key` | string | required | As on `/seller` |
| `rating` | integer | all | Only feedback with this many stars, 1-5 |
| `with_comment` | boolean | `false` | Only feedback that has a written comment |
| `page` | integer | 1 | Page, 1-based (1-500) |
| `limit` | integer | 10 | Feedback per page, 1-50 |

### Seller products (`/seller-products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller_key` | string | required | As on `/seller` |
| `query` | string | none | Only the seller's products matching these keywords |
| `game` | string | all | As on `/search` |
| `sort` | string | `relevance` | As on `/search` |
| `page` | integer | 1 | 1-200 |
| `limit` | integer | 24 | 1-50 |

## Examples

### Product with the market price per SKU

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 219058}'
```

Captured `data` (3 of 6 detail rows and 2 of 5 SKUs trimmed):

```json
{
  "product_id": 219058,
  "name": "Charizard - 3/70 (#39 Charizard Stamped)",
  "url": "https://www.tcgplayer.com/product/219058/pokemon-battle-academy-charizard-3-70-39-charizard-stamped",
  "images": {
    "small": "https://tcgplayer-cdn.tcgplayer.com/product/219058_in_200x200.jpg",
    "medium": "https://tcgplayer-cdn.tcgplayer.com/product/219058_in_400x400.jpg",
    "large": "https://tcgplayer-cdn.tcgplayer.com/product/219058_in_1000x1000.jpg"
  },
  "game": "Pokemon",
  "game_id": 3,
  "set_name": "Battle Academy",
  "set_code": "BTA",
  "set_id": 2686,
  "number": "003/070",
  "rarity": "Promo",
  "product_type": "Cards",
  "product_type_id": 1,
  "sealed": false,
  "foil_only": false,
  "normal_only": true,
  "release_date": "2020-07-31",
  "market_price": 7.09,
  "median_price": 8.44,
  "lowest_price": 4,
  "lowest_price_with_shipping": 4.9,
  "listing_count": 64,
  "seller_count": 61,
  "description": "Ability — Resolute Flame\nThis Pokémon's attacks do 30 more damage to your opponent's Active Pokémon for each of their Pokémon-GX and Pokémon-EX in play.",
  "flavor_text": "NO. 006 Flame Pokémon HT: 5'07\" WT: 199.5 lbs.\nIts wings can carry this Pokémon close to an altitude of 4,600 feet. It blows out fire at very high temperatures.",
  "note": null,
  "attributes": {
    "stage": "Stage 2",
    "energy_type": ["Fire"],
    "card_type": ["Pokemon"],
    "retreat_cost": "2",
    "card_type_b": "Fire",
    "weakness": "Wx2",
    "attack1": "[1RR] Fiery Blast (130)\nDiscard an Energy from this Pokémon.",
    "hp": "160"
  },
  "details": [
    { "name": "Card Number / Rarity", "value": "003/070 / Promo" },
    { "name": "Card Type / HP / Stage", "value": "Fire / 160 / Stage 2" },
    { "name": "Artist", "value": "Ryota Murayama" }
  ],
  "sku_count": 5,
  "skus": [
    { "sku_id": 4514135, "condition": "Near Mint", "printing": "Normal", "language": "English", "market_price": 7.09, "lowest_sale_price": 6, "highest_sale_price": 9.99, "sale_count": 25, "calculated_at": "2026-11-08T17:49:17.632Z" },
    { "sku_id": 4514136, "condition": "Lightly Played", "printing": "Normal", "language": "English", "market_price": 6.25, "lowest_sale_price": 4.99, "highest_sale_price": 7.99, "sale_count": 25, "calculated_at": "2026-11-08T20:32:08.712Z" },
    { "sku_id": 4514139, "condition": "Damaged", "printing": "Normal", "language": "English", "market_price": 4.79, "lowest_sale_price": 2.5, "highest_sale_price": 6.52, "sale_count": 21, "calculated_at": "2026-11-07T06:08:15.348Z" }
  ]
}
```

Read a SKU row as: the Near Mint / Normal / English copy has a market price of $7.09, computed from 25 recent sales that went for between $6.00 and $9.99. `lowest_sale_price`, `highest_sale_price` and `sale_count` describe those SALES, not live listings. `lowest_price` ($4.00) at the top level is the cheapest live listing in any condition. `attributes` keys depend on the game.

### Listings

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/listings \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1479, "condition": ["Near Mint"]}'
```

Captured `data` (8 of 10 listings trimmed):

```json
{
  "product_id": 1479,
  "filters": { "condition": ["Near Mint"], "printing": [], "language": [], "verified_sellers": false, "direct_only": false },
  "sort": "price_shipping",
  "page": 1,
  "limit": 10,
  "total_results": 98,
  "count": 10,
  "has_more": true,
  "listings": [
    {
      "listing_id": 26597027,
      "price": 1.09,
      "shipping_price": 1.49,
      "total_price": 2.58,
      "quantity": 1,
      "condition": "Near Mint",
      "printing": "Normal",
      "language": "English",
      "language_code": "EN",
      "listing_type": "standard",
      "direct_listing": false,
      "custom_title": null,
      "custom_description": null,
      "photo_count": 0,
      "listed_at": null,
      "seller": {
        "key": "f799c994",
        "id": 37904,
        "name": "LegionsGames",
        "url": "https://www.tcgplayer.com/sellers/LegionsGames/f799c994",
        "rating_percent": 100,
        "sales": "50000+",
        "gold_star": true,
        "verified": true,
        "direct": false,
        "programs": ["Presale", "Pro", "International", "VIP", "CertifiedHobbyShop", "WizardsPlayNetwork"],
        "city": "Pittsburgh",
        "state": "PA",
        "country": "US"
      }
    },
    {
      "listing_id": 642718134,
      "price": 2.35,
      "shipping_price": 1.49,
      "total_price": 3.84,
      "quantity": 2,
      "condition": "Near Mint",
      "printing": "Normal",
      "language": "English",
      "language_code": "EN",
      "listing_type": "standard",
      "direct_listing": false,
      "custom_title": null,
      "custom_description": null,
      "photo_count": 0,
      "listed_at": null,
      "seller": {
        "key": "b67e1599",
        "id": 178743,
        "name": "Spellfinder",
        "url": "https://www.tcgplayer.com/sellers/Spellfinder/b67e1599",
        "rating_percent": 100,
        "sales": "50000+",
        "gold_star": true,
        "verified": false,
        "direct": false,
        "programs": ["Pro", "International", "VIP"],
        "city": "Sandy",
        "state": "UT",
        "country": "US"
      }
    }
  ],
  "facets": {
    "condition": [{ "value": "Near Mint", "count": 98 }],
    "listing_type": [{ "value": "standard", "count": 87 }, { "value": "custom", "count": 11 }],
    "language": [{ "value": "English", "count": 98 }],
    "printing": [{ "value": "Normal", "count": 98 }]
  }
}
```

The default sort is by `total_price`, so a $1.09 item with $1.49 shipping comes first. `seller.sales` is a band as TCGplayer shows it (`"50000+"`, `"320"`), not an exact count. `seller.key` feeds the three seller endpoints.

### Price history

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/price-history \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 219058, "range": "month"}'
```

Captured `data` (4 of 5 SKUs and 27 of the Near Mint SKU's 30 daily buckets trimmed; the oldest bucket kept):

```json
{
  "product_id": 219058,
  "range": "month",
  "sku_count": 5,
  "totals": { "quantity_sold": 100, "transaction_count": 93 },
  "skus": [
    {
      "sku_id": 4514135,
      "condition": "Near Mint",
      "printing": "Normal",
      "language": "English",
      "total_quantity_sold": 60,
      "total_transaction_count": 56,
      "average_daily_quantity_sold": 1,
      "average_daily_transaction_count": 1,
      "bucket_days": 1,
      "buckets": [
        { "date": "2026-11-09", "market_price": 7.09, "quantity_sold": 0, "transaction_count": 0, "low_sale_price": null, "low_sale_price_with_shipping": null, "high_sale_price": null, "high_sale_price_with_shipping": null },
        { "date": "2026-11-08", "market_price": 7.09, "quantity_sold": 1, "transaction_count": 1, "low_sale_price": 9.99, "low_sale_price_with_shipping": 11.21, "high_sale_price": 9.99, "high_sale_price_with_shipping": 11.21 },
        { "date": "2026-11-07", "market_price": 6.95, "quantity_sold": 2, "transaction_count": 2, "low_sale_price": 6, "low_sale_price_with_shipping": 7.78, "high_sale_price": 6.48, "high_sale_price_with_shipping": 8 },
        { "date": "2026-10-11", "market_price": 6.63, "quantity_sold": 2, "transaction_count": 2, "low_sale_price": 6.11, "low_sale_price_with_shipping": 7.36, "high_sale_price": 7.93, "high_sale_price_with_shipping": 7.93 }
      ]
    }
  ]
}
```

Buckets are newest first, and the first one is today's partial day. A bucket with no sales keeps its `market_price` but has every sale price `null`: that means nothing sold, never a $0 sale. Here the Near Mint copy sold 60 units in the month; all five conditions together sold 100.

### Recent sales

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/sales \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 219058}'
```

Captured `data` (2 of 5 sales trimmed):

```json
{
  "product_id": 219058,
  "conditions": [],
  "count": 5,
  "sales": [
    { "date": "2026-11-08T17:47:16.847Z", "condition": "Near Mint", "printing": "Normal", "language": "English", "quantity": 1, "price": 9.99, "shipping_price": 1.22, "total_price": 11.21, "title": "Charizard - 3/70 (#39 Charizard Stamped)", "listing_type": "ListingWithoutPhotos" },
    { "date": "2026-11-07T17:51:16.763Z", "condition": "Near Mint", "printing": "Normal", "language": "English", "quantity": 1, "price": 6, "shipping_price": 2, "total_price": 8, "title": "Charizard - 3/70 (#39 Charizard Stamped)", "listing_type": "ListingWithoutPhotos" },
    { "date": "2026-11-07T17:51:16.757Z", "condition": "Lightly Played", "printing": "Normal", "language": "English", "quantity": 1, "price": 6, "shipping_price": 1.49, "total_price": 7.49, "title": "Charizard - 3/70 (#39 Charizard Stamped)", "listing_type": "ListingWithoutPhotos" }
  ]
}
```

Five is the most TCGplayer shows; there is no page 2. `conditions: []` means no condition filter was applied.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "charizard", "game": "pokemon", "limit": 10}'
```

Captured `data` (9 of 10 products, 2 of the first product's 3 featured listings, and all but 2 values of each facet trimmed; 6 of 10 facets left out):

```json
{
  "query": "charizard",
  "game": "pokemon",
  "set": null,
  "rarity": null,
  "product_type": null,
  "total_results": 382,
  "page": 1,
  "limit": 10,
  "sort": "relevance",
  "count": 10,
  "has_more": true,
  "duplicates_removed": 0,
  "products": [
    {
      "product_id": 654213,
      "name": "Mega Charizard X ex Ultra Premium Collection",
      "url": "https://www.tcgplayer.com/product/654213/pokemon-miscellaneous-cards-and-products-mega-charizard-x-ex-ultra-premium-collection",
      "image_url": "https://tcgplayer-cdn.tcgplayer.com/product/654213_in_400x400.jpg",
      "game": "Pokemon",
      "game_id": 3,
      "set_name": "Miscellaneous Cards & Products",
      "set_code": "MCAP",
      "set_id": 2374,
      "number": null,
      "rarity": null,
      "product_type": null,
      "sealed": null,
      "foil_only": false,
      "release_date": null,
      "market_price": 211.28,
      "median_price": 270,
      "lowest_price": 3,
      "lowest_price_with_shipping": 216.98,
      "listing_count": 231,
      "listings": [
        {
          "listing_id": 4494491,
          "price": 7.99,
          "shipping_price": 0,
          "total_price": 7.99,
          "quantity": 96,
          "condition": "Unopened",
          "printing": "Normal",
          "language": "English",
          "language_code": "EN",
          "listing_type": "custom",
          "direct_listing": false,
          "custom_title": "Set of 60 dice",
          "custom_description": null,
          "photo_count": 1,
          "listed_at": "2026-05-02T21:04:29.947Z",
          "seller": { "key": "3a90cc27", "id": 674790, "name": "DrZard", "url": "https://www.tcgplayer.com/sellers/DrZard/3a90cc27", "rating_percent": 100, "sales": "320", "gold_star": true, "verified": false, "direct": false, "programs": [], "city": "Oceanside", "state": "NY", "country": "US" }
        }
      ]
    }
  ],
  "facets": {
    "set": [
      { "value": "Battle Academy", "url_value": "battle-academy", "count": 61, "active": false },
      { "value": "Miscellaneous Cards & Products", "url_value": "miscellaneous-cards-and-products", "count": 37, "active": false }
    ],
    "rarity": [
      { "value": "Promo", "url_value": "Promo", "count": 114, "active": false },
      { "value": "Ultra Rare", "url_value": "Ultra Rare", "count": 38, "active": false }
    ],
    "product_type": [
      { "value": "Cards", "url_value": "Cards", "count": 255, "active": false },
      { "value": "Sealed Products", "url_value": "Sealed Products", "count": 127, "active": false }
    ],
    "game": [
      { "value": "Pokemon", "url_value": "pokemon", "count": 382, "active": true },
      { "value": "Pokemon Japan", "url_value": "pokemon-japan", "count": 356, "active": false }
    ]
  }
}
```

This row is the trap to learn from: a $211.28 market-price sealed box whose `lowest_price` is $3 and whose featured listing is a `custom` listing titled "Set of 60 dice" for $7.99. Custom listings can sell part of a product. Quote `market_price` for what the product is worth, and filter to `listing_type: "standard"` before calling anything the cheapest copy.

### Price guide

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/price-guide \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"set_id": 604, "limit": 20}'
```

Captured `data` (17 of 20 rows trimmed; one foil row from the same page kept):

```json
{
  "set_id": 604,
  "set_name": "Base Set",
  "game": "Pokemon",
  "product_type": "cards",
  "page": 1,
  "limit": 20,
  "total_results": 505,
  "count": 20,
  "has_more": true,
  "rows": [
    { "product_id": 42386, "name": "Abra", "url": "https://www.tcgplayer.com/product/42386", "number": "043/102", "rarity": "Common", "printing": "Normal", "condition": "Damaged", "market_price": 0.25, "low_price": 0.09, "product_type": "Cards", "set_name": "Base Set", "set_abbreviation": "BS", "game": "Pokemon" },
    { "product_id": 42386, "name": "Abra", "url": "https://www.tcgplayer.com/product/42386", "number": "043/102", "rarity": "Common", "printing": "Normal", "condition": "Lightly Played", "market_price": 0.53, "low_price": 0.09, "product_type": "Cards", "set_name": "Base Set", "set_abbreviation": "BS", "game": "Pokemon" },
    { "product_id": 42346, "name": "Alakazam", "url": "https://www.tcgplayer.com/product/42346", "number": "001/102", "rarity": "Holo Rare", "printing": "Holofoil", "condition": "Damaged Holofoil", "market_price": 12.99, "low_price": 12, "product_type": "Cards", "set_name": "Base Set", "set_abbreviation": "BS", "game": "Pokemon" }
  ]
}
```

`total_results` (505) counts rows, not cards: each card appears once per condition and printing. On foil rows `condition` carries the printing too (`"Damaged Holofoil"`); read `printing` for the printing. `low_price` repeats across a card's conditions in this capture (Abra is $0.09 on every row), so do not present it as the low price of one condition.

### Sets and games

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/sets \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"game": "pokemon"}'
```

Captured `data` (218 of 221 sets trimmed):

```json
{
  "game": "pokemon",
  "game_id": 3,
  "count": 221,
  "sets": [
    { "set_id": 24938, "name": "McDonald's Promos 2026", "url_name": "mcdonalds-promos-2026", "abbreviation": "M26", "release_date": "2026-11-06", "is_supplemental": true, "active": true },
    { "set_id": 24831, "name": "ME06: Delta Reign", "url_name": "me06-delta-reign", "abbreviation": "DLR", "release_date": "2026-11-06", "is_supplemental": false, "active": true },
    { "set_id": 604, "name": "Base Set", "url_name": "base-set", "abbreviation": "BS", "release_date": "1999-01-09", "is_supplemental": false, "active": true }
  ]
}
```

`/tcgplayer/games` (send `{}`) returns `{ "count": 71, "games": [...] }`, each `{ "game_id": 1, "name": "Magic: The Gathering", "url_name": "magic", "direct": true }`. 19 of the 221 Pokemon sets have `release_date: null` (older POP Series sets among them) and sort to the end.

### Suggestions and trending

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "charizard"}'
```

Captured `data` (4 of 5 products and 4 of 5 sets trimmed):

```json
{
  "query": "charizard",
  "count": 5,
  "products": [
    { "product_id": 659612, "name": "Mega Charizard X ex - 023", "url": "https://www.tcgplayer.com/product/659612/pokemon-me-mega-evolution-promo-mega-charizard-x-ex-023", "set_name": "ME: Mega Evolution Promo", "game": "Pokemon", "score": 1556 }
  ],
  "sets": [
    { "name": "Pokemon TCG Classic: Charizard", "game": "Pokemon Japan", "score": 25 }
  ],
  "games": [
    { "name": "Pokemon", "count": 10 },
    { "name": "Pokemon Japan", "count": 5 }
  ]
}
```

`/tcgplayer/trending` with `{"game": "pokemon"}` returned 10 terms such as `{ "term": "30th celebration ultimate premium collection", "score": 158.5295378543 }` and `{ "term": "prismatic evalutions", "score": 88.8396058184 }`. Terms are what shoppers typed, misspellings included.

### Seller

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_key": "58f7acae"}'
```

Captured `data` (5 of 7 weekdays of `store_hours` and 11 of 14 games trimmed):

```json
{
  "seller_key": "58f7acae",
  "seller_id": 498321,
  "name": "ARVpro",
  "url": "https://www.tcgplayer.com/sellers/ARVpro/58f7acae",
  "about": null,
  "city": "Tallahassee",
  "state": "FL",
  "country": "US",
  "member_since": "May 2024",
  "created_at": "2024-05-15T16:16:18.000Z",
  "active": true,
  "status": "Live",
  "seller_level": 4,
  "lifetime_sales": "10000+",
  "completed_sales_rank": "10000+",
  "rating_percent": 100,
  "gold_star": true,
  "direct": true,
  "pro": true,
  "vip": false,
  "certified_hobby_shop": false,
  "wizards_play_network": false,
  "presale_enabled": false,
  "ships_us": true,
  "ships_international": true,
  "logo_url": null,
  "banner_url": null,
  "social": {},
  "store_hours": { "monday": { "open": false }, "tuesday": { "open": false } },
  "games": [
    { "game_id": 1, "name": "Magic" },
    { "game_id": 3, "name": "Pokemon" },
    { "game_id": 2, "name": "YuGiOh" }
  ],
  "feedback": {
    "period_days": 365,
    "total": 6186,
    "percent_positive": 100,
    "stars": { "five": 6183, "four": 3, "three": 0, "two": 0, "one": 0 },
    "as_described": { "positive": 567, "negative": 26 },
    "arrived_when_expected": { "positive": 575, "negative": 13 },
    "good_communication": { "positive": 201, "negative": 6 }
  }
}
```

`percent_positive` is 4 and 5 stars over the total, as the seller page shows it. The three checkbox counts cover only the buyers who ticked them (593 of 6,186 for "as described"), so do not divide them by `total`.

### Seller feedback

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/seller-feedback \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_key": "bf43b501"}'
```

Captured `data` (8 of 10 rows trimmed):

```json
{
  "seller_key": "bf43b501",
  "period_days": 365,
  "rating": null,
  "with_comment": false,
  "page": 1,
  "limit": 10,
  "total_results": 801,
  "count": 10,
  "has_more": true,
  "feedback": [
    { "date": "2026-10-27T03:54:44.000Z", "rating": 5, "comment": "Delivered 5 days after purchase, in good condition", "as_described": true, "arrived_when_expected": true, "good_communication": false, "buyer": "a********0" },
    { "date": "2026-10-26T20:08:06.000Z", "rating": 5, "comment": null, "as_described": false, "arrived_when_expected": false, "good_communication": false, "buyer": "M**********3" }
  ]
}
```

The second row is a 5-star review with every checkbox `false`: a `false` can mean the buyer left the box empty, so never read it as a complaint. `buyer` is the masked nickname as the site shows it; there is no way to identify a buyer.

### Seller products

```bash
curl -X POST https://api.scavio.dev/api/v1/tcgplayer/seller-products \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_key": "58f7acae", "game": "pokemon", "limit": 10}'
```

The captured page (`total_results: 1547`, `count: 10`) has the search envelope with `seller_key` added. Its first product is `Gengar`, `ME03: Perfect Order` `050/088`, market price $0.44, and its `listings[]` holds that seller's own listing: Near Mint, Reverse Holofoil, $4.99 plus $3.99 shipping, quantity 4, `direct_listing: true`. The seller on that listing shows Louisville, KY while the `/seller` profile says Tallahassee, FL: report each location where it appears and do not reconcile them.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def tcgplayer(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/tcgplayer/{endpoint}", headers=HEADERS, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["data"]

# 1. Find the card (1 credit)
found = tcgplayer("search", {"query": "charizard", "game": "pokemon", "product_type": "cards", "limit": 5})
pid = found["products"][0]["product_id"]

# 2. Market price by condition and printing (1 credit)
item = tcgplayer("product", {"product_id": pid})
for s in item["skus"]:
    print(s["condition"], s["printing"], s["language"], s["market_price"],
          f'({s["sale_count"]} sales, {s["lowest_sale_price"]}-{s["highest_sale_price"]})')

# 3. Units sold over the last quarter (1 credit)
hist = tcgplayer("price-history", {"product_id": pid, "range": "quarter"})
for s in hist["skus"]:
    print(s["condition"], s["printing"], "sold", s["total_quantity_sold"])

# 4. Cheapest Near Mint standard listings (1 credit)
offers = tcgplayer("listings", {"product_id": pid, "condition": ["Near Mint"], "limit": 20})
for l in offers["listings"]:
    if l["listing_type"] == "standard":
        print(l["total_price"], l["seller"]["name"], l["seller"]["rating_percent"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when TCGplayer answered.

- **search** - `query`, `game`, `set`, `rarity`, `product_type`, `total_results`, `page`, `limit`, `sort`, `count`, `has_more`, `duplicates_removed`, `products[]` (`product_id`, `name`, `url`, `image_url`, `game`, `game_id`, `set_name`, `set_code`, `set_id`, `number`, `rarity`, `product_type`, `sealed`, `foil_only`, `release_date`, `market_price`, `median_price`, `lowest_price`, `lowest_price_with_shipping`, `listing_count`, `listings[]` in the listing shape), `facets` {facet name: [{`value`, `url_value`, `count`, `active`}]}.
- **product** - `product_id`, `name`, `url`, `images` ({`small`, `medium`, `large`} or null), `game`, `game_id`, `set_name`, `set_code`, `set_id`, `number`, `rarity`, `product_type`, `product_type_id`, `sealed`, `foil_only`, `normal_only`, `release_date`, `market_price`, `median_price`, `lowest_price`, `lowest_price_with_shipping`, `listing_count`, `seller_count`, `description`, `flavor_text`, `note`, `attributes` {game-specific}, `details[]` {`name`, `value`}, `sku_count`, `skus[]` {`sku_id`, `condition`, `printing`, `language`, `market_price`, `lowest_sale_price`, `highest_sale_price`, `sale_count`, `calculated_at`}.
- **listings** - `product_id`, `filters` {`condition[]`, `printing[]`, `language[]`, `verified_sellers`, `direct_only`}, `sort`, `page`, `limit`, `total_results`, `count`, `has_more`, `listings[]` {`listing_id`, `price`, `shipping_price`, `total_price`, `quantity`, `condition`, `printing`, `language`, `language_code`, `listing_type`, `direct_listing`, `custom_title`, `custom_description`, `photo_count`, `listed_at`, `seller` {`key`, `id`, `name`, `url`, `rating_percent`, `sales`, `gold_star`, `verified`, `direct`, `programs[]`, `city`, `state`, `country`}}, `facets` {`condition`, `listing_type`, `language`, `printing`: [{`value`, `count`}]}.
- **price-history** - `product_id`, `range`, `sku_count`, `totals` {`quantity_sold`, `transaction_count`}, `skus[]` {`sku_id`, `condition`, `printing`, `language`, `total_quantity_sold`, `total_transaction_count`, `average_daily_quantity_sold`, `average_daily_transaction_count`, `bucket_days`, `buckets[]` {`date`, `market_price`, `quantity_sold`, `transaction_count`, `low_sale_price`, `low_sale_price_with_shipping`, `high_sale_price`, `high_sale_price_with_shipping`}}.
- **sales** - `product_id`, `conditions[]`, `count`, `sales[]` {`date`, `condition`, `printing`, `language`, `quantity`, `price`, `shipping_price`, `total_price`, `title`, `listing_type`}.
- **games** - `count`, `games[]` {`game_id`, `name`, `url_name`, `direct`}.
- **sets** - `game`, `game_id`, `count`, `sets[]` {`set_id`, `name`, `url_name`, `abbreviation`, `release_date`, `is_supplemental`, `active`}.
- **price-guide** - `set_id`, `set_name`, `game`, `product_type`, `page`, `limit`, `total_results` (null for sealed), `count`, `has_more`, `rows[]` {`product_id`, `name`, `url`, `number`, `rarity`, `printing`, `condition`, `market_price`, `low_price`, `product_type`, `set_name`, `set_abbreviation`, `game`}.
- **suggestions** - `query`, `count`, `products[]` {`product_id`, `name`, `url`, `set_name`, `game`, `score`}, `sets[]` {`name`, `game`, `score`}, `games[]` {`name`, `count`}.
- **trending** - `game`, `count`, `terms[]` {`term`, `score`}.
- **seller** - `seller_key`, `seller_id`, `name`, `url`, `about`, `city`, `state`, `country`, `member_since`, `created_at`, `active`, `status`, `seller_level`, `lifetime_sales`, `completed_sales_rank`, `rating_percent`, `gold_star`, `direct`, `pro`, `vip`, `certified_hobby_shop`, `wizards_play_network`, `presale_enabled`, `ships_us`, `ships_international`, `logo_url`, `banner_url`, `social` {`homepage`, `facebook`, `twitter`, `instagram`, `discord` when set}, `store_hours` {weekday: {`open`, ...}} or null, `games[]` {`game_id`, `name`}, `feedback` {`period_days`, `total`, `percent_positive`, `stars` {`five`...`one`}, `as_described`, `arrived_when_expected`, `good_communication` {`positive`, `negative`}}.
- **seller-feedback** - `seller_key`, `period_days`, `rating`, `with_comment`, `page`, `limit`, `total_results`, `count`, `has_more`, `feedback[]` {`date`, `rating`, `comment`, `as_described`, `arrived_when_expected`, `good_communication`, `buyer`}.
- **seller-products** - the search shape plus `seller_key`; each product's `listings[]` are that seller's own listings.

## Guardrails

- Prices are in US dollars on the US marketplace: `7.09` is $7.09. `shipping_price` is the shipping to a US address. There is no other storefront or currency.
- `market_price` is TCGplayer's Market Price, computed from recent sales. It is not a live listing price. On a SKU, `lowest_sale_price`, `highest_sale_price` and `sale_count` are the range and count of the sales behind that market price, and `calculated_at` is when it was last computed; they are not listing prices.
- Always quote a price for a specific SKU (`condition` x `printing` x `language`). A Near Mint Holofoil and a Damaged Normal copy of the same card can differ by an order of magnitude. When the user does not say, give Near Mint in the card's usual printing and say so.
- `lowest_price` is the cheapest live listing in any condition and can be a `custom` listing that sells part of a product (the captured $211.28 box shows `lowest_price: 3` and a "Set of 60 dice" listing). Never present `lowest_price` as what the product costs; use `market_price`, or `/listings` filtered to `listing_type: "standard"` and the right condition.
- Search and seller-products rows carry at most 3 featured `listings[]`, not every offer. Use `/listings` for the full list (`total_results` there is the real count).
- `market_price` can be `null` on a product with no recent sales (one captured search row has it null with a `lowest_price` of $549.98). Say there is no market price; do not substitute the listing price without saying so.
- `/sales` returns at most the 5 newest sales and has no pagination. Never call it a sales history or say "the last N sales" for N above 5. For volume and older sale ranges use `/price-history`.
- Price-history buckets are newest first, and the first is today's partial bucket. A bucket with `quantity_sold: 0` has every sale price `null` (nothing sold), never a $0 sale; its `market_price` is still set, except before a product's first sale, when `market_price` is `null` too (no price yet). `bucket_days` is the measured bucket width (1 for `month`) and is null when there are fewer than 3 buckets. History goes back one year at most (`annual`).
- Search and seller-products hits have no reliable product type. Pass `product_type` (`cards` or `sealed`) and every hit gets `product_type` and `sealed`; without it, `sealed` is `true` only when TCGplayer flags it, `false` only when the hit says Cards, and otherwise `null` (unknown). `/tcgplayer/product` gives the definitive type.
- A product with no sales in the range is a 404 on `/price-history` (the same as an unknown id). Try a longer `range` before saying the card never sells.
- Under `relevance` and `best_match`, TCGplayer's ranking shifts between calls, so page 2+ drops products the previous page already showed; `duplicates_removed` says how many, and `count` can be below `limit` while `has_more` is still true. To walk every result, use `price_asc`, `price_desc` or `name_asc`, which page predictably.
- `game` and `set` take `url_name` values (`pokemon`, `base-set`), the same as a facet's `url_value`; `rarity` takes the facet's display value (`Holo Rare`). Game names differ by endpoint (`"Magic: The Gathering"` on `/games`, `"Magic"` in a seller's `games[]`, `"YuGiOh"` without punctuation): match on `game_id`, not on the name.
- `/suggestions` has no game filter and mixes games (the captured `charizard` sets are all Pokemon Japan). Filter on `game` yourself. `score` is TCGplayer's ranking score, not a search volume.
- `/trending` terms are raw shopper searches, typos included (`"prismatic evalutions"`, `"illustration raraes"`). Quote them as given; `score` is relative popularity, not a count of searches.
- Price guide rows repeat each card once per condition and printing, so `total_results` counts rows, not cards. On foil rows `condition` carries the printing (`"Damaged Holofoil"`). `low_price` repeats across a card's conditions in the capture, so do not present it as one condition's low. `total_results` is null for `sealed`, and then `has_more` only means the page was full.
- On `/seller`, `lifetime_sales` and `completed_sales_rank` are bands (`"10000+"`), and so is a listing's `seller.sales` (`"50000+"`, `"320"`). Never turn a band into an exact sales count. `rating_percent` and `feedback.percent_positive` are different measures; report the one asked for.
- Seller feedback covers the last 365 days only. A checkbox that is `false` can mean the buyer left it empty, not that they complained; the real complaint counts are the `negative` numbers in `/seller`'s `feedback`. `total_results` on `/seller-feedback` is approximate under the `rating` and `with_comment` filters, and `has_more` is true whenever the page is full.
- `buyer` on a feedback row is the site's masked nickname. Do not try to identify buyers.
- The location on a listing's `seller` can differ from the location on that seller's `/seller` profile. Report each where it appears.
- There is no store locator, no product reviews, no buylist prices, no graded-card (PSA, BGS) prices and no full sold-listing history. Do not claim any of them.
- This API reads public marketplace data for price checks, collection tracking, repricing research and alerts. It does not buy, list or reprice anything on TCGplayer; do not present it as a buying or listing bot.
- Never fabricate prices, sales, quantities sold, listings or seller data. Only return what the API returned, with the product `url` or `product_id`.

## Failure handling

- `400` means a missing or invalid parameter (neither `product_id` nor `url`, a `product_id` that is not a number, a `url` that is not a tcgplayer.com `/product/<id>` URL, `query` missing on `/search` with no `game` or `set`, a `game` or `set` that is not a `url_name`, an unknown `sort`, `range`, `product_type` or condition, `page` or `limit` out of range, more than 10 values in a list filter, a `seller_key` that is not 4-16 letters and digits, `rating` outside 1-5, a `set_id` that is not numeric, or a missing `query` on `/suggestions`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product (unknown id), no price history in the range, no such game, a set with nothing in the price guide, or no seller with that key. Not charged. Re-run the search for a fresh `product_id`, or `/games` and `/sets` for valid ids.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api).
- `502` or `503` means TCGplayer is temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.

## SDKs

```bash
pip install scavio==0.40.0
npm install scavio@0.41.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.tcgplayer.search({ query: "charizard", game: "pokemon", sort: "price_desc" });
const { data: item } = await scavio.tcgplayer.product({ product_id: found.products[0].product_id });
const { data: offers } = await scavio.tcgplayer.listings({ product_id: item.product_id, condition: ["Near Mint"] });
const { data: hist } = await scavio.tcgplayer.priceHistory({ product_id: item.product_id, range: "annual" });
const { data: last5 } = await scavio.tcgplayer.sales({ product_id: item.product_id });
const { data: sets } = await scavio.tcgplayer.sets({ game: "pokemon" });
const { data: guide } = await scavio.tcgplayer.priceGuide({ set_id: 604, limit: 500 });
const { data: seller } = await scavio.tcgplayer.seller({ seller_key: offers.listings[0].seller.key });
const { data: stock } = await scavio.tcgplayer.sellerProducts({ seller_key: seller.seller_key, game: "pokemon" });
```

Python uses the same namespace with snake_case methods: `client.tcgplayer.price_history(...)`, `price_guide`, `seller_feedback`, `seller_products`.

## MCP

The Scavio MCP server exposes all thirteen endpoints as tools: `search_tcgplayer`, `get_tcgplayer_product`, `get_tcgplayer_listings`, `get_tcgplayer_price_history`, `get_tcgplayer_sales`, `get_tcgplayer_games`, `get_tcgplayer_sets`, `get_tcgplayer_price_guide`, `get_tcgplayer_suggestions`, `get_tcgplayer_trending`, `get_tcgplayer_seller`, `get_tcgplayer_seller_feedback` and `get_tcgplayer_seller_products`. TCGplayer is opt-in: add `tcgplayer` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.38.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,tcgplayer"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/tcgplayer-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [product](https://scavio.dev/docs/tcgplayer-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [listings](https://scavio.dev/docs/tcgplayer-listings?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [price history](https://scavio.dev/docs/tcgplayer-price-history?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [sales](https://scavio.dev/docs/tcgplayer-sales?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [games](https://scavio.dev/docs/tcgplayer-games?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [sets](https://scavio.dev/docs/tcgplayer-sets?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [price guide](https://scavio.dev/docs/tcgplayer-price-guide?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [suggestions](https://scavio.dev/docs/tcgplayer-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [trending](https://scavio.dev/docs/tcgplayer-trending?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [seller](https://scavio.dev/docs/tcgplayer-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [seller feedback](https://scavio.dev/docs/tcgplayer-seller-feedback?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api), [seller products](https://scavio.dev/docs/tcgplayer-seller-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api). Overview: [TCGplayer API](https://scavio.dev/tcgplayer-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api).
