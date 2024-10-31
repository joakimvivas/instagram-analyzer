from transformers import pipeline

def analyze_sentiment(description: str):
    if description:
        try:
            # Inicializamos el pipeline con el modelo especificado en cada llamada para asegurarnos
            sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                revision="714eb0f"
            )
            print(f"Analyzing sentiment for description: '{description[:50]}...'")  # Log inicial
            result = sentiment_analyzer(description)[0]
            label = result['label']
            score = result['score']
            
            # Log detallado para confirmar el resultado
            print(f"Sentiment Analysis Result: {result}")  # Muestra label y score
            
            # Condicional para establecer "NEUTRAL" cuando la puntuación es baja
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
