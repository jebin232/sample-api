from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/remove_background/")
async def remove_background(file: UploadFile):
    # Check if the uploaded file is an image
    if file.content_type.startswith('image'):
        # Read the uploaded image
        image_bytes = await file.read()

        # Use rembg to remove the background
        output_bytes = remove(image_bytes)

        # Open the processed image with Pillow
        image = Image.open(BytesIO(output_bytes))

        # Save the processed image to a temporary file
        output_path = "output.png"
        image.save(output_path, "PNG")

        # Return the processed image
        return FileResponse(output_path, media_type="image/png")

    return {"error": "Uploaded file is not an image."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
