# ARES Agent (locale)

Agente AI locale basato su FastAPI e interfaccia Angular. Offre chat con modelli Ollama, ricerca file, metriche di sistema e RAG di base, utilizzabile sia da console sia via UI web.

## Requisiti
- Python 3.10+ (consigliato 3.12)
- Node.js 18+ per la UI Angular
- Ollama in esecuzione con i modelli definiti in `config.py`
- Accesso ai percorsi definiti in `config.py`/`data/config.json` (opzionale)

## Setup backend (FastAPI + console)
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Effetti:
- API FastAPI su `http://127.0.0.1:8000`
- Console interattiva nel terminale corrente (comandi: testo libero; `/files <q>` ricerca file; `/system` metriche; `/rag <q>` ricerca semantica; `exit` esce).

### Variabili d'ambiente (.env)
Compila `.env` (parti da `.env.example`) per token e credenziali:
```
TELEGRAM_TOKEN=
WHATSAPP_TOKEN=
GMAIL_USER=
GMAIL_PASSWORD=
NOTION_TOKEN=
NOTION_DB_ID=
```
`utils/config_manager` carica .env e `data/config.json`; i servizi leggono i token da lì.

### Client CLI separato (via API)
Con il server avviato:
```bash
python cli_client.py
```
Dialoga con `POST /chat` e termina con `exit`.

### Swagger / OpenAPI
- UI: `http://127.0.0.1:8000/docs`
- JSON: `http://127.0.0.1:8000/openapi.json`

### Endpoint principali
- `GET /health`
- `GET /models`
- `POST /chat` — `{ "message": "...", "model": "llama3.1", "temperature": 0.7 }`
- `POST /search/files` — `{ "query": "nome" }`
- `POST /search/rag` — `{ "query": "testo" }`
- `GET /memory` / `DELETE /memory`
- `GET /system`

## Setup frontend (Angular UI)
```bash
cd angular_ui
npm install
npm start
```
L’app si connette al backend su `http://127.0.0.1:8000` e offre selezione modello, chat e pulizia cronologia.

## Comandi (CLI / Web)
| Comando | Descrizione | Parametri |
|---------|-------------|-----------|
| `/news <tema>` | Cerca e sintetizza notizie recenti sul tema indicato. | `<tema>`: testo libero (es. “tecnologia AI”). |

I comandi sono memorizzati in `data/commands.db` e accessibili via `GET /commands`.

## Struttura progetto (sintesi)
- `main.py` — avvio API e console
- `api/app.py` — FastAPI con chat, search, memoria, sistema
- `core/` — orchestratore agente
- `service/` — servizi (ollama, memoria, file, sistema, news, scheduler, notifiche)
- `rag/` — ricerca semantica con Chroma (opzionale)
- `angular_ui/` — interfaccia web
- `cli_client.py` — client da terminale che usa l’API
- `Documentazione/` — guide d’uso

## Note
- La vector memory Chroma viene disattivata se la configurazione locale non è compatibile; per abilitarla vedi `memory/memory_manager.py`.
- Configurazioni personalizzate possono essere poste in `data/config.json` (sovrascrive `config.py`).
