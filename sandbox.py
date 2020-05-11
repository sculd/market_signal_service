from tda import auth, client
import json

token_path = '/path/to/token.pickle'
api_key = 'N3RLUXMOAU5FA16TYU1FXPEFTCSN8CQC'
redirect_uri = 'http://localhost'
try:
    c = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)

print(c)
