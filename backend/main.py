"""
# @ Author: Abdallah - Copyright © 2026 Abdallah
# @ Creation Date: 2026-06-24 22:47:36 CT
# @ Last Modification Date: 2026-07-13 CT
# @ Modified by: Abdallah
# @ Description:
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers.users import router as auth_router
import os

init_db()

app = FastAPI(title="Chat App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok"}
