#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Import Pandas
import pandas as pd
# Import Numpy
import numpy as np
# Import Itertools
import itertools
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

"""
Since you have used the TF-IDF vectorizer, calculating the dot product will
directly give you the cosine similarity score. Therefore, you will use
sklearn's linear_kernel() instead of cosine_similarities() since it is faster.
"""

import mysql.connector

np.set_printoptions(threshold=np.inf)

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
poems['lines'].head()

# Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')
# flatten poem lines into a list of strings

# Replace NaN with an empty string
poems['lines'] = poems['lines'].fillna('')
# Construct the required TF-IDF matrix by fitting and transforming the data

tfidf_matrix = tfidf.fit_transform(poems['lines'])

# Compute the cosine similarity matrix
# Linear kernel used as it's faster
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# Construct a reverse map of indices and movie titles
indices = pd.Series(poems.index, index=poems['poem_id']).drop_duplicates()


# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(poem_id, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[poem_id]
    # Get the pairwsie similarity scores of all movies with that moviee
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return poems['title'].iloc[movie_indices]


# print(get_recommendations(102))


# Function to convert all strings to lower case and strip names of spaces
def clean_author(x):
    return str.lower(x.replace(" ", ""))


poems['author'] = poems['author'].apply(clean_author)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(poems['author'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

poems = poems.reset_index()
indices = pd.Series(poems.index, index=poems['poem_id']).drop_duplicates()

# Downweight author significance in vectorizer
cosine_sim2 = np.multiply(cosine_sim2, 0.1)
# print(cosine_sim2)
# Average the two cosine similarities
final_sim = np.mean(np.array([cosine_sim, cosine_sim2]), axis=0)


# In[46]:


print(cosine_sim[2])


# In[7]:


print(cosine_sim2[0])


# In[4]:


print(final_sim[0])


# In[8]:


print(get_recommendations(102, cosine_sim))


# In[9]:


print(get_recommendations(102, cosine_sim2))


# In[10]:


print(get_recommendations(102, final_sim))


# In[53]:


simMatrix = []
for x in poems['linecount']:
    row = []
    for y in poems['linecount']:
        # this math is quite important
        # find difference between two numbers
        # add 1 to prevent / 0 error
        # divide 1 by new number to get scaled similarity
        row.append(1/((max(x, y)-min(x, y))+1))
    simMatrix.append(row)
lines_sim = np.array(simMatrix)
print(lines_sim[2])


# In[55]:


print(get_recommendations(107, lines_sim))


# In[ ]:




