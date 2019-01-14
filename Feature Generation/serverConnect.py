from createFeatures import poemsShorterOrEqualTo, json, findWordCount

import mysql.connector

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

poems = poemsShorterOrEqualTo(6)

mycursor = mydb.cursor()
for poem in poems:
    sql = "INSERT INTO poems (title, author, `lines`, linecount, wordcount) VALUES (%s, %s, %s, %s, %s)"
    val = (poem['title'], poem['author'],
           json.dumps(poem["lines"]), poem['linecount'], findWordCount(poem))
    # sql = "INSERT INTO poems (`lines`) VALUES (%s)"
    # val = (json.dumps(poem["lines"]),)
    mycursor.execute(sql, val)

mydb.commit()
