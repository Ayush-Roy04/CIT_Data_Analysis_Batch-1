#Second largest: Find the second largest number in a list of numbers.
def second_largest(numbers):
    unique_numbers = list(set(numbers))
    sorted_numbers = sorted(unique_numbers)
    if len(sorted_numbers) < 2:
        return "LIST IS SHORT"
    else:
        return sorted_numbers[-2]
numbers = [5, 10, 3, 8, 15, 20]
print (second_largest(numbers))