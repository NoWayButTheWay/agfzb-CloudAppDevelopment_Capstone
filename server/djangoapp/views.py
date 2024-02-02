from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)    
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp:index', context)
    return ""
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    if request.method == "POST":
        logout(request)
        return redirect('djangoapp:index')
    if request.method == "GET":
        logout(request)
        return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))    
        if not user_exist:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index")
        
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "http://localhost:4444/api/dealership" #ibm function does not work 
        dealership_list = get_dealers_from_cf(url)
        context['dealership_list'] = dealership_list
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "http://localhost:4444/api/review" #ibm function does not work 
        dealer_reviews = get_dealer_reviews_from_cf(url, int(dealer_id))
        context['dealer_reviews'] = dealer_reviews
        context['dealer_id'] = dealer_id
        context['image'] = dealer_reviews
        url2 = "http://localhost:4444/api/dealership/"+str(dealer_id) #ibm function does not work 
        dealer_name = get_dealers_from_cf(url2)
        context['dealer_name'] = dealer_name
        return render(request, 'djangoapp/dealer_details.html', context)
# ...

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        context["dealer_id"] = dealer_id
        url2 = "http://localhost:4444/api/dealership/"+str(dealer_id) #ibm function does not work 
        dealer_name = get_dealers_from_cf(url2)
        context['dealer_name'] = dealer_name
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == "POST":
        print("ASDFSADFASDFASFDASFASD")
        url = "http://localhost:4444/api/review" #ibm function does not work
        json = {
            
            "name": request.POST["name"],
            "dealership": dealer_id,
            "review": request.POST["review"],
            "purchase": request.POST["purchase"],
            "purchase_date": request.POST["purchase_date"],
            "car_model": request.POST["car_model"],
    
        }
        dealer_reviews = post_request(url, json)
        context['dealer_reviews'] = dealer_reviews
        return redirect("/djangoapp/dealer/"+str(dealer_id))
# ...

