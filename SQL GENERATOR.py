import mysql.connector
import csv

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ryuben011104#"
)
cursor = conn.cursor()

cursor.execute('DROP DATABASE IF EXISTS library_db')
cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
cursor.execute("USE library_db")

cursor.execute("""
    CREATE TABlE IF NOT EXISTS Table4 (
        AuthorID int AUTO_INCREMENT,
        BookAuthor varchar(50),
        PRIMARY KEY (AuthorID)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Table1 (
        ExamplarCode int,
        BookTitle varchar(255),
        AuthorID int,
        PRIMARY KEY (ExamplarCode),
        FOREIGN KEY (AuthorID) REFERENCES Table4(AuthorID)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Table2 (
        ExamplarCode int NOT NULL,
        BookTitle varchar(255) NOT NULL,
        BookYear year NOT NULL,
        BookCategory varchar(25) NOT NULL,
        BookStock int NOT NULL,
        FOREIGN KEY (ExamplarCode) REFERENCES Table1(ExamplarCode) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Table3 (
        ExamplarCode int NOT NULL,
        BookTitle varchar(255) NOT NULL,
        AmountBorrowed int default 0,
        AmountAvailable int NOT NULL,
        FOREIGN KEY (ExamplarCode) REFERENCES Table1(ExamplarCode) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Table5 (
        NIM varchar(100),
        Name varchar(255) NOT NULL,
        Email varchar(255) NOT NULL,
        Password varchar(25) NOT NULL,
        Mode enum("admin","user") DEFAULT "user",
        PRIMARY KEY (NIM)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Table6 (
        NIM varchar(100),
        Book_borrowed_id int,
        Rating int,
        FOREIGN KEY (NIM) REFERENCES Table5(NIM) ON DELETE CASCADE,
        FOREIGN KEY (Book_borrowed_id) REFERENCES Table1(ExamplarCode) ON DELETE CASCADE
    )
""")

csv_path = "LIBRARY_DATABASE_with_categories_and_year.csv"
with open(csv_path, mode='r') as file:
    reader = csv.DictReader(file)

    # Memasukkan data ke Table4
    for row in reader:
        cursor.execute("""
            INSERT INTO Table4 (AuthorID, BookAuthor)
            VALUES (%s, %s)
        """, (row['Author ID'], row['Author Name']))

    file.seek(0)
    next(reader)

    # Memasukkan data ke Table1
    for row in reader:
        cursor.execute("""
            INSERT INTO Table1 (ExamplarCode, BookTitle, AuthorID)
            VALUES (%s, %s, %s)
        """, (row['Examplar Code'], row['Book Title'], row['Author ID']))

    file.seek(0)
    next(reader)

    # Memasukkan data ke Table2
    for row in reader:
        cursor.execute("""
            INSERT INTO Table2 (ExamplarCode, BookTitle, BookYear, BookCategory, BookStock)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['Examplar Code'], row['Book Title'], row['BookYear'], row['Category'], row['Stock']))

    file.seek(0)
    next(reader)

    # Memasukkan data ke Table3
    for row in reader:
        cursor.execute("""
            INSERT INTO Table3 (ExamplarCode, BookTitle, AmountBorrowed, AmountAvailable)
            VALUES (%s, %s, %s, %s)
        """, (row['Examplar Code'], row['Book Title'], row['Borrowed'], row['Available']))

conn.commit()

csv_user_path = "user_data.csv"
with open(csv_user_path, mode="r") as myfile:
    reader = csv.DictReader(myfile)

    for row in reader:
        cursor.execute("""
            INSERT INTO Table5 (NIM, Name, Email, Password, Mode)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['NIM'], row['Name'], row['Email'], row['Password'], row['Mode']))

conn.commit()

csv_history_borrow_path = "BORROW HISTORY.csv"
with open(csv_history_borrow_path, "r") as myfile:
    reader = csv.DictReader(myfile)

    for row in reader:
        cursor.execute("""
            INSERT INTO Table6 (NIM, Book_borrowed_id, Rating)
            VALUES (%s, %s, %s)
        """, (row['NIM'], row['ExamplarCode'], row['Rating']))

conn.commit()

print("\nData in Table1:")
cursor.execute("SELECT * FROM Table1")
for row in cursor.fetchall():
    print(row)

print("\nData in Table2:")
cursor.execute("SELECT * FROM Table2")
for row in cursor.fetchall():
    print(row)

print("\nData in Table3:")
cursor.execute("SELECT * FROM Table3")
for row in cursor.fetchall():
    print(row)

print("\nData in Table4:")
cursor.execute("SELECT * FROM Table4")
for row in cursor.fetchall():
    print(row)

print("\nData in Table5:")
cursor.execute("SELECT * FROM Table5")
for row in cursor.fetchall():
    print(row)

print("\nData in Table6:")
cursor.execute("SELECT * FROM Table6")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
