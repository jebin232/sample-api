from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO
from rembg import remove
import base64

app = FastAPI()

@app.post("/remove_background/")
async def remove_background(file: UploadFile):
    try:
        # Read the uploaded image and remove the background using rembg
        with BytesIO() as buffer:
            image = Image.open(file.file)
            output = remove(image)

            # Save the result to a buffer
            output.save(buffer, format="PNG")
            buffer.seek(0)

            # Encode the image as base64
            result_base64 = base64.b64encode(buffer.read()).decode()

        return {"image_base64": result_base64}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
