import json 

class Tweet():
	
	def __init__(self,i,tex,ca,rc,fc,lg,uid):
		self.id = i
		self.text = tex
		self.created_at = ca 
		self.retweet_count = rc
		self.favorite_count = fc 
		self.lang = lg 
		self.user_id = uid 
		self.mention = []
		self.label = ""
	def __str__(self):
		# on ne retourne que le text l'id et la langue 
		return "tweet_id:{} \ncontenu: {} \nlangue du tweet: {}\n".format(self.id,self.text,self.lang)

	def dump(self):
		return {'id': self.id,
				'text': self.text,
				'created_at': self.created_at,
				'retweet_count': self.retweet_count,
				'favorite_count': self.favorite_count,
				'lang': self.lang,
				'mention': self.mention,
				'label': self.label,
				'user_id': self.user_id}

class TweetEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj,Tweet):
			return [obj]
		return json.JSONEncoder.default(self,obj)
		