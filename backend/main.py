from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
from io import BytesIO
import requests

# Custom Functions import
from functions.database import store_messages, reset_messages
from functions.openai_request import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

# NFT.Storage API key
NFT_STORAGE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDdGOTA4QjNBRDJGMDFGNjE2MjU1MTA0ODIwNjFmNTY5Mzc2QTg3MjYiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTcwNjkyODU5OTI1OCwibmFtZSI6IkNoYXRib3QifQ.VWrWdKJ8HNZd1T3lFfuKuprcOM9qzTCxb6RD78eO_bo"

app = FastAPI()

# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5000",
    "https://scripting-chatbot.vercel.app/",
    "https://nextjs-fastapi-starter-two-delta.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def check_health():
    return {"message": "healthy"}

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}

def upload_to_nft_storage(file_content: bytes, api_key: str) -> str:
    """
    Uploads file to NFT.Storage and returns the CID of the uploaded file.
    """
    url = "https://api.nft.storage/upload"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/octet-stream",
    }
    response = requests.post(url, headers=headers, data=file_content)
    response.raise_for_status()  # Raises an HTTPError if the response was an error
    result = response.json()
    return f"https://ipfs.io/ipfs/{result['value']['cid']}"

@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    file_content = await file.read()
    audio_input = BytesIO(file_content)
    
    message_decoded = convert_audio_to_text(audio_input)
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    chat_response = get_chat_response(message_decoded)
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")
    
    store_messages(message_decoded, chat_response)
    audio_output = convert_text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to convert chat response to audio")
    
    # Upload audio response to NFT.Storage
    audio_cid_url = upload_to_nft_storage(audio_output, NFT_STORAGE_API_KEY)
    
    return {
        "chat_response": chat_response,
        "decoded_message": message_decoded,
        "audio_cid_url": audio_cid_url
    }
