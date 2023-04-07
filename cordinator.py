# -*- coding: utf-8 -*-
"""
3PC Distributed Computing
 
"""

import pymongo
from time import sleep

# ****************************************************************************
# Setup connection with DB
# ****************************************************************************
# default ip address & port of Mongodb 
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

# Pick DB from MongoDB with its name 
cor_db = client['Cordinator']

# from selected DB, select "Tiktok_Accounts" collection 
admin_record = cor_db.admin

commit_db = cor_db.commit

# ===========================================================================
# Set up DB 2
# ===========================================================================

# Pick DB from MongoDB with its name 
part_db = client['Participant']

# from selected DB, select "Tiktok_Accounts" collection 
user_records = part_db.user

# ****************************************************************************
# Setup connection with DB
# ****************************************************************************


# cordinator = "Being to Commit"

# user 1
user_1 = input("> User 1 add your name: ")

user_0 = ""

user_ = user_1
for record in user_records.find({'name': user_}):
    user_0 = record["name"]


if user_1 == user_0:
    print("==================================================")
    print("User 1 name alredy exist you can use this name")
    print("==================================================")
    
    cor_1 = input("So, Are you Ready to commit: ")
    
    user_records.update_one({'name' : f'{user_1}'},{"$set": {'commit_status' : f'{cor_1}'}})
    
else:
    cor_1 = input("Are you Ready to commit: ")
    user_records.insert_one({'name' : f'{user_1}', 'commit_status' : f'{cor_1}'})

# user 2
user_2 = input("> User 2 add your name: ")

user_ = user_2
for record in user_records.find({'name': user_}):
    user_0 = record["name"]

if user_2 == user_0:
    print("==================================================")
    print("User 2 name alredy exist you can use this name")
    print("==================================================")
    cor_2 = input("So, Are you Ready to commit: ")
    user_records.update_one({'name' : f'{user_2}'},{"$set": {'commit_status' : f'{cor_2}'}})
else:
    cor_2 = input("Are you Ready to commit: ")
    user_records.insert_one({'name' : f'{user_2}', 'commit_status' : f'{cor_2}'})


print("> Do you want to fail the Coordinator")
print("1) Click 1 for server pass")
print("2) Click 2 for server fail")

server_status = None

server = int(input("Enter Your Value : "))
if server == 1:
    print("Server is Okay")
    server_status = True
else:
    print(" Server isn't Okay")
    server_status = False


# Check the user commits
if cor_2 == "YES" or cor_2 == "yes" or cor_2 == "Yes" and  cor_1 == "YES" or cor_1 == "yes" or cor_1 == "Yes":
    
    for record in admin_record.find_one():
        status = record
    
    if status == "":
        admin_record.insert_one({"Status": "Yes"})
        print("> All users are Ready")
    
    else: 
        admin_record.update_one({},{"$set":{"Status" : "Yes"}})
        print("> All users are Ready")
        
        print("==================================================")
        print("Ready to prepare the commit")
        print("==================================================")
        
        sleep(2)
        
        user_records.update_many({},{"$set":{"all_users_status":"Yes"}})
        print("> Done to send prepare commit acknowledge to Users by Cordinator")
        
        sleep(2)
        
        admin_record.update_one({"Status" : "Yes"},{"$set":{"user_ready_state" : "Done"}})
        print("> Done to send (ready commit) acknowledge to cordinator by Users")
        
        sleep(2)
        user_records.update_many({"Status" : "Yes"},{"$set":{"cordinator_order":"You are ready to commit"}})
        print("> Done to send (You may write your commit now) acknowledge to Users by cordinator")
        
        sleep(2)
        admin_record.update_many({"Status" : "Yes"},{"$set":{"cordinator_order":"You are ready to commit"}})
        print("> Done to send (I am writing commit) acknowledge to Users by cordinator")
        
        sleep(2)
        
        commit = input("Enter your commit : ")
        commit_db.update_one({"commit": []},{"$push" : {"commit" : commit}})
        
        print("> Commited ")
        print("> Transaction End ")

else:
    
    for record in admin_record.find_one():
        status = record
        
    admin_record.update_one({},{"$set":{"Status" : "No"}})
    print("> All users are not Ready")
    
    sleep(2)
    print("==================================================")
    print("I am not Ready to commit prepration")
    print("==================================================")
    
    sleep(2)
    user_records.update_many({"Status" : "No"},{"$set":{"all_users_status":"No"}})
    print("> Done to send Not prepare commit acknowledge to Users by Cordinator")
    print("Check Db now")
    
    sleep(2)
    admin_record.update_one({"Status" : "No"},{"$set":{"user_ready_state" : "Failed!"}})
    print("> Done to send (not ready commit) acknowledge to cordinator by Users")
    print("Check Db now")
    
    sleep(2)
    user_records.update_many({"Status" : "No"},{"$set":{"cordinator_order":"You are not ready to commit"}})
    print("> Done to send (You may write your commit now) acknowledge to Users by cordinator")
    
    sleep(2)
    admin_record.update_many({"Status" : "Yes"},{"$set":{"cordinator_order":"You are not ready to commit"}})
    print("> Done to send (I am writing commit) acknowledge to Users by cordinator")
    
    sleep(2)
    
    print("you can't add the commit here")
    
    print("> Transaction End ")