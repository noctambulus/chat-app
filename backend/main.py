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
from routers.channels import router as channels_router
from routers.messages import router as messages_router
from routers.ws import router as ws_router
from routers.files import router as files_router
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
app.include_router(channels_router)
app.include_router(messages_router)
app.include_router(ws_router)
app.include_router(files_router)


@app.get("/")
def root():
    return {"status": "ok"}
