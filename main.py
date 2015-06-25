import requests, csv, os.path
import Configuration, PresentAPI
from collections import OrderedDict
from random import randint
import time, string, threading

class RetrieveUser:
    def __init__(self):
        self.filename = 'users.csv'
        self.userList = []
        self.initialize()
    
    def initialize(self):
        if self.userCount() == 0:
            fieldnames = ['firstname', 'lastname', 'id', 'email', 'password', 'picture']
            csvwriter = csv.DictWriter(open(self.filename,'a'), delimiter=',', fieldnames=fieldnames, lineterminator="\n")
            csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
        self.storeUserInfo()
            
    def writeToFile(self, data):
        fieldnames = ['firstname', 'lastname', 'id', 'email', 'password', 'picture']
        csvwriter = csv.DictWriter(open(self.filename,'a'), delimiter=',', fieldnames=fieldnames, lineterminator="\n")
        csvwriter.writerow(data)
        print("Done writing")
    
    def userCount(self):
        if os.path.isfile(self.filename) == False:
            open(self.filename, 'a').close()
            return 0
        
        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            num_lines = sum(1 for row in csvreader)
            csvfile.close()
            return num_lines
    
    def retrieveUsers(self, count, apikey):
        r = requests.get('http://api.randomuser.me/?results=%s&key=%s' % (count, apikey))
        r = r.json()
        return r['results']
    
    def saveUserInfo(self, userlist):
        data = {}
        for user in userlist:
            user = user['user']
            data['firstname'] = user['name']['first']
            data['lastname']  = user['name']['last']
            data['email']     = user['email']
            data['password']  = user['password']
            data['picture']   = user['picture']['large']
            self.writeToFile(data)
    
    def storeUserInfo(self):
        fieldnames = {k:v for v,k in enumerate(['firstname', 'lastname', 'id', 'email', 'password', 'picture'])}
        file = csv.DictReader(open(self.filename, 'r'), delimiter=',')
        for row in file:
            self.userList.append(OrderedDict(sorted(row.items(), key=lambda i:fieldnames.get(i[0]))))
    
    def resetUserList(self):
        fieldnames = {k:v for v,k in enumerate(['firstname', 'lastname', 'id', 'email', 'password', 'picture'])}
        file = csv.DictReader(open(self.filename, 'r'), delimiter=',')
        del self.userList[:]
        for row in file:
            self.userList.append(OrderedDict(sorted(row.items(), key=lambda i:fieldnames.get(i[0]))))
            
    def writeUserID(self, username, userid):
        once = False
        csvfile = open(self.filename, "a+", newline='')
        csvfile.seek(0, 0)
        reader = csv.reader(csvfile)
        writer = csv.writer(csvfile)
        for row in reader:
            if once == False:
                open(self.filename, 'w').close()
                once = True
            if username == row[0]:
                row[2] = userid
            writer.writerow(row)
        csvfile.close()
                    
    def retrieveAll(self):
        return self.userList
        
    def retrieveIndividual(self, index):
        return self.userList[index-1]
    
    def removeIndividual(self, user):
        self.userList.remove(user)
        
    def removeIndividualByName(self, name):
        for user in self.userList:
            if name == user['firstname']:
                self.userList.remove(user)
                return 1
        print("User not found or already removed")
        
api = PresentAPI.PresentAPI()
config = Configuration.Configuration('config.ini')
apikey = config.dictionary['apikey']

class Timer(threading.Thread):
    def __init__(self):
        super(Timer, self).__init__()
        self.elapsed = 0
        self.tempelapsed = 0
        self.timing = []
        self.previousTime = 0
        self.stop = False
        self.remainingTime = 0
        self.timingSize= 0
 
    def setTiming(self, timing):
        self.timing = list(timing)
        self.timingSize = len(self.timing)
    
    def resetTiming(self):
        self.tempelapsed = 0
        
    def indicator(self):  
        if len(self.timing[0]) != 0:
            if self.tempelapsed == self.timing[0][0]:
                self.timing[0].remove(self.tempelapsed)
                return True
        else:
            self.timing.remove(self.timing[0])
        
        if self.timingSize != len(self.timing):
            self.timingSize = len(self.timing)
            try:
                remainingTime = (self.timing[0][0] - (self.timing[0][0] - self.tempelapsed)) - self.tempelapsed
            except IndexError:
                remainingTime = 23 * 60 * 60
            if remainingTime > 0:
                print("\nWaiting remaining", remainingTime, "seconds")
                time.sleep(remainingTime+1)
            self.previousTime = 0

    
        return False
    
    def run(self):
        while self.stop == False:
            time.sleep(1)
            self.elapsed += 1
            self.tempelapsed += 1
            print("Elapsed:", self.elapsed, "Temp Elapsed:", self.tempelapsed)
        return
    
class PresentFollows(threading.Thread):
    def __init__(self):
        super(PresentFollows, self).__init__()
        
        self.Login = RetrieveUser()
        self.alluser = self.Login.retrieveAll()
        
        self.timer = Timer()
        self.timer.start()
         
        self.timings = []
        self.timings.append([10, 40])                             # 1st
        self.timings.append([75, 90, 105, 120])                   # 2nd
        self.timings.append([130, 140, 150, 160, 170, 180])       # 3rd
        self.timings.append([450, 720])                           # 12th
        self.timings.append([900, 1080, 1260, 1440])              # 24th
        self.timings.append([1560, 1680, 1800, 1920, 2040, 2160]) # 36th
        self.timings.append([2520, 2880])                         # 48th
        self.timings.append([3060, 3260, 3420, 3600])             # 60th
        self.timer.setTiming(self.timings)
        
        self.maxtime = []
        self.maxtime.append(3600)
        self.maxtime.append(12 * 60 * 60)
        self.maxtimeindex = 0
         
        self.numoffollower = 0
        self.lengthOfFollower = 0
        
    def run(self):
        print("Start")
     
        # First hour
        while True:
#             if len(self.alluser) == 0:
#                 print("All user followed")
#                 break    
            
            if self.timer.tempelapsed >= self.maxtime[self.maxtimeindex]:          
                del self.timings[:]
                
                if self.maxtimeindex == 0:    
                    self.timings.append([7200, 10800, 14400, 18000, 21600, 
                                        25200, 28800, 32400, 36000, 39600, 43200])
                    self.timer.setTiming(self.timings)
                    self.maxtimeindex += 1
                    print("First hour done")
                elif self.maxtimeindex == 1:
                    self.timer.tempelapsed = 0
                    randomfollowersnum = randint(5, 10)
                     
                    timing = []
                    dividedtime = int(self.maxtime[self.maxtimeindex] / randomfollowersnum)
                    for time in range(randomfollowersnum):
                        timing.append(dividedtime)
                     
                    self.timings.append(timing) 
                    self.timer.setTiming(self.timings)
 
            result = self.timer.indicator()
            
            if result:
                # Get rand user and login
                randindex = randint(1, len(self.alluser))
                randloginuser = self.Login.retrieveIndividual(randindex)
                #Login.removeIndividual(randloginuser)
                #api.loginUser(randloginuser['email'], randloginuser['password'])
                      
                # Follow user
                print(randloginuser['firstname'] + " followed random user")
                self.numoffollower+=1
                print("Followers:", self.numoffollower)
                #api.followUser("123")
                #api.logoutUser()

            if len(self.timer.timing[0]) != 0:
                self.timer.previousTime = self.timer.tempelapsed
                if self.lengthOfFollower != len(self.timer.timing[0]):
                    self.lengthOfFollower = len(self.timer.timing[0])
                    print("\nWaiting",  self.timer.timing[0][0] - self.timer.previousTime, "seconds until", self.timer.timing[0][0], "seconds")
            
        self.timer.stop = True

class PresentLikes(threading.Thread):
    def __init__(self):
        super(PresentLikes, self).__init__()
         
        self.Login = RetrieveUser()
        self.alluser = self.Login.retrieveAll()
         
        self.timer = Timer()
        self.timer.start()
          
        self.timings = []
        self.timings.append([60])
        self.timings.append([90, 120])
        self.timings.append([140, 160, 180])
        self.timings.append([240])
        self.timings.append([360, 480])
        self.timings.append([1200, 1800, 2400, 3000, 3600])
        self.timer.setTiming(self.timings)
        
        self.maxtime = []
        self.maxtime.append(3600)
        self.maxtime.append(24 * 60 * 60)
        self.maxtimeindex = 0
         
        self.numofliker = 0
        self.lengthOfLiker = 0
    
    def run(self):
        print("Start")
             
        # First hour
        while True:
            if self.timer.tempelapsed >= self.maxtime[self.maxtimeindex]:          
                del self.timings[:]
                
                if self.maxtimeindex == 1:   
                    self.timer.tempelapsed = 0 
                    self.timings.append([600])
                    self.timings.append([750, 900])
                    self.timings.append([1200])
                    self.timings.append([1350, 1500])
                    self.timings.append([2100])
                    self.timings.append([2400, 2700])
                    self.timings.append([3600])
                    self.timer.setTiming(self.timings)
                    self.maxtimeindex = 0
                
                self.maxtimeindex = 1
 
            result = self.timer.indicator()
            
            if result:
                # Get rand user and login
                randindex = randint(1, len(self.alluser))
                randloginuser = self.Login.retrieveIndividual(randindex)
                #Login.removeIndividual(randloginuser)
                #api.loginUser(randloginuser['email'], randloginuser['password'])
                      
                # Like user
                print(randloginuser['firstname'] + " liked random user")
                self.numofliker+=1
                print("Likers:", self.numofliker)
                #api.likerPresent("123")
                #api.logoutUser()

            if len(self.timer.timing[0]) != 0:
                if self.lengthOfLiker != len(self.timer.timing[0]):
                    self.lengthOfLiker = len(self.timer.timing[0])
                    print("\nWaiting",  self.timer.timing[0][0] - self.timer.elapsed, "seconds until", self.timer.timing[0][0], "seconds")
            elif len(self.timer.timing[0]) == 0:
                self.lengthOfLiker = 0
                            
        self.timer.stop = True
        
if __name__ == "__main__":
    follow = PresentFollows()
    follow.start()
    
    like = PresentLikes()
    like.start()
   
    
