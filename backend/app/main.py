from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Library Assistant API"}


@app.get("/health")
async def health():
    return {"status": "ok"}