from transformers import pipeline
import logging

logging.basicConfig(level=logging.DEBUG)
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(description: str):
    if description:
        result = sentiment_analyzer(description)[0]
        label = result['label']
        score = result['score']
        logging.debug(f"Description: {description}\nResult: {result}\nLabel: {label}, Score: {score}\n")
        if score < 0.6:
            sentiment = "NEUTRAL"
        else:
            sentiment = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    return sentiment