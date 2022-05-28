import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image

#load the image from local folder
img = Image.open('logo.png')

st.set_page_config(page_title='vitz-movie-recommendation',page_icon=img)

#to find poster of the movie through tmdb website using API
def movie_poster(movie_id):
    responce = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=cd6d3e0fc5659c70b34cb0d01bedef77&language=en-US'.format(movie_id))
    poster = responce.json()
    return "https://image.tmdb.org/t/p/w500/" + poster['poster_path']

#function to recommend the movie according to movie tittle
def recommend(movie_name):
    mvf1_index = mvf[mvf['title'] == movie_name].index[0]
    distance = similarities[mvf1_index]
    rec_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_posters=[]
    for i in rec_list:
        movie_id = mvf.iloc[i[0]].movie_id
        recommended_movies.append(mvf.iloc[i[0]].title)
        recommended_posters.append(movie_poster(movie_id))
    return recommended_movies, recommended_posters

movie_file=pickle.load(open('movies_file.pkl','rb')) #here movies_file.pkl is preprossed dataset of movies
mvf=pd.DataFrame(movie_file)

similarities=pickle.load(open('Similar_movies.pkl','rb')) #here similar_movies.pkl is file which contains vectors of all the movies in the dataset


st.title('VITZ Movie Recomender')

#search box 
movie_search=st.selectbox(
    'Search Your Movies',
    mvf['title'].values)

if st.button('Recommend'):
    movie_name,movie_pos=recommend(movie_search)

    col1, col2, col3, col4,col5 = st.columns(5)  #creating colomn for movie posters
    with col1:
        st.text(movie_name[0])
        st.image(movie_pos[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_pos[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_pos[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_pos[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_pos[4])

#To hide streamlit menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style,unsafe_allow_html=True)
