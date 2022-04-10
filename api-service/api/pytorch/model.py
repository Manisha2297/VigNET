from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image


def load_processor_model():
    global processor, model
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")


def encode_input_data(image_path, question):
    image = Image.open(image_path).convert("RGB")
    print("shape =", image.size)
    encoding = processor(image, question, return_tensors="pt")
    return encoding


def make_prediction(input_data_encoding):
    # forward pass
    outputs = model(**input_data_encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    predicted_ans = model.config.id2label[idx]
    print("Predicted answer:", predicted_ans)
    return predicted_ans


def get_prediction(image_path, question):

    # Load & preprocess
    input_data_encoding = encode_input_data(image_path, question)

    # Make prediction
    prediction = make_prediction(input_data_encoding)

    return {
        "predicted_ans": prediction,
    }