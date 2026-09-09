# GitHub API - Profiles, Repos, Issues, Search, Email Finder

Pull GitHub profiles, repositories, READMEs, releases, issues and comments, run GitHub search across five verticals, and get composite intelligence: a full repo dossier, a user's public-activity velocity, reaction-ranked top issues, and public commit emails. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Look up a GitHub user's profile, or a repository's stars, forks, issues, license, topics and metadata
- List a user's repositories, or a repository's releases with assets and download counts
- Read a repository's README, its issues (PRs filtered out by default), or a single issue / PR and its comments
- Search repositories, users, issues, code or commits
- Rank a repository's most-reacted open issues, or build a full repo dossier (metadata, README excerpt, releases, top issues, language breakdown, top contributors, weekly activity)
- Measure a user's public-activity velocity, or resolve a username to public commit email(s)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=github-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=github-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most endpoints cost **1 credit**; the composite/intelligence endpoints cost more (see the table).

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/github/profile` | 1 | A user's public profile |
| `POST /api/v1/github/repo` | 1 | A repository's stars, forks, issues, license, topics and metadata |
| `POST /api/v1/github/profile/repos` | 1 | A user's repositories, paginated and sortable |
| `POST /api/v1/github/repo/readme` | 1 | A repository's README as decoded markdown |
| `POST /api/v1/github/repo/releases` | 1 | A repository's releases with assets and download counts |
| `POST /api/v1/github/repo/issues` | 1 | A repository's issues (PRs filtered out by default) |
| `POST /api/v1/github/issue` | 1 | A single issue or pull request |
| `POST /api/v1/github/issue/comments` | 1 | The comments on an issue or PR |
| `POST /api/v1/github/search` | 1 | Search repositories, users, issues, code or commits |
| `POST /api/v1/github/repo/top-issues` | 5 | A repository's most-reacted open issues (reaction-ranked) |
| `POST /api/v1/github/user/email` | 2 | Resolve a username to public commit email(s); flags `@users.noreply.github.com` |
| `POST /api/v1/github/repo/dossier` | 5 | Composite repo profile: metadata, README excerpt, latest releases, top issues, language breakdown, top contributors, weekly activity |
| `POST /api/v1/github/user/profile-velocity` | 10 | A user's public-activity velocity: event counts, active days, events/week and most-active repo over the last 90 days |

## Parameters

`handle` = username, `@handle`, or a `github.com/<user>` URL. `url` = a `github.com/<owner>/<repo>` URL or a bare `<owner>/<repo>`. `per_page` = 1-100, `page` = 1-based.

| Endpoint | Fields |
|---|---|
| `profile`, `user/email`, `profile-velocity` | `handle` (required). `profile-velocity` also takes `depth`: `quick` (1 page of events), `default`/`deep` (up to 3; the public feed is capped at 300 events / 90 days) |
| `repo`, `repo/readme`, `repo/dossier` | `url` (required) |
| `profile/repos` | `handle` (required); `type` (`all`/`owner`/`member`), `sort` (`created`/`updated`/`pushed`/`full_name`, default `updated`), `direction` (`asc`/`desc`), `per_page`, `page` |
| `repo/releases` | `url` (required); `per_page`, `page` |
| `repo/issues` | `url` (required); `type` (`issue`/`pr`/`all`), `state` (`open`/`closed`/`all`, default `open`), `labels` (comma-separated), `sort`, `direction`, `since` (ISO8601), `per_page`, `page` |
| `issue` | `url` (required) - an issue/PR URL (`.../issues/<n>` or `.../pull/<n>`) or `<owner>/<repo>#<n>` |
| `issue/comments` | `url` (required, same forms as `issue`); `since` (ISO8601), `per_page`, `page` |
| `search` | `query` (required); `type` (`repositories`/`users`/`issues`/`code`/`commits`, default `repositories`), `sort`, `order` (`asc`/`desc`), `per_page`, `page` |
| `repo/top-issues` | `url` (required); `sort` (`reactions` default, or `comments`), `per_page` (default 10) |

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. A repo's core metadata (1 credit)
repo = requests.post(f"{BASE}/api/v1/github/repo", headers=HEADERS,
    json={"url": "facebook/react"}).json()

# 2. Its most-reacted open issues (5 credits)
top = requests.post(f"{BASE}/api/v1/github/repo/top-issues", headers=HEADERS,
    json={"url": "facebook/react", "sort": "reactions", "per_page": 10}).json()

# 3. Search the top ML repositories by stars (1 credit)
search = requests.post(f"{BASE}/api/v1/github/search", headers=HEADERS,
    json={"query": "machine learning", "type": "repositories",
          "sort": "stars", "order": "desc", "per_page": 20}).json()

# 4. A full repo dossier (5 credits) and a user's 90-day velocity (10 credits)
dossier = requests.post(f"{BASE}/api/v1/github/repo/dossier", headers=HEADERS,
    json={"url": "facebook/react"}).json()
velocity = requests.post(f"{BASE}/api/v1/github/user/profile-velocity", headers=HEADERS,
    json={"handle": "torvalds", "depth": "default"}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/github/profile \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handle":"torvalds"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. Paginated endpoints put their rows in `data.items`; `search` also returns the vertical's total. `credits_used` on each response tells you exactly what the call cost.

## Guardrails

- Costs are **not uniform**: `profile-velocity` is 10 credits, `top-issues` and `dossier` are 5, `user/email` is 2, everything else is 1. Check the table before a loop.
- A `400` (bad input), `404` (unknown user/repo/issue) and `429` (upstream rate limit) all cost nothing - only a fully-served `200` is billed.
- `repo/issues` filters pull requests out by default; pass `type: "all"` or `type: "pr"` to include them.
- `profile-velocity` and the public feed it reads are capped at 300 events / 90 days - it is a recent-activity signal, not a full history.
- `user/email` is public-commit OSINT and flags `@users.noreply.github.com` addresses. It is personal data - use it responsibly and do not build profiles of individuals.
- Never fabricate stars, issue text, contributor names or emails. Only return what the API returned.

## Failure handling

- `400` means an invalid or missing parameter. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the user, repo or issue does not exist.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=github-api).
- `502` means the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
