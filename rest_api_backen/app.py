from flask import Flask, request, make_response
import json
import requests


app = Flask(__name__)

@app.route('/api/dealership')
def dealership():
    
    if not request.args:
        url = "http://admin:password@localhost:5984/dealerships/_all_docs?include_docs=true"
        response = requests.get(url)
        return response.json()
    
    if "state" in request.args:
        headers = {"Content-Type": "application/json"}
        url = "http://admin:password@localhost:5984/dealerships/_find"
        json = {"selector":{"state":request.args["state"]}}
        response = requests.post(url, json=json, headers=headers)
        return response.json().get("docs")[0]
    
    if "dealerId" in request.args:
        headers = {"Content-Type": "application/json"}
        url = "http://admin:password@localhost:5984/dealerships/_find"
        json = {"selector":{"id":int(request.args["dealerId"])}}
        response = requests.post(url, json=json, headers=headers)
        return response.json().get("docs")[0]
    
    return "error"
   # /api/review?dealerId=""
    

#curl -X POST http://admin:password@localhost:5984/dealerships/_find -H "Content-Type: application/json" -d '{"selector": {"id": 3}}'
@app.get("/api/dealership/<int:id>")
def get_dealership_by_id(id):
    headers = {"Content-Type": "application/json"}
    url = "http://admin:password@localhost:5984/dealerships/_find"
    json = {"selector":{"id":id}}
    response = requests.post(url, json=json, headers=headers)

    return response.json().get("docs")[0]

@app.get("/api/dealership/state/<string:state>")
def get_dealership_by_state(state):
    headers = {"Content-Type": "application/json"}
    url = "http://admin:password@localhost:5984/dealerships/_find"
    json = {"selector":{"state":state}}
    response = requests.post(url, json=json, headers=headers)
    return response.json().get("docs")[0]

@app.get("/api/review")
def get_review():
    url = "http://admin:password@localhost:5984/reviews/_all_docs?include_docs=true"
    response = requests.get(url)
    return response.json().get('rows')

@app.get("/api/review/<int:id>")
def get_review_by_id(id):
    headers = {"Content-Type": "application/json"}
    url = "http://admin:password@localhost:5984/reviews/_find"
    json = {"selector":{"id":id}}
    response = requests.post(url, json=json, headers=headers)

    return response.json().get("docs")[0]


@app.post("/api/review")
def add_reviews():
    headers = {"Content-Type": "application/json"}
    '''{
      "id": 2,
      "name": "Gwenora Zettoi",
      "dealership": 23,
      "review": "Future-proofed foreground capability",
      "purchase": true,
      "purchase_date": "09/17/2020",
      "car_make": "Pontiac",
      "car_model": "Firebird",
      "car_year": 1995
    }'''

    url = "http://admin:password@localhost:5984/reviews"
    json = {"selector":{"state":"state"}}
    response = requests.post(url, json=json, headers=headers)

    return response.json().get("docs")[0]


if __name__ == '__main__':
    app.run(debug=True,port=4444)
