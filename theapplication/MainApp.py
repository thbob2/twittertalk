#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import json
import pickle
import regex as re 
from os import listdir
from os.path import isfile, join
import os 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import matplotlib.style as mplstyle
from publications import *
from textblob import *
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier
from neotweet import * 
from searcher import * 
from analyser import * 
from twitter_client import *
import tweepy
from owlready2 import * 
import traceback, sys
from samples import *
import pandas as pd 
import numpy as np
import datetime as dt 
import socket

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
			ck': "WouN94K3npYkZDHVpHGQDOwyl",
			'cs': "RQyYPzLRXOA5QMs5OnVP91wAYB4dSnTAd2X5dKXvIr4NKkWY3F",
			'act': "295286840-5yd7qcXg1WfZplnrb78UYE2CKY1N1MZlLZdsMSSZ",
			'acs': "E8QWRogAahyutRgdhsqcAdAhrHonzJtF8JLcPpBxylTu5"}
# Authentification grace à la fonction authentif
	logapp.main()
	#if logapp.exec_() == QtWidgets.QDialog.Accepted:
		#window.main()
	sys.exit(app.exec_())
	