import tweepy
import random
import requests
import json
import os

consumer_key    = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_KEY_SECRET']
access_token  = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_TOKEN_SECRET']

generator_url = os.environ['GENERATOR_URL']

character_freq = {
    "犬吠埼 風": 5001,
    "乃木 園子": 4893,
    "東郷 美森": 3695,
    "乃木 若葉": 3618,
    "結城 友奈": 3489,
    "三好 夏凜": 3485,
    "三ノ輪 銀": 3180,
    "土居 球子": 3158,
    "犬吠埼 樹": 3027,
    "上里 ひなた": 2956,
    "白鳥 歌野": 2849,
    "鷲尾 須美": 2684,
    "伊予島 杏": 2680,
    "秋原 雪花": 2598,
    "郡 千景": 2547,
    "藤森 水都": 2165,
    "楠 芽吹": 2013,
    "高嶋 友奈": 1960,
    "古波蔵 棗": 1946,
    "加賀城 雀": 1678,
    "弥勒 夕海子": 1453,
    "国土 亜耶": 1380,
    "赤嶺 友奈": 1179,
    "山伏 しずく": 917,
    "弥勒 蓮華": 699,
    "桐生 静": 616,
    "山伏 シズク": 269}

def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    api = setup_api()
    character = pickup_character()
    (character, text) = get_generated_words(character)
    status_text = "%s\n「%s」" % (character, text)
    post_tweet(api, status_text)
    update_profile_image(api, character)
    return


def setup_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, retry_count=2, retry_delay=5)
    return api


def pickup_character():
    charas  = list(character_freq.keys())
    weights = list(character_freq.values())
    return random.choices(charas, weights=weights, k=1)[0]


def get_generated_words(character):
    headers = {'content-type': 'application/json'}
    payload = {"character": character}
    response = requests.post(generator_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception("generate-words returned status_code %d" % response.status_code)
    (character, text) = json.loads(response.text)
    return (character, text)


def post_tweet(api, status_text):
    return api.update_status(status_text)


def update_profile_image(api, character):
    path = "icons/%s.png" % character
    api.update_profile_image(path)
    return
