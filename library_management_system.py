import json

# Define a Book class to represent individual books with attributes like title, author, ISBN, and quantity.
class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity

    def __repr__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}"

# Define a Library class to manage a collection of books. It has methods to add, update, remove, list books, load books from file, and save books to file.
class Library:
    def __init__(self, filepath):
        self.books = []  # Initialize an empty list to store books
        self.filepath = filepath  # Store the file path where book data will be saved

        # Load existing books from file (if any) when creating a Library object
        self.load_books()

    # Method to add a new book to the library
    def add_book(self, book):
        self.books.append(book)  # Add the book to the list
        self.save_books()  # Save the updated list of books to file

    # Method to update information about an existing book
    def update_book(self, isbn, title=None, author=None, quantity=None):
        for book in self.books:
            if book.isbn == isbn:  # Search for the book by ISBN
                # Update the book attributes if provided
                if title:
                    book.title = title
                if author:
                    book.author = author
                if quantity is not None:
                    book.quantity = quantity
                self.save_books()  # Save the updated list of books to file
                return True
        return False

    # Method to remove a book from the library
    def remove_book(self, isbn):
        for i, book in enumerate(self.books):
            if book.isbn == isbn:  # Search for the book by ISBN
                del self.books[i]  # Remove the book from the list
                self.save_books()  # Save the updated list of books to file
                return True
        return False

    # Method to list all books in the library
    def list_books(self):
        for book in self.books:
            print(book)

    # Method to load books from file when the library is initialized
    def load_books(self):
        try:
            with open(self.filepath, 'r') as file:
                books_data = json.load(file)  # Load JSON data from file
                self.books = [Book(**book) for book in books_data]  # Convert JSON data to Book objects
        except FileNotFoundError:
            print("Books file not found. Starting with an empty library.")
        except json.JSONDecodeError:
            print("Error reading the books file. Data might be corrupted.")

    # Method to save the current list of books to file
    def save_books(self):
        with open(self.filepath, 'w') as file:
            json.dump([book.__dict__ for book in self.books], file)  # Convert Book objects to JSON and write to file

# Main function to interact with the library management system
def main():
    library = Library('books.json')  # Create a Library object with file path 'books.json'

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. List Books")
        print("5. Exit")
        choice = input("Enter your choice: ")  # Prompt user for choice

        # Perform actions based on user's choice
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity: "))
            library.add_book(Book(title, author, isbn, quantity))  # Add a new book
        elif choice == '2':
            isbn = input("Enter ISBN of the book to update: ")
            title = input("Enter new title (leave blank to skip): ")
            author = input("Enter new author (leave blank to skip): ")
            quantity = input("Enter new quantity (leave blank to skip): ")
            quantity = int(quantity) if quantity else None
            if not library.update_book(isbn, title, author, quantity):  # Update an existing book
                print("Book not found.")
        elif choice == '3':
            isbn = input("Enter ISBN of the book to remove: ")
            if not library.remove_book(isbn):  # Remove a book
                print("Book not found.")
        elif choice == '4':
            library.list_books()  # List all books
        elif choice == '5':
            break  # Exit the program
        else:
            print("Invalid choice. Please try again.")  # Display message for invalid input

# Check if the script is being run directly
if __name__ == "__main__":
    main()  # Call the main function
