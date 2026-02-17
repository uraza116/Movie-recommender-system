from flask import Flask, render_template,request
import pandas as pd
import os
import numpy as np
import requests


app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

df=pd.read_pickle('./dataset/movies.pkl')
similarity=pd.read_pickle('./dataset/similarity.pkl')
movies_list=df['title'].tolist()

def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a27871bd7dd47a60c97487a4de8fe57a')
    data=response.json()
    poster_path=data.get('poster_path')
    
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    return "https://image.tmdb.org/t/p/original/"+ poster_path

    

def recommend(movie):
    
    recs=[]
    recs_poster=[]
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
        movie_id=df.iloc[i[0]].movie_id
        recs.append(df.iloc[i[0]].title)
        recs_poster.append(fetch_poster(movie_id))
    return recs,recs_poster


@app.route('/', methods=['GET', 'POST'])
def Title():
    
    selected=None
    recs=[]
    recs_poster=[]
    if request.method == "POST":
        selected = request.form.get("movie")   # name="movie" in your <select>
        #recs = recommend(str(selected))
        recs,recs_poster = recommend(selected)
    return render_template(
        "index.html",
        items=movies_list,
        selected=selected,
        recs=recs,
        recs_poster=recs_poster
    )
        


if __name__ == '__main__':
    app.run(debug=True)