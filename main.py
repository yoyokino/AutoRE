from fastapi import FastAPI
from routers import workflow

app = FastAPI(
    title="Actor API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.include_router(workflow.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)