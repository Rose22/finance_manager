# -*- coding: utf-8 -*-
import os, sys, pickle

# TODO: Euro sign support
currency = ""

class financialManager:
	def __init__(self):
		self.data = {
			"income":	0,
			"expenses":	[],
			"payments":	[],
			"leftover_prevmonth": 0
		}

		if os.path.exists(os.path.expanduser("~/financialmanager_data.p")):
			self.data = pickle.load(open(os.path.expanduser("~/financialmanager_data.p"), "rb"))

	def save(self):
		pickle.dump(self.data, open(os.path.expanduser("~/financialmanager_data.p"), "wb"))
	def reset(self):
		"""Runs a prompt to allow the user to reset the internal data"""

		print "Reset payments? (y/N)",
		yesno = raw_input()
		if yesno.lower() == "y" or yesno.lower() == "yes":
			self.data['payments']			= []

		print "Reset income? (y/N)",
		yesno = raw_input()
		if yesno.lower() == "y" or yesno.lower() == "yes":
			self.data['income']				= 0

		print "Reset expenses? (y/N)",
		yesno = raw_input()
		if yesno.lower() == "y" or yesno.lower() == "yes":
			self.data['expenses']			= []
		
		self.save()

	def getLeftovers(self):
		"""Returns the money that was leftover (not spent) from the previous month"""

		return self.data['leftover_prevmonth']
	def getPureBudget(self):
		"""Calculates the income minus the monthly expenses, to form the budget (allowed money to spend in a month)"""

		return self.data['income']-self.getPaymentsMoney("expenses")
	def getBudget(self):
		"""Calculates the budget like getPureBudget(), except it also takes into account the leftover money from the previous month."""

		return (self.data['income']+self.data['leftover_prevmonth'])-self.getPaymentsMoney("expenses")
	def getIncome(self):
		"""Returns the set income"""

		return self.data['income']
	def getPaymentsMoney(self, typeOfPayment = ""):
		"""Returns the total amount of money spent this month."""

		paymentsMoney = 0
		for payment in self.data[typeOfPayment]:
			paymentsMoney += payment['money']

		return paymentsMoney
	def calculateMoneyLeft(self):
		"""Calculates the current budget minus the total amount of money spent this month."""

		return self.getBudget()-self.getPaymentsMoney("payments")

	def printTotal(self):
		print "Income: %s%.2f" % (currency, self.getIncome())
		print "Monthly Expenses: %s%.2f" % (currency, self.getPaymentsMoney("expenses"))
		print
		self.printBudget()
	def printBudget(self):
		print "Monthly allowed budget, based on income minus expenses: %s%.2f" % (currency, self.getPureBudget()) 
		print "Leftovers from previous month: %s%.2f" % (currency, self.getLeftovers())
		print "Resulting Budget: %s%.2f" % (currency, self.getBudget())
		print "Payments so far: %s%.2f" % (currency, self.getPaymentsMoney("payments"))
		print "Money left: %s%.2f" % (currency, self.calculateMoneyLeft())

	def askForIncome(self):
		"""Run a prompt that allows the user to set their income.""" 

		print "Currently set to: %s%.2f" % (currency, self.getIncome())
		print "What's your income?>",

		try:
			self.data['income'] = float(raw_input())
		except:
			print "Invalid input"
			return False

		self.save()
		print "Income set."
	def askForLeftovers(self):
		"""Allows the user to correct the calculated leftovers, in case something went wrong"""

		print "Currently set to: %s%.2f" % (currency, self.getLeftovers())
		print "What is your current leftover money from the previous months?>",

		try:
			self.data['leftover_prevmonth'] = float(raw_input())
		except:
			print "Invalid input"
			return False

		self.save()
		print "Leftovers set."

	def nextMonth(self):
		"""Stores the money still left over from this month into the previous month leftovers, and then resets payments."""

		self.data['leftover_prevmonth'] = self.calculateMoneyLeft()
		self.data['payments'] = []
		self.save()

		print "Stored leftover money into leftovers and emptied payment list."
		print "Moved on to next month"
	def printForesight(self):
		print "Predicted amount of money next month: %s%.2f" % (currency, self.calculateMoneyLeft()+self.getPureBudget())
		
	def addPayment(self, typeOfPayment = "", askString = ""):
		print "%s>" % askString,
		biller = raw_input()
		print "How much money?>",
		payment = raw_input()

		try:
			payment = float(payment)
		except:
			print "Invalid input"
			return False

		self.data[typeOfPayment].append({"biller": biller, "money": payment})
		self.save()

		print "Payment added."
	def editPayment(self, typeOfPayment = ""):
		self.printPayments(typeOfPayment)

		print
		print "Which one do you want to edit?>",
		index = raw_input()

		try:
			index = int(index)
		except:
			print "Invalid input"
			return False

		print
		print "%s." % self.data[typeOfPayment][index]['biller']
		print "How much money?>",
		payment = raw_input()

		try:
			payment = float(payment)
		except:
			print "Invalid input"
			return False

		try:
			self.data[typeOfPayment][index]['money'] = payment
			self.save()
		except:
			print "That payment does not exist."
			return False

		print "Payment modified."
	def removePayment(self, typeOfPayment = ""):
		self.printPayments(typeOfPayment)

		print
		print "Which one do you want to remove?>",
		index = raw_input()

		try:
			index = int(index)
		except:
			print "Invalid input"
			return False

		try:
			print "%s? (y/N)>" % self.data[typeOfPayment][index]['biller'],
			yesno = raw_input().lower()

			if yesno == "y" or yesno == "yes":
				del self.data[typeOfPayment][index]
				self.save()
			else:
				print "Payment not removed."
				return False
		except:
			print "That payment does not exist."
			return False

		print "Payment removed."

	def printPayments(self, typeOfPayment = ""):
		if not self.data[typeOfPayment]:
			print "No %s have been added yet." % typeOfPayment

		indexCounter = 0
		for expense in self.data[typeOfPayment]:
			print "%i | %s: %s%.2f" % (indexCounter, expense['biller'], currency, expense['money'])
			indexCounter += 1

		print "Total %s: %s%.2f" % (typeOfPayment, currency, self.getPaymentsMoney(typeOfPayment))

if __name__ == "__main__":
	helpstr = """Simply set your income, then add your monthly expenses/bills. You can do this every month, or only once if your expenses are the same every month.

	The program then calculates a budget. This is the money you have left over after all the bills are paid..
	The budget represents the amount of money you REALLY have - I.E. that you can spend on fun stuff and on groceries.

	The program tracks how much money you have left at the end of each month. When you move onto the next month,
	the program will add the money you had left in the previous month, to the budget in your current month.
	This additional budget is called "leftovers" within the manager.
	That way, if you save well, your budget will grow :)

	Add and remove payments to keep track of how much money you still have left :)

	setincome: Set your income
	setleftovers: Set your leftovers to a manual value in case you need to correct it
	ae: Add Expense | ee: Edit Expense | re: Remove Expense
	ap: Add Payment | ep: Edit Payment | rp: Remove Payment
	---
	expenses: Shows your monthly expenses
	payments: Shows your payments
	total: Shows your income and budget
	budget: Shows your current budget and money left
	details: Shows income, budget, money left, and an overview of all expenses and payments
	foresight: Shows how much money you would have next month, if you were to not buy anything anymore this month.
	nextmonth: Moves the manager onto the next month, which means it stores your leftover money from this month, which gets added to your budget.
	reset: Resets the lists of your choosing, such as expenses and payments (it's recommended to reset payments every month)
	exit: Quits the program"""

	# Allows you to execute any of the commands by supplying the command as an argument on the command line
	singleCmd = False
	if len(sys.argv) >= 2:
			singleCmd = True

	if not singleCmd:
		print "Financial Manager by Rose"
		print "Type 'help' for help."
		print
		print "Quick reminder: expenses, payments, total, budget, details, nextmonth, foresight, reset, exit"
		print

	finman = financialManager()

	while True:
		if singleCmd:
			cmd = sys.argv[1]
		else:
			print "Manager>",
			cmd = raw_input().lower()

		if cmd == "total":
			finman.printTotal()
		elif cmd == "budget":
			print "budget: %s%.2f (prev month: %s%.2f), payments: %s%.2f, money left: %s%.2f" % (currency, finman.getBudget(), currency, finman.getLeftovers(), currency, finman.getPaymentsMoney("payments"), currency, finman.calculateMoneyLeft())
		elif cmd == "details":
			print

			finman.printTotal()

			print "---"

			print "Monthly Expenses:"
			finman.printPayments("expenses")

			print

			print "Payments:"
			finman.printPayments("payments")

			print "---"

			print "Money left: %s%.2f" % (currency, finman.calculateMoneyLeft())
		elif cmd == "setincome":
			finman.askForIncome()
		elif cmd == "setleftovers":
			finman.askForLeftovers()
		elif cmd == "ae" or cmd == "addexpense":
			finman.addPayment("expenses", "Who bills the monthly expense?")
		elif cmd == "ee" or cmd == "editexpense":
			finman.editPayment("expenses")
		elif cmd == "re" or cmd == "removeexpense":
			finman.removePayment()
		elif cmd == "expenses":
			finman.printPayments("expenses")
		elif cmd == "ap" or cmd == "addpayment":
			finman.addPayment("payments", "What did you buy?")
		elif cmd == "ep" or cmd == "editpayment":
			finman.editPayment("payments")
		elif cmd == "rp" or cmd == "removepayment":
			finman.removePayment("payments")
		elif cmd == "payments":
			finman.printPayments("payments")
		elif cmd == "nextmonth":
			finman.nextMonth()
		elif cmd == "foresight":
			finman.printForesight()
		elif cmd == "reset":
			finman.reset()
		elif cmd == "h" or cmd == "help":
			print helpstr
		elif cmd == "exit" or cmd == "quit" or cmd == "q":
			break
		else:
			print "Unknown command. Type 'help' for help."

		if singleCmd:
			exit(0)

		print