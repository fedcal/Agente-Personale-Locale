# Ares Agent

Creazione di un agente AI personale che lavora in locale sul proprio pc. Il progetto nasce dall'esigenza di ridurre
i costi delle api di Claude o di altri sistemi, sfruttando Ollama e LLM locali gratuti.

(Area in fase di sviluppo)

## Comandi utili

**Creazione Venv**: 

- Linux/mac: ```python3 -m venv venv```
- Windows: ```python -m venv venv```

**Attivazione Venv**:

- Linux: ```source venv/bin/activate```
- Windows: ```venv\Scripts\activate```

**Modelli ollama**

- ollama pull qwen2.5-coder 
- ollama pull llama3.1 
- ollama pull nomic-embed-text

# Architettura generale dell'agente

## 1️⃣ Core Agent
Modulo principale che coordina tutti i sottosistemi, gestisce i comandi, le richieste dei servizi e le pipeline AI.

## 2️⃣ File Manager
Gestione e ricerca dei file locali con funzionalità avanzate:

- **Scansione ricorsiva** delle cartelle principali (`Documents`, `Desktop`, `Downloads`).
- **Indicizzazione dei metadati**: dimensione, tipo, data di creazione/modifica.
- **Funzioni avanzate**:
  - Ricerca intelligente per nome, contenuto (PDF/Docx) e tag.
  - Apertura o esecuzione file direttamente da Python.
  - Organizzazione automatica (es. PDF in `/PDF`, immagini in `/Images`).
- **Tecnologie**: `os`, `pathlib`, `shutil`, `PyPDF2`, `python-docx`.

## 3️⃣ Voice Interface
Gestione input/output vocale:

- **Speech-to-Text (STT)**: Whisper, Vosk, OpenAI Whisper API.
- **Text-to-Speech (TTS)**: pyttsx3, gTTS, TTS di Coqui.
- **Pipeline**: microfono → STT → agente → risposta → TTS → speaker.
- **Extra**: hotword detection tipo “Hey Jarvis” con Snowboy o Porcupine.

## 4️⃣ Coding Assistant
Assistente per lo sviluppo e debugging del codice:

- Apertura editor integrati (`VSCode`, `PyCharm` via plugin, o CLI).
- Suggerimenti su richiesta e completamento automatico.
- Funzionalità:
  - Analisi snippet di codice.
  - Debug degli errori.
  - Generazione di boilerplate.
- Possibile integrazione con modelli Ollama locali addestrati su Python/Java/JS.

## 5️⃣ Integrazione Gmail
Gestione della posta elettronica tramite Gmail API:

- Lettura email importanti.
- Invio email programmatico.
- Notifiche in tempo reale (webhook o polling).
- Autenticazione sicura via OAuth2.

## 6️⃣ Integrazione WhatsApp
Invio e ricezione messaggi:

- **Opzioni**:
  - Twilio API for WhatsApp.
  - Automazione con WhatsApp Web (`pywhatkit`, `selenium`) per uso locale.
- Possibile combinazione con agenti LLM per risposte automatiche.

## 7️⃣ Telegram Integration
Bot Telegram per interazioni testuali o vocali:

- Ricezione messaggi e comandi personalizzati.
- Integrazione con `agent_core` per eseguire task o rispondere tramite LLM.
- Notifiche push e alert da agent.

## 8️⃣ News & Web Scraping
Estrazione e gestione notizie da siti web:

- Librerie: `requests`, `BeautifulSoup4`, `newspaper3k`.
- Funzioni:
  - Titoli e link recenti.
  - Riassunto e analisi trend.
- Possibile invio notizie a Telegram o Gmail.

## 9️⃣ Memory & Context
Gestione delle memorie a breve e lungo termine:

- Salvataggio cronologia conversazioni in SQLite o MySQL.
- **Breve termine**: sessione corrente.
- **Lungo termine**: informazioni personali, file recenti, abitudini.
- Possibile integrazione con LangChain per gestione intelligente del contesto.

## 🔟 Pipeline LLM
Flusso di elaborazione AI:

- Input vocale o testuale → preprocessing → Ollama → postprocessing → output (testo o voce).
- Multi-modello:
  - `chat`: conversazione naturale.
  - `coding`: completamento codice.
  - `file`: ricerca e gestione file.
  - `news`: riassunto e analisi notizie.

## 1️⃣1️⃣ Scheduler & Task Manager
- Esecuzione di task pianificati (backup, report, scraping, notizie).
- Libreria consigliata: `APScheduler`.

## 1️⃣2️⃣ System Monitor
- Monitoraggio CPU, RAM, spazio su disco.
- Notifiche e alert su anomalie.
- Libreria: `psutil`.

## 1️⃣3️⃣ Plugin & Security
- **Plugin Manager**: caricamento moduli esterni senza modificare core.
- **Security Service**: gestione sicura di credenziali e cifratura dei dati sensibili.

## 1️⃣4️⃣ Notifications & Alerts
- Notifiche desktop, Telegram o Gmail.
- Alert su mail, file o task completati.
- Libreria consigliata: `plyer` per desktop, API per messaggistica.

## 1️⃣5️⃣ Notion Integration
- Interazione con Notion API per note, task e database.
- Librerie: `notion-client`, `notion-py`.

## 1️⃣6️⃣ Tecnologie consigliate
- **Python**: core logic.
- **Ollama**: LLM locali.
- **LangChain**: gestione agenti e memoria.
- **SQLite/MySQL**: storage locale.
- **pyttsx3 / TTS / Whisper**: voice.
- **PyPDF2 / python-docx**: gestione documenti.
- **Gmail API / Twilio / pywhatkit / Telegram API**: messaggistica.
- **Watchdog**: monitoraggio cartelle in tempo reale.
- **FastAPI / Flask**: interfaccia web locale.
- **psutil**: monitoraggio sistema.


```text
agent/
├─ main.py                  # Entry point dell'agente
├─ agent_core.py            # Logica centrale: dispatcher comandi e task

├─ services/                # Moduli principali dei servizi
│   ├─ file_manager.py      # Gestione file locali e ricerca intelligente
│   ├─ voice_service.py     # STT e TTS
│   ├─ gmail_service.py     # Gmail API
│   ├─ whatsapp_service.py  # WhatsApp API
│   ├─ telegram_service.py  # Telegram bot
│   ├─ news_scraper.py      # Web scraping notizie
│   ├─ ollama_service.py    # LLM backend (chat, coding, file)
│   ├─ memory_service.py    # Memoria breve/lunga termine
│   ├─ scheduler_service.py # Esecuzione task pianificati
│   ├─ web_service.py       # Interfaccia web locale (Flask/FastAPI)
│   ├─ system_service.py    # Monitoraggio risorse e processi
│   ├─ plugin_manager.py    # Gestione plugin esterni
│   ├─ security_service.py  # Gestione credenziali e cifratura
│   ├─ notification_service.py # Notifiche desktop/Telegram/Gmail
│   └─ notion_service.py    # Interazione con Notion API

├─ utils/                   # Utility condivise tra i moduli
│   ├─ logger.py            # Logging coerente
│   ├─ file_utils.py        # Utility file generiche
│   └─ config_manager.py    # Gestione centralizzata configurazioni

└─ data/                    # Dati e configurazioni
    ├─ memory.db            # SQLite memorie e cronologia
    └─ config.json          # Config generali e API keys

