import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router  # Import the router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the chat router
app.include_router(chat_router)

@app.get("/")
def read_route():
    return {"message": "Hospital bot API is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use PORT assigned by Render
    uvicorn.run(app, host="0.0.0.0", port=port)
