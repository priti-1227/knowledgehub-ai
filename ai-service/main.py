from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.document import router as document_router

app = FastAPI(
    title="KnowledgeHub AI Service",
    description="Microservice for Document Processing and RAG Pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(document_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Welcome to KnowledgeHub AI Microservice",
        "data": {}
    }