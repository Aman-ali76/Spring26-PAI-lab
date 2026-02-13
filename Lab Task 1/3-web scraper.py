import re
import pandas as pd
import requests
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

OUTPUT_FILE = "scraped_emails.csv"


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


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    output_file = None

    if request.method == "POST":
        urls = []

        # Single URL input
        single_url = request.form.get("url")
        if single_url:
            urls.append(single_url.strip())

        # CSV upload (saved in root directory)
        file = request.files.get("file")
        if file and file.filename.endswith(".csv"):
            filename = secure_filename(file.filename)
            file.save(filename)

            df = pd.read_csv(filename)
            urls.extend(df.iloc[:, 0].dropna().astype(str).tolist())

        for url in urls:
            print(f"🔍 Scraping: {url}")
            emails = extract_emails(url)

            if emails:
                for email in emails:
                    results.append({
                        "website": url,
                        "email": email
                    })
            else:
                results.append({
                    "website": url,
                    "email": ""
                })

        # Save output CSV in root directory
        if results:
            out_df = pd.DataFrame(results)
            out_df.to_csv(OUTPUT_FILE, index=False)
            output_file = OUTPUT_FILE

    return render_template(
        "index.html",
        results=results,
        output_file=output_file
    )


@app.route("/download")
def download():
    return send_file(OUTPUT_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
