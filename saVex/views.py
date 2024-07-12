from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from .utils import RetirementCalculations
from .models import *
from django.views.generic import TemplateView
from django.urls import path
import requests, json
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .payload import *

# create a view that will render the index.html template
# def index(request):
#     return HttpResponse("Hello, world. You're at the saVex index.")


urlpatterns = [
    # ... your other URL patterns ...
    path('template/', TemplateView.as_view(template_name='index.html'),  name='template')
]


import requests


# make sure that correct data type is passed to the class
data_type_mapper = {
    'retirement_age': lambda x: int(x),
    'birth_date': lambda x: datetime.strptime(x, '%Y-%m-%d'),
    'life_expectancy': lambda x: int(x),
    'annual_interest_rate': lambda x: float(x),
    'current_income': lambda x: int(x),
    'age': lambda x: int(x),
    'inflation_rate': lambda x: float(x),
    'retirement_recurring': lambda x: int(x),
    'rate_of_return': lambda x: float(x)
}

# use this function to get the life expectancy of a country and use as default value
@api_view(['GET'])
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
@api_view(['GET'])
def get_default_values(request):
    if request.method == 'GET':
        args_ = {}
        params = ["retirement_age", "birth_year","life_expectancy",
                "annual_interest_rate", "current_income"]
        birth_date = datetime(1985, 10, 31)
        values = [65, birth_date.strftime('%Y-%m-%d'), 80, 0.05, 1000000]
        for i in range(len(params)):
            args_[params[i]] = values[i]
        return JsonResponse(args_)

@require_POST
@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=MonthlyRetirementPayload)
@api_view(['POST'])
def get_monthly_retirement_fund(request):
    # Instantiate the RetirementCalculations class
    
    # Create a dictionary to store the values from the request
    arg_data = {}
    data = request.data
    args_ = list(data.keys())
    # Get the values from the request
    for arg in args_:
        if arg == 'infaltion_rate' or arg == 'annual_interest_rate':
            data[arg] = data_type_mapper[arg](data[arg])
            data[arg] = data[arg] / 100
        else: 
            arg_data[arg] = data[arg]  # Use request.POST.get(arg) for POST requests
            data[arg] = data_type_mapper[arg](data[arg])
    print(data)
    print(arg_data)

    retirement_calculations = RetirementCalculations(**data)
    monthly_investment = retirement_calculations.retirement()
    result = {
        'monthly_retirement_fund': monthly_investment
    }
    print(result)
    return JsonResponse(result)

@csrf_exempt
@api_view(['GET', 'POST'])
def get_inflation_intrest_rate_matrix(request):
    if request.method == 'GET':
        interest_rate = [0.10,0.12,0.14,0.16,0.18,0.20]
        inflation_rate = [0.04,0.05,0.06,0.07,0.08,0.09]
        # prepare the standard data arguments.
        matrix_collector_ = {}
        for int_ in range(len(interest_rate)):
            for rate_ in range(len(inflation_rate)):
                data = {"rate_of_return":interest_rate[int_],"inflation_rate":inflation_rate[int_],
                        "current_age":30,"retirement_age":60,"life_expectancy":80}
                retire = RetirementCalculations(**data)
                matrix_collector_["{},{}".format(interest_rate[int_],inflation_rate[rate_])] = retire.retirement()
        print(matrix_collector_)
        return JsonResponse(matrix_collector_, safe=False)

@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=GetPortfolioPayload)
@api_view(['GET','POST'])
def get_portfolio_trajectory(request):
    if request.method == 'GET':
        data = {"current_age":40,"retirement_age":65,"life_expectancy":80,
                "retirement_recurring": 30000}
        retire = RetirementCalculations(**data)
        portfolio_trajectory = retire.get_portfolio_trajectory()
        return JsonResponse(portfolio_trajectory, safe=False)
    
    if request.method == 'POST':
        # Create a dictionary to store the values from the request
        arg_data = {}
        data = request.data
        args_ = list(data.keys())
        # Get the values from the request
        for arg in args_:
            if arg == 'infaltion_rate' or arg == 'annual_interest_rate':
                data[arg] = data_type_mapper[arg](data[arg])
                data[arg] = data[arg] / 100
            else: 
                arg_data[arg] = data[arg]  # Use request.POST.get(arg) for POST requests
                data[arg] = data_type_mapper[arg](data[arg])
        retire = RetirementCalculations(**data)
        portfolio_trajectory = retire.get_portfolio_trajectory()
        return JsonResponse(portfolio_trajectory, safe=False)

@require_POST
@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=MonthlyRetirementPayload)
@api_view(['POST'])
def get_retirement_gap(request):
    # Create a dictionary to store the values from the request
    arg_data = {}
    data = request.data
    args_ = list(data.keys())
    # Get the values from the request
    for arg in args_:
        if arg == 'infaltion_rate' or arg == 'annual_interest_rate':
            data[arg] = data_type_mapper[arg](data[arg])
            data[arg] = data[arg] / 100
        else: 
            arg_data[arg] = data[arg]  # Use request.POST.get(arg) for POST requests
            data[arg] = data_type_mapper[arg](data[arg])
    print(data)
    print(arg_data)
    retire = RetirementCalculations(**data)
    retirement_gap = retire.Retirement_monthly_gap()
    result = {
        'retirement_gap': retirement_gap
    }
    return JsonResponse(result)
