from fastapi import FastAPI

from src.api.routes import router


def create_app() -> FastAPI:

    app = FastAPI(
        title="KnowledgeHub AI Service",

        description=(
            "AI retrieval and RAG service "
            "for KnowledgeHub."
        ),

        version="1.0.0",
    )

    app.include_router(
        router
    )

    return app


app = create_app()