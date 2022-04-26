import os
import json
import numpy as np
import tensorflow as tf
import gensim
import spacy
from tensorflow.keras.models import load_model
from keras.applications.vgg16 import preprocess_input



AUTOTUNE = tf.data.experimental.AUTOTUNE
local_experiments_path = "/persistent/experiments"
best_model = None
best_model_id = None
prediction_model = None
data_details = None
image_width = 224
image_height = 224
num_channels = 3
model = None


def load_prediction_model():
    print("Loading Model...")
    global prediction_model, data_details

    best_model_path = os.path.join(
        local_experiments_path, best_model["experiment"], best_model["model_name"]+".hdf5")

    print("best_model_path:", best_model_path)
    prediction_model = tf.keras.models.load_model(best_model_path)
    print(prediction_model.summary())

    # data_details_path = os.path.join(
    #     local_experiments_path, best_model["experiment"], "data_details.json")

    # # Load data details
    # with open(data_details_path, 'r') as json_file:
    #     data_details = json.load(json_file)


def check_model_change():
    global best_model, best_model_id
    best_model_json = os.path.join(local_experiments_path, "best_model.json")
    if os.path.exists(best_model_json):
        with open(best_model_json) as json_file:
            best_model = json.load(json_file)

        if best_model_id != best_model["experiment"]:
            load_prediction_model()
            best_model_id = best_model["experiment"]


def load_preprocess_image_from_path(image_path):
    print("Image", image_path)

    image_width = 224
    image_height = 224
    num_channels = 3

    # Prepare the data
    def load_image(path):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=num_channels)
        image = tf.image.resize(image, [image_height, image_width])
        return image

    # Normalize pixels
    def normalize(image):
        image = image / 255
        return image

    test_data = tf.data.Dataset.from_tensor_slices(([image_path]))
    test_data = test_data.map(load_image, num_parallel_calls=AUTOTUNE)
    test_data = test_data.map(normalize, num_parallel_calls=AUTOTUNE)
    test_data = test_data.repeat(1).batch(1)

    return test_data

def get_questions_sum(questions, nlp):
    nb_samples = len(questions)
    word2vec_dim = 300
    ques_matrix = np.zeros((nb_samples, word2vec_dim))
    for index in range(len(questions)):
        tokens = nlp(questions[index])
        for j in range(len(tokens)):
            ques_matrix[index,:] += tokens[j].vector

    return ques_matrix


def decode_img(img):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.io.decode_jpeg(img, channels=3)
    # resize the image to the desired size
    img = img/255-0.5
    img = preprocess_input(img)
    return tf.image.resize(img, [224, 224])

def get_image_data(img):
    img = tf.io.read_file(img)
    resized_image_data = decode_img(img)
    return resized_image_data

def get_tensors(image_tensor, question_dataset):
    return (image_tensor, question_dataset)

def create_dataset(question_matrix, image_input):
    images = tf.data.Dataset.list_files(image_input)
    image_tensor = images.map(get_image_data)

    question_dataset = tf.convert_to_tensor(question_matrix)
    question_dataset = tf.data.Dataset.from_tensor_slices((question_dataset))

    #Combining dataset
    dataset = tf.data.Dataset.zip((image_tensor, question_dataset))
    dataset = tf.data.Dataset.zip((dataset, tf.data.Dataset.from_tensor_slices((tf.constant(np.zeros(1000))))))
    dataset = dataset.repeat(1).batch(1)
    dataset = dataset.prefetch(1)
    return dataset

def get_prediction(dataset):
    global prediction_model
    prediction = prediction_model.predict(dataset)
    idx = prediction.argmax(axis=1)[0]
    
    with open('./api/label_encoded.json', 'r') as f:
        label_encoded = json.load(f)

    prediction_label = label_encoded[str(idx)]
    return prediction_label

def load_pretrained_weights():
    global model
    google_news_path = '../persistent/experiments/pretrained_weights/GoogleNews-vectors-negative300.bin.gz'
    print("Loading word2vec")
    model = gensim.models.KeyedVectors.load_word2vec_format(google_news_path, binary=True)
    print("Done loading word2vec")


def get_test_data(image_path, question):
    global model
    nlp = spacy.blank('en')

    # Loop through range of all indexes, get words associated with each index.
    # The words in the keys list will correspond to the order of the google embed matrix
    keys = model.vocab.keys()

    # Set the vectors for our nlp object to the google news vectors
    nlp.vocab.vectors = spacy.vocab.Vectors(data=model.syn0, keys=model.index2word)
    question_representation = get_questions_sum(question, nlp)

    # saving image in a temp path and reading the image from that path 
    dataset = create_dataset(question_representation, image_path)
    return dataset


def make_prediction(image_path, question):
    check_model_change()

    # Load & preprocess
    test_data = get_test_data(image_path, question)

    # Make prediction
    prediction = get_prediction(test_data)

    return {
        "prediction_label_base": prediction,
    }



