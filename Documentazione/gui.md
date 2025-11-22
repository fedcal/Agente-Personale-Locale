# Uso da interfaccia grafica (Angular UI)

L’app Angular fornisce una chat web con selezione modello e gestione cronologia.

## Avvio
```bash
# server Python (API)
source venv/bin/activate
python main.py

# frontend
cd angular_ui
npm install
npm start
```
Apri il browser su `http://localhost:4200`.

## Funzioni disponibili
- Chat: invia messaggi e ricevi risposte dal modello selezionato.
- Selezione modello: elenco recuperato da `GET /models`.
- Cancella cronologia: pulisce la history locale (chiama `DELETE /memory`).
- Sidebar/Model selector: cambio rapido del modello attivo.

## Endpoint coinvolti
- `GET /models`
- `POST /chat`
- `GET /memory` / `DELETE /memory`

## Futuri sviluppi (UI)
- Upload file/PDF per contesto RAG e sintesi.
- Visualizzazione risultati `/files` e `/system` con pannelli dedicati.
- Stato modello (caricamento, token progress) e retry automatico.
- Temi aggiuntivi e layout mobile migliorato.
- Pannello scheduler/notifiche (Telegram, email) quando i servizi saranno abilitati.
