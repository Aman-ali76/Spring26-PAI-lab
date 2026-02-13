import re
import pandas as pd
import requests

EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

INPUT_CSV = "input_websites.csv"
OUTPUT_CSV = "output_emails.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def extract_emails(url: str) -> list[str]:
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        html = response.text
        return list(set(EMAIL_REGEX.findall(html)))

    except requests.RequestException as e:
        print(f"❌ Failed: {url} → {e}")
        return []


def main():
    # Read input CSV
    df = pd.read_csv(INPUT_CSV)
    websites = df.iloc[:, 0].dropna().astype(str)

    results = []

    for website in websites:
        website = website.strip()
        if not website:
            continue

        print(f"🔍 Scraping: {website}")
        emails = extract_emails(website)

        if emails:
            for email in emails:
                results.append({
                    "website": website,
                    "email": email
                })
        else:
            results.append({
                "website": website,
                "email": ""
            })

    # Save output CSV
    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n✅ Done! Saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
