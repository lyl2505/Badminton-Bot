import unittest
import manage_players
import sqlite3 as sql

class TestManagePlayers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup temporary database in memory"""
        cls.conn = sql.connect(":memory:")
        manage_players.init_db(cls.conn)
        cls.c = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_member_management(self): 
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

        # Checkin user 1st time
        manage_players.checkin_member(self.conn, member[0], 60, "12-1-21")
        self.c.execute("""SELECT * FROM CheckIns WHERE id = ? AND ticket_id = ?""",
            (member[0], 0))
        self.assertEqual(self.c.fetchone(), (member[0], 0, 60, "12-1-21"))

        # Checkin user 2nd time
        manage_players.checkin_member(self.conn, member[0], 60, "12-1-21")
        self.c.execute("""SELECT * FROM CheckIns WHERE id = ? AND ticket_id = ?""",
            (member[0], 1))
        self.assertEqual(self.c.fetchone(), (member[0], 1, 60, "12-1-21"))

        # Checkin different user
        manage_players.checkin_member(self.conn, 421, 75, "12-2-21")
        self.c.execute("""SELECT * FROM CheckIns WHERE id = ? AND ticket_id = ?""",
            (421, 0))
        self.assertEqual(self.c.fetchone(), (421, 0, 75, "12-2-21"))

        # Get member info
        member_info = manage_players.get_member(self.conn, "Foobar")
        self.assertEqual(member_info, (421, "Foobar", 0,))

        # Getting non-existant member info
        member_info = manage_players.get_member(self.conn, "Kento")
        self.assertIsNone(member_info)


if __name__ == "__main__":
    unittest.main()

