import requests, csv, os.path
from collections import OrderedDict

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
    
    def retrieveUsers(self, nat, count, apikey):
        r = requests.get('http://api.randomuser.me/?nat=%s&results=%s&key=%s' % (nat, count, apikey))
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
            
    def writeUserID(self, email, userid):
        once = False
        csvfile = open(self.filename, "a+", newline='')
        csvfile.seek(0, 0)
        reader = csv.reader(csvfile)
        writer = csv.writer(csvfile)
        for row in reader:
            if once == False:
                open(self.filename, 'w').close()
                once = True
            if email == row[3]:
                row[2] = userid
            writer.writerow(row)
        csvfile.close()
        print("Done writing id to csv")
                    
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
    
    def saveImage(self, user):
        filename = "dp/%s.jpg" % (user['firstname']+user['lastname'])
        if not os.path.exists("dp"):
            os.makedirs("dp")
        if os.path.isfile(filename) == True:
            print("Image %s already exist" % filename)
            return 0
        
        r = requests.get(user['picture'])
        with open(filename, "wb") as f:
            f.write(r.content)
        print("Done saving image")