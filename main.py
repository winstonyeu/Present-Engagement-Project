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

# if config.dictionary.get('accesstoken') == None:
#     config.AddAtribute('accesstoken', presentAPI.getAccessToken(config.dictionary['email'], config.dictionary['password']))
#     print("Added accesstoken to file")

# class Stopwatch(threading.Thread): 
#     def __init__(self, seconds):
#         super(Stopwatch, self).__init__()
#         self.seconds = seconds
#         self.current = 0
#         self.elapsed = 0
#         self.buffer = 0
#         self.temptiming = []
#         self.timing = []
#     
#     def setTiming(self, timing):
#         self.timing = list(timing)
#         self.temptiming = list(timing)
#     
#     def setBuffer(self, buffer):
#         self.buffer = buffer
#         pass
#     
#     def indicator(self):
#         while True:
#             if len(self.timing) <= 0:
#                 wait = self.buffer - (self.seconds-self.current)
#                 if wait > 0:
#                     print("Waiting remaining", wait, "seconds")
#                     time.sleep(wait)
#                 self.resetTiming()
#                 return False
#                 #break
#             
#             for number in self.timing:
#                 if (self.seconds-self.current) == number:
#                     print(number)
#                     self.timing.remove(number)
#                     return True
#     
#     def resetTiming(self):
#         self.timing = self.temptiming
#         #self.current = self.seconds
#         
#     def run (self):
#         while True:
#             self.current = self.seconds
#             while self.current >= 0:
#                 time.sleep(1)
#                 self.current -= 1
#                 #print(self.seconds, self.current, self.seconds-self.current)
#         
#         start = time.time()
#         time.clock()    
#         
#         while self.elapsed < self.seconds+1:
#             self.elapsed = int(time.time() - start) + 1
#             print(self.elapsed)
#             time.sleep(1)

class Timer(threading.Thread):
    def __init__(self):
        super(Timer, self).__init__()
        self.elapsed = 0
        self.tempcurrent = 0
        self.tempcurrent2 = 0
        self.buffer = 0
        self.tempstart = time.time()
        self.timing = []
        self.previousTime = 0
        self.stop = False
    
    def bufferTime(self, buffer):
        self.buffer = buffer
    
    def timeBetween(self, followerCount):
        return int(self.buffer/followerCount)
    
    def setTiming(self, timing):
        self.timing = list(timing)
    
    def resetTiming(self):
        self.tempcurrent = 0
        
    def reset(self):
        self.tempcurrent = 0
        self.buffer = 0
        del self.timing[:]
        
    def indicator(self):
        if len(self.timing) <= 0:
            remainingTime = self.buffer - self.tempcurrent
            if remainingTime > 0:
                print("\nWaiting remaining", remainingTime, "seconds")
                time.sleep(remainingTime)
            self.previousTime = 0
            self.resetTiming()
            return 1

        for timing in self.timing:
            if self.tempcurrent == timing:
                self.timing.remove(timing)
                return 0
        
        return 2
    
    def run(self):
        while self.stop == False:
            time.sleep(1)
            self.elapsed += 1
            self.tempcurrent += 1
            self.tempcurrent2 += 1
            print("Elapsed:", self.elapsed, "Current", self.tempcurrent)
        return
            
if __name__ == "__main__":
    Login = RetrieveUser()
    alluser = Login.retrieveAll()
     
    timer = Timer()
    timer.start()
     
    timings = []
    timings.append([10, 40])                 # 0-1  mins
    timings.append([15, 30, 45, 60])         # 1-2  mins
    timings.append([10, 20, 30, 40, 50, 60]) # 2-3  mins
    timings.append([270, 540])               # 3-12 mins
     
    index = 0
    bufferTime = 60
    timer.bufferTime(bufferTime)
     
    timer.setTiming(timings[0])
    
    maxtime = []
    maxtime.append(720)
    maxtime.append(3600)
    maxtime.append(12*60*60)
    maxtimeindex = 0
     
    numoffollower = 0
    lengthOfFollower = 0
    
    print("Start")
     
    # First hour
    while True:
        if len(alluser) == 0:
            print("All user followed")
            break    

        if timer.tempcurrent2 >= maxtime[maxtimeindex]:
            index = 0

            del timings[:]
            if maxtimeindex == 0:    
                timings.append([180, 360, 540, 720])            # 12-24 48-60 # 12 mins
                timings.append([120, 240, 360, 480, 600, 720])  # 24-36       # 12 mins
                timings.append([360, 720])                      # 36-48       # 12 mins  
                maxtimeindex += 1
            elif maxtime == 1:
                timings.append([3600, 3600, 3600, 3600, 3600, 3600,
                                3600, 3600, 3600, 3600, 3600])
                maxtimeindex += 1
            elif maxtimeindex == 2:
                timer.tempcurrent2 = 0
                randomfollowersnum = randint(5, 10)
                
                timing = []
                dividedtime = int(maxtime[maxtimeindex] / randomfollowersnum)
                for time in range(randomfollowersnum):
                    timing.append(dividedtime)
                
                timings.append(timing)
            
            bufferTime = maxtime[maxtimeindex]
            timer.bufferTime(bufferTime)
            
            timer.setTiming(timings[0])
            timer.resetTiming()
            
#         while timer.elapsed >= maxtime:
#             if timer.elapsed < 3600:
#                 print("First 12 minutes done")  
#                 index = 0
#                 maxtime = 3600
#                 bufferTime = 720
#                 timer.bufferTime(bufferTime)
#             
#                 del timings[:]
#                 timings.append([180, 360, 540, 720])            # 12-24 48-60 # 12 mins
#                 timings.append([120, 240, 360, 480, 600, 720])  # 24-36       # 12 mins
#                 timings.append([360, 720])                      # 36-48       # 12 mins
#                 timer.setTiming(timings[0])
#                 timer.resetTiming()
#             elif timer.elapsed > 3600+1:
#                 print("First hour done")
#                 index = 0
#                 maxtime = 11 * 60 * 60
#                 bufferTime = 1 * 60 * 60
#                 timer.bufferTime(bufferTime)
#                 
#                 del timings[:]
#                 timings.append([3600, 3600, 3600, 3600, 3600, 3600,
#                                 3600, 3600, 3600, 3600, 3600])
#                 timer.setTiming(timings[0])
#                 timer.resetTiming()

        result = timer.indicator()
        
        if result == 0:
            # Get rand user and login
            randindex = randint(1, len(alluser))
            randloginuser = Login.retrieveIndividual(randindex)
            #Login.removeIndividual(randloginuser)
            #api.loginUser(randloginuser['email'], randloginuser['password'])
                  
            # Follow user
            print(randloginuser['firstname'] + " followed random user")
            numoffollower+=1
            print("Followers:", numoffollower)
            #api.followUser("123")
            #api.logoutUser()
        elif result == 1:
            index += 1
            if index >= len(timings):
                index = 0
                 
            timer.setTiming(timings[index])
            print("Time elapsed:", timer.elapsed)
            print("Done, continuing with next minute")
        
        if len(timer.timing) != 0:
            if lengthOfFollower != len(timer.timing):
                lengthOfFollower = len(timer.timing)
                print("\nWaiting",  timer.timing[0] - timer.previousTime, "seconds until", timer.timing[0], "seconds")
            timer.previousTime = timer.timing[0]
    
    timer.stop = True
    
#     maxtime = 11 * 60 * 60
#     bufferTime = 1 * 60 * 60
#     timer.bufferTime(bufferTime)
#     timings.append([3600, 3600, 3600, 3600, 3600, 3600,
#                     3600, 3600, 3600, 3600, 3600])   
#      
#     while timer.elapsed < maxtime+1:
#         result = timer.indicator()
#          
#         if result == 0:
#             randindex = randint(1, len(alluser))
#             randloginuser = Login.retrieveIndividual(randindex)
#             #Login.removeIndividual(randloginuser)
#             #api.loginUser(randloginuser['email'], randloginuser['password'])        
#                       
#             print(randloginuser['firstname'] + " followed random user")
#             numoffollower+=1
#             print("Followers:", numoffollower)
#             #api.followUser("123")
#             #api.logoutUser()
#      
#     print("First day done")
# 
#     randomnumfollowers = randint(5, 10)
#     print(randomnumfollowers)
    
#     Login = RetrieveUser()
#     timer = Stopwatch(43200)
#     
#     alluser = Login.retrieveAll()
#     
#     timer.start()
# 
#     timing = []
#     timing.append([10, 40])
#     timing.append([15, 30, 45, 60])
#     timing.append([10, 20, 30, 40, 50, 60])
# 
#     index = 0
#     buffer = 60
#     
#     print("Start")
#     timer.setTiming(timing[index])
#     while True:
#         if len(alluser) == 0:
#             print("All user followed")
#             break
#         
#         timer.setBuffer(60)
#         while True: 
#             if timer.indicator():
#                 # Get rand user and login
#                 randindex = randint(1, len(alluser))
#                 randloginuser = Login.retrieveIndividual(randindex)
#                 Login.removeIndividual(randloginuser)
#                 api.loginUser(randloginuser['email'], randloginuser['password'])
#                     
#                 # Follow user
#                 print(randloginuser['firstname'] + " followed random user")
#                 #api.followUser("123")
#                 api.logoutUser()
#             else:
#                 index+=1
#                 if index >= len(timing):
#                     index = 0
#                     
#                 timer.setTiming(timing[index])
#                 print("Done\n")
#                 break    
#       
#     Login = RetrieveUser()
#     Follow = RetrieveUser()
#     
#     start = time.time()
#     while True:
#         alluser = Login.retrieveAll()
#         
#         if len(alluser) <= 0:
#             print("Done unfollowing all users")
#             break
# 
#         randindex = randint(1, len(alluser))
#         randloginuser = Login.retrieveIndividual(randindex)
#         
#         print("No. of login users in list -", len(Login.retrieveAll()))
#         print("Logged in as", randloginuser['firstname'])
#         api.loginUser(randloginuser['email'], randloginuser['password'])
#         Follow.removeIndividual(randloginuser)
#         
#         while True:
#             alluser = Follow.retrieveAll()
#              
#             if len(alluser) <= 0:
#                 print("followed all user")
#                 print("Removing", randloginuser['firstname'], "from login list\n")
#                 Login.removeIndividual(randloginuser)
#                 Follow.resetUserList()
#                 break
#              
#             randindex = randint(1, len(alluser))
#             randfollowuser = Follow.retrieveIndividual(randindex)
#              
#             randusername = randfollowuser['firstname']
#             randuserid = randfollowuser['id']
#              
#             if api.checkFollowingStatus(randuserid):
#                 print("Already followed", randusername)
#                 Follow.removeIndividual(randfollowuser)
#             else:
#                 print("following", randusername)
# #                 print("Waiting 5 seconds before following")
# #                 time.sleep(5)
#                 api.followUser(randuserid)
#                 print("Done following", randusername, "\n")
#                 Follow.resetUserList()
#                 break
#     end = time.time()
#     elapsed = end - start
#     print("Took %s seconds to complete" % elapsed)


