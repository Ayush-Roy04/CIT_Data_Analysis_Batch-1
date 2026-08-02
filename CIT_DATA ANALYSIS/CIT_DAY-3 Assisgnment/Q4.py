#Even or Odd Write a function that accepts a number and returns whether it is Even or Odd.
def number(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"
    
print(number(10))
print(number(15))