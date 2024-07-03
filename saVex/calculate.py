from .models import AggregatedItems, SavingsItems, EarningItems
from datetime import datetime


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
        self.annual_interest_rate = kwargs.get('annual_interest_rate', 0.05)
        # if salary input is not provided, fetch from models
        item = EarningItems.objects.get(id=1)
        self.current_income = kwargs.get('current_income', item.Salary)
        

    def future_value(PV, r, n, t):
        """
        Calculate the future value of an amount.

        Parameters:
        PV (float): The present value (the initial amount of money).
        r (float): The annual interest rate (in decimal).
        n (int): The number of times that interest is compounded per year.
        t (int): The time the money is invested for in years.

        Returns:
        float: The future value of the amount.
        """
        FV = PV * (1 + r/n)**(n*t)
        return FV

    def pmt(interest_rate, periods, present_value, future_value=0, when='end'):
        """
        Calculate the payment against loan principal plus interest.

        Parameters:
        interest_rate (float): The interest rate (as a decimal, e.g., 0.05 for 5%).
        periods (int): The number of periods (e.g., number of payments).
        present_value (float): The total amount that a series of future payments is worth now.
        future_value (float, optional): The future value remaining after the last payment has been made. Default is 0.
        when (str, optional): When payments are due ('beginning' or 'end'). Default is 'end'.

        Returns:
        float: The (fixed) periodic payment.
        """
        if when == 'beginning':
            adjust = (1 + interest_rate)
        else:
            adjust = 1

        pmt = - (future_value + present_value * (1 + interest_rate)**periods) / ((1 + interest_rate * (when == 'beginning')) * ((1 + interest_rate)**periods - 1))

        return pmt * adjust

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
        retirement_life_corpus_years_left = self.life_expectancy - self.retirement_age
        #FV of currently monthly Income minus total_liabilities_per_month
        current_liability = AggregatedItems.total_liabilities()
        current_monthly_income = self.current_income / 12
        future_value_of_current_income = self.future_value(current_monthly_income, self.annual_interest_rate, 12, no_terms_left)
        future_value_of_current_liability = self.future_value(current_liability, self.annual_interest_rate, 12, no_terms_left)
        # TODO calculate realistic Life Expectancy.
        retirement_fund = (future_value_of_current_income - future_value_of_current_liability) * retirement_life_corpus_years_left * 12
        monthly_retirment_fund = self.pmt(self.annual_interest_rate, no_terms_left, 0, retirement_fund)
        return monthly_retirment_fund

    def Retirement_monthly_gap(self):
        """
        Calculate the retirement monthly gap.

        Returns:
        float: The retirement monthly gap.
        """
        # Calcualate the retirment monthly fund with new inputs.

        
        retirement_monthly_gap = self.retirement() - SavingsItems.NPS
        return retirement_monthly_gap
    
    
        


