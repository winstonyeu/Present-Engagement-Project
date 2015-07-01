import hashlib, requests, json
import urllib.parse
import re, os.path
import base64

class PresentAPI:
    #url = 'http://jr2.presentapp.co:8000'
    url = 'https://private-api.presentapp.co'
    
    def __init__(self):
        self.accesstoken = ""
    
    def loginUser(self, email, password):
        accesstokenurl = self.url + "/accesstoken"
        hashpswd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        payload = {
                    'email': email,
                    'password': hashpswd,
                    'client': {
                        'id': '1',
                        'type': 'automationscripts',
                        'version': '1.0',
                        'os': 'automationscripts'
                    }
                  }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(accesstokenurl, data=json.dumps(payload), headers=headers)
        r = r.json()
        self.accesstoken = r['accesstoken']
        return r['accesstoken']
    
    def logoutUser(self):
        accesstokenurl = self.url + "/accesstoken/" + self.me()['_id']
        r = requests.delete(accesstokenurl)
        
    def registerUser(self, name, email, password):
        registerurl = self.url + "/users"
        hashpswd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        payload = {
                    'name': name,
                    'email': email,
                    'password': hashpswd
                  }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(registerurl, data=json.dumps(payload), headers=headers)
        if r.status_code == 422:
            return False
        return True
    
    def me(self):
        userurl = self.url + "/users/me"
        headers = {'X-Accesstoken': self.accesstoken}
        r = requests.get(userurl, headers=headers)
        r = r.json()
        return r
        
    def getUser(self, email):
        userurl = self.url + "/users/_search?q=%s" % email
        headers = {'X-Accesstoken': self.accesstoken}
        r = requests.get(userurl, headers=headers)
        r = r.json()
        return r[0]
    
    def getfollower(self):
        userurl = self.url + "/users/me/followers?page=1"
        headers = {'content-type': 'application/json', 'X-Accesstoken': self.accesstoken}
        r = requests.get(userurl, headers=headers)
        print(r.text)
        r = r.json()
        #return r
    
    def getfollowing(self):
        userurl = self.url + "/users/me/following"
        headers = {'content-type': 'application/json', 'X-Accesstoken': self.accesstoken}
        r = requests.get(userurl, headers=headers)
        r = r.json()
        return r
    
    def checkFollowingStatus(self, userid):
        following = self.getfollowing()
        for user in following:
            if userid == user['_id']:
                return True
        return False
    
    def followUser(self, userid):
        followurl = self.url + "/users/me/follow/%s" % userid
        headers = {'X-Accesstoken': self.accesstoken}
        r = requests.put(followurl, headers=headers)
        #print(r.text)
        
    def unfollowUser(self, userid):
        followurl = self.url + "/users/me/follow/%s" % userid
        headers = {'X-Accesstoken': self.accesstoken}
        requests.delete(followurl, headers=headers)
    
    def updateName(self, name):
        upurl = self.url + "/users/me"
        payload = {
                    'name' : name
                  }
        headers = {'X-Accesstoken': self.accesstoken}

        requests.put(upurl, data=payload, headers=headers)
        
    def updateAbout(self, about):
        upurl = self.url + "/users/me"
        payload = {
                    'about' : about
                  }
        headers = {'X-Accesstoken': self.accesstoken}

        requests.put(upurl, data=payload, headers=headers)
        
    def changeDisplayPicture(self, dp):
        dpurl = self.url + "/users/me/dp"       
        file = open(dp+".jpg", 'rb')
        files = {'dp': file}

        headers = {'X-Accesstoken': self.accesstoken}
        requests.put(dpurl, files = files, headers=headers)
        
    def likePresent(self, presentid):
        lpurl = self.url + "presents/%s/like" + presentid
        
        headers = {'X-Accesstoken': self.accesstoken}
        
        requests.post(lpurl, headers=headers)
        
    def unlikePresent(self, presentid):
        lpurl = self.url + "presents/%s/like" + presentid
        
        headers = {'X-Accesstoken': self.accesstoken}
        
        requests.delete(lpurl, headers=headers)

class PresentAPIError(Exception):
    def __init__(self, status_code, error_type, error_message, *args, **kwargs):
        self.status_code = status_code
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        return "(%s) %s-%s" % (self.status_code, self.error_type, self.error_message)
    
        
        
        
        