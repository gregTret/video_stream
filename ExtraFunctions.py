import subprocess

class ExtraFunctions:
    def __init__(self):
        pass

    # Constructing Object to pass to Main Page
    def getMostPopular(self,mostPopular):
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
    def loadIp(self):
        try:
            result = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE)
            value=str(result.stdout)
            value=(value.replace('b\'',''))
            return (value.split(' ')[1])
        except:
            return "Issue in IP Configuration please fix me"
