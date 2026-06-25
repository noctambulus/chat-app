# Chat App

Real-time chat application with DMs and group channels.

**Stack:** FastAPI · React · WebSockets · SQLite

## Project status

| Phase | Feature | Status |
| --- | --- | --- |
| 1 | Project setup & structure | Done |
| 2 | Auth (JWT) | In progress |
| 3 | Channels & DMs | Pending |
| 4 | Real-time messaging | Pending |
| 5 | File sharing | Pending |

## Getting started

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

coming soon

## Branch conventions

`env.type/scope@description`

Example: `dev.feat/auth@jwt-login`
