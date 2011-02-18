#!/usr/bin/env python

import sys
import tweepy
import cfg

#print 'consumer_key:', cfg.keys.consumer_key
#print 'consumer_secret:', cfg.keys.consumer_secret
#print 'access_key:', cfg.keys.access_key
#print 'access_secret:', cfg.keys.access_secret

auth = tweepy.OAuthHandler(cfg.keys.consumer_key, cfg.keys.consumer_secret)
auth.set_access_token(cfg.keys.access_key, cfg.keys.access_secret)
api = tweepy.API(auth)
print api.update_status(sys.argv[1])
