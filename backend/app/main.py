from fastapi import FastAPI

app = FastAPI(title="AI Dropshipping Agent")

@app.get("/")
def health_check():
    return {"status": "ok"}
