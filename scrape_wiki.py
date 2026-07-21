import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Gqeberha"


def scrape_location_info(url: str) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Network error: {exc}")
        return

    if response.status_code != 200:
        print(f"Unexpected status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    heading = soup.find("h1")
    location_name = heading.get_text(strip=True) if heading else "N/A"

    content_container = soup.select_one("div.mw-parser-output") or soup.select_one("div#mw-content-text")
    summary_paragraph = None

    if content_container:
        for paragraph in content_container.find_all("p"):
            text = paragraph.get_text(" ", strip=True)
            if len(text) > 50:
                summary_paragraph = text
                break

    if summary_paragraph is None:
        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(" ", strip=True)
            if len(text) > 50:
                summary_paragraph = text
                break

    if summary_paragraph is None:
        summary_paragraph = "No summary paragraph found."

    print("Location Name:", location_name)
    print("\nSummary Paragraph:")
    print(summary_paragraph)


if __name__ == "__main__":
    scrape_location_info(URL)
