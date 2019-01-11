import pandas as pd
import numpy as np
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from userProfile import get_user_profile
from decorators import timeit

"""
Since you have used the TF-IDF vectorizer, calculating the dot product will
directly give you the cosine similarity score. Therefore, you will use
sklearn's linear_kernel() instead of cosine_similarities() since it is faster.
"""


def to_similarity_matrix(feature):
    'input is an array of numbers, returns a numpy 2d matrix'
    simMatrix = []
    for x in feature:
        row = []
        for y in feature:
            # this math is quite important
            # find difference between two numbers
            # add 1 to prevent / 0 error
            # divide 1 by new number to get scaled similarity
            row.append(1/((max(x, y)-min(x, y))+1))
        simMatrix.append(row)
    return np.array(simMatrix)


# Function to convert all strings to lower case and strip names of spaces
# Hyphens separate authors, and so are replaced with spaces for many authors
def clean_author(x):
    if isinstance(x, list):
        return " ".join(x)
    else:
        return str.lower(x.replace(" ", ""))


def weight(similarity_matrix, weight=1):
    return np.multiply(similarity_matrix, weight)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="cKeecl00",
  database="sys"
)


@timeit
def recommend_user_poems():

    def get_recommendations(poem_id, similarity_matrix, recommendations=10):
        # Get the index of the movie that matches the title
        idx = indices[poem_id]
        # Get the pairwise similarity scores of all movies with that moviee
        sim_scores = list(enumerate(similarity_matrix[idx]))
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:recommendations+1]
        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
        # Return the top 10 most similar movies
        return poems['title'].iloc[movie_indices]

    # Load Movies Metadata as a DataFrame
    poems = pd.read_sql("SELECT * FROM poems", mydb)
    poems = poems[['poem_id', 'title', 'author',
                   'lines', 'linecount', 'wordcount']]
    # Load user profile for comparison and add it to poem matrix
    userProfile = get_user_profile()
    poems = poems.append(userProfile, ignore_index=True)
    # Clean fields
    poems['lines'] = poems['lines'].map(lambda x: ''.join(x))
    poems['lines'] = poems['lines'].fillna('')
    poems['author'] = poems['author'].apply(clean_author)

    # Construct the TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(poems['lines'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Construct the author matrix
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(poems['author'])
    author_sim = cosine_similarity(count_matrix, count_matrix)

    # Construct the line and word count matrices
    lines_sim = to_similarity_matrix(poems['linecount'])
    wordcount_sim = to_similarity_matrix(poems['wordcount'])

    # Create reverse map
    indices = pd.Series(poems.index, index=poems['poem_id']).drop_duplicates()

    # Average the  matrices with weights
    final_features = [weight(cosine_sim), weight(author_sim, 0.1),
                      weight(lines_sim), weight(wordcount_sim, 0.2)]
    final_sim = np.mean(np.array(final_features), axis=0)

    # Return recommendations for user 1
    return(get_recommendations(1, final_sim, 10))


print(recommend_user_poems())
