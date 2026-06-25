"""
# @ Author: Abdallah - Copyright © 2026 Abdallah
# @ Creation Date: 2026-06-24 22:47:36 CT
# @ Last Modification Date: 2026-06-24 23:32:41 CT
# @ Modified by: Abdallah
# @ Description:
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

init_db()

app = FastAPI(title="Chat App")

app.add_middleware(
    CORSMiddleware,
    allow_origin=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/")


def root():
    return {"status": "ok"}
