from django.shortcuts import render
from django.db.models import Sum
# Create your views here.
from django.http import HttpResponse
from saVex.calculate import RetirementCalculations


def index(request):
    return HttpResponse("Hello, world. You're at the saVex index.")

from .models import *

def create_agg_items(request):
        # calculate the overall aggregated items
        TotalExpense = ExpenseItems.total_expense()
        TotalEarning = EarningItems.total_earning()
        SavingPerMonth = SavingsItems.total_savings()
        TotalInvestment = InvestmentItems.total_investment()
        TotalLiabilities = LiabilitiesItems.total_liabilities()
        NetWorth = TotalEarning - TotalExpense
        EmergencyFund = TotalExpense * 3
        RetirementFund += SavingsItems.NPS + SavingsItems.PF
        HouseFund += SavingsItems.HouseDownPayment
        ExpectedSavings_6months = (TotalEarning - TotalExpense) * 6
        # call the retirement function to calculate the retirement monthly gap
        RF = RetirementCalculations()
        Retirement_monthly_gap = RF.Retirement_monthly_gap()


        agg_items = AggregatedItems(
            TotalExpense = models.IntegerField(default=0),
            TotalEarning = models.IntegerField(default=0),
            SavingPerMonth = models.IntegerField(default=0),
            TotalInvestment = models.IntegerField(default=0),
            TotalLiabilities = models.IntegerField(default=0),
            NetWorth = models.IntegerField(default=0),
            EmergencyFund = models.IntegerField(default=0),
            RetirementFund = models.IntegerField(default=0),
            HouseFund = models.IntegerField(default=0),
            ExpectedSavings_6months = models.IntegerField(default=0),
            Retirement_monthly_gap = models.IntegerField(default=0),
            Savings_gap = models.IntegerField(default=0),
            Home_downpayment_gap = models.IntegerField(default=0))
        
        return render(request, 'index.html', {'agg_items': agg_items})