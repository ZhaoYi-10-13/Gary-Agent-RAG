# Copyright 2024
# Directory: yt-rag/main.py

from fastapi import FastAPI
from datetime import datetime
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="YouTube RAG API")

# Define allowed origins for CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://yt-rag.vercel.app"
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],    # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to YouTube RAG API"}

@app.get("/greet/{name}")
async def greet(name: str):
    """
    Greet endpoint that returns a personalized greeting.
    
    Args:
        name (str): Name of the person to greet
    """
    return {"message": f"Hello, {name}! I think you are great!"}
