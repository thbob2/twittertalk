import time
import matplotlib.pyplot as plt
import json
import datetime as dt
import math 
import numpy as np 
if __name__ == '__main__':
	
	axx = [0,1]
	ay = [15,22805]
	plt.bar(1,15,width=0.5,color='g')
	plt.bar(2,22805,width=0.5,color = 'r')
	plt.xlabel("Méthode d'analyse")
	plt.ylabel("Durrée d'execution (s)")
	plt.title(" Graphe de comparaison des deux methodes d'analyse sur un Corpus de taill d'un 1Mo ")
	plt.xticks([1,2],["Analyseur lexical","Analyseur Naïve Bayesien"])
	#
	#plt.legend()
	plt.show()