# Job Hunter

A personal automation pipeline that scrapes job vacancies, filters and scores them with AI, and delivers the best matches via Telegram.

## How it works

Vacancies move through three layers, each with a clear responsibility:

```
Bronze  →  raw scraped vacancies
Silver  →  rule-filtered, profile-matched, ready for AI
Gold    →  AI-scored, ranked, ready for notification
```

The candidate profile lives in `profiles.json` and drives both the Silver filtering rules and the AI scoring prompt. The current implementation covers the full Bronze layer and profile loading — Silver promotion rules and AI scoring are next.

## Project structure

| File | Responsibility |
|---|---|
| `main.py` | Pipeline entrypoint |
| `cathoScraper.py` | Catho vacancy scraper (Playwright) |
| `database.py` | MongoDB connection, collections, indexes |
| `user_profile.py` | Profile loading and prompt generation |
| `profiles.json` | Candidate profile config |
| `ai_scoring.py` | _(reserved — AI scoring)_ |
| `telegram.py` | _(reserved — Telegram delivery)_ |
| `notification.py` | _(reserved — notification tracking)_ |

## Setup

**Requirements:** Python 3.10+, a MongoDB Atlas cluster, a Playwright-compatible environment.

**Environment variables** (`.env` at project root):

```env
MONGODB_URL=your_mongodb_connection_string
MONGODB_DB=JobHunter
```

**Install:**

```bash
pip install pymongo python-dotenv playwright
playwright install
```

**Run:**

```bash
python3 main.py
```

This scrapes Catho vacancies, builds vacancy documents, and inserts them into MongoDB with duplicate URL protection.

## What's working

- Catho scraping via Playwright
- MongoDB Atlas connection via environment variables
- Vacancy insertion with duplicate URL blocking
- Profile loading from `profiles.json`
- Profile-to-prompt conversion for the AI layer

## Roadmap

- [ ] Deterministic Bronze → Silver promotion rules
- [ ] AI scoring in `ai_scoring.py`
- [ ] Persist scored vacancies to Gold
- [ ] Telegram notifications
- [ ] Scheduling and monitoring

## Notes

- `.env` is gitignored
- `profiles.json` stores candidate configuration, not application logic