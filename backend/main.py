from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def check():
    return {"status": "ok"}
