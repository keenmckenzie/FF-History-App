Application to pull historical fantasy football league data from the espn fantasy football API

To RUN:

1) Create virtual environment:
$ python3 venv .venv

2) Activate virtual environment:
$ source .venv/bin/activate 

3) Install requirements:
$ pip install -r requirements.txt

4) Run:
$ python3 run.py

5) Go to https://localhost:5000/espn/home


TO TEST:

1) Run:
$ coverage run -m unittest tests

2) Kill application

3) Run:
$ coverage report 
OR
$ coverage html (saved in project directory)

  
