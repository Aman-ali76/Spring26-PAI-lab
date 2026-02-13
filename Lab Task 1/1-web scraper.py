import re
import requests

EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def extract_emails_from_url(url: str) -> set[str]:
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        html = response.text
        return set(EMAIL_REGEX.findall(html))

    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return set()


if __name__ == "__main__":
    target_url = input("Enter URL: ").strip()
    emails = extract_emails_from_url(target_url)

    if emails:
        print("\nFound emails 📧")
        for email in sorted(emails):
            print("-", email)
    else:
        print("\nNo emails found ❌")
