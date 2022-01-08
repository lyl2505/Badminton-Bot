"""
Controller for Database operations, including updating entries and 
adding entries in both Players and CheckIn tables
"""

import sqlite3 as sql


def init_db(conn):
    """Creates Players and CheckIns tables"""


    c = conn.cursor()

    c.execute("""CREATE TABLE Players(
            id int NOT NULL, 
            username text,
            shame_list int NOT NULL,
            current_member NOT NULL,
            PRIMARY KEY (id)
        )""")
    c.execute("""CREATE TABLE CheckIns(
            id int,
            ticket_id int,
            minutes int, 
            date text,
            ticketed int,
            FOREIGN KEY (id) REFERENCES Players(id)
        )""")
    conn.commit()


def left_member(conn, id: int):
    """Sets status of member as not-in-server-anymore"""


    c = conn.cursor()
    c.execute("""UPDATE Players SET current_member = ? WHERE id = ?""", (0, id))
    conn.commit()


def add_member(conn, id: int, name: str, shamelisted: int, current_member: int = 1):
    """
    Adds a member into Players table if their id is not currently in the table.
    If their id is in the table, then their information is updated.

    :param id int: Unique id of a member
    :param name str: Username of a member
    :param shamelisted int: 0 if member isn't shame listed and 1 if member is shamed
    :raises sql.IntegrityError: If member already exists in Player table,
        then update member information instead.
    """
    

    c = conn.cursor()
    try:
        c.execute("""INSERT INTO Players VALUES(?, ?, ?, ?)""", (id, name, shamelisted, current_member))
    except sql.IntegrityError as ex:
        print(f"{ex}: {name} already exists in the database")
        update_member(conn, id, name, shamelisted)
    conn.commit()
    
def update_member(conn, id : int, name : str, shamelisted : int):
    """
    Updates both the username and if the member is shamelisted.
    
    :param id int: Unique id of a member
    :param name str: Username of a member
    :param shamelisted int: 0 if member isn't shame listed and 1 if member is shamed
    """


    c = conn.cursor()
    c.execute("""SELECT username, shame_list FROM Players WHERE id = ?""", (id, ))
    for old, new in zip(c.fetchone(), [name, shamelisted]):
        if old != new:
            print(f"{old} has been updated to {new}")
    c.execute("""UPDATE Players SET username=?, shame_list=? WHERE ID=?""", (name, shamelisted, id))
    conn.commit()

def checkin_member(conn, id: int, minutes: int, date: str, ticketed: int = 0):
    """
    Inserts an entry into CheckIns table. The entry contains it's id based on the member,
    the member id, how many minutes played, and the date played.

    :param conn Connection: Connection to the database
    :param id int: Unique id of a member
    :param minutes int: Amount of minutes a user played.
    :param date str: Formatted YYYY-MM-DD. The date played.
    """


    c = conn.cursor()
    c.execute("""SELECT MAX(ticket_id) FROM CheckIns WHERE id = ?""", (id, ))
    max_ticket_id = c.fetchone()[0]
    new_ticket_id = 0 if max_ticket_id is None else max_ticket_id + 1
    c.execute("""INSERT INTO CheckIns VALUES(?, ?, ?, ?, ?)""", 
        (id, new_ticket_id, minutes, date, ticketed))
    conn.commit()

def get_member(conn, name: str):
    """Returns id, name, and shamelist status of a member"""


    c = conn.cursor()
    c.execute("""SELECT * FROM Players WHERE username = ?""", (name, ))
    return c.fetchone()

def has_ticket(conn, name: str):
    """
    :param conn Connection: Connection to the database
    :param name str: Name of member to check if they have an active ticket
    :return True: If member has an active ticket
    :return False: IF member doesn't have an active ticket
    """


    c = conn.cursor()
    c.execute("""SELECT id FROM Players WHERE username = ?""", (name, ))
    id = c.fetchone()[0]
    c.execute("""SELECT MAX(ticketed) FROM CheckIns WHERE id = ?""", (id, ))
    return True if c.fetchone()[0] == 1 else False


if __name__ == "__main__":
    conn = sql.connect("players.db")
    init_db(conn)
