<div align="center">

# Scavio Agent Skills

**Give your AI agent live data from 78 platforms as structured JSON, through one API key**

[![Platforms](https://img.shields.io/badge/Platforms-78-blue?style=flat-square)](https://scavio.dev)
[![Endpoints](https://img.shields.io/badge/Endpoints-447-green?style=flat-square)](https://scavio.dev/docs)
[![Skills](https://img.shields.io/badge/Skills-80-orange?style=flat-square)](#skills)
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black?style=flat-square)](https://skills.sh/scavio-ai/skills)
[![Agents](https://img.shields.io/badge/Agents-40+-blueviolet?style=flat-square)](https://skills.sh)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Overview](#overview) | [Install](#install) | [Setup](#setup) | [Skills](#skills) | [Which skill](#which-skill-do-i-want) | [Links](#links)

</div>

---

## Overview

[Scavio](https://scavio.dev) is a unified web data API: one key, 78 platforms, structured JSON instead of HTML. This repo holds 81 Agent Skills: one per platform, a website crawler skill, plus `scavio`, an umbrella that covers all of them from a single install. A skill teaches your agent which Scavio endpoints exist for a platform, what parameters they take, what the response looks like, and what each call costs in credits, so the agent can call the API correctly without you writing an integration. Every skill is in the open Agent Skills format and loads in Claude Code, Cursor, Codex, OpenCode, Goose, OpenHands, Hermes Agent, OpenClaw, and any other client that reads the format.

## Install

One skill for everything:

```
npx skills add scavio-ai/skills --skill scavio
```

Or one skill per platform, picking the ones you use:

```
npx skills add scavio-ai/skills --skill amazon-product-data --skill google-search-api
```

Without `--skill` the CLI opens a picker; `--all` installs every skill into every agent it detects. To see what is in the repo before installing anything:

```
npx skills add scavio-ai/skills --list
```

To install straight into a specific agent, pass `-a`:

```
npx skills add scavio-ai/skills --skill scavio -a claude-code -a opencode
```

Any client that reads the Agent Skills format can also load a folder directly. Clone this repo and point the client at the repo root, or copy a single skill directory into wherever that client keeps its skills.

### Umbrella or per-platform

`scavio` is one `SKILL.md` that routes to a `references/` file per platform. Your agent carries one description in its context instead of fifty, and the platform detail loads only when a platform is used. The per-platform skills are the same content split up: each one is a fifth of what the umbrella loads per call, and each has its own trigger, so they fit a project that uses two or three platforms. Install one or the other, not both.

Hermes Agent caps a community skill at 50 files and the umbrella ships 81, so on Hermes install the per-platform skills instead; every one of them passes the Hermes scan.

## Setup

The skills need one environment variable:

```
export SCAVIO_API_KEY=...
```

Get the key at [scavio.dev](https://scavio.dev). The free tier is 50 credits on signup, no card required.

## Skills

### Search

| Skill | What it does |
| --- | --- |
| `google-search-api` | Full Google SERP as JSON: organic, ads, knowledge graph, AI Overview, PAA; drop-in Custom Search JSON API replacement |
| `google-ai-mode-api` | Google AI Mode answers with their cited sources |
| `chatgpt-scraper-api` | ChatGPT's answer to a prompt with its cited pages, web searches and recommended products, for AI visibility tracking |
| `gemini-scraper-api` | Gemini's answer to a prompt with its cited URLs and recommended products, same shape as ChatGPT |
| `google-news-api` | Headlines by keyword, topic, story or publication |
| `google-trends-api` | Search interest over time, by region, and related queries |
| `google-maps-api` | Local business search, place detail, reviews, and a local-SEO geo-grid |

### Commerce

| Skill | What it does |
| --- | --- |
| `amazon-product-data` | Keyword search, ASIN detail, and all seller offers with the buy box |
| `ebay-product-data` | Live and sold listings for comps, plus listing and seller detail |
| `walmart-product-data` | Search, item detail, reviews, categories, offers, and seller storefronts |
| `target-product-data` | Search, category browse, TCIN detail, and reviews with store-aware pricing |
| `home-depot-product-data` | Search with per-store pickup and delivery, item specs, and reviews |
| `costco-product-data` | Search with per-warehouse shelf prices, online vs in-warehouse prices, stock, gas, coupons, deals, and clearance |
| `heb-grocery-data` | Search, product detail with ingredients and nutrition, and store locator, with per-store prices, stock and aisle via `store_id` |
| `kroger-grocery-data` | Kroger, QFC and Fred Meyer search, category, product detail and weekly digital deals, price, stock and aisle for up to 25 UPCs at the store you choose, a store locator, and digital coupons |
| `publix-api` | Publix weekly ad and BOGO list, Extra Savings, digital coupons and one keyword across all three at the store you choose, search and category listings with aisle and promo, product cards with nutrition, the deli and bakery order-ahead menu with each store's Pub Sub prices, and a store locator with each store's weekly-ad start day; prices only where Publix shows them (promotions and order-ahead items) |
| `decathlon-product-data` | Decathlon sporting-goods search and product detail across country sites |
| `specs-liquor-prices` | Spec's (Texas) search, every store's price and stock for a product in one call, and a store locator by region |
| `lowes-product-data` | Lowe's search, item detail and deals at the store you choose (price, was-price, units on hand, aisle and bay, nearby-store stock), a store locator, and reviews |
| `sams-club-product-data` | Sam's Club search, item detail with the club shelf price, stock and aisle at the club you choose, a club locator, Instant Savings, category and clearance listings, and reviews |
| `canadian-tire-api` | Canadian Tire search and product detail at the store you choose (CAD price, stock, aisle), price and stock for up to 50 SKUs, a store locator with per-store stock, and each store's clearance and deals |
| `dollar-general-api` | Dollar General search and UPC lookup at the store you choose (price, units on hand), one product's stock at up to 25 nearby stores, on-sale and clearance listings, and digital coupons |
| `aldi-grocery-data` | ALDI search and product detail at the store you choose (price, sale price, unit price, stock level, in-store location) for in-store, pickup or delivery, plus a store locator |
| `walgreens-product-data` | Walgreens search and product detail with national prices, coupons, rewards and rebates, a store locator, and live unit counts at up to 20 stores in one call |
| `cvs-product-data` | CVS search with prices, ExtraBucks and manufacturer coupons and stock at the store you choose, product detail, and stock for up to 20 SKUs at one store |
| `sephora-product-data` | Sephora search and category listings, and product detail with every shade or size, stock per shade, and the review summary with pro and con sentiment counts |
| `ulta-beauty-api` | Ulta Beauty search and category listings, product detail with every shade, the latest reviews, and in-stock or out-of-stock per shade at the 10 stores nearest a ZIP |
| `micro-center-api` | Micro Center search and product detail at the store you choose (stock count capped at 25+, open-box units and price), stock flags at every store, and the store list |
| `whole-foods-grocery-data` | Whole Foods Market search, category and deals listings at the store you choose (shelf, sale and Prime member price), product detail with nutrition and in-store vs online price, a store locator, store detail, and the weekly sales flyer |
| `harbor-freight-api` | Harbor Freight search and clearance with national, sale, coupon and Inside Track member prices, product detail with specs and manuals, batch prices for 50 items, a store locator, in-stock or out-of-stock status and aisle at nearby stores, and reviews |
| `petsmart-product-data` | PetSmart search and product detail with national prices, every size and flavor, sale end dates and Autoship first-order and recurring prices, a store locator, live unit counts at one store or across store and SKU pairs, and the Sale section |
| `petco-product-data` | Petco search and category listings with price, list price and Repeat Delivery autoship price per size, product detail with UPC and ingredients, a store locator, and units on hand for up to 10 products at one store |
| `iherb-product-data` | iHerb search by keyword or brand, product detail with supplement facts, price per serving and variants, price and stock for up to 50 products in one call, and the review summary (US store, USD) |
| `chewy-product-data` | Chewy search and category listings with one-time, Autoship and first-Autoship prices and ratings, and product detail with MAP price, star distribution, specifications and every size and flavor variant |
| `menards-product-data` | Menards product detail by item id or URL with the everyday and sale price, mail-in rebates and the price after rebate, stock quantity and aisle at the store you choose, and a store locator (no search) |
| `nordstrom-product-data` | Nordstrom search, category and sale-section listings and brand catalogs with current and original price, percent off, rating, badges, marketplace seller, every color and filter counts, sortable by percent off; product detail with every size and color as a SKU (UPC, regular or clearance price, stock, units available to ship), the star histogram, size-fit distribution and the reviews on the page; review history up to 200 per call, sorted and filtered by stars, verified purchase, photos or text, with the rating summary and AI review summary; per-SKU ship and store-pickup availability with the stores that can do pickup; a store locator with hours and services; and search autocomplete |
| `nordstrom-rack-product-data` | Nordstrom Rack (nordstromrack.com) search, /shop and /clearance category listings including Clear the Rack and flash events, and brand catalogs with current and compare-at price, percent off, the clearance price and any extra-off promotion price on top, rating, badges, every color and filter counts, sortable by percent off; product detail with every size and color as a SKU (UPC, price type, stock, units available to ship), the star histogram, size-fit distribution and the reviews on the page; Rack's own review history up to 200 per call, sorted and filtered by stars, verified purchase, photos or text; per-SKU ship and Rack store-pickup availability with the stores that can do pickup; a Rack store locator with hours; and search autocomplete |
| `best-buy-product-data` | Best Buy (bestbuy.com) search and category or deals-page listings, 18 per page, with price, regular price, savings, deal badge, condition, rating and seller type, filtered by brand, on sale, clearance, open box or a price range; product detail with UPC, model, every open-box offer by condition (fair, good, excellent) with its price and savings, the full spec table and the AI review summary; store pickup status of a SKU at up to 8 stores near a ZIP (in stock, limited, ship to store, out of stock); a store locator with 35 days of dated hours; today's Deal of the Day; batch prices for up to 15 SKUs; first-party reviews with the star histogram and pros and cons; and search autocomplete |
| `tcgplayer-api` | TCGplayer (tcgplayer.com) card and sealed-product search across Pokemon, Magic, Yu-Gi-Oh!, One Piece, Lorcana and 70+ games; product detail with the market price of every SKU (condition x printing x language) and its recent sale range; every live seller listing with price, shipping and seller rating; up to a year of price history with quantity sold; the 5 most recent sales; a set's full price guide; sets and games; autocomplete and trending searches; and seller profiles, feedback and catalogues |
| `vinted-api` | Vinted second-hand listing search on 27 country sites (France, UK, US, Germany, Poland, Spain, Italy, the Netherlands, Australia and more) by keyword, category, brand, condition, size, color, material and price range, 96 per page with price, the Vinted fee and the total; listing detail with category path, photos and sold or reserved state; seller profiles, listed items and reviews; brand ids, filter options with live counts, the localized category tree and search autocomplete |
| `macys-product-data` | Macy's (macys.com) search, category, brand-page and sale-section listings (Sales & Offers, Clearance, Today Only, Last Act, Limited-Time Specials, Black Friday Deals), 60 per page, with current, regular and sale price, percent off, sale end date, deal label, promotions, rating and colors, filtered by brand, color, special offer, any price range, store pickup or any facet; product detail with every variant (UPC, color, size, availability), each color's price, the rating histogram and fit; up to 10 products per call for price tracking; Macy's own reviews up to 100 per page; stores near a ZIP, a point or a city with pickup cut-off; and store pickup near you or per variant at one store |
| `saks-fifth-avenue-api` | Saks Fifth Avenue (saksfifthavenue.com) search, category, designer-page and sale or new-arrival listings (Sale, Women's Clothing Sale, Men's Sale, Women's and Men's New Arrivals), 24 grid positions per page with `start` / `next_start` paging, with price, regular and sale price, percent off, badge, final-sale, clearance and returnable flags, promotions and colors, filtered by designer, color, size, any price range, on sale, new arrivals or any facet; product detail with every color and size, per-SKU online units, restock date, the average rating and review count (no review text); a variant's stock at nearby Saks pickup stores with the store's unit count where shown; stores near a ZIP or a point; search suggestions; and the A-Z designer index |
| `kohls-product-data` | Kohl's (kohls.com) search, category, brand and deal listings (Clearance, Sale, Earn Kohl's Cash, Sephora at Kohl's), 120 products per page with sponsored items flagged, with current, regular and sale price, sale or clearance label, percent off, the price after a public coupon code with the code, BOGO promotions, rating, review count and badges, filtered by brand, color, size, on sale, clearance or any facet (price buckets, discount, rating, store pickup); product detail with every variant's SKU, UPC, online units and price, Kohl's Cash earn and redeem windows and the offers that apply, plus one store's price per variant; one SKU's pickup unit count at every store within about 50 miles of a ZIP; stores near a ZIP, a city or a point; search suggestions; and today's public coupon codes |
| `jcpenney-product-data` | JCPenney (jcpenney.com) search, category, brand and deal listings (Clearance, Sale, Black Friday, Big Buy, Limited Time Special, Closeout, Buy 1 Get 1), 48 products per page up to 25 pages, with the current and regular price range, price type, percent off, deal label, the price after today's coupon with the code, rating, review count and colors, filtered by brand, color, size, price range, deal label or any facet; product detail with every variant's SKU, UPC, color, size and online stock level, or up to 20 products per call for price checks (prices are product-level ranges); real unit counts for one SKU at the 5 nearest stores to a ZIP; stores near a ZIP, a city or a point with hours and services; search suggestions; today's public coupon codes; review text with five sorts, a star filter and verified, incentivized and syndicated badges; and product Q&A with every answer labelled brand, JCPenney staff, AI or customer |
| `dicks-sporting-goods-api` | Dick's Sporting Goods (dickssportinggoods.com) search, category, brand and deal listings (Clearance, Sale, This Week's Deals), 48 products per page by default up to 144, with the current and list price range, percent off, rating, review count, badge, colors, pinned items flagged and the offer-price windows Dick's has planned, filtered by brand, an approximate price range or any facet; product detail with every SKU's own price, list price, clearance flag, UPC and online units (sizes and colors are priced separately), or a style-level summary of up to 5 products per call; unit counts for up to 20 SKUs at up to 100 Dick's, Golf Galaxy or Public Lands stores near a ZIP; the 15 newest reviews with rating statistics; and search suggestions |
| `foot-locker-api` | Foot Locker release calendar for the US, Canada and the UK (launch date and time, retail price, colorway, heat level, size run, reservation windows) as monitoring data; search, category, brand and deal listings (Sale, Foot Locker Exclusives, promo-code-eligible) on footlocker.com and 12 country storefronts in local language and currency, 48 products per page with price, list price, percent off, the EU 30-day lowest price, rating and each colorway's price, filtered by brand, gender, color, price, shoe size or any facet; product detail with per-size availability (yes / no to ship and pick up, and how many stores show each size) and launch info; US store locator and which nearby stores show a size as available; US review text and shopper Q&A |
| `fanatics-merchandise-api` | Fanatics merchandise (not sportsbook) search, team / player / league / department / brand / collection listings and Sale, Clearance and Under-25 deals on fanatics.com, 7 international storefronts (UK, Germany, France, Spain, Italy, Japan, Canada) in local language and currency and the US league stores (NFL Shop, MLB Shop, NHL Shop, MLS Store), up to 72 products per page with current, regular, sale, clearance and with-code price, ship-by and delivery estimates; product detail with per-size availability and stock level (low / out), the active promo code, personalization fields and team roster, Jersey Assurance and authentic flags and fit / value / quality ratings; US review text pooled across the style with the site's AI-written summary |
| `carrefour-api` | Carrefour (carrefour.fr) search, category (aisle) and promotion listings (catalogue, immediate discounts, loyalty-card offers, festive selection), 30 products per page with price, unit price per kg or litre, the promotion with its loyalty-card flag and dates, Nutri-Score, Eco-Score, rating and marketplace seller, filtered by brand, promotion, Nutri-Score, organic, Carrefour brands or price; the national online price or one store's shelf price and range via a store ref; product detail with ingredients, allergens and nutrition; verified reviews; stores near a French postal code, which nearby stores carry a product (yes / no, no price), and a store's services, hours, next pickup slot and fuel prices per litre; search and product also on Carrefour Argentina, Romania and Belgium in local language and currency |
| `allegro-api` | Allegro (allegro.pl, plus allegro.cz, allegro.sk and allegro.hu in local language and currency) search and category listings, 60 organic offers per page plus sponsored slots, with price, price incl. delivery, condition, auction state, discount and the EU 30-day lowest price, sold counts, Allegro Smart!, the seller and the placement (regular, promoted, sponsored), filtered by price, new or used, buy now or auction, Smart! and the deals zone; offer detail with parameters, GTIN, delivery prices, stock, returns, warranty and auction bids; catalog product detail with the lowest price, offer count, buy-box offer, star distribution and the first 20 reviews; every seller's offer for one product; a seller's offers and categories and the seller's buyer ratings |
| `olx-api` | OLX Europe classifieds (olx.pl, olx.ro, olx.pt, olx.bg, olx.ua, olx.kz, olx.uz; not OLX Brasil, OLX India or Dubizzle-run OLX sites) search by keyword or category, sorted by newest or price and filtered by price, condition, private or business seller, OLX delivery, location with a radius and each category's own filters (rooms, area, year, mileage), up to 1,000 results per search with promoted ads flagged by slot, in each site's currency and language; ad detail with every parameter, breadcrumb, photos and job salary ranges; a seller's business flag, business name, member-since date and live ads; category tree, location ids, search suggestions and similar ads. Private sellers' names and contact details are never returned |
| `ikea-api` | IKEA prices by country: one article number on up to 10 IKEA country sites in one call, each in its own currency; search, category and deal listings (new lower price, last chance, IKEA Family price), product detail with packages and assembly PDFs, the 20 newest reviews, stores, stock level by store, batch lookup and As-is second-hand offers on 55 markets |
| `wayfair-api` | Wayfair (wayfair.com, wayfair.ca in English or French, wayfair.co.uk, wayfair.ie, plus AllModern, Birch Lane, Joss & Main and Perigold) search and category listings with price, sale price, was price (Wayfair's strikethrough), price label, badge, rating, stock and open-box price, sorted by price or rating and filtered by sale, closeout, open box, brand or price; product detail with every option and the price of one option, the rating histogram, review summary, the 5 reviews on the page and a delivery estimate to a US ZIP or Canadian postal code; current sale events. Poll it to build a Wayfair price history |
| `mercadolibre-product-data` | Mercado Libre and Mercado Livre search by keyword or seller, product detail with the buy-box seller, reviews, buyer questions, and best sellers (MX, BR, AR, CO) |
| `google-shopping-api` | Product search with price filters, product detail, and every store selling it |
| `aliexpress-product-data` | Search, category browse, product with every SKU variant, translated reviews, and seller storefronts |
| `etsy-product-data` | Listing search, listing detail with variations and reviews, shop profiles and shop reviews |
| `tiktok-shop-api` | Catalog search, product detail, reviews, categories, and shop catalogs |

### Social and video

| Skill | What it does |
| --- | --- |
| `instagram-scraper-api` | Profiles, posts, reels, stories, highlights, comments, likers, followers, and search |
| `tiktok-scraper-api` | Profiles, videos, transcripts, comments, hashtags, sounds and charts, trending, similar creators, live status, and search |
| `youtube-data-api` | Video and channel search, metadata, comments, transcripts, community posts, and streams |
| `twitter-scraper-api` | Tweet and people search, tweet detail, profiles, followers, Communities, and trends |
| `reddit-search-api` | Post, comment and subreddit search, post detail, threaded comments, and redditor profiles |
| `linkedin-scraper-api` | Person and company profiles, their posts, job search, and job detail |
| `facebook-scraper-api` | Page profile, posts, reels and photos, post comments, groups, events, and hashtag posts |
| `threads-net-api` | Threads profiles, posts, replies, post detail, and people search |
| `pinterest-api` | Pin search, pin detail with save counts, user profiles, boards, and URL save counts |
| `twitch-api` | Channel profile and live status, VODs, stream schedule, and clip download URLs |
| `douyin-scraper-api` | Videos, profiles, feeds, comments, hashtags, music, live rooms, hot search, and keyword search |
| `weibo-scraper-api` | Profiles, posts, comments, keyword search, and hot-search and ranking boards |
| `kuaishou-scraper-api` | Kuaishou.com profiles, videos, comments, hashtags, and search |

### Travel

| Skill | What it does |
| --- | --- |
| `airbnb-scraper-api` | Stay search with the discount ledger, listing detail, and guest reviews |
| `booking-com-hotel-data` | Destination search with live nightly prices, property detail, and reviews |
| `google-hotels-api` | Hotel search for a stay, plus per-property booking-site vendor prices |
| `google-flights-api` | Route search by date with price, carrier, duration, and stops |
| `tripadvisor-reviews-api` | Resolve places, list ranked venues in a geo, location detail, and reviews |

### Jobs and reviews

| Skill | What it does |
| --- | --- |
| `indeed-jobs-api` | Job search, full posting detail with the ATS link, employers, and reviews |
| `glassdoor-salary-data` | Salary percentiles by title, employer profiles, ratings, and reviews |
| `g2-software-reviews-api` | B2B product search, profiles with pricing editions, and faceted reviews |
| `capterra-reviews-api` | Software search, full profiles with the pricing table, and scored reviews |
| `trustpilot-reviews-api` | Business search with TrustScore, full profiles with reply rate, filtered reviews, and category rankings |
| `yelp-business-data` | Business search, full business detail with hours, and review pages |

### Real estate

| Skill | What it does |
| --- | --- |
| `zillow-property-data` | For sale, rent and sold listings, property detail, Zestimate, agent profiles |
| `redfin-property-data` | Listing search, property detail with Redfin Estimate, and market stats |
| `realtor-com-property-data` | For sale, pending, rent and sold search at up to 200 rows per call, property detail with valuations and tax history, market stats, agents |
| `rightmove-property-data` | UK listings for sale and to rent, full listing detail, England and Wales sold prices since 1995, agent branches |

### App stores

| Skill | What it does |
| --- | --- |
| `apple-app-store-api` | App search, listing detail by App Store or bundle id, and user reviews |
| `google-play-store-api` | Android app search, listing with install counts and Data safety, reviews |

### Companies and code

| Skill | What it does |
| --- | --- |
| `sec-edgar-api` | Ticker to CIK, filer profile, filings with documents, XBRL, full-text search |
| `companies-house-api` | UK company search, register entry, officers, and filing history PDFs |
| `company-enrichment-api` | A business's published emails, phone numbers, social profiles and contact page, plus the owner or founder's name and title with the page that names them, from its website or a Google Maps place_id |
| `github-api` | Profiles, repos, READMEs, releases, issues, search, and repo dossier and velocity composites |

### Ads

| Skill | What it does |
| --- | --- |
| `google-ads-transparency-api` | Advertiser lookup and the live ad creatives a brand runs, with dates |
| `meta-ad-library-api` | Facebook and Instagram ad search by keyword, Page id, or archive id |
| `tiktok-ad-library-api` | Ad search by keyword or industry, top-performing ads, and single-ad detail with video |
| `linkedin-ad-library-api` | Ad search by keyword or advertiser, and single-ad detail with media and payer |

### Utility

| Skill | What it does |
| --- | --- |
| `url-to-markdown-api` | Any URL to clean Markdown, plain text, or raw HTML for prompts and RAG |
| `website-screenshot-api` | Full-page PNG of any public URL as an inline base64 image |
| `website-crawler-api` | Crawl a whole site to Markdown, map every URL from its sitemap, and batch extract up to 1,000 URLs as one job |

### Umbrella

| Skill | What it does |
| --- | --- |
| `scavio` | All 78 platforms behind one trigger: routing table, shared setup, request format, cost gate, and failure handling, with a reference file per platform |

## Which skill do I want

**I need prices for a product across retailers.** Start with `google-shopping-api` for the cross-merchant view, then go per retailer: `amazon-product-data` for ASIN detail and offers, `walmart-product-data`, `target-product-data`, `home-depot-product-data`, `costco-product-data`, `heb-grocery-data` for groceries, `kroger-grocery-data` for Kroger, QFC and Fred Meyer prices by store and digital coupons, `publix-api` for the Publix weekly ad, BOGO list, Extra Savings, digital coupons and Pub Sub prices store by store, `carrefour-api` for Carrefour France grocery prices by store, promotions with the loyalty-card flag and Nutri-Score (plus Carrefour Argentina, Romania and Belgium), `specs-liquor-prices` for liquor, wine and beer, `lowes-product-data` for home improvement, `sams-club-product-data` for warehouse-club prices, `dollar-general-api` for discount stores, `aldi-grocery-data` for ALDI groceries, `walgreens-product-data` and `cvs-product-data` for drugstores, `sephora-product-data` and `ulta-beauty-api` for beauty, `nordstrom-product-data` for fashion prices, markdowns, per-size stock, store pickup and reviews, `nordstrom-rack-product-data` for Nordstrom Rack clearance, Clear the Rack and flash-event prices, Rack store pickup and Rack reviews, `best-buy-product-data` for Best Buy open-box prices by condition, store pickup stock, the Deal of the Day and batch price checks, `macys-product-data` for Macy's sale, clearance, Last Act and Black Friday prices, batch price checks and store pickup by size and color, `saks-fifth-avenue-api` for Saks Fifth Avenue designer sale prices, per-SKU stock, store stock and the designer index, `kohls-product-data` for Kohl's clearance, Kohl's Cash, coupon-code prices and store pickup unit counts, `jcpenney-product-data` for JCPenney clearance, after-coupon prices, today's coupon codes, store unit counts, reviews and Q&A, `dicks-sporting-goods-api` for Dick's Sporting Goods clearance by size and color, per-SKU prices and store unit counts at Dick's, Golf Galaxy and Public Lands, `foot-locker-api` for the Foot Locker release calendar, per-size availability and sale prices on 13 storefronts, `fanatics-merchandise-api` for Fanatics jersey prices, sale, clearance and with-code prices, size stock levels and the NFL, MLB, NHL and MLS league shops, `micro-center-api` for PC parts and open-box stock, `whole-foods-grocery-data` for Whole Foods store prices, Prime deals and the weekly flyer, `petsmart-product-data`, `petco-product-data` and `chewy-product-data` for pet supplies with autoship prices, `iherb-product-data` for supplements and vitamins, `harbor-freight-api` for tools, coupons and member prices, `menards-product-data` for Menards prices, rebates and store stock, `canadian-tire-api` for Canada, `decathlon-product-data`, `aliexpress-product-data`, and `mercadolibre-product-data` for Mexico, Brazil, Argentina and Colombia. For resale and used comps, `ebay-product-data` searches sold listings. For trading card prices (Pokemon, Magic, Yu-Gi-Oh! and the rest), `tcgplayer-api` gives TCGplayer market prices by condition and printing, price history with units sold, live listings and set price guides. For Allegro, Poland's largest marketplace (and allegro.cz, allegro.sk and allegro.hu), `allegro-api` gives every seller's price and price with delivery for one product, the EU 30-day lowest price on discounts, sold counts, auctions and seller ratings. For OLX classifieds in Poland, Romania, Portugal, Bulgaria, Ukraine, Kazakhstan and Uzbekistan (the OLX Europe sites), `olx-api` gives asking prices for used goods, cars, property and rentals with each category's own filters, salary ranges from job ads, and business sellers, with promoted ads flagged and no private-seller contact details. For second-hand fashion across Europe, the UK, the US and Australia, `vinted-api` searches Vinted's live listings in each site's currency with the Vinted fee and checks sellers before you buy. For IKEA prices by country, `ikea-api` prices one article number on up to 10 IKEA country sites in one call in each site's own currency, and adds product detail, stock level by store, reviews and As-is second-hand offers. For Wayfair price history, `wayfair-api` reads price, sale price and the was (strikethrough) price per SKU and per size or color on wayfair.com, wayfair.ca, wayfair.co.uk, wayfair.ie and the AllModern, Birch Lane, Joss & Main and Perigold sites, for you to poll and store. For handmade and vintage, `etsy-product-data`.

**I need a lead list of local businesses.** `google-maps-api` gives places, addresses, phone numbers, hours, and coordinates for a query and map center. `company-enrichment-api` turns each result's place_id (or any business website) into the emails, phones and socials the business publishes, plus the owner's name and title with a source. `yelp-business-data` adds price band, amenities, and review text for the same kind of venue. `trustpilot-reviews-api` ranks online businesses in a category by star rating, with the website and the email and phone they published. `tripadvisor-reviews-api` covers restaurants, hotels, and attractions ranked within a geo.

**I need to feed a RAG index or an LLM prompt.** `url-to-markdown-api` converts arbitrary pages to Markdown chunks, and `website-crawler-api` crawls a whole docs site or sitemap to Markdown in one job. For discussion text, `reddit-search-api` returns threaded comments. For video, `youtube-data-api` returns transcripts. For code and issues, `github-api` returns READMEs, releases, and issue threads.

**I need to see what a competitor is doing.** `google-ads-transparency-api`, `meta-ad-library-api`, `tiktok-ad-library-api` and `linkedin-ad-library-api` return the ad creatives a brand is running and when they ran. `g2-software-reviews-api` and `capterra-reviews-api` return their pricing tables and review facets. `glassdoor-salary-data` and `indeed-jobs-api` return what they pay and what they are hiring for.

**I need one install that covers everything.** `scavio`.

## Links

- Docs: [scavio.dev/docs](https://scavio.dev/docs)
- Hosted MCP server: [mcp.scavio.dev](https://mcp.scavio.dev)
- Python SDK: `pip install scavio`
- JavaScript SDK: `npm i scavio`

## Regenerating

`skills/` is generated from `../openclaw/`, the single source of truth shared with ClawHub.
Do not hand-edit it. Edit the source skill, then:

```
python3 build.py       # regenerate skills/, including the scavio umbrella
python3 verify.py      # prove nothing but naming, H1 and UTM changed
python3 build.py --check   # exits 1 if skills/ is stale
```

The umbrella is generated too: `umbrella.md` is its router template, the platform table
comes from `naming.json`, and every `skills/scavio/references/<slug>.md` is the body of the
matching per-platform skill, byte for byte.

`verify.py` asserts the technical body is byte-identical to the source, the umbrella
references are byte-identical to the generated skills, the frontmatter parses as YAML, names
are unique, every prose link carries a UTM, every skill is listed in this README, no example
reads an environment key, and every install is version-pinned.
