# Import Pandas
import pandas as pd
# Import mean
from statistics import mean

import mysql.connector

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)


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
