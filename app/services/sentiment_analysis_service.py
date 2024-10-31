from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

def analyze_sentiment(description: str):
    if description:
        try:
            # Especificar el modelo y asegurarnos de que cargue correctamente
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=AutoModelForSequenceClassification.from_pretrained(model_name),
                tokenizer=AutoTokenizer.from_pretrained(model_name),
                revision="714eb0f"
            )
            print(f"Analyzing sentiment for description: '{description[:50]}...'")  # Registro inicial

            # Realizar el análisis de sentimiento y registrar el resultado
            result = sentiment_analyzer(description)[0]
            label = result['label']
            score = result['score']
            print(f"Sentiment Analysis Result: {result}")  # Mostrar label y score

            # Usar un umbral para establecer "NEUTRAL" si la confianza es baja
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
