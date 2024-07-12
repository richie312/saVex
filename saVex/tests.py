from django.test import TestCase
from datetime import datetime
from .models import *  # replace with your model
from django.db.models import Sum, Min, Max
from .utils import *
import numpy_financial as npf

# Create your tests here.    
class TestUtilGenricFunctions(TestCase):
    def setUp(self):
        self.annual_rate_return = 0.10
        self.annual_interest_rate = 0.06
        self.adjusted_rate_return = ((1+self.annual_rate_return)/(1+self.annual_interest_rate)) - 1
        self.PV = 35000
        self.n = 1 # number of times that interest is compounded per year
        self.t = 25 # time the money is invested for in years
        self.nper = 20*12
        self.expense_item = ExpenseItems.objects.create(total_expense=1000)

    def test_total_grocery_expense(self):
        min_id = get_min_id(ExpenseItems)
        item = ExpenseItems.objects.get(id=min_id)
        fixed_expense = item.total_expense

class TestRetirementCalcuations(TestCase):
    def setUp(self):
        self.expense_item = ExpenseItems.objects.create(total_expense=1000)
        self.Salary = EarningItems.objects.create(Salary=122000)
        self.total_liabilities = LiabilitiesItems.objects.create(total_liabilities=50000)
        self.NPS = SavingsItems.objects.create(NPS=20000)
        
    def test_calculate_retirement_fund(self):
        retire = RetirementCalculations()
        monthly_nps_investment = retire.retirement()
        print("The monthy retirement investment is:".format(retire.monthly_nps_investment))

    def test_retirement_gap(self):
        retire = RetirementCalculations()
        retirement_gap = retire.Retirement_monthly_gap()
        print("The monthly investment gap is to maintain same life style and beat inflation:".format(retirement_gap))

    def test_inflation_intrest_rate_matrix(self):
        # Test the inflation and intrest rate matrix.
        interest_rate = [0.10,0.12,0.14,0.16,0.18,0.20]
        inflation_rate = [0.04,0.05,0.06,0.07,0.08,0.09]
        # prepare the standard data arguments.
        matrix_collector_ = {}
        for int_ in range(len(interest_rate)):
            for rate_ in range(len(inflation_rate)):
                data = {"rate_of_return":interest_rate[int_],"inflation_rate":inflation_rate[int_],
                        "current_age":30,"retirement_age":60,"life_expectancy":80}
                retire = RetirementCalculations(data)
                matrix_collector_[interest_rate[int_],inflation_rate[rate_]] = retire.retirement()
        print(matrix_collector_)

    def test_get_portfolio_trajectory(self):
        retire = RetirementCalculations()
        portfolio_trajectory = retire.get_portfolio_trajectory()