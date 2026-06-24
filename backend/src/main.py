from src.database import init_db
from fastapi import FastAPI
import uvicorn
import os
from src.routes.auth import router as auth_router
from src.routes.chats import router as chats_router
import sys
from fastapi.middleware.cors import CORSMiddleware
from src.routes.pressReviews import router as press_reviews_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
     #    "https://newsfoundry.vercel.app",
        "https://news-foundry-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(press_reviews_router)

@app.get("/")
async def hello():
    return {"message": "👋"}


if __name__ == "__main__":
    init_db()

# Railway ne fonctionnait pas avec le port 8000, j'ai donc ajouté une variable d'environnement pour récupérer le port dynamique fourni par Railway
    port = int(os.environ.get("PORT", 8000))
    print("PORT =", port)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )


