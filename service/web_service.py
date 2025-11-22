from fastapi import FastAPI


def build_web_service():
    app = FastAPI(title="ARES Web Service")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
