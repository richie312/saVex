from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from .calculate import RetirementCalculations
from .models import *
from django.views.generic import TemplateView
from django.urls import path
import requests, json
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt




# create a view that will render the index.html template
# def index(request):
#     return HttpResponse("Hello, world. You're at the saVex index.")


urlpatterns = [
    # ... your other URL patterns ...
    path('template/', TemplateView.as_view(template_name='index.html'),  name='template')
]


import requests

# use this function to get the life expectancy of a country and use as default value
def get_life_expectancy(country_code):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/SP.DYN.LE00.IN?format=json"
    response = requests.get(url)
    data = response.json()
    # Get the most recent life expectancy data
    for item in data[1]:
        if item['value'] is not None:
            return item['value']
    return None
@csrf_exempt
def get_default_values(request):
    if request.method == 'GET':
        args_ = {}
        params = ["retirement_age", "birth_year","life_expectancy",
                "annual_interest_rate", "current_income"]
        birth_date = datetime(1985, 10, 31)
        values = [65, birth_date.strftime('%Y-%m-%d'), round(get_life_expectancy('IN')), 0.05, 1000000]
        for i in range(len(params)):
            args_[params[i]] = values[i]
        return JsonResponse(args_)

@require_POST
@csrf_exempt
def get_monthly_retirement_fund(request):
    # Instantiate the RetirementCalculations class
    
    # Create a dictionary to store the values from the request
    arg_data = {}
    data = json.loads(request.body)
    args_ = list(data.keys())

    # Get the values from the request
    for arg in args_:
        arg_data[arg] = data[arg]  # Use request.POST.get(arg) for POST requests
    print(data)
    print(arg_data)
    retirement_calculations = RetirementCalculations(**data)
    monthly_investment = retirement_calculations.retirement()
    result = {
        'monthly_retirement_fund': monthly_investment
    }
    print(result)
    return JsonResponse(result)
