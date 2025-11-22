import smtplib
from email.mime.text import MIMEText
from typing import Optional

from utils.logger import get_logger

log = get_logger(__name__)


class NotificationService:
    """
    Invia notifiche email semplici usando SMTP locale o remoto.
    """

    def __init__(self, smtp_host="localhost", smtp_port=25, username: Optional[str] = None, password: Optional[str] = None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.username or "ares@localhost"
            msg["To"] = to

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as smtp:
                if self.username and self.password:
                    smtp.starttls()
                    smtp.login(self.username, self.password)
                smtp.send_message(msg)
            log.info("Email inviata a %s", to)
            return True
        except Exception as exc:
            log.error("Errore invio email: %s", exc)
            return False
