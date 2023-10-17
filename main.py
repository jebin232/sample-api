from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Store conversation history
conversation_history = []

class Message(BaseModel):
    text: str

@app.post("/send_message/")
async def send_message(message: Message):
    user_message = message.text
    conversation_history.append({"role": "user", "content": user_message})

    # You can add logic here to generate a response based on user_message
    response_message = "Hello! How can I assist you today?"
    conversation_history.append({"role": "assistant", "content": response_message})

    return {"message": response_message}

@app.get("/get_history/")
async def get_conversation_history():
    return conversation_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
