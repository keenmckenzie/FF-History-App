import unittest
from espn import app

class TestAppPages(unittest.TestCase):
   def setUp(self):
      self.app = app.test_client()

   def test_leagueHistory_page(self):
       response = self.app.get("/leagueHistory/test", follow_redirects=True)
       self.assertEqual(response.status_code, 200)
   
   def test_owners_page(self):
       response = self.app.get("/leagueHistory/owners/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)
   
   def test_records(self):
       response = self.app.get("/leagueHistory/records/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_years(self):
       response = self.app.get("/leagueHistory/years/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_alltime(self):
       response = self.app.get("/leagueHistory/alltime/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_year(self):
       response = self.app.get("/leagueHistory/season/1107328/2018", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
