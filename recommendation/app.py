import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open("movie_dict.pkl",'rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie recommender system")
def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    movies_list= sorted(list(enumerate(similarity[movie_index])),reverse=True, key=lambda x:x[1])[1:6]
    recommended =[]
    recommended_movie_posters = []

    for i in movies_list:
         id = movies.iloc[i[0]].id
         recommended_movie_posters.append(fetch_poster(id))
         recommended.append(movies.iloc[i[0]].title)
    return recommended,recommended_movie_posters

option = st.selectbox(
'Choose a movie',
movies['title'].values)

st.write('You selected:', option)

if st.button('Recommend'):
    recommended,recommended_movie_posters =recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended[4])
        st.image(recommended_movie_posters[4])