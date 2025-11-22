import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class NewsScraper:
    """
    Estrattore molto semplice di titoli da una pagina di news.
    Per siti diversi potrebbe essere necessario adattare il selettore CSS.
    """

    def fetch(self, url: str, limit: int = 5) -> List[Dict[str, str]]:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as exc:
            return [{"title": "Errore nel download", "link": str(exc)}]

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = []
        for a in soup.select("a")[: limit * 3]:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                articles.append({"title": title, "link": href})
            if len(articles) >= limit:
                break
        return articles
