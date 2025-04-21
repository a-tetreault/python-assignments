import json
import psycopg2
import datetime

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
DROP TABLE IF EXISTS states CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tweets CASCADE;

CREATE TABLE IF NOT EXISTS states (
    id SERIAL PRIMARY KEY,
    name varchar(128)
);

CREATE TABLE IF NOT EXISTS users (
    id              bigint primary key,
    created_at      timestamp,
    name            varchar(128),
    screen_name     varchar(128),
    description     text,
    friends_count   int,
    followers_count int,
    statuses_count  int,
    location        varchar(128),
    url             text,
    verified        boolean
);

CREATE TABLE IF NOT EXISTS tweets (
    id                      bigint primary key,
    user_id                 bigint references users(id),
    text                    text,
    created_at              timestamp,
    retweeted               boolean,
    retweet_count           int,
    in_reply_to_status_id   bigint,
    in_reply_to_user_id     bigint,
    is_quote_status         boolean
);
""")

# Import text file: States
fname = "states.txt"
handle = open(fname)
for line in handle:
    line = line.strip()
    cur.execute("""INSERT INTO states(name) VALUES (%s)""", (line,))
    conn.commit()

# Import JSON from file: Users
file = input("Enter location: ")
if len(file) < 1:
    file = "users.json"
print("Retrieving", file)
with open(file, "r") as handle:
    line_count = 0
    for line in handle:
        line_count += 1
        line = line.strip()

        if line:
            json_data = json.loads(line)
            created_at = json_data.get("created_at", "N/A")
            if created_at != "N/A":
                if isinstance(created_at, str):
                    created_at = datetime.datetime.strptime(
                        created_at, "%a %b %d %H:%M:%S +0000 %Y"
                    )
                else:
                    created_at = datetime.datetime.fromtimestamp(created_at)
            description = json_data.get("description", "N/A")
            followers_count = json_data.get("followers_count", "N/A")
            friends_count = json_data.get("friends_count", "N/A")
            id = json_data.get("id", "N/A")
            location = json_data.get("location", "N/A")
            name = json_data.get("name", "N/A")
            screen_name = json_data.get("screen_name", "N/A")
            statuses_count = json_data.get("statuses_count", "N/A")
            entities = json_data.get("entities", {})
            url_data = json_data.get("entities", {}).get("url", {}).get("urls", {})
            url = "N/A"
            if url_data:
                url = url_data[0].get("expanded_url", "N/A")
            verified = json_data.get("verified")

            print(
                created_at,
                description,
                followers_count,
                friends_count,
                id,
                location,
                name,
                screen_name,
                statuses_count,
                url,
                verified,
            )

            cur.execute(
                """INSERT INTO users (created_at, description, followers_count, friends_count, id,
                location, name, screen_name, statuses_count, url, verified)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""",
                (
                    created_at,
                    description,
                    followers_count,
                    friends_count,
                    id,
                    location,
                    name,
                    screen_name,
                    statuses_count,
                    url,
                    verified,
                ),
            )
        conn.commit()

# Import JSON from file: Tweets
file = input("Enter location: ")
if len(file) < 1:
    file = "tweets.json"
print("Retrieving", file)
with open(file, "r") as handle:
    line_count = 0
    for line in handle:
        line_count += 1
        line = line.strip()

        if line:
            json_data = json.loads(line)
            created_at = json_data.get("created_at", "N/A")
            if created_at != "N/A":
                if isinstance(created_at, str):
                    created_at = datetime.datetime.strptime(
                        created_at, "%a %b %d %H:%M:%S +0000 %Y"
                    )
                else:
                    created_at = datetime.datetime.fromtimestamp(created_at)
            id = json_data.get("id", "N/A")
            in_reply_to_status_id = json_data.get("in_reply_to_status_id", "N/A")
            in_reply_to_user_id = json_data.get("in_reply_to_user_id", "N/A")
            is_quote_status = json_data.get("is_quote_status", "N/A")
            retweet_count = json_data.get("retweet_count", "N/A")
            retweeted = json_data.get("retweeted", "N/A")
            text = json_data.get("text", "N/A")
            user_id = json_data.get(
                "user_id",
            )

            print(
                created_at,
                id,
                in_reply_to_status_id,
                in_reply_to_user_id,
                is_quote_status,
                retweet_count,
                retweeted,
                text,
                user_id,
            )

            cur.execute(
                """INSERT INTO tweets (created_at, id, in_reply_to_status_id, in_reply_to_user_id,
                is_quote_status, retweet_count, retweeted, text, user_id)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )""",
                (
                    created_at,
                    id,
                    in_reply_to_status_id,
                    in_reply_to_user_id,
                    is_quote_status,
                    retweet_count,
                    retweeted,
                    text,
                    user_id,
                ),
            )
        conn.commit()

cur.close()
conn.close()
