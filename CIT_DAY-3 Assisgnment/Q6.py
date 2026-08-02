def numbers(a,b):
    add = a + b
    sub = a - b
    multiply = a * b    
    divide = a / b if b != 0 else None
    return add, sub, multiply, divide
print(numbers(10, 5))