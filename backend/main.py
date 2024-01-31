# uvicorn main:app
# uvicorn main:app --reload
# python -m venv venv
# .\venv\Scripts\activate


#Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai 


# Custom Functions import
from functions.openai_request import convert_audio_to_text, get_chat_response

# init app
app = FastAPI()

# CORS - Origins

origins = [
    "http://localhost:5173",
    "http://localhost:5173",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://localhost:5000",
]

# CORS - Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Check Health 
@app.get("/health")
async def check_health():
    return {"message": "healthy"}   


# Get Audio
@app.post("/post-audio-get/")
async def get_audio():

    # Get saved audio
    audio_input = open("voice.mp3", "rb")

    # Decode Audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Esnure message decoded 
    if not message_decoded:
        raise HTTPException(status_code=404, detail="Failed to decode audio")


    # Get ChatGpt Response
    chat_response = get_chat_response(message_decoded)

    print (chat_response)
    
    return "Done"

# Post bot response 
# Note: Not playing in browser when using post request

# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):

#     print("hello")
    