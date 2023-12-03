'''
@authors:Beryl Koram Ayaw , Ewurama Boateng-Yeboah
'''

#import necessary libraries
import mysql.connector as mysql
import csv
import streamlit as str
import pickle
import joblib

# Function to get the index of a movie title
def get_movie_title_index(movie_title, indices):
    try:
        return indices[movie_title]
    except KeyError:
        return None

# Load the content_based recommender file (which contains all our components)
with open('content_based_recommender.pkl', 'rb') as recommend:
    loaded_model_components = joblib.load(recommend)

with open('streaming_data.pkl', 'rb') as sd:
    streaming_data = joblib.load(sd)

# we unpacked these saved components from our content-based recommender file
loaded_vectorizer = loaded_model_components['tfidf_vectorizer']
loaded_similarity = loaded_model_components['cosine_similarity_matrix']
loaded_indices = loaded_model_components['indices_mapping']

# This function to recommend movie titles
def recommend_movie_titles(movie_title, indices, cosine_similarity, streaming_data):
    title_index = get_movie_title_index(movie_title, indices)
    if title_index is None:
        return []

    index = indices[movie_title]
    similarity = sorted(list(enumerate(cosine_similarity[index])), key=lambda x: x[1], reverse=True)
    similarity_list = similarity[1:7]  # Exclude the input movie itself and then recommends the most similar six

    recommendations = []
    for i in similarity_list:
        recommended_title = streaming_data['Title'].iloc[i[0]]
        recommended_date = streaming_data['Release Date'].iloc[i[0]]
        recommended_genre = streaming_data['Genre'].iloc[i[0]]
        recommended_poster = streaming_data['Image'].iloc[i[0]]
        recommendation_info = {
            'Poster': recommended_poster,
            'Title': recommended_title,
            'Date': recommended_date,
            'Genre': recommended_genre
        }
        recommendations.append(recommendation_info)

    return recommendations
# This part will support streamlit in displaying the needed information for recommendation
def display_recommendations(movie_title, streaming_movies):
    # Use the loaded components to get recommendations
    recommendations = recommend_movie_titles(movie_title, loaded_indices, loaded_similarity, streaming_movies)

    # Will display recommendations
    str.subheader("Recommended Movies:")
    for recommendation in recommendations:
        str.image(recommendation['Poster'], caption=recommendation['Title'], use_column_width=False, width = 100)
        str.write(f"**Title:** {recommendation['Title']}")
        str.write(f"**Date:** {recommendation['Date']}")
        str.write(f"**Genre:** {recommendation['Genre']}")
        str.write("---")

# establishes a connection to our database which stores movie information for our system
movie_db = mysql.connect(host='127.0.0.1', user='root', password='beryl123', database ='movie', auth_plugin='mysql_native_password')
cursor = movie_db.cursor()

def main(cursor, streaming_movies):
    str.title("E & B Recommendation System")

   
    cursor.execute('SELECT title, image  FROM movie')
    image_data = cursor.fetchall()

    # This displays images representing movies and get recommendations when an image is clicked
    for title, image in image_data:
            movie_image = str.image(image, caption = title, output_format = 'JPEG')

            # Get recommendations when an image is clicked
            if str.button(f"Get Recommendations for {title}", key=title):
                display_recommendations(title, streaming_data)

if __name__ == '__main__':
    main(cursor, streaming_data)

if cursor:
    cursor.close()