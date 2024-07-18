import torch
from transformers import AutoTokenizer, CLIPModel
from PIL import Image
import requests


### this is the code that requires a token from the owner of christophschuhmann/improved-aesthetic-predictor


# Load the aesthetic predictor model and processor
model = CLIPModel.from_pretrained("christophschuhmann/improved-aesthetic-predictor")
processor = AutoTokenizer.from_pretrained("christophschuhmann/improved-aesthetic-predictor")

# Example image path
img_path = "C:\Users\User\OneDrive\Desktop\from-0-to-AI-3Sides\data_sample\example1.jpg"
pil_image = Image.open(requests.get(img_path, stream=True).raw)

# Preprocess the image
inputs = processor(images=pil_image, return_tensors="pt")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

with torch.no_grad():
    inputs = {k: v.to(device) for k, v in inputs.items()}
    image_features = model.get_image_features(**inputs)

    # Assuming the output is directly the aesthetic score
    aesthetic_score = image_features.cpu().detach().numpy().flatten()

print("Aesthetic score predicted by the model:")
print(aesthetic_score)
