#!/usr/bin/env python
# -*- coding: utf-8 -*-
import regex as re
import pickle
import tweepy
import json
import pandas as pd
import ast
from IPython.display import display
from textblob import TextBlob
from owlready2 import  *
from twitter_client import *
from publications import *
from analyser import * 
from PyQt5.QtWidgets import QLabel,QProgressBar
from os import listdir
from os.path import isfile, join
import os 
import datetime as dt
class Searcher(object):    
#########################################################################################################################################################################################################
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
#########################################################################################################################################################################################################
    
if __name__=="__main__":
    
    #Authentification en utilisant les clés fournies par TWITTER
    #api = get_twitter_client()
    #Collecte des Twitter en se basant sur les mots clé introduits
    #Tweets = searchCle(mot_cle="galaxy s8",api=api)
    
    #Keeping and saving only tweets that is mentionned in their texts at least a class of the ontology,  the file is called 'file.json'
    #elagedFile = elaguerCursor("file://C:/Users/bob/Documents/scarp/smart.owl",Tweets) 
    ontop = "file://"+os.getcwd()+"/scarp/docs/smart.owl"
    #file = "what i dont need in the pfe/shit/Galaxy S8.json"
    path = "cache/file.json"
    searcher = Searcher()    
    analyser = Analyser()
    user = {'name':"Boubekeur",
            'pwd': "2305",  
            'ck': "WouN94K3npYkZDHVpHGQDOwyl",
            'cs': "RQyYPzLRXOA5QMs5OnVP91wAYB4dSnTAd2X5dKXvIr4NKkWY3F",
            'act': "295286840-5yd7qcXg1WfZplnrb78UYE2CKY1N1MZlLZdsMSSZ",
            'acs': "E8QWRogAahyutRgdhsqcAdAhrHonzJtF8JLcPpBxylTu5"}
# Authentification grace à la fonction authentif
    agent = TwitterAgent(user["ck"],user['cs'],user["act"],user["acs"])
    api = agent.get_twitter_client()
    until = dt.datetime.today()
    since = until - dt.timedelta(days=5)

    #path = searcher.fullExtraction('Galaxy S8+',path)
    #path = searcher.elaguerFichier(ontop,path)
    #with open("docs/samsung_smartphones.txt","r",encoding="utf-8") as file1:
        #for line in file1:
        #    phoneNames.append(line.strip())
    #for name in phoneNames:
        #p = "what i dont need in the pfe/shit/"+name+".json"
        #p = searcher.fullExtraction(name,p)
    #file = searcher.fullExtraction("Galaxy S9",'cache/file.json')
    #print ("Elagage... of {}".format(file)) 
    #ElaguedF = searcher.elaguerFichier(ontop,file)
    #Labeling each tweet based on the each feature contained in its text and save it in a file called 'etiquetted.json'
    #print("Etiquetage ... of {}".format(ElaguedF))
    #etiquettedFile=searcher.etiqueter(ElaguedF,ontop)
    
    #Clean tweets fro url's, hashtags and special caracteres in a file called 'cleanedTweets.json'
    #print("netoyage...of {}".format(etiquettedFile))
    #cleanedFile=searcher.cleanTweets('cache/etiquetted.json')                     
    #searcher.afficherTweets("cache/cleanedTweets.json")
    # Labeling each tweet in file "cleanedTweets.json"   with 'pos' and 'neg' 
    #cleanedFile=analyser.analizeFile("cache/cleanedTweets.json")
    
    # Calculating positiviy and negativity's pourcentage  and saving the results in the two files "results" and "smar.json"    
    #analyser.negativityAndPositivity("cache/cleanedTweets.json",ontop,searcher)
    
    #Influence the results calculated before depending on the sub classes of each classed of the ontology
    #analyser.influenceResults("docs/smar.json")
    
