import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key = "9f02567388789873fc5653ae8bbc4806"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            print(f"[TMDB Error] Movie ID {movie_id} returned Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[Connection Error] {e}")
        
    return "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=500&q=80"

movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Agli Konsi Dekhu?")

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown:",
    movies['title'].values
)

if st.button("Show Recommendations"):
    index = movies[movies['title'] == selected_movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_names = []
    recommended_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_names, recommended_posters):
        with col:
            st.caption(name)
            st.image(poster, use_container_width=True)