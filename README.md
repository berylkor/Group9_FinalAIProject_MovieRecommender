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
   git clone https://
