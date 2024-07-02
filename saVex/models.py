from django.db import models

# Create your models here.


class ExpenseItems(models.Model):
    Rent = models.IntegerField(default=0)
    Maintenance = models.IntegerField(default=0)
    Electricity = models.IntegerField(default=0)
    netflix = models.IntegerField(default=0)
    youtube = models.IntegerField(default=0)
    amazon_prime = models.IntegerField(default=0)
    onedrive = models.IntegerField(default=0)
    Grocery = models.IntegerField(default=0)
    Misc = models.IntegerField(default=5000)
    date = models.DateField(auto_now_add=True)

    @property
    def total_expense(self):
        return self.Rent + self.Maintenance + self.Electricity + self.netflix + self.youtube + self.amazon_prime + self.onedrive + self.Misc

class EarningItems(models.Model):
    Salary = models.IntegerField(default=0)
    Bonus = models.IntegerField(default=0)
    Interest = models.IntegerField(default=0)
    PartTime = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    @property
    def total_earning(self):
        return self.Salary + self.Bonus + self.Interest + self.PartTime

class SavingsItems(models.Model):
    NPS = models.IntegerField(default=0)
    PF = models.IntegerField(default=0)
    LiquidFund = models.IntegerField(default=0)
    FixedDeposit = models.IntegerField(default=0)
    HouseDownPayment = models.IntegerField(default=0)

    @property
    # not including pf in current savings. this will be part of retirement solutions.
    def total_savings(self):
        return self.NPS + self.LiquidFund + self.FixedDeposit + self.HouseDownPayment

class InvestmentItems(models.Model):
    Stock = models.IntegerField(default=0)
    MutualFund = models.IntegerField(default=0)
    Gold = models.IntegerField(default=0)
    RealEstate = models.IntegerField(default=0)
    Crypto = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    @property
    def total_investment(self):
        return self.Stock + self.MutualFund + self.Gold + self.RealEstate + self.Crypto

class LiabilitiesItems(models.Model):
    PersonalLoan = models.IntegerField(default=0)
    CreditCard = models.IntegerField(default=0)
    MotherLoan = models.IntegerField(default=0)
    CreditLoan = models.IntegerField(default=0)
    MedicalInsurance = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    @property
    def total_liabilities(self):
        return self.PersonalLoan + self.CreditCard + self.CreditLoan + self.MotherLoan + self.MedicalInsurance


class AggregatedItems(models.Model):
    TotalExpense = models.IntegerField(default=0)
    TotalEarning = models.IntegerField(default=0)
    SavingPerMonth = models.IntegerField(default=0)
    TotalInvestment = models.IntegerField(default=0)
    TotalLiabilities = models.IntegerField(default=0)
    NetWorth = models.IntegerField(default=0)
    EmergencyFund = models.IntegerField(default=0)
    RetirementFund = models.IntegerField(default=0)
    HouseFund = models.IntegerField(default=0)
    ExpectedSavings_6months = models.IntegerField(default=0)
    Retirement_monthly_gap = models.IntegerField(default=0)
    Savings_gap = models.IntegerField(default=0)
    Home_downpayment_gap = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
