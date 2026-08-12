"""Sales Report
Monthly sales list.
Calculate 
Higest sales, lowest sales, average sales, and total sales."""

import numpy as np

n = int(input("Enter the number of months: "))
sales = np.array([float(input(f"Enter sales for month {i+1}: ")) for i in range(n)])
highest_sales = np.max(sales)
lowest_sales = np.min(sales)
average_sales = np.mean(sales)
total_sales = np.sum(sales)

print("Sales Report:")
print("Highest Sales:", highest_sales)
print("Lowest Sales:", lowest_sales)
print("Average Sales:", average_sales)
print("Total Sales:", total_sales)