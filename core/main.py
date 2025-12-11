from fastapi import FastAPI

app = FastAPI(title="NAS Super-App Core")

@app.get("/")
def read_root():
    return {"message": "Welcome to NAS Super-App Core"}
