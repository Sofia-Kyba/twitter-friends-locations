import urllib.request, urllib.parse, urllib.error
import twurl_1
import json
import ssl
from flask import Flask, render_template

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def friends_information(acct):
    url = twurl_1.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '50'})
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js_ = json.loads(data)
    with open('js_.json', 'w') as f:
        json.dump(js_, f, ensure_ascii=False, indent=4)
    dict = json.dumps(js_, indent=2)
    return js_




