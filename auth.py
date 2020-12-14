import os
from dotenv import load_dotenv

load_dotenv()

def getAccessTokens(tp):
    auth = tp.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET_KEY"))
    try:
        redirect_url = auth.get_authorization_url()
        print(redirect_url)
    except tp.TweepError:
        print('Error! Failed to get request token.')
    verifier = input('Verifier:')
    try:
        auth.get_access_token(verifier)
    except tp.TweepError:
        print('Error! Failed to get access token.')
    print(auth.access_token)
    print(auth.access_token_secret)

def getApi(tp):
    auth = tp.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET_KEY"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tp.API(auth)
    return api