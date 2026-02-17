from flask import Flask, render_template,request
import pandas as pd
import os
import numpy as np

app = Flask(__name__)
df=pd.read_pickle('./dataset/movies.pkl')
similarity=pd.read_pickle('./dataset/similarity.pkl')


movies_list=df['title'].tolist()


def recommend(movie):
    
    recs=[]
    if not movie:
        return recs

    movie = movie.strip()
    matches = df.index[df["title"].astype(str).str.strip() == movie].tolist()
    if not matches:
        # nothing matched, return empty instead of crashing
        return recs

    
    movie_index = matches[0]
    # movie_index=df[df['title']==movie].index[0]
    movie_distance=similarity[movie_index]
    movies_list=sorted(list(enumerate(movie_distance)), reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        recs.append(df.iloc[i[0]].title)
    return recs


@app.route('/', methods=['GET', 'POST'])
def Title():
    
    selected=None
    recs=[]
    if request.method == "POST":
        selected = request.form.get("movie")   # name="movie" in your <select>
        #recs = recommend(str(selected))
        recs = recommend(selected)
    return render_template(
        "index.html",
        items=movies_list,
        selected=selected,
        recs=recs
    )
        


if __name__ == '__main__':
    app.run(debug=True)