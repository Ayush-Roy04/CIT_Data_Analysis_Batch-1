"""Employee Salary Slip
Store the following details:
Employee Name
Employee ID
Basic Salary
Calculate:
HRA = 20% of Basic Salary
DA = 15% of Basic Salary
PF = 12% of Basic Salary
Gross Salary
Net Salary
Print a professional salary slip."""

emp_name = input("Enter Employee Name: ")
emp_id = input("Enter Employee ID: ")
basic_salary = float(input("Enter Basic Salary: "))

HRA = 0.20 * basic_salary
DA = 0.15 * basic_salary
PF = 0.12 * basic_salary
Gross_Salary = basic_salary + HRA + DA
Net_Salary = Gross_Salary - PF

print("\n--- Salary Slip ---")
print(f"Employee Name: {emp_name}")
print(f"Employee ID: {emp_id}")
print(f"Basic Salary: {basic_salary}")
print(f"HRA: {HRA}")
print(f"DA: {DA}")
print(f"PF: {PF}")
print(f"Gross Salary: {Gross_Salary}")
print(f"Net Salary: {Net_Salary}")