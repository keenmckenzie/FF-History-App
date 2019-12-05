import unittest
from espn import app

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

class TestStringMethodsAgain(unittest.TestCase):
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestAppPages(unittest.TestCase):
   def setUp(self):
      self.app = app.test_client()

   def test_main_page(self):
       response = self.app.get("/leagueHistory/test", follow_redirects=True)
       self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
