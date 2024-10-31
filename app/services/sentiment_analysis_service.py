from transformers import pipeline

# Inicializar el pipeline de análisis de sentimiento con un modelo explícito
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(description: str):
    if description:
        try:
            print(f"Analyzing sentiment for description: '{description[:50]}...'")
            result = sentiment_analyzer(description)[0]
            label = result['label']
            score = result['score']
            
            # Registro detallado para confirmar resultados del análisis
            print(f"Sentiment Analysis Result: {result}")
            
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
