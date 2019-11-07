from neo4j.v1 import *
import os 
import signal
import subprocess
import time
import sys
from publications import *
import json
#decorateur de la class sigleton 
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
			self.server = subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
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
#************************************************************************#,
if __name__ == '__main__':
	uri = "bolt://127.0.0.1:7687"
	user = "thbob"
	password = "2305"
	path_t = """file:D:/corp/CorpusPrincipal_2018-03-10.json"""
	file = """file:C:/Users/bob/Documents/scarp/docs/smar.json"""
	client = Neo4j(uri,user,password) 

	#client.import_onto("file:/D:/scarp/docs/smart_phone.json")
	#now = time.localtime()
	#date = "{}-{}-{}".format(now.tm_year,now.tm_mon,now.tm_mday)
	#time = "{}:{}:{}".format(now.tm_hour,now.tm_min,now.tm_sec)

	client.createUser(user["name"],user["pwd"],user["ck"],user["cs"],user["act"],user["acs"])
	print(client.load_user_mod("admin"))

	 
	 #client.importresult(user["name"],file,date,time,'Galaxy S8')
	 #d = "2018-5-2"
	 #t="10:19:30"
	 #con= client.load_user_mod(user['name'])
	 #print(con)
	 #m = "Galaxy S8"
	 #tel,concespts = client.loadresult('bob',d,t,m)
	 

	 #bob = client.allSignedUsers()
	 #print(bob)
	 #if bob["pwd"] == "2305":
	 #	print("you re the boss bro ")
	 #date = "2018-04-11"
	 #client.import_result(path_s,"2018-4-11","Galaxy")	 
	 #s= client.loadSmar("2018-4-11","Galaxy")
	 #print(s)
	 #client.import_tweets(file=path_t)	 
	 #mydic = client.alltweet_list()
	 #s = json.dumps({'tweets':[o.dump() for o in mydic]},indent=4)
	 #print(s)