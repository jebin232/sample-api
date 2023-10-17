import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import os
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse

from rembg import remove
import cv2
import numpy as np

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:19006",
    "http://localhost:63342",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined responses for the chatbot
responses = {
    "hi": "Hello! How can I help you?",
    "how are you": "I'm just a bot, but I'm here to assist you!",
    "bye": "Goodbye! Have a great day!",
}

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/chatbot/")
def chatbot_response(message: str):
    message = message.lower()
    if message in responses:
        return {"response": responses[message]}
    else:
        return {"response": "I'm sorry, I don't understand that"}

# def process_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#
#         if not ret:
#             break
#
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         pil_frame = Image.fromarray(frame)
#
#         # Remove background using rembg
#         output_frame = remove(pil_frame)
#
#         yield cv2.imencode('.jpg', np.array(output_frame))[1].tobytes()
#
#     cap.release()
@app.post("/background/")
async def remove_image_background(image: UploadFile = File(...), background: UploadFile = File(...)):
    try:
        # Read the uploaded image and background into memory
        image_data = await image.read()
        background_data = await background.read()

        # Open the image and background using PIL
        input_image = Image.open(io.BytesIO(image_data))
        background_image = Image.open(io.BytesIO(background_data))

        # Check transparency channels of the images
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
        if background_image.mode != 'RGBA':
            background_image = background_image.convert('RGBA')

        # Resize background image to match input image dimensions
        background_image = background_image.resize(input_image.size)

        # Remove background from input image
        output = "out.png"

        removed_background = remove(input_image)
        removed_background.save(output)
        # waits for user to press any key
        # (this is necessary to avoid Python kernel form crashing)
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()


        # Composite the input image with the background
        output_image = Image.alpha_composite( background_image,removed_background)

        # Save the resulting image
        output_path = "output.png"
        output_image.save(output_path)

        return FileResponse(output_path, media_type='image/png', filename=output_path)

    except Exception as e:
        return {"result": "error", "error_message": str(e)}

@app.post("/remove-background/")
async def remove_video_background(video: UploadFile = File(...)):
    try:
        # Save the uploaded video to a temporary file
        video_path = f"temp_{video.filename}"
        with open(video_path, "wb") as f:
            f.write(video.file.read())

        # Open the video using OpenCV
        cap = cv2.VideoCapture(video_path,cv2.CAP_FFMPEG)
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to PIL Image
            pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Remove background using rembg
            output_frame = remove(pil_frame)
            frames.append(output_frame)

        cap.release()
        cv2.destroyAllWindows()

        # Convert the list of PIL frames back to OpenCV format
        output_frames = [np.array(frame) for frame in frames]

        # Save the background-removed frames to a video file
        output_path = "output.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (output_frames[0].shape[1], output_frames[0].shape[0]))
        for frame in output_frames:
            out.write(frame)
        out.release()

        return FileResponse(output_path, media_type='video/mp4', filename=output_path)

    except Exception as e:
        return JSONResponse(content={"result": "error", "error_message": str(e)})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
