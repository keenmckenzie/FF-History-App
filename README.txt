TO RUN:

1) Create virtual environment:
$ python3 venv .venv

2) Activate virtual environment:
$ source .venv/bin/activate 

3) Install requirements:
$ pip install -r requirements.txt

4) Run:
$ python3 run.py

5) Go to localhost:5000/leagueHistory/test & localhost:5000/leagueHistory/alltime/1107328 to test


TO TEST:

1) Run:
$ coverage run -m unittest tests

2) Kill application

3) Run:
$ coverage report 
OR
$ coverage html (saved in project directory)

  
