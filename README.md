Library Management System

A command-line Library Management System built with Python OOP as part of a 90-day Python learning roadmap (Week 2 challenge). Models a real library's core operations — books, members, and loans — with full test coverage.

Features
- Book management — add and remove books, each auto-assigned a unique ISBN
- Member management — add and remove members, each auto-assigned a unique member ID
- Search — find books by title or author (partial match, case-insensitive)
- Loans — issue and return loans, with availability tracking on each book
- Overdue fines — automatically calculated based on days late and a daily rate
- Full test suite — 15 pytest tests covering every method, including edge cases

Project Structure

week_two_project/
├── library.py       # Core classes: Book, Member, Loan, Library
└── test_library.py  # pytest test suite
Classes

*Book* — represents a single book. Auto-generates its own ISBN via a class-level counter. Tracks title, author, and availability.

*Member* — represents a library member. Auto-generates a member ID and tracks borrowed books. Has borrow() and return_book() methods.

*Loan* — represents a borrowing transaction — links a Book and a Member, with issue date, due date (14-day period), and return date. Calculates overdue fines.

*Library* — the central manager. Holds collections of books, members, and loans, and coordinates operations:
- add(title, author) / remove(isbn)
- add_member(name) / remove_member(name)
- search_by_title(title) / search_by_author(author)
- issue_loan(isbn, member_id) / return_loan(isbn)
- find_book(isbn) / find_member(member_id) — internal lookup helpers

Usage
from library import Library

l = Library()
l.add('Harry Potter', 'J K Rowling')
l.add_member('Shokhruz')
l.issue_loan('ISBN0001', 'Member ID: 0001')
l.return_loan('ISBN0001')
results = l.search_by_title('harry')
Running Tests
pytest test_library.py
All 15 tests pass, covering: adding/removing books and members, searching (with no-match cases), issuing loans (success, not found, already borrowed), returning loans (success, no active loan), and fine calculation (on-time and overdue).

What I Learned

This project was a deep dive into OOP fundamentals — class design, dunder methods, class-level counters for auto-generated IDs, and separating concerns between classes (Library coordinates, but Member manages its own borrowed list). It pushed me to think through design questions like "does this method belong on this class, or the one managing the collection?"

Tech Stack
- Python 3.12
- pytest
- datetime (loan dates, fine calculations)
