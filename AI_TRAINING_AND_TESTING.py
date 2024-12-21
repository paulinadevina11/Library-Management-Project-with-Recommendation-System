import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import time, math
from sklearn.preprocessing import scale
from scipy import sparse
from sklearn.decomposition import NMF
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import ShuffleSplit
import warnings

warnings.filterwarnings("ignore")


read_file_df = pd.read_csv("BORROW HISTORY.csv")

describe_rate = read_file_df["Rating"].describe()
print(describe_rate)

read_file_df["Rating"].hist(grid=True)
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.title("Distribution of ratings")
# plt.show()

le_nim = LabelEncoder()
le_examplar = LabelEncoder()

read_file_df["NIM"] = le_nim.fit_transform(read_file_df["NIM"])
read_file_df["ExamplarCode"] = le_examplar.fit_transform(read_file_df["ExamplarCode"])

X = read_file_df[["NIM", "ExamplarCode"]].values
Y = read_file_df["Rating"].values

n_NIM = len(read_file_df["NIM"].unique())
n_ExamplarCode = len(read_file_df["ExamplarCode"].unique())
R_shape = (n_NIM, n_ExamplarCode)

def preprocess_data(filename):
    df = pd.read_csv(filename)
    describe_rate = df["Rating"].describe()
    print(describe_rate)

    df["Rating"].hist(grid=True)
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title("Distribution of ratings")
    plt.show()

    le_nim = LabelEncoder()
    le_examplar = LabelEncoder()

    df["NIM"] = le_nim.fit_transform(df["NIM"])
    df["ExamplarCode"] = le_examplar.fit_transform(df["ExamplarCode"])
    return df

def ConvertToDense(X, Y, shape):
    row = X[:, 0]
    col = X[:, 1]
    data = Y
    matrix_sparse = sparse.csr_matrix((data, (row, col)), shape=shape)
    R = matrix_sparse.todense()
    R = np.asarray(R)
    return R

R = ConvertToDense(X, Y, R_shape)
sparsity_of_R = len(R.nonzero()[0]) / float(R.shape[0] * R.shape[1])
print("Dense Matrix R:")
print(R)
print("Shape of R:", R.shape)
print(sparsity_of_R)

nmf_model = NMF(n_components=20)
nmf_model.fit(R)
Theta = nmf_model.transform(R)
M = nmf_model.components_.T

R_prediction = M.dot(Theta.T)
R_prediction = R_prediction.T

print("Item features - M: ", M.shape)
print("User features - Theta: ", Theta.shape)
print()
print("R - M * Theta.T: ")
print(R_prediction.round(2))
print(R_prediction.shape)
print(f"-------------------")

#HYPERPARAMETER TUNING with NMF

#Load the data set
def GetShape(filename):
    names = ["NIM", "ExamplarCode", "Rating"]
    df = pd.read_csv(filename)
    n_NIM = len(df["NIM"].unique())
    n_ExamplarCode = len(df["ExamplarCode"].unique())
    return(n_NIM, n_ExamplarCode)

def Load_Data(filename):
    names = ["NIM", "ExamplarCode", "Rating"]
    df = pd.read_csv(filename)
    le_nim = LabelEncoder()
    le_examplar = LabelEncoder()

    df["NIM"] = le_nim.fit_transform(df["NIM"])
    df["ExamplarCode"] = le_examplar.fit_transform(df["ExamplarCode"])

    X = df[["NIM", "ExamplarCode"]].values
    Y = df["Rating"].values
    R_shape = GetShape(filename)
    R = ConvertToDense(X, Y, R_shape)
    return X, Y, R, R_shape

filename = "BORROW HISTORY.csv"
X, Y, R, R_shape = Load_Data(filename)

# Sparsity calculation
sparsity_of_R = 1.0 - (len(R.nonzero()[0]) / float(R_shape[0] * R_shape[1]))
print("Dense Matrix R:")
print(R)
print("Shape of R:", R.shape)
print("Sparsity of R:", sparsity_of_R)

# NMF decomposition
nmf_model = NMF(n_components=20, init="random", random_state=42)
nmf_model.fit(R)
Theta = nmf_model.transform(R)
M = nmf_model.components_

# Matrix reconstruction
R_prediction = Theta.dot(M)
print("Item features - M: ", M.shape)
print("User features - Theta: ", Theta.shape)
print()
print("R_prediction (rounded):")
print(R_prediction.round(2))
print("Shape of R_prediction:", R_prediction.shape)

#SPLIT INTO TRAINING AND TEST SET
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.33)

R_train = ConvertToDense(X_train, Y_train, R_shape)
R_test = ConvertToDense(X_test, Y_test, R_shape)

print("R train")
print(R_train)
print(R_train.shape)
print()
print("R_test")
print(R_test)
print(R_test.shape)


#Choosing Model
parametersNMF = {
                "n_components" : 20,
                "init" : "random",
                "random_state" : 0,
                # "alpha" : 0.01,
                "l1_ratio" : 0,
                "max_iter" : 100
                }

estimator = NMF(**parametersNMF)

def get_rmse(pred, actual):
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return np.sqrt(mean_squared_error(pred, actual))

kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Initialize error tracking
err = 0
n_iter = 0.
n_splits_count = 5
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]

    R_train = ConvertToDense(X_train, Y_train, R_shape)
    R_test = ConvertToDense(X_test, Y_test, R_shape)

    t0 = time.time()
    estimator.fit(R_train)
    Theta = estimator.transform(R_train)
    M = estimator.components_.T
    print("Fit in %0.3fs" % (time.time() - t0))
    n_iter += estimator.n_iter_

    R_pred = M.dot(Theta.T)
    R_pred = R_pred.T

    R_pred[R_pred > 5] = 5.
    R_pred[R_pred < 1] = 1.

    err += get_rmse(R_pred, R_test)
    print(get_rmse(R_pred, R_test))

print("*** RMSE Error: ", err / n_splits_count)
print("Mean number of iterations: ", n_iter /n_splits_count)

cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=42)

for train_index, test_index in cv.split(X, Y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = Y[train_index], Y[test_index]
param = {
        "n_components" : [15, 20, 25],
        "l1_ratio" : [0],
        "max_iter" : [15, 20, 25]
}


# Number of grid search iterations (3^3 combinations)
n_iterations = len(param["n_components"]) * len(param["l1_ratio"]) * len(param["max_iter"])

# Initialize grid_search with the correct number of rows (n_iterations)
grid_search = pd.DataFrame(np.zeros((n_iterations, 4)), columns=["n_components", "l1_ratio", "max_iter", "RMSE"])

grid_search.columns = ["n_components", "l1_ratio", "max_iter", "RMSE"]


n_folds = 25
i = 0

for n_components in param["n_components"]:
    for l1_ratio in param["l1_ratio"]:
        for max_iter_num in param["max_iter"]:

            err = 0
            n_iter = 0
            print("Search", i, "/", 3 ** 3 - 1)
            for train_index, test_index in cv.split(X, Y):
                # Use the original X and Y for indexing
                X_train_cv, X_test_cv = X[train_index], X[test_index]
                Y_train_cv, Y_test_cv = Y[train_index], Y[test_index]

                R_train = ConvertToDense(X_train_cv, Y_train_cv, R_shape)
                R_test = ConvertToDense(X_test_cv, Y_test_cv, R_shape)

                parametersNMF = {
                    "n_components": n_components,
                    "init": "random",
                    "random_state": 0,
                    "l1_ratio": l1_ratio,
                    "max_iter": max_iter_num}
                estimator = NMF(**parametersNMF)

                t0 = time.time()
                estimator.fit(R_train)
                Theta = estimator.transform(R_train)
                M = estimator.components_.T
                n_iter += estimator.n_iter_

                R_pred = M.dot(Theta.T).T
                R_pred[R_pred > 5] = 5.
                R_pred[R_pred < 1] = 1.

                err += get_rmse(R_pred, R_test)

            grid_search.loc[i] = [n_components, l1_ratio, max_iter_num, err / n_folds]
            print(grid_search.loc[i].tolist(), "Mean number of iterations: ", n_iter / n_folds)
            i += 1

best_params = grid_search.sort_values("RMSE")[:1]
print("*** best params ***")
print(best_params)

parametersNMF_opt = {
        "n_components" : 20,
        "init" : "random",
        "random_state" : 0,
        "l1_ratio" : 0,
        "max_iter" : 15
}

estimator = NMF(**parametersNMF_opt)
estimator.fit(R_train)
Theta = estimator.transform(R_train)
M = estimator.components_.T

R_pred = M.dot(Theta.T).T
R_pred[R_pred > 5] = 5.
R_pred[R_pred < 1] = 1.

print("RMSE test: ", get_rmse(R_pred, R_train))

estimator = NMF(**parametersNMF_opt)
estimator.fit(R)
Theta = estimator.transform(R)
M = estimator.components_.T

R_pred = M.dot(Theta.T).T
R_pred[R_pred > 5] = 5.
R_pred[R_pred < 1] = 1.

print(R)

#Making Item Recommendations
read_file_df = read_file_df['ExamplarCode']
def make_recommendation(R, prediction, user_index, k=5):
    if user_index >= R.shape[0]:
        print(f"Invalid user_index: {user_index}. It must be between 0 and {R.shape[0] - 1}.")
        return

    rated_items_df = pd.DataFrame(R).iloc[user_index, :] # The actual ratings
    user_prediction_df = pd.DataFrame(prediction).iloc[user_index, :] # Simpan predicted ratings
    reco_df = pd.concat([rated_items_df, user_prediction_df, read_file_df], axis= 1)
    reco_df.columns = ["Rating", "prediction", "ExamplarCode"]

    print("Shape of reco_df:", reco_df.shape)

    if reco_df.shape[1] != 3:  # Ensure reco_df has exactly 3 columns
        print(f"Error: reco_df has {reco_df.shape[1]} columns but expected 3.")
        return

    print("Preffered books for user #", user_index)
    print(reco_df.sort_values(by="Rating", ascending= False)[:k])
    print("Recommended books for user #", user_index)
    reco_df = reco_df[reco_df["Rating"] == 0]
    print(reco_df.sort_values(by="prediction", ascending = False)[:k])
    print()
    print()

make_recommendation(R, R_pred, 2, k=5)
