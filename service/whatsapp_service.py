from utils.config_manager import get_secret


class WhatsappService:
    """
    Placeholder per l'integrazione WhatsApp.
    """

    def __init__(self, token: str = ""):
        self.token = token or get_secret("whatsapp_token")

    def send_message(self, number: str, text: str) -> bool:
        # Qui si integrerebbe Twilio o automazione WhatsApp Web usando self.token
        return False
