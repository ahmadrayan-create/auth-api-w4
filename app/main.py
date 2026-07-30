from fastapi import FastAPI

app = FastAPI(title="Auth API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Auth API is running and connected to Supabase"}