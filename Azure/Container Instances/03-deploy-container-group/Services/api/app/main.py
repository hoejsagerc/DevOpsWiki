import json
import os
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# creating the application object
app = FastAPI()
basedir = os.path.abspath(os.path.dirname(__file__))


class Item(BaseModel):
    username: str
    firstName: str
    lastName: str


# Rout for displaying all the users in users.json file
@app.get("/users", status_code=200)
async def get_users():
    data_file = os.path.join(basedir, 'data/users.json')
    with open(data_file, "r") as file:
        response = json.load(file) 
    return response


# Route for creating a new user to the users.json file
@app.post('/users', status_code=201)
async def new_user(item: Item):
    data_file = os.path.join(basedir, 'data/users.json')
    with open(data_file, "r") as file:
        users = json.load(file)
        new_user = {
            "username": item.username,
            "firstName": item.firstName,
            "lastName": item.lastName
        }
        users['users'].append(new_user)

    with open(data_file, "w") as file:
        json.dump(users, file)
    return item


# Route for deleting a user from the users.json file
@app.delete("/users/{username}", status_code=200)
async def delete_users(username):
    data_file = os.path.join(basedir, 'data/users.json')
    with open(data_file, "r") as file:
        users = json.load(file)
        i = 0
        for user in users['users']:
            if user['username'] == username:
                users['users'].remove(user)
                switch = True
            else:
                i += 1
        
    if switch == True:
        with open(data_file, "w") as file:
            json.dump(users, file)
        return {"message": f"user with username: {username}, was deleted"}
    else:
        return {"message": f"Could not find user with username: {username}"}
        

