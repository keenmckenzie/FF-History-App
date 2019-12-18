import unittest
from espn import app

class TestRegularSeasonPages(unittest.TestCase):
   def setUp(self):
      self.app = app.test_client()

   def test_leagueHistory_page(self):
       response = self.app.get("/regularSeason/test", follow_redirects=True)
       self.assertEqual(response.status_code, 200)
   
   def test_owners_page(self):
       response = self.app.get("/regularSeason/owners/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)
   
   def test_records(self):
       response = self.app.get("/regularSeason/records/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_years(self):
       response = self.app.get("/regularSeason/years/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_year(self):
       response = self.app.get("/regularSeason/season/1107328/2018", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_performance(self):
       response = self.app.get("/regularSeason/performance/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

   def test_records(self):
       response = self.app.get("/regularSeason/records/1107328", follow_redirects=True)
       self.assertEqual(response.status_code, 200)


class TestPostSeasonPages(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_page(self):
        response = self.app.get("/postseason/test", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_performance(self):
        response = self.app.get('postseason/performance/1107328', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class TestAllTimePages(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_performance(self):
        response = self.app.get("/alltime/performance/1107328", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
