from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model to handle incoming messages
class Message(BaseModel):
    text: str

# Create a list of predefined responses
responses = [
    "Hello! How can I assist you?",
    "I'm here to help. What can I do for you?",
    "Please ask me a question, and I'll do my best to answer.",
]

# Define the endpoint for handling user messages
@app.post("/chat")
async def chat(message: Message):
    user_message = message.text
    # You can add more advanced logic here to generate responses.
    # For now, we'll just rotate through the predefined responses.
    response = responses[len(responses) % len(responses)]
    return {"response": response}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
