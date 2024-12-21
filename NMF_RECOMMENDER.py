import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.decomposition import NMF
import warnings
import pickle

warnings.filterwarnings("ignore")

names = ['NIM,  ExamplarCode', 'Ratings']
ratings_df = pd.read_csv('BORROW HISTORY.csv')

item_df = pd.read_csv('LIBRARY_DATABASE_with_categories_and_year.csv')
item_df = item_df[['Examplar Code', 'Book Title']]

n_users = len(ratings_df['NIM'].unique())
n_items = len(ratings_df['ExamplarCode'].unique())
R_shape = (n_users, n_items)

nim_df = ratings_df['NIM']
examplar_code = ratings_df['ExamplarCode']

counter = 0
nim_map, examplar_map = {}, {}
nim_back_map, examplar_back_map = {}, {}
for nim in nim_df.unique():
    nim_map[nim] = counter
    nim_back_map[counter] = nim
    counter += 1

counter = 1
for examplar in examplar_code.unique():
    examplar_map[examplar] = counter
    examplar_back_map[counter] = examplar
    counter += 1

nim_codex_data = {'NIM': []}
for nim in nim_df:
    nim_codex_data['NIM'].append(nim_map[nim])

examplar_codex_data = {'ExamplarCode': []}
for examplar in examplar_code:
    examplar_codex_data['ExamplarCode'].append(examplar_map[examplar])

nim_codex_df = pd.DataFrame(nim_codex_data)
examplar_codex_df = pd.DataFrame(examplar_codex_data)
rating_df = ratings_df['Rating']
ratings_df = pd.concat([nim_codex_df, examplar_codex_df, rating_df], axis=1)

item_codex_data = {'Examplar Code': [], 'Mapped Code': [], 'Book Title': []}

for _, row in item_df.iterrows():
    examplar_code = row['Examplar Code']
    book_title = row['Book Title']
    mapped_code = examplar_map.get(examplar_code, None)  # Get the mapped ID or None if not found
    # Add to the codex data
    item_codex_data['Examplar Code'].append(examplar_code)
    item_codex_data['Mapped Code'].append(mapped_code)
    item_codex_data['Book Title'].append(book_title)

item_mapped_df = pd.DataFrame(item_codex_data)

feature_X = ratings_df[['NIM', 'ExamplarCode']].values
target_Y = ratings_df['Rating'].values
X = feature_X
y = target_Y

def ConvertToDense(X, y, shape):  # from R=(X,y), in sparse format 
    row  = X[:,0]
    col  = X[:,1]
    data = y
    matrix_sparse = sparse.csr_matrix((data,(row,col)), shape=(shape[0]+1,shape[1]+1))  # sparse matrix in compressed format (CSR)
    R = matrix_sparse.todense()   # convert sparse matrix to dense matrix, same as: matrix_sparse.A
    R = R[1:,1:]                  # removing the "Python starts at 0" offset
    R = np.asarray(R)             # convert matrix object to ndarray object
    return R

R = ConvertToDense(X, y, R_shape)
# print(R)
# print(R.shape)

parametersNMF_opt = {
                    'n_components' : 10,     # number of latent factors
                    'init' : 'random', 
                    'random_state' : 0, 
                    'l1_ratio' : 1,          # set regularization = L2 
                    'max_iter' : 5
                }
estimator = NMF(**parametersNMF_opt)
                
# Training (matrix factorization)
estimator.fit(R)  
Theta = estimator.transform(R)            # user features
M = estimator.components_.T               # item features

# Making the predictions
R_pred = M.dot(Theta.T).T
                    
# Clipping values                                                    
R_pred[R_pred > 5] = 5.           # clips ratings above 5             
R_pred[R_pred < 1] = 1.           # clips ratings below 1

# Save the trained model to file
# with open('nmf_model.pkl', 'wb') as f:
#     pickle.dump(estimator, f)

def make_recommendation_activeuser(R, prediction, user_idx, k=5):
    '''
    user_idx ...... select an active user
    k  ............ number of movies to recommend
    '''
    rated_items_df_user = pd.DataFrame(R).iloc[user_idx, :]                 # get the list of actual ratings of user_idx (seen movies)
    user_prediction_df_user = pd.DataFrame(prediction).iloc[user_idx,:]     # get the list of predicted ratings of user_idx (unseen movies)
    reco_df = pd.concat([rated_items_df_user, user_prediction_df_user, item_df], axis=1)   # merge both lists with the movie's title
    reco_df.columns = ['rating','prediction','Examplar Code', 'title']

    print('Preferred movies for user #', user_idx)
    print(reco_df.sort_values(by='rating', ascending=False)[:k].to_string())           # returns the 5 seen movies with the best actual ratings
    print('Recommended movies for user #', user_idx)
    reco_df = reco_df[ reco_df['rating'] == 0 ]
    print(reco_df.sort_values(by='prediction', ascending=False)[:k].to_string())     # returns the 5 unseen movies with the best predicted ratings
    print()
    print()

make_recommendation_activeuser(R, R_pred, user_idx=7, k=10)
# make_recommendation_activeuser(R, R_pred, user_idx=10, k=5)