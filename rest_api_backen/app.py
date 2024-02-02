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
    if not request.args:
        url = "http://admin:password@localhost:5984/reviews/_all_docs?include_docs=true"
        response = requests.get(url)
        return response.json().get('rows')

    if "dealerId" in request.args:
            headers = {"Content-Type": "application/json"}
            url = "http://admin:password@localhost:5984/reviews/_find"
            json = {"selector":{"dealership":int(request.args["dealerId"])}}
            response = requests.post(url, json=json, headers=headers)
            return response.json().get("docs")

@app.get("/api/review/<int:dealership>")
def get_review_by_id(dealership):
    headers = {"Content-Type": "application/json"}
    url = "http://admin:password@localhost:5984/reviews/_find"
    json = {"selector":{"dealership":dealership}}
    response = requests.post(url, json=json, headers=headers)

    return response.json().get("docs")


@app.post("/api/review")
def add_reviews():
    headers = {"Content-Type": "application/json"}
    
    json = request.get_json()
    url = "http://admin:password@localhost:5984/reviews"
    response = requests.post(url, json=json, headers=headers)

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=4444)
