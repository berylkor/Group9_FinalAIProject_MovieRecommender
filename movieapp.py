'''
@authors:Beryl Koram Ayaw , Ewurama Boateng-Yeboah
'''

#import necessary libraries
import mysql.connector as mysql
import csv
import streamlit as str
import pickle
import joblib
import gzip
import zipfile



# Function to get the index of a movie title
def get_movie_title_index(movie_title, indices):
    try:
        return indices[movie_title]
    except KeyError:
        return None

# Load the content_based recommender model(which contains all our models)
with open('content_based_recommender.pkl', 'rb') as recommend:
    loaded_model_components = joblib.load(recommend)

# with open('cosine_similarity_matrix.joblib.gz', 'rb') as recommend:
#     loaded_model_components = joblib.load(recommend)

# with open('indices_mapping.joblib', 'rb') as indices:
#     loaded_indices = joblib.load(indices)

#load the pkl version of our movie dataset in order to use for our recommender system in our interface
with open('streaming_data.pkl', 'rb') as sd:
    streaming_data = joblib.load(sd)

# we unpacked these saved models from our content-based recommender model
loaded_vectorizer = loaded_model_components['tfidf_vectorizer']
loaded_similarity = loaded_model_components['cosine_similarity_matrix']
loaded_indices = loaded_model_components['indices_mapping']

# This Function will recommend using movie titles
def recommend_movie_titles(movie_title, indices, cosine_similarity, streaming_data):
    title_index = get_movie_title_index(movie_title, indices)
    if title_index is None:
        return []

    index = indices[movie_title]
    similarity = sorted(list(enumerate(cosine_similarity[index])), key=lambda x: x[1], reverse=True)
    similarity_list = similarity[1:7]  # Exclude the input movie itself

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

#this part will support streamlit in displaying the needed information for recommendation
def display_recommendations(movie_title, streaming_movies):
    # Use the loaded model to get recommendations
    recommendations = recommend_movie_titles(movie_title, loaded_indices, loaded_model_components, streaming_movies)

    # Will display recommended movies
    str.subheader("Recommended Movies:")
    for recommendation in recommendations:
        str.image(recommendation['Poster'], caption=recommendation['Title'], use_column_width=False, width = 100)
        str.write(f"**Title:** {recommendation['Title']}")
        str.write(f"**Date:** {recommendation['Date']}")
        str.write(f"**Genre:** {recommendation['Genre']}")
        str.write("---") #create breaks in between recommended movies.

#creates a connection to our database which stores necessary information for our system
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

# with zipfile.ZipFile('content_based_recommender.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
#     zipf.write('content_based_recommender.pkl', arcname='content_based_recommender.pkl')
