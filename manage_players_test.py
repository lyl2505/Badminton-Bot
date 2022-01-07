import unittest
import manage_players
import sqlite3 as sql

class TestManagePlayers(unittest.TestCase):
    def setUp(self):
        """Setup temporary database in memory"""
        self.conn = sql.connect(":memory:")
        manage_players.init_db(self.conn)
        self.c = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_add_member(self): 
        member = (420, "Foobar", 0)
        manage_players.add_member(self.conn, member[0], member[1], member[2])
        self.c.execute("""SELECT * FROM PLAYERS WHERE id = ?""", (member[0], ))
        self.assertEqual(self.c.fetchone(), member)

        member = (421, "Foobar", 0)
        manage_players.add_member(self.conn, member[0], member[1], member[2])
        self.c.execute("""SELECT * FROM PLAYERS WHERE id = ?""", (member[0], ))
        self.assertEqual(self.c.fetchone(), member)

        member = (420, "Zabraf", 1)
        manage_players.add_member(self.conn, member[0], member[1], member[2])
        self.c.execute("""SELECT * FROM PLAYERS WHERE id = ?""", (member[0], ))
        self.assertEqual(self.c.fetchone(), member)

if __name__ == "__main__":
    unittest.main()

