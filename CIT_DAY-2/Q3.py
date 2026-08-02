"""Find
Sum
Difference
Product
Division
of two numbers."""

a = int(input("Enter 1st Number: "))
b = int(input("Enter 2st Number: "))

sum = a + b
diff = a - b

product = a * b
if (a or b != 0):
    div = a/b
else:
    div = "Undefined"

print(sum)
print(diff)
print(product)
print(div)
