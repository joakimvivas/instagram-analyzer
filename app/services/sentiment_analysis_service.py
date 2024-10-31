from transformers import pipeline

# Inicializar el pipeline de análisis de sentimiento
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(description: str):
    if description:
        try:
            # Intento de análisis con mensaje de entrada y salida
            print(f"Executing sentiment analysis for description: {description[:50]}...")
            result = sentiment_analyzer(description)[0]
            label = result['label']
            score = result['score']

            print(f"Sentiment Analysis Result: {result}")  # Log completo
            if score < 0.4:
                sentiment = "NEUTRAL"
            else:
                sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            sentiment = "NEUTRAL"  # Asigna "NEUTRO" en caso de error
    else:
        print("No description provided; setting sentiment to NEUTRAL.")
        sentiment = "NEUTRAL"
    
    return sentiment
