import os, pdb
from saVex.models import *
from django.db.models import Sum, Min
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from twilio.rest import Client
from datetime import datetime
# setup the twilio client
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_sms(client, body_):
    message = client.messages.create(
        body=body_,
        from_=os.environ["TWILIO_PHONE_NUMBER"],  # Your Twilio number
        to=os.environ["PERSONAL_NUMBER"]  # Your phone number
    )
    print(message.sid)

def send_whatsapp(client, body_):
    message = client.messages.create(
        body= body_,
        from_='whatsapp:'+ os.environ["TWILIO_PHONE_NUMBER"],  # Your Twilio number
        to='whatsapp:'+ os.environ["PERSONAL_NUMBER"]   # Your phone number
    )

    print(message.sid)

class Command(BaseCommand):
    help = 'calculate the AggregatedItems w.r.t grocery expense and notify the user if the total expense crosses the threshold.'

    def add_arguments(self, parser):
        parser.add_argument('amount_fixed_for_grocery', type=int, help='Amount fixed for grocery')

    def get_min_id(self, item_):
        """Get the smallest id of the model object for the current date.
        :param item_: model object
        :return: smallest id of the model object for the current month.
        """
        smallest_id = ExpenseItems.objects.filter(month=datetime.now().month).aggregate(Min('id'))
        id_ = smallest_id['id__min']
        return id_

    def handle(self, *args, **options):
        # Calculate total expense
        grocery_exp = ExpenseItems.objects.latest('date').Grocery
        total_grocery_expense = ExpenseItems.objects.aggregate(total=Sum('Grocery'))['total']
        print(total_grocery_expense)
        # write the logic for when to send the notification w.r.t threshold of 80%
        # the grocery amount is dynamic and can be changed by the user.
        # calculate the logic for expected amount of grocery to be spent on a monthly basis.
        # determine the fixed cost of expenses monthly basis
        min_id = self.get_min_id(ExpenseItems)
        item = ExpenseItems.objects.get(id=min_id)  # replace with your own criterion
        fixed_expense = item.total_expense
        print(fixed_expense)
        min_id = self.get_min_id(LiabilitiesItems)
        print(min_id)
        item = LiabilitiesItems.objects.get(id=min_id)
        current_liabilities = item.total_liabilities
        print(current_liabilities)
        min_id = self.get_min_id(SavingsItems)
        item = SavingsItems.objects.get(id=min_id)
        current_savings = item.total_savings
        print(current_savings)
        min_id = self.get_min_id(EarningItems)
        item = EarningItems.objects.get(id=min_id)
        total_earning = item.total_earning
        print(total_earning)
        # print(fixed_expense, current_liabilities,current_savings, total_earning)
        expected_amount_fixed_for_grocery = total_earning - (fixed_expense + current_liabilities + current_savings)
        amount_fixed_for_grocery = options.get('amount_fixed_for_grocery', 20000)
        # per day maximum expense for grocery capped,
        today = datetime.now().day
        last_date_of_month = 30
        number_of_days = last_date_of_month - today
        per_day_expense = (amount_fixed_for_grocery-total_grocery_expense)/ number_of_days

        if total_grocery_expense >= 0.8 * amount_fixed_for_grocery:
            # send notification
            body_ = """ Warning for Grocery Expense Update!!!
            IMMEDIATELY STOP THE GROCERY EXPENSES.
            IMMEDIATELY STOP THE GROCERY EXPENSES.
            IMMEDIATELY STOP THE GROCERY EXPENSES.
            ######################################
            ######################################
            Till now, the total grocery expense is {}.
            The expected amount for grocery this month is {}.
            The amount fixed for grocery is {}.
            Surplus amount which can be saved(expected_amt_grocery - amt_fixed_grcry) is {}.
            per_day_expense is {}.
            number_of_days left is {}.
            """.format(total_grocery_expense, expected_amount_fixed_for_grocery, 
                       amount_fixed_for_grocery, 
                       expected_amount_fixed_for_grocery - amount_fixed_for_grocery,
                       per_day_expense, number_of_days)

        else:
            # send notification
            body_ = """ Warning for Grocery Expense Update!!!
            Till now, the total grocery expense is {}.
            The expected amount for grocery this month is {}.
            The amount fixed for grocery is {}.
            Surplus amount which can be saved(expected_amt_grocery - amt_fixed_grcry) is {}.
            per_day_expense is {}.
            number_of_days left is {}.
            """.format(total_grocery_expense, expected_amount_fixed_for_grocery, 
                       amount_fixed_for_grocery, 
                       expected_amount_fixed_for_grocery - amount_fixed_for_grocery,
                       per_day_expense, number_of_days)
            #TODO upgrade twilio account for whats app messages, once the applicaiton is deployed on
            # either raspberry pi or on android phone.
            #send_whatsapp()
            print("Printing the passed argument for the grocery expense: ", amount_fixed_for_grocery)
            send_sms(client, body_)