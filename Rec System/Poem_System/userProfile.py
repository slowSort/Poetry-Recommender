# Import Pandas
import pandas as pd
# Import Numpy
import numpy as np
# Import mean
from statistics import mean
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

import mysql.connector

np.set_printoptions(threshold=np.inf)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="cKeecl00",
  database="sys"
)


def clean_author(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        return str.lower(x.replace(" ", ""))


def get_user_profile():
    likedPoems = pd.read_sql("""
    SELECT p.poem_id, title, author, p.lines, linecount, wordcount
    FROM poems as p
    INNER JOIN poems_users as pu
        ON p.poem_id = pu.poem_id
    WHERE pu.opinion = 1
    """, mydb)

    userProfile = {}
    userProfile['poem_id'] = 1
    userProfile['title'] = 'USER_PROFILE'
    userProfile['author'] = [i for i in likedPoems['author']]
    userProfile['lines'] = [i for i in likedPoems['lines']]
    userProfile['linecount'] = mean(likedPoems['linecount'])
    userProfile['wordcount'] = mean(likedPoems['wordcount'])
    return userProfile
