# https://www.datacamp.com/community/tutorials/recommender-systems-python

# Import Pandas
import pandas as pd
# Import String
import string
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

"""
Since you have used the TF-IDF vectorizer, calculating the dot product will
directly give you the cosine similarity score. Therefore, you will use
sklearn's linear_kernel() instead of cosine_similarities() since it is faster.
"""

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="cKeecl00",
  database="sys"
)

# Load Movies Metadata as a DataFrame
poems = pd.read_sql("SELECT * FROM poems", mydb)
poems = poems[['poem_id', 'title', 'author',
               'lines', 'linecount', 'wordcount']]
poems['lines'] = poems['lines'].map(lambda x: ''.join(x))
remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
poems['lines'] = poems['lines'].map(lambda x: x.translate(remove_punct_map))
# Define a TF-IDF Vectorizer Object.
# Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')
# flatten poem lines into a list of strings

# Replace NaN with an empty string
poems['lines'] = poems['lines'].fillna('')
# Construct the required TF-IDF matrix by fitting and transforming the data

tfidf_matrix = tfidf.fit_transform(poems['lines'])
# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# Construct a reverse map of indices and movie titles
indices = pd.Series(poems.index, index=poems['title']).drop_duplicates()


# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return poems['title'].iloc[movie_indices]


print(get_recommendations('The Lily'))