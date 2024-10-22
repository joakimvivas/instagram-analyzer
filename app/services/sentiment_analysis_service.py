from transformers import pipeline

# Inicializar el pipeline de análisis de sentimiento
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(description: str):
    if description:
        sentiment = sentiment_analyzer(description)[0]['label']
    else:
        sentiment = "NEUTRAL"
    return sentiment
