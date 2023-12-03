# -*- coding: utf-8 -*-
"""MovieRecommender.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OMFQnbuUXdM1RGLnuqqK22ecrXCG7tyD

# **1. Import Data and Libraries**
"""

import os
import sklearn
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer
from google.colab import drive
drive.mount('/content/drive')

# to run from Beryl's laptop
movie_set = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/AI Final Project/netflix-rotten-tomatoes-metacritic-imdb.csv') # import the dataset

movie_set.head(10)

movie_set.info()

"""# 1. Data Preprocessing"""

# remove duplicate data
movie_set.drop_duplicates(inplace = True)

# drop columns with 30% or more missing data
missing_data = (movie_set.isnull().sum() / len(movie_set)) * 100 # calculate the percentage of missing data in the columns
columns_missing_data = missing_data[missing_data >= 30].index # store those with more than 30% missing data in a variable
movie_set.drop(columns = columns_missing_data, inplace = True) # drop the columns with more than 30% missing data

movie_set.info()

# grouped all columns with non-numeric values and are objects
object_streaming = movie_set.select_dtypes(exclude = ['int', 'float']).columns
object_streaming = movie_set[object_streaming]
object_streaming.info()

# imputed the non numeric values using most_frequent ie. to fill in with the most appearing
imp = SimpleImputer(strategy = 'most_frequent')
object_streaming['Tags'] = imp.fit_transform(object_streaming[['Tags']])
object_streaming['Genre'] = imp.fit_transform(object_streaming[['Genre']])
object_streaming['Languages'] = imp.fit_transform(object_streaming[['Languages']])
object_streaming['Runtime'] = imp.fit_transform(object_streaming[['Runtime']])
object_streaming['Writer'] = imp.fit_transform(object_streaming[['Writer']])
object_streaming['Actors'] = imp.fit_transform(object_streaming[['Actors']])
object_streaming['Release Date'] = imp.fit_transform(object_streaming[['Release Date']])
object_streaming['Genre'] = imp.fit_transform(object_streaming[['Genre']])
object_streaming.info()

#we will be dropping this because they will not be needed in our recommender system.Moreover, these are features that will be difficult to impute.
object_streaming.drop('IMDb Link', axis = 1, inplace = True)
object_streaming.drop('Poster', axis = 1, inplace = True)
object_streaming.drop('Tags', axis = 1, inplace = True)

object_streaming.info()

#this is to store all columns that have int or float as their datatypes
numeric_streaming = movie_set.select_dtypes(include = ['int', 'float']).columns
numeric_streaming = movie_set[numeric_streaming]
numeric_streaming.info()

# we will now impute these features using the mean method
imp = SimpleImputer(strategy = 'mean')
numeric_streaming['IMDb Score'] = imp.fit_transform(numeric_streaming[['IMDb Score']])
numeric_streaming['IMDb Votes'] = imp.fit_transform(numeric_streaming[['IMDb Votes']])
numeric_streaming['Hidden Gem Score'] = imp.fit_transform(numeric_streaming[['Hidden Gem Score']])
numeric_streaming.info()

streaming_data = pd.DataFrame()
streaming_data = pd.concat([object_streaming, numeric_streaming], axis = 1)
streaming_data.info()

streaming_data.dropna(how='any', inplace = True)
streaming_data.info()

streaming_data.to_csv('Movie_data.csv', index = False)

#this column extracts the primary gender for the gender column
streaming_data['Genre'] = streaming_data['Genre'].str.replace(r'[', '').str.replace(r"'", '').str.replace(r']', '').str.split(',').str[0]

"""# **3.Exploratory Data Analysis**"""

#Description
streaming_data.describe()

"""# **EDA on StreamingMovies**"""

#Distribution of Genre
genre_count=streaming_data['Genre'].value_counts()
plt.figure(figsize=(12,6))
genre_count.plot(kind='bar')
plt.title('Genre Distribution of Movies')
plt.xlabel('genre')
plt.ylabel('Count')
plt.show()

"""This bar chart shows us the genres which are more prevalent in the dataset. From above we can see that the comedy genre is the leading genre and has a higher popularity. This is followed by drama and action and it can also be seen that talk-shows,Adult,Reality,western,sports,etc have lesser popularity."""

import plotly.graph_objects as go

count = streaming_data['Series or Movie'].value_counts()


fig = go.Figure(data=[go.Bar(
    x=streaming_data["Series or Movie"],
    y=count,
    text=count,
    textposition='auto',

)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(
    title_text='Comparison between Movie and Series in the dataset',
    uniformtext_minsize=8, uniformtext_mode='hide',
    barmode='group', xaxis_tickangle=-45,
    yaxis=dict(title='Quantity', titlefont_size=14),
    xaxis=dict(title='Category', titlefont_size=14)
)

# Show the plot
fig.show()

#We will create a boxplot to analyze our genres
plt.figure(figsize=(16,8))
sns.boxplot(x='Genre', y='IMDb Score',data=streaming_data)
plt.title('Ratings by Genre')
plt.xlabel('Genre')
plt.ylabel('Rating')
plt.xticks(rotation=45,ha='right')#helps readability by rotating the x-axis labels
plt.show()

#Correlation HeatMap
correlation_mat=streaming_data.corr()
plt.figure(figsize=(10,8))
sns.heatmap(correlation_mat,annot=True,cmap='coolwarm',linewidths=5)
plt.title('Correlation Heatmap')
plt.show()

"""The above correlation map is what we are using to understand the relationship between the different variables in the dataset,streaming_movies. The diagonal line, red indicates a perfect correlation between the variable and itself."""

#One important aspect of the movie recommender system is the description feature. Using a word cloud helps us provide a visual representation of most occurring words which can help identify common themes in movies.
#since we will be using a content-based recommender , it will be beneficial to have a look at the most appeared words in our descriptions
wordcloud=WordCloud(width=800,height=400,background_color='white').generate(' '.join(streaming_data['Summary'].dropna()))
plt.figure(figsize=(12,6))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud For Movie Descriptions')
plt.show()

"""In word clouds the size of each word indicates the frequency. Here we can see that most visible ones are the ones with larger fonts which are find , life, family. This indicates that these are words with high frequency and the smaller words are less common in our movie descriptions.

# **4. Building the Movie Recommender System**
"""

streaming_data.info()

#import the NLTK library
import nltk
nltk.download('stopwords') # download stopwords

#we will now create a TfidfVectorizer with english words removed and we will fit and transform our movie descriptions into Tf-idf vectors
vectorizer = TfidfVectorizer(stop_words = 'english')
vectorized_streamingdata = vectorizer.fit_transform(streaming_data['Summary'])

"""More indepthly, the Tf-idf values of the words in the descriptions will be computed."""

from sklearn.metrics.pairwise import cosine_similarity

#thepourpose of the cosine similarity here is to calculate the similarity between the Tf-idf vectors in our vectorized movie dataset.
streaming_similarity = cosine_similarity(vectorized_streamingdata, vectorized_streamingdata)

"""Our resulting streaming_similarity will be used in our content-based recommendation system. This similarity matrix will be used to identify and recommend movies that are similar to a given movie."""

#We will create a variable streaming_indices which will store a panda series that will map movie titles to their indices later on in our code.
streaming_indices = pd.Series(streaming_data.index, index = streaming_data['Title'])

#This is a function that takes a movie title and returns the index of the specified movie.
def get_movie_title_index(movie, indices):
  index = indices[movie]
  if isinstance(index, np.int64):
    return index
  else:
    t = 0
    print('Select title: ')
    for i in range(len(index)):
      print(f'({i} - {streaming_data["Title"].iloc[index[i]]})', end=' ')
    rt = int(input())
    return index[t]

get_movie_title_index('The Avengers',streaming_indices)#calls the function

#this is a function that recommends similar movies to the users based on the titles inputed
def recommend_movie_titles(movie_title, indices, cosine_similarity):
    title_index = get_movie_title_index(movie_title, indices)
    if title_index is None:
        return

    print(f"Movie selected: {movie_title}")
    print("\nRecommended Movies:")

    index = indices[movie_title]
    similarity = sorted(list(enumerate(cosine_similarity[index])), key=lambda x: x[1], reverse=True)
    similarity_list = similarity[1:6]  # Exclude the input movie itself

    for i in similarity_list:
        recommended_title = streaming_data['Title'].iloc[i[0]]
        recommended_year = streaming_data['Release Date'].iloc[i[0]]
        recommended_genre = streaming_data['Genre'].iloc[i[0]]
        print(f"Title: {recommended_title} | Date: {recommended_year} | Genre: {recommended_genre}")

recommend_movie_titles('The Avengers', streaming_indices, cosine_similarity = streaming_similarity)#calls the function

"""# **5. Saving components**"""

import joblib
import gzip
import pickle

with gzip.open('cosine_similarity_matrix.joblib.gz', 'wb') as similarity:
    joblib.dump(streaming_similarity, similarity, compress=('gzip', 3)) # saving the cosine similarity

with open('indices_mapping.joblib', 'wb') as indices:
    joblib.dump(streaming_indices, indices) # saving the indices