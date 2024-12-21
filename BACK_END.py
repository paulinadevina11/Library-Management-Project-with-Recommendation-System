import mysql.connector as mc
from mysql.connector import Error
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import NMF
from scipy import sparse
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# Function to create a connection to the database
def create_connection():
    try:
        connection = mc.connect(
            host='localhost',          # Database host
            database='library_db',  # Database name
            user='root',      # Database username
            password='Ryuben011104#'   # Database password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def retrieve_user_by_filter(search_key: str = None):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    try:
        search_arr = []
        if search_key:
            search_key = f"%{search_key}%"
            cursor.execute("""
                SELECT NIM, Name, Email, Password FROM Table5
                WHERE Mode = 'user' AND Name LIKE %s
            """, [search_key])
            for row in cursor.fetchall():
                search_arr.append(row)
        else:
            cursor.execute("""
                SELECT NIM, Name, Email, Password FROM Table5
                WHERE Mode = 'user'
            """)
            for row in cursor.fetchall():
                search_arr.append(row)

        return search_arr if len(search_arr) > 0 else None

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()


def retrieve_user_history_by_filter(search_key_nim: str):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
    try:
        result_arr = []
        cursor.execute("""
            SELECT Table6.Book_borrowed_id, Table1.BookTitle, Table4.BookAuthor
            FROM Table6
            JOIN Table1 ON (Table6.Book_borrowed_id = Table1.ExamplarCode)
            JOIN Table4 ON (Table1.AuthorID = Table4.AuthorID)
            WHERE Table6.NIM = %s
            ORDER BY Table1.BookTitle ASC
        """, [search_key_nim])
        for row in cursor.fetchall():
            result_arr.append(row)

        return result_arr if len(result_arr) > 0 else None

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def create_entry_book(ExamplarCode: int, BookTitle: str, Author: str, BookYear: str, BookCategory: str, BookStock: int):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    # Check to see if the Examplar Code or the book title exists or not
    cursor.execute("""
        SELECT ExamplarCode, BookTitle FROM Table1
    """)
    examplar_arr = []
    book_title_arr = []
    for i, row in enumerate(cursor.fetchall()):
        examplar_arr.append(row[0])
        book_title_arr.append(row[1])

    if ExamplarCode in examplar_arr:
        return None, 'examplar'
    elif BookTitle in book_title_arr:
        return None, 'title'
        
    try:
        cursor.execute("""
            SELECT * FROM Table4
        """)

        AuthorID, AuthorName = None, None
        for row in cursor.fetchall():
            if row[1] == Author:
                AuthorID, AuthorName = row
                break
        
        # Do this if there is a new author
        if not AuthorName:
            cursor.execute("""
                INSERT INTO Table4(BookAuthor)
                VALUES (%s)
            """, (Author,))
            AuthorName = Author

            # Get the AuthorID
            cursor.execute("""
                SELECT AuthorID from Table4
                ORDER BY AuthorID DESC
                LIMIT 1
            """)
            for row in cursor.fetchall():
                AuthorID = row[0]
        
        # add the new data in the tables
        cursor.execute("""
            INSERT INTO Table1 (ExamplarCode, BookTitle, AuthorID)
            VALUES (%s, %s, %s)
        """, (ExamplarCode, BookTitle, AuthorID))

        cursor.execute("""
            INSERT INTO Table2 (ExamplarCode, BookTitle, BookYear, BookCategory, BookStock)
            VALUES (%s, %s, %s, %s, %s)
        """, (ExamplarCode, BookTitle, BookYear, BookCategory, BookStock))

        cursor.execute("""
            INSERT INTO Table3 (ExamplarCode, BookTitle, AmountAvailable)
            VALUES (%s, %s, %s)
        """, (ExamplarCode, BookTitle, BookStock))

        connection.commit()

        return True, ''

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def create_entry_admin_user(NIM: str, Name: str, Email: str, Password: str, Mode:str):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    # Check to see if the NIM exists or not
    cursor.execute("""
        SELECT NIM, Name, Email, Password from Table5
    """)
    for row in cursor.fetchall():
        if str(row[0]) == NIM:
            return None, 'nim'

        if str(row[1]) == Name:
            return None, 'name'
        
        if str(row[2]) == Email:
            return None, 'email'
        
        if str(row[3]) == Password:
            return None, 'password'
    
    try:
        cursor.execute("""
            INSERT INTO Table5(NIM, Name, Email, Password, Mode)
            VALUES (%s, %s, %s, %s, %s)
        """, (NIM, Name, Email, Password, Mode))

        connection.commit()

        return True, ""

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def retrieve_books(search_key: str, order_by: str = None, limit: int = None, sort: str = "ASC", filter: str = "book"):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            search_pattern = f"%{search_key}%"
            result_arr = []
            query = f"""
                    SELECT Table1.BookTitle, Table4.BookAuthor, Table1.ExamplarCode, BookYear, BookCategory, BookStock, AmountBorrowed, AmountAvailable
                    FROM Table1
                    JOIN Table2 ON (Table1.ExamplarCode = Table2.ExamplarCode)
                    JOIN Table3 ON (Table1.ExamplarCode = Table3.ExamplarCode)
                    JOIN Table4 ON (Table1.AuthorID = Table4.AuthorID)
                """
            
            if filter.lower() == 'book':
                query += f"\nWHERE Table1.BookTitle LIKE %s"

            elif filter.lower() == 'author':
                query += f"\nWHERE Table4.BookAuthor LIKE %s"
            
            if order_by:
                if order_by == "Book Title":
                    order_by = f"Table1.BookTitle"
                elif order_by == "Book Author":
                    order_by = f"Table4.BookAuthor"
                elif order_by == "Stock":
                    order_by = f"BookStock"
                else:
                    order_by = f"Table1.ExamplarCode"

                query += f"\nORDER BY {order_by} {sort}"

            if limit:
                query += f"\nLIMIT {limit}"

            cursor.execute(query, (search_pattern,))
            
            for row in cursor.fetchall():
                result_arr.append(row)

            return result_arr
        
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            connection.close()


def recommend_book(nim: str, k=10):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    cursor.execute("""
        SELECT NIM, Book_borrowed_id, Rating FROM Table6
    """)
    ratings = cursor.fetchall()

    # Check to see if the NIM exists or not
    found = False
    cursor.execute("""
        SELECT NIM FROM Table6
        WHERE NIM = %s
    """, (nim,))
    for row in cursor.fetchall():
        if row[0] == nim:
            found = True

    if not found:
        return []

    if not ratings:
        print("No borrowing history available to generate recommendations.")
        return

    # Prepare data for NMF
    df = pd.DataFrame(ratings, columns=["NIM", "ExamplarCode", "Rating"])
    le_nim = LabelEncoder()
    le_examplar = LabelEncoder()
    df["NIM"] = le_nim.fit_transform(df["NIM"])
    df["ExamplarCode"] = le_examplar.fit_transform(df["ExamplarCode"])

    X = df[["NIM", "ExamplarCode"]].values
    Y = df["Rating"].values
    R_shape = (len(df["NIM"].unique()), len(df["ExamplarCode"].unique()))

    # Convert to dense matrix
    R = ConvertToDense(X, Y, R_shape)

    # Train the NMF model
    parametersNMF_opt = {
        "n_components": 20,
        "init": "random",
        "random_state": 0,
        "l1_ratio": 0,
        "max_iter": 15
    }
    estimator = NMF(**parametersNMF_opt)
    estimator.fit(R)
    Theta = estimator.transform(R) # matrix user x weight_model_examplar_code
    M = estimator.components_.T # matrix weight_model_examplar_code x examplar_code

    # Predict ratings
    R_pred = M.dot(Theta.T).T
    R_pred[R_pred > 5] = 5.
    R_pred[R_pred < 1] = 1.

    # Generate recommendations for the user
    user_index = le_nim.transform([nim])[0]
    return make_recommendation(R, R_pred, user_index, le_examplar, k)


def make_recommendation(R, prediction, user_index, le_examplar, k):
    rated_items_df = pd.DataFrame(R).iloc[user_index, :]  # The actual ratings
    user_prediction_df = pd.DataFrame(prediction).iloc[user_index, :]  # Predicted ratings

    # Retrieve book titles and map codex to original examplar code
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ExamplarCode, BookTitle FROM Table1
        """)
        book_titles = {row[0]: row[1] for row in cursor.fetchall()}

    # Map codex back to original examplar code
    codex_to_examplar = {i: le_examplar.inverse_transform([i])[0] for i in range(len(book_titles))}

    # Combine data into DataFrame
    reco_df = pd.DataFrame({
        "Codex": range(len(rated_items_df)),
        "Rating": rated_items_df,
        "Prediction": user_prediction_df
    })
    reco_df["ExamplarCode"] = reco_df["Codex"].map(codex_to_examplar)
    reco_df["BookTitle"] = reco_df["ExamplarCode"].map(book_titles)

    recommended = reco_df[reco_df["Rating"] == 0].sort_values(by="Prediction", ascending=False)
    examplar_code_df = pd.DataFrame(recommended.index.tolist())
    recommended = recommended['BookTitle']
    book_title_df = pd.DataFrame(recommended.values.tolist())

    result_df = pd.concat([examplar_code_df, book_title_df], axis=1)
    result_df.columns = ['ExamplarCode', 'BookTitle']

    examplar_arr = result_df['ExamplarCode'].head(k).to_list()
    title_arr = result_df['BookTitle'].head(k).to_list()

    result_arr = [(examplar_arr[i], title_arr[i]) for i in range(len(title_arr)) if len(title_arr) == len(examplar_arr)]

    return result_arr


def ConvertToDense(X, Y, shape):
    row = X[:, 0]
    col = X[:, 1]
    data = Y
    matrix_sparse = sparse.csr_matrix((data, (row, col)), shape=shape)
    R = matrix_sparse.todense()
    R = np.asarray(R)
    return R


def return_book(NIM: str, Book_borrowed_code: int, rating: int):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Table6 (NIM, Book_borrowed_id, Rating)
            VALUES (%s, %s, %s)
        """, (NIM, Book_borrowed_code, rating))

        connection.commit()

        # Update the entry by one
        cursor.execute("""
            SELECT Table2.BookTitle, BookStock, AmountBorrowed, AmountAvailable
            FROM Table2
            JOIN Table3 ON (Table2.ExamplarCode = Table3.ExamplarCode)
            WHERE Table2.ExamplarCode = %s
        """, (Book_borrowed_code,))
        for row in cursor.fetchall():
            BookTitle, BookStock, AmountBorrowed, AmountAvailable = row[0], row[1], row[2], row[3]
        
        update_entry(BookTitle, BookStock, AmountAvailable + 1, AmountBorrowed - 1)

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def delete_entry(BookTitle: str):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    # Find the BookTitle
    book_title_arr = []
    cursor.execute("""
        SELECT Table1.BookTitle FROM Table1
    """)
    for row in cursor.fetchall():
        book_title = row[0]
        book_title_arr.append(book_title)

    if BookTitle not in book_title_arr:
        return None, 'title'
    
    try:
        # Find the examplar code
        cursor.execute("""
            SELECT ExamplarCode FROM Table1
            WHERE BookTitle = %s
        """, (BookTitle,))
        examplar_code = None
        for row in cursor.fetchall():
            examplar_code = row[0]

        cursor.execute("""
            DELETE
            FROM Table3
            WHERE BookTitle = %s
        """, (BookTitle,))

        cursor.execute("""
            DELETE
            FROM Table2
            WHERE BookTitle = %s
        """, (BookTitle,))

        cursor.execute("""
            DELETE
            FROM Table1
            WHERE BookTitle = %s
        """, (BookTitle,))

        cursor.execute("""
            DELETE
            FROM Table6
            WHERE Book_borrowed_id = %s
        """, (examplar_code,))

        connection.commit()

        return True, ''

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def update_entry(BookTitle: str, new_stock: int, new_available: int, new_borrowed: int):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Table2
            SET BookStock = %s
            WHERE BookTitle = %s
        """, (new_stock, BookTitle))

        cursor.execute("""
            UPDATE Table3
            SET AmountBorrowed = %s, AmountAvailable = %s
            WHERE BookTitle = %s
        """, (new_borrowed, new_available, BookTitle))

        connection.commit()
    
    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def login(username: str, password: str):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()

    login_input = (username, password)
    logged_on = False

    cursor.execute("""
        SELECT NIM, Name, Password, Mode from Table5
    """)
    for row in cursor.fetchall():
        credentials = (row[1], row[2])
        if login_input == credentials:
            return credentials, row[3].lower(), row[0] # Return (Name, Password), admin/ user, nim
        
    if not logged_on:
        return None



if __name__ == "__main__":
    #"""
        # data_storage = {(BookTitle, AuthorName): [BookTitle, AuthorName, Examplar Code, BookYear, BookCategory, BookStock, AmountBorrowed, AmountAvailable]}
        # user_storage = {NIM: [Name, Email, Password, Mode]}
    # """
    pass