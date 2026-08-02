"""Restaurant Bill Calculator
Store:
Customer Name
Food Bill
GST = 5%
Service Charge = 10%
Calculate the final payable amount."""

customer_name = input("Enter Customer Name: ")
food_bill = float(input("Enter Food Bill Amount: "))
gst = 0.05 * food_bill
service_charge = 0.10 * food_bill
final_amount = food_bill + gst + service_charge

print(f"Customer Name: {customer_name}")
print(f"Food Bill: {food_bill}")
print(f"GST (5%): {gst}")
print(f"Service Charge (10%): {service_charge}")
print(f"Final Amount: {final_amount}")