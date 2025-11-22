class TelegramService:
    """
    Piccolo wrapper per notifiche Telegram.
    """

    def __init__(self, bot_token: str = ""):
        self.bot_token = bot_token

    def is_configured(self) -> bool:
        return bool(self.bot_token)
