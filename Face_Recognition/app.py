from PIL import Image, ImageFont, ImageDraw, ImageFilter
import gradio as gr
from fastapi import FastAPI
from face_recognition import FaceRecognition
from FaceDetection import FaceDetection

FaceRecognition = FaceRecognition()
FaceDetection = FaceDetection()

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "This is your main app"}


io_recognition = gr.Interface(fn=FaceRecognition.recognition,
                              inputs=[gr.inputs.Image(type='pil', label="Original Image")],
                              outputs=[gr.outputs.Image(type="pil", label="Output Image")])
io_detection = gr.Interface(fn=FaceDetection.detection2,
                            inputs=[gr.inputs.Image(type='pil', label="Original Image")],
                            outputs=[gr.outputs.Image(type="pil", label="Output Image")])
gr.mount_gradio_app(app, io_recognition, path="/recognition")
gr.mount_gradio_app(app, io_detection, path="/detection")

# Run this from the terminal as you would normally start a FastAPI app: `uvicorn app:app`
# and navigate to http://localhost:8000/gradio in your browser.
