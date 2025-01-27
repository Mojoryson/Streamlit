import sqlite3


# Connection to database
conenction = sqlite3.connect("/Users/rmorrison/Projects/Streamlit/sql_lite/db/movie.db")
cursor = conenction.cursor()


# Create the movies table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")
conenction.commit()

while True:
    choice = input(
        "Enter your choice: Press A to add a new record, Press V to view all records, Press D to delete a record, Press U to update a record, Press Q to quit: \n"
    )
    choice = choice.upper()

    if choice == "A":
        name = input("Please enter the name of a movie: \n")

        data = [name]
        cursor.execute("INSERT INTO `movies` (`name`) VALUES (?)", data)
        conenction.commit()

    elif choice == "U":
        id = input("Please enter the ID of the record you want to update: \n")
        name = input("Please enter the new name of a movie: \n")
        
        data = [name, id]
        cursor.execute("UPDATE `movies` SET `name` = ? WHERE `id` = ?", data)
        conenction.commit()

    elif choice == "D":
        id = input("Please enter the ID of the record you want to delete: \n")
        
        data = [id]
        cursor.execute("DELETE FROM `movies` WHERE `id` = ?", data)
        conenction.commit()

    elif choice == "V":
        print("Here are all the records: \n")
        
        result = cursor.execute("SELECT * FROM `movies`")
        movies = result.fetchall()
        for movie in movies:
            print(f"ID: {str(movie[0])} NAME: {movie[1]}")
            
    elif choice == "Q":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
        continue
