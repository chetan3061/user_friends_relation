# USER FRIENDS RELATION PROJECT
 
## Getting started
download the file and install the requirements using requirements.txt and connect to database 
  
### To seed data to database
To seed data to the database run seeder.py  
  
ex: python seeder.py 
  
the seeder adds 1000 users to the database first and then develops relation table to add friends to the users.
  
The batch size to do bulk insert is 100. You can change it manually 
 
### To get friends list and suggested friends list using api  

Access local api @ local_host/friends 

**ex: http://127.0.0.1:8000/friends**
 
To get the friends and the suggest friends through api, you have to post the user name 
 
**ex: {"user_name":"nihit"}**   

if many users found with the same name the result will be only for one user 
 
The obtained  result is in the form of 
 
{'friends': ['chetan', 'siddhu', 'mouli'], 'suggested_friends': ['ravi', 'ram', 'shiva']} 
