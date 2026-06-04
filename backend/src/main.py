from src.database import init_db
from fastapi import FastAPI
import uvicorn
import os
from src.routes.auth import router as auth_router
import sys
print(sys.path)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
async def hello():
    return {"message": "👋"}


if __name__ == "__main__":
    init_db()

# Railway ne fonctionnait pas avec le port 8000, j'ai donc ajouté une variable d'environnement pour récupérer le port dynamique fourni par Railway
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    port = int(os.environ.get("PORT", 8000))
    print("PORT =", port)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
