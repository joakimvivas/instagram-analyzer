from transformers import pipeline

# Inicializar el pipeline de análisis de sentimiento
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(description: str):
    if description:
        result = sentiment_analyzer(description)[0]
        label = result['label']
        score = result['score']
        
        # Log de depuración para mostrar los resultados detallados
        print(f"Sentiment Analysis - Description: {description[:50]}...")  # Primeros 50 caracteres
        print(f"Result: {result}\nLabel: {label}, Score: {score}\n")

        # Ajustar el umbral de neutralidad para pruebas
        if score < 0.4:  # Umbral más bajo para verificar resultados
            sentiment = "NEUTRAL"
        else:
            sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    
    return sentiment
