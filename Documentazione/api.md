# API Reference (ARES Agent)

Base URL: `http://127.0.0.1:8000`

## Health
- `GET /health` → `{ "status": "ok" }`

## Modelli
- `GET /models` → `string[]`  
  Elenco modelli disponibili (da Ollama o config).

## Chat
- `POST /chat`  
  Body:
  ```json
  {
    "message": "testo utente",
    "model": "llama3.1",     // opzionale
    "temperature": 0.7       // opzionale
  }
  ```
  Response:
  ```json
  {
    "response": "risposta del modello",
    "model": "llama3.1"
  }
  ```

## Ricerca file
- `POST /search/files`  
  Body:
  ```json
  { "query": "nome-parziale" }
  ```
  Response: array di:
  ```json
  {
    "name": "file.txt",
    "path": "/percorso/assoluto/file.txt",
    "size": 1234,
    "modified": 1710000000.0
  }
  ```

## RAG (ricerca semantica)
- `POST /search/rag`  
  Body:
  ```json
  { "query": "domanda" }
  ```
  Response:
  ```json
  { "answer": "testo sintetico basato su Chroma" }
  ```
  Nota: richiede indice Chroma; se disabilitato restituisce fallback stringa.

## Memoria
- `GET /memory` → `{ "history": [ { "role": "user|assistant", "text": "..." } ] }`
- `DELETE /memory` → `{ "ok": true }`

## Sistema
- `GET /system` →  
  ```json
  {
    "platform": "...",
    "cpu_percent": 12.3,
    "memory": { "total": ..., "available": ..., "percent": ... },
    "disk": { "total": ..., "used": ..., "free": ... }
  }
  ```

## Note
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- Le richieste accettano JSON; le risposte sono JSON. Nessuna autenticazione prevista in locale.
