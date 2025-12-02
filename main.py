from fastapi import FastAPI
from app.api import auth, files,search
app=FastAPI(title="Semantic Doc Finder")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(search.router, prefix="/search", tags=["search"])
