import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class NewsScraper:
    """
    Estrattore di titoli da Google News (ricerca).
    """

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        url = f"https://news.google.com/search?q={requests.utils.quote(query)}&hl=it&gl=IT&ceid=IT:it"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as exc:
            return [{"title": "Errore nel download", "link": str(exc)}]

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = []
        for a in soup.select("a.DY5T1d")[: limit]:
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href:
                link = href
                if link.startswith("./"):
                    link = "https://news.google.com/" + link[2:]
                articles.append({"title": title, "link": link})
        return articles
