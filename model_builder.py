# %%
import numpy as np
import pandas as pd
import ast

# %%
movies=pd.read_csv("./dataset/tmdb_5000_movies.csv")
credits=pd.read_csv("./dataset/tmdb_5000_credits.csv")

# %%
# merging both dataset

df=movies.merge(credits,on="title")

# %% [markdown]
# ## EDA ##

# %% [markdown]
# ### Remove unnecessary columns ###

# %%
df=df[["movie_id","title","overview","genres","keywords","cast","crew"]]

# %%
df.dropna(inplace=True)

# %%
df.isna().sum()

# %%
df["genres"][0]

# %%
def convert(obj):
    L_genre=[]
    for i in ast.literal_eval(obj):
        L_genre.append(i["name"])
    return L_genre

# %%
def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i["name"])
            break
    return L

# %%
df["genres"]=df["genres"].apply(convert)

# %%
df["keywords"]=df["keywords"].apply(convert)

# %%
df["cast"]=df["cast"].apply(convert).apply(lambda x:x[:3])

# %%
df["crew"]=df["crew"].apply(fetch_director)

# %%
df["overview"]=df["overview"].apply(lambda x:x.split())

# %% [markdown]
# Removing spaces between the names to avoid confusion for recommender systems
# 
# For example
# 
# Sam Mendes -> SamMendis
# Sam Worthington ->SamWorthington
# 
# otherwise system gets confused which sam are we looking for

# %%
def remove_spaces(obj):
    return obj.apply(lambda x:[i.replace(" ","") for i in x])

# %%
df["genres"]=remove_spaces(df["genres"])
df["keywords"]=remove_spaces(df["keywords"])
df["cast"]=remove_spaces(df["cast"])
df["crew"]=remove_spaces(df["crew"])

# %%
df["tags"]=df["overview"]+df["genres"]+df["keywords"]+df["cast"]+df["crew"]

# %%
df=df[["movie_id","title","tags"]]

# %%
df["tags"]=df["tags"].apply(lambda x:" ".join(x))

# %%
df["tags"]=df["tags"].apply(lambda x:x.lower())

# %%
df["tags"][0]

# %% [markdown]
# we have converted tags now. 
# to find similiarity between movies, we find similiarty between tags
# 
# convert tags to vector using bag of words and perform vectorization without stop words
# 
# 

# %% [markdown]
# ## Vectorization ##

# %%
from sklearn.feature_extraction.text import TfidfVectorizer


tfidf = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1,2), min_df=2)
vectors = tfidf.fit_transform(df["tags"])



# %% [markdown]
# ## Stemming ##

# %% [markdown]
# We do stemming now to avoid words like (action actions), (love loved loving) to be counted as different.

# %%
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

# %%
def stem(txt):
    y=[]
    for i in txt.split():
        y.append(ps.stem(i))
    return " ".join(y)

# %%
df["tags"]=df["tags"].apply(stem)

# %%
from sklearn.metrics.pairwise import cosine_similarity

# %%
similarity=cosine_similarity(vectors)

# %%
def recommend(movie):
    #get index of movie
    
    movie_index=df[df['title']==movie].index[0]
    movie_distance=similarity[movie_index]
    movies_list=sorted(list(enumerate(movie_distance)), reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(df.iloc[i[0]].title)

# %%
import pickle

# %%
pickle.dump(df,open('./dataset/movies.pkl','wb'))

# %%
pickle.dump(similarity,open('./dataset/similarity.pkl','wb'))


