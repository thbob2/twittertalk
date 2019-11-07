#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle
from publications import *
from textblob import *
from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
from searcher import * 
from PyQt5.QtWidgets import QLabel
import datetime as dt 

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
#########################################################################################################################################################################################################

if __name__=="__main__":
    searcher = Searcher()
    analyser = Analyser()
    ontop = "file://C:/Users/bob/Documents/scarp/docs/smart.owl"
    
    file = searcher.fullExtraction('Galaxy J7','cache/file.json')
    ElaguedF = searcher.elaguerFichier(ontop,file)
    #Labeling each tweet based on the each feature contained in its text and save it in a file called 'etiquetted.json'
    print("Etiquetage ... of {}".format(ElaguedF))
    etiquettedFile=searcher.etiqueter(ElaguedF,ontop)
    
    #Clean tweets fro url's, hashtags and special caracteres in a file called 'cleanedTweets.json'
    #print("netoyage...of {}".format(etiquettedFile))
    cleanedFile=searcher.cleanTweets('cache/etiquetted.json')                     
    #searcher.afficherTweets("cache/cleanedTweets.json")
    # Labeling each tweet in file "cleanedTweets.json"   with 'pos' and 'neg' 
    start = dt.datetime.now()
    cleanedFile=analyser.analizeFile("cache/cleanedTweets.json")
    stop = dt.datetime.now()
    # Calculating positiviy and negativity's pourcentage  and saving the results in the two files "results" and "smar.json"    
    analyser.negativityAndPositivity("cache/cleanedTweets.json",ontop,searcher)
    
    #Influence the results calculated before depending on the sub classes of each classed of the ontology
    analyser.influenceResults("docs/smar.json")
    with open("docs/smar.json","r",encoding="utf-8") as r : 
        data = json.load(r)

    with open("docs/approcheLexical.json","w",encoding="utf-8") as w2: 
        s = json.dumps({"start": str(start),"stop":str(stop),"concepts":[o for o in data['concepts']]},indent=4)
        w2.write(s)
    
#######################
    print ("Elagage... of {}".format(file)) 
    ElaguedF = searcher.elaguerFichier(ontop,file)
    #Labeling each tweet based on the each feature contained in its text and save it in a file called 'etiquetted.json'
    print("Etiquetage ... of {}".format(ElaguedF))
    etiquettedFile=searcher.etiqueter(ElaguedF,ontop)
    
    #Clean tweets fro url's, hashtags and special caracteres in a file called 'cleanedTweets.json'
    print("netoyage...of {}".format(etiquettedFile))
    cleanedFile=searcher.cleanTweets('cache/etiquetted.json')                     
    #searcher.afficherTweets("cache/cleanedTweets.json")
    # Labeling each tweet in file "cleanedTweets.json"   with 'pos' and 'neg' 
    start = dt.datetime.now()
    cleanedFile=analyser.analizeFileBayes("cache/cleanedTweets.json")
    stop = dt.datetime.now()
    # Calculating positiviy and negativity's pourcentage  and saving the results in the two files "results" and "smar.json"    
    analyser.negativityAndPositivity("cache/cleanedTweets.json",ontop,searcher)
    
    #Influence the results calculated before depending on the sub classes of each classed of the ontology
    analyser.influenceResults("docs/smar.json")
    with open("docs/smar.json","r",encoding="utf-8") as r : 
        data = json.load(r)

    with open("docs/approcheNVB.json","w",encoding="utf-8") as w1: 
        s = json.dumps({"start": str(start),"stop":str(stop),"concepts":[o for o in data['concepts']]},indent=4)
        w1.write(s)
###################


     
   