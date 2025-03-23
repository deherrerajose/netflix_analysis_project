import pandas as pd

# Global Variables
NETFLIX_FILE = 'netflix_titles.csv'
OUTPUT_FILE = 'netflix_db.sql'
FIELDS = ['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added', 
          'release_year', 'rating', 'duration', 'listed_in', 'description']

class Show:
    def __init__(self, show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
        self.show_id = show_id
        self.type = type
        self.title = title
        self.director = director
        self.cast = cast
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.rating = rating
        self.duration = duration
        self.listed_in = listed_in
        self.description = description

# Helper Functions
def initialize_db():
    '''
    This function is used to call the initial creation queries for the 'netflix_db'. It first creates the schema,
    selects the schema for use, and finally creates the table 'shows'.
    '''
    my_sql = []

    my_sql.append(f"""
        CREATE SCHEMA netflix_db;
    """.strip())

    my_sql.append(f"""
        USE netflix_db;
    """.strip())

    my_sql.append(f"""
        CREATE TABLE IF NOT EXISTS shows (
            show_id VARCHAR(10),
            `type` VARCHAR(20),
            title VARCHAR(150),
            director VARCHAR(250),
            `cast` VARCHAR(1000),
            country VARCHAR(150),
            date_added VARCHAR(50),
            release_year INT,
            rating VARCHAR(10),
            duration VARCHAR(20),
            listed_in VARCHAR(100),
            description VARCHAR(250)
        );
    """.strip())

    return my_sql

def quote(string):
    '''
    This function is used to wrap strings in a 'single-quote' to be used by SQL.
    Example: input is "Ryan Reynolds", output is "'Ryan Reynolds'"
    '''
    safe_string = str(string).replace("'", "''")
    return f"'{safe_string}'"

def main():
    my_sql = initialize_db()

    df = pd.read_csv(NETFLIX_FILE)

    rows = df.to_dict(orient='records')
    shows = [Show(**row) for row in rows]

    for show in shows:
        my_sql.append(f"""
            INSERT INTO shows
            VALUES (
                {quote(show.show_id)}, 
                {quote(show.type)}, 
                {quote(show.title)}, 
                {quote(show.director)}, 
                {quote(show.cast)}, 
                {quote(show.country)}, 
                {quote(show.date_added)}, 
                {show.release_year}, 
                {quote(show.rating)}, 
                {quote(show.duration)}, 
                {quote(show.listed_in)}, 
                {quote(show.description)}
            ); 
        """.strip())

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write('\n'.join(my_sql))
    print("'netflix_db.sql' Created Successfully!")


if __name__ == "__main__":
    main()