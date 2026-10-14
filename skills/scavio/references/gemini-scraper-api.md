# Gemini Scraper API - Answers, Citations, AI Visibility

Send a prompt to Google Gemini and get back the answer it gives: the full answer as Markdown, the URLs it cites, and the products it recommended. The response has the same shape as the ChatGPT endpoint, so one parser tracks both assistants. 5 credits per answered prompt; failed prompts are free.

## When to trigger

Use this skill when the user asks to:
- See what Gemini says or recommends for a question, product category or brand
- Check whether a brand, product or website is mentioned or cited in Gemini's answer
- Find which sites Gemini cites for a topic
- Track AI visibility or share of voice in Gemini across a list of prompts
- Compare Gemini's answer with ChatGPT's (use the `chatgpt-scraper-api` skill for the other half)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=gemini-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=gemini-scraper-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits, enough for 10 prompts on this endpoint.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

## Endpoint

```
POST https://api.scavio.dev/api/v1/gemini/prompt
Authorization: Bearer $SCAVIO_API_KEY
```

Every answered prompt costs 5 credits. Answers typically take 10-40 seconds: use an HTTP timeout of at least 90 seconds.

## Workflow

1. Send the question the way a buyer would type it as `prompt`.
2. Read `data.answer.markdown` for the answer, `data.sources[]` for the URLs it cited and `data.shopping[]` for the products it recommended.
3. For visibility tracking, run each prompt several times: answers vary between runs, so report a mention rate, not a single yes or no.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | string | required | The prompt, 1-4000 characters |

## Example

```python
import requests

# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"

response = requests.post(
    "https://api.scavio.dev/api/v1/gemini/prompt",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"prompt": "What are the best running shoes for beginners?"},
    timeout=120,
)
data = response.json()["data"]
print(data["answer"]["markdown"][:800])
print("cited:", [s["url"] for s in data["sources"]])
print("recommended:", [p["title"] for p in data["shopping"]])
```

## Response

```json
{
  "data": {
    "platform": "gemini",
    "prompt": "What are the best running shoes for beginners?",
    "model": null,
    "answer": {
      "markdown": "Choosing your first running shoe is an important step. The best beginner running shoes focus on **balanced cushioning**... The Brooks Ghost 18 is a **fan-favorite daily trainer**..."
    },
    "sources": [
      { "url": "https://www.runnersworld.com/gear/a19663621/best-running-shoes/", "title": null, "snippet": null, "source": null, "published_at": null }
    ],
    "search_queries": [],
    "shopping": [
      { "title": "Brooks Men's Ghost 18", "url": null, "price": null, "image_url": null, "merchant": null }
    ]
  },
  "response_time": 36631,
  "credits_used": 5,
  "credits_remaining": 45
}
```

Gemini returns cited URLs only, so `title`, `snippet`, `source` and `published_at` are null, and `search_queries` is always empty. A comparison grid in the answer comes back as a Markdown table inside `answer.markdown`.

## Guardrails

- Each answered prompt costs 5 credits. Confirm before running large prompt lists.
- Never fabricate or paraphrase the answer as if it were Gemini's words. Quote `answer.markdown` and surface `sources` so the user can verify.
- Answers vary between runs and are never cached. Do not present one run as Gemini's fixed opinion.
- Prompts are limited to 4000 characters.

## Failure handling

- `400` means a missing or too-long prompt - fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=gemini-scraper-api).
- `502` means Gemini did not return an answer. Retry once; it is not charged.
- `503` means answer capacity is busy. Wait for the `Retry-After` header, then retry; it is not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
