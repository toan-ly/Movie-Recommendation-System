import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url =f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    respond = requests.get(url)
    data = respond.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    list_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in list_movies[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters

st.header('Movie Recommendation System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    num_recommendations = 5
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(num_recommendations)
    for i in range(num_recommendations):
      with cols[i]:
          st.text(recommended_movie_names[i])
          st.image(recommended_movie_posters[i])




