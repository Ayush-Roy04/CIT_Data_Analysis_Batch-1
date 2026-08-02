"""Student Management System:
Store details of multiple students using dictionaries and allow the user to:
Add a student
Update marks
Delete a student
Search by name"""

student = {}
def add_student():
    roll = int(input("Enter Roll Number: "))
    if roll in student:
        print("Student already exists.")
    else:
        name = input("Enter Name: ")
        marks = float(input("Enter Marks: "))
        student[roll] = {'name': name, 'marks': marks}
        print(f"Student {name} added successfully.")

def update_marks():
    roll = int(input("Enter Roll Number to update marks: "))
    if roll in student:
        marks = float(input("Enter new Marks: "))
        student[roll]['marks'] = marks
        print(f"Marks updated successfully for student {student[roll]['name']}.")
    else:
        print("Student not found.")

def delete_student():
    roll = int(input("Enter Roll Number to delete: "))
    if roll in student:
        name = student.pop(roll)    
        print(f"{name} has been successfully deleted")
    else:
        print("Student not found.")

def search_by_name():
    name = input("Enter Name to search: ")
    found = False
    for roll, info in student.items():
        if info['name'] == name:
            print(f"Roll Number: {roll}, Name: {info['name']}, Marks: {info['marks']}")
        else:
         print("Student not found.")

def display_students():
    if not student:
        print("No students in the system.")
    else:
        print("Student Details:")
        for roll, info in student.items():
            print(f"Roll Number: {roll}, Name: {info['name']}, Marks: {info['marks']}")

while True:
    print("\nStudent Management System")
    print("1. Add Student")
    print("2. Update Marks")
    print("3. Delete Student")
    print("4. Search by Name")
    print("5. Display All Students")
    print("6. Exit")

    choice = input("Enter your choice: ")
    
    if choice == '1':
        add_student()
    elif choice == '2':
        update_marks()
    elif choice == '3':
        delete_student()
    elif choice == '4':
        search_by_name()
    elif choice == '5':
        display_students()
    elif choice == '6':
        print("Exiting the system.")
        break
    else:
        print("Invalid choice. Please try again.")

