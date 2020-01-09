from requests_oauthlib import OAuth2Session

def login():
   client_id = 'insert client id'
   authorization_base_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
   yahoo = OAuth2Session(client_id)
   authorization_url, state = yahoo.authorization_url(authorization_base_url)
   return {'authorizationLink': authorization_url}
