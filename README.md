# Rental Price Tracker Per Day (FastAPI)

A simple, password-protected web app to fetch and display rental prices from a target website.

## Quickstart

1. Copy env:
   ```bash
   cp .env.example .env
   # edit .env to set APP_PASSWORD, SECRET_KEY, TARGET_URL
   ```

2. Create venv and install deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install -r requirements.txt
   ```

3. Run server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Visit:
   - Login: http://localhost:8000/login
   - Dashboard: http://localhost:8000/

## Notes
- Set `TARGET_URL` to the site you want to read prices from. If the page is highly dynamic, we may switch to Playwright.
- This app uses a simple shared password from `.env` and a signed session cookie.

## Scraping carjet.com with a proxy (optional)

If the target site blocks direct requests or requires JavaScript rendering, configure a free proxy like ScrapeOps:

1. Create a free ScrapeOps account and get an API key: https://scrapeops.io/
2. In `.env`, set:
   ```
   SCRAPER_SERVICE=scrapeops
   SCRAPER_API_KEY=your_key_here
   TARGET_URL=https://www.carjet.com/en/search?pickup=...&dropoff=...&pickupDate=...&dropoffDate=...
   ```
3. Start the server and fetch. The backend will route via `https://proxy.scrapeops.io/v1/` with `render_js=true`.

Limitations:
- Respect the website's Terms of Service and robots.txt. Use scraping responsibly.
- Sites may use anti-bot protections that require additional techniques (rotating proxies, headless browsers). If needed, we can integrate Playwright.
