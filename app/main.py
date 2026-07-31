from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, EmailStr, Field
from app.auth import supabase



app = FastAPI(title="Auth API", version="1.0.0")

class AuthBody(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

@app.get("/")
def root():
    return {"message": "Auth API is running and connected to Supabase"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/signup", status_code=201)
def signup(body: AuthBody):
    try:
        res = supabase.auth.sign_up({"email": body.email, "password": body.password})
        return {"user": res.user}
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@app.post("/auth/login")
def login(body: AuthBody):
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": res.user
        }
    except Exception:
        raise HTTPException(401, detail="Invalid login credentials")



@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile(authorization: str | None = Header(None)):
    # Check that a token was presented in the Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, detail="Access token required")
    return {"message": "Token was presented (not verified yet)"}

