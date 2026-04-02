from fastapi import APIRouter

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/")
async def get_documents():
    return {"documents": []}
