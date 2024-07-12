from rest_framework import serializers

class MonthlyRetirementPayload(serializers.Serializer):
    retirement_age = serializers.IntegerField(required=True)
    birth_date = serializers.DateField(required=True)
    life_expectancy = serializers.IntegerField(required=True)
    annual_interest_rate = serializers.FloatField(required=False)
    current_income = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=False)
    inflation_rate = serializers.FloatField(required=True)
    retirement_recurring = serializers.IntegerField(required=True)
    rate_of_return = serializers.FloatField(required=False)

class GetPortfolioPayload(serializers.Serializer):
    retirement_age = serializers.IntegerField(required=True)
    birth_date = serializers.DateField(required=True)
    life_expectancy = serializers.IntegerField(required=True)
    current_income = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=False)
    retirement_recurring = serializers.IntegerField(required=True)
    rate_of_return = serializers.FloatField(required=False)