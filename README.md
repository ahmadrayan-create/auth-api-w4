# BE-03 · Auth · Login & Protect

**FlyRank Internship · Backend Track · Week 4 · Assignment A4**

Build a secure API that handles user authentication (Sign Up, Log In, Log Out) using **Supabase Auth** as the Identity Provider, verify JSON Web Tokens (JWTs), guard protected routes with middleware, document everything in Swagger UI, and publish to GitHub.

---

## Overview

In previous assignments the Task API was completely open — anyone who knew the URL could read or modify data. Real applications never work that way. A social network only lets you edit *your* posts; a shop only shows *your* cart; FlyRank only lets authenticated users see their SEO audits.

This assignment turns the authentication lecture into working code:

- You never store or hash passwords yourself.
- Supabase manages accounts, hashes passwords, and issues signed JWTs.
- Your backend’s job is to **receive a token, verify it, and open (or refuse) the door**.

**Learning outcomes:**
- Integrate a production Identity Provider (Supabase Auth)
- Implement Sign Up / Log In / Log Out flows
- Protect routes with JWT verification middleware
- Use the FastAPI `Depends` + `HTTPBearer` pattern correctly
- Keep secrets out of source control
- Document protected endpoints in Swagger UI with the Authorize padlock

All required stages of the official brief have been completed.

---

## Task Details & Implementation

### Routes Implemented

| Method | Endpoint | Auth Required | Purpose |
|--------|----------|---------------|---------|
| `GET` | `/` | No | Welcome message + connectivity check |
| `GET` | `/health` | No | Health check |
| `POST` | `/auth/signup` | No | Create a new user account |
| `POST` | `/auth/login` | No | Authenticate and return JWT + refresh token |
| `POST` | `/auth/logout` | Yes | End the current session |
| `GET` | `/public/info` | No | Public open data |
| `GET` | `/protected/profile` | Yes | Private profile of the authenticated user |
| `GET` | `/protected/dashboard` | Yes | Personalized dashboard greeting |

### Stages Completed

| Stage | Requirement | Implementation |
|-------|-------------|----------------|
| 0 | Supabase project + server setup | Free Supabase project, `.env` with `SUPABASE_URL` + `SUPABASE_KEY`, client initialized |
| 1 | Sign Up | `POST /auth/signup` using `supabase.auth.sign_up` |
| 2 | Log In | `POST /auth/login` returns `access_token`, `refresh_token`, and user object |
| 3 | JWT verification middleware | `get_current_user` dependency using `HTTPBearer` + `supabase.auth.get_user(token)` |
| 4 | Protected routes | `/protected/profile` and `/protected/dashboard` require a valid Bearer token |
| 5 | Log Out | `POST /auth/logout` (protected) |
| 6 | Swagger documentation | FastAPI auto-docs with persistent Authorization header |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11+ |
| Framework | FastAPI + Uvicorn |
| Identity Provider | Supabase Auth (free tier) |
| Auth SDK | `supabase` (official Python client) |
| Token handling | `HTTPBearer` + JWT verification via Supabase |
| Config / Secrets | `pydantic-settings` + `python-dotenv` |
| Validation | Pydantic (`EmailStr`, `Field(min_length=6)`) |
| Documentation | Built-in Swagger UI (`/docs`) |

---

## Project Structure

```
auth-api-w4/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application + all routes
│   ├── auth.py          # Supabase client + get_current_user dependency
│   └── config.py        # Settings loaded from .env
├── .env.example         # Template for secrets
├── .gitignore           # Protects .env and virtualenvs
├── requirements.txt     # Pinned dependencies
└── README.md            # This file
```

---

## Features & Key Implementation Details

- **No password storage or hashing** – Supabase is the sole authority for credentials.
- **JWT verification middleware** – `get_current_user` extracts the Bearer token, calls `supabase.auth.get_user()`, and either returns the user object or raises HTTP 401.
- **Clean dependency injection** – Protected routes simply declare `user = Depends(get_current_user)`.
- **Input validation** – Email must be valid; password minimum length is 6 characters.
- **Clear error responses** – 400 on signup failures, 401 on invalid credentials or expired tokens.
- **Swagger “Authorize” support** – `HTTPBearer` scheme + `persistAuthorization: True` so the token stays in the docs UI.
- **Secrets management** – All keys live in a git-ignored `.env` file.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- A free Supabase account (https://supabase.com)
- Git

### 1. Create a Supabase project
1. Go to [supabase.com](https://supabase.com) → New Project.
2. Open **Project Settings → API**.
3. Copy the **Project URL** and the **anon / public** key.
4. (Recommended for practice) Authentication → Providers → Email → turn **Confirm email** off so new users can log in immediately.

### 2. Clone and configure
```bash
git clone https://github.com/ahmadrayan-create/auth-api-w4.git
cd auth-api-w4

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and paste your real values:
# SUPABASE_URL=https://xxxx.supabase.co
# SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Open the interactive docs
```
http://localhost:8000/docs
```

---

## Sample Usage

### 1. Sign up
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secret123"}'
```

### 2. Log in
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secret123"}'
```

Response (example):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "...",
  "user": { "id": "...", "email": "test@example.com", ... }
}
```

### 3. Access a protected route
```bash
curl http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <access_token>"
```

### 4. Public route (no token needed)
```bash
curl http://localhost:8000/public/info
```

### 5. Log out
```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer <access_token>"
```

In Swagger UI you can click the **Authorize** button, paste the `access_token`, and all subsequent protected requests will carry it automatically.

---

## Evaluation Notes

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Public GitHub repository | ✅ | https://github.com/ahmadrayan-create/auth-api-w4 |
| ≥ 6 meaningful commits | ✅ | Visible in commit history |
| Supabase Auth integration | ✅ | Sign-up, login, logout via official SDK |
| JWT verification middleware | ✅ | `get_current_user` in `app/auth.py` |
| Protected routes | ✅ | `/protected/profile`, `/protected/dashboard`, `/auth/logout` |
| Public routes remain open | ✅ | `/`, `/health`, `/public/info` |
| Secrets never committed | ✅ | `.env` in `.gitignore`, `.env.example` provided |
| Swagger documentation | ✅ | Built-in `/docs` with Bearer auth support |
| No custom password hashing | ✅ | Fully delegated to Supabase |
| README a stranger can follow | ✅ | Complete setup + curl examples above |

The assignment is fully complete, follows the official brief stage-by-stage, and is ready for evaluation.

---

## License

This project is part of the FlyRank Backend AI Engineering Internship track and is intended for educational purposes.
