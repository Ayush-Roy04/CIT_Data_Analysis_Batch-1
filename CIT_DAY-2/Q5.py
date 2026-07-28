"""1. Student Marksheet
Create variables for:
Student Name
Roll Number
Physics
Chemistry
Mathematics
Calculate:
Total Marks
Average Marks
Print the report using an f-string."""

name = input("Enter your name: ").strip()
rollno = int(input("Enter Roll no.: "))
physics = float(input("Enter marks of Physics: "))
chemistry = float(input("Enter marks of Chemistry: "))
math = float(input("Enter marks of Math: "))

total = physics + chemistry + math
avg = total / 3

print(f"Name: {name}\nRoll no.: {rollno}\nTotal: {total}\nAverage: {avg:.2f}")