"""Electricity Bill
store:
customer name
unit consumed
cost per unit
Calculate:
total bill
electricity tax(8%)
final bill"""

customer_name = input("Enter Customer Name: ")
unit_consumed = float(input("Enter Units Consumed: "))
cost_per_unit = float(input("Enter Cost per Unit: "))
total_bill = unit_consumed * cost_per_unit
electricity_tax = total_bill * 0.08
final_bill = total_bill + electricity_tax

print(f"Customer Name: {customer_name}")
print(f"Units Consumed: {unit_consumed}")
print(f"Cost per Unit: {cost_per_unit}")
print(f"Total Bill: {total_bill}")
print(f"Electricity Tax (8%): {electricity_tax}")
print(f"Final Bill: {final_bill}")
