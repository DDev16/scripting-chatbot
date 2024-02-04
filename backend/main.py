# uvicorn main:app
# uvicorn main:app --reload
# python -m venv venv
# .\venv\Scripts\activate


# Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import openai

# Custom Functions import
from functions.database import store_messages, reset_messages
from functions.openai_request import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech
import requests

# Temporary storage for audio response
# In a production environment, consider using a more persistent storage solution
temp_audio_storage = None

# Init app
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

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_to_nft_storage(file_content: bytes, api_key: str) -> str:
    """
    Uploads file content to NFT.Storage and returns the IPFS URL of the uploaded file.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/octet-stream"
    }
    response = requests.post("https://api.nft.storage/upload", headers=headers, data=file_content)
    
    if response.status_code == 200:
        result = response.json()
        cid = result["value"]["cid"]
        return f"https://ipfs.io/ipfs/{cid}"
    else:
        raise HTTPException(status_code=500, detail="Failed to upload file to NFT.Storage")

# Check Health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}

# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}

# Get Audio and Text Responses
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    global temp_audio_storage  # Reference the global variable for temporary audio storage
    
    # Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    
    with open(file.filename, "rb") as audio_input:
        print("File saved and ready for processing")
        
        # Decode Audio
        message_decoded = convert_audio_to_text(audio_input)
        print(f"Decoded message: {message_decoded}")
        
        # Guard: Ensure message decoded
        if not message_decoded:
            return HTTPException(status_code=400, detail="Failed to decode audio")
        
        # Get ChatGPT Response
        chat_response = get_chat_response(message_decoded)
        print(f"ChatGPT response: {chat_response}")
        
        # Guard: Ensure chat response
        if not chat_response:
            return HTTPException(status_code=400, detail="Failed to get chat response")
        
        # Store Messages
        store_messages(message_decoded, chat_response)
        
        # Convert Chat Response to audio
        audio_output = convert_text_to_speech(chat_response)
        
        # Guard: Ensure audio response
        if not audio_output:
            return HTTPException(status_code=400, detail="Failed to convert chat response to audio")
        
        # Store audio response temporarily
        temp_audio_storage = audio_output
    
    return {
        "chat_response": chat_response,
        "decoded_message": message_decoded
    }

# Get Audio Response
@app.get("/get-audio-response/")
async def get_audio_response():
    global temp_audio_storage  # Ensure we're using the global variable
    
    if temp_audio_storage is None:
        return HTTPException(status_code=404, detail="Audio response not found")
    
    def iterfile():
        yield temp_audio_storage
    
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
    

# Post bot response 

# Note: Not playing in browser when using post request

# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):

#     print("hello")
    