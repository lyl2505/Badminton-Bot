import unittest

from discord.ext.commands.core import check
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

    def test_add_member(self): 
        member = (420, "Foobar", 0, 1)
        manage_players.add_member(self.conn, member[0], member[1], member[2])
        self.c.execute("""SELECT * FROM PLAYERS WHERE id = ?""", (member[0], ))
        self.assertEqual(self.c.fetchone(), member)

        member = (421, "Foobar", 0, 1)
        manage_players.add_member(self.conn, member[0], member[1], member[2])
        self.c.execute("""SELECT * FROM PLAYERS WHERE id = ?""", (member[0], ))
        self.assertEqual(self.c.fetchone(), member)

        member = (420, "Zabraf", 1, 1)
        manage_players.add_member(self.conn, member[0], member[1], member[2])
        self.c.execute("""SELECT * FROM PLAYERS WHERE id = ?""", (member[0], ))
        self.assertEqual(self.c.fetchone(), member)

    def test_checkin_member(self):
        member = (420, "Foobar", 0)

        # Checkin user 1st time
        manage_players.checkin_member(self.conn, member[0], 60, "12-1-21")
        checkin_info = manage_players.get_checkin(self.conn, member[0], 0)
        self.assertEqual(checkin_info, (member[0], 0, 60, "12-1-21", 0))

        # Checkin user 2nd time
        manage_players.checkin_member(self.conn, member[0], 60, "12-1-21")
        checkin_info = manage_players.get_checkin(self.conn, member[0], 1)
        self.assertEqual(checkin_info, (member[0], 1, 60, "12-1-21", 0))

        # Checkin different user
        manage_players.checkin_member(self.conn, 421, 75, "12-2-21")
        checkin_info = manage_players.get_checkin(self.conn, 421, 0)
        self.assertEqual(checkin_info, (421, 0, 75, "12-2-21", 0))

    def test_get_member(self):
        # Get member info
        member_info = manage_players.get_member(self.conn, "Foobar")
        self.assertEqual(member_info, (421, "Foobar", 0, 1))

        # Getting non-existant member info
        member_info = manage_players.get_member(self.conn, "Kento")
        self.assertIsNone(member_info)  

    def test_has_ticket(self):
        # Check member has ticket without ticket
        ticketed = manage_players.has_ticket(self.conn, "Foobar")
        self.assertFalse(ticketed)

        # Check member has ticket with ticket
        manage_players.add_member(self.conn, 1101, "Eddie", 0)
        manage_players.checkin_member(self.conn, 1101, 60, "12-3-21", 1)
        self.c.execute("""SELECT ticketed FROM CheckIns WHERE id = ? AND ticket_id = 0""", (1101, ))
        self.assertEqual(self.c.fetchone()[0], 1)
        ticketed = manage_players.has_ticket(self.conn, "Eddie")
        self.assertTrue(ticketed)

    def test_member_left(self):
        # Check status of current member
        self.c.execute("""SELECT current_member FROM Players WHERE id = ?""", (1101, ))
        self.assertEqual(self.c.fetchone()[0], 1)

        # Current member Eddie leaves
        manage_players.left_member(self.conn, 1101)
        self.c.execute("""SELECT current_member FROM Players WHERE id = ?""", (1101, ))
        self.assertEqual(self.c.fetchone()[0], 0)

        # Get member of a member who left
        member = manage_players.get_member(self.conn, "Eddie")
        self.assertIsNone(member)

        # Checkin member who left
        self.c.execute("""SELECT MAX(ticket_id) FROM Checkins WHERE id = ?""", (1101, ))
        before_checkin = self.c.fetchone()[0]
        manage_players.checkin_member(self.conn, 1101, 5, 12-1-19)
        self.c.execute("""SELECT MAX(ticket_id) FROM Checkins WHERE id = ?""", (1101, ))
        after_checkin = self.c.fetchone()[0]
        self.assertEqual(after_checkin, before_checkin)
        



if __name__ == "__main__":
    unittest.main()

