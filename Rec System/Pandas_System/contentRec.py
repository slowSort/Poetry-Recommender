# https://www.datacamp.com/community/tutorials/recommender-systems-python

# Import Pandas
import pandas as pd
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

"""
Since you have used the TF-IDF vectorizer, calculating the dot product will
directly give you the cosine similarity score. Therefore, you will use
sklearn's linear_kernel() instead of cosine_similarities() since it is faster.
"""

# Load Movies Metadata as a DataFrame
metadata = pd.read_csv('./the-movies-dataset/movies_metadata.csv',
                       low_memory=False)
# Define a TF-IDF Vectorizer Object.
# Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')
# Calculate the minimum number of votes required to be in the chart, m
m = metadata['vote_count'].quantile(0.90)
# replace metadata with the 80th percentile for memory problems
metadata = metadata.copy().loc[metadata['vote_count'] >= m]
metadata = metadata.reset_index()
# Replace NaN with an empty string
metadata['overview'] = metadata['overview'].fillna('')
# Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(metadata['overview'])
print(metadata['overview'])
# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# Construct a reverse map of indices and movie titles
indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()


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
    return metadata['title'].iloc[movie_indices]


print(get_recommendations('The Dark Knight Rises'))
print(get_recommendations('The Godfather'))
