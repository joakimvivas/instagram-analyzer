from transformers import pipeline

# Inicializa el pipeline especificando tanto el modelo como la revisión
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"  # Confirmamos la revisión exacta del modelo
)

def analyze_sentiment(description: str):
    if description:
        try:
            print(f"Analyzing sentiment for description: '{description[:50]}...'")  # Registro inicial
            result = sentiment_analyzer(description)[0]
            label = result['label']
            score = result['score']
            
            # Registro detallado para confirmar resultados del análisis
            print(f"Sentiment Analysis Result: {result}")  # Muestra label y score
            
            if score < 0.4:
                sentiment = "NEUTRAL"
            else:
                sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            sentiment = "NEUTRAL"
    else:
        print("No description provided; setting sentiment to NEUTRAL.")
        sentiment = "NEUTRAL"
    
    return sentiment
