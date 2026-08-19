---
name: google-news-api
description: Google News headlines as structured JSON - title, source name, publish date, link and thumbnail - searched by keyword with relevance or date sort, or browsed by topic, section, full-coverage story, publication token or kgmid. One endpoint, 1 credit per request, country and language scoped.
version: 1.0.0
tags: google-news, google-news-api, news-api, headlines, current-events, media-monitoring, brand-monitoring, pr, journalism, research, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F4F0"
    homepage: https://scavio.dev/docs/google-news?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-news-api
---

# Google News API - Headlines by Keyword, Topic, Publication

Search Google News and return structured JSON — headline, source, date, and link — for a keyword, topic, section, or publication. One credit per request.

## When to trigger

Use this skill when the user asks to:
- Find recent news or headlines on a topic
- Monitor a company, person, or keyword in the news
- Follow a Google News topic, section, or publication
- Answer a current-events question that needs fresh reporting

Always call the API for time-sensitive news — never answer from training data.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-news-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Endpoint

```
POST https://api.scavio.dev/api/v2/google/news
Authorization: Bearer $SCAVIO_API_KEY
```

Every request costs 1 credit.

## Workflow

1. **Keyword search:** pass `query`. Add `so: 1` to sort by date instead of relevance.
2. **Localize:** set `gl` (country) and `hl` (language) for regional editions.
3. **Browse structured feeds:** pass a `topic_token`, `section_token`, `story_token`, `publication_token`, or `kgmid` (returned in prior responses) to drill into a topic, section, full-coverage story, or publisher.
4. Read `news_results[]` for headlines, sources, dates, and links.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | -- | Keyword search (one of `query` or a token/`kgmid` is required) |
| `so` | number | `0` | `0` relevance, `1` date (valid with `query`/`kgmid`) |
| `topic_token` | string | -- | Browse a Google News topic |
| `section_token` | string | -- | Browse a section within a topic |
| `story_token` | string | -- | Full-coverage story |
| `publication_token` | string | -- | A specific publisher's feed |
| `kgmid` | string | -- | Knowledge Graph entity id (e.g. `/m/02_286`) |
| `hl` | string | -- | UI language, ISO 639-1 |
| `gl` | string | -- | Geo country, ISO 3166-1 alpha-2 |
| `google_domain` | string | `google.com` | Regional Google domain |

## Example

```python
import requests

# Your key from https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-news-api. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"

response = requests.post(
    "https://api.scavio.dev/api/v2/google/news",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"query": "openai", "gl": "us", "hl": "en", "so": 1},
)
data = response.json()
for n in data["news_results"]:
    print(n.get("date"), n.get("source", {}).get("name"), n.get("title"))
    print(" ", n.get("link"))
```

## Response

```json
{
  "news_results": [
    {
      "position": 1,
      "title": "Headline text",
      "source": { "name": "Example Times" },
      "link": "https://example.com/article",
      "date": "2 hours ago",
      "thumbnail": "https://..."
    }
  ],
  "response_time": 934,
  "credits_used": 1,
  "credits_remaining": 996,
  "cached": false
}
```

## Guardrails

- Each call costs 1 credit. Inform the user before paginating widely.
- Never fabricate headlines, sources, dates, or links. Only return API data.
- One of `query`, `kgmid`, or a `*_token` must be provided.
- `so` (relevance vs date) only applies to `query`/`kgmid` requests.
- Cite the source and link when summarizing news.

## Failure handling

- `400` means an invalid parameter (e.g. no query and no token) — fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-news-api.
- `502` / `503` mean upstream is temporarily unavailable. Wait a few seconds before retrying.
- If no results are returned, broaden the query or drop the date sort.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
