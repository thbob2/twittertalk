import sys
from tweepy import API
from tweepy import OAuthHandler
import tweepy
import json 
#consumer_key = "WouN94K3npYkZDHVpHGQDOwyl"
#consumer_secret = "RQyYPzLRXOA5QMs5OnVP91wAYB4dSnTAd2X5dKXvIr4NKkWY3F"
#access_token = "295286840-5yd7qcXg1WfZplnrb78UYE2CKY1N1MZlLZdsMSSZ"
#access_secret = "E8QWRogAahyutRgdhsqcAdAhrHonzJtF8JLcPpBxylTu5"

#decorateur de la class sigleton 
"""def singleton(defined_class):
		instances = {}
		def get_instance(*arg,**kwargs):
			 if defined_class not in instances:
			 	instances[defined_class] = defined_class(*arg, **kwargs)
			 return instances[defined_class]
		return get_instance
@singleton"""
class TwitterAgent():
	
	def __init__(self,consumer_key,consumer_secret,access_token,access_secret):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token = access_token
		self.access_secret = access_secret
		self.api = self.get_twitter_client()
	def get_twitter_auth(self):
		auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_secret)
		return auth

	def get_twitter_client(self):

		auth = self.get_twitter_auth()
		client = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		return client

	def get_twitter_Oauth(self):
		oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
		return oauth

if __name__ == '__main__':
	consumer_key = "WouN94K3npYkZDHVpHGQDOwyl"
	consumer_secret = "RQyYPzLRXOA5QMs5OnVP91wAYB4dSnTAd2X5dKXvIr4NKkWY3F"
	access_token = "295286840-5yd7qcXg1WfZplnrb78UYE2CKY1N1MZlLZdsMSSZ"
	access_secret = "E8QWRogAahyutRgdhsqcAdAhrHonzJtF8JLcPpBxylTu5"
# Authentification grace à la fonction authentif
	agent = TwitterAgent(consumer_key,consumer_secret,access_token,access_secret)
	twitter = agent.api.me()
	print(twitter)
		
