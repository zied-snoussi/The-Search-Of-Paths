from flask import Flask, request
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from collections import Counter
import numpy as np
import os

app = Flask(__name__)
#nltk.download('punkt')
#nltk.download('stopwords')
stemmer = FrenchStemmer()
######################Ouverture de documents######################
dataset = np.zeros((6,3), dtype=object)
economies=os.listdir("./data/economie")
association=os.listdir("./data/association")

######################Les fonctions######################
def getWord(data):
  return word_tokenize(data)

def deleteStopWord(data):
   return [i for i in data if not i.lower() in stopwords.words()]

def normalisation(data):
   li = []
   for word in data:
     li.append(stemmer.stem(word))
   return li

def CalcPoids(data):
  list_freq = []
  for i in data:
    word = i
    counter = Counter(data)
    list_freq.append((counter[word]))
  return list_freq

def rech(word,data):
    word=getWord(word)
    token = deleteStopWord(word)
    mots_cles = normalisation(token)
    listdoc=[]
    for i in range(0,data.shape[0]):
        k=0
        for j in mots_cles:
            if j in data[i,0]:
                k+=1
        if k == len(mots_cles):
            listdoc.append(data[i,2])
    return listdoc
##################Appels des fonctions##########################
i=-1
for nom_file in economies:
    File=open("./data/economie/"+nom_file,"r",encoding="utf-8")
    data = File.read()
    word = getWord(data)
    token = deleteStopWord(word)
    mots_cles = normalisation(token)
    nb_occ = CalcPoids(mots_cles)
    i+=1
    dataset[i,0]=mots_cles
    dataset[i,1]=nb_occ
    dataset[i,2]="./data/economie/"+nom_file
    File.close()


for nom_file in association:
    File=open("./data/association/"+nom_file,"r",encoding="utf-8")
    data = File.read()
    word = getWord(data)
    token = deleteStopWord(word)
    mots_cles = normalisation(token)
    nb_occ = CalcPoids(mots_cles)
    i+=1
    dataset[i, 0]=mots_cles
    dataset[i, 1]=nb_occ
    dataset[i, 2]="./data/association/"+nom_file
    File.close()

req = ""
@app.route('/postPaths' ,methods=['POST'])
def postPaths():
    #req= "tunisie"
    #if request.method == "POST":
    global req
    req = request.json["inputText"]
    return req
@app.route('/paths' ,methods=['GET'])
def paths():
    res = []
    global req
    for j in rech(req, dataset):
        res.append(j)
    return {"paths": res}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
