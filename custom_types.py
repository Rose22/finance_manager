import config
import os
import yaml

class PaymentList(object):
    """A list of payments, with functionalities to add, edit, filter, delete, and show a nicely formatted version"""

    def __init__(self, name = "payment"):
        self.name     = name
        self._list    = []

    def load(self, payment_list):
        self._list = payment_list
        return self._list

    def get(self):
        return self._list

    def get_total(self):
        """Get the total sum of money from all items in this list"""

        price = 0.0;
        for payment in self._list:
            price += payment['price']

        return price

    def exists(self, index):
        """Check whether the given index exists in the list"""

        if (index > (len(self._list)-1)):
            return False

        return True

    def add(self, price, category, name, day):
        """Add a payment"""

        self._list.append({
            'price':    price,
            'category': category,
            'name':     name,
            'day':      day
        })

        return True
    def edit(self, index, price, category, name, day):
        """Edit a payment by index"""

        if (index > len(self._list)):
            return False

        self._list[index] = {
            'price':    price,
            'category': category,
            'name':     name,
            'day':      day
        }

        return True
    def delete(self, index):
        """Delete a payment from the list by index"""

        if (index > len(self._list)):
            return False

        del self._list[index]

        return True

    def display(self, key_name = "", key_query = ""):
        """Displays a formatted list of payments, and allows you to search any of the keys by a value (key_query)"""

        output = ""

        for index, payment in enumerate(self._list):
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
            output += "{0:0>3d} | day {1:0>2d} | {2:<15} | {3:<40} | {4}{5:>05.2f}\n".format(index, payment['day'], payment['category'][0:15], payment['name'][0:40], config.currency, payment['price'])

        if not self._list:
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
        # Stores copies of the PaymentList instances
        self.payment_lists = {
            "expenses":	 PaymentList('expenses'),
            "income":    PaymentList('income'),
            "payments":	 PaymentList('payments'),
            "+payments": PaymentList('+payments'),
        }

        # Miscellaneous data
        self.data = {
            "leftover_prevmonth": 0
        }

        # For loading the data
        buffer = {
            "expenses":	            [],
            "income":               [],
            "payments":	            [],
            "+payments":            [],
            "leftover_prevmonth":   0
        }

        self.save_path = os.path.expanduser(path)

        # Load the data from our YAML file into the buffer
        if os.path.exists(self.save_path):
            buffer = yaml.safe_load(open(self.save_path, "rb"))
        else:
            with open(self.save_path, "w") as f:
                f.write(yaml.safe_dump(buffer))

        # Load the respective lists from the buffer into our PaymentList instances
        for payment_list in self.payment_lists.values():
            payment_list.load(buffer[payment_list.name])

        # Load miscellaneous data
        self.data['leftover_prevmonth'] = buffer['leftover_prevmonth']

    def save(self):
        """Saves to disk"""

        # Create a buffer for saving into the file
        buffer = {
            "expenses":             self.get_payments("expenses").get(),
            "income":               self.get_payments("income").get(),
            "payments":             self.get_payments("payments").get(),
            "+payments":            self.get_payments("+payments").get(),
            "leftover_prevmonth":   self.get_leftovers()
        }

        # And write it to disk in YAML format
        with open(self.save_path, "w") as f:
            f.write(yaml.safe_dump(buffer))

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
        if self.payment_lists[type_of_payment]:
            return self.payment_lists[type_of_payment]

    def get_payments_total(self, type_of_payment = "payment"):
        """Returns the total sum of a PaymentList."""

        if self.payment_lists[type_of_payment]:
            return self.payment_lists[type_of_payment].get_total()

    def get_money_left(self):
        """Calculates the current budget minus the total amount of money spent this month."""

        return self.get_budget()-self.get_payments_total("payments")

    def get_foresight(self):
        """Calculates the amount of money you would have if you were to spend nothing and move onto the next month"""

        return self.get_money_left()+self.get_pure_budget()

    def next_month(self):
        """Stores the money still left over from this month into the previous month leftovers, and then resets payments."""

        self.data['leftover_prevmonth'] = self.get_money_left()
        self.payment_lists['payments']  = PaymentList("payments")
        self.payment_lists['+payments'] = PaymentList("+payments")
