from fastapi import FastAPI
from app.routes.chat import router as chat_router  # Import the router

app = FastAPI()

# Include the chat router
app.include_router(chat_router)

@app.post("/")
def read_route():
    return {"message": "Hospital bot API is running"}
