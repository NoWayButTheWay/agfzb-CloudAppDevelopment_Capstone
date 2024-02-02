import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url, 
            headers={'Content-Type': 'application/json'},
            params=kwargs
        )
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    
# post request to make new review
def post_request(url, json):
    print()
    headers={'Content-Type': 'application/json'}
    response = requests.post(url, json=json, headers=headers)
    print(response.text)
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    
    results = []
    # Call get_request with a URL parameter
    array_result = get_request(url, dealerId=dealerId)
    if array_result:
        # Get the row list in JSON as dealers
        reviews = array_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership=review_doc["dealership"], 
                name=review_doc["name"], 
                purchase=review_doc["purchase"], 
                review=review_doc["review"], 
                purchase_date=review_doc["purchase_date"], 
                car_make=review_doc["car_make"], 
                car_model=review_doc["car_model"], 
                car_year=review_doc["car_year"], 
                sentiment=analyze_review_sentiments(review_doc["review"]), # will be change to data from ai 
                id=review_doc["id"]
            )
            results.append(review_obj)
    return results



# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/cb302777-500f-445e-a9f4-a14f79c0efbb/v1/analyze'
    api_key = '8PQfmmA6s_tLBB7y5g4bgjuCtRUkxy4Y5Q4TIf7qNCmR'
    json = {
        "text": "I love apples! I do not like oranges."
    }
    headers = {
    'Content-Type': 'application/json'
    }

    params = {
        'version': '2021-08-01',
        'features': {
            'sentiment': {},
        }
    }
    response = requests.post(url, json=json, params=params, headers=headers, auth=HTTPBasicAuth('apikey', api_key))
    result = response.json()
    sentiment = result['sentiment']['document']
    sentiment_label = sentiment['label']
    if sentiment_label == 'positive':
        print("Sentiment: Positive")
        return 'Positive'
    elif sentiment_label == 'neutral':
        print("Sentiment: Neutral")
        return 'Neutral'
    elif sentiment_label == 'negative':
        print("Sentiment: Negative")
        return 'Negative'
    else:
        print("Sentiment: Unknown")
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



