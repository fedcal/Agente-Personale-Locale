"""
Client da terminale per usare l'agente via API FastAPI.

Prerequisiti: server avviato (python main.py) su http://127.0.0.1:8000
Esecuzione: python cli_client.py
"""
import json
import requests


API_URL = "http://127.0.0.1:8000/chat"


def chat_loop():
    print("Console API — digita 'exit' per uscire.")
    while True:
        try:
            text = input("Tu: ").strip()
            if text.lower() == "exit":
                break
            payload = {"message": text}
            res = requests.post(API_URL, json=payload, timeout=120)
            res.raise_for_status()
            data = res.json()
            print("ARES:", data.get("response", data))
        except KeyboardInterrupt:
            break
        except Exception as exc:
            print(f"Errore: {exc}")


if __name__ == "__main__":
    chat_loop()
