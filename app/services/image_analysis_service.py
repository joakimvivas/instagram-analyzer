from transformers import AutoFeatureExtractor, AutoModelForImageClassification
import torch
from PIL import Image

def analyze_image_quality(image_path: str):
    # Inicializar el modelo de Hugging Face (por ejemplo, ResNet)
    feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/resnet-50")
    model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-50")

    # Cargar la imagen
    image = Image.open(image_path)

    # Preprocesar la imagen
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Hacer la predicción de calidad
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Obtener la etiqueta de la clase con mayor probabilidad (el índice de la clase predicha)
    predicted_label = logits.argmax(-1).item()

    # Normalizar la puntuación basada en el número de clases (en este caso, 1000 clases)
    max_quality_score = 100
    num_classes = 1000  # ResNet-50 tiene 1000 clases

    # Escalar el valor de predicted_label a una escala de 0 a 100
    normalized_score = (predicted_label / num_classes) * max_quality_score

    return round(normalized_score, 2)
