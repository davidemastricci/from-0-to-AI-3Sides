from PIL import Image
import torch
from transformers import AutoProcessor, CLIPModel
import requests
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from src.common.utils import ROOT_PATH

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)


def _load_image_PIL(url_or_path):
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        return Image.open(requests.get(url_or_path, stream=True).raw)
    else:
        return Image.open(url_or_path)


def _cosine_similarity(vec1, vec2):
    # Compute the dot product of vec1 and vec2
    dot_product = np.dot(vec1, vec2)

    # Compute the L2 norm of vec1 and vec2
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # Compute the cosine similarity
    similarity = dot_product / (norm_vec1 * norm_vec2)

    return similarity


def _initialize_model(processor, model, device):
    image_classes = pd.read_csv(Path(ROOT_PATH) / "artifacts/image_class.csv")
    classes = image_classes["Col_Names"].tolist()
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

    with open(Path(ROOT_PATH) / "artifacts/positive_prompt.pkl", "wb") as f:
        pickle.dump(average_positive_vector, f)
    with open(Path(ROOT_PATH) / "artifacts/negative_prompt.pkl", "wb") as f:
        pickle.dump(average_negative_vector, f)


def predict(image: Image):
    if (
        not (Path(ROOT_PATH) / "artifacts/positive_prompt.pkl").exists()
        or not (Path(ROOT_PATH) / "artifacts/negative_prompt.pkl").exists()
    ):
        _initialize_model(processor, model, device)
    else:
        with open(Path(ROOT_PATH) / "artifacts/positive_prompt.pkl", "rb") as f:
            average_positive_vector = pickle.load(f)
        with open(Path(ROOT_PATH) / "artifacts/negative_prompt.pkl", "rb") as f:
            average_negative_vector = pickle.load(f)
    with torch.no_grad():
        inputs1 = processor(images=image, return_tensors="pt").to(device)
        image_features1 = model.get_image_features(**inputs1)
        image_vector = image_features1.numpy()
    positive_similarity = _cosine_similarity(
        average_positive_vector, np.transpose(image_vector)
    )
    negative_similarity = _cosine_similarity(
        average_negative_vector, np.transpose(image_vector)
    )
    aesthetic_score = (+1 * positive_similarity) + (-1 * negative_similarity)

    return aesthetic_score * 1000
