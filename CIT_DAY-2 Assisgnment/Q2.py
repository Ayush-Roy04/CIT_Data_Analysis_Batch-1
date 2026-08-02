"""Shopping bill generator 
store:
customer name
Product name
Quantity
Price per item
Calculate:
subtotal
GST (18%)
Final Amount
print the invoice"""

customer_name = input("Enter Customer Name: ")
product_name = input("Enter Product Name: ")
quantity = int(input("Enter Quantity: "))
price_per_item = float(input("Enter Price per item: "))

subtotal = quantity * price_per_item
gst = subtotal * 0.18
final_amount = subtotal + gst

print("\n--- Invoice ---")
print("Customer Name:", customer_name)
print("Product Name:", product_name)
print("Quantity:", quantity)
print("Price per item:", price_per_item)
print("Subtotal:", subtotal)
print("GST (18%):", gst)
print("Final Amount:", final_amount)
