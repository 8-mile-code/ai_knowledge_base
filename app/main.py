from fastapi import FastAPI

from app.api.routers import documents, search

app = FastAPI(title="AI Knowledge Base API")


app.include_router(documents.router)
app.include_router(search.router)


@app.get("/")
async def health_check():
    return {"status": "ok"}
