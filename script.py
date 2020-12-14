import auth
import tweeter
import tweepy as tp

def main():
    # auth.getAccessTokens(tp)
    api = auth.getApi(tp)
    streaming_api = tp.streaming.Stream(api.auth, tweeter.DonaldTweetListener(api), timeout=60)
    streaming_api.filter(follow=['25073877'])

if __name__ == '__main__':
    main()