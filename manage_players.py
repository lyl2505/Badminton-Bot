import sqlite3  as sql

def init_db():
    conn = sql.connect("players.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE Players(
            id int NOT NULL, 
            username text,
            PRIMARY KEY (id)
        )""")
    c.execute("""CREATE TABLE CheckIns(
            id int NOT NULL,
            count int,
            date text,
            FOREIGN KEY (id) REFERENCES Players(id)
        )""")
    conn.commit()
    conn.close()

def add_player(id, name):
    conn = sql.connect("players.db")
    c = conn.cursor()
    

def checkin_player(id, date):
    conn = sql.connect("players.db")
    c = conn.cursor()

if __name__ == "__main__":
    init_db()