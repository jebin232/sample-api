from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

responses = {
    "hi": "Hello! How can I help you?",
    "how are you": "I'm just a bot, but I'm here to assist you!",
    "bye": "Goodbye! Have a great day!",
}

class MessageResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/chatbot/")
def chatbot_response(message: str):
    message = message.lower()
    if message in responses:
        return MessageResponse(response=responses[message])
    else:
        return MessageResponse(response="I'm sorry, I don't understand that")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
