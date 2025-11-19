import threading
import uvicorn
from core.agent_builder import build_agent
from tools.memory import init_db
from api.app import app as fastapi_app

def run_console(agent):
    init_db()
    print("\n🤖 ARES Avviato — Chat console")
    print("Scrivi 'exit' per uscire.\n")
    while True:
        try:
            q = input("Tu: ")
            if q.lower() == "exit":
                print("Chiusura agente...")
                break
            print("ARES:", agent.run(q))
        except KeyboardInterrupt:
            print("\nChiusura agente...")
            break

def run_api():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    agent = build_agent()
    # Avvia FastAPI in thread separato (daemon)
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    # Avvia console interattiva
    run_console(agent)
