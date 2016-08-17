import os
import imp
import pickle

imp.load_source("config", "finance.conf")
import config

class PaymentsList(object):
    def __init__(self, name = "payment"):
        self.name     = name
        self.payments = []

    def get(self):
        return self.payments

    def get_total(self):
        price = 0.0;
        for payment in self.payments:
            price += payment['price']

        return price

    def exists(self, index):
        if (index > (len(self.payments)-1)):
            return False

        return True

    def add(self, price, category, name, day):
        self.payments.append({
            'price':    price,
            'category': category,
            'name':     name,
            'day':      day
        })

        return True
    def edit(self, index, price, category, name, day):
        if (index > len(self.payments)):
            return False

        self.payments[index] = {
            'price':    price,
            'category': category,
            'name':     name,
            'day':      day
        }

        return True
    def delete(self, index):
        if (index > len(self.payments)):
            return False

        del self.payments[index]

        return True

    def display(self, key_name = "", key_query = ""):
        output = ""

        for index, payment in enumerate(self.payments):
            if key_name:
                if key_query.isdigit():
                    if key_query != str(payment[key_name]):
                        continue
                else:
                    if str(key_query).lower() not in str(payment[key_name]).lower():
                        continue

            output += "{0:0>3d} | day {1:0>2d} | {2:<15} | {3:<40} | {4}{5:>05.2f}\n".format(index, payment['day'], payment['category'], payment['name'][0:40], config.currency, payment['price'])

        if not self.payments:
            output += "This list doesn't have anything in it yet.\n"

        output += "---\n"
        output += "Total: {0:>05.2f}\n".format(self.get_total())

        return output

    def __str__(self):
        return self.display()


class FinanceData(object):
    # TODO: Add the ability to create a "payment" that adds price instead of subtracting

    def __init__(self, path):
        self.data = {
            "income":	0,
            "expenses":	 PaymentsList('expenses'),
            "income":    PaymentsList('income'),
            "payments":	 PaymentsList('payments'),
            "+payments": PaymentsList('+payments'),
            "leftover_prevmonth": 0
        }

        self.save_path = path;

        if os.path.exists(self.save_path):
            self.data = pickle.load(open(self.save_path, "rb"))
        else:
            with open(self.save_path, "w") as f:
                f.write(pickle.dumps(self.data))

    def save(self):
        pickle.dump(self.data, open(self.save_path, "wb"))

    def set_leftovers(self, leftovers):
        self.data['leftover_prevmonth'] = leftovers
        self.save()
    def get_leftovers(self):
        """Returns the money that was leftover (not spent) from the previous month"""

        return self.data['leftover_prevmonth']

    def get_pure_budget(self):
        """Calculates the income minus the monthly expenses, to form the budget (allowed money to spend in a month)"""

        return self.get_payments_total("income")-self.get_payments_total("expenses")
    def get_budget(self):
        """Calculates the budget like getPureBudget(), except it also takes into account the other factors."""

        return (self.get_payments_total("income")+self.data['leftover_prevmonth']+self.get_payments_total("+payments"))-self.get_payments_total("expenses")

    def get_payments(self, type_of_payment):
        if self.data[type_of_payment]:
            return self.data[type_of_payment]

    def get_payments_total(self, type_of_payment = ""):
        """Returns the total amount of money spent this month."""

        if self.data[type_of_payment]:
            return self.data[type_of_payment].get_total()

    def get_money_left(self):
        """Calculates the current budget minus the total amount of money spent this month."""

        return self.get_budget()-self.get_payments_total("payments")

    def get_foresight(self):
        return self.get_money_left()+self.get_pure_budget()

    def next_month(self):
        """Stores the money still left over from this month into the previous month leftovers, and then resets payments."""

        self.data['leftover_prevmonth'] = self.get_money_left()
        self.data['payments'] = PaymentsList("payments")
