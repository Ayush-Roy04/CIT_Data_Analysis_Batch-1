#Student Records: Store student records using tuples and print students whose marks are greater than 80.
students = [
    ("Aysuh", 85),
    ("Rahul", 75),
    ("Rishita", 90),
    ("Priya", 56),
    ("Sayan", 67),
    ("Vishal", 82),
    ("Aritra", 80)
]

for name, marks in students:
    if marks > 80:
        print(f"{name}: {marks}")
