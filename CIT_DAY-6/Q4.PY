"""Grocery Billing system
use: function, list and dictionary 
Features: Add items, Calculate total, apply discount, generate receipt ."""

# Grocery Billing System

items = []   # List to store purchased items

# Function to add items
def add_item():
    name = input("Enter item name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))

    item = { 
        "name": name,
        "price": price,
        "quantity": quantity
    }

    items.append(item)
    print("Item added successfully!\n")


# Function to calculate total
def calculate_total():
    total = 0

    for item in items:
        total += item["price"] * item["quantity"]

    return total


# Function to apply discount
def apply_discount(total):
    if total >= 1000:
        discount = total * 0.10
    elif total >= 500:
        discount = total * 0.05
    else:
        discount = 0

    return discount


# Function to generate receipt
def generate_receipt():
    total = calculate_total()
    discount = apply_discount(total)
    final_amount = total - discount

    print("\n========== GROCERY RECEIPT ==========")

    for item in items:
        amount = item["price"] * item["quantity"]

        print(item["name"],
              "x", item["quantity"],
              "=", amount)

    print("-------------------------------------")
    print("Total     :", total)
    print("Discount  :", discount)
    print("Final Bill:", final_amount)
    print("=====================================")


# Main program
while True:
    print("\n1. Add Item")
    print("2. Generate Receipt")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_item()

    elif choice == "2":
        if len(items) == 0:
            print("No items added!")
        else:
            generate_receipt()

    elif choice == "3":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")