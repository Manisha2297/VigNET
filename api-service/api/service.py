import os
import asyncio
import json
from fastapi import FastAPI, File, UploadFile, Form
from starlette.middleware.cors import CORSMiddleware
from api.ViLT.demo_vqa import get_predictions
from api.ViLT.vilt.config import ex

# from api.tracker import TrackerService remove comment
# import dataaccess.session as database_session
# from dataaccess import leaderboard

from tempfile import TemporaryDirectory
from api import model

# Initialize Tracker Service
# tracker_service = TrackerService() remove comment

# Setup FastAPI app
app = FastAPI(
    title="API Server",
    description="API Server",
    version="v1"
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
    # # Connect to database
    # await database_session.connect()
    # Start the tracker service

    # print("===Loading Pre trained weights===")
    # model.load_pretrained_weights()   

    print("===Tracking experiments===")
    # asyncio.create_task(tracker_service.track()) remove comment


# @app.on_event("shutdown")
# async def shutdown():
#     # Shutdown tasks
#     # Disconnect from database
#     await database_session.disconnect()

# Routes


@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }


# @app.get("/leaderboard")
# async def get_leaderboard():
#     return await leaderboard.browse()


# @app.get("/best_model")
# async def get_best_model():
#     model.check_model_change()
#     if model.best_model is None:
#         return {"message": 'No model available to serve'}
#     else:
#         return {
#             "message": 'Current model being served:'+model.best_model["model_name"],
#             "model_details": model.best_model
#         }



# @app.post("/predict/{question}")
# async def predict(
#         question: str = '',
#         file: bytes = File(...),
#         # question: str
# ):
#     print("question is ",question)
#     print("predict file:", len(file), type(file))

#     # Save the image
#     with TemporaryDirectory() as image_dir:
#         image_path = os.path.join(image_dir, "test.png")
#         with open(image_path, "wb") as output:
#             output.write(file)

#         # Make prediction
#         prediction_results = {}
#         get_predictions(image_path, question)
#         prediction_results['prediction_label_vilt'] = ex.info['answer']

#     return prediction_results


@app.post("/predict/")
async def predict(
        question: str = Form(...),
        file: UploadFile = File(...),
        # question: str
):
    file_content = await file.read()
    print("question is ",question)
    print("predict file:", len(file_content), type(file_content))

    # Save the image
    with TemporaryDirectory() as image_dir:
        image_path = os.path.join(image_dir, "test.png")
        with open(image_path, "wb") as output:
            output.write(file_content)

        # Make prediction
        prediction_results = {}
        get_predictions(image_path, question)
        prediction_results['prediction_label_vilt'] = ex.info['answer']

    return prediction_results

