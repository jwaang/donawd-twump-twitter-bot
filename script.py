import os
import uwu
import logging
import sys
import tweepy as tp
import simplejson as json
from time import sleep
from datetime import datetime

# TODO:
# - Attach Images/Videos in tweets
# - Truncated tweets should be displayed in multiple parts (1/2), (2/2), etc.
# - Users that are @'d should not have thier names converted
# - Make sure Error 503 is being caught properly

def readConfig():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        auth = tp.OAuthHandler(data.get('consumer_key'), data.get('consumer_secret'))
        auth.set_access_token(data.get('access_token'), data.get('access_secret'))
        api = tp.API(auth)
        return data, api

def getUserTimeline(api, username, last_id, c):
    return api.user_timeline(username, since_id=last_id, count=c)

def getStatusAndConvert(api, status_id):
    full_status = api.get_status(status_id, tweet_mode='extended')
    if 'retweeted_status' in full_status._json:
        only_status_text = full_status._json.get('retweeted_status').get('full_text').split(' https://')[0]
    else:
        only_status_text = full_status._json.get('full_text').split(' https://')[0]
    return uwu.convert(only_status_text)[0:280]

def postStatus(api, data, status_id, converted):
    api.update_status(converted)
    data['LAST_ID'] = status_id
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def startBot(data, api):
    try:
        status_recents = getUserTimeline(api, "realDonaldTrump", data.get('LAST_ID'), 20)
        for status in reversed(status_recents):
            status_id = status._json.get('id')
            converted = getStatusAndConvert(api, status_id)
            postStatus(api, data, status_id, converted)
            logging.info(str(status_id))
            logging.info(converted + "\n")
    except tp.error.TweepError as e:
        if e.reason[0]['code'] == "503":
            print('1 Error 503 Caught')
            logging.info('1 tweep error caught')
    except tp.TweepError as e:
        if e.reason[0]['code'] == "503":
            print('2 Error 503 Caught')
            logging.info('2 tweep error caught')
    except tp.TweepError:
        print('3 tweep error caught')
        logging.info('3 tweep error caught')

def main():
    print("Script is currently running")
    logging.basicConfig(filename="updates.log", level=logging.INFO)
    configRes = readConfig()
    while True:
        now = datetime.now()
        logging.info("Retrieving latest tweets from Donald Trump at: " + now.strftime("%m/%d/%Y, %H:%M:%S"))
        logging.info("===================================================================")
        startBot(configRes[0], configRes[1])
        sleep(300)
        print(".", end="", flush=True)

if __name__ == '__main__':
    main()