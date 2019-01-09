# Based on the work found at
# https://towardsdatascience.com/how-to-build-from-scratch-a-content-based-movie-recommender-with-natural-language-processing-25ad400eb243

import pandas as pd
from rake_nltk import Rake
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')

df = df[['Title', 'Genre', 'Director', 'Actors', 'Plot']]
df.head()  # this displays data, use print

# discarding the commas between the actors' full names and getting only
df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])

# putting the genres in a list of words
df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))

df['Director'] = df['Director'].map(lambda x: x.split(' '))

# merging together first and last name for each actor and director, so
# and there is no mix up between people sharing a first name
for index, row in df.iterrows():
    row['Actors'] = [x.lower().replace(' ', '') for x in row['Actors']]
    row['Director'] = ''.join(row['Director']).lower()

# initializing the new column
df['Key_words'] = ""

for index, row in df.iterrows():
    plot = row['Plot']
    # instantiating Rake, by default it uses english stopwords from NLTK
    # and discards all puntuation characters as well
    r = Rake()

    # extracting the words by passing the text
    # could change this by not extracting keywords
    r.extract_keywords_from_text(plot)

    # getting the dictionary with key words as keys and their scores as values
    key_words_dict_scores = r.get_word_degrees()

    # assigning the key words to the new column for the corresponding movie
    row['Key_words'] = list(key_words_dict_scores.keys())


print(df['Key_words'])
# dropping the Plot column
df.drop(columns=['Plot'], inplace=True)

df.set_index('Title', inplace=True)
df.head()

df['bag_of_words'] = ''
columns = df.columns
for index, row in df.iterrows():
    words = ''
    for col in columns:
        if col != 'Director':
            words = words + ' '.join(row[col]) + ' '
        else:
            words = words + row[col] + ' '
    row['bag_of_words'] = words

df.drop(columns=[col for col in df.columns if col != 'bag_of_words'],
        inplace=True)

# in the article at this point artist names and genres were cleaned and added

# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df['bag_of_words'])

# generating the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# creating a Series for the movie titles so they are associated to an ordered
# numerical list I will use in the function to match the indexes
indices = pd.Series(df.index)

#  defining the function that takes in movie title
# as input and returns the top 10 recommended movies


def recommendations(title, cosine_sim=cosine_sim):

    # initializing the empty list of recommended movies
    recommended_movies = []

    # gettin the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)

    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])

    return recommended_movies


print("Fargo:")
fargo = recommendations('Fargo')
for i in fargo:
    print(i)

print("Pulp:")
pulp = recommendations('Pulp Fiction')
for i in pulp:
    print(i)
