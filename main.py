import threading

import uvicorn

from api.app import app as fastapi_app
from core.agent_builder import build_agent
from core.router import CommandRouter
from utils.logger import setup_logging


def run_console(router: CommandRouter):
    print("\n🤖 ARES Avviato — Chat console")
    print("Scrivi 'exit' per uscire. Comandi rapidi: /files <q>, /system, /rag <q>\n")
    while True:
        try:
            q = input("Tu: ")
            if q.lower() == "exit":
                print("Chiusura agente...")
                break
            res = router.dispatch(q)
            print("ARES:", res)
        except KeyboardInterrupt:
            print("\nChiusura agente...")
            break


def run_api():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    setup_logging()
    agent = build_agent()
    router = CommandRouter(agent)
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    run_console(router)
