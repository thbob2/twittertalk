this is my licens project made in the year 2018 
it's a desktop app coded in python 
the packages mainly used in other the create it are:
	-neo4j-driver the python driver for neo4j database
	-tweepy  it's the twitter api package for python 
	-PyQt  for the UI and the UX 
	-textblob  for the lexical analyses
	-matplotlib for the graphe making

the project is divided into folders:

the cache folder contain the cache of the app 
--WARNING-- do not delete any of the files or it won't work
docs contains the files needed in orther to calculate the scores
corp: is the folder containing the data set we collected from twitter over 5 months  of work
neo4j-community-3.3.2 is the database folder the community version of neo4j is lightweighted



/////////////////////////////////
analyser.py is the module of the semantic and lexical analyser
searcher.py is the module used for data extraction
gui.py and samples.py are the ui designed by pyqt

neotweet.py is the module of the database controler import export

twitter_client.py is for the api configuration

MainApp.py is the main application module