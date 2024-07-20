from PIL import Image
import torch
from transformers import AutoProcessor, CLIPModel
import torch.nn as nn
import requests
from io import BytesIO
import os
import pickle
import numpy as np
import pandas as pd

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)


def load_image_PIL(url_or_path):
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        return Image.open(requests.get(url_or_path, stream=True).raw)
    else:
        return Image.open(url_or_path)


def cosine_similarity(vec1, vec2):
    # Compute the dot product of vec1 and vec2
    dot_product = np.dot(vec1, vec2)

    # Compute the L2 norm of vec1 and vec2
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # Compute the cosine similarity
    similarity = dot_product / (norm_vec1 * norm_vec2)

    return similarity


temp = pd.read_csv(
    r"/Users/davidemastricci/Documents/personal_workspace/from-0-to-AI-3Sides/experiments/image_class.csv",
)  ### make an image_class.xlsx of trending fashion pictures
classes = temp["Col_Names"].tolist()
classes = [s.lstrip() for s in classes]
positive_classes = []
negative_classes = []
for i in range(len(classes)):
    positive_classes.append(f"a outstanding picture, of a #{classes[i]}")
    negative_classes.append(f"a horrible picture, of a #{classes[i]}")

positive_inputs = processor(
    text=positive_classes, return_tensors="pt", padding=True
).to(device)
with torch.no_grad():
    positive_text_features = model.get_text_features(**positive_inputs)
negative_inputs = processor(
    text=negative_classes, return_tensors="pt", padding=True
).to(device)
with torch.no_grad():
    negative_text_features = model.get_text_features(**negative_inputs)

positive_prompt_vectors = np.array(positive_text_features)
# Compute the average vector
average_positive_vector = np.mean(positive_prompt_vectors, axis=0)

negative_prompt_vectors = np.array(negative_text_features)
# Compute the average vector
average_negative_vector = np.mean(negative_prompt_vectors, axis=0)

with open("./positive_prompt.pkl", "wb") as f:
    pickle.dump(average_positive_vector, f)
with open("./negative_prompt.pkl", "wb") as f:
    pickle.dump(average_negative_vector, f)

##CODE FOR RUNTIME
with open("./positive_prompt.pkl", "rb") as f:
    average_positive_vector = pickle.load(f)
with open("./negative_prompt.pkl", "rb") as f:
    average_negative_vector = pickle.load(f)


def predict(img_url):
    image1 = load_image_PIL(img_url)
    with torch.no_grad():
        inputs1 = processor(images=image1, return_tensors="pt").to(device)
        image_features1 = model.get_image_features(**inputs1)
        image_vector = image_features1.numpy()
    positive_similarity = cosine_similarity(
        average_positive_vector, np.transpose(image_vector)
    )
    negative_similarity = cosine_similarity(
        average_negative_vector, np.transpose(image_vector)
    )
    aesthetic_score = (+1 * positive_similarity) + (-1 * negative_similarity)

    return (
        aesthetic_score * 1000
    )  # Multiplied by 1000 just to make it easier to compare scores


if __name__ == "__main__":
    img_path = r"/Users/davidemastricci/Documents/personal_workspace/from-0-to-AI-3Sides/data_sample/goodexaple1.jpg"
    scored = predict(img_path)

    print(f"Aesthetic score for this image : {scored}")
