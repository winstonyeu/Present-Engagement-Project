import Configuration
from PresentAPI import PresentAPI
from random import randint
import time, threading
from RetrieveUser import RetrieveUser
from colors import red, green
        
api = PresentAPI()
config = Configuration.Configuration('config.ini')
apikey = config.dictionary['apikey']

class Timer(threading.Thread):
    def __init__(self, className):
        super(Timer, self).__init__()
        self.className = className
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
        self.elapsed = 0
        
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
                print("\n" + self.className + " - Waiting remaining", remainingTime, "seconds")
                time.sleep(remainingTime+1)
            self.previousTime = 0

    
        return False
    
    def run(self):
        while self.stop == False:
            time.sleep(1)
            self.elapsed += 1
            self.tempelapsed += 1
            #print("Elapsed:", self.elapsed, "Temp Elapsed:", self.tempelapsed)
        return
    
class PresentFollows(threading.Thread):
    def __init__(self):
        super(PresentFollows, self).__init__()
        
        self.Login = RetrieveUser()
        self.alluser = self.Login.retrieveAll()
        
        self.timer = Timer("Follow")
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
        self.show = True
        self.starttime = 0
        self.stoptime = 0
        self.currentuserid = 0
       
    
    def reset(self):
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
        self.show = True
        self.starttime = 0
        self.stoptime = 0
        self.currentuserid = 0
        
    def followUser(self, userid):
        # Get rand user and login
        randindex = randint(1, len(self.alluser))
        randloginuser = self.Login.retrieveIndividual(randindex)
        self.Login.removeIndividual(randloginuser)
        api.loginUser(randloginuser['email'], randloginuser['password'])
              
        # Follow user
        api.followUser(userid)
        print(red("Follow - " + randloginuser['firstname'] + " followed Stephen"))
        self.numoffollower+=1
        print(red("Follow - Followers: " + str(self.numoffollower)))
        api.logoutUser()
        self.show = True
        
    def run(self):
        print(red("Follow - Start"))
        while True:
            # Get new user
            # E.g.
#             userid = self.alluser[0]['id']
#             self.Login.removeIndividual(self.alluser[0])
            
            #Not real API function, check PresentAPI class
            userid = api.getNewUser()['_id']
            
            if self.currentuserid != userid:
                # Reset
                self.reset()
                self.timer.resetTiming()
                self.currentuserid = userid
            
                # First hour
                while True:
                    if len(self.alluser) == 0:
                        print(red("All user followed"))
                        break    
                    
                    if self.timer.tempelapsed >= self.maxtime[self.maxtimeindex]:          
                        del self.timings[:]
                        
                        self.starttime = time.time()
                        threading.Thread(target=self.followUser, args=(userid,)).start()
                        if self.maxtimeindex == 0:    
                            self.timings.append([7200, 10800, 14400, 18000, 21600, 
                                                25200, 28800, 32400, 36000, 39600, 43200])
                            self.timer.setTiming(self.timings)
                            self.maxtimeindex += 1
                            print(red("Follow - First hour done"))
                        elif self.maxtimeindex == 1:
                            self.timer.tempelapsed = 0
                            randomfollowersnum = randint(5, 10)
                             
                            timing = []
                            dividedtime = int(self.maxtime[self.maxtimeindex] / randomfollowersnum)
                            for t in range(randomfollowersnum):
                                timing.append(dividedtime)
                             
                            self.timings.append(timing) 
                            self.timer.setTiming(self.timings)
         
                    result = self.timer.indicator()
                    
                    if result:
                        self.starttime = time.time()
                        threading.Thread(target=self.followUser, args=(userid,)).start()
                        
                    if len(self.timer.timing[0]) != 0 and self.show:
                        self.timer.previousTime = self.timer.tempelapsed
                        if self.lengthOfFollower != len(self.timer.timing[0]):
                            self.lengthOfFollower = len(self.timer.timing[0])
                            if self.starttime != 0:
                                self.stoptime = int(time.time() - self.starttime)
                            print(red("\nFollow - Waiting " +  str(self.timer.timing[0][0] - (self.timer.previousTime-self.stoptime)) + " seconds until " + str(self.timer.timing[0][0]) + " seconds"))
                        self.show = False
            time.sleep(1)

class PresentLikes(threading.Thread):
    def __init__(self):
        super(PresentLikes, self).__init__()
         
        self.Login = RetrieveUser()
        self.alluser = self.Login.retrieveAll()
         
        self.timer = Timer("Like")
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
        self.starttime = 0
        self.stoptime = 0
        self.show = True
        self.currentpresentid = 0
    
    def reset(self):
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
        self.starttime = 0
        self.stoptime = 0
        self.show = True
        self.currentpresentid = 0
    
    def likeUser(self, presentID):
        # Get rand user and login
        randindex = randint(1, len(self.alluser))
        randloginuser = self.Login.retrieveIndividual(randindex)
        #Login.removeIndividual(randloginuser)
        #api.loginUser(randloginuser['email'], randloginuser['password'])
              
        # Like user
        print(green("Like - " + randloginuser['firstname'] + " liked random user"))
        self.numofliker+=1
        print(green("Like - Likers: " + str(self.numofliker)))
        #api.likerPresent(presentID)
        #api.logoutUser()
        self.show = True
                
    def run(self):
        print(green("Like - Start"))
        
        while True:
            presentID = "123"
            
            if self.currentpresentid != presentID:
                # Reset
                self.reset()
                self.timer.resetTiming()
                self.currentpresentid = presentID
                    
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
                        self.starttime = time.time()
                        threading.Thread(target=self.likeUser, args=(presentID,)).start()
        
                    if len(self.timer.timing[0]) != 0 and self.show:
                        self.timer.previousTime = self.timer.tempelapsed
                        if self.lengthOfLiker != len(self.timer.timing[0]):
                            self.lengthOfLiker = len(self.timer.timing[0])
                            if self.starttime != 0:
                                self.stoptime = int(time.time() - self.starttime)
                            print(green("\nLike - Waiting " +  str(self.timer.timing[0][0] - (self.timer.previousTime-self.stoptime)) + " seconds until " + str(self.timer.timing[0][0]) + " seconds"))
                        self.show = False
                    elif len(self.timer.timing[0]) == 0:
                        self.lengthOfLiker = 0
                time.sleep(1)
        
if __name__ == "__main__":
#     randomuser = RetrieveUser()
#     users = randomuser.retrieveAll()
#   
#     userid = users[0]['id']
#     randomuser.removeIndividual(users[0])
#         
#     for user in users:
#         api.loginUser(user['email'], user['password'])
#         api.unfollowUser(userid)
#         print(user['firstname'], "unfollowed stephen")
#         api.logoutUser()
        
#    for user in users:
#         if api.registerUser(user['firstname'], user['email'], user['password']) == False:
#             continue
#         api.loginUser(user['email'], user['password'])
#         userid = api.me()['_id']
#         randomuser.writeUserID(user['email'], userid)
#         api.logoutUser()
#    
#    print("Done")
    
# Example of API use
#     for user in users:
#         api.loginUser(user['email'], user['password'])
#         # Change display pic
#         api.changeDisplayPicture("dp/%s.jpg" % user['firstname'])
#         # Update name
#         api.updateName(str(user['firstname']).title())
#         # Update about
#         api.updateAbout("Hello, my name is " + str(user['firstname']).title() + "!")
#         api.logoutUser()

    follow = PresentFollows()
    follow.start()
        
    like = PresentLikes()
    like.start()
    
