# Group9_FinalAIProject_MovieRecommender

# Movie Recommender System

Authors: Beryl Koram, Ewurama Boateng-Yeboah

## Overview

This project is a movie recommendation system that uses content based recommendation through cosine similarity to suggests movies based on user preferences and content-based analysis. The system is built using Python, Streamlit, and MySQL for database interaction.

## Project Structure

- `content-based-recommender`: Contains the content-based recommender model components and the script to load and use the recommender.
  - `content_based_recommender.pkl`: Pickled file containing the TF-IDF vectorizer, cosine similarity matrix, and indices mapping.
  - `streaming_data.pkl`: Pickled file containing the streaming data used in the recommender.

- `movieapp`: Streamlit application folder.
  - `app.py`: Main Streamlit application script.
  - `requirements.txt`: Dependencies required for the application.

## Setting Up the Recommender System

1. **Clone the Repository:**
   ```bash
   git clone [https://](https://github.com/berylkor/Group9_FinalAIProject_MovieRecommender/tree/main)https://github.com/berylkor/Group9_FinalAIProject_MovieRecommender/tree/main

2. **Install Dependencies**
   ```bash
   cd movie-recommender
   pip install -r movieapp/requirements.txt

3. **Run the Streamlit App**
    ```bash
    cd movieapp
    streamlit run app.py

## How to use 

1. Open the application in your web browser.
2. Click on a movie image to get recommendations for that movie.
3. Explore recommended movies with details such as title, release date, and genre.

## Video Demonstration of App 
https://www.youtube.com/watch?v=Z2Z3MXaofEE
