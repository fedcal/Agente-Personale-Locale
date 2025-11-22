from typing import List, Dict


class NotionService:
    """
    Placeholder per integrazione Notion.
    Fornisce un'interfaccia minima così da non lasciare file vuoti.
    """

    def __init__(self, token: str = "", database_id: str = ""):
        self.token = token
        self.database_id = database_id

    def is_configured(self) -> bool:
        return bool(self.token and self.database_id)

    def list_items(self) -> List[Dict[str, str]]:
        if not self.is_configured():
            return []
        # In un'implementazione completa qui si userebbe notion-client.
        return []
