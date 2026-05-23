from fastapi import FastAPI

from app.api.routers import documents, search, ask, auth

app = FastAPI(title="AI Knowledge Base API")


app.include_router(documents.router)
app.include_router(search.router)
app.include_router(ask.router)
app.include_router(auth.router)


@app.get(
        "/",
        summary="Health check",
        tags=["🩻 Health"],
    )
async def health_check():
    return {"status": "ok"}
