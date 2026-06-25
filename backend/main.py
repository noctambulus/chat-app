from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title= "Chat App")

app.add_middleware(
    CORSMiddleware,
    allow_origin = ["http://localhost:5173"], #Vite dev server
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.get("/")
def root():
    return {"status": "ok"}