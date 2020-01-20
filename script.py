import os
import uwu
import logging
import sys
import tweepy as tp
import simplejson as json
from datetime import datetime
from time import sleep

# TODO:
# - Attach Images/Videos in tweets (?)
# - Truncated tweets should be displayed in multiple parts (1/2), (2/2), etc.

isRetweet = False

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
    if 'RT @' in full_status._json.get('full_text')[:4]:
        global isRetweet
        isRetweet = True
        return ""
    if 'retweeted_status' in full_status._json:
        only_status_text = full_status._json.get('retweeted_status').get('full_text').split(' https://')[0]
    else:
        only_status_text = full_status._json.get('full_text').split(' https://')[0]
    return uwu.convert(only_status_text)

def postStatus(api, data, status_id, converted):
    # api.update_status(converted[0:280])
    converted = "@realDonaldTrump " + converted
    if len(converted) > 280:
        firstStatus = api.update_status(converted[:280], in_reply_to_status_id=status_id)
        firstStatusId = firstStatus._json.get('id')
        api.update_status(converted[280:], in_reply_to_status_id=firstStatusId)
    else:
        api.update_status(converted[:280], in_reply_to_status_id=status_id)
    data['LAST_ID'] = status_id
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def startBot(data, api):
    try:
        status_recents = getUserTimeline(api, "realDonaldTrump", data.get('LAST_ID'), 20)
        for status in reversed(status_recents):
            global isRetweet
            isRetweet = False
            status_id = status._json.get('id')
            converted = getStatusAndConvert(api, status_id)
            if not isRetweet:
                # postStatus(api, data, status_id, converted)
                logging.info(str(status_id))
                logging.info(converted)
    except Exception as e:
        logging.error(e)
        pass

def main():
    print("Script is currently running")
    dt = datetime.now().strftime("%m-%d-%Y")
    logging.basicConfig(filename="logs/LOG_" + dt + ".log", level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    configRes = readConfig()
    while True:
        logging.info("Retrieving latest tweets from Donald Trump")
        startBot(configRes[0], configRes[1])
        sleep(30)
        print(".", end="", flush=True)

if __name__ == '__main__':
    main()