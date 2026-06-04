from database import init_db
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "👋"}


if __name__ == "__main__":
    init_db()

#     uvicorn.run(app, host="0.0.0.0", port=8000)
    port = int(os.environ.get("PORT", 8000))
    print("PORT =", port)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
