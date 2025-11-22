# Uso da terminale

L’agente può essere usato in due modi dal terminale: console locale (dentro `python main.py`) o client CLI separato (`cli_client.py`) che dialoga via API.

## Avvio
```bash
source venv/bin/activate
python main.py      # server FastAPI + console locale
# in altra shell (facoltativo):
python cli_client.py
```

## Comandi disponibili (console locale)
- `testo libero` — invia il messaggio al modello scelto.
- `/files <query>` — ricerca file nei percorsi consentiti.
- `/system` — mostra CPU/RAM/disk.
- `/rag <query>` — ricerca semantica (se l’indice Chroma è disponibile).
- `exit` — chiude la console locale.

## Client CLI via API (`cli_client.py`)
- Invia messaggi a `POST /chat`, termina con `exit`.
- Modello predefinito: quello di `config.py` (`models.reasoning`).

## Endpoint utili (curl)
- Chat:
```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
  -d '{"message":"ciao","model":"llama3.1","temperature":0.7}'
```
- Ricerca file:
```bash
curl -X POST http://127.0.0.1:8000/search/files -H "Content-Type: application/json" \
  -d '{"query":"README"}'
```
- Sistema:
```bash
curl http://127.0.0.1:8000/system
```
- Pulizia memoria:
```bash
curl -X DELETE http://127.0.0.1:8000/memory
```

## Futuri sviluppi (CLI)
- Comando `/schedule` per gestire task pianificati (APScheduler).
- Integrazione vocale (`tts`/`stt`) da linea di comando.
- Comando per allegare file e inviare contenuto al modello.
- Comandi per gestione plugin locali e notifiche Telegram/email.
