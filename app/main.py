import os
import uvicorn
from fastapi import FastAPI
from app.routes.chat import router as chat_router  # Import the router

app = FastAPI()

# Include the chat router
app.include_router(chat_router)

@app.post("/")
def read_route():
    return {"message": "Hospital bot API is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use PORT from env or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
