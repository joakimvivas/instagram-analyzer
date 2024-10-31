from transformers import pipeline

# Inicializar el pipeline de análisis de sentimiento
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(description: str):
    if description:
        result = sentiment_analyzer(description)[0]
        label = result['label']
        score = result['score']
        
        # Interpretar el resultado para agregar una categoría "NEUTRAL" cuando el score sea bajo
        if score < 0.6:  # Umbral ajustable para definir "neutralidad"
            sentiment = "NEUTRAL"
        else:
            sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    
    return sentiment
