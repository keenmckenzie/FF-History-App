from requests_oauthlib import OAuth2Session
from creds import client_id, client_secret

redirect_uri = 'https://localhost:5000/yahoo/login/redirect'

def login():
    authorization_base_url = 'https://api.login.yahoo.com/oauth2/request_auth'
    yahoo = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = yahoo.authorization_url(authorization_base_url)
    return {'authorizationLink': authorization_url}


def auth(response):
   yahoo = OAuth2Session(client_id, redirect_uri=redirect_uri)
   token_url = 'https://api.login.yahoo.com/oauth2/get_token'
   yahoo.fetch_token(token_url, client_secret=client_secret, authorization_response=response)
   return {'response': 'You\'ve been redirected'}
