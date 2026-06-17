import urllib2
import json

userAgent = "TigerJython"

def setUserAgent(name):
    global userAgent
    userAgent = nam
    
def getUserAgent():
    return userAgent
    
class Patch(urllib2.Request):
    def get_method(self):
        return "PATCH"

class Put(urllib2.Request):
    def get_method(self):
        return "PUT"
    
class Get(urllib2.Request):
    def get_method(self):
        return "GET"
    
class Head(urllib2.Request):
    def get_method(self):
        return "HEAD"
    
class Options(urllib2.Request):
    def get_method(self):
        return "OPTIONS"
    
class Post(urllib2.Request):
    def get_method(self):
        return "POST"

def sendRequest(mode, url, data = None, headers = None, prefferedMode = None):
    global userAgent
    if mode == "GET":
        request = Get(url)
    elif mode == "PATCH":
        request = Patch(url, data)
    elif mode == "PUT":
        request = Put(url, data)
    elif mode == "POST":
        request = Post(url, data)
    elif mode == "HEAD":
        request = Head(url)
    elif mode == "OPTIONS":
        request = Options(url)
    if data != None:
        request.add_data(data)
    if headers != None:
        for i in headers:
            request.add_header(i, headers[i])
    request.add_header("User-Agent", userAgent)
    f = urllib2.urlopen(request)
    if prefferedMode == None:
        return f
    elif prefferedMode == "read":
        return f.read()
    elif prefferedMode == "info":
        return f.info()
        
class Database(): #use a database with the free website JSONHosting (max 1 MB)
    allowModifikationNonexistantData = True
    @staticmethod
    def getData(url):
        f = urllib2.Request(url, None)
        f.add_header("User-Agent", "AndromedaOS")
        l = urllib2.urlopen(f)
        return l
    @staticmethod
    def getOptions(url): #equivalent to HTTP OPTIONS
        f = Options(url, None, {"User-Agent": "AndromedaOS"})
        l = urllib2.urlopen(f)
        return l
    @staticmethod
    def setData(url, data, key): #equivalent to HTTP POST
        data = json.dumps(data)
        f = Patch(url, data, {"User-Agent": "AndromedaOS", "X-Edit-Key": key, "Content-Type": "application/json"})
        l = urllib2.urlopen(f)
        return l
    @staticmethod
    def setSpecificData(url, data, key): #equivalent to HTTP PATCH
        data = json.dumps(data)
        oldData = json.loads(Database.getData(url))
        for i in data:
            if i in oldData.keys():
                oldData[i] = data[i]
            else:
                print "Warning in Database.setSpecificData: key \"{}\" doesn't exist"
                if allowModifikationNonexistantData:
                    oldData[i] = data[i]
    @staticmethod
    def createDatabase(data = {}):
        data = json.dumps(data)
        f = urllib2.Request("https://jsonhosting.com/api/json/save", data, {"User-Agent": "AndromedaOS", "Content-Type": "application/json"})
        l = urllib2.urlopen(f)
        return l