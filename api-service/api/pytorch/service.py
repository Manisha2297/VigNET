import os
from fastapi import FastAPI, File, Form, UploadFile
from tempfile import TemporaryDirectory
from starlette.middleware.cors import CORSMiddleware
from api.pytorch.model import load_processor_model, get_prediction

# Setup FastAPI app
app = FastAPI(
    title="API Server",
    description="API Server",
    version="v2"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # Startup tasks

    print("=== Loading Pre-trained vilt model ===")
    await load_processor_model()
    print("== Successfully loaded! ==")


# Routes
@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }


@app.post("/predict/")
async def predict(
        question: str = Form(...),
        file: UploadFile = File(...)
):
    file_content = await file.read()
    print("question is ", question)
    print("predict file:", len(file_content), type(file_content))

    # Save the image
    with TemporaryDirectory() as image_dir:
        image_path = os.path.join(image_dir, "test.png")
        with open(image_path, "wb") as output:
            output.write(file_content)

        # Make prediction
        prediction_results = {}
        answer = get_prediction(image_path, question)
        prediction_results['prediction_label_vilt'] = answer

    return prediction_results


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
