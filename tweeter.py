import sys
import uwu
import tweepy as tp

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

class DonaldTweetListener(tp.StreamListener):
    def __init__(self, api):
        self.api = api
    def on_status(self, status):
        if from_creator(status):
            try:
                converted = uwu.convert(status.text)
                postStatus(self.api, converted)
                return True
            except BaseException as e:
                print("Error on_data %s" % str(e))
            return True
        return True
    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True
    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True

def postStatus(api, converted):
    if len(converted) > 280:
        firstStatus = api.update_status(converted[:280])
        firstStatusId = firstStatus._json.get('id')
        api.update_status(converted[280:], in_reply_to_status_id=firstStatusId)
    else:
        newStatus = api.update_status(converted[:280])
        newStatusId = newStatus._json.get('id')
        api.retweet(newStatusId)