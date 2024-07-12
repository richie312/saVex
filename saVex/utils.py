from .models import LiabilitiesItems, SavingsItems, EarningItems
from datetime import datetime
from django.db.models import Sum, Min
import numpy_financial as npf

def get_min_id(item_):
    """Get the smallest id of the model object for the current date.
    :param item_: model object
    :return: smallest id of the model object for the current month.
    """
    smallest_id = item_.objects.filter(month=datetime.now().month).aggregate(Min('id'))
    if smallest_id['id__min'] is None:
        id_ = 1
    else:
        id_ = smallest_id['id__min']
    return id_

class RetirementCalculations:
    """
    A class to calculate the retirement corpus and monthly gap.
    """
    def __init__(self,**kwargs):
        self.retirement_age = kwargs.get('retirement_age', 65)
        self.birth_year = kwargs.get('birth_year', 1985)
        self.current_age = kwargs.get('current_age', datetime.now().year - self.birth_year)
        self.number_of_years_left = self.retirement_age - self.current_age
        self.current_month = datetime.now().month
        self.life_expectancy = kwargs.get('life_expectancy', 85)
        self.rate_of_return = kwargs.get('rate_of_return', 0.10)
        # this annual rate of interest should be atleast 10 to 15% to beat inflation.
        self.annual_inflation_rate = kwargs.get('annual_interest_rate', 0.06)
        # if salary input is not provided, fetch from models
        min_id = get_min_id(EarningItems)
        item = EarningItems.objects.get(id=min_id)
        self.current_income = kwargs.get('current_income', item.Salary)
        self.retirement_recurring = kwargs.get('retirement_recurring', 20000)

    def retirement(self):
        
        """
        Calculate the amount of money you'll have when you retire.

        :Parameters:
        :param current_income (float): Your current annual income. Default will be fetch from models.
        :param savings_rate (float): The percentage of your income that you save each year, as a decimal (e.g., 0.1 for 10%).
        :param years_until_retirement (int): The number of years until you plan to retire.
        :param annual_interest_rate (float): The annual interest rate of your savings, as a decimal (e.g., 0.05 for 5%).

        Returns:
        float: The amount of money you'll have when you retire.
        """
        
        no_terms_left_this_year = 12 - self.current_month
        no_terms_left = self.number_of_years_left * 12 + no_terms_left_this_year
        #FV of currently monthly Income minus total_liabilities_per_month
        min_id = get_min_id(LiabilitiesItems)    
        item = LiabilitiesItems.objects.get(id=min_id)
        current_liability = item.total_liabilities
        current_monthly_income = self.current_income
        # Assuming these credits are paid off by the time of retirement.
        net_income = current_monthly_income - current_liability
        # retirement investment period
        reitrement_investment_period = self.retirement_age - self.current_age
        # get the retirement aamount immediately after retirement.
        future_value_of_current_income = npf.fv(self.annual_inflation_rate,reitrement_investment_period,0,net_income)
        # Adjust the rate of return for inflation.
        adjusted_rate_return = ((1+self.rate_of_return)/(1+self.annual_inflation_rate)) - 1
        #retirement period
        reitrement_period = self.life_expectancy - self.retirement_age
        # reitrement fund should be the ideal corpus to beat the inflation and stay at same valuation.
        retirment_corpus = npf.pv(adjusted_rate_return, reitrement_period, future_value_of_current_income,0,when='begin')
        # Savings required per month to achieve the retirement fund.
        monthly_retirment_fund = npf.pmt(rate=self.rate_of_return/12,nper = no_terms_left, pv=retirment_corpus)
        return abs(int(str(round(monthly_retirment_fund))))

    def Retirement_monthly_gap(self):
        """
        Calculate the retirement monthly gap.

        Returns:
        float: The retirement monthly gap.
        """
        # Calcualate the retirment monthly fund with new inputs.

        min_id = get_min_id(SavingsItems)
        item = SavingsItems.objects.get(id=min_id)
        retirement_monthly_gap = self.retirement() - item.NPS
        return retirement_monthly_gap
    
    def get_portfolio_trajectory(self):
        """
        Calculate the portfolio trajectory.

        Returns:
        float: The portfolio trajectory.
        """
        keys_ = ["age","year", "rate_of_return", "inflation_rate","inv_begin","inv_end",
                    "net_gain", "inflation_adj_rate", "real_growth"]
        birth_year = self.birth_year
        current_year = datetime.today().year
        future_year = current_year + (self.retirement_age - self.current_age)
        years = range(current_year, future_year+1)
        year = [year_ for year_ in years]
        age = [year - birth_year for year in years]
        rate_of_return = [0.10 for i in range(len(years))]
        inflation_rate = [0.06 for i in range(len(years))]
        # calculate the cash flow of investment at the start and end of year respectively,
        inv_begin = []
        inv_end = []
        net_gain = []
        adj_income = self.retirement_recurring
        real_adj_income = self.retirement_recurring
        real_growth = []
        real_income_end = []
        inflation_adj_rate = [round(((1+rate_of_return[i])/(1+inflation_rate[i])) - 1,2) for i in range(len(years))]
        for i in range(len(years)):
            inv_begin.append(round(adj_income,2))
            adj_income += round(rate_of_return[i]*adj_income,2)
            # adj_income += rate_of_return[i]*current_income + inv_end[i-1]

            inv_end.append(round(adj_income+inv_end[i-1],2) if i > 0 else adj_income)
            # calculate the net gain of the investment
            net_gain.append(inv_end[i] - inv_begin[i])
            real_adj_income += inflation_adj_rate[i]*self.retirement_recurring + self.retirement_recurring if i >0 else inflation_adj_rate[i]*self.retirement_recurring
            real_income_end.append(round(real_adj_income+ real_income_end[i-1],2) if i > 0 else real_adj_income)
            real_growth.append(round(real_income_end[i] - real_income_end[i-1], 2)if i > 0 else real_income_end[i])
        #prepare the json output
        values_ = zip(age, year, rate_of_return, inflation_rate, inv_begin, inv_end, net_gain, inflation_adj_rate, real_growth)
        col_heads = []
        for key in keys_:
            col_heads.append(key)
        data_ = []
        for j, value in enumerate(values_):
            temp = {}
            for i in range(len(col_heads)):
                temp[col_heads[i]] = value[i]
            data_.append(temp)
        return data_
        

        