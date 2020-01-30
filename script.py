import os
import uwu
import logging
import sys
import re
import indicoio
import tweepy as tp
import simplejson as json
from datetime import datetime
from time import sleep

isRetweet = False

def readConfig():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        indico = indicoio.config.api_key = data.get('indico_key')
        auth = tp.OAuthHandler(data.get('consumer_key'), data.get('consumer_secret'))
        auth.set_access_token(data.get('access_token'), data.get('access_secret'))
        api = tp.API(auth)
        return data, api, indico

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
    sentiment = getSentimentAnalysis(only_status_text)
    return uwu.convert(only_status_text, sentiment)

def postStatus(api, data, status_id, converted):
    converted = "@realDonaldTrump " + converted
    if len(converted) > 280:
        firstStatus = api.update_status(converted[:280], in_reply_to_status_id=status_id)
        firstStatusId = firstStatus._json.get('id')
        api.update_status(converted[280:], in_reply_to_status_id=firstStatusId)
    else:
        newStatus = api.update_status(converted[:280], in_reply_to_status_id=status_id)
        newStatusId = newStatus._json.get('id')
        api.retweet(newStatusId)
    updateConfigFile(data, status_id)

def updateConfigFile(data, status_id):
    data['LAST_ID'] = status_id
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def startBot(data, api, indico):
    try:
        status_recents = getUserTimeline(api, "realDonaldTrump", data.get('LAST_ID'), 20)
        for status in reversed(status_recents):
            global isRetweet
            isRetweet = False
            status_id = status._json.get('id')
            converted = getStatusAndConvert(api, status_id)
            if not isRetweet:
                postStatus(api, data, status_id, converted)
                logging.info(str(status_id))
                logging.info(converted)
    except Exception as e:
        logging.error(e)
        pass

def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", "", tweet).split()) 

def getSentimentAnalysis(tweet):
    sentiment = indicoio.sentiment_hq(clean_tweet(tweet))
    if sentiment > .6:
        return 'positive'
    elif sentiment < .4:
        return 'negative'
    else:
        return 'neutral'

def main():
    dt = datetime.now().strftime("%m-%d")
    logging.basicConfig(filename="logs/" + dt + ".log", level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    logging.info("Script Started")
    configRes = readConfig()
    while True:
        print(uwu.convert("45th President of the United States of America", 'neutral'))
        # startBot(configRes[0], configRes[1], configRes[2])
        print(".", end="", flush=True)
        sleep(10)

if __name__ == '__main__':
    main()