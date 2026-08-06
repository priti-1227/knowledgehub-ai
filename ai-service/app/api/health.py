from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    return {
        "success": True,
        "message": "KnowledgeHub AI Service is healthy and active",
        "data": {
            "status": "ok",
            "service": "ai-service"
        }
    }