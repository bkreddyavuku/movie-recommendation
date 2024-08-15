import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()

    # Check if 'poster_path' exists in the response
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder image URL

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit UI
st.title('Movie Recommender System')

option = st.selectbox(
    'Search Here',
    movies['title'].values
)

if st.button('I will Say'):
    recommended_movies, recommended_movies_posters = recommend(option)
    
    # Display the recommended movies and their posters
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movies_posters[4])
