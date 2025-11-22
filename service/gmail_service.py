class GmailService:
    """
    Gestione basica placeholder per Gmail.
    """

    def __init__(self, credentials_path: str = "data/credentials.json"):
        self.credentials_path = credentials_path

    def is_configured(self) -> bool:
        return False

    def send_mail(self, to: str, subject: str, body: str) -> bool:
        return False
