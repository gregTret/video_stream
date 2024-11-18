import subprocess
from flask import Flask, render_template, send_from_directory,request,redirect
import os
import logging
from pymongo import MongoClient
import json
from bson import json_util

# Configuring Logging File
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="./logs/log", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")

# Server Setup + Connecting to MongoDB
app = Flask(__name__,static_url_path='')
client = MongoClient('localhost', 27017)
db = client["host"]
collection = db["movies"]

# Constructing Object to pass to Main Page
def getMostPopular(mostPopular):
    current=0
    movieInfo={}
    for movie in mostPopular:
        current+=1
        movieId='movie'+str(current)+'id'
        movieName='movie'+str(current)+'name'
        movieSrc='movie'+str(current)+'src'
        movieVideo='movie'+str(current)+'video'
        movieInfo[movieId]=movie['id']
        movieInfo[movieName]=movie["original_title"],
        movieInfo[movieSrc]=movie["poster_path"]
        movieInfo[movieVideo]=movie["video"]
    return movieInfo

# Server Specific, retrieval of current external IP address for population
def loadIp():
    try:
        result = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE)
        value=str(result.stdout)
        value=(value.replace('b\'',''))
        return (value.split(' ')[1])
    except:
        return "Issue in IP Configuration please fix me"

# Get and Store Current IP
currentIp=loadIp()

# Get movie Details by ID
@app.route('/getMovieById', methods=['GET'])
def movie_details():
    try:
        id=request.args['id']
        result=collection.find_one({"id":int(id)})
        if (result!=None):
            return json.loads(json_util.dumps(result))
        else:
            raise TypeError("Invalid Query")
    except:
        return "Are you messing about with my server?"

# Go to NGINX server stream for the selected video
@app.route('/movie', methods=['GET'])
def playMovie():
    try:
        url=request.args['url']
        return redirect("http://"+currentIp+':5001/'+url)
    except:
        return "Error Loading Resource"

# Go to NGINX server stream for the selected video
@app.route('/results', methods=['GET'])
def searchResults():
    try:
        query=request.args['q']
        findQuery={"title":{"$regex" : query,"$options": 'i'}}
        result=(collection.find(findQuery).sort({"release_date":1}).limit(20))
        if (result!=None):
            vars=getMostPopular(result)
            return render_template('movies.html',**vars)
        else:
            raise TypeError("Invalid Query")
    except:
        return "404"

# Default Route Redirect
@app.route('/')
def hello():
    return redirect("/movies")

# Main Landing Page population 
@app.route('/movies')
def movies():
    # getting Most Popular Films
    mostPopular=collection.find().sort({"popularity":-1}).limit(20)
    # Getting Highest Rated Movies
    highestRated=collection.find().sort({"vote_average":-1}).limit(50)
    jsonMerged=[]
    for i in mostPopular:
        if (len(jsonMerged)<6):
            jsonMerged.append(i)

    for i in highestRated:
        if (len(jsonMerged)<24 and i not in jsonMerged):
            jsonMerged.append(i)

    vars=getMostPopular(jsonMerged)
    return render_template('movies.html',**vars)

@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

app.run(host='0.0.0.0',debug=True,port=5000)

