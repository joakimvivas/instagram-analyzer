# Instagram Account Analyzer

This project is a web application built with [FastAPI](https://fastapi.tiangolo.com/) that allows users to investigate and analyze public Instagram accounts. It retrieves the latest photos, analyzes image quality, performs sentiment analysis on the descriptions, and generates a global score based on various criteria. The analysis results, including likes, image quality, and sentiment, are stored and displayed in a simple and intuitive web interface.

![Example investigation](fcbarcelona-10-22-2024_12_38_PM.png)

### Features

- **Instagram Scraping**: Retrieves posts from public Instagram accounts using instaloader.
- **Image Quality Analysis**: Uses deep learning models to assess the quality of images.
- **Sentiment Analysis**: Analyzes the sentiment (positive, neutral, negative) of photo descriptions.
- **Global Scoring**: Combines various metrics (likes, image quality, sentiment) to generate a final score ("good" or "bad").
- **Historical Investigations**: Stores previous investigations in JSON files for easy re-access and re-analysis.
- **Progress Monitoring**: Uses server-sent events to display real-time progress during the analysis process.

### Project Structure
- **FastAPI Backend**: Manages the API, routes, and handles the analysis tasks.
- **Jinja2 Templates**: For rendering HTML pages, including the investigation form, results display, and past investigations.
- **Instaloader Integration**: Scrapes data from Instagram without needing an API key.
- **Sentiment Analysis**: Uses transformers to analyze descriptions of Instagram posts.
- **Image Quality Scoring**: Leverages torch and torchvision models to evaluate image quality on a scale of 100 points.

### Key Parts of the Project
- **Instagram Scraper**: The instaloader library is used to scrape Instagram profiles and collect post information like images, likes, and captions.
- **Image Quality Analysis**: Images are analyzed for quality using pre-trained models from torchvision, and the scores are normalized to a 0-100 scale.
- **Sentiment Analysis**: Descriptions of posts are run through a transformers pipeline to detect sentiment (positive, negative, or neutral).
- **Global Scoring**: Based on rules that combine the average likes, image quality, and sentiment analysis, each post gets a "good" or "bad" global score.
- **Storage & Retrieval**: Each investigation is saved as a JSON file under the storage directory, allowing users to revisit past investigations.
- **Real-Time Progress Updates**: The application uses SSE (Server-Sent Events) to show real-time analysis progress to the user.

### How It Works
- User enters the Instagram account and the number of photos to analyze.
- The system scrapes the latest photos, analyzes image quality, performs sentiment analysis, and calculates a global score.
- Results are displayed, showing likes, quality, sentiment, and a final score for each photo.
- Users can re-analyze old investigations or run new investigations on different accounts.

## List of main milestones and features

- [x] Implement a small form where the user enters the Instagram user (public) to start the investigation.
- [x] Using the instaloader library we will obtain information about the last 20 photos published by the user, generating a JSON file with the information (URL of the image, the number of likes, the description, hashtags and the publication date) and saving the photos in /app/storage with a unique identifier.
- [x] We will have the ability to see the result of the investigation, in the index.html we will have access to the list of old previous investigations and we will be able to see the results of each one of them.
- [x] We will have the ability to redo the investigation, in the index.html we will have access to the button to redo the investigation.
- [x] We will have the ability to see the results of a previous investigation, in the view_investigation.html we will have access to the button to return to the main page and redo the investigation.
- [x] Analyze the quality of the images with pre-trained models in Fastai, such as ResNet or EfficientNet, to detect common elements in the photos that have more "engagement" (lights, colours, compositions).
- Analysis of the description and hashtags, from the descriptions and hashtags of each post, we can apply natural language processing (NLP) to analyze:
    - [] Frequency of words and hashtags.
    - [x] Sentiment of the descriptions (positive, negative, neutral).
    - [] Keywords that appear in the most popular posts.
    - [] We will use Fastai and pre-trained models such as ULMFiT for text analysis.
- We will apply Data analysis models, such as:
    - [] Linear regression or classification models, after obtaining the data (likes, hashtags, sentiment of the descriptions, etc.), to apply a regression or classification model to find correlations between these factors and the "likes".
    - [] Clustering, grouping posts into clusters with techniques such as K-Means to discover patterns between photos with similar engagement.
- [] And more...

## Requirements and dependencies

The project relies on several **Python libraries**:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python.
- Uvicorn: ASGI server for FastAPI.
- [Jinja2 Templates](https://jinja.palletsprojects.com/en/3.0.x/): A templating engine for rendering HTML pages.
- Instaloader: A tool to scrape Instagram profiles, posts, and metadata.
- Python Multipart: Handles form data and file uploads in FastAPI.
- SSE-Starlette: Provides Server-Sent Events for real-time progress updates.
- Transformers: Hugging Face library for sentiment analysis using pre-trained language models.
- Torch: PyTorch is used for running deep learning models.
- Torchvision: Provides access to pre-trained models for image classification.
- Pillow: Python Imaging Library (PIL) fork for opening, manipulating, and saving images.

## Running the project locally (How to Run)

1. Create the Python virtual environment

```sh
python3 -m venv instagram-scraping
```

```sh
source instagram-scraping/bin/activate
```

2. Install dependencies:

It is recommended, first, upgrade pip:
```sh
pip install --upgrade pip
```

Install dependencies/requirements:
```sh
pip install -r requirements.txt
```

3. Execute the following command:

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

4. You should see an output similar to:

```
INFO:     Uvicorn running on http://127.0.0.1:3000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Licensing

All packages in this repository are open-source software and licensed under the [MIT License](https://github.com/joakimvivas/marco-bot/blob/main/LICENSE). By contributing in this repository, you agree to release your code under this license as well.

Let's build the future of **Instagram Analyzer** development together! 🤖🚀