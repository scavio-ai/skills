---
name: yesstyle-api
description: YesStyle API for YesStyle (yesstyle.com, the Hong Kong-based online store for Asian beauty and fashion, shipping to 150+ countries, owned by YesAsia Holdings) - K-beauty and J-beauty prices by shipping country, YesStyle's own regional price list per country in that country's currency (not a conversion - COSRX Advanced Snail 96 Mucin Power Essence 100ml read 16.09 USD in the US, 14.86 USD in South Africa, 16.31 EUR in France, Spain, Italy and the Netherlands, 2,497 JPY in Japan, 20,740 KRW in South Korea and 17.16 CAD in Canada on Nov 26, 2026), each answer checked for the country it was priced for; keyword search, any category, any brand and the deal lists (Black Friday, flash sales, clearance, rock-bottom prices, price drops, value and gift sets, twin packs), 100 per page with total and pages, seven sorts and YesStyle's filters (in stock, Korean or Japanese brands, cruelty-free, vegan, YesStyle Awards, price band, skin type, skin concern, brand region, ingredients); one product with price, list price, YesStyle's discount, sale end date, deal claimed share, availability for the country, ingredients, bestseller ranks, packs, shipping time and the site coupon tiers, plus every shade and size with its own price and availability on request; customer reviews 15 reviewers a page with four sorts and star, photo or video filters (no reviewer names); search suggestions, the brand list (about 4,300) and the 153 shipping countries. Page endpoints serve 39 countries (Brazil not offered); reviews and suggestions any of 153. 9 endpoints - search, category, brand, deals and product 2 credits, product with shades and sizes 3, reviews, suggestions, brands and markets 1. No stores, currency choice, EAN or UPC, price history, cart or checkout.
version: 1.0.0
tags: yesstyle, yesstyle-com, yesstyle-api, yesstyle-prices, yesstyle-price-api, yesstyle-product-data, yesstyle-reviews, yesstyle-deals, yesstyle-black-friday, yesstyle-flash-sale, yesstyle-clearance, yesstyle-coupon, yesstyle-brands, yesstyle-cosrx, yesstyle-anua, yesstyle-shades, yesasia, k-beauty, k-beauty-prices, korean-skincare, korean-beauty, j-beauty, asian-beauty, beauty, beauty-prices, skincare, skincare-prices, cosmetics, regional-pricing, price-by-country, multi-currency, international-prices, shades, variant-data, product-search, product-data, customer-reviews, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/yesstyle-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api
---

# YesStyle API - K-Beauty Prices by Country, Reviews, Deals

Read YesStyle (yesstyle.com, the Hong Kong-based online store for Asian beauty and fashion, shipping to 150+ countries, owned by YesAsia Holdings): keyword search, any category, any brand, the deal lists, one product in full with every shade and size, customer reviews, search suggestions, the brand list and the shipping countries. Every answer is YesStyle's page for the shipping country you ask for, in that country's currency and language, as a visitor without an account sees it. All 9 endpoints return structured JSON at 1 to 3 credits per call.

**Read-only data.** This skill reads the public pages YesStyle shows to any visitor and returns them as JSON for analysis. It uses no YesStyle account, no rewards login, no cart and no checkout.

**The job this skill is for: one K-beauty product priced across shipping countries.** YesStyle sets its own price list per shipping country (regional prices, not a currency conversion), and which products ship differs by country. Captured 2026-11-26 with `/product` (`product_id` `1052684695`, one call per country, 2 credits each), COSRX Advanced Snail 96 Mucin Power Essence 100ml:

| Country (`country`) | Currency | `price` | `list_price` | `availability` |
|---|---|---|---|---|
| United States (`us`) | USD | 16.09 | 25 | In-Stock |
| South Africa (`za`) | USD | 14.86 | 21.23 | In-Stock |
| Canada (`ca`) | CAD | 17.16 | 28.56 | In-Stock |
| France, Spain, Italy, Netherlands (`fr`, `es`, `it`, `nl`) | EUR | 16.31 | 25 | in stock (in the page language: En stock, Disponible, Disponibile, Op voorraad) |
| Switzerland (`ch`) | CHF | 13.51 | 19.53 | In-Stock |
| Poland (`pl`) | PLN | 52.88 | 88.38 | W magazynie |
| Sweden (`se`) | SEK | 155.1 | 221.57 | In-Stock |
| Japan (`jp`) | JPY | 2497 | 3566 | In-Stock |
| South Korea (`kr`) | KRW | 20740 | 29629 | In-Stock |
| Taiwan (`tw`) | TWD | 424.35 | 606.21 | in stock (Chinese) |
| Singapore (`sg`) | SGD | 18.09 | 25.84 | In-Stock |
| New Zealand (`nz`) | NZD | 23.28 | 45.75 | In-Stock |
| Mexico (`mx`) | MXN | 304.14 | 434.48 | Disponible |
| India (`in`) | INR | 1670 | 2386 | Not available for your shipping destination |
| Saudi Arabia (`sa`) | SAR | 57.43 | 82.04 | not available for your shipping destination (Arabic) |

The US and South Africa are both priced in USD and differ (16.09 against 14.86): never convert one country's price to stand for another. India and Saudi Arabia were priced but not shippable: report `availability` with the price.

Ten limits shape every answer, so say them plainly:
- **Credits depend on the endpoint.** search, category, brand, deals and product 2; product with `include_variants` 3; reviews, suggestions, brands and markets 1. `credits_used` in every answer says what was spent. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are per shipping country.** `country` (ISO-2, default `us`; `uk` is read as `gb`) sets the currency, the prices and which products ship. Every answer carries `market` {`country`, `country_name`, `currency`, `language`}: quote the price with that country. The currency is the country's own; choosing another currency is not offered.
- **Country checked on every answer.** Each page answer is checked for the country it was priced for; a page for another country is never returned or billed. When every attempt comes back for another country the answer is an unbilled `502` naming the country ("YesStyle is temporarily unavailable for <country> (<code>). Please try again."): retry later.
- **39 countries on the page endpoints, 153 on reviews and suggestions.** search, category, brand, deals and product serve `ae at au be ca ch cl cz de dk es fr gb gr hk hu ie il in it jp kr kz mx my nl no nz ph pl pt ro sa se sg th tw us za`. Brazil (`br`) is not offered there (a `400`, not charged). reviews and suggestions answer for any of the 153 countries `/markets` lists.
- **The catalog differs by country.** Products YesStyle cannot ship to a country drop out of its lists: `/search` for `cosrx` with `country` `ae` returned `total` 0 in a `200` on 2026-11-26, while the US listed COSRX items. An empty list for one country is not proof the product does not exist.
- **List prices and discounts are YesStyle's.** `list_price`, `discount_percent`, `price_text` and `list_price_text` are as YesStyle shows them. Lists and the product page can round the discount differently (36 on search, 35 on the product page for the same essence): quote the one you read, from where you read it.
- **Lists carry no stock.** Lists show no per-item stock; `featured: ["in_stock"]` limits a list to items in stock. Availability is on `/product` (per shade or size with `include_variants`), in the page language.
- **Product families.** A product page can price one option of a family: `requested_product_id` is what you sent, `product_id` the option the page prices (`1052684695` answered with option `100ml`, `product_id` `1052684694`). Shades and sizes are in `child_product_ids`; `include_variants` adds each one's name, price and availability (+1 credit).
- **Reviews per family, 15 reviewers a page.** A reviewer can have more than one review on a page (`reviewer_group`), so a page can hold 16 or 19 reviews. YesStyle answers up to 67 pages (about 1,000 reviews) per sort and filter: change `sort` or `filter` to reach others. Reviewer names, gender and age are not returned.
- **What is not there.** No stores (YesStyle has none to look up), no currency choice, no EAN or UPC (YesStyle shows its Catalog No., the product id), no price history (store your own answers with `fetched_at`), no cart or checkout, so a coupon price is your own arithmetic.

YesStyle publishes no public API for its catalog, prices or reviews. Its affiliate program (through Commission Factory and AWIN) offers publishers creatives, product information and promotions for approved partners; this skill reads YesStyle's public pages with one Scavio key and needs no affiliate approval. Other vendors offer YesStyle data tools; this skill reads YesStyle's own public pages.

YesStyle is owned by YesAsia Holdings (HKEX 2209). YesAsia reported first-half 2026 revenue of US$301.51m, with YesStyle B2C revenue of US$215.07m (YesAsia interim results, released Aug 28, 2026). Quote these with their source, never from the samples.

See also: for the same product at other retailers use `sephora-product-data` (Sephora), `ulta-beauty-api` (Ulta Beauty), `iherb-product-data` (iHerb), `amazon-product-data` (Amazon), and for European beauty retailers `douglas-beauty-api` (Douglas), `lookfantastic-api` (Lookfantastic) and `notino-api` (Notino). Same product and size only: YesStyle shows no barcode, so match brand + product name + size in both titles, each price with its seller, country and date.

## When to trigger

Use this skill when the user asks to:
- Price one YesStyle product (K-beauty, J-beauty, skincare, makeup) in several shipping countries, each in its own currency
- Read a YesStyle product's price, list price, discount, sale end date, deal claimed share, availability for a country, ingredients and bestseller ranks
- Compare every shade or size of a YesStyle product with its own price and availability
- Search YesStyle by keyword, or browse a category or a brand, sorted by bestsellers, newest, price, best value, availability or discount, filtered by in stock, Korean or Japanese brands, cruelty-free, vegan, YesStyle Awards, price band, skin type or skin concern
- List YesStyle's Black Friday, flash sale, clearance, rock-bottom price, price drop, value set or twin pack deals in a country
- Read YesStyle customer reviews of a product, sorted or filtered by stars, positive, negative, photo or video, with the star counts and satisfaction
- Read YesStyle's current site coupon code and its spend tiers for a country
- List YesStyle's brands, its search suggestions, or the countries it ships to with their currencies

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 to 3 credits, so 50 credits cover 25 product calls or 50 review pages.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1-6 seconds, product 1-9, markets 2-4, reviews 4-5, brands 6-8, search, category, brand and deals 3-20, and product with shades and sizes 8-29. Allow up to a few minutes for an answer, set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/yesstyle/search` | Products for keywords: price, list price, discount, rating, review count, size, status, badges; total, pages, sorts, facets on request, the site coupon | 2 |
| `POST /api/v1/yesstyle/category` | One category by id or link, with paging, sorts and filters (Featured, price, type, brand region, ingredients, any facet) | 2 |
| `POST /api/v1/yesstyle/brand` | One brand's products, with the brand's name, region, satisfaction and star counts | 2 |
| `POST /api/v1/yesstyle/deals` | A deal list (Black Friday, flash sales, clearance, rock-bottom prices, price drops, 24-hour sale, value and gift sets, twin packs) on a department | 2 |
| `POST /api/v1/yesstyle/product` | One product: price, list price, discount, sale end date, deal claimed share, availability, ingredients, bestseller ranks, packs, shipping, returns, coupon; every shade and size with `include_variants` | 2; 3 with `include_variants` |
| `POST /api/v1/yesstyle/reviews` | Reviews of one product family, 15 reviewers a page, with the star counts and satisfaction | 1 |
| `POST /api/v1/yesstyle/suggestions` | The search terms and products YesStyle suggests for what a shopper typed, priced for the country | 1 |
| `POST /api/v1/yesstyle/brands` | YesStyle's brand list (about 4,300): `brand_id`, link name, URL | 1 |
| `POST /api/v1/yesstyle/markets` | The 153 shipping countries with currency, language and whether the page endpoints serve them; currencies; languages | 1 |

## Markets

| Scope | Countries |
|---|---|
| search, category, brand, deals, product (39) | `ae` (AED), `at` (EUR), `au` (AUD), `be` (EUR), `ca` (CAD), `ch` (CHF), `cl` (USD), `cz` (CZK), `de` (EUR), `dk` (DKK), `es` (EUR), `fr` (EUR), `gb` (GBP), `gr` (EUR), `hk` (HKD), `hu` (HUF), `ie` (EUR), `il` (ILS), `in` (INR), `it` (EUR), `jp` (JPY), `kr` (KRW), `kz` (USD), `mx` (MXN), `my` (MYR), `nl` (EUR), `no` (NOK), `nz` (NZD), `ph` (PHP), `pl` (PLN), `pt` (EUR), `ro` (USD), `sa` (SAR), `se` (SEK), `sg` (SGD), `th` (THB), `tw` (TWD), `us` (USD, default), `za` (USD) |
| reviews, suggestions | any of the 153 countries in `/markets` |
| not offered | Brazil (`br`) on the page endpoints (`held_back` in `/markets` says why) |

- **Language:** `language` is one of `en`, `fr`, `de`, `es`, `it`, `nl`, `pl`, `pt`, `ru`, `ar`, `zh_TW`; the default is the country's own on YesStyle (`de` for Germany, `ar` for Saudi Arabia and the UAE, `zh_TW` for Taiwan and Hong Kong, `en` for most). Names, availability words, review dates and labels follow it; prices follow `country`.
- **Currency** is the country's default (`market.currency`). Some countries are priced in USD (`cl`, `kz`, `ro`, `za`), each with its own USD price list.

## Prices and product fields

| Field | Meaning |
|---|---|
| `price`, `price_text` | YesStyle's price for the country, as a number and as shown ("US$ 16.09", "18,00 €") |
| `list_price`, `list_price_text` | YesStyle's list price next to the price, as shown |
| `discount_percent` | YesStyle's own discount figure as shown (`null` when YesStyle hides it) |
| `status`, `badges` | YesStyle's label (FLASH SALE, Black Friday, Trending New) and badges (`flash_sale`, `black_friday`, `clearance`, `buy_one_get_one`, `trending_new`, `yesstyle_awards_2026`, `high_discount` ...) |
| `sale_end_date` (product) | When the sale price ends, as YesStyle gives it ("2026-12-01T00:00:00Z") |
| `deal_claimed_percent`, `deal_claimed_text` (product) | The deal's claimed share as YesStyle shows it (86, "Deal is 86% claimed") |
| `availability`, `sellable` (product) | YesStyle's availability for the country, in the page language (In-Stock, Temporarily Out of Stock, Not available for your shipping destination) |
| `coupon` | The site coupon YesStyle shows for the country: `code`, `name`, `tiers` [{`discount`, `min_order`}], `expires_at` |
| `brand_region` (lists), `brand.region` (product) | The brand's country (`kr`; "Brand from South Korea") |
| `rating`, `review_count`, `star_counts` | YesStyle's rating (0-5), review count and stars 1-5 |
| `market` | {`country`, `country_name`, `currency`, `language`}: the country the answer was priced for |

- **Coupon prices:** a price after the site code is your own computation from `coupon.tiers`; label it "computed, not checked out". The tiers apply to an order total, not one item.
- **Product ids:** `product_id` is a string of digits (`"1052684695"`). Every shade and size has its own id; reviews take the family's `parent_product_id`.

## Workflow

1. **Find the product.** `/search` with `query` (and `country`), or `/brand` with a `brand_id` from `/brands` (`317041` COSRX), or `/category` with a category id from `breadcrumbs` (`15556` Face Serums). Note `product_id`, `name` and `size`.
2. **Price it per country.** `/product` with `product_id` and one `country` per call (2 credits each). Read `price`, `list_price`, `discount_percent`, `availability` and `market.currency`.
3. **Shades and sizes.** `/product` with `include_variants: true` (3 credits): `variants[]` with each option's `product_id`, `name`, `price` and `availability`.
4. **Deals.** `/deals` with `deal` (`black_friday`, `flash_sales`, `clearance` ...) and `country`; read `sale_end_date` and `deal_claimed_percent` on `/product` for the items you report.
5. **Reviews.** `/reviews` with the family's `product_id` (`parent_product_id` from `/product`), `sort` and `filter`; page 1 carries the `summary`.
6. **Report.** Each price with its currency, country and `fetched_at` date; availability for that country; a discount as YesStyle shows it, a coupon price labelled computed.
7. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`), category (`/category`), brand (`/brand`) and deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required (search) | Keywords or a brand name, up to 200 chars |
| `category` | string or integer | required (category) | A category id (`15556`) or a category link (`.../list.html/bcc.15556_bpt.46`) |
| `brand` | string or integer | required (brand) | A brand id (`317041`, from `/brands` or `items[].brand_id`) or a brand link |
| `deal` | string | `black_friday` | Deals only: `black_friday`, `flash_sales`, `clearance`, `rock_bottom_prices`, `price_drop`, `new_items_24hr_sale`, `value_gift_sets`, `twin_packs_bundles` |
| `department` | string or integer | none (deals: `15478` Beauty) | A department id (`15478` Beauty, `15544` Skin Care). Not used on category (a `400`: send the category itself) |
| `country` | string | `us` | One of the 39 page countries |
| `language` | string | country's own | See Markets |
| `page` | integer | 1 | 100 products a page; `total_pages` says how many |
| `sort` | string | `bestsellers` | `bestsellers`, `newest`, `price_low_to_high`, `price_high_to_low`, `best_value`, `availability`, `discount` |
| `featured` | string or list | none | `in_stock`, `just_arrived`, `new_this_week`, `trending_new`, `flash_sales`, `black_friday`, `clearance`, `rock_bottom_prices`, `price_drop`, `new_items_24hr_sale`, `value_gift_sets`, `twin_packs_bundles`, `mini_travel_sizes`, `mini_size_exclusives`, `korean_brands`, `japanese_brands`, `chinese_cosmetics`, `southeast_asian_beauty`, `western_beauty`, `korean_pharmacy`, `cruelty_free`, `vegan`, `yesstyle_awards_2026`, or Featured ids from facets (key `oc`) |
| `min_price`, `max_price` | number | none | Price band in whole units of the country's currency |
| `filters` | list | none | Any other facet as {`key`, `value`} from `facets[].key` and `facets[].values[].value` (`stp` skin type, `scrn` skin concern, `si` size, `cf` color family); at most 12 filter values in all |
| `type`, `region`, `ingredients` | string or list | none | Category, brand and deals only: Type (`t`), Brand Region (`bcs`, e.g. `1` South Korea) and Ingredient (`inp`) ids from facets. On search they are a `400` |
| `include_facets` | boolean | false | Also return `facets`, `price_range` and `sorts` |

### Product (`/product`), reviews (`/reviews`), suggestions, brands, markets

| Endpoint | Parameters |
|---|---|
| `/product` | `product_id` (digits) or `url` (a yesstyle.com product link, `.../info.html/pid.<id>`), not both; `country` (39), `language`, `include_variants` (+1 credit) |
| `/reviews` | `product_id` or `url`; `page` 1-67; `sort` `relevant` (default), `highest_rating`, `newest`, `helpful`; `filter` `all` (default), `5`, `4`, `3`, `2`, `1`, `positive`, `negative`, `photo`, `video`; `include_summary` (the summary on later pages); `country` (any of 153), `language` |
| `/suggestions` | `query` (at least 2 characters), `country` (any of 153), `language` |
| `/brands` | `query` (link name contains; accents, case and punctuation ignored), `page`, `page_size` 1-5000 (default 500) |
| `/markets` | `language` (names in this language, default `en`) |

## Examples

### One product in one country

```bash
curl -X POST https://api.scavio.dev/api/v1/yesstyle/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1052684695", "include_variants": true}'
```

Captured `data` (2026-11-26; `description`, `about_brand`, `breadcrumbs`, `images`, `videos`, `ingredients`, `packs` and `notes` dropped):

```json
{
  "market": {"country": "us", "country_name": "United States", "currency": "USD", "language": "en"},
  "requested_product_id": "1052684695",
  "product_id": "1052684694",
  "parent_product_id": "1052684695",
  "name": "Advanced Snail 96 Mucin Power Essence",
  "option": "100ml",
  "brand": {"name": "COSRX", "brand_id": "317041", "region": "Brand from South Korea"},
  "price": 16.09,
  "list_price": 25,
  "discount_percent": 35,
  "currency": "USD",
  "price_text": "US$ 16.09",
  "list_price_text": "US$ 25.00",
  "sale_end_date": "2026-12-01T00:00:00Z",
  "deal_claimed_percent": 86,
  "deal_claimed_text": "Deal is 86% claimed",
  "badges": ["flash_sale"],
  "availability": "In-Stock",
  "sellable": true,
  "child_product_ids": ["1052684694"],
  "rating": 4.6,
  "review_count": 30843,
  "star_counts": {"1": 477, "2": 460, "3": 1357, "4": 4027, "5": 24522},
  "brand_satisfaction": {"percent": 96.6, "total_reviews": 264078},
  "bestseller_ranks": [{"text": "#17 in Face Serums", "department_id": "15556"}, {"text": "#67 in Skin Care", "department_id": "15544"}, {"text": "#89 in Beauty", "department_id": "15478"}],
  "product_information": [{"title": "Cruelty-free", "content": "Yes"}, {"title": "Imported from", "content": "South Korea"}, {"title": "Catalog No.", "content": "1052684695"}],
  "shipping": {"to": "Shipping to United States", "free_shipping_offer": "Free Standard Shipping with any US$ 35 purchase", "delivery_days": "7 - 11 business days"},
  "returns_days": 14,
  "coupon": {"code": "BLACK26", "name": "Week 48 - BLACK26", "tiers": [{"discount": "8% OFF", "min_order": "US$ 79 order"}, {"discount": "10% OFF", "min_order": "US$ 149 order"}, {"discount": "15% OFF", "min_order": "US$ 199 order"}], "expires_at": "2026-11-27T08:00:00Z"},
  "variants": [{"product_id": "1052684694", "name": "100ml", "availability": "In-Stock", "sellable": true, "price": 16.09, "price_text": "US$ 16.09", "currency": "USD", "flash_sale": true}],
  "variants_status": null
}
```

This call cost 3 credits (`include_variants`). A shade family returns one row per shade: Glaze Craze Tinted Lip Serum (`1134513399`, `country` `gb`) returned 11 `variants` (Sugar Glaze, Peach Glaze, Maple Glaze ... each 12.68 GBP, In-Stock).

### Search in one country

```bash
curl -X POST https://api.scavio.dev/api/v1/yesstyle/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "snail mucin"}'
```

Captured `data` (2026-11-26; `items` cut to 2 of 100, `url`, `image`, `category`, `coupon` and `notes` dropped):

```json
{
  "market": {"country": "us", "country_name": "United States", "currency": "USD", "language": "en"},
  "query": "snail mucin",
  "department": null,
  "page": 1,
  "page_size": 100,
  "sort": "bestsellers",
  "sort_applied": "Bestsellers",
  "filters_applied": [],
  "total": 422,
  "total_pages": 5,
  "has_more": true,
  "count": 100,
  "items": [
    {"product_id": "1052684695", "name": "Advanced Snail 96 Mucin Power Essence", "brand": "COSRX", "brand_id": "317041", "price": 16.09, "list_price": 25, "discount_percent": 36, "currency": "USD", "price_text": "US$ 16.09", "list_price_text": "US$ 25.00", "rating": 4.67, "review_count": 30843, "size": "100ml", "status": "FLASH SALE", "badges": ["flash_sale", "high_discount", "yesstyle_awards_2026"], "brand_region": "kr", "pack_label": "Value Set Available", "child_product_ids": ["1052684694"], "has_videos": true},
    {"product_id": "1052684665", "name": "Advanced Snail 92 All In One Cream", "brand": "COSRX", "brand_id": "317041", "price": 16.59, "list_price": 26, "discount_percent": 36, "currency": "USD", "price_text": "US$ 16.59", "list_price_text": "US$ 26.00", "rating": 4.66, "review_count": 14804, "size": null, "status": "FLASH SALE", "badges": ["flash_sale", "high_discount"], "brand_region": "kr", "pack_label": "Value Set Available", "child_product_ids": ["1052684664"], "has_videos": true}
  ]
}
```

In German (`{"query": "retinol", "country": "de"}`) the same search returned 1,258 products with German names and EUR prices: first celimax The Vita-A Retinol Shot Thightening Serum - Gesichtsserum at 18 (list 24, "18,00 €").

### Reviews filtered by stars

```bash
curl -X POST https://api.scavio.dev/api/v1/yesstyle/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1052684695", "country": "jp", "filter": "1"}'
```

Captured `data` (2026-11-26; `reviews` cut to 1 of 16, `text` shortened, `notes` dropped):

```json
{
  "market": {"country": "jp", "country_name": "Japan", "currency": "JPY", "language": "en"},
  "product_id": "1052684695",
  "page": 1,
  "page_size": 15,
  "sort": "relevant",
  "filter": "1",
  "sort_applied": "Most Relevant",
  "has_more": true,
  "count": 16,
  "summary": {"total_reviews": 30843, "star_counts": {"1": 477, "2": 460, "3": 1357, "4": 4027, "5": 24522}, "satisfaction_percent": 96.8},
  "reviews": [
    {"review_id": "38858894", "product_id": "1052684695", "rating": 1, "title": "Didn’t work for my skin", "text": "For some reason this irritated my skin a lot. ...", "date": "August 10, 2018", "helpful_count": 6, "helpful_text": "6 of 17 people found this review helpful", "images": [], "skin_type": null, "skin_tone": null, "reviewer_country": null, "translatable": false, "reviewer_group": 1}
  ]
}
```

Page 1 of the 1-star filter held 16 reviews from 15 reviewers (`reviewer_group`). `date` is as YesStyle shows it in the page language ("17. April 2026" in German).

### Deals, brand, category, suggestions, brands, markets

- `/deals` `{}` (Black Friday on Beauty, US): `total` 151 over 2 pages; first Dr. Althea 345 Relief Cream (Renewed - 50ml) at 18.9 (list 27, `status` Black Friday), with `coupon` BLACK26 (8% off a US$ 79 order, 10% off US$ 149, 15% off US$ 199, `expires_at` 2026-11-27T08:00:00Z). `{"deal": "clearance", "country": "de"}` listed 1,632; `{"deal": "flash_sales", "country": "gb"}` 6,164.
- `/brand` `{"brand": "317041"}`: COSRX, `brand` {`region` "Brand from South Korea", `satisfaction_percent` 96.6, `total_reviews` 264078}, `total` 271 over 3 pages; first Acne Pimple Master Patch (24 patches) at 4.2 (list 6). Anua in Japan (`country` `jp`) read 293 items.
- `/category` `{"category": "15556", "include_facets": true}`: Face Serums, `total` 6527 over 66 pages; first celimax The Vita-A Retinal Shot Tightening Booster at 18 (list 24, Black Friday).
- `/suggestions` `{"query": "cosrx"}`: `suggestions` ["COSRX"] and priced products (a Bundle: Azelaic Acid 10 B5 + Azelaic Acid 20 B5 Redness Soothing Cream at 33.91, list 53). Finland (`fi`, not a page country) answered for `"toner"` in EUR.
- `/brands` `{"query": "cosrx"}`: `total` 4274, `matched` 1, {`brand_id` "317041", `slug` "cosrx", `last_modified` "2025-01-17"}.
- `/markets` `{}`: 153 countries, `page_endpoint_countries` 39; each with `currency`, `language`, `page_endpoints` and `held_back` (Brazil's reason given there).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def yesstyle(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/yesstyle/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# One product priced in several shipping countries (2 credits each)
for country in ["us", "gb", "de", "jp", "kr", "au"]:
    d = yesstyle("product", {"product_id": "1052684695", "country": country})["data"]
    m = d["market"]
    print(m["country"], m["currency"], d["price"], d["list_price"], d["availability"])

# Lowest-rated reviews first page (1 credit)
r = yesstyle("reviews", {"product_id": "1052684695", "filter": "1"})["data"]
print(r["summary"], [x["title"] for x in r["reviews"]])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` (except brands and markets) and `notes`.

- **item** (search, category, brand, deals, suggestions products) - `product_id`, `name`, `brand`, `brand_id`, `url`, `image`, `price`, `list_price`, `discount_percent`, `currency`, `price_text`, `list_price_text`, `rating`, `review_count`, `size`, `status`, `badges`, `brand_region`, `pack_label`, `child_product_ids`, `has_videos`.
- **list** (search, category, brand, deals) - `page`, `page_size` (100), `sort`, `sort_applied`, `filters_applied`, `total`, `total_pages`, `has_more`, `count`, `items[]`, `heading`, `description`, `breadcrumbs`, `category` (tree), `facets` / `price_range` / `sorts` (with `include_facets`: {`name`, `type`, `key`, `values[]` {`value`, `name`, `selected`}}), `coupon`; plus `query` and `department` (search), `category_id` (category), `brand_id` and `brand` {`name`, `region`, `satisfaction_percent`, `total_reviews`, `star_counts`} (brand), `deal` and `department_id` (deals).
- **product** - `requested_product_id`, `product_id`, `parent_product_id`, `name`, `option`, `brand` {`name`, `brand_id`, `url`, `region`}, `url`, `canonical_url`, `description`, `about_brand`, `breadcrumbs[]` {`id`, `name`, `url`}, `images`, `videos`, `price`, `list_price`, `discount_percent`, `currency`, `price_text`, `list_price_text`, `sale_end_date`, `deal_claimed_percent`, `deal_claimed_text`, `badges`, `availability`, `sellable`, `child_product_ids`, `rating`, `review_count`, `star_counts`, `brand_satisfaction` {`percent`, `total_reviews`}, `ingredients`, `ingredient_notes`, `bestseller_ranks[]` {`text`, `department_id`}, `packs[]` {`title`, `product_id`, `url`, `image`, `price`, `price_text`, `saving_text`}, `product_information[]` {`title`, `content`}, `shipping` {`to`, `free_shipping_offer`, `delivery_days`}, `returns_days`, `coupon`; with `include_variants`: `variants[]` {`product_id`, `name`, `availability`, `sellable`, `price`, `price_text`, `currency`, `flash_sale`} and `variants_status` (`null` when read; `unavailable` when the list could not be read, and then that part is not charged).
- **reviews** - `product_id`, `page`, `page_size`, `sort`, `filter`, `sort_applied`, `has_more`, `count`, `summary` {`total_reviews`, `star_counts`, `satisfaction_percent`} (page 1, or with `include_summary`), `reviews[]` {`review_id`, `product_id`, `rating`, `title`, `text`, `date`, `helpful_count`, `helpful_text`, `images[]` {`url`, `thumbnail`}, `skin_type`, `skin_tone`, `reviewer_country`, `translatable`, `reviewer_group`}.
- **suggestions** - `query`, `count`, `suggestions` (terms), `products[]` (items).
- **brands** - `query`, `total`, `matched`, `page`, `page_size`, `has_more`, `count`, `brands[]` {`brand_id`, `slug`, `url`, `last_modified`}.
- **markets** - `language`, `count`, `page_endpoint_countries`, `countries[]` {`country`, `name`, `country_id`, `currency`, `language`, `page_endpoints`, `held_back`}, `currencies[]` {`code`, `name`}, `languages[]` {`code`, `name`, `lang_id`}.

## Guardrails

- Name it "YesStyle (yesstyle.com, the Hong Kong-based online store for Asian beauty and fashion, shipping to 150+ countries)" on first mention, "YesStyle" after that.
- Prices: quote each with its currency, the shipping country and the `fetched_at` date ("listed on yesstyle.com for the United States on Nov 26, 2026"). YesStyle prices by shipping country; never present one country's price as YesStyle's price everywhere, and never convert one country's price to stand for another.
- Availability: report it for the country it was read for; a product priced for a country can still be "Not available for your shipping destination".
- Discounts: `discount_percent` and `list_price` as YesStyle shows them; a coupon price is computed, never checked out.
- Reviews: quote titles, texts, ratings and dates as given; no reviewer names, gender or age are returned, and none should be inferred. `skin_type` and `skin_tone` describe the review, not a person to identify.
- Descriptive only: no commentary on YesStyle's business, pricing practices or policies. Quote YesAsia figures only with their source and date.
- Do not republish YesStyle product photos, descriptions or logos. Write yesstyle.com as plain text and cite product names, product ids, countries and capture dates rather than linking YesStyle pages.
- Terms: Scavio does not collect or store YesStyle data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account, no cart and no checkout. YesStyle's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, list prices, discounts, sale dates, product ids, availability or reviews. Only return what the API returned, with the `fetched_at` time.
- Not available: stores, currency choice, EAN or UPC, price history (store your own), Brazil on the page endpoints, cart or checkout.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `query`; a `country` YesStyle does not ship to, or not among the 39 on a page endpoint ("Brazil is held back: ..."); a `language` outside the list; `product_id` and `url` both sent or neither ("product_id or url is required ..."); a `product_id` that is not digits; a link that is not yesstyle.com; `type`, `region` or `ingredients` on search ("... is a category filter: YesStyle applies it on category, brand and deals pages, not on search."); `department` on category ("department is not used here: send the category itself."); more than 12 filter values; `min_price` above `max_price`; suggestions `query` under 2 characters; reviews `page` above 67.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Product 1000000001 was not found on YesStyle." Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api).
- `502` means YesStyle data was temporarily unavailable ("YesStyle is temporarily unavailable. Please try again."), or every attempt came back priced for another country ("YesStyle is temporarily unavailable for <country> (<code>). Please try again."). Not charged: retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy: wait the `Retry-After` seconds and send it again. Not charged.
- A list with `total` 0 in a `200` (search `cosrx` in the UAE) means nothing in that list ships to that country, not that the product does not exist. Try another country or the product endpoint.
- `variants_status` `unavailable` means the shade and size list could not be read this time (that part not charged); request a `child_product_ids` id for its own page, or retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: product } = await scavio.yesstyle.product({ product_id: "1052684695", country: "jp", include_variants: true });
const { data: results } = await scavio.yesstyle.search({ query: "snail mucin", country: "gb", sort: "discount" });
const { data: deals } = await scavio.yesstyle.deals({ deal: "flash_sales", country: "de" });
const { data: reviews } = await scavio.yesstyle.reviews({ product_id: "1052684695", filter: "photo" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.yesstyle.search(...)`, `category`, `brand`, `brands`, `deals`, `product`, `reviews`, `suggestions` and `markets`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_yesstyle`, `get_yesstyle_category`, `get_yesstyle_brand`, `get_yesstyle_brands`, `get_yesstyle_deals`, `get_yesstyle_product`, `get_yesstyle_reviews`, `get_yesstyle_suggestions` and `get_yesstyle_markets`. YesStyle is opt-in: add `yesstyle` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,yesstyle"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/yesstyle-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [category](https://scavio.dev/docs/yesstyle-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [brand](https://scavio.dev/docs/yesstyle-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [brands](https://scavio.dev/docs/yesstyle-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [deals](https://scavio.dev/docs/yesstyle-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [product](https://scavio.dev/docs/yesstyle-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [reviews](https://scavio.dev/docs/yesstyle-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api), [suggestions](https://scavio.dev/docs/yesstyle-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api) and [markets](https://scavio.dev/docs/yesstyle-markets?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api). Overview: [scavio.dev/yesstyle-api](https://scavio.dev/yesstyle-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=yesstyle-api).
