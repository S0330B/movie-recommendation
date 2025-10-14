import streamlit as st
import pickle
import bz2
import pandas as pd
import requests
import os

st.title("🎬 Movie Recommendation System")

movies = pickle.load(open('model/movies.pkl', 'rb'))
with bz2.BZ2File('model/similarity.pbz2', 'rb') as f:
    similarity = pickle.load(f)
movie_list = movies['title'].values

def fetch_poster(movie_id):
    api_key = "946d58132484899786a4802671506951"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
   

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list_sorted:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

selected_movie = st.selectbox("Type or select a movie:", movie_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
