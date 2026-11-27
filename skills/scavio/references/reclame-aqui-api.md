# Reclame Aqui API - Company Reputation, Complaints, Rankings, Segments

Read Reclame Aqui (reclameaqui.com.br, Brazil's company complaint and reputation site): company search, one company's reputation by period, its complaints with the site's tabs and filters, one complaint with its whole thread, complaint search across every company, the 11 site-wide rankings, the segment list and each segment's best and worst companies. Brazil only, Portuguese text as published, no prices. Every endpoint returns structured JSON and costs 1 credit (company complaints addressed by shortname 2).

**The job this skill is for: how a Brazilian company's reputation reads on Reclame Aqui today, and what its complaints are about.** The site scores each company per period and this skill returns each number as the site publishes it, never computed. On 2026-11-27 Nubank (company `88850`, shortname `nubank`) read the RA1000 seal for 2026-05-01 to 2026-10-31: 56,825 complaints, 56,800 answered and 14 unanswered, 25,678 ratings, `answered_percent` 100, `solved_percent` 93.2, `would_do_business_again_percent` 81.5, `consumer_score` 7.81, `final_score` 8.8, an average answer time of 341,174 seconds (about 3.9 days); over 3 years, 345,780 complaints and a final score of 8.5. Credit cards were behind 34.95 percent of its complaints, and it ranked first in the site's best credit card issuers list. Site-wide, Mercado Livre was the most complained-about company of the last 30 days (43,433), and in the Bancos Digitais segment InfinitePay led the best list at 9.7.

Seven limits shape every answer, so say them plainly:
- **1 credit per call.** Company complaints by `shortname` cost 2 (the company id is looked up first; 3 if the search misses it and the company page is read); by `company_id` 1. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **No consumer identities.** Consumer names, emails, IPs, user ids, phones and cities are never returned; only the consumer's state is. A consumer's name inside a company's greeting is replaced with `[nome]`. Complaint text is as the consumer published it.
- **Scores are the site's.** `final_score`, `consumer_score`, the percents and the seal (`status`) are Reclame Aqui's numbers for a named period with `start` and `end`. Quote the period with every number.
- **Newest first, 500 deep.** Complaints come newest first (the site has no other order), 5 or 10 per page, up to offset 500 per filter combination (page 51 at 10 per page). `total` is the exact count; narrow with `status`, `category`, `product`, `problem` or `query` to reach more.
- **Company search is short.** The site's own company search returns about 7 matches, no paging.
- **Rankings are the site's lists.** The 11 ranking lists hold 20 companies each, as the site shows them; segment rankings show 10 best and 10 worst on page 1.
- **Nothing is stored.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Reclame Aqui's own API is paid and serves a company its own complaints only. Reputation and complaints of any company are shown on reclameaqui.com.br, and this skill reads those public pages with one Scavio key.

See also: Trustpilot `trustpilot-reviews-api`; Google Maps reviews `google-maps-api`.

## When to trigger

Use this skill when the user asks to:
- Read a Brazilian company's Reclame Aqui reputation: the seal (RA1000, GREAT, GOOD, REGULAR, BAD, NOT_RECOMMENDED), final score, solved percent, answered percent, would-do-business-again percent, average answer time, for 6 months, 12 months, last year, the year before or 3 years
- Find a company on Reclame Aqui by name, with its CNPJ, segment and seal
- List a company's complaints, filtered by unanswered, answered, evaluated, resolved or not resolved, by category, product or problem, Black Friday purchases, or keywords
- Read one complaint with the company's answer, the consumer's replies, the score and the closing evaluation
- Search complaints across every company by keywords and see which companies they are about
- Read the Reclame Aqui rankings: best resolution rate, best rating, most complained about yesterday, in 7 days, 30 days or 6 months, newly registered
- Read the best and worst companies of a segment (Bancos Digitais, Marketplace, ...) or list every segment
- Compare the reputation of several companies in the same segment, each for the same period

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 1 credit, so 50 credits cover about 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 2-16 seconds (in the captures: complaints 1.8, complaint search 2.1, company 2.9, segments 3.9, complaint 5.8, segment ranking 6.3, rankings 7.0, company search 15.7). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/reclameaqui/company-search` | The site's company search (about 7 matches): id, shortname, name, seal, final score, solved percent, complaints in 6 months, CNPJ, city, state, segment, verified | 1 |
| `POST /api/v1/reclameaqui/company` | One company: reputation for 5 periods, CNPJ, plan, verified, published phones and social links, segments, main problems, segment ranking, 6 months of seal history, notice | 1 |
| `POST /api/v1/reclameaqui/complaints` | One company's complaints, newest first, by tab, category, product, problem, Black Friday and keywords, 5 or 10 per page, with the exact total and the filter ids | 1 by `company_id`, 2 by `shortname` |
| `POST /api/v1/reclameaqui/complaint` | One complaint with its whole thread: company answer, consumer replies, final evaluation, score, similar complaints | 1 |
| `POST /api/v1/reclameaqui/complaint-search` | Complaints across every company that match some words, with the companies they are about | 1 |
| `POST /api/v1/reclameaqui/rankings` | The 11 site-wide rankings of 20, or one list | 1 |
| `POST /api/v1/reclameaqui/segments` | Every ranked segment (165 under 15 main segments) | 1 |
| `POST /api/v1/reclameaqui/segment-ranking` | One segment's best and worst companies, 10 each on page 1 | 1 |

Every answer carries `site`, `host`, `country` (br) and `language` (pt-BR).

## Reputation

`/company` returns `reputation[]`, one entry per period:

| Field | Meaning |
|---|---|
| `period`, `start`, `end`, `main` | `6_months`, `12_months`, `last_year`, `year_before_last`, `3_years`, the dates the site scores, and the period the site headlines |
| `complaints`, `answered`, `unanswered`, `ratings` | Counts in the period as the site gives them |
| `answered_percent`, `solved_percent`, `would_do_business_again_percent` | The site's percents |
| `consumer_score`, `final_score` | The consumers' average rating and the site's final score (0-10) |
| `average_answer_time_seconds` | The company's average time to answer |
| `status`, `status_label` | The seal: RA1000, GREAT, GOOD, REGULAR, BAD, NOT_RECOMMENDED, NO_INDEX (too few ratings), ... |

- Quote "Nubank on Reclame Aqui: RA1000, final score 8.8, 93.2 percent solved (6 months to 2026-10-31, read 2026-11-27)", always with the period.
- `main_problems[]` `{id, name, complaints, percent}` are the site's own split; their ids work as the complaints `category` filter.
- `reputation_history[]` is the seal per month for 6 months, as the site shows it.
- Compare companies only on the same period, each with its dates. Report the site's numbers and the arithmetic only; never rate a company yourself.

## Workflow

1. **Find the company.** `/company-search` with `query` (`nubank`): take `id` and `shortname`.
2. **Reputation.** `/company` with `shortname` (or a `reclameaqui.com.br/empresa/<shortname>/` link): the 5 periods, main problems, segment ranking and seal history.
3. **Complaints.** `/complaints` with `company_id` (1 credit) or `shortname` (2), and `status` (`resolved`), `category` / `product` / `problem` ids from `filters` of a previous answer, `black_friday`, or `query` (`cartão bloqueado`).
4. **One thread.** `/complaint` with the `url` of a complaint, or `company` with `complaint_id`.
5. **Across companies.** `/complaint-search` with `query` (`iphone quebrado`): matching complaints and the companies they are about.
6. **Benchmarks.** `/rankings` (all 11, or one `list`), `/segments` for the segment shortnames, `/segment-ranking` with `main_segment` and `segment`.
7. **Watching a reputation:** poll `/company` on a schedule and store each answer with its `fetched_at`; that stored series is your history beyond the site's 6 months of seals.

## Parameters

| Endpoint | Param | Notes |
|---|---|---|
| company-search | `query` | Company name or brand, 2-100 characters |
| company | `shortname` / `url` | A shortname (`nubank`) or a `reclameaqui.com.br/empresa/<shortname>/` link; exactly one |
| complaints | `company_id` / `shortname` | Exactly one: `company_id` (`88850`, 1 credit) or `shortname` (2 credits) |
| complaints | `status` | `latest` (default, every complaint), `unanswered`, `answered` (answered, not yet evaluated), `evaluated`, `resolved`, `not_resolved` (as the consumer evaluated it) |
| complaints | `category`, `product`, `problem` | Ids from `filters.categories`, `filters.products`, `filters.problems` of an answer (`0000000000000003`) |
| complaints | `black_friday` | Only complaints the consumer marked as Black Friday purchases |
| complaints, complaint-search | `query` | Words inside the company's complaints, or across every company (required on complaint-search) |
| complaints, complaint-search | `page`, `page_size` | Page from 1 (up to offset 500 per filter combination); 5 or 10 per page (default 10) |
| complaint | `url` / `company` + `complaint_id` | A complaint link, or the company shortname with the 16-character id (`NhIy-6O6osFhQdJ-`) |
| rankings | `list` | One of `best_resolution_rate`, `would_do_business_again`, `best_rating`, `most_resolved_30_days`, `most_resolved_6_months`, `most_complained_yesterday`, `most_complained_7_days`, `most_complained_30_days`, `most_complained_6_months`, `worst`, `newly_registered`; leave out for all 11 |
| segments | (none) | `{}` |
| segment-ranking | `main_segment` + `segment` / `url` | Shortnames from segments (`bancos-e-financeiras`, `bancos-digitais`) or a `/segmentos/<main>/<segment>/` link; `page` for the next 10 best |

## Examples

### One company's reputation

`POST /api/v1/reclameaqui/company` with `{"shortname": "nubank"}` (1 credit), trimmed from the 2026-11-27 capture:

```json
{
  "id": "88850",
  "shortname": "nubank",
  "name": "Nubank",
  "cnpj": "18236120000158",
  "cnpj_validated": true,
  "plan": "PREMIUM",
  "verified": true,
  "city": "SAO PAULO",
  "state": "SP",
  "on_platform_since": "2014-12-12T10:47:00",
  "segments": { "main": { "shortname": "bancos-e-financeiras", "name": "Bancos e Financeiras" } },
  "reputation": [
    {
      "period": "6_months",
      "main": true,
      "start": "2026-05-01T00:00:00",
      "end": "2026-10-31T23:59:59",
      "complaints": 56825,
      "answered": 56800,
      "unanswered": 14,
      "ratings": 25678,
      "answered_percent": 100,
      "solved_percent": 93.2,
      "would_do_business_again_percent": 81.5,
      "consumer_score": 7.81,
      "final_score": 8.8,
      "average_answer_time_seconds": 341174,
      "status": "RA1000"
    }
  ],
  "main_problems": [
    { "id": "0000000000000003", "name": "Cartões de Crédito", "complaints": 120803, "percent": 34.95 },
    { "id": "0000000000000001", "name": "Bancos", "complaints": 57367, "percent": 16.6 }
  ],
  "segment_ranking": { "position": 1, "list": "best", "segment_name": "Melhores Emissoras e Bandeiras de Cartão de Crédito" },
  "reputation_history": [{ "month": "Mai 2026", "status": "RA1000" }, { "month": "Out 2026", "status": "RA1000" }]
}
```

### A company's resolved complaints

`POST /api/v1/reclameaqui/complaints` with `{"company_id": "88850", "status": "resolved"}` (1 credit): `total` 164495, `reachable_pages` 51.

```json
{
  "position": 1,
  "id": "NhIy-6O6osFhQdJ-",
  "title": "Quero aumentar meu limite no cartão pois o atual é insuficiente",
  "status": "resolved",
  "solved": true,
  "evaluated": true,
  "score": 10,
  "would_deal_again": true,
  "evaluation": "Atendimento rápido",
  "created": "2026-11-26T12:45:24",
  "first_answer_at": "2026-11-26T15:25:37",
  "interaction_count": 2,
  "category": { "id": "0000000000000003", "name": "Cartões de Crédito" },
  "problem": { "id": "0000000000000091", "name": "Limite" },
  "state": "PI",
  "company": { "id": "88850", "shortname": "nubank", "name": "Nubank" }
}
```

`/complaint` `{"company": "nubank", "complaint_id": "NhIy-6O6osFhQdJ-"}` returns the same complaint with `text` and `interactions[]`: the company answer (`author` company, greeting with `[nome]`) and the consumer's final evaluation, `names_masked` 1, and `similar[]` complaints.

### Rankings, segments and complaint search

- `/rankings` `{"list": "most_complained_30_days"}`: "Mais reclamadas nos ultimos 30 dias", 20 companies, Mercado Livre first (43,433, reputation Boa) and iFood second (37,397, Regular).
- `/segments` `{}`: `main_segments` 15, `count` 165, each `{main_segment, main_segment_name, segment, name, url}`.
- `/segment-ranking` `{"main_segment": "bancos-e-financeiras", "segment": "bancos-digitais"}`: best 40 companies over 4 pages, InfinitePay first (RA1000, final score 9.7, 98.1 percent solved, 12,429 complaints), CloudWalk second (9.6); worst 27, the first two SUSPENDED.
- `/complaint-search` `{"query": "iphone quebrado"}`: `total` 3774, `reachable_pages` 51, with `companies[]` the matches are about (Apple 604, Mercado Livre 174, ...).
- `/company-search` `{"query": "nubank"}`: 6 companies, Nubank (RA1000, 8.8) first, then Nubank Parque (NO_INDEX, previous name Allianz Parque).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ra(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/reclameaqui/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Find the company (1 credit), then its reputation (1 credit)
co = ra("company-search", {"query": "nubank"})["data"]["companies"][0]
rep = ra("company", {"shortname": co["shortname"]})["data"]
for p in rep["reputation"]:
    print(p["period"], p["start"][:10], p["end"][:10], p["status"], p["final_score"], p["solved_percent"])

# 2. Unanswered complaints by company id (1 credit)
open_ = ra("complaints", {"company_id": co["id"], "status": "unanswered"})["data"]
print(open_["total"], [c["title"] for c in open_["complaints"]])

# 3. The segment's best and worst (1 credit)
seg = ra("segment-ranking", {"main_segment": "bancos-e-financeiras", "segment": "bancos-digitais"})["data"]
print([(c["name"], c["final_score"]) for c in seg["best"]["companies"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `host`, `country` and `language`; complaint answers carry `note`.

- **company-search** - `query`, `count`, `companies[]` {`position`, `id`, `shortname`, `name`, `company_name`, `fantasy_name`, `url`, `reputation`, `final_score`, `solved_percent`, `complaints_6_months`, `cnpj`, `documents`, `city`, `state`, `website`, `logo`, `main_segment`, `segment`, `verified`, `previous_names`, `sub_brands`}.
- **company** - `requested`, `id`, `legacy_id`, `shortname`, `name`, `url`, `known_as`, `description`, `cnpj`, `cnpj_validated`, `plan`, `account_status`, `verified`, `website`, `logo`, `city`, `state`, `phones[]` {`number`, `country_code`}, `social_networks`, `on_platform_since`, `time_on_platform`, `page_views`, `segments` {`main`, `secondary[]`}, `reputation[]`, `main_problems[]`, `segment_ranking` {`position`, `list`, `segment_name`, `main_segment`, `segment`}, `reputation_history[]` {`month`, `status`}, `notice` {`title`, `text`}, `related_companies`.
- **complaints / complaint-search** - (`company_id`, `shortname`, `company_name`, `status`, `category`, `product`, `problem`, `black_friday`, `sort` on complaints), `query`, `page`, `page_size`, `total`, `total_pages`, `reachable_pages`, `count`, `complaints[]` {`position`, `id`, `legacy_id`, `title`, `excerpt`, `url`, `status`, `site_status`, `solved`, `evaluated`, `score`, `would_deal_again`, `evaluation`, `created`, `modified`, `first_answer_at`, `interaction_count`, `category`, `product`, `problem`, `other_product`, `other_problem`, `special`, `state`, `company` {`id`, `shortname`, `name`}, `frozen`, `in_moderation`}, `filters` {`categories`, `products`, `problems`} (complaints) or `companies[]` {`id`, `shortname`, `name`, `complaints`} (complaint-search), `note`.
- **complaint** - `requested`, `id`, `legacy_id`, `title`, `text`, `url`, `status`, `site_status`, `solved`, `evaluated`, `score`, `would_deal_again`, `created`, `category`, `problem`, `product`, `special`, `state`, `company`, `segment_ranking`, `interaction_count`, `interactions[]` {`position`, `id`, `type` (company_answer, consumer_reply, company_reply, final_evaluation), `site_type`, `author` (company or consumer), `created`, `text`}, `names_masked`, `similar[]` {`id`, `title`, `url`, `created`, `status`}, `note`.
- **rankings** - `list`, `count`, `lists[]` {`list`, `name`, `period`, `url`, `count`, `companies[]` {`position`, `name`, `shortname`, `url`, `logo`, `reputation_label`, `value`, `value_text`}}.
- **segments** - `main_segments`, `count`, `segments[]` {`main_segment`, `main_segment_name`, `segment`, `name`, `url`}.
- **segment-ranking** - `main_segment`, `segment`, `url`, `page`, `segment_name`, `main_segment_name`, `best` {`total`, `pages`, `count`, `companies[]`}, `worst` (page 1 only, else null), `note`; companies {`position`, `shortname`, `name`, `url`, `website`, `logo`, `verified`, `reputation`, `final_score`, `solved_percent`, `answered_percent`, `complaints`, `solved_complaints`, `unsolved_complaints`, `balance`}.

## Guardrails

- Name it "Reclame Aqui (reclameaqui.com.br, Brazil's company complaint and reputation site)" on first mention.
- Reputation: quote the seal, scores and percents with their period (`start`, `end`) and the `fetched_at` date, as "Reclame Aqui's score". Never present them as Scavio's rating, and never rate a company beyond the site's numbers.
- Consumers: no consumer names or contact details are returned, and none should be added. Quote a complaint by its title and as "a consumer complaint on Reclame Aqui", with its state and date only. Never try to identify a consumer from complaint text.
- Complaint text is as the consumer published it, a claim by one party; the company's answer is part of the thread. Present both when quoting a complaint, and do not state a complaint's claims as fact.
- Company data: CNPJ, published phones, website and social links are the company's public business data as the site shows it.
- Images and copy: do not republish the site's logos or page copy; link companies by `shortname` and complaints by `id`.
- Not available: consumer identities, complaints past offset 500 per filter combination, any order but newest first, filing or answering complaints, company account data.
- Terms: Scavio does not store Reclame Aqui data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Reclame Aqui's terms of use restrict automated access to its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate scores, counts, seals, complaints, rankings or dates. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "query must be at least 2 characters."; "Send exactly one of shortname or url."; "Send exactly one of company_id or shortname."; "Send url, or company (shortname) with complaint_id."; "<field> must be a 16-character Reclame Aqui complaint id (e.g. NhIy-6O6osFhQdJ-)."; "<field> must be an id from the filters of a complaints answer (e.g. 0000000000000003)."; "page_size must be 5 or 10 (the two sizes Reclame Aqui serves)."; "page <n> is past the last page Reclame Aqui serves for one filter combination (page 51 at 10 per page). Narrow with status, category, product, problem or query to reach more."; "status must be one of: ..."; "list must be one of: ..."; "Send main_segment and segment (both from the segments endpoint), or a segment url.".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: an unknown company shortname, complaint or segment.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api).
- `502` and `503` mean Reclame Aqui data was temporarily unavailable ("Reclame Aqui is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.reclameaqui.companySearch({ query: "nubank" });
const { data: company } = await scavio.reclameaqui.company({ shortname: "nubank" });
const { data: list } = await scavio.reclameaqui.complaints({ company_id: "88850", status: "resolved" });
const { data: thread } = await scavio.reclameaqui.complaint({ company: "nubank", complaint_id: "NhIy-6O6osFhQdJ-" });
const { data: matches } = await scavio.reclameaqui.complaintSearch({ query: "iphone quebrado" });
const { data: rankings } = await scavio.reclameaqui.rankings({ list: "most_complained_30_days" });
const { data: segments } = await scavio.reclameaqui.segments({});
const { data: segment } = await scavio.reclameaqui.segmentRanking({ main_segment: "bancos-e-financeiras", segment: "bancos-digitais" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.reclameaqui.company_search(...)`, `company`, `complaints`, `complaint`, `complaint_search`, `rankings`, `segments` and `segment_ranking`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_reclameaqui_companies`, `get_reclameaqui_company`, `get_reclameaqui_complaints`, `get_reclameaqui_complaint`, `search_reclameaqui_complaints`, `get_reclameaqui_rankings`, `get_reclameaqui_segments` and `get_reclameaqui_segment_ranking`. Reclame Aqui is opt-in: add `reclameaqui` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,reclameaqui"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [company search](https://scavio.dev/docs/reclameaqui-company-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api), [company](https://scavio.dev/docs/reclameaqui-company?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api), [complaints](https://scavio.dev/docs/reclameaqui-complaints?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api), [complaint](https://scavio.dev/docs/reclameaqui-complaint?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api), [complaint search](https://scavio.dev/docs/reclameaqui-complaint-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api), [rankings](https://scavio.dev/docs/reclameaqui-rankings?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api), [segments](https://scavio.dev/docs/reclameaqui-segments?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api) and [segment ranking](https://scavio.dev/docs/reclameaqui-segment-ranking?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api). The platform page is [scavio.dev/reclameaqui-api](https://scavio.dev/reclameaqui-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=reclame-aqui-api).
