import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="political_tweets",
    user="postgres",
    password="Maya24-Nova42",
    connect_timeout=10,
)
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS role;

CREATE TABLE IF NOT EXISTS role (
    id SERIAL PRIMARY KEY,
    role varchar(128)
);
""")

# Import text file
roles = ["President", "Governor", "Representative", "Sentator"]
for line in handle:
    line = line.strip()
    cur.execute("""INSERT INTO states(role) VALUES (%s)""", (line,))
    conn.commit()

cur.close()
conn.close()
