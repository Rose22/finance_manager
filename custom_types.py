import config
import os
import pickle

class PaymentList(object):
    def __init__(self, name = "payment"):
        self.name     = name
        self.payments = []

    def get(self):
        return self.payments

    def get_total(self):
        """Get the total sum of money from all items in this list"""

        price = 0.0;
        for payment in self.payments:
            price += payment['price']

        return price

    def exists(self, index):
        """Check whether the given index exists in the list"""

        if (index > (len(self.payments)-1)):
            return False

        return True

    def add(self, price, category, name, day):
        """Add a payment"""

        self.payments.append({
            'price':    price,
            'category': category,
            'name':     name,
            'day':      day
        })

        return True
    def edit(self, index, price, category, name, day):
        """Edit a payment by index"""

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
        """Delete a payment from the list by index"""

        if (index > len(self.payments)):
            return False

        del self.payments[index]

        return True

    def display(self, key_name = "", key_query = ""):
        """Displays a formatted list of payments, and allows you to search any of the keys by a value (key_query)"""

        output = ""

        for index, payment in enumerate(self.payments):
            # Search
            if key_name:
                # Exact search for numbers
                if key_query.isdigit():
                    if key_query != str(payment[key_name]):
                        continue
                # Substring search for strings
                else:
                    if str(key_query).lower() not in str(payment[key_name]).lower():
                        continue

            # Formatted list item
            output += "{0:0>3d} | day {1:0>2d} | {2:<15} | {3:<40} | {4}{5:>05.2f}\n".format(index, payment['day'], payment['category'], payment['name'][0:40], config.currency, payment['price'])

        if not self.payments:
            output += "This list doesn't have anything in it yet.\n"

        output += "---\n"
        output += "Total: {0:>05.2f}\n".format(self.get_total())

        return output

    def __str__(self):
        """String representation of the PaymentList. Simply calls self.display()."""

        return self.display()


class FinanceData(object):
    """This class does the calculations for the money management part of the program"""

    def __init__(self, path):
        self.data = {
            "income":	0,
            "expenses":	 PaymentList('expenses'),
            "income":    PaymentList('income'),
            "payments":	 PaymentList('payments'),
            "+payments": PaymentList('+payments'),
            "leftover_prevmonth": 0
        }

        self.save_path = path;

        if os.path.exists(self.save_path):
            self.data = pickle.load(open(self.save_path, "rb"))
        else:
            with open(self.save_path, "w") as f:
                f.write(pickle.dumps(self.data))

    def save(self):
        """Saves to disk"""

        pickle.dump(self.data, open(self.save_path, "wb"))

    def set_leftovers(self, leftovers):
        """Sets the amount of money left over (not spent) from the previous month"""

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

    def get_payments(self, type_of_payment = "payment"):
        """Returns the PaymentList of the specified type"""
        if self.data[type_of_payment]:
            return self.data[type_of_payment]

    def get_payments_total(self, type_of_payment = "payment"):
        """Returns the total sum of a PaymentList."""

        if self.data[type_of_payment]:
            return self.data[type_of_payment].get_total()

    def get_money_left(self):
        """Calculates the current budget minus the total amount of money spent this month."""

        return self.get_budget()-self.get_payments_total("payments")

    def get_foresight(self):
        """Calculates the amount of money you would have if you were to spend nothing and move onto the next month"""

        return self.get_money_left()+self.get_pure_budget()

    def next_month(self):
        """Stores the money still left over from this month into the previous month leftovers, and then resets payments."""

        self.data['leftover_prevmonth'] = self.get_money_left()
        self.data['payments']  = PaymentList("payments")
        self.data['+payments'] = PaymentList("+payments")
