import sys
from tweepy import API
from tweepy import OAuthHandler
import tweepy
import json 


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


		
