"""Library Management System
use: function, list and dictionary
features: issue book, return book, view all books, search book, display available books."""

from turtle import title


books = [{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "available": True},
          {"title": "To Kill a Mockingbird", "author": "Harper Lee", "available": True},
          {"title": "1984", "author": "George Orwell", "available": True}]

def issue_book():
    title = input("Enter book title to issue: ")

    for book in books:
        if book["title"].lower() == title.lower():
            if book["available"]:
                book["available"] = False
                print("Book issued successfully!")
            else:
                print("Book is already issued.")
            return

    print("Book not found.")


def return_book():
    title = input("Enter book title to return: ")

    for book in books:
        if book["title"].lower() == title.lower():
            if not book["available"]:
                book["available"] = True
                print("Book returned successfully!")
            else:
                print("This book was not issued.")
            return

    print("Book not found.")    

def view_all_books():
    print("\n ALL BOOKS IN THE LIBRARY")

    for book in books:
        status = "Available" if book["available"] else "Issued"

        print("Title :", book["title"])
        print("Author:", book["author"])
        print("Status:", status)
        print("-----------------------------")

def search_book():
    title = input("Enter book title to search: ")

    for book in books:
        if book["title"].lower() == title.lower():
            print("\nBook Found!")
            print("Title :", book["title"])
            print("Author:", book["author"])
            print("Status:", "Available" if book["available"] else "Issued")
            return

    print("Book not found.")

def available_books():
    print("\n====== AVAILABLE BOOKS ======")

    found = False

    for book in books:
        if book["available"]:
            print(book["title"], "-", book["author"])
            found = True

    if not found:
        print("No books are currently available.")

while True:

    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Issue Book")
    print("2. Return Book")
    print("3. View All Books")
    print("4. Search Book")
    print("5. Display Available Books")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        issue_book()

    elif choice == "2":
        return_book()

    elif choice == "3":
        view_all_books()

    elif choice == "4":
        search_book()

    elif choice == "5":
        available_books()

    elif choice == "6":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")