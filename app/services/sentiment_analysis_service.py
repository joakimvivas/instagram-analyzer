from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import transformers

# Configurar el logging de transformers para mostrar más detalles
transformers.logging.set_verbosity_debug()

def analyze_sentiment(description: str):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"

    # Cargar el modelo y tokenizador de manera explícita con el nombre y la revisión correctos
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model=AutoModelForSequenceClassification.from_pretrained(model_name, revision="714eb0f"),
        tokenizer=AutoTokenizer.from_pretrained(model_name, revision="714eb0f")
    )

    if description:
        try:
            # Registrar que se realiza el análisis
            print(f"Analyzing sentiment for: {description[:50]}...")
            result = sentiment_analyzer(description)[0]
            label = result['label']
            score = result['score']

            # Log de depuración para mostrar el resultado exacto
            print(f"Sentiment result: {result}")

            # Usar un umbral para la neutralidad
            if score < 0.6:
                sentiment = "NEUTRAL"
            else:
                sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            sentiment = "NEUTRAL"
    else:
        sentiment = "NEUTRAL"
    
    return sentiment
