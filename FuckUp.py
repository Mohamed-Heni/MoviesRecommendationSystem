def image_srcs(Image_srcs):
    for i in range(FinalDataFrame.shape[0]-1):
        x=FinalDataFrame.iloc[i]
        for j in range(Links.shape[0]):
            y=Links.iloc[j]
            if x["movieId"]==y["movieId"]:
                Image_srcs[i]=f"https://www.imdb.com/title/tt{y['imdbId']}/mediaviewer/rm1969689600/?ref_=tt_ov_i"
Image_srcs=[]
image_srcs(Image_srcs)
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

# ...

if st.button("Show Recommendation"):
    RecommendationM, poster = rocommendation(selectedMovie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(RecommendationM[1])
        st.image(poster[1], width=200)
    with col2:
        st.text(RecommendationM[2])
        st.image(poster[2], width=200)
    with col3:
        st.text(RecommendationM[3])
        st.image(poster[3], width=200)
    with col4:
        st.text(RecommendationM[4])
        st.image(poster[4], width=200)
    with col5:
        st.text(RecommendationM[5])
        st.image(poster[5], width=200)
