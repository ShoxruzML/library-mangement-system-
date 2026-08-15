# Library Management System
from datetime import date, timedelta

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.loans = []

    def add(self, title, author):
        new_book = Book(title, author)
        self.books.append(new_book)

    def remove(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                return
        print('Book Not Found!')

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]

    def add_member(self, name):
        new_member = Member(name)
        self.members.append(new_member)

    def remove_member(self, name):
        for member in self.members:
            if member.name == name:
                self.members.remove(member)
                return

        print('Member Not Found!')

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def issue_loan(self, isbn, member_id):
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if book is None or member is None:
            print('Book or Member not found.')
            return
        if not book.available:
            print('Book not found.')
            return

        new_loan = Loan(book, member)
        self.loans.append(new_loan)
        book.available = False
        member.borrow(book)

    def return_loan(self, isbn):
        book = self.find_book(isbn)
        if book is None:
            print('Book not found.')
            return
        for loan in self.loans:
            if loan.book == book and loan.return_date is None:
                loan.return_date = date.today()
                book.available = True
                loan.member.return_book(book)
                fine = loan.calculate_fine()
                print(f'Returned. Fine: {fine}')
                return

        print('No active loan found for this book.')
class Book:
    _counter = 1
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.isbn = f'ISBN{Book._counter:04d}'
        self.available = True
        Book._counter += 1

    def __repr__(self):
        return f'{self.title} by {self.author} {self.isbn}'

    def check_avail(self):
        return self.available


class Member:
    _counter = 1
    def __init__(self, name):
        self.name = name
        self.member_id = f'Member ID: {Member._counter:04d}'
        self.borrowed_books = []
        Member._counter += 1

    def borrow(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        self.borrowed_books.remove(book)

    def __repr__(self):
        return f'Name {self.name}, Member ID: {self.member_id}'

class Loan:
    def __init__(self, book, member):
        self.book = book
        self.member = member
        self.issue_date = date.today()
        self.due_date = self.issue_date + timedelta(14)
        self.return_date = None

    def calculate_fine(self, rate_per_day=0.5):
        if self.return_date and  self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * rate_per_day
        return 0

l = Library()
l.add('Harry Potter', 'J K')
l.add_member('Shokhruz')

print(l.books)
print(l.members)

l.issue_loan('ISBN0001', 'Member ID: 0001')

print(l.books[0].available)
print(l.members[0].borrowed_books)

l.issue_loan('ISBN001', 'Member ID: 0001')
l.issue_loan('FAKE_ISBN', 'Member ID: 0001')
print(l.search_by_title('Harry'))

l.return_loan('ISBN0001')

print(l.books[0].available)
print(l.members[0].borrowed_books)

l.return_loan('ISBN0001')

l.return_loan('FAKE_ISBN')

l.issue_loan('ISBN0001', 'Member ID: 0001')
l.loans[-1].due_date = date.today() -timedelta(days=5)
l.return_loan('ISBN0001')