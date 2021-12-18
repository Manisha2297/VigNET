import os
import asyncio
from glob import glob
import json
import pandas as pd

import tensorflow as tf
from google.cloud import storage

# from dataaccess.session import database

gcp_project = os.environ["GCP_PROJECT"]
bucket_name = "vqa-dataset-bucket"
local_experiments_path = "/persistent/experiments"

# Setup experiments folder
if not os.path.exists(local_experiments_path):
    os.mkdir(local_experiments_path)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def download_experiment_metrics():
    # Get all model metrics
    models_list = tf.io.gfile.glob(
        "gs://vqa-dataset-bucket/model/*/*")

    nested_folders_list = tf.io.gfile.glob(
        "gs://vqa-dataset-bucket/model/*/*/*")

    models_list = models_list + nested_folders_list

    timestamp = 0

    for model_file in models_list:
        print("Metrics file:", model_file)

        if model_file.endswith("/"):
            print("Skipping since its a folder")
            continue

        relative_path = model_file.split("/model/")[1]

        local_model_file = os.path.join(local_experiments_path, relative_path)
        

        if not os.path.exists(local_model_file):
            print("Copying:", model_file, local_model_file)

            # Ensure user directory exists
            os.makedirs(os.path.dirname(local_model_file), exist_ok=True)

            model_file = model_file.replace(
                "gs://vqa-dataset-bucket/", "")
            # Download the metric json file
            download_blob(bucket_name, model_file, local_model_file)

            file_timestamp = os.path.getmtime(local_model_file)
            if file_timestamp > timestamp:
                timestamp = file_timestamp

    return timestamp


def download_best_models():
    print("Download leaderboard models and artifacts")
    try:

        df = pd.read_csv(local_experiments_path+"/leaderboard.csv")
        print("Shape:", df.shape)
        print(df.head())

        for index, row in df.iterrows():
            print(row["user"], row["experiment"], row["model_name"])

            download_file = os.path.join(
                row["user"], row["experiment"], row["model_name"]+".hdf5")
            download_blob(bucket_name, download_file,
                          os.path.join(local_experiments_path, download_file))

            download_file = os.path.join(
                row["user"], row["experiment"], row["model_name"]+"_train_history.json")
            download_blob(bucket_name, download_file,
                          os.path.join(local_experiments_path, download_file))

            # Data details
            download_file = os.path.join(
                row["user"], row["experiment"], "data_details.json")
            download_blob(bucket_name, download_file,
                          os.path.join(local_experiments_path, download_file))
    except:
        print("Error in download_best_models")


async def save_leaderboard_db():
    # read leaderboard
    df = pd.read_csv(local_experiments_path+"/leaderboard.csv")
    print("Shape:", df.shape)
    print(df.head())

    # Delete current data in table
    query = "delete from leaderboard;"
    print("query:", query)
    await database.execute(query)

    # Insert rows
    query = f"""
        INSERT INTO leaderboard (
                trainable_parameters ,
                execution_time ,
                loss ,
                accuracy ,
                model_size ,
                learning_rate ,
                batch_size ,
                epochs ,
                optimizer ,
                email ,
                experiment ,
                model_name 
            ) VALUES (
                :trainable_parameters ,
                :execution_time ,
                :loss ,
                :accuracy ,
                :model_size ,
                :learning_rate ,
                :batch_size ,
                :epochs ,
                :optimizer ,
                :email ,
                :experiment ,
                :model_name 
            );
       """
    for index, row in df.iterrows():
        await database.execute(query, {
            "trainable_parameters": row["trainable_parameters"],
            "execution_time": row["execution_time"],
            "loss": row["loss"],
            "accuracy": row["accuracy"],
            "model_size": row["model_size"],
            "learning_rate": row["learning_rate"],
            "batch_size": row["batch_size"],
            "epochs": row["epochs"],
            "optimizer": row["optimizer"],
            "email": row["user"],
            "experiment": row["experiment"],
            "model_name": row["model_name"]
        })


class TrackerService:
    def __init__(self):
        self.timestamp = 0

    async def track(self):
        while True:
            await asyncio.sleep(60)
            print("Tracking experiments...")

            # Download new model metrics
            timestamp = download_experiment_metrics()