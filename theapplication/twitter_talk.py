#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle
from textblob import *
from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
from PyQt5.QtWidgets import QLabel
import datetime as dt
from tweepy import API
from tweepy import OAuthHandler
import tweepy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import regex as re
from os import listdir
from os.path import isfile, join
import os 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import matplotlib.style as mplstyle
import traceback, sys
from samples import *
import pandas as pd 
import numpy as np
import socket
from owlready2 import  *
from neo4j.v1 import *
import signal
import subprocess
import time
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

class Searcher(object):    
############################################################
#methode called within the class to return the names of the ontology classes 
    def ontology_classesNames(self,onto):
        ontol=get_ontology(onto).load()
        objects=ontol.classes()
        names_list=[]
        for obj in objects: 
            tuple=str(obj).split('.')
            name=tuple[1]
            if("_" in name):
                tuple1=name.split("_")
                name=" ".join(tuple1)
            names_list.append(name)
        return list(set(names_list))
#method that elague a tweet file 
    def elaguerFichier(self,ontology,file):
        classesNames = self.ontology_classesNames(ontology)
        Tweets=[]
        with open(file,"r",encoding="utf-8") as f:
            data=json.load(f)
        for tweet in data["tweets"]:
            for name in classesNames:
                if (re.search(r'\b{}\b'.format(name.lower()),tweet["text"]) or re.search(r'\b{}\b'.format(name.upper()),tweet["text"]) or re.search(r'\b{}\b'.format(name),tweet["text"])!=None):
                    tempo=Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"])
                    Tweets.append(tempo)
        with open(file,"w",encoding="utf-8") as f:
            string = json.dumps({'tweets':[o.dump() for o in Tweets]},indent=4)
            f.write(string)
        f.close()
        return file
#methode that elague a cursur of tweets
    def elaguerCursor(self,ontology,AllTweets): 
        classesNames=self.ontology_classesNames(ontology)
        cpt=1
        errorCpt=0
        file = open('cache/file.json','w',encoding="utf-8")  
        Tweets=[] 
        for page in AllTweets:
            for tweet in page:
                for name in classesNames:
                    if (re.search(r'\b{}\b'.format(name.lower()),tweet.text) or re.search(r'\b{}\b'.format(name.upper()),tweet.text) or re.search(r'\b{}\b'.format(name),tweet.text)!=None):
                                tempo = Tweet(tweet.id,tweet.text,str(tweet.created_at),tweet.retweet_count,tweet.favorite_count,tweet.lang,tweet.user.id)
                                Tweets.append(tempo)
                                if(cpt%100==0):
                                     #state.setText("tweet number "+str(cpt)+" downloaded")
                                    pass                            
                                cpt+=1
                                break
        string=json.dumps({'tweets':[o.dump() for o in Tweets]},indent=4)
        file.write(string)
        file.close()
        #state.setText("Tweets have been filtered and loaded in a file")
        return 'cache/file.json'
#methode that etiquete the elagued tweet file
    def etiqueter(self,file,ontology):
        classesNames = self.ontology_classesNames(ontology)
        file1=open(file,'r',encoding="utf-8")
        data=json.load(file1)
        file2=open('cache/etiquetted.json','w',encoding="utf-8")
        Tempos=[]
        cpt=1
        for tweet in data["tweets"]: 
            tempo=Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"])
            for name in classesNames:
                if (re.search(r'\b{}\b'.format(name.lower()),tweet["text"]) or re.search(r'\b{}\b'.format(name.upper()),tweet["text"]) or re.search(r'\b{}\b'.format(name),tweet["text"])!=None):
                    tempo.mention.append(name)
                    #state.setText("Tweet number {} etiquetted".format(cpt))
                    cpt+=1
            if(len(tempo.mention)!=0) : Tempos.append(tempo)
            #state.setText("Tweet number {} etiquetted".format(cpt))
            cpt+=1
        string=json.dumps({'tweets':[o.dump() for o in Tempos]},indent=4)  
        file2.write(string)      
        file1.close()
        file2.close()
        #state.setText("Le corpus a été étiqueter")
        return 'cache/etiquetted.json'
#methode that clean the tweet file from urls and '#'
    def cleanTweets(self,file):
        with open(file,"r",encoding="utf-8") as f1:
            data=json.load(f1)
        f1.close()
        tweets=[]
        text=""
        for tweet in data["tweets"]:
            text=re.sub("(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|((http[s]?:\/\/)?(www[\.])?\S+[\.]\S{2,3})","",tweet["text"])
            tempo=Tweet(tweet["id"],text,str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"])
            tempo.mention=tweet["mention"]
            tweets.append(tempo)
        string=json.dumps({'tweets':[o.dump() for o in tweets]},indent=4)
        with open("cache/cleanedTweets.json","w",encoding="utf-8") as f2:
            f2.write(string)
        f2.close()
        #state.setText("The corpus has been cleaned")
        return "cache/cleanedTweets.json"      
#methode that print a tweet text form a file                       
    def afficherTweets(self,file):
        #Affiche un fichier json
        with open(file,"r",encoding="utf-8") as file: 
            data=json.load(file)
            for tweet in data["tweets"]:
                print(tweet["text"])
        file.close()
##Getting tweets using key words in a forme of a cursor
    def searchCle(self,mot_cle,api): 
        Alltweets=tweepy.Cursor(api.search,q=mot_cle,lang="en",wait_on_rate_limit=True, wait_on_rate_limit_notify=True,count=200).pages(100)    
        return Alltweets
# methode that extract tweet that talk about a model
    def extractModel(self,model,file,path):
        tweets = []
        with open(file,'r',encoding="utf-8") as f: 
            data = json.load(f)
        for tweet in data['tweets']:
            if ((re.search(r'\b{}\b'.format(model.lower()),tweet["text"]) or re.search(r'\b{}\b'.format(model.upper()),tweet["text"]) or re.search(r'\b{}\b'.format(model),tweet["text"]))!=None):
                tempo = Tweet(tweet['id'],tweet['text'],tweet['created_at'],tweet['retweet_count'],tweet['favorite_count'],tweet['lang'],tweet['user_id'])
                tweets.append(tempo)
        with open(path,'w',encoding='utf-8') as w:
            string = json.dumps({'tweets':[o.dump() for o in tweets]},indent=4)
            w.write(string)
        return path
#methode that extract all the tweets talking about a model from the main corpus
    def fullExtraction(self,model,path):
        pathc = os.getcwd()+"/corp/"
        Tweets = []
        corp = [f for f in listdir(pathc)]
        for file in corp:
            with open(pathc+file,'r',encoding="utf-8") as read:
                data = json.load(read)
            for tweet in data["tweets"]:
                if ((re.search(r'\b{}\b'.format(model.lower()),tweet["text"]) or re.search(r'\b{}\b'.format(model.upper()),tweet["text"]) or re.search(r'\b{}\b'.format(model),tweet["text"]))!=None):
                    tempo=Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"])
                    Tweets.append(tempo)
            #print(" we re done with {}".format(file))
        with open(path,'w',encoding="utf-8") as w:
            string = json.dumps({'tweets':[t.dump() for t in Tweets]},indent=4)
            w.write(string)
        w.close()
        return path
############################
    def MainCorpExtraction(self,api,ontology,since,until,lab):
        start = since.strftime('%Y-%m-%d')
        end = until.strftime('%Y-%m-%d')
        dayDate = (until - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        Alltweets=tweepy.Cursor(api.search,q="samsung OR SAMSUNG",
                lang="en",wait_on_rate_limit=True, wait_on_rate_limit_notify=True,since=start,until=end,count=200).pages()

        cpt=1
        Tweets=[]
        phoneNames=[]
        
        with open("docs/samsung_smartphones.txt","r",encoding="utf-8") as file1:
            for line in file1:
                phoneNames.append(line.strip())
        file1.close() 
        for page in Alltweets:
            for tweet in page:
                for name in phoneNames:
                    if (re.search(r'\b{}\b'.format(name.lower()),tweet.text) or re.search(r'\b{}\b'.format(name.upper()),tweet.text) or re.search(r'\b{}\b'.format(name),tweet.text)!=None):
                        tempo = Tweet(tweet.id,tweet.text,str(tweet.created_at),tweet.retweet_count,tweet.favorite_count,tweet.lang,tweet.user.id)
                        if(cpt%100==0):
                            #print(tweet.text)
                            #print("Tweet number {} downloaded,time: {}".format(cpt,str(tempo.created_at))) # on la garde pour l'instant
                            lab.setText("Tweet number {} downloaded,time: {}".format(cpt,str(tempo.created_at))) # on la garde pour l'instant
                        lastDate=str(tempo.created_at)[:10]
                        if(lastDate!=dayDate):
                            newf ="corp/CorpusPrincipal_{}.json".format(dayDate)
                            with open(newf,"w",encoding="utf-8") as file2:
                                string=json.dumps({'tweets':[o.dump() for o in Tweets]},indent=4)
                                file2.write(string)
                                self.elaguerFichier(ontology,newf)
                                Tweets=[]
                                dayDate=lastDate
                        Tweets.append(tempo)
                        cpt+=1
                        break

class Analyser():
 ##a methode that return the score of a given text
    @classmethod
    def feeling(cls,text):
        result = TextBlob(text)           
        if(result.sentiment[0]>0): 
            return "pos".format(result.sentiment[0])
        elif(result.sentiment[0]==0): 
            return"nutral".format(result.sentiment[0])
        else: 
            return "neg".format(result.sentiment[0])
        return result.sentiment[0]

#Cette fonction note les tweets du fichier donné en entré en utilisant la fonction feeling(text)
    def analizeFile(self,file):
        with open(file,"r",encoding="utf-8") as f:
            data=json.load(f)
        f.close()
        cpt=1                                    
        Tweets=[]
        for tweet in data["tweets"]:
            tempo=Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"])
            tempo.mention=tweet["mention"]
            tempo.label=self.feeling(tweet["text"])
            Tweets.append(tempo)
            #state.setText("tweet number {} has been analyzed".format(cpt))
            cpt+=1
        string=json.dumps({'tweets':[o.dump() for o in Tweets]},indent=4)
        with open(file,"w",encoding="utf-8") as f:
            f.write(string)
        f.close()
        #state.setText("L'analyse des sentiments à été effectuée")
        return file
#Cette fonction calcule le pourcentage de positivié et de négativité pour chaque mention

    def negativityAndPositivity(self,file,ontology,searcher):
        list_mentionsBis=[]
        mention={}
        
        onto=searcher.ontology_classesNames(ontology)
        for name in onto:
            mention["name"]=name                        
            mention["pos"]=0
            mention["neg"]=0
            mention["pourNeg"]=0
            mention["pourPos"]=0
            list_mentionsBis.append(mention)
            mention={}
        list_mentions=[]
        for v1 in list_mentionsBis:
            if v1 not in list_mentions:
                list_mentions.append(v1)
        
        #loading the file already labeled with "pos" and 'neg'
        with open(file,"r",encoding="utf-8") as f:
            data=json.load(f)         
        f.close()
        
        for tweet in data["tweets"]:
            for element in list_mentions:
                if(element["name"] in tweet["mention"]):
                    if(tweet["label"]=="pos"): element["pos"]+=1
                    if(tweet["label"]=="neg"): element["neg"]+=1 
                    
        with open("cache/results","wb") as f:
            mon_pickler=pickle.Pickler(f)
            
            for m in list_mentions:
                somme=m["neg"]+m["pos"]
                if(somme!=0):
                    m["pourNeg"]=round((m["neg"]/somme)*100,2)
                    m["pourPos"]=round((m["pos"]/somme)*100,2)
                #print("concept : {} , positivity : {} % , negativy : {} %".format(m["name"],m["pourPos"],m["pourNeg"]))
            mon_pickler.dump(list_mentions)
        f.close()
        #state.setText("Les résultats ont été sauvegardés")
        
        with open("cache/results","rb") as f:
            mon_pickler=pickle.Unpickler(f)
            list1=mon_pickler.load()
            
        with open("docs/smar.json","r",encoding="utf-8") as f:
             list2=json.load(f)
        for l in list1:
            for l1 in list2["concepts"]:
                if(l["name"]==l1["name"]):
                    l1["pourPos"]=l["pourPos"]
                    l1["pourNeg"]=l["pourNeg"]
                    l1["pos"]=l["pos"]
                    l1["neg"]=l["neg"]
                    break
        with open("docs/smar.json","w",encoding="utf-8") as f:
             string=json.dumps({"concepts":[o for o in list2["concepts"]]},indent=4)
             f.write(string)
#########################################################################################################################################################################################################
    
    def influenceRec(self,concept,data):
        actuel={}
        for d in data["concepts"]:
            if d["name"]==concept:
                actuel=d
                break
        if(actuel["subClasses"]==[]):
            actuel["influenced"]=True
            return(actuel["pourPos"],actuel["pourNeg"],data["concepts"])
        else:
            sommeNeg=0
            sommePos=0
            for concept in actuel["subClasses"]:
                re=self.influenceRec(concept,data)
                sommeNeg+=re[1]
                sommePos+=re[0]
            if(sommePos!=0): actuel["pourPos"]=(actuel["pourPos"]+(sommePos/len(actuel["subClasses"])))/2
            if(sommeNeg!=0): actuel["pourNeg"]=(actuel["pourNeg"]+(sommeNeg/len(actuel["subClasses"])))/2
            actuel["influenced"]=True
            return(actuel["pourPos"],actuel["pourNeg"],data["concepts"])
#########################################################################################################################################################################################################
    def influenceResults(self,file):
        with open(file,"r",encoding="utf-8") as f:
            data=json.load(f)
        results=self.influenceRec("Smartphone",data)
#########################################################""
# naive bayes felling analyser 
    def feelingBayes(self,text):
        result = TextBlob(text,analyzer=NaiveBayesAnalyzer())
        return result.sentiment[0]
# calculating the polarity of tweets usin naiveBayes
    def analizeFileBayes(self,file):
        with open(file,"r",encoding='utf-8') as f : 
            data = json.load(f)
        f.close()
        cpt = 1
        tweets = [] 
        for tweet in data['tweets']:
            tempo=Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"])
            tempo.mention=tweet["mention"]
            tempo.label=self.feelingBayes(tweet["text"])
            tweets.append(tempo)
            #print("Tweet number {} has been analysed, time = {} ".format(cpt,dt.datetime.today().strftime('%H:%M:%S')))
            cpt+=1
        string = json.dumps({"tweets":[o.dump() for o in tweets]},indent=4)
        with open(file,"w",encoding="utf-8") as f :
            f.write(string)
        f.close()
        #print("DONE")
        return file

def singleton(defined_class):
		instances = {}
		def get_instance(*arg,**kwargs):
			 if defined_class not in instances:
			 	instances[defined_class] = defined_class(*arg, **kwargs)
			 return instances[defined_class]
		return get_instance
@singleton
class Neo4j(object):
	def __init__(self, uri, user, password):
		try:
			self._driver = GraphDatabase.driver(uri, auth=(user, password), trust=TRUST_ALL_CERTIFICATES)
		except ServiceUnavailable: 
			root = os.getcwd().replace("\\","/")
			s = root+"/neo4j-community-3.3.2/bin/neo4j.bat console>"+root+"/docs/logs.txt"
			self.server = subprocess.Popen(s,
				stdout=subprocess.PIPE,shell=True)
			time.sleep(60)
			self._driver = GraphDatabase.driver(uri, auth=(user, password), trust=TRUST_ALL_CERTIFICATES)
		except Exception as e:
			time.sleep(15)

	##################################################		
	#  les methodes d'ecriture dans la base de donnée#
	##################################################

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	@classmethod
	def detach(cls,tx):
		tx.run("match(n) detach delete(n)")
	def delete_all(self):
		print("supperssion du contenu de la base")
		try:
			with self._driver.session() as d:
				d.write_transaction(self.detach)
				print("supperssion effectuer ")
		except :
			print("une érreur est parevenue ")
		finally: 
			print(" opération effectuer ")

#################################################################################################
#methode de gestion de compte utilisateur
	@classmethod
	def tx_cuser(cls,tx,uname,pwd,ck,cs,act,acs):
		tx.run("merge(u:User{name: $uname,pwd: $pwd, consumer_key: $ck,"
			"consumer_secret: $cs,access_token: $act,access_secret: $acs})",uname=uname,pwd=pwd,ck=ck,cs=cs,act=act,acs=acs)
	def createUser(self,uname,pwd,ck,cs,act,acs):
		with self._driver.session() as w:
			w.write_transaction(self.tx_cuser,uname,pwd,ck,cs,act,acs)
	@classmethod
	def tx_loaduser(cls,tx,uname):
		result = tx.run("match(u:User{name: $uname}) " 
						"return u.name,u.pwd,u.consumer_key,u.consumer_secret,u.access_token,u.access_secret ",uname=uname)
		user = dict()
		for record in result:
			user["name"] = record["u.name"]
			user["pwd"] = record["u.pwd"]
			user["ck"] = record["u.consumer_key"]
			user["cs"] = record["u.consumer_secret"]
			user["act"] = record["u.access_token"]
			user["acs"] = record["u.access_secret"]
			return user
	def loadUser(self,uname):
		with self._driver.session() as r: 
			return r.read_transaction(self.tx_loaduser,uname)
	@classmethod
	def tx_allSignedUser(cls,tx):
		vec = tx.run("match(u:User) return u.name")
		users = list()
		for record in vec:
			users.append(record["u.name"])
		return users
	def allSignedUsers(self):
		with self._driver.session() as r:
			return r.read_transaction(self.tx_allSignedUser)
#now we work with this 
	@classmethod
	def tx_impres(cls,tx,file,model,date,time):
		try:
			tx.run("call apoc.load.json($file) yield value as res "
					"UNWIND res.concepts as r "
					"merge (c:Concepte{name: r.name, " 
					"pos: r.pos, neg:r.neg,pourPos: r.pourPos,pourNeg: r.pourNeg, model: $model,date:$date,time:$time})",file=file,model=model,date=date,time=time)
		except Neo.ClientError:
			print("erreur de la part du client serveur")
	@classmethod
	def tx_matchsmart(cls,tx):
		try:
			tx.run(" match(c:Concepte),(m:Model),(a:Analyse) "
					" where c.name='Smartphone' and c.model=m.name and a.day = m.date and m.time=a.time and c.date= m.date and c.time = m.time "
					" merge(c)-[:is]->(m) ")
		except Neo.ClientError as e :
			raise e
	@classmethod
	def tx_crdate(cls,tx, user, date,time):
		try:
			tx.run("merge(a:Analyse{ day: $date,time: $time,user: $user})",user=user,date=date,time=time)
		except Neo.ClientError:
			print("error from server")
	@classmethod
	def tx_crmodel(cls,tx,model,date,time):
		try:
			tx.run("merge (m:Model{name: $model,date: $date, time: $time})",model=model,date=date,time=time)
		except Neo.ClientError as e:
			raise e
	@classmethod
	def tx_mchuser(cls,tx):
		try:
			tx.run("match(a:Analyse),(c:Concepte),(m:Model),(u:User) "
				   "where (u.name = a.user AND m.date = a.day AND m.time=a.time) AND (m.name = c.model and m.date= c.date and m.time= c.time and  NOT(c.name='Smartphone')) "
				   " merge(u)-[:effected]->(a) "
					"merge (a)-[:concerne]->(m) "
					"merge(m)-[:contains]->(c) " )
		except Neo.ClientError:
			print("error from server")
	def importresult(self,user,file,date,time,model):
		with self._driver.session() as B:
			B.write_transaction(self.tx_crdate,user,date,time)
			B.write_transaction(self.tx_crmodel,model,date,time)
			B.write_transaction(self.tx_impres,file,model,date,time)
			B.write_transaction(self.tx_matchsmart)
			B.write_transaction(self.tx_mchuser)
	@classmethod
	def tx_loadmod(cls,tx,user,date,time,model):
		try:
		 	models = tx.run("match (c:Concepte)<-[:contains]-(m:Model{name: $model })<-[:concerne]-(a:Analyse{ day: $date,time: $time})<-[:effected]-(u:User{name: $user}) "
							"return m.name,c.name,c.pos,c.neg,c.pourPos,c.pourNeg "
							"ORDER BY m.name",user=user,date=date,time=time,model=model)
		 	res = list()
		 	temp = dict()
		 	result = dict()
		 	smart_phone = {}
		 	for record in models:
		 		result["model"] = record["m.name"]
		 		temp["name"]= record["c.name"]
		 		temp["pos"] = record["c.pos"]
		 		temp["neg"] = record["c.neg"]
		 		temp["pourPos"] = record["c.pourPos"]
		 		temp["pourNeg"] = record["c.pourNeg"]
		 		res.append(temp)
		 		temp = {}
		 	result["concepts"] = res
		 	head = tx.run("match(c:Concepte)-[:is]->(m:Model{name:$model})<-[:concerne]-(a:Analyse{day:$date,time:$time})<-[:effected]-(u:User{name: $user}) "
							"return c.pos,c.neg,c.pourPos,c.pourNeg ",user=user,date=date,time=time,model=model)
		 	for record in head:
		 		smart_phone["name"] = model
		 		smart_phone["pos"] = record['c.pos']
		 		smart_phone["neg"] = record['c.neg']
		 		smart_phone["pourPos"] = record['c.pourPos']
		 		smart_phone["pourNeg"] = record['c.pourNeg']
		 	if result["concepts"] != [] and smart_phone != {}:
		 		return smart_phone,result
		 	else:
		 		return False
		except Exception as e:
		 	raise
	def loadresult(self,user,date,time,model):
		with self._driver.session() as r:
			return r.read_transaction(self.tx_loadmod,user,date,time,model)
	@classmethod
	def tx_loadmodelsu(cls,tx,user):
		if user=="admin":
			models = tx.run("match (u:User)-[]->()-[]->(m:Model) return u.name,m.name,m.date,m.time ")
			result = list()
			for record in models:
				s =record["m.name"]+"/"+record["m.date"]+"/"+record["m.time"]+"/"+ record["u.name"]
				result.append(s)
		else:	
			models = tx.run("match (u:User{name:$user})-[]->()-[]->(m:Model) return m.name,m.date,m.time " ,user=user )
			result = list()
			for record in models:
				s = record["m.name"]+"/"+record["m.date"]+"/"+record["m.time"]
				result.append(s)
		return result
	def load_user_mod(self,user):
		with self._driver.session() as r:
			return r.read_transaction(self.tx_loadmodelsu,user)
	@classmethod
	def tx_loadAnalyses(cls,tx,user):
		if user != "admin":
			cur = tx.run("match(u:User{name:$user})-[]->(a:Analyse)-[]->(m:Model)  return a.day,a.time,m.name ",user=user)
			res = []
			temp = {}
			for record in cur: 
				temp['model'] = record['m.name']
				temp['date']=record['a.day']
				temp['time'] = record['a.time']
				res.append(temp)
				temp = {}
		else :
			cur = tx.run("match(u:User)-[]->(a:Analyse)-[]->(m:Model)  return u.name,a.day,a.time,m.name ")
			res = []
			temp = {}
			for record in cur:
				temp ['user']= record['u.name'] 
				temp['model'] = record['m.name']
				temp['date']=record['a.day']
				temp['time'] = record['a.time']
				res.append(temp)
				temp = {}
		return res 
	def loadAnalyses(self,user):
		with self._driver.session() as b : 
			return b.read_transaction(self.tx_loadAnalyses,user)

#########################################################################
	@classmethod
	def tx_detach(cls,tx,user,date,time):
		tx.run("match(a:Analyse{day: $date,time: $time,user: $user})-[]->(m:Model)-[]->(c:Concepte) detach delete a,m,c ",user=user,date=date,time=time)
	def deleteAnalyse(self,user,date,time):
		with self._driver.session() as A:
			try:
				A.write_transaction(self.tx_detach,user,date,time)
			except Exception as e:
				raise e 
	@classmethod
	def tx_dtu(cls,tx,user):
		tx.run(" match (u:User{name:$user})-[]->(a:Analyse)-[]->(m:Model)-[]->(c:Concepte) detach delete u,a,m,c ",user=user)
	def deleteUser(self,user):
		with self._driver.session() as b : 
			try:
				b.write_transaction(self.tx_dtu,user)
			except Exception as e:
				raise e
				
#########################################################################
	@classmethod 
	def tx_UpdU(cls,tx,user):
		tx.run("match(u:User) where u.name = $name set u.pwd = $pwd  ",pwd=user['pwd'],name=user['name'])
	def updatePass(self,user):
		try:
			with self._driver.session() as b :
				b.write_transaction(self.tx_UpdU,user)
		except Exception as e:
			raise e
	@classmethod
	def tx_UpTokens(cls,tx,user):
		tx.run("match(u:User) where u.name=$name set u.consumer_key=$ck set u.consumer_secret=$cs" 
			" set u.access_token= $act set u.access_secret=$acs ",name=user['name'],ck=user['ck'],cs=user['cs'],act=user['act'],acs=user['acs'])
	def updateTokens(self,user):
		try:
			with self._driver.session() as s : 
				s.write_transaction(self.tx_UpTokens,user)
		except Exception as e:
			raise e

	#load all users 
	@classmethod
	def tx_allusers(cls,tx):
		cur = tx.run(" match (u:User)-[:effected]-(Analyse) return u.name, count(*) ")
		user = {}
		result = []
		for record in cur:
			user["name"] = record['u.name']
			user["nba"] = record['count(*)']
			result.append(user)
			user = {}
		return result
	def allusers(self):
		with self._driver.session() as r :
			return r.read_transaction(self.tx_allusers)
###############
	@classmethod
	def tx_luser(cls,tx,user):
		cur = tx.run(" match (u:User{name:$user})-[:effected]-(Analyse) return u.name, count(*) ",user=user)
		user = {}
		result = []
		for record in cur:
			user["name"] = record['u.name']
			user["nba"] = record['count(*)']
			result.append(user)
			user = {}
		return result
	def luser(self,user):
		with self._driver.session() as r :
			return r.read_transaction(self.tx_luser,user)

MAIN_WIN = """QMainWindow{
    border: 2px solid grey;
    border-radius: 4px;
    background-color: #24292E;
    QLabel{
    color:#15c0ef;
    }
    QMessageBox QLabel{
    color:#ffffff;
    }
}   

"""
GRPB=""" QGroupBox{
     border:2px solid grey;
     border-radius:5px;
     color: #15c0ef;
     text-align: left;
     background-color: #24292E;
}
"""
TVIEW="""
    QTableView{
    border:2px solid grey;
    border-radius: 4px;
    background-color: #E6ECF0
    }
    QTreeView{
    border:2px solid grey;
    background-color: #E6ECF0;
    border-radius: 4px
    } 
"""
TABW=""" 
    QTabWidget::pane {
    border: 1px solid black;
    background: #24292E;
 }

    QTabWidget::tab-bar:top {
        top: 1px;
    }

    QTabWidget::tab-bar:bottom {
        bottom: 1px;
    }

    QTabWidget::tab-bar:left {
        right: 1px;
    }

    QTabWidget::tab-bar:right {
        left: 1px;
    }

    QTabBar::tab {
        border: 1px solid black;
    }

    QTabBar::tab:selected {
        background: white;
    }

    QTabBar::tab:!selected {
        background: silver;
    }

    QTabBar::tab:!selected:hover {
        background: #999;
    }

    QTabBar::tab:top:!selected {
        margin-top: 3px;
    }

    QTabBar::tab:bottom:!selected {
        margin-bottom: 3px;
    }

    QTabBar::tab:top, QTabBar::tab:bottom {
        min-width: 8ex;
        margin-right: -1px;
        padding: 5px 10px 5px 10px;
    }

    QTabBar::tab:top:selected {
        border-bottom-color: none;
    }

    QTabBar::tab:bottom:selected {
        border-top-color: none;
    }

    QTabBar::tab:top:last, QTabBar::tab:bottom:last,
    QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
        margin-right: 0;
    }

    QTabBar::tab:left:!selected {
        margin-right: 3px;
    }

    QTabBar::tab:right:!selected {
        margin-left: 3px;
    }

    QTabBar::tab:left, QTabBar::tab:right {
        min-height: 8ex;
        margin-bottom: -1px;
        padding: 10px 5px 10px 5px;
    }

    QTabBar::tab:left:selected {
        border-left-color: none;
    }

    QTabBar::tab:right:selected {
        border-right-color: none;
    }

    QTabBar::tab:left:last, QTabBar::tab:right:last,
    QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
        margin-bottom: 0;
    }
    QTabWidget::chunk{
         background-color:  #24292E;
    }
    QWidgets{
        border:2px solid grey;
        border-radius:3px;
        background-color: #4EC3DD;
    }
    QWidgets::chunk{
        background-color:  #24292E;
}
"""
BLUE_BAR = """QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: #0565d9;
    width: 10px;
    border-radius: 4px;
}
"""
RED_BAR = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: #af0d0d;
    width: 10px;
    border-radius: 4px;
}
"""
LOADB = """ QProgressBar{
    border: 2px solid grey;
    text-align: centre
}
QProgressBar::chunk {
    background-color: #4ec3dd;
    width: 10px;
 
}
"""
STATSLAB=""" QLabel{
    color: #ffffff
}

"""
LAB = """
    QLabel{
    color:#15c0ef;
    }
"""
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1079, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadLab = QtWidgets.QLabel(self.centralwidget)
        self.loadLab.setText("")
        self.loadLab.setObjectName("loadLab")
        self.horizontalLayout.addWidget(self.loadLab)
        self.LoadBar = QtWidgets.QProgressBar(self.centralwidget)
        self.LoadBar.setMaximumSize(QtCore.QSize(16777203, 15))
        self.LoadBar.setProperty("value", 0)
        self.LoadBar.setObjectName("LoadBar")
        self.horizontalLayout.addWidget(self.LoadBar)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(106, 111))
        self.groupBox.setMaximumSize(QtCore.QSize(200, 16777180))
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.MyTree = QtWidgets.QTreeView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MyTree.sizePolicy().hasHeightForWidth())
        self.MyTree.setSizePolicy(sizePolicy)
        self.MyTree.setMaximumSize(QtCore.QSize(1700, 16777199))
        self.MyTree.setMouseTracking(True)
        self.MyTree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.MyTree.setAutoFillBackground(True)
        self.MyTree.setFrameShape(QtWidgets.QFrame.Panel)
        self.MyTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.MyTree.setDragEnabled(False)
        self.MyTree.setAlternatingRowColors(True)
        self.MyTree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.MyTree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.MyTree.setAutoExpandDelay(1)
        self.MyTree.setIndentation(20)
        self.MyTree.setRootIsDecorated(True)
        self.MyTree.setUniformRowHeights(True)
        self.MyTree.setSortingEnabled(True)
        self.MyTree.setAnimated(True)
        self.MyTree.setAllColumnsShowFocus(True)
        self.MyTree.setObjectName("MyTree")
        self.MyTree.header().setVisible(False)
        self.MyTree.header().setCascadingSectionResizes(True)
        self.MyTree.header().setDefaultSectionSize(200)
        self.MyTree.header().setHighlightSections(False)
        self.MyTree.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.MyTree, 3, 0, 1, 1)
        self.ModelsBox = QtWidgets.QComboBox(self.groupBox)
        self.ModelsBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ModelsBox.sizePolicy().hasHeightForWidth())
        self.ModelsBox.setSizePolicy(sizePolicy)
        self.ModelsBox.setMinimumSize(QtCore.QSize(35, 44))
        self.ModelsBox.setMouseTracking(True)
        self.ModelsBox.setFrame(True)
        self.ModelsBox.setObjectName("ModelsBox")
        self.gridLayout.addWidget(self.ModelsBox, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(60, 60))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab1 = QtWidgets.QWidget()
        self.Tab1.setAutoFillBackground(True)
        self.Tab1.setObjectName("Tab1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Tab1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.CP = QtWidgets.QRadioButton(self.Tab1)
        self.CP.setObjectName("CP")
        self.gridLayout_3.addWidget(self.CP, 6, 0, 1, 1)
        self.NB = QtWidgets.QRadioButton(self.Tab1)
        self.NB.setObjectName("NB")
        self.gridLayout_3.addWidget(self.NB, 7, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.Tab1)
        self.tableView.setMouseTracking(True)
        self.tableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableView.setAutoFillBackground(True)
        self.tableView.setInputMethodHints(QtCore.Qt.ImhPreferLatin)
        self.tableView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableView.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableView.setLineWidth(0)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setProperty("showDropIndicator", False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setGridStyle(QtCore.Qt.SolidLine)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setDefaultSectionSize(150)
        self.tableView.horizontalHeader().setMinimumSectionSize(100)
        self.tableView.horizontalHeader().setSortIndicatorShown(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.tableView, 0, 0, 1, 6)
        self.groupBox_2 = QtWidgets.QGroupBox(self.Tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(500, 500))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.posBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.posBar.setProperty("value", 0)
        self.posBar.setObjectName("posBar")
        self.verticalLayout.addWidget(self.posBar)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.negBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.negBar.setProperty("value", 0)
        self.negBar.setObjectName("negBar")
        self.verticalLayout.addWidget(self.negBar)
        self.gridLayout_3.addWidget(self.groupBox_2, 4, 4, 9, 2)
        self.choiceBox = QtWidgets.QCheckBox(self.Tab1)
        self.choiceBox.setObjectName("choiceBox")
        self.gridLayout_3.addWidget(self.choiceBox, 8, 0, 1, 1)
        self.SearchBtn = QtWidgets.QPushButton(self.Tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBtn.sizePolicy().hasHeightForWidth())
        self.SearchBtn.setSizePolicy(sizePolicy)
        self.SearchBtn.setObjectName("SearchBtn")
        self.gridLayout_3.addWidget(self.SearchBtn, 6, 1, 1, 1)
        self.showtweetsbtn = QtWidgets.QPushButton(self.Tab1)
        self.showtweetsbtn.setObjectName("showtweetsbtn")
        self.gridLayout_3.addWidget(self.showtweetsbtn, 6, 2, 1, 1)
        self.refrechBtn = QtWidgets.QPushButton(self.Tab1)
        self.refrechBtn.setObjectName("refrechBtn")
        self.gridLayout_3.addWidget(self.refrechBtn, 7, 1, 1, 1)
        self.saveBtn = QtWidgets.QPushButton(self.Tab1)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout_3.addWidget(self.saveBtn, 7, 2, 1, 1)
        self.tableView.raise_()
        self.groupBox_2.raise_()
        self.CP.raise_()
        self.NB.raise_()
        self.choiceBox.raise_()
        self.SearchBtn.raise_()
        self.showtweetsbtn.raise_()
        self.refrechBtn.raise_()
        self.saveBtn.raise_()
        self.tabWidget.addTab(self.Tab1, "")
        self.Tab2 = QtWidgets.QWidget()
        self.Tab2.setObjectName("Tab2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Tab2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QtCore.QSize(400, 300))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SavedModels = QtWidgets.QComboBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SavedModels.sizePolicy().hasHeightForWidth())
        self.SavedModels.setSizePolicy(sizePolicy)
        self.SavedModels.setMinimumSize(QtCore.QSize(200, 30))
        self.SavedModels.setMaximumSize(QtCore.QSize(500, 400))
        self.SavedModels.setObjectName("SavedModels")
        self.verticalLayout_3.addWidget(self.SavedModels)
        self.LoadBtn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadBtn.sizePolicy().hasHeightForWidth())
        self.LoadBtn.setSizePolicy(sizePolicy)
        self.LoadBtn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.LoadBtn.setObjectName("LoadBtn")
        self.verticalLayout_3.addWidget(self.LoadBtn)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.posBar_2 = QtWidgets.QProgressBar(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posBar_2.sizePolicy().hasHeightForWidth())
        self.posBar_2.setSizePolicy(sizePolicy)
        self.posBar_2.setMaximumSize(QtCore.QSize(250, 300))
        self.posBar_2.setProperty("value", 0)
        self.posBar_2.setObjectName("posBar_2")
        self.verticalLayout_3.addWidget(self.posBar_2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.negBar_2 = QtWidgets.QProgressBar(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.negBar_2.sizePolicy().hasHeightForWidth())
        self.negBar_2.setSizePolicy(sizePolicy)
        self.negBar_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.negBar_2.setProperty("value", 0)
        self.negBar_2.setObjectName("negBar_2")
        self.verticalLayout_3.addWidget(self.negBar_2)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.Loaded = QtWidgets.QTableView(self.Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Loaded.sizePolicy().hasHeightForWidth())
        self.Loaded.setSizePolicy(sizePolicy)
        self.Loaded.setMinimumSize(QtCore.QSize(5, 0))
        self.Loaded.setMouseTracking(True)
        self.Loaded.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Loaded.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Loaded.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Loaded.setObjectName("Loaded")
        self.Loaded.horizontalHeader().setCascadingSectionResizes(True)
        self.Loaded.horizontalHeader().setSortIndicatorShown(True)
        self.Loaded.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.Loaded)
        self.tabWidget.addTab(self.Tab2, "")
        self.Tab3 = QtWidgets.QWidget()
        self.Tab3.setObjectName("Tab3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Tab3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.Tab3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMaximumSize(QtCore.QSize(600, 200))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setMaximumSize(QtCore.QSize(120, 20))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setMaximumSize(QtCore.QSize(120, 18))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_6)
        self.histModlesBox = QtWidgets.QComboBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histModlesBox.sizePolicy().hasHeightForWidth())
        self.histModlesBox.setSizePolicy(sizePolicy)
        self.histModlesBox.setMinimumSize(QtCore.QSize(250, 40))
        self.histModlesBox.setMaximumSize(QtCore.QSize(250, 40))
        self.histModlesBox.setObjectName("histModlesBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.histModlesBox)
        self.prod2 = QtWidgets.QComboBox(self.groupBox_4)
        self.prod2.setMinimumSize(QtCore.QSize(250, 40))
        self.prod2.setMaximumSize(QtCore.QSize(250, 40))
        self.prod2.setObjectName("prod2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.prod2)
        self.graphChoice = QtWidgets.QComboBox(self.groupBox_4)
        self.graphChoice.setMinimumSize(QtCore.QSize(100, 30))
        self.graphChoice.setEditable(False)
        self.graphChoice.setObjectName("graphChoice")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/both.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.graphChoice.addItem(icon1, "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.graphChoice.addItem(icon2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.graphChoice.addItem(icon3, "")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.graphChoice)
        self.showhisbtn = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showhisbtn.sizePolicy().hasHeightForWidth())
        self.showhisbtn.setSizePolicy(sizePolicy)
        self.showhisbtn.setMaximumSize(QtCore.QSize(100, 40))
        self.showhisbtn.setObjectName("showhisbtn")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.showhisbtn)
        self.saveGraph = QtWidgets.QPushButton(self.groupBox_4)
        self.saveGraph.setMinimumSize(QtCore.QSize(30, 30))
        self.saveGraph.setMaximumSize(QtCore.QSize(100, 25))
        self.saveGraph.setObjectName("saveGraph")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.saveGraph)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.HistLay = QtWidgets.QVBoxLayout()
        self.HistLay.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.HistLay.setSpacing(0)
        self.HistLay.setObjectName("HistLay")
        self.verticalLayout_2.addLayout(self.HistLay)
        self.tabWidget.addTab(self.Tab3, "")
        self.plotevo = QtWidgets.QWidget()
        self.plotevo.setObjectName("plotevo")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.plotevo)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.plotevo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(260, 180))
        self.groupBox_5.setMaximumSize(QtCore.QSize(400, 180))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_5)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QtCore.QSize(200, 20))
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.startDE = QtWidgets.QDateEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDE.sizePolicy().hasHeightForWidth())
        self.startDE.setSizePolicy(sizePolicy)
        self.startDE.setMinimumSize(QtCore.QSize(200, 30))
        self.startDE.setMaximumSize(QtCore.QSize(200, 30))
        self.startDE.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2018, 3, 9), QtCore.QTime(0, 0, 2)))
        self.startDE.setMinimumDate(QtCore.QDate(2018, 3, 9))
        self.startDE.setCalendarPopup(True)
        self.startDE.setObjectName("startDE")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.startDE)
        self.plotChoice = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotChoice.sizePolicy().hasHeightForWidth())
        self.plotChoice.setSizePolicy(sizePolicy)
        self.plotChoice.setMinimumSize(QtCore.QSize(100, 30))
        self.plotChoice.setMaximumSize(QtCore.QSize(150, 40))
        self.plotChoice.setObjectName("plotChoice")
        self.plotChoice.addItem(icon1, "")
        self.plotChoice.addItem(icon2, "")
        self.plotChoice.addItem(icon3, "")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.plotChoice)
        self.label_8 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMaximumSize(QtCore.QSize(200, 20))
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.endDE = QtWidgets.QDateEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endDE.sizePolicy().hasHeightForWidth())
        self.endDE.setSizePolicy(sizePolicy)
        self.endDE.setMinimumSize(QtCore.QSize(200, 30))
        self.endDE.setMaximumSize(QtCore.QSize(200, 30))
        self.endDE.setMinimumDate(QtCore.QDate(2018, 3, 9))
        self.endDE.setCalendarPopup(True)
        self.endDE.setObjectName("endDE")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.endDE)
        self.saveplot = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveplot.sizePolicy().hasHeightForWidth())
        self.saveplot.setSizePolicy(sizePolicy)
        self.saveplot.setMinimumSize(QtCore.QSize(150, 30))
        self.saveplot.setMaximumSize(QtCore.QSize(150, 30))
        self.saveplot.setObjectName("saveplot")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.saveplot)
        self.showp = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showp.sizePolicy().hasHeightForWidth())
        self.showp.setSizePolicy(sizePolicy)
        self.showp.setMinimumSize(QtCore.QSize(150, 30))
        self.showp.setMaximumSize(QtCore.QSize(150, 30))
        self.showp.setObjectName("showp")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.showp)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        self.pltlayot = QtWidgets.QVBoxLayout()
        self.pltlayot.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.pltlayot.setSpacing(0)
        self.pltlayot.setObjectName("pltlayot")
        self.verticalLayout_5.addLayout(self.pltlayot)
        self.tabWidget.addTab(self.plotevo, "")
        self.DbSettings = QtWidgets.QWidget()
        self.DbSettings.setObjectName("DbSettings")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.DbSettings)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.DbPicture = QtWidgets.QTableView(self.DbSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DbPicture.sizePolicy().hasHeightForWidth())
        self.DbPicture.setSizePolicy(sizePolicy)
        self.DbPicture.setMinimumSize(QtCore.QSize(800, 560))
        self.DbPicture.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.DbPicture.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.DbPicture.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.DbPicture.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.DbPicture.setObjectName("DbPicture")
        self.DbPicture.horizontalHeader().setDefaultSectionSize(150)
        self.DbPicture.horizontalHeader().setStretchLastSection(True)
        self.DbPicture.verticalHeader().setVisible(False)
        self.DbPicture.verticalHeader().setDefaultSectionSize(50)
        self.DbPicture.verticalHeader().setMinimumSectionSize(70)
        self.verticalLayout_6.addWidget(self.DbPicture)
        self.deleteA = QtWidgets.QPushButton(self.DbSettings)
        self.deleteA.setMaximumSize(QtCore.QSize(167, 16777116))
        self.deleteA.setObjectName("deleteA")
        self.verticalLayout_6.addWidget(self.deleteA)
        self.tabWidget.addTab(self.DbSettings, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1079, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionChange_Password = QtWidgets.QAction(MainWindow)
        self.actionChange_Password.setObjectName("actionChange_Password")
        self.actionChange_Token_keys = QtWidgets.QAction(MainWindow)
        self.actionChange_Token_keys.setObjectName("actionChange_Token_keys")
        self.actionCheck_for_updates = QtWidgets.QAction(MainWindow)
        self.actionCheck_for_updates.setObjectName("actionCheck_for_updates")
        self.actionAccount_Management = QtWidgets.QAction(MainWindow)
        self.actionAccount_Management.setObjectName("actionAccount_Management")
        self.actionAdmin_Settings = QtWidgets.QAction(MainWindow)
        self.actionAdmin_Settings.setObjectName("actionAdmin_Settings")
        self.menuSettings.addAction(self.actionCheck_for_updates)
        self.menuSettings.addAction(self.actionAccount_Management)
        self.menuSettings.addAction(self.actionAdmin_Settings)
        self.menuBar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        self.ModelsBox.setCurrentIndex(-1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#############################################################
        self.loadLab.setText("")
        self.LoadBar.setEnabled(False)
        self.LoadBar.setValue(0)
        self.statusbar.addPermanentWidget(self.loadLab,2)
        self.statusbar.addPermanentWidget(self.LoadBar,1)
        self.loadLab.setText("")
        MainWindow.setStyleSheet(MAIN_WIN) 
        self.groupBox.setStyleSheet(GRPB)
        self.groupBox_3.setStyleSheet(GRPB)
        self.groupBox_2.setStyleSheet(GRPB)
        self.groupBox_4.setStyleSheet(GRPB)
        self.groupBox_5.setStyleSheet(GRPB)
        self.MyTree.setStyleSheet(TVIEW)
        self.tableView.setStyleSheet(TVIEW)
        self.tabWidget.setStyleSheet(TABW)
        self.Loaded.setStyleSheet(TVIEW)   
        self.negBar.setStyleSheet(RED_BAR)
        self.negBar_2.setStyleSheet(RED_BAR)
        self.posBar.setStyleSheet(BLUE_BAR)
        self.posBar_2.setStyleSheet(BLUE_BAR)
        self.loadLab.setStyleSheet(STATSLAB)
        self.LoadBar.setStyleSheet(LOADB)
        self.label.setStyleSheet(LAB)
        self.label_8.setStyleSheet(LAB)
        self.label_7.setStyleSheet(LAB)
        self.label_6.setStyleSheet(LAB)
        self.label_5.setStyleSheet(LAB)
        self.label_4.setStyleSheet(LAB)
        self.label_3.setStyleSheet(LAB)
        self.label_2.setStyleSheet(LAB)
        self.CP.setChecked(True)
################################################################################    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Twitter Talk"))
        self.CP.setText(_translate("MainWindow", "Lexical Approche (PatternAnalyzer) "))
        self.NB.setText(_translate("MainWindow", "Automatic approche (Naive Bayes)"))
        self.label.setText(_translate("MainWindow", "Positivity:"))
        self.label_2.setText(_translate("MainWindow", "Negativity:"))
        self.choiceBox.setText(_translate("MainWindow", "Actuall Tendency"))
        self.SearchBtn.setText(_translate("MainWindow", "Search"))
        self.showtweetsbtn.setText(_translate("MainWindow", "show tweets"))
        self.refrechBtn.setText(_translate("MainWindow", "Refresh"))
        self.saveBtn.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("MainWindow", "Search and analyse"))
        self.LoadBtn.setText(_translate("MainWindow", "Load"))
        self.label_3.setText(_translate("MainWindow", "Positivity:"))
        self.label_4.setText(_translate("MainWindow", "Negativity:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), _translate("MainWindow", "Saved results"))
        self.label_5.setText(_translate("MainWindow", "First Analyse :"))
        self.label_6.setText(_translate("MainWindow", "second Analyse:"))
        self.graphChoice.setItemText(0, _translate("MainWindow", "Both"))
        self.graphChoice.setItemText(1, _translate("MainWindow", "Positivity"))
        self.graphChoice.setItemText(2, _translate("MainWindow", "Negativity"))
        self.showhisbtn.setText(_translate("MainWindow", "Show Progress"))
        self.saveGraph.setText(_translate("MainWindow", "save Graphe"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab3), _translate("MainWindow", "comparatif study"))
        self.label_7.setText(_translate("MainWindow", "Start point:"))
        self.plotChoice.setItemText(0, _translate("MainWindow", "Both"))
        self.plotChoice.setItemText(1, _translate("MainWindow", "Positive"))
        self.plotChoice.setItemText(2, _translate("MainWindow", "Negative"))
        self.label_8.setText(_translate("MainWindow", "end point:"))
        self.saveplot.setText(_translate("MainWindow", "Save graphe "))
        self.showp.setText(_translate("MainWindow", "Show Progression"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotevo), _translate("MainWindow", "Time Evolution"))
        self.deleteA.setText(_translate("MainWindow", "delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DbSettings), _translate("MainWindow", "Neo4j Settings"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionChange_Password.setText(_translate("MainWindow", "Change Password"))
        self.actionChange_Token_keys.setText(_translate("MainWindow", "Change Token keys"))
        self.actionCheck_for_updates.setText(_translate("MainWindow", "Check for updates"))
        self.actionAccount_Management.setText(_translate("MainWindow", "General"))
        self.actionAdmin_Settings.setText(_translate("MainWindow", "Admin Settings"))
        MAIN="""QDialog{
    border: 2px solid grey;
    background-color: #24292E;
    border-radius:5px
    }
    QLabel{
    color:#15c0ef;
    }
    QMessageBox QLabel{
    color:#ffffff;
    }
    
"""
TABW=""" 
    QTabWidget::pane {
    border: 1px solid black;
    background: #24292E;
 }

    QTabWidget::tab-bar:top {
        top: 1px;
    }

    QTabWidget::tab-bar:bottom {
        bottom: 1px;
    }

    QTabWidget::tab-bar:left {
        right: 1px;
    }

    QTabWidget::tab-bar:right {
        left: 1px;
    }

    QTabBar::tab {
        border: 1px solid black;
    }

    QTabBar::tab:selected {
        background: white;
    }

    QTabBar::tab:!selected {
        background: silver;
    }

    QTabBar::tab:!selected:hover {
        background: #999;
    }

    QTabBar::tab:top:!selected {
        margin-top: 3px;
    }

    QTabBar::tab:bottom:!selected {
        margin-bottom: 3px;
    }

    QTabBar::tab:top, QTabBar::tab:bottom {
        min-width: 8ex;
        margin-right: -1px;
        padding: 5px 10px 5px 10px;
    }

    QTabBar::tab:top:selected {
        border-bottom-color: none;
    }

    QTabBar::tab:bottom:selected {
        border-top-color: none;
    }

    QTabBar::tab:top:last, QTabBar::tab:bottom:last,
    QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
        margin-right: 0;
    }

    QTabBar::tab:left:!selected {
        margin-right: 3px;
    }

    QTabBar::tab:right:!selected {
        margin-left: 3px;
    }

    QTabBar::tab:left, QTabBar::tab:right {
        min-height: 8ex;
        margin-bottom: -1px;
        padding: 10px 5px 10px 5px;
    }

    QTabBar::tab:left:selected {
        border-left-color: none;
    }

    QTabBar::tab:right:selected {
        border-right-color: none;
    }

    QTabBar::tab:left:last, QTabBar::tab:right:last,
    QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
        margin-bottom: 0;
    }
    QTabWidget::chunk{
         background-color:  #24292E;
    }
    QWidgets{
        border:2px solid grey;
        border-radius:3px;
        background-color: #4EC3DD;
    }
    QWidgets::chunk{
        background-color:  #24292E;
}
"""
MAIN_WIN = """QMainWindow{
    border: 2px solid grey;
    border-radius: 4px;
    background-color: #24292E;
    
    QMessageBox QLabel{
    color:#ffffff;
    }
}"""
GRPB=""" QGroupBox{
     border:2px solid grey;
     border-radius:5px;
     color: #15c0ef;
     text-align: left;
     background-color: #24292E;
}
"""
STATSLAB=""" QLabel{
    color: #ffffff;
    
}
"""
ERROREDIT="""QLineEdit{
        border: 2px solid #f40404;
        background-color: #24292E;
        color: #f40404;}
"""
VALIDLINE="""
QLineEdit{
    border: 2px solid green;
    background-color: #24292E;
    color: green;}

"""
SWITCHBTN="""QPushButton{
        
        color:#ffffff;
        text-align:left;
}
"""
LEDIT="""QLineEdit{
    border: 2px solid #0565d9;
    background-color: #24292E;
    color: #ffffff;
}
"""
TEDIT="""QTextEdit{
    border: 2px solid #0565d9;
    background-color: #24292E;
    color: #ffffff;
}
"""
PBAR ="""QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
"""
class Ui_AuthWindow(object):
    def setupUi(self, AuthWindow):
        AuthWindow.setObjectName("AuthWindow")
        AuthWindow.setWindowModality(QtCore.Qt.NonModal)
        AuthWindow.resize(419, 182)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AuthWindow.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(AuthWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.login = QtWidgets.QPushButton(AuthWindow)
        self.login.setMinimumSize(QtCore.QSize(0, 31))
        self.login.setObjectName("login")
        self.gridLayout.addWidget(self.login, 5, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(AuthWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.switch = QtWidgets.QPushButton(AuthWindow)
        self.switch.setStyleSheet("text-align:left")
        self.switch.setFlat(True)
        self.switch.setObjectName("switch")
        self.gridLayout.addWidget(self.switch, 5, 1, 1, 1)
        self.pwd = ClickableLineEdit(AuthWindow)
        self.pwd.setMaxLength(32)
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setObjectName("pwd")
        self.gridLayout.addWidget(self.pwd, 4, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(AuthWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(AuthWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 2, 2)
        self.id = ClickableLineEdit(AuthWindow)
        self.id.setMaxLength(32)
        self.id.setObjectName("id")
        self.gridLayout.addWidget(self.id, 2, 1, 1, 2)
        self.label = QtWidgets.QLabel(AuthWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.signin = QtWidgets.QPushButton(AuthWindow)
        self.signin.setMinimumSize(QtCore.QSize(0, 46))
        self.signin.setObjectName("signin")
        self.gridLayout.addWidget(self.signin, 6, 2, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        
        self.retranslateUi(AuthWindow)
        QtCore.QMetaObject.connectSlotsByName(AuthWindow)
        AuthWindow.setStyleSheet(MAIN)
        self.label.setStyleSheet(STATSLAB)
        self.label_2.setStyleSheet(STATSLAB)
        self.label_3.setStyleSheet(STATSLAB)
        self.label_4.setStyleSheet(STATSLAB)
        self.switch.setStyleSheet(SWITCHBTN)
        self.id.setStyleSheet(LEDIT)
        self.pwd.setStyleSheet(LEDIT)
    def retranslateUi(self, AuthWindow):
        _translate = QtCore.QCoreApplication.translate
        AuthWindow.setWindowTitle(_translate("AuthWindow", "Twitter Talk Auth"))
        self.login.setText(_translate("AuthWindow", "Login"))
        self.label_2.setText(_translate("AuthWindow", "      password:"))
        self.switch.setText(_translate("AuthWindow", "show password"))
        self.label_4.setText(_translate("AuthWindow", "welcome to Twitter Talk "))
        self.label_3.setText(_translate("AuthWindow", "don\'t have an account ? join us .."))
        self.label.setText(_translate("AuthWindow", "      username :"))
        self.signin.setText(_translate("AuthWindow", "Sign In"))
#################################################################################
class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLineEdit.mousePressEvent(self, event)


##################################################################################################"
class SignWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 418)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(9, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setMinimumSize(QtCore.QSize(0, 21))
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.acctoken = ClickableLineEdit(Dialog)
        self.acctoken.setMinimumSize(QtCore.QSize(0, 28))
        self.acctoken.setObjectName("acctoken")
        self.gridLayout_2.addWidget(self.acctoken, 6, 1, 1, 1)
        self.username = ClickableLineEdit(Dialog)
        self.username.setMinimumSize(QtCore.QSize(40, 28))
        self.username.setMaxLength(32)
        self.username.setObjectName("username")
        self.gridLayout_2.addWidget(self.username, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setMinimumSize(QtCore.QSize(0, 21))
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 7, 0, 1, 1)
        self.accsecret = ClickableLineEdit(Dialog)
        self.accsecret.setMinimumSize(QtCore.QSize(0, 28))
        self.accsecret.setObjectName("accsecret")
        self.gridLayout_2.addWidget(self.accsecret, 7, 1, 1, 1)
        self.switch = QtWidgets.QPushButton(Dialog)
        self.switch.setStyleSheet("text-align:left")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../index.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.switch.setIcon(icon1)
        self.switch.setCheckable(False)
        self.switch.setChecked(False)
        self.switch.setFlat(True)
        self.switch.setObjectName("switch")
        self.gridLayout_2.addWidget(self.switch, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
        self.csecret = ClickableLineEdit(Dialog)
        self.csecret.setMinimumSize(QtCore.QSize(0, 28))
        self.csecret.setObjectName("csecret")
        self.gridLayout_2.addWidget(self.csecret, 5, 1, 1, 1)
        self.cancel = QtWidgets.QPushButton(Dialog)
        self.cancel.setMinimumSize(QtCore.QSize(96, 0))
        self.cancel.setMaximumSize(QtCore.QSize(160, 16777215))
        self.cancel.setObjectName("cancel")
        self.gridLayout_2.addWidget(self.cancel, 10, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 18))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.pwd = ClickableLineEdit(Dialog)
        self.pwd.setMinimumSize(QtCore.QSize(0, 28))
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd.setObjectName("pwd")
        self.gridLayout_2.addWidget(self.pwd, 1, 1, 1, 1)
        self.ckey = ClickableLineEdit(Dialog)
        self.ckey.setMinimumSize(QtCore.QSize(0, 28))
        self.ckey.setObjectName("ckey")
        self.gridLayout_2.addWidget(self.ckey, 4, 1, 1, 1)
        self.pwdconfirm = ClickableLineEdit(Dialog)
        self.pwdconfirm.setMinimumSize(QtCore.QSize(0, 28))
        self.pwdconfirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwdconfirm.setObjectName("pwdconfirm")
        self.gridLayout_2.addWidget(self.pwdconfirm, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(0, 17))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)
        self.submit = QtWidgets.QPushButton(Dialog)
        self.submit.setMinimumSize(QtCore.QSize(0, 0))
        self.submit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.submit.setFlat(False)
        self.submit.setObjectName("submit")
        self.gridLayout_2.addWidget(self.submit, 10, 1, 1, 1)
        self.twitterLink = QtWidgets.QLabel(Dialog)
        self.twitterLink.setMinimumSize(QtCore.QSize(89, 20))
        self.twitterLink.setStyleSheet("text-align:centre")
        self.twitterLink.setObjectName("twitterLink")
        self.gridLayout_2.addWidget(self.twitterLink, 9, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        urlLink="<a href=\"https://developer.twitter.com/en/apply/user\"> <font face=verdana size=4 color=#ffffff> don't have your tokens? get them now </a>"

        self.twitterLink.setText(urlLink)
        self.twitterLink.setOpenExternalLinks(True)
        Dialog.setStyleSheet(MAIN)
        self.label.setStyleSheet(STATSLAB)
        self.label_2.setStyleSheet(STATSLAB)
        self.label_3.setStyleSheet(STATSLAB)
        self.label_4.setStyleSheet(STATSLAB)
        self.label_5.setStyleSheet(STATSLAB)
        self.label_6.setStyleSheet(STATSLAB)
        self.label_7.setStyleSheet(STATSLAB)
        self.switch.setStyleSheet(SWITCHBTN)
        self.username.setStyleSheet(LEDIT)
        self.pwd.setStyleSheet(LEDIT)
        self.pwdconfirm.setStyleSheet(LEDIT)
        self.ckey.setStyleSheet(LEDIT)
        self.csecret.setStyleSheet(LEDIT)
        self.acctoken.setStyleSheet(LEDIT)
        self.accsecret.setStyleSheet(LEDIT)
        self.twitterLink.setStyleSheet("text-align:centre")
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Signing in "))
        self.label_3.setText(_translate("Dialog", "confirm password :"))
        self.label_7.setText(_translate("Dialog", "consumer key :"))
        self.label_6.setText(_translate("Dialog", "access secret :"))
        self.label_4.setText(_translate("Dialog", "consumer secret :"))
        self.switch.setText(_translate("Dialog", "show password"))
        self.label_5.setText(_translate("Dialog", "access token :"))
        self.label_2.setText(_translate("Dialog", "password:"))
        self.cancel.setText(_translate("Dialog", "cancel"))
        self.label.setText(_translate("Dialog", "user name:"))
        self.submit.setText(_translate("Dialog", "confirm"))
        self.twitterLink.setText(_translate("Dialog", "get your tokens "))
#########################################################################################
class Ui_UpdateWindow(object):
    def setupUi(self, UpdateWindow):
        self.movie = QMovie("icon/loading.gif")
        size = self.movie.scaledSize()
        UpdateWindow.setObjectName("UpdateWindow")
        UpdateWindow.setGeometry(200,200,size.width(),size.height())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UpdateWindow.sizePolicy().hasHeightForWidth())
        UpdateWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateWindow.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(UpdateWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.MainExtraLab = QtWidgets.QLabel(UpdateWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainExtraLab.sizePolicy().hasHeightForWidth())
        self.MainExtraLab.setSizePolicy(sizePolicy)
        self.MainExtraLab.setMaximumSize(QtCore.QSize(430, 28))
        self.MainExtraLab.setText("")
        self.MainExtraLab.setObjectName("MainExtraLab")
        self.gridLayout.addWidget(self.MainExtraLab, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(UpdateWindow)
        self.label.setText("")
        
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(UpdateWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdateWindow)
        #################""
        UpdateWindow.setStyleSheet(MAIN)
        self.label.setMovie(self.movie)
        self.movie.start()
    def retranslateUi(self, UpdateWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindow.setWindowTitle(_translate("UpdateWindow", "Twitter Talk "))


##########################
class Ui_ShowTweets(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(650, 550)
        form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setObjectName("gridLayout")
        self.MyTweets = QtWidgets.QTableView(form)
        self.MyTweets.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.MyTweets.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.MyTweets.setAlternatingRowColors(True)
        self.MyTweets.setObjectName("MyTweets")
        self.MyTweets.horizontalHeader().setDefaultSectionSize(150)
        self.MyTweets.horizontalHeader().setMinimumSectionSize(90)
        self.MyTweets.horizontalHeader().setStretchLastSection(True)
        self.MyTweets.verticalHeader().setVisible(True)
        self.MyTweets.verticalHeader().setDefaultSectionSize(40)
        self.MyTweets.verticalHeader().setMinimumSectionSize(120)
        self.MyTweets.verticalHeader().setSortIndicatorShown(True)
        self.MyTweets.verticalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.MyTweets, 0, 0, 1, 1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Tweets"))
################################################
class Ui_Acm(object):
    def setupUi(self, acm):
        acm.setObjectName("acm")
        acm.resize(424, 506)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        acm.setWindowIcon(icon)
        self.formLayout_2 = QtWidgets.QFormLayout(acm)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(acm)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.setStyleSheet(TABW)
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(200, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.Npwd = ClickableLineEdit(self.groupBox)
        self.Npwd.setMinimumSize(QtCore.QSize(200, 30))
        self.Npwd.setMaximumSize(QtCore.QSize(200, 30))
        self.Npwd.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.Npwd.setObjectName("Npwd")
        self.gridLayout_2.addWidget(self.Npwd, 1, 0, 1, 1)
        self.submit = QtWidgets.QPushButton(self.groupBox)
        self.submit.setMinimumSize(QtCore.QSize(150, 30))
        self.submit.setMaximumSize(QtCore.QSize(150, 30))
        self.submit.setObjectName("submit")
        self.gridLayout_2.addWidget(self.submit, 2, 1, 1, 1)
        self.Npwdc = ClickableLineEdit(self.groupBox)
        self.Npwdc.setMinimumSize(QtCore.QSize(200, 30))
        self.Npwdc.setMaximumSize(QtCore.QSize(200, 30))
        self.Npwdc.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.Npwdc.setObjectName("Npwdc")
        self.gridLayout_2.addWidget(self.Npwdc, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(200, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.cs = ClickableLineEdit(self.groupBox_2)
        self.cs.setMinimumSize(QtCore.QSize(250, 30))
        self.cs.setObjectName("cs")
        self.gridLayout.addWidget(self.cs, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.act = ClickableLineEdit(self.groupBox_2)
        self.act.setMinimumSize(QtCore.QSize(250, 30))
        self.act.setObjectName("act")
        self.gridLayout.addWidget(self.act, 5, 0, 1, 1)
        self.ck = ClickableLineEdit(self.groupBox_2)
        self.ck.setMinimumSize(QtCore.QSize(250, 30))
        self.ck.setMaximumSize(QtCore.QSize(400, 30))
        self.ck.setObjectName("ck")
        self.gridLayout.addWidget(self.ck, 1, 0, 1, 1)
        self.gapi = QtWidgets.QPushButton(self.groupBox_2)
        self.gapi.setMinimumSize(QtCore.QSize(100, 30))
        self.gapi.setObjectName("gapi")
        self.gridLayout.addWidget(self.gapi, 3, 1, 1, 1)
        self.acs = ClickableLineEdit(self.groupBox_2)
        self.acs.setMinimumSize(QtCore.QSize(250, 30))
        self.acs.setMaximumSize(QtCore.QSize(300, 30))
        self.acs.setObjectName("acs")
        self.gridLayout.addWidget(self.acs, 9, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.groupBox_2)
        self.Cancel = QtWidgets.QPushButton(self.tab)
        self.Cancel.setMinimumSize(QtCore.QSize(150, 30))
        self.Cancel.setMaximumSize(QtCore.QSize(100, 40))
        self.Cancel.setObjectName("Cancel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Cancel)
        self.Ok = QtWidgets.QPushButton(self.tab)
        self.Ok.setMinimumSize(QtCore.QSize(150, 30))
        self.Ok.setMaximumSize(QtCore.QSize(150, 16777215))
        self.Ok.setObjectName("Ok")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Ok)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setMinimumSize(QtCore.QSize(100, 20))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 16777071))
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)
        self.confrimbtn = QtWidgets.QPushButton(self.tab_2)
        self.confrimbtn.setMinimumSize(QtCore.QSize(24, 15))
        self.confrimbtn.setMaximumSize(QtCore.QSize(167, 30))
        self.confrimbtn.setObjectName("confrimbtn")
        self.gridLayout_3.addWidget(self.confrimbtn, 4, 1, 1, 1)
        self.pwd = ClickableLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pwd.sizePolicy().hasHeightForWidth())
        self.pwd.setSizePolicy(sizePolicy)
        self.pwd.setMinimumSize(QtCore.QSize(200, 30))
        self.pwd.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pwd.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.pwd.setObjectName("pwd")
        self.gridLayout_3.addWidget(self.pwd, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.userinfo = QtWidgets.QTextEdit(self.tab_2)
        self.userinfo.setMinimumSize(QtCore.QSize(0, 300))
        self.userinfo.setMaximumSize(QtCore.QSize(300, 300))
        self.userinfo.setObjectName("userinfo")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.userinfo.setFont(font)
        self.userinfo.setReadOnly(True)
        self.gridLayout_3.addWidget(self.userinfo, 2, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabWidget)

        self.retranslateUi(acm)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(acm)


        self.userinfo.setStyleSheet(TEDIT)
        acm.setStyleSheet(MAIN)
        self.Npwd.setStyleSheet(LEDIT)
        self.Npwdc.setStyleSheet(LEDIT)
        self.ck.setStyleSheet(LEDIT)
        self.cs.setStyleSheet(LEDIT)
        self.act.setStyleSheet(LEDIT)
        self.acs.setStyleSheet(LEDIT)
        self.groupBox.setStyleSheet(GRPB)
        self.groupBox_2.setStyleSheet(GRPB)
        self.pwd.setStyleSheet(LEDIT)
    def retranslateUi(self, acm):
        _translate = QtCore.QCoreApplication.translate
        acm.setWindowTitle(_translate("acm", "General Account Settings"))
        self.groupBox.setTitle(_translate("acm", "New Password"))
        self.label.setText(_translate("acm", "Password:"))
        self.submit.setText(_translate("acm", "submit"))
        self.label_2.setText(_translate("acm", "Confirm password:"))
        self.groupBox_2.setTitle(_translate("acm", "Update Tokens"))
        self.label_5.setText(_translate("acm", "Access Token:"))
        self.label_4.setText(_translate("acm", "Consumer key:"))
        self.label_6.setText(_translate("acm", "Secret Token:"))
        self.gapi.setText(_translate("acm", "Generate api "))
        self.label_3.setText(_translate("acm", "Consumer Secret:"))
        self.Cancel.setText(_translate("acm", "Cancel"))
        self.Ok.setText(_translate("acm", "Ok"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("acm", "Account settings"))
        self.label_7.setText(_translate("acm", "Password:"))
        self.confrimbtn.setText(_translate("acm", "confirm"))
        self.label_8.setText(_translate("acm", "User Info:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("acm", "Delete Account"))
#######
class Ui_Admins(object):
    def setupUi(self, Ads):
        Ads.setObjectName("Ads")
        Ads.resize(498, 505)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/Circle-icons-computer.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ads.setWindowIcon(icon)
        self.formLayout_2 = QtWidgets.QFormLayout(Ads)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Ads)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab1 = QtWidgets.QWidget()
        self.Tab1.setObjectName("Tab1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Tab1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.usersT = QtWidgets.QTableView(self.Tab1)
        self.usersT.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.usersT.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.usersT.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.usersT.setObjectName("usersT")
        self.usersT.horizontalHeader().setMinimumSectionSize(100)
        self.usersT.horizontalHeader().setStretchLastSection(True)
        self.usersT.verticalHeader().setVisible(False)
        self.usersT.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.usersT)
        self.deleteU = QtWidgets.QPushButton(self.Tab1)
        self.deleteU.setMinimumSize(QtCore.QSize(50, 30))
        self.deleteU.setMaximumSize(QtCore.QSize(100, 16777215))
        self.deleteU.setObjectName("deleteU")
        self.verticalLayout.addWidget(self.deleteU)
        self.tabWidget.addTab(self.Tab1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setMinimumSectionSize(100)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setDefaultSectionSize(45)
        self.tableView.verticalHeader().setMinimumSectionSize(40)
        self.verticalLayout_2.addWidget(self.tableView)
        self.removeC = QtWidgets.QPushButton(self.tab_2)
        self.removeC.setMinimumSize(QtCore.QSize(0, 25))
        self.removeC.setMaximumSize(QtCore.QSize(200, 30))
        self.removeC.setObjectName("removeC")
        self.verticalLayout_2.addWidget(self.removeC)
        self.tabWidget.addTab(self.tab_2, "")
        self.Tab_3 = QtWidgets.QWidget()
        self.Tab_3.setObjectName("Tab_3")
        self.formLayout = QtWidgets.QFormLayout(self.Tab_3)
        self.formLayout.setObjectName("formLayout")
        self.newModel = QtWidgets.QLineEdit(self.Tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newModel.sizePolicy().hasHeightForWidth())
        self.newModel.setSizePolicy(sizePolicy)
        self.newModel.setMinimumSize(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.newModel.setFont(font)
        self.newModel.setObjectName("newModel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.newModel)
        self.Add = QtWidgets.QPushButton(self.Tab_3)
        self.Add.setMaximumSize(QtCore.QSize(100, 30))
        self.Add.setObjectName("Add")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Add)
        self.modtable = QtWidgets.QTableView(self.Tab_3)
        self.modtable.setMinimumSize(QtCore.QSize(450, 370))
        self.modtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.modtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.modtable.setObjectName("modtable")
        self.modtable.horizontalHeader().setDefaultSectionSize(130)
        self.modtable.horizontalHeader().setMinimumSectionSize(70)
        self.modtable.horizontalHeader().setStretchLastSection(True)
        self.modtable.verticalHeader().setVisible(True)
        self.modtable.verticalHeader().setDefaultSectionSize(60)
        self.modtable.verticalHeader().setMinimumSectionSize(40)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.modtable)
        self.removeModel = QtWidgets.QPushButton(self.Tab_3)
        self.removeModel.setMinimumSize(QtCore.QSize(100, 30))
        self.removeModel.setMaximumSize(QtCore.QSize(150, 30))
        self.removeModel.setObjectName("removeModel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.removeModel)
        self.apply = QtWidgets.QPushButton(self.Tab_3)
        self.apply.setMinimumSize(QtCore.QSize(0, 30))
        self.apply.setMaximumSize(QtCore.QSize(200, 16777215))
        self.apply.setObjectName("apply")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.apply)
        self.tabWidget.addTab(self.Tab_3, "")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabWidget)

        self.retranslateUi(Ads)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ads)
        QtCore.QMetaObject.connectSlotsByName(Ads)
        Ads.setStyleSheet(MAIN)
        self.tabWidget.setStyleSheet(TABW)
        self.newModel.setStyleSheet(LEDIT)

    def retranslateUi(self, Ads):
        _translate = QtCore.QCoreApplication.translate
        Ads.setWindowTitle(_translate("Ads", "Adminstrative Settings"))
        self.deleteU.setText(_translate("Ads", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("Ads", "Manage Users"))
        self.removeC.setText(_translate("Ads", "remove"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Ads", "Manage Corpus"))
        self.Add.setText(_translate("Ads", "Add"))
        self.removeModel.setText(_translate("Ads", "Remove Model"))
        self.apply.setText(_translate("Ads", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_3), _translate("Ads", "Manage Model"))

def is_connected():
	try :
		socket.create_connection(("www.google.com",80))
		return True
	except OSError:
		pass
	return False
class MainWindow(QMainWindow,Ui_MainWindow):
#the init methode construct the window and all the features
	def __init__(self,parent=None):
		super(MainWindow,self).__init__(parent)
		self.setupUi(self)
		root = os.getcwd().replace("\\","/")
		self.ontopath = "file://"+root+"/docs/smart.owl"
		self.modalfile = "docs/smar.json"
		self.path_smar = "file:"+root+"/docs/smar.json"
		self.corppath = root+"/corp/"
		self.graphecache = root+"/cache/graphecache/"
		self.savegraphpath = root+"/picture/graph.png"
		self.analyser = Analyser()
		self.searcher = Searcher()
		self.saveBtn.setEnabled(False)
		self.refrechBtn.setEnabled(False)
		self.showtweetsbtn.setEnabled(False)
		self.fillbox()
		self.fillTree()
		self.declareTable()
		self.setDates()
		self.setLoadingTable()
		self.threadpool = QThreadPool()
		self.lastselectedModel = str(self.ModelsBox.currentText())
		self.plotWidget = MplHist(self.Tab3)
		self.plotWidget.setObjectName("plotWidget")
		self.HistLay.addWidget(self.plotWidget)
		self.plotWidget2 = MplHist(self.plotevo)
		self.plotWidget2.setObjectName("plotWidget2")
		self.pltlayot.addWidget(self.plotWidget2)
		self.tabWidget.currentChanged.connect(self.switchonglet)
		self.conceptes.itemChanged.connect(self.handleItemChecking)
		self.SearchBtn.clicked.connect(self.search_onClick)
		self.saveBtn.clicked.connect(self.save)
		self.LoadBtn.clicked.connect(self.load)
		self.showhisbtn.clicked.connect(self.drawHist)
		self.saveGraph.clicked.connect(self.saveFig)
		self.showp.clicked.connect(self.showp_onclick)
		self.saveplot.clicked.connect(self.savePlot_Onclick)
		self.showtweetsbtn.clicked.connect(self.showtOnClick)
		self.refrechBtn.clicked.connect(self.refrechOnClick)
		self.deleteA.clicked.connect(self.deleteOnClick)
		self.actionAccount_Management.triggered.connect(self.showMyacm)
		self.actionCheck_for_updates.triggered.connect(self.checkForUp)
		self.actionAdmin_Settings.triggered.connect(self.showAdminSettings)

# methode that show the acount mangement Gui 
	def showMyacm(self):
		acm = MyAcm(self)
		acm.main(self.neo4j,self.user)

	def showAdminSettings(self):
		Adm = AdminS(self)
		Adm.main(self.neo4j,self.corppath)
		if Adm.exec_() == QtWidgets.QDialog.Accepted:
			self.fillbox()
			self.setDates()
			self.setSavedModels()
	def setFirstV(self):		
		self.switchonglet(self.tabWidget.currentIndex())
#method that sets each onglet on click 
	def switchonglet(self,index):
		if index==0:
			self.ModelsBox.setEnabled(True)
			self.MyTree.setEnabled(True)
		elif index == 3:
			self.MyTree.setEnabled(False)
			self.ModelsBox.setEnabled(True)
		elif index == 1 or index == 2:
			self.ModelsBox.setEnabled(False)
			self.MyTree.setEnabled(True)
#####################################################
	def setDates(self):
		files = [f for f in listdir(self.corppath)]
		dates = [f.split('_')[1].split('.json')[0] for f in files]
		first = min(dates)
		last = max(dates)
		day = first.split('-')
		self.startDE.setDate(QDate(int(day[0]),int(day[1]),int(day[2])))
		self.startDE.setMinimumDate(QDate(int(day[0]),int(day[1]),int(day[2])))
		self.endDE.setMinimumDate(QDate(int(day[0]),int(day[1]),int(day[2])))
		day = last.split('-')
		self.startDE.setMaximumDate(QDate(int(day[0]),int(day[1]),int(day[2])))
		self.endDE.setMaximumDate(QDate(int(day[0]),int(day[1]),int(day[2])))
		self.endDE.setDate(QDate(int(day[0]),int(day[1]),int(day[2])))

		def backtoauth(self):
			pass
#the neo4j object catcher when the Neo4j object is emitted
	def catchneo(self,neo4j):
		self.neo4j = neo4j
#the window main methode  agent is the twiiterAgent object the twitter api handler
	def main(self,user):
		self.show()
		neoworker = Neo4jWorker()
		neoworker.signals.neostarted.connect(lambda: self.loadLab.setText("Setting up neo4j"))
		neoworker.signals.neofinished.connect(self.setSavedModels)
		#catch neo 
		neoworker.signals.neo4jconnected.connect(self.catchneo)
		self.threadpool.start(neoworker)
		self.user = user
		if user['name']!= "admin":
			self.actionAdmin_Settings.setEnabled(False)

		try:
			self.agent= TwitterAgent(user['ck'],user['cs'],user['act'],user['acs'])
			me = self.agent.api.me()
		except tweepy.TweepError as e:
			if str(e).find('Invalid or expired token.') !=-1 :#if str(e) == "[{'code': 89, 'message': 'Invalid or expired token.'}]":
				error = QMessageBox.information(self,'Invalide Inpute','your Tokens are expired please update them  ',QMessageBox.Ok)	
			else:
				if not is_connected():
					error = QMessageBox.information(self,'HTTP ERROR',"Can't establish connexion to server please check your host",QMessageBox.Ok)
		self.setFirstV()
		self.checkforRegUp()
	def checkforRegUp(self):
		last = max([f for f in listdir(self.corppath)]).split('_')[1].split('.json')[0]
		today = dt.datetime.today()
		if (today - dt.timedelta(days=4)).strftime("%Y-%m-%d") < last:
			QMessageBox.information(self,'','No Update available',QMessageBox.Ok)
		elif (today - dt.timedelta(days=4)).strftime("%Y-%m-%d") == last:
			if(QMessageBox.information(self,"Update notifier"," A new set of data is Available Would you like to download it ",
				QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
				until = today
				since = today - dt.timedelta(days=4)
				updatewin = UpdateWin(self)
				updatewin.main(self.searcher,self.agent.get_twitter_client(),self.ontopath,since,until)
		
	def checkForUp(self):
		last = max([f for f in listdir(self.corppath)]).split('_')[1].split('.json')[0]
		today = dt.datetime.today()
		if (today - dt.timedelta(days=4)).strftime("%Y-%m-%d") < last:
			QMessageBox.information(self,'','No Update available',QMessageBox.Ok)
		elif (today - dt.timedelta(days=4)).strftime("%Y-%m-%d") == last:
			if(QMessageBox.information(self,"Update notifier"," A new set of data is Available Would you like to download it ",
				QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
				until = today
				since = today - dt.timedelta(days=4)
				updatewin = UpdateWin(self)
				updatewin.main(self.searcher,self.agent.get_twitter_client(),self.ontopath,since,until)
			else: # to fill 
				pass
		elif (today - dt.timedelta(days=4)).strftime("%Y-%m-%d") > last:
			if (today - dt.timedelta(days= 7)).strftime("%Y-%m-%d")<= last:
				if(QMessageBox.information(self,"Update notifier"," A new set of data is Available Would you like to download it ",
				QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
					until = today
					since = today - dt.timedelta(days=7)
					updatewin = UpdateWin(self)
					updatewin.main(self.searcher,self.agent.get_twitter_client(),self.ontopath,since,until)
				else:
					if(QMessageBox.information(self,"Update notifier"," A new set of data is Available Would you like to download it ",
				QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
						until = today
						since = today - dt.timedelta(days=7)
						updatewin = UpdateWin(self)
						updatewin.main(self.searcher,self.agent.get_twitter_client(),self.ontopath,since,until)
# filling the combobox with the models
	def fillbox(self):
		self.ModelsBox.clear()
		with open('docs/samsung_smartphones.txt',encoding='utf-8') as r:
			for l in r:
				self.ModelsBox.addItem(l.strip())
# method that fill the tree model with the concepets 	
	def fillTree(self):
		with open('docs/conceptetree.json',encoding='utf-8') as f :
			data = json.load(f)
		self.conceptes = QStandardItemModel()
		self.additems(self.conceptes,data["concepte"])
		self.MyTree.setSortingEnabled(True)
		self.MyTree.sortByColumn(0,Qt.AscendingOrder)
		self.MyTree.setModel(self.conceptes)
		head = self.conceptes.index(0,0)
		self.MyTree.expand(head)
#setting the analyse table
	def declareTable(self):
		self.tableView.setSortingEnabled(True)
		self.tableView.sortByColumn(0,Qt.AscendingOrder)
		self.MyTableModele = QStandardItemModel()
		self.MyTableModele.setColumnCount(5)
		header = QStandardItem("Key word")
		self.MyTableModele.setHorizontalHeaderItem(0,header)
		header = QStandardItem("Positivity")
		self.MyTableModele.setHorizontalHeaderItem(1,header)
		header = QStandardItem("Number of appovals")
		self.MyTableModele.setHorizontalHeaderItem(2,header)
		header = QStandardItem("Negativity")
		self.MyTableModele.setHorizontalHeaderItem(3,header)
		header = QStandardItem("Number of disappovals")
		self.MyTableModele.setHorizontalHeaderItem(4,header)
		self.tableView.setModel(self.MyTableModele)
# setting the loading table
	def setLoadingTable(self):
		self.Loaded.setSortingEnabled(True)
		self.Loaded.sortByColumn(0,Qt.AscendingOrder)
		self.loadingMod = QStandardItemModel()
		self.Loaded.setModel(self.loadingMod)
		self.loadingMod.setColumnCount(5)
		head = QStandardItem("Key word")
		self.loadingMod.setHorizontalHeaderItem(0,head)
		head = QStandardItem("Positivity")
		self.loadingMod.setHorizontalHeaderItem(1,head)
		head = QStandardItem("Approuves")
		self.loadingMod.setHorizontalHeaderItem(2,head)
		head = QStandardItem("Negativity")
		self.loadingMod.setHorizontalHeaderItem(3,head)
		head = QStandardItem("DisApprouves")
		self.loadingMod.setHorizontalHeaderItem(4,head)
# methode that add items to the tree
	def additems(self, parent, data):
		for c in data:
			item = QStandardItem(c["name"])
			item.setFlags(item.flags()|Qt.ItemIsTristate|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.CheckStateRole)
			item.setCheckState(Qt.Unchecked)
			parent.appendRow(item)
			self.additems(item,c["childs"])
###########################################################################
	def handleItemChecking(self,root):
		if root.checkState()== Qt.Checked:
			if root.hasChildren():
				for row in range(root.rowCount()):
					for col in range(root.columnCount()):
						son = root.child(row,col)
						son.setCheckState(Qt.Checked)
		elif root.checkState()==Qt.Unchecked:
			if root.hasChildren():
				for row in range(root.rowCount()):
					for col in range(root.columnCount()):
						son = root.child(row,col)
						son.setCheckState(Qt.Unchecked)
#iterate over the tree items
	def iterItems(self,root):
		def recurese(parent):
			for row in range(parent.rowCount()):
				for column in range(parent.columnCount()):
					child = parent.child(row,column)
					if child.checkState() == Qt.Checked:
						yield child
					if child.hasChildren():
						yield from recurese(child)
		if (root is not None) :
			return recurese(root)
#select all item of the tree view
	def selecAll(self,parent):
		def recurseAll(root):
			for row in range(root.rowCount()):
				for column in range(root.columnCount()):
					child = root.child(row,column)
					yield child
					if child.hasChildren():
						yield from recurseAll(child)
		if parent is not None:
			return recurseAll(parent)
#method that get the user selection 
	def getSelections(self):
		selectedModel = str(self.ModelsBox.currentText())
		selectedConcepte = list()
		start = self.MyTree.model().item(0,0)
		if start.checkState() == Qt.Checked:
			for item in self.selecAll(start):
				selectedConcepte.append(str(item.text()))
			return selectedModel,selectedConcepte
		else:
			for item in self.iterItems(start):
				selectedConcepte.append(str(item.text()))
			return selectedModel,selectedConcepte
#methode of actuall tendency
	def actuallTendency(self,selectedModel,selectedConcepte,NBA):
		livefetcher = TendencyWorker(self.agent,self.searcher,self.analyser,self.ontopath,self.modalfile,selectedModel,NBA)
		livefetcher.signals.progress_txt.connect(self.handllabtxt)
		livefetcher.signals.progress.connect(self.handlprogress)
		livefetcher.signals.extraerror.connect(self.errormess)
		livefetcher.signals.ended.connect(lambda:self.endofftecher(selectedModel,selectedConcepte))
		self.threadpool.start(livefetcher)
# methode reset the window after error
	def reset(self,text):
		self.SearchBtn.setEnabled(True)
		self.saveBtn.setEnabled(True)
		self.showtweetsbtn.setEnabled(False)
		self.refrechBtn.setEnabled(False)
		self.LoadBar.setEnabled(False)
		self.LoadBar.setValue(0)
		self.ModelsBox.setEnabled(True)
		self.MyTree.setEnabled(True)
		self.posBar.setValue(0)
		self.negBar.setValue(0)
		self.LoadBar.setValue(0)
		self.choiceBox.setEnabled(True)
		self.choiceBox.setCheckState(Qt.Unchecked)
		self.loadLab.setText(text)
#show off a Dialogue in case of error 
	def errormess(self,excp):
		if not is_connected():
			error = QMessageBox.information(self,'notificaton error',"please check your internet ",QMessageBox.Ok)
			self.reset('check your host and try again ')
		elif str(excp).find("[{'code': 89, 'message': 'Invalid or expired token.'}]")!=-1:
			error = QMessageBox.information(self,'notificaton error',"Expired keys please check your Tokens and Try Again ",QMessageBox.Ok)
			self.reset('')
			
		
# methode of the main corpus analyse 
	def fullfetch(self,selectedModel,selectedConcepte,NBA):
		self.LoadBar.setValue(5)
		fetcher = FullWorker(self.searcher,self.analyser,self.ontopath,self.modalfile,selectedModel,NBA)
		fetcher.signals.extraerror.connect(self.errormess)
		fetcher.signals.progress.connect(self.handlprogress)
		fetcher.signals.progress_txt.connect(self.handllabtxt)
		fetcher.signals.ended.connect(lambda:self.endofftecher(selectedModel,selectedConcepte))
		self.threadpool.start(fetcher)
# methode that is called when the analyses are done what ever thier kind 
	def endofftecher(self,selectedModel,selectedConcepte):
		with open("docs//smar.json","r",encoding="utf-8") as v:
			data = json.load(v)
		row = self.MyTableModele.rowCount()
		for  concepte in selectedConcepte:
			for element in data["concepts"]: 
				sc = str(concepte).replace(' ','').lower()
				dc = element["name"].replace('_','').lower()
				if sc == dc:
					self.MyTableModele.insertRow(row,[QStandardItem(concepte),QStandardItem(str(element['pourPos'])+"%"),QStandardItem(str(element["pos"])+" Tweets"),
						QStandardItem(str(element['pourNeg'])+"%"),QStandardItem(str(element['neg'])+" Tweets")])
		self.LoadBar.setValue(100)
		self.LoadBar.setEnabled(False)
		moyp,moyn = self.calcres(data["concepts"])
		self.posBar.setValue(moyp)
		self.negBar.setValue(moyn)
		self.loadLab.setText("Done")
		self.MyTree.setEnabled(True)
		self.ModelsBox.setEnabled(True)
		self.SearchBtn.setEnabled(True)
		self.SearchBtn.setText("Launch new search")
		self.choiceBox.setEnabled(True)
		self.saveBtn.setEnabled(True)
		self.showtweetsbtn.setEnabled(True)
		self.refrechBtn.setEnabled(True)
# setting the view to avoid selection while the processes are running 
	def setwin(self):
		self.refrechBtn.setEnabled(False)
		self.MyTree.setEnabled(False)
		self.ModelsBox.setEnabled(False)
		self.SearchBtn.setEnabled(False)

		self.choiceBox.setEnabled(False)
		self.showtweetsbtn.setEnabled(False)
		self.posBar.setValue(0)
		self.negBar.setValue(0)
		self.LoadBar.setValue(0)
		self.LoadBar.setEnabled(True)
# methode that run when search button is clicked
	def search_onClick(self):
		self.setwin()
		self.lastselectedModel,selectedConcepte = self.getSelections()
		NBA = self.NB.isChecked()
		if NBA : 
			if QMessageBox.question(self,"Validation"," You have chose the Naive Bayes Analyser, the process may take several Hours Are you sure to continue or would you prefere a quick analyse",QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:

				if self.choiceBox.checkState()==Qt.Checked:
					self.MyTableModele.clear()
					self.declareTable()
					self.actuallTendency(self.lastselectedModel,selectedConcepte,NBA)
				else:
					self.MyTableModele.clear()
					self.declareTable()
					self.fullfetch(self.lastselectedModel,selectedConcepte,NBA)
			else: 
				NBA = False
				if self.choiceBox.checkState()==Qt.Checked:
					self.MyTableModele.clear()
					self.declareTable()
					self.actuallTendency(self.lastselectedModel,selectedConcepte,NBA)
				else:
					self.MyTableModele.clear()
					self.declareTable()
					self.fullfetch(self.lastselectedModel,selectedConcepte,NBA) 
		else :
			if self.choiceBox.checkState()==Qt.Checked:
				self.MyTableModele.clear()
				self.declareTable()
				self.actuallTendency(self.lastselectedModel,selectedConcepte,NBA)
			else:
				self.MyTableModele.clear()
				self.declareTable()
				self.fullfetch(self.lastselectedModel,selectedConcepte,NBA) 
# methode that refreche the result 
	def refrechOnClick(self):
		selectedModel,selectedConcepte = self.getSelections()
		with open("docs//smar.json","r",encoding="utf-8") as v:
			data = json.load(v)
		self.MyTableModele.clear()
		self.declareTable()
		row = self.MyTableModele.rowCount()
		for  concepte in selectedConcepte:
			for element in data["concepts"]: 
				sc = str(concepte).replace(' ','').lower()
				dc = element["name"].replace('_','').lower()
				if sc == dc:
					self.MyTableModele.insertRow(row,[QStandardItem(concepte),QStandardItem(str(element['pourPos'])+"%"),QStandardItem(str(element["pos"])+" Tweets"),
						QStandardItem(str(element['pourNeg'])+"%"),QStandardItem(str(element['neg'])+" Tweets")])

# methode that show the tweets
	def showtOnClick(self):
		showWin = Tweetswin(self)
		showWin.main()
# methode called when the save button is clicked
	def save(self):
		d = time.localtime()
		today = "{}-{}-{}".format(d.tm_year,d.tm_mon,d.tm_mday)
		t = "{}:{}:{}".format(d.tm_hour,d.tm_min,d.tm_sec)
		self.neo4j.importresult(self.user['name'],self.path_smar,today,t,self.lastselectedModel)
		item = self.lastselectedModel+"/"+today+"/"+t
		item = QStandardItem(item)
		self.existingModels.insertRow(self.existingModels.rowCount(),item)	
		self.setSavedModels()
		self.setNeo4jsettings()
		self.loadLab.setText("results have been saved in neo4j")
		self.saveBtn.setEnabled(False)
# methode called when the load button is clicked	
	def load(self):
		self.posBar_2.setValue(0)
		self.negBar_2.setValue(0)
		selectedModel,selectedConcepte = self.getSelections()
		model = str(self.SavedModels.currentText()).split("/")
		if model[0] != 'Select':
			if self.user['name']!="admin":
				sm,results = self.neo4j.loadresult(self.user['name'],model[1],model[2],model[0])
			else: 
				sm,results = self.neo4j.loadresult(model[3],model[1],model[2],model[0])
			self.loadingMod.clear()
			self.setLoadingTable()
			if results != False:
				if sm["name"] == model[0]:
					self.loadingMod.insertRow(0,[QStandardItem(results["model"]),QStandardItem(str(sm['pourPos'])+"%"), QStandardItem(str(sm['pos'])),QStandardItem(str(sm['pourNeg'])+"%"),QStandardItem(str(sm['neg']))])
					row = self.loadingMod.rowCount()
					if results['concepts']!=[]:
						for c in selectedConcepte:
							for e in results["concepts"]:
								cm = c.replace(' ','').lower()
								em = e["name"].replace('_','').lower()
								if cm == em:
									self.loadingMod.insertRow(row,[QStandardItem(c.upper()),
										QStandardItem(str(e["pourPos"])+"%"),QStandardItem(str(e["pos"])+" tweets"),
										QStandardItem(str(e["pourNeg"])+"%"),QStandardItem(str(e["neg"])+" tweets")])
									row = self.loadingMod.rowCount()

						moyp,moyn = self.calcres(results["concepts"])
						self.posBar_2.setValue(moyp)
						self.negBar_2.setValue(moyn)
					else:
						self.loadLab.setText("no match results have been found check your selection")	
				else:
					self.loadLab.setText("inexistant model")
			else:
				self.loadLab.setText("no match found")
		else: 
			mess = QMessageBox.information(self,"No Model selected","please select a model",QMessageBox.Cancel|QMessageBox.Ok)
# methode the calculate the result of the product
	def calcres(self,reslist):
		try:
			size = len(reslist)
			totp = 0 
			pos = 0
			totn = 0 
			neg = 0
			for e in reslist:
				if (e["pourPos"]!=0 and e["pourNeg"]!=0) :
					totp+=e["pourPos"]
					totn+=e["pourNeg"]
					pos+=1
					neg+=1
			moyp = round(totp/pos,2)
			moyn = round(totn/neg,2)
			return moyp,moyn
		except Exception as e:
			#err = QMessageBox.information(self,'Empty file ','No Result Found',QMessageBox.Ok)
			return 0,0
#**************************************************	
# methode that handles the progress bar signals 
	def handlprogress(self,n):
		self.LoadBar.setValue(n)
#methode that handles the status bar text
	def handllabtxt(self,s):
		self.loadLab.setText(s)
#methode that sets the combobox with the existing models already analysed in the neo4j
	def setSavedModels(self):
		self.existingModels = QStandardItemModel()
		row = self.existingModels.rowCount()
		self.existingModels.insertRow(row,QStandardItem('Select'))
		models = self.neo4j.load_user_mod(self.user['name'])
		row = self.existingModels.rowCount()
		for m in models:
			item = QStandardItem(m)
			self.existingModels.insertRow(row,item)
		self.SavedModels.setModel(self.existingModels)
		self.histModlesBox.setModel(self.existingModels)
		self.prod2.setModel(self.existingModels)
		self.setNeo4jsettings()
		self.loadLab.setText("Neo4j is Ready")
	def setNeo4jsettings(self):
		if self.user['name'] !="admin":
			analyses = self.neo4j.loadAnalyses(self.user['name'])
			self.existingAnalyses = QStandardItemModel()
			self.existingAnalyses.setColumnCount(3)
			self.existingAnalyses.setHorizontalHeaderItem(0, QStandardItem("Model"))
			self.existingAnalyses.setHorizontalHeaderItem(1, QStandardItem("Date"))
			self.existingAnalyses.setHorizontalHeaderItem(2,QStandardItem('Time'))
			self.DbPicture.setModel(self.existingAnalyses)
			rowc = self.existingAnalyses.rowCount()
			for a in analyses:
				self.existingAnalyses.insertRow(rowc,[QStandardItem(a['model']),QStandardItem(a['date']),QStandardItem(a['time'])])
		else:
			analyses = self.neo4j.loadAnalyses(self.user['name'])
			self.existingAnalyses = QStandardItemModel()
			self.existingAnalyses.setColumnCount(4)
			self.existingAnalyses.setHorizontalHeaderItem(0, QStandardItem("Model"))
			self.existingAnalyses.setHorizontalHeaderItem(1, QStandardItem("Date"))
			self.existingAnalyses.setHorizontalHeaderItem(2,QStandardItem('Time'))
			self.existingAnalyses.setHorizontalHeaderItem(3,QStandardItem('user'))
			self.DbPicture.setModel(self.existingAnalyses)
			rowc = self.existingAnalyses.rowCount()
			for a in analyses:
				self.existingAnalyses.insertRow(rowc,[QStandardItem(a['model']),QStandardItem(a['date']),QStandardItem(a['time']),QStandardItem(a['user'])])
	def deleteOnClick(self):
		if ( QMessageBox.question(self,"Delete","Are you sure you want to delete this item",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
			rows = self.DbPicture.selectionModel().selectedRows()
			for r in rows: 
				row = self.existingAnalyses.takeRow(r.row())
			strow = []
			for item in row:
				strow.append(str(item.text()))
			if self.user['name'] !="admin":
				self.neo4j.deleteAnalyse(self.user['name'],strow[1],strow[2])
			else:
				self.neo4j.deleteAnalyse(strow[3],strow[1],strow[2])
			self.setSavedModels()
			self.setNeo4jsettings()
###############################################################		
#########################
#drawing section 
	def drawHist(self):
		selectedModel,selectedConcepte = self.getSelections()
		choice = self.graphChoice.currentText()
		model1 = str(self.histModlesBox.currentText()).split("/")
		model2= str(self.prod2.currentText()).split('/')
		if model1[0] !='Select' and model2[0] != 'Select': 
			if self.user["name"] != "admin":
				sm1,result = self.neo4j.loadresult(self.user['name'],model1[1],model1[2],model1[0])
				sm2,result2 = self.neo4j.loadresult(self.user['name'],model2[1],model2[2],model2[0])
			else: 
				sm1,result = self.neo4j.loadresult(model1[3],model1[1],model1[2],model1[0])
				sm2,result2 = self.neo4j.loadresult(model2[3],model2[1],model2[2],model2[0])

			raw_data = {
			'name':[],
			'pos':[],
			'neg':[]}
			raw_data2 = {
			'name':[],
			'pos':[],
			'neg':[]}
			w = 0.25
			self.plotWidget.canvas.ax.clear()
			if result['concepts']!=[] and result2['concepts']!=[] and selectedConcepte !=[] :
				for c in selectedConcepte:
					for e in result["concepts"]:
						cm = c.replace(' ','').lower()
						em = e["name"].replace('_','').lower()
						if cm ==em: 
							raw_data["name"].append(e['name'])
							raw_data["pos"].append(e["pourPos"])
							raw_data["neg"].append(e["pourNeg"])
			
					for e in result2["concepts"]:
						cm = c.replace(' ','').lower()
						em = e["name"].replace('_','').lower()
						if cm ==em: 
							raw_data2["name"].append(e['name'])
							raw_data2["pos"].append(e["pourPos"])
							raw_data2["neg"].append(e["pourNeg"])

				df = pd.DataFrame(raw_data,columns = ['name','pos','neg'])
				df2 = pd.DataFrame(raw_data2,columns = ['name','pos','neg'])
				pos = list(range(len(df["name"])))
				if choice =='Both':
					self.plotWidget.canvas.ax.bar(pos,df['pos'],
						width=w,color='#0565d9')
					self.plotWidget.canvas.ax.bar([p+w for p in pos]
						,df['neg'],width=w,color='#af0d0d')
					self.plotWidget.canvas.ax.bar([p+w*2 for p in pos],df2['pos'],width=w,color='#15c0ef')
					self.plotWidget.canvas.ax.bar([p+w*3 for p in pos],df2['neg'],width=w,color='#c700ff')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks([p+1.5*w for p in pos])
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df['name'])

					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model1[0]+"pos",model1[0]+"neg",model2[0]+"pos",model2[0]+"neg"], loc='upper right')
					self.plotWidget.canvas.ax.set_title("Scores of "+model1[0]+" and "+model2[0])
					self.plotWidget.canvas.draw()		
				elif choice =='Positivity':
					self.plotWidget.canvas.ax.bar(pos,df['pos'],
						width=w,color='#0565d9')
					self.plotWidget.canvas.ax.bar([p+w for p in pos],df2['pos'],width=w,color='#15c0ef')
				
				#set the position of the x tick
					self.plotWidget.canvas.ax.set_xticks([p+0.5*w for p in pos])
				# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df['name'])

					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model1[0],model2[0]], loc='upper right')
					self.plotWidget.canvas.ax.set_title("positive scores of "+model1[0]+" And "+model2[0])
					self.plotWidget.canvas.draw()
				elif choice == 'Negativity':

					self.plotWidget.canvas.ax.bar([p for p in pos]
						,df['neg'],width=w,color='#af0d0d')
					self.plotWidget.canvas.ax.bar([p+w for p in pos],df2['neg'],width=w,color='#c700ff')
				#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks([p+0.5*w for p in pos])
				# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df['name'])

					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model1[0],model2[0]], loc='upper right')
					self.plotWidget.canvas.ax.set_title("Negative scores of "+model1[0]+" and "+model2[0])
					self.plotWidget.canvas.draw()
				
			else:
				mess = QMessageBox.information(self,'invalide input','please select a concepte',QMessageBox.Ok)
		elif model1[0]!='Select':
			if self.user["name"] != "admin":
				sm1,result = self.neo4j.loadresult(self.user['name'],model1[1],model1[2],model1[0])
			else: 
				sm1,result = self.neo4j.loadresult(model1[3],model1[1],model1[2],model1[0])
			raw_data = {
			'name':[],
			'pos':[],
			'neg':[]}
			w = 0.25
			self.plotWidget.canvas.ax.clear()
			if result['concepts']!=[] and selectedConcepte !=[] :
				for c in selectedConcepte:
					for e in result["concepts"]:
						cm = c.replace(' ','').lower()
						em = e["name"].replace('_','').lower()
						if cm ==em: 
							raw_data["name"].append(e['name'])
							raw_data["pos"].append(e["pourPos"])
							raw_data["neg"].append(e["pourNeg"])
				df = pd.DataFrame(raw_data,columns = ['name','pos','neg'])
				pos = list(range(len(df["name"])))
				if choice =='Both':
					self.plotWidget.canvas.ax.bar(pos,df['pos'],
						width=w,color='#0565d9')
					self.plotWidget.canvas.ax.bar([p+w for p in pos]
						,df['neg'],width=w,color='#af0d0d')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks([p+0.5*w for p in pos])
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df['name'])
					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model1[0]+" pos",model1[0]+" neg"], loc='upper right')
					self.plotWidget.canvas.ax.set_title("scores of  "+model1[0]+" on the "+model1[1])
					self.plotWidget.canvas.draw()


				elif choice == 'Positivity':
					self.plotWidget.canvas.ax.bar(pos,df['pos'],
						width=w,color='#0565d9')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks(pos)
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df['name'])
					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model1[0]], loc='upper right')
					self.plotWidget.canvas.ax.set_title("positive scores of  "+model1[0]+" on the "+model1[1])
					self.plotWidget.canvas.draw()

				elif choice=='Negativity':
					
					self.plotWidget.canvas.ax.bar(pos,df['neg'],width=w,color='#af0d0d')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks(pos)
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df['name'])
					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model1[0]], loc='upper right')
					self.plotWidget.canvas.ax.set_title("negative scores of  "+model1[0]+" on the "+model1[1])
					self.plotWidget.canvas.draw()

				
			else:
				mess = QMessageBox.information(self,'invalide input','please select a concepte',QMessageBox.Ok)
		elif model2[0]!='Select':
			if self.user["name"] != "admin":
				sm2,result2 = self.neo4j.loadresult(self.user['name'],model2[1],model2[2],model2[0])
			else: 
				sm2,result2 = self.neo4j.loadresult(model2[3],model2[1],model2[2],model2[0])
			raw_data2 = {
			'name':[],
			'pos':[],
			'neg':[]}
			w = 0.25
			self.plotWidget.canvas.ax.clear()
			if result2['concepts']!=[] and selectedConcepte !=[] :
				for c in selectedConcepte:	
					for e in result2["concepts"]:
						cm = c.replace(' ','').lower()
						em = e["name"].replace('_','').lower()
						if cm ==em: 
							raw_data2["name"].append(e['name'])
							raw_data2["pos"].append(e["pourPos"])
							raw_data2["neg"].append(e["pourNeg"])
				df2 = pd.DataFrame(raw_data2,columns = ['name','pos','neg'])
				pos = list(range(len(df2["name"])))
				if choice=='Both':
					self.plotWidget.canvas.ax.bar(pos,df2['pos'],width=w,color='#15c0ef')
					self.plotWidget.canvas.ax.bar([p+w for p in pos],df2['neg'],width=w,color='#c700ff')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks([p+0.5*w for p in pos])
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df2['name'])
					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model2[0]+" pos",model2[0]+" neg"], loc='upper right')
					self.plotWidget.canvas.ax.set_title("scores of  "+model2[0]+" on the "+model2[1])
					self.plotWidget.canvas.draw()
					
				elif choice == 'Positivity':
					self.plotWidget.canvas.ax.bar(pos,df2['pos'],width=w,color='#15c0ef')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks(pos)
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df2['name'])
					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model2[0]], loc='upper right')
					self.plotWidget.canvas.ax.set_title("positive scores of  "+model2[0]+" on the"+model2[1])
					self.plotWidget.canvas.draw()
					

				elif choice=='Negativity':
					self.plotWidget.canvas.ax.bar(pos,df2['neg'],width=w,color='#c700ff')
					#set the position of the x ticks
					self.plotWidget.canvas.ax.set_xticks(pos)
					# set the labels for the x ticks
					self.plotWidget.canvas.ax.set_xticklabels(df2['name'])
					for label in self.plotWidget.canvas.ax.xaxis.get_ticklabels():
						label.set_rotation(55)
						label.set_fontsize(6)
					#print(help(label))
					self.plotWidget.canvas.ax.legend([model2[0]], loc='upper right')
					self.plotWidget.canvas.ax.set_title("negative scores of  "+model2[0]+" on the "+model2[1])
					self.plotWidget.canvas.draw()
					
			else:
				mess = QMessageBox.information(self,'invalide input','please select a concepte',QMessageBox.Ok)
		else:
			mess = QMessageBox.information(self,'invalide input','please select your models ',QMessageBox.Ok)
#plot gram 
	def showp_onclick(self):
		selectedModel,selectedConcepte =self.getSelections()
		dat = self.startDE.date()
		begin =dt.date(dat.year(),dat.month(),dat.day())
		dat = self.endDE.date()
		end =dt.date(dat.year(),dat.month(),dat.day())
		self.showp.setEnabled(False)
		self.saveplot.setEnabled(False)
		self.plotChoice.setEnabled(False)
		self.ModelsBox.setEnabled(False)
		plotdrawer = PlotWorker(self.searcher,self.analyser,self.ontopath,selectedModel,self.modalfile,self.corppath,self.graphecache,begin,end)
		plotdrawer.signals.caldone.connect(self.catchaxes)
		plotdrawer.signals.progress.connect(self.handlprogress)
		self.threadpool.start(plotdrawer)
	
	def catchaxes(self,title):
		axes = []
		files = [f for f in listdir(self.graphecache)]
		self.LoadBar.setValue(91)
		for f in files:
			date = f.split('.json')[0]
			with open(self.graphecache+f,'r',encoding='utf-8') as r:
				temp = json.load(r)
			moyp,moyn = self.calcres(temp['concepts'])
			axes.append({'date':date,'pos':moyp,'neg':moyn})
			os.remove(self.graphecache+f)
		self.plotWidget2.canvas.ax.clear()
		pos = range(len(axes))
		#case selected both
		if self.plotChoice.currentText()== 'Both':
			self.plotWidget2.canvas.ax.plot(pos,[e['pos'] for e in axes],color='b')
			self.plotWidget2.canvas.ax.plot(pos,[e['neg'] for e in axes],color='r')
			self.plotWidget2.canvas.ax.set_xticks(pos)
			self.plotWidget2.canvas.ax.set_xticklabels([e['date'] for e in axes])
			for label in self.plotWidget2.canvas.ax.xaxis.get_ticklabels():
				label.set_rotation(45)
				label.set_fontsize(5)
			self.plotWidget2.canvas.ax.grid(True,linestyle='-',linewidth=1)
			self.plotWidget2.canvas.ax.legend(['positive','negative'],loc ='upper right')
			self.plotWidget2.canvas.ax.set_title("Opinions Evolution of the "+title)
		# case selected only positive
		elif self.plotChoice.currentText() == "Positive":
			self.plotWidget2.canvas.ax.plot(pos,[e['pos'] for e in axes],color='b')
			self.plotWidget2.canvas.ax.set_xticks(pos)
			self.plotWidget2.canvas.ax.set_xticklabels([e['date'] for e in axes])
			for label in self.plotWidget2.canvas.ax.xaxis.get_ticklabels():
				label.set_rotation(45)
				label.set_fontsize(5)
			self.plotWidget2.canvas.ax.grid(True,linestyle='-',linewidth=1)
			self.plotWidget2.canvas.ax.legend(['positive'],loc ='upper right')
			self.plotWidget2.canvas.ax.set_title("Opinions Evolution of the "+title)
		else:#else only negative 
			self.plotWidget2.canvas.ax.plot(pos,[e['neg'] for e in axes],color='r')
			self.plotWidget2.canvas.ax.set_xticks(pos)
			self.plotWidget2.canvas.ax.set_xticklabels([e['date'] for e in axes])
			for label in self.plotWidget2.canvas.ax.xaxis.get_ticklabels():
				label.set_rotation(45)
				label.set_fontsize(5)
			self.plotWidget2.canvas.ax.grid(True,linestyle='-',linewidth=1)
			self.plotWidget2.canvas.ax.legend(['negative'],loc ='upper right')
			self.plotWidget2.canvas.ax.set_title("Opinions Evolution of the "+title)
		
		self.plotWidget2.canvas.draw()
		self.LoadBar.setValue(100)
		self.showp.setEnabled(True)
		self.saveplot.setEnabled(True)
		self.ModelsBox.setEnabled(True)
		self.plotChoice.setEnabled(True)
		#self.removeGrapheCache()
	def removeGrapheCache(self):
		files = [f for f in listdir(self.graphecache)]
		for f in files:
			os.remove(self.graphecache+f)
#saving the graph 
	def saveFig(self):
		path = QFileDialog.getSaveFileName(self,'Save File',self.savegraphpath,"Images (*.png *.svg *.pdf)")
		self.plotWidget.canvas.fig.savefig(path[0])
	def savePlot_Onclick(self):
		path = QFileDialog.getSaveFileName(self,'Save File',self.savegraphpath,"Images (*.png *.svg *.pdf)")
		self.plotWidget2.canvas.fig.savefig(path[0])
##class for the show tweets window
class Tweetswin(QDialog,Ui_ShowTweets):
	def __init__(self,parent=None):
		super(Tweetswin,self).__init__(parent)
		self.setupUi(self)
		self.Fill_Tweets()
	def main(self):
		self.show()
	def Fill_Tweets(self):
		model = QStandardItemModel()
		model.setColumnCount(4)
		item = QStandardItem("Text")
		model.setHorizontalHeaderItem(0,item)
		item = QStandardItem("Mentions")
		model.setHorizontalHeaderItem(1,item)
		item = QStandardItem('Polarity')
		model.setHorizontalHeaderItem(2,item)
		item = QStandardItem('Date')
		model.setHorizontalHeaderItem(3,item)
		with open("cache/cleanedTweets.json",'r',encoding='utf-8') as clean:
			data  = json.load(clean)
		rowc = model.rowCount()
		for t in data['tweets']:
			mentions = str()
			for e in t['mention']:
				mentions = e +', '+mentions 
			model.insertRow(rowc,[QStandardItem(str(t['text'])),QStandardItem(mentions),QStandardItem(t['label']),QStandardItem(t['created_at'][:10])])
		self.MyTweets.setModel(model)


################################################################################
class PlotWorker(QRunnable):
	def __init__(self,searcher,analyser,ontopath,selectedModel,modalfile,corppath,exitpath,begin,end):
		super(PlotWorker,self).__init__()
		self.signals = WrokerSignals()
		self.ontopath = ontopath
		self.selectedModel = selectedModel
		self.searcher = searcher
		self.analyser = analyser
		self.modalfile = modalfile 
		self.corppath = corppath
		self.exitpath = exitpath
		self.begin = begin
		self.end = end
	@pyqtSlot()
	def run(self):
		self.signals.progress.emit(10)
		files = [f for f in listdir(self.corppath)]
		todraw = []
		for f in files: 
			fd = f.split('_')[1].split('.json')[0]
			fdt = dt.date(int(fd[:4]),int(fd[5:7]),int(fd[8:]))
			if (fdt >= self.begin) and (fdt <= self.end) : 
				todraw.append({'date':fd,'path':self.corppath+f})
		yx = []
		self.signals.progress.emit(20)
		bar = 20
		c = 1
		for e in todraw:
			exit= self.exitpath+e['date']+".json"
			file = self.searcher.extractModel(self.selectedModel,e['path'],exit)
			ef = self.searcher.elaguerFichier(self.ontopath,file)
			etf = self.searcher.etiqueter(ef,self.ontopath)
			cf = self.searcher.cleanTweets(etf)
			cf = self.analyser.analizeFile(cf)
			self.analyser.negativityAndPositivity(cf,self.ontopath,self.searcher)
			self.analyser.influenceResults(self.modalfile)
			with open(self.modalfile,'r',encoding='utf-8') as read:
				temp = json.load(read)
			temp = str(json.dumps(temp,indent=4))
			with open(exit,'w',encoding='utf-8') as w:
				w.write(temp)
			pr = bar + (c*100/len(todraw))/2
			self.signals.progress.emit(pr)
			c+=1
		self.signals.progress.emit(90)
		self.signals.caldone.emit(self.selectedModel)
#worker of neo4j handle the connexion to data base 
class Neo4jWorker(QRunnable):
	def __init__(self):
		super(Neo4jWorker,self).__init__()
		self.signals = WrokerSignals()
	@pyqtSlot()
	def run(self):
		try:
			self.signals.neostarted.emit()
			neo4j = Neo4j("bolt://127.0.0.1:7687","thbob","2305")
			self.signals.neo4jconnected.emit(neo4j)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.neoerror.emit((exctype,value,traceback.format_exc()))
		finally:
			self.signals.neofinished.emit()
# worker of the main corpus process
class FullWorker(QRunnable):
	def __init__(self,searcher,analyser,ontopath,modalfile,selectedModel,NBA):
		super(FullWorker,self).__init__()
		self.signals = WrokerSignals()
		self.ontopath=ontopath
		self.modalfile = modalfile
		self.searcher = searcher
		self.analyser = analyser
		self.selectedModel = selectedModel
		self.NBA = NBA
	@pyqtSlot()
	def run(self): #should work now
		try:
			self.signals.progress_txt.emit("lunching analysis")
			file = self.searcher.fullExtraction(self.selectedModel,'cache/file.json')
			elaguedfile = self.searcher.elaguerFichier(self.ontopath,file)
			self.signals.progress.emit(9)
			etiquettedfile = self.searcher.etiqueter(elaguedfile,self.ontopath)
			self.signals.progress_txt.emit("Tweets have been etiquetted")
			self.signals.progress.emit(40)
			cleanedfile = self.searcher.cleanTweets(etiquettedfile)
			self.signals.progress.emit(60)
			self.signals.progress_txt.emit("Tweets have been cleaned")
			if self.NBA:
				cleanedfile = self.analyser.analizeFileBayes(cleanedfile)
				self.signals.progress.emit(70)
			else:	
				cleanedfile = self.analyser.analizeFile(cleanedfile)
				self.signals.progress.emit(70)
			self.analyser.negativityAndPositivity(cleanedfile,self.ontopath,self.searcher)
			self.signals.progress.emit(80)
			self.analyser.influenceResults(self.modalfile)
			self.signals.progress.emit(99)
			self.signals.progress_txt.emit("Scores have been Calculated please wait..")
			self.signals.ended.emit()
		except Exception as e :
			exctype, value = sys.exc_info()[:2]
			self.signals.extraerror.emit((exctype,value,traceback.format_exc()))
# worker of the actuall tendency 
class TendencyWorker(QRunnable):
	def __init__(self,agent,searcher,analyser,ontopath,modalfile,selectedModel,NBA):
		super(TendencyWorker,self).__init__()
		self.signals = WrokerSignals()
		self.ontopath=ontopath
		self.modalfile=modalfile
		self.selectedModel = selectedModel
		self.agent = agent
		self.analyser = analyser
		self.searcher = searcher
		self.NBA = NBA
	@pyqtSlot()
	def run(self):
		try:
			self.signals.progress_txt.emit("Starting...")
			self.signals.progress_txt.emit("Running Live Extraction")
			#self.agent = TwitterAgent()
			self.api = self.agent.get_twitter_client()
			tweets = self.searcher.searchCle(self.selectedModel,self.api)
			self.signals.progress.emit(5)
			elaguedfile = self.searcher.elaguerCursor(self.ontopath, tweets)
			self.signals.progress.emit(20)
			self.signals.progress_txt.emit("EXTRACTION DONE wait for Analysis")
			etiquettedfile = self.searcher.etiqueter(elaguedfile,self.ontopath)
			self.signals.progress.emit(30)
			self.signals.progress_txt.emit("Tweets have been Etiqutted")
			cleanedfile = self.searcher.cleanTweets(etiquettedfile)
			self.signals.progress_txt.emit("Tweets have been cleaned")
			self.signals.progress.emit(40)
			if self.NBA:
				cleanedfile = self.analyser.analizeFileBayes(cleanedfile)
				self.signals.progress.emit(60)
			else:	
				cleanedfile = self.analyser.analizeFile(cleanedfile)
				self.signals.progress.emit(60)
			
			self.analyser.negativityAndPositivity(cleanedfile,self.ontopath,self.searcher)
			self.signals.progress.emit(70)
			self.analyser.influenceResults(self.modalfile)
			self.signals.progress.emit(90)
			self.signals.progress_txt.emit("Scores have been Calculated please wait..")
			self.signals.ended.emit()
		except Exception as e :
			exctype, value = sys.exc_info()[:2]
			self.signals.extraerror.emit((exctype,value,traceback.format_exc()))
# class of the signals 
class WrokerSignals(QObject):
	neo4jconnected = pyqtSignal(object)	
	neostarted = pyqtSignal()
	neofinished = pyqtSignal()
	neoerror = pyqtSignal(tuple)
	extraerror = pyqtSignal(tuple)
	progress = pyqtSignal(int)
	progress_txt = pyqtSignal(object)
	ended = pyqtSignal()
	succsubmit = pyqtSignal(object)
	caldone = pyqtSignal(object)
	extractionStart = pyqtSignal()
	extractionNotif  = pyqtSignal(object)
	extractionEnd = pyqtSignal()
####################################################################################################
# the following classes are for the login and the sign in GUI 
class AdminS(QDialog,Ui_Admins):
	def __init__(self,parent=None):
		super(AdminS,self).__init__(parent)
		self.setupUi(self)
		self.deleteU.clicked.connect(self.delete_Onclick)
		self.removeC.clicked.connect(self.removec_onclick)
		self.Add.clicked.connect(self.addOnclick)
		self.removeModel.clicked.connect(self.removeModelOnclick)
		self.apply.clicked.connect(self.applyOn)
	def main(self,neo4j,path):
		self.neo4j = neo4j
		self.path = path
		self.decTables()
		self.fillTables()
		self.show()
	def decTables(self):
		self.usersM = QStandardItemModel()
		self.usersM.setColumnCount(2)
		item = QStandardItem("user")
		self.usersM.setHorizontalHeaderItem(0,item)
		item = QStandardItem("Number of anlyzes")
		self.usersM.setHorizontalHeaderItem(1,item)
		self.usersT.setModel(self.usersM)
		#
		self.corpM = QStandardItemModel()
		self.corpM.setColumnCount(2)
		item = QStandardItem("Date")
		self.corpM.setHorizontalHeaderItem(0,item)
		item = QStandardItem("Size")
		self.corpM.setHorizontalHeaderItem(1,item)
		self.tableView.setModel(self.corpM)
		#
		self.models = QStandardItemModel()
		self.models.setColumnCount(1)
		self.models.setHorizontalHeaderItem(0,QStandardItem("Model Name"))
		self.modtable.setModel(self.models)
#FILLING THE TABLES
	def fillTables(self):
		def convert_bytes(num):
			for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
				if num < 1024.0:
					return "%3.1f %s" % (num, x)
				num /= 1024.0
		#tab1
		users = self.neo4j.allusers()
		rowc = self.usersM.rowCount()
		for u in users:
			item1 = QStandardItem(u['name'])
			item2 = QStandardItem(str(u['nba']))
			self.usersM.insertRow(rowc,[item1,item2])
		#tab2
		files = [ f for f in listdir(self.path)]
		files.sort(reverse=True)
		row = self.corpM.rowCount()
		for f in files:
			item1 = QStandardItem(f.split('_')[1].split('.json')[0])
			info = os.stat(self.path+f)
			size = convert_bytes(info.st_size)
			item2 =QStandardItem(size)
			self.corpM.insertRow(row,[item1,item2])
		#tab3
		with open("docs/samsung_smartphones.txt","r",encoding="utf-8") as read:
			row = self.models.rowCount()
			for l in read:
				self.models.insertRow(row,QStandardItem(l.strip()))
	
	def addOnclick(self):
		if self.newModel.text() !="":
			self.models.insertRow(self.models.rowCount(),QStandardItem(self.newModel.text()))
	def removeModelOnclick(self):
		if(QMessageBox.question(self,"Delete","Are you sure you want to delete this Model ?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
			indexs = self.modtable.selectionModel().selectedRows()
			rows = []
			for index in sorted(indexs,reverse=False):
				rows.append(self.models.takeRow(index.row()))
#DELETE ON CLICK
	def delete_Onclick(self):
		if(QMessageBox.question(self,"Delete","Are you sure you want to delete this user ?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
			rows = self.usersT.selectionModel().selectedRows()
			for r in rows:
				row = self.usersM.takeRow(r.row())
			strow = []
			for item in row: 
				strow.append(str(item.text()))
			self.neo4j.deleteUser(strow[0])
			self.decTables()
			self.fillTables()
	def removec_onclick(self):
		if(QMessageBox.question(self,"Delete","Are you sure you want to delete these DATA ?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
			indexs = self.tableView.selectionModel().selectedRows()
			rows = []
			for index in sorted(indexs,reverse=False):
				rows.append(self.corpM.takeRow(index.row()))
			files = [ f for f in listdir(self.path)]
			for f in files:
				for row in rows:
					if f.find(row[0].text())>=0:
						os.remove(self.path+f)
			self.decTables()
			self.fillTables()
	def applyOn(self):
		mymodels = []
		for row in range(self.models.rowCount()):
			mymodels.append(str(self.models.item(row,0).text()))
		mymodels.sort(reverse=True)
		with open("docs/samsung_smartphones.txt","w",encoding="utf-8") as w:
			for m in mymodels:	
				w.write(m+"\n")
		self.accept()
############################################
class MyAcm(QDialog,Ui_Acm):
	def __init__(self,parent=None):
		super(MyAcm,self).__init__(parent)
		self.setupUi(self)
		self.Ok.clicked.connect(lambda:self.close())
		self.Cancel.clicked.connect(lambda:self.close())
		self.Npwd.clicked.connect(lambda:self.resetEdit(self.Npwd))
		self.Npwd.clicked.connect(lambda:self.resetEdit(self.Npwdc))
		self.ck.clicked.connect(lambda:self.resetEdit(self.ck))
		self.cs.clicked.connect(lambda:self.resetEdit(self.cs))
		self.act.clicked.connect(lambda:self.resetEdit(self.act))
		self.acs.clicked.connect(lambda:self.resetEdit(self.acs))
		self.submit.clicked.connect(self.submitOnclick)
		self.gapi.clicked.connect(self.gapi_onclick)
		self.confrimbtn.clicked.connect(self.confirmOnclick)
	def setError(self,edit,string):
		edit.setText("")
		edit.setPlaceholderText(string)
		edit.setStyleSheet(ERROREDIT)
	def resetEdit(self,edit):
		edit.setStyleSheet(LEDIT)
	def validate(self,edit,text):
		edit.setText("")
		edit.setPlaceholderText(text)
		edit.setStyleSheet(VALIDLINE)
	def main(self,neo4j,user):
		self.show()
		self.neo4j = neo4j
		self.user = user
		if user['name'] == 'admin':
			self.confrimbtn.setEnabled(False)	
		else:
			
			res = self.neo4j.luser(user['name'])
			s = "name: {}\nnumber of analyzes: {}\nconsumer key: {}\nconsumer secret: {}\naccess token: {}\naccess secret: {}".format(user['name'],res[0]['nba'],user['ck'],user['cs'],user['act'],user['acs'])
			self.userinfo.setPlainText(s)
	def gapi_onclick(self):
		tokens = [(self.ck,str(self.ck.text()).strip()),(self.cs,str(self.cs.text()).strip()),(self.act,str(self.act.text()).strip()),(self.acs,str(self.acs.text()).strip())]
		b = False
		tempo = {}
		try:
			
			for obj,txt in tokens:
				if txt == "":
					raise SigninError("BLANC AREA DENIED")
				else: 
					tempo[obj.objectName()] = txt
			#print(tempo)
			b = True 
		except SigninError as e :
			if str(e).find("BLANC AREA DENIED")!= -1:
				for obj,txt in tokens:
					if txt =="":
						self.setError(obj,'fill the blanks')
		if b == True : 
			try:
				
				#self.agent = TwitterAgent(tempo['ck'],tempo['cs'],tempo['act'],tempo['acs'])
				#if self.agent.get_twitter_client().me():
				test = TwitterAgent(tempo['ck'],tempo['cs'],tempo['act'],tempo['acs']) 
				me = test.api.me()
				succs = QMessageBox.information(self,'Success','Tokens have been Updated Successfully',QMessageBox.Ok)
				user['ck']=tempo['ck']
				user['cs']= tempo['cs']
				user['act'] = tempo['act']
				user['acs']= tempo['acs']
				self.neo4j.updateTokens(user)
				for obj,txt in tokens: 
					self.validate(obj,"Token updated")
				 
					#raise SigninErro('ERROR')

			except Exception as te:
				if str(te) == "[{'code': 89, 'message': 'Invalid or expired token.'}]":
					error = QMessageBox.information(self,'Invalide Inpute','Invalide or expired Tokens',QMessageBox.Ok)	
					for obj,txt in tokens:
						self.setError(obj,"Expired")
				else:
					if not is_connected():
						error = QMessageBox.information(self,'HTTP ERROR',"please check your host and try again",QMessageBox.Ok)
			#except SigninError as se:
				#if str(se).find("ERROR")!=-1:
					#self.setError(self.ck,"Expired")
			
	def confirmOnclick(self):
		if self.pwd.text()== self.user['pwd']:
			if(QMessageBox.question(self,"Delete","Are you sure you want to delete your Account ?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes):
				self.neo4j.deleteUser(user['name'])
				sys.exit()
############
	def submitOnclick(self):
		pwd = str(self.Npwd.text())
		pwdc = str(self.Npwdc.text())
		if re.search(r"^[a-zA-Z][a-zA-Z0-9_]{5,32}",pwd) is None:
			self.setError(self.Npwd,"wrong password format")

		elif pwd != pwdc:
			self.setError(self.Npwdc,"password don't match")
		else: 
			user["pwd"]= pwd
			self.neo4j.updatePass(user)
			self.validate(self.Npwd,"Password Changed Successfully")
			self.validate(self.Npwdc,"")

#loging window
class logingWindow(QDialog,Ui_AuthWindow):
# the loging window init
	def __init__(self,parent=None):
		super(logingWindow,self).__init__(parent)
		self.setupUi(self)
		self.signals = WrokerSignals()
		self.login.clicked.connect(self.login_clicked)
		self.signin.clicked.connect(self.signin_clicked)
		self.switch.clicked.connect(lambda:self.switch_clicked(self.pwd))
		self.id.clicked.connect(lambda:self.resetEdit(self.id))
		self.pwd.clicked.connect(lambda:self.resetEdit(self.pwd))
		self.signals.succsubmit.connect(self.firstlog)
		self.threadpool = QThreadPool()
#the loggin window neo4j catcher
	def catchneo(self,neo4j):
		self.neo4j = neo4j
	def firstlog(self,user):
		mainApp = MainWindow(self)
		mainApp.main(user)
#loggin button clicked
	def login_clicked(self):
		username = self.id.text()
		passw = self.pwd.text()
		user = self.neo4j.loadUser(username)
		if user == {}: 
			self.setError(self.id,"inexistant user")
			self.setError(self.pwd,"Invalide  ")
		elif passw == user['pwd']:
			mainApp = MainWindow(self)
			mainApp.main(user)			
			#self.accept()
			self.hide()
		else:
			self.setError(self.pwd,"Wrong password ")
#switching the LineEdits style according if an error occured
	def setError(self,edit,string):
		edit.setText("")
		edit.setPlaceholderText(string)
		edit.setStyleSheet(ERROREDIT)
#reseting the lineEdits to normal		
	def resetEdit(self,edit):
		edit.setStyleSheet(LEDIT)
# show hide password
	def switch_clicked(self,edit):
		if edit.echoMode() == QtWidgets.QLineEdit.Password:
			edit.setEchoMode(QtWidgets.QLineEdit.Normal)
		elif edit.echoMode() == QtWidgets.QLineEdit.Normal and edit.objectName() == "pwd":
			edit.setEchoMode(QtWidgets.QLineEdit.Password)
#signin button clicked
	def signin_clicked(self):
		self.signw = SigninWindow(self)
		self.signw.main()
#loggin windowd main method
	def main(self):
		neoworker = Neo4jWorker()
		neoworker.signals.neostarted.connect(lambda: self.setEnabled(False))
		neoworker.signals.neofinished.connect(lambda:self.setEnabled(True))
		#catch neo 
		neoworker.signals.neo4jconnected.connect(self.catchneo)
		self.threadpool.start(neoworker)
		self.show()
#the signing window section
class SigninWindow(QDialog,SignWindow):
# the signin window init 
	def __init__(self,parent=None):
		super(SigninWindow,self).__init__(parent)
		self.setupUi(self)
		self.signals = WrokerSignals()
		self.cancel.clicked.connect(lambda:self.close())
		self.submit.clicked.connect(self.submit_onclick)
		self.switch.clicked.connect(lambda:self.switch_onclick(self.pwd,self.pwdconfirm))
		self.username.clicked.connect(lambda:self.resetEdit(self.username))
		self.pwd.clicked.connect(lambda:self.resetEdit(self.pwd))
		self.pwdconfirm.clicked.connect(lambda:self.resetEdit(self.pwdconfirm))
		self.ckey.clicked.connect(lambda:self.resetEdit(self.ckey))
		self.csecret.clicked.connect(lambda:self.resetEdit(self.csecret))
		self.acctoken.clicked.connect(lambda:self.resetEdit(self.acctoken))
		self.accsecret.clicked.connect(lambda:self.resetEdit(self.accsecret))
		self.threadpool = QThreadPool()
#setting the lineEdits in case of error
	def setError(self,edit,string):
		edit.setText("")
		edit.setPlaceholderText(string)
		edit.setStyleSheet(ERROREDIT)
# reseting the lineEdits in case of Edit	
	def resetEdit(self,edit):
		edit.setStyleSheet(LEDIT)
#the singing window neo4j Catcher
	def catchneo(self,neo4j):
		self.neo4j = neo4j
# the switch button method show /hide password this one have to edits
	def switch_onclick(self,edit,edit2=None):
		if edit.echoMode() == QtWidgets.QLineEdit.Password:
			edit.setEchoMode(QtWidgets.QLineEdit.Normal)
		elif edit.echoMode() == QtWidgets.QLineEdit.Normal and(edit.objectName()=="pwd" or edit.objectName() == "pwdconfirm"):
			edit.setEchoMode(QtWidgets.QLineEdit.Password)
		if edit2 != None:	
			if edit2.echoMode() == QtWidgets.QLineEdit.Password:
				edit2.setEchoMode(QtWidgets.QLineEdit.Normal)
			elif edit2.echoMode() == QtWidgets.QLineEdit.Normal and(edit2.objectName()=="pwd" or edit2.objectName() == "pwdconfirm"):
				edit2.setEchoMode(QtWidgets.QLineEdit.Password)
#submit button method called when it' s clicked
	def submit_onclick(self):
	# colapse all these 
		users = self.neo4j.allSignedUsers()
		edits = list()
		edits= [(self.username,self.username.text()),
		(self.pwd,self.pwd.text()),(self.pwdconfirm,self.pwdconfirm.text()),(self.ckey,self.ckey.text()),
		(self.csecret,self.csecret.text()),(self.acctoken,self.acctoken.text()),(self.accsecret,self.accsecret.text())]
		user = dict()
		try:
			for obj,txt in edits:
				if txt =="":
					raise SigninError("BLANC AREA DENIED")
				else: 
					user[obj.objectName()] = txt
			if user != {}:	
				if re.search(r"^[a-zA-Z][a-zA-Z0-9]{4,32}$",user['username']) is None:
					self.setError(self.username,"please insert a valide username ")
				if user["username"] in users:
					self.setError(self.username,"user name exist already")
				if re.search(r"^[a-zA-Z][a-zA-Z0-9_]{5,32}",user['pwd']) is None:
					raise SigninError("wrong password format")

				elif user["pwd"] != user["pwdconfirm"]:
					raise SigninError("password don't match")
				# TEST THE Tokens
				try:
					test = TwitterAgent(user['ckey'],user['csecret'],user['acctoken'],user['accsecret']) 
					me = test.api.me()
					self.neo4j.createUser(user["username"],user["pwd"],user["ckey"],user["csecret"],user["acctoken"],user["accsecret"])			
					succs = QMessageBox.information(self,'Success','User have been Created Successfully',QMessageBox.Ok)
					self.close()
				except tweepy.TweepError as e:
					if str(e).find('Invalid or expired token.') !=-1: #if str(e) == "[{'code': 89, 'message': 'Invalid or expired token.'}]":
						error = QMessageBox.information(self,'Invalide Inpute','Invalide or expired Tokens',QMessageBox.Ok)	
						self.setError(self.ckey,"expired Token")
						self.setError(self.csecret,"expired Token")
						self.setError(self.acctoken,"expired Token")
						self.setError(self.accsecret,"expired Token")
					else:
						if not is_connected:
							error = QMessageBox.information(self,'HTTP Error',"please check your host and try again",QMessageBox.Ok)
		
		except SigninError as e :
			if str(e).find("BLANC AREA DENIED")!= -1:
				for obj,txt in edits:
					if txt =="":
						self.setError(obj,'blancs are not allowed')
			if str(e).find("password don't match") != -1 :
				self.setError(self.pwdconfirm,"passwords don't match each other")
			if str(e).find("wrong password format") != -1 :
				self.setError(self.pwd,"password is not alpha numric")
				self.setError(self.pwdconfirm,"password is not alpha numric")
				# the main method od the signing window
	def main(self):
		self.show()
		neoworker = Neo4jWorker()
		neoworker.signals.neostarted.connect(lambda:self.setEnabled(False))
		neoworker.signals.neofinished.connect(lambda:self.setEnabled(True))
		#catch neo 
		neoworker.signals.neo4jconnected.connect(self.catchneo)
		self.threadpool.start(neoworker)
# the matplotlib classes section 
# the canvas class used for dispaly the the figure 
class MplCanvas(Canvas):
	def __init__(self):
		self.fig = Figure()
		self.ax = self.fig.add_subplot(111)
		Canvas.__init__(self,self.fig)
		Canvas.setSizePolicy(self,QSizePolicy.Preferred,QSizePolicy.Preferred)
		Canvas.updateGeometry(self)
		#mplstyle.use(['dark_background', 'ggplot', 'fast'])
# the mpl widget class this is used for drawing 
class MplHist(QWidget):
	def __init__(self,parent=None):
		QWidget.__init__(self,parent)
		self.canvas = MplCanvas()
		#mplstyle.use([ 'ggplot', 'fast'])
		self.vbl = QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
class SigninError(Exception):
	def __init__(self,message):
		super(SigninError,self).__init__(message)
#############################################################################################################
class UpdateWin(QDialog,Ui_UpdateWindow):
	def __init__(self,parent=None):
		super(UpdateWin,self).__init__(parent)
		self.setupUi(self)
		self.threadpool = QThreadPool()
	def main(self,api,searcher,ontopath,since,until):
		self.show()
		extractor = MainExtractionWorker(api,searcher,ontopath,since,until,self.MainExtraLab)#,self.mainpbar)
		extractor.signals.extractionStart.connect(self.extraStart)
		extractor.signals.extractionNotif.connect(self.extraOntif)
		extractor.signals.extractionEnd.connect(lambda:self.close())
		extractor.signals.extraerror.connect(self.extraOnError)
		self.threadpool.start(extractor)
	def extraStart(self):
		self.MainExtraLab.setText("Update is runnig ...")
		
	def extraOntif(self,string):
		self.MainExtraLab.setText(string)
	def extraOnError(self,excp):
		mess = QMessageBox.information(self,"Extraction Error","An Error Occured from the server please try again later",QMessageBox.Ok)	
		self.close()
class MainExtractionWorker(QRunnable):
	def __init__(self,searcher,api,ontopath,since,until,lab):
		super(MainExtractionWorker,self).__init__()
		self.searcher = searcher
		self.api = api
		self.ontopath = ontopath
		self.since = since
		self.until = until 
		self.signals = WrokerSignals()
		self.lab = lab 
	@pyqtSlot()
	def run(self):
		self.signals.extractionStart.emit()
		try:
			self.signals.extractionNotif.emit("Running extraction")
			self.searcher.MainCorpExtraction(self.api,self.ontopath,self.since,self.until,self.lab)
		except Exception as e:
			exctype, value = sys.exc_info()[:2]
			self.signals.extraerror.emit((exctype,value,traceback.format_exc()))
#the main class here all become alive 
if __name__ == '__main__':
	app = QApplication(sys.argv)
	#window = MainWindow()
	logapp = logingWindow()
	user = {'name':"admin",
	 		'pwd': "admin",	
	 		'ck': "WouN94K3npYkZDHVpHGQDOwyl",
			'cs': "RQyYPzLRXOA5QMs5OnVP91wAYB4dSnTAd2X5dKXvIr4NKkWY3F",
			'act': "295286840-5yd7qcXg1WfZplnrb78UYE2CKY1N1MZlLZdsMSSZ",
			'acs': "E8QWRogAahyutRgdhsqcAdAhrHonzJtF8JLcPpBxylTu5"}
# Authentification grace à la fonction authentif
	logapp.main()
	#if logapp.exec_() == QtWidgets.QDialog.Accepted:
		#window.main()
	sys.exit(app.exec_())
