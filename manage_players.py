"""
Controller for Database operations, including updating entries and 
adding entries in both Players and CheckIn tables
"""

import sqlite3 as sql

def init_db():
    """Creates Players and CheckIns tables"""
    conn = sql.connect("players.db")
    c = conn.cursor()
    # c.execute("""CREATE TABLE Players(
    #         id int NOT NULL, 
    #         username text,
    #         shame_list int NOT NULL,
    #         PRIMARY KEY (id)
    #     )""")
    # c.execute("""CREATE TABLE CheckIns(
    #         id int NOT NULL,
    #         count int,
    #         date text,
    #         FOREIGN KEY (id) REFERENCES Players(id)
    #     )""")
    conn.commit()
    conn.close()

def add_member(id : int, name : str, shamelisted : int):
    """
    Adds a member into Players table if their id is not currently in the table.
    If their id is in the table, then their information is updated.

    :param id int: Unique id of a member
    :param name str: Username of a member
    :param shamelisted int: 0 if member isn't shame listed and 1 if member is shamed
    :raises sql.IntegrityError: If member already exists in Player table,
        then update member information instead.
    """
    conn = sql.connect("players.db")
    c = conn.cursor()
    args = (id, name, shamelisted)
    try:
        c.execute("""INSERT INTO Players VALUES(?, ?, ?)""", args)
        c.execute("""INSERT INTO CheckIns (id) VALUES(?)""", (id, ))
    except sql.IntegrityError as ex:
        print(f"{ex}: {name} already exists in the database")
    conn.commit()
    conn.close()
    update_member(id, name, shamelisted)
    
def update_member(id : int, name : str, shamelisted : int):
    """
    Updates both the username and if the member is shamelisted.
    
    :param id int: Unique id of a member
    :param name str: Username of a member
    :param shamelisted int: 0 if member isn't shame listed and 1 if member is shamed
    """
    conn = sql.connect("players.db")
    c = conn.cursor()
    c.execute("""UPDATE Players SET username=?, ShameListed=? WHERE ID=?""", (name, shamelisted, id))
    conn.commit()
    conn.close()

def checkin_member(id, date):
    # TODO
    conn = sql.connect("players.db")
    c = conn.cursor()

if __name__ == "__main__":
    # init_db()
    pass