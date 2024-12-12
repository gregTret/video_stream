from flask import Flask, render_template, send_from_directory, url_for ,request, send_file,jsonify,redirect
import os
import logging
import json
from bson import json_util
from MongoDB import MongoDB
from ExtraFunctions import ExtraFunctions

# Configuring Logging File

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="./logs/log", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")


# Server Setup + Connecting to MongoDB
app = Flask(__name__,static_url_path='')
db=MongoDB()
helper=ExtraFunctions()

# Go to NGINX server stream for the selected video
@app.route('/movie', methods=['GET'])
def playMovie():
    try:
        currentIp=helper.loadIp()
        url=request.args['url']
        return redirect("http://"+currentIp+':5001/'+url)
    except:
        return "Error Loading Resource"

# Default Route Redirect
@app.route('/')
def hello():
    try:
        return redirect("/movies")
    except:
        return {"status":500,"message":"Internal Server Error - Failed to redirect"}

# Main Landing Page population 
@app.route('/movies')
def movies():
    try:
        jsonMerged=db.construct_main_page()
        vars=helper.getMostPopular(jsonMerged)
        return render_template('movies.html',**vars)
    except:
        return {"status":500,"message":"Internal Server Error - DB Down"}

@app.route('/favicon.ico')
def fav():
    try:
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')
    except:
        return {"status":500,"message":"Internal Server Error - Failed to load favicon"}
    
@app.route('/requestFilm')
def requestLoadPage():
    try:
        return render_template('request.html')
    except:
        return {"status":500,"message":"Internal Server Error - Failed to render template request.html"}

@app.route('/requestForm',methods=['POST'])
def saveUserQuery():
    try:
        content = request.get_json(silent=True)
        db.handle_movie_requests(content)
        return {}
    except:
        return {"status":500,"message":"Internal Server Error - Failed to save request"}

@app.route('/searchGeneric',methods=['GET'])
def searchGeneric():
    try:
        query=request.args['q']
        result=db.movie_search_bar(query)
        if (result!=None):
            return json.loads(json_util.dumps(result))
        else:
            raise TypeError("Invalid Query")
    except:
        return {}

@app.route('/searchResults',methods=['GET'])
def forceMainPage():
    try:
        query=request.args['q']
        if (query==""):
            raise Exception("Empty search going back to movies")
        result=db.movie_search_screen(query)
        vars=helper.getMostPopular(result)
        return render_template('movies.html',**vars)
    except:
        return redirect("/movies")
    
@app.route('/dashboardPage')
def loadDashboard():
    try:
        return render_template('dashboard.html')
    except:
        return {"status":500,"message":"Internal Server Error - DB Down"}

@app.route('/dashboard')
def getDashboard():
    try:
        docs=db.getRequests()
        return json.loads(json_util.dumps(docs))
    except:
        return {"status":500,"message":"Internal Server Error - DB Down"}

@app.route('/updateRequest',methods=['POST'])
def updateRequest():
    try:
        content = request.get_json(silent=True)
        response=db.updateRequestStatus(content)
        return response
    except:
        return {"status":500,"message":"Internal Server Error - DB Down"}

app.run(host='0.0.0.0',debug=True,port=5000)

