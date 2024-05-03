import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as mpl

#Data Loading
Movies = pd.read_csv('movies-small/movies.csv')
Ratings = pd.read_csv('movies-small/ratings.csv')
Ratings = Ratings[['userId', 'movieId', 'rating']]
Tags = pd.read_csv('movies-small/tags.csv')
Tags = Tags[['userId', 'movieId', 'tag']]
Links = pd.read_csv('movies-small/links.csv')

#Analayzing Data
x=Ratings['userId'].value_counts()>200
y=x[x].index
Ratings=Ratings[Ratings['userId'].isin(x[x].index)]
RatedMovies=Ratings.merge(Movies , on="movieId")
MoviesRatingsN=RatedMovies.groupby("title")["rating"].count().reset_index()
MoviesRatingsN.rename(columns={"rating":"NumOfRatings"},inplace=True)
FinalDataFrame=RatedMovies.merge(MoviesRatingsN, on="title")
#print(FinalDataFrame.shape[0])
FinalDataFrame=FinalDataFrame[FinalDataFrame["NumOfRatings"]>=5]
FinalDataFrame.drop_duplicates(["userId","title"],inplace=True)
FinalDataFrame=FinalDataFrame.merge(Links , on="movieId")
print(FinalDataFrame)
#Machin Learning Shit
DataMat=FinalDataFrame.pivot_table(columns="userId",index="title",values="rating")
DataMat.fillna(0 , inplace=True)
from scipy.sparse import csr_matrix
Msparse=csr_matrix(DataMat)
from sklearn.neighbors import NearestNeighbors
model=NearestNeighbors(algorithm="brute")
model.fit(Msparse)
dis,sug=model.kneighbors(DataMat.iloc[50,:].values.reshape(1,-1),n_neighbors=6)
MoviesNames=DataMat.index



import pickle
pickle.dump(model,open("model.pkl","wb"))
pickle.dump(MoviesNames,open('MoviesName.pkl',"wb"))
pickle.dump(FinalDataFrame,open("FinalDataFrame.pkl","wb"))
pickle.dump(DataMat,open("DataMat.pkl","wb"))

def recommend_Movie(Movie_Name):
    Movie_Id=np.where(DataMat.index==Movie_Name)[0][0]
    dis,sug=model.kneighbors(DataMat.iloc[Movie_Id,:].values.reshape(1,-1),n_neighbors=6)
    for i in range(len(sug)):
        movies=DataMat.index[sug[i]]
        for j in movies:
            print(j)
    