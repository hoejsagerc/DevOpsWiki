import json
from this import d
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == "GET":
        data = None
        try:
            req = requests.get('http://localhost:5001/users')
            data = req.json()['users']
        except:
            print("Failed getting users from api")

        if data != None:
            return render_template('index.html', data=data, message="")
        else:
            return render_template('index.html', data={}, message="No connection to API Service")
    elif request.method == "POST":
        username = request.form.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        payload = json.dumps({
            "username": username,
            "firstName": firstName,
            "lastName": lastName
        })
        post_req = requests.post('http://localhost:5001/users', data=payload, headers={"content-type": "application/json"})
        req = requests.get('http://localhost:5001/users')
        data = req.json()['users']
        return render_template('index.html', data=data, message="")


@app.route('/<username>', methods=['POST'])
def delete_user(username):
    del_req = requests.delete(f'http://localhost:5001/users/{username}')
    req = requests.get('http://localhost:5001/users')
    data = req.json()['users']
    return render_template('index.html', data=data, message="")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)