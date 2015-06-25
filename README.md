# python-present-engagement
A project for Present Engagement using Present API

Refer to Present API for endpoints: https://github.com/winstonyeu/PresentAPI

**Info**
--------------------------
Uses Present API to follow and like user posts

Integrates randomuser.me API & RandomAPI to create seed users for Present 

**Authenticatication**
--------------------------
**Authenticating a user for Present**

Logging in to retrieve and sets the access token

```python
from PresentAPI import PresentAPI

api = PresentAPI()
api.loginUser("email", "password")
```
 
**Authenticating a user for RandomAPI**

Authenticating with RandomAPI allows for more data retrieval from randomuser.me

[Register](https://randomapi.com/) and get the API key from RandomAPI

Save API key into config.ini file

```
[AUTHENTICATION]
apikey = 0000-0000-0000-0000
```

**Creating user using randomuser API**
-------------------------------------
Create users and stores into csv file

```python
randomuser = RetrieveUser()
users      = randomuser.retrieveUsers("count", "apikey")
randomuser.saveUserInfo(users)
```

Retrieve from csv file

```python
randomuser = RetrieveUser()

users    = randomuser.retrieveAll()
user     = randomuser.retrieveIndividual(0)
user     = randomuser.retrieveIndividualByName("scarlett")
```

Available user info : firstname, lastname, present id, email, password, profile picture url

Present ID only available after registering with Present

```python
randomuser = RetrieveUser()
user     = randomuser.retrieveIndividualByName("scarlett")

print(user['firstname'], user['lastname'], user['id'], user['email'], user['password'], user['picture'])

# scarlett, lowe, 5453ae9h109493857463q183, scarlett.lowe33@example.com, monarch, http://api.randomuser.me/portraits/women/14.jpg
```

**Creating Present user**
-------------------------
Create Present user

```python
from PresentAPI import PresentAPI

api = PresentAPI()
api.registerUser("name", "email", "password")
```

Creating with the randomme list

```python
from PresentAPI import PresentAPI

api = PresentAPI()

randomuser = RetrieveUser()
users    = randomuser.retrieveAll()

for user in users:
	api.registerUser(user.firstname, user.email, user.password)
```

**Classes & Functions**
-------------
**Timer class**

Threaded timer class to run asynchronously with main function

```
init()
setTiming(timing)
resetTiming()
indicator()
run()
```

**PresentFollows class**

Threaded follow class to run asynchronously with like class (See below for like class)

```
init()
run()
```

**How it works**
----------------
**Main function**

The indicator will check whether to wait or to follow

```python
result = self.timer.indicator()
if result:
	# Follow
else:
	# Do whatever
```

**Follow class**

Create custom timing and number of follows

- John joins Present 
- 1st Minute: 2 New Followers (10 second mark, 40 second mark)
- 2nd Minute: 4 New Followers 
- 3rd Minutes: 6 New Followers 
- 12th Minutes: 2 New Follower
- After 24 Minutes: 4 New Followers
- After 36 Minutes: 6 New Followers
- After 48 Minutes: 2 New Follower
- After 60 Minutes: 4 New Followers
- THE VERY FIRST HOUR: 30 Followers

```python
self.timings = []
# Number of value in list = number of follows (e.g. [10, 40] = 2 follows)
# Value in list = the time it will like (e.g. 10 = 10 second mark, 40 = 40 second mark)
self.timings.append([10, 40])                             # 1st minute 2 follows on 10 & 40 sec mark
self.timings.append([75, 90, 105, 120])                   # 2nd minute 4 follows on 75, 90, 105, 120 sec mark
self.timings.append([130, 140, 150, 160, 170, 180])       # 3rd minute
self.timings.append([450, 720])                           # 12th minute
self.timings.append([900, 1080, 1260, 1440])              # 24th minute
self.timings.append([1560, 1680, 1800, 1920, 2040, 2160]) # 36th minute
self.timings.append([2520, 2880])                         # 48th minute
self.timings.append([3060, 3260, 3420, 3600])             # 60th minute
self.timer.setTiming(self.timings)
```

It will wait accordingly to the next timing (e.g. 20 + 15 secs from 1st min to 2nd min as 1st min ended on 40 sec and 2nd min starts on 75 sec)

**Like class**

FIRST 8 Minutes:

- 1st Minute: 1 Like
- 2nd Minutes: 2 Likes
- 3rd Minutes: 3 Likes
- 6th Minute = 1 Likes
- 8th Minute =  2 Likes
- Total Likes in 8 Minutes: 9 Likes

- 20th Minute = 1 Like 
- 30th Minute = 1 Like 
- 40th Minute = 1 Like 
- 50th Minute = 1 Like 
- 60th Minute = 1 Like 
- Total Likes in 40 Minutes: 5 Likes

- Total Likes For Video: 14

```python
self.timings = []
# Number of value in list = number of likes (e.g. [60] = 1 like)
# Value in list = the time it will follow (e.g. 60 = 60 second mark)
self.timings.append([60])							# 1st minute 1 like on 60 sec mark
self.timings.append([90, 120])						# 2nd minute 2 like on 90, 120 sec mark
self.timings.append([140, 160, 180])				# 3rd minute 3 like on 140, 160, 180 sec mark
self.timings.append([240])							# 6th minute 1 like on 240 sec mark
self.timings.append([360, 480])						# 8th minute 2 like on 360, 480 sec mark
self.timings.append([1200, 1800, 2400, 3000, 3600]) # 20, 30, 40, 50, 60th minute each 1 like
self.timer.setTiming(self.timings)
```

It will wait accordingly to the next timing (e.g. 20 + 10 secs from 2nd min to 3rd min as 2nd min ended on 120 sec and 3rd min starts on 140 sec)

**Create custom time markers**

```python
self.maxtime = []
self.maxtime.append(3600)
self.maxtimeindex = 0

# If time elapsed reaches time marker, do whatever
if self.timer.elapsed >= self.maxtime[self.maxtimeindex]:          
	# Do whatever you want    
	
(Example)
if self.timer.elapsed >= self.maxtime[self.maxtimeindex]:          
	del self.timings[:]

	if self.maxtimeindex == 0:    
		self.timings.append([7200, 10800, 14400, 18000, 21600, 
							25200, 28800, 32400, 36000, 39600, 43200])
		self.timer.setTiming(self.timings)
		self.maxtimeindex += 1
		print("First hour done")
``` 

