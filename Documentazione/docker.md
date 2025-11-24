# Docker / Docker Compose (ARES)

## Prerequisiti
- Docker Engine installato.
- Plugin Compose incluso (`docker compose version` deve restituire la versione).

## Build e avvio
Esegui dalla root del progetto:
```bash
docker compose up -d --build
```
Espone l'API su `http://127.0.0.1:8000` (usata dalla UI Angular).

## Volumi montati
- `./data:/app/data` — contiene `commands.db` (comandi e siti), memory, config. Serve per mantenere i dati tra i riavvii.
- `./persist:/app/persist` — spazio extra (se non esiste, viene creato).
- `/home/federico/projects:/data/projects:ro` — mount di sola lettura per i progetti host. Cambia il percorso se usi una directory diversa.

## Variabili d'ambiente
- `OLLAMA_URL=http://host.docker.internal:11434` — URL dell'istanza Ollama host (su Docker Desktop/WSL usa `host.docker.internal`).

## Comandi utili
- Stop: `docker compose down`
- Log API: `docker compose logs -f ares-api`
- Rebuild forzato: `docker compose up -d --build`
- Restart servizio API: `docker compose restart ares-api`

## Troubleshooting rapido
- Lista siti vuota nella UI → verifica che l'API risponda (`curl 127.0.0.1:8000/health`) e che il volume `./data` sia montato (Compose lo fa di default).
- `host.docker.internal` non risolto su Linux legacy → esporta l'IP host manualmente in `OLLAMA_URL` (es. `http://172.17.0.1:11434`).
