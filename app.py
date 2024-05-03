import pickle 
import streamlit as st 
import numpy as np

st.header("Project 3 Movie Recommender System Using ML")


model=pickle.load(open("artifacts/model.pkl","rb"))
DataMat=pickle.load(open("artifacts/DataMat.pkl","rb"))
MoviesNames=pickle.load(open("artifacts/MoviesName.pkl","rb"))
FinalDataFrame=pickle.load(open("artifacts/FinalDataFrame.pkl","rb"))

def fetch_link(sug):
    MName=[]
    MIndex=[]
    MLinks=[]
    
    for MId in sug:
        MName.append(DataMat.index[MId])
    for name in MName[0]:
        ids=np.where(FinalDataFrame["title"]==name)[0][0]
        MIndex.append(ids)
    print(FinalDataFrame)
    for idx in MIndex:
        imd=FinalDataFrame.iloc[idx]['imdbId']
        MLinks.append(f"https://whatismymovie.com/item?item={imd}")
    return MLinks

def rocommendation(Movie_Name):
    Movie_List = []
    Poster_Links = []
    Movie_Id = np.where(DataMat.index == Movie_Name)[0][0]
    dis, sug = model.kneighbors(DataMat.iloc[Movie_Id,:].values.reshape(1, -1), n_neighbors=6)
    poster_links = fetch_link(sug)

    for i in range(len(sug)):
        Ms = DataMat.index[sug[i]]
        for j in Ms:
            Movie_List.append(j)
            print(j)
    
    return Movie_List, poster_links
selectedMovie=st.selectbox("Select Your Favorit Movie",MoviesNames)

if st.button("Show Recommendation"):
    RecommendationM, poster = rocommendation(selectedMovie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.link_button(f"{RecommendationM[1]}",poster[1])
    with col2:
        st.link_button(f"{RecommendationM[2]}",poster[2])
    with col3:
        st.link_button(f"{RecommendationM[3]}",poster[3])
    with col4:
        st.link_button(f"{RecommendationM[4]}",poster[4])
    with col5:
        st.link_button(f"{RecommendationM[5]}",poster[5])