import requests
import json
import os
import argparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into os.getenv()

# ── Argument Parser (for agentic/CLI invocation) ──────────────────────────────
parser = argparse.ArgumentParser(description="Fetch jobs from Adzuna API")
parser.add_argument("--keyword", type=str, default="developer", help="Job search keyword")
parser.add_argument("--country", type=str, default="gb", help="Country code (e.g. gb, us, in)")
parser.add_argument("--max-pages", type=int, default=3, help="Number of pages to fetch")
parser.add_argument("--results-pp", type=int, default=10, help="Results per page (max 50)")
parser.add_argument("--output", type=str, default="jobs-fetched.json", help="Output JSON file path")
args = parser.parse_args()

# ── Config ────────────────────────────────────────────────────────────────────
APP_ID = os.getenv("ADZUNA_APP_ID", "YOUR_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY", "YOUR_APP_KEY")

COUNTRY = args.country
KEYWORD = args.keyword
MAX_PAGES = args.max_pages
RESULTS_PP = args.results_pp
OUTPUT = args.output

BASE_URL = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search"
# ─────────────────────────────────────────────────────────────────────────────

def fetch_page(page: int) -> dict:
    url = f"{BASE_URL}/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": KEYWORD,
        "results_per_page": RESULTS_PP,
        "content-type": "application/json",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()

def fetch_all_jobs() -> list[dict]:
    all_jobs = []
    print(f"🔍 Searching Adzuna for: '{KEYWORD}' ({COUNTRY.upper()})")

    for page in range(1, MAX_PAGES + 1):
        print(f" Fetching page {page}/{MAX_PAGES}...", end=" ")
        try:
            data = fetch_page(page)
        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
            break
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break

        results = data.get("results", [])
        if not results:
            print("no more results.")
            break

        all_jobs.extend(results)
        print(f"got {len(results)} jobs (total: {len(all_jobs)})")

        total_available = data.get("count", 0)
        if len(all_jobs) >= total_available:
            print(f" All {total_available} available result(s) fetched.")
            break

    return all_jobs

def save_jobs(jobs: list[dict]) -> None:
    output = {
        "meta": {
            "keyword": KEYWORD,
            "country": COUNTRY,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "total_jobs": len(jobs),
        },
        "jobs": jobs,
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved {len(jobs)} job(s) to '{OUTPUT}'")

def main():
    if APP_ID == "YOUR_APP_ID" or APP_KEY == "YOUR_APP_KEY":
        print("⚠️ ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables are not set.")
        return

    jobs = fetch_all_jobs()
    if jobs:
        save_jobs(jobs)
    else:
        print("\n⚠️ No jobs found. The output file was not created.")

if __name__ == "__main__":
    main()
