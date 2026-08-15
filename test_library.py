from library import Library, Book , Member, Loan
from datetime import date, timedelta

def test_add_book():
    l = Library()
    l.add('Harry Potter', 'J K')
    assert len(l.books) == 1
    assert l.books[0].title == 'Harry Potter'

def test_search_by_title():
    l = Library()
    l.add('Harry Potter', 'J K')
    results = l.search_by_title('harry')
    assert len(results) == 1
    assert results[0].title == 'Harry Potter'

def test_search_by_title_no_match():
    l = Library()
    l.add('Harry Potter', 'J K')
    results = l.search_by_title('nonexistent')
    assert results == []

def test_search_by_author():
    l = Library()
    l.add('Harry Potter', 'J K')
    results = l.search_by_author('j k')
    assert len(results) == 1

def test_issue_loan_success():
    l = Library()
    l.add('Harry Potter', 'J K')
    l.add_member('Shokhruz')
    isbn = l.books[0].isbn
    member_id = l.members[0].member_id
    l.issue_loan(isbn, member_id)
    assert l.books[0].available == False
    assert len(l.members[0].borrowed_books) == 1
    assert len(l.loans) == 1

def test_issue_loan_book_not_found():
    l = Library()
    l.add_member('Shokhruz')
    member_id = l.members[0].member_id
    l.issue_loan('FAKE_ISBN', member_id)
    assert len(l.loans) == 0

def test_issue_loan_member_not_found():
    l = Library()
    l.add('Harry Potter', 'J K')
    isbn = l.books[0].isbn
    l.issue_loan(isbn, 'FAKE_ID')
    assert len(l.loans) == 0

def test_issue_loan_already_borrowed():
    l = Library()
    l.add('Harry Potter', 'J K')
    l.add_member('Shokhruz')
    isbn = l.books[0].isbn
    member_id = l.members[0].member_id
    l.issue_loan(isbn, member_id)
    l.issue_loan(isbn, member_id)  # try again while still out
    assert len(l.loans) == 1  # should NOT create a second loan

def test_return_loan_success():
    l = Library()
    l.add('Harry Potter', 'J K')
    l.add_member('Shokhruz')
    isbn = l.books[0].isbn
    member_id = l.members[0].member_id
    l.issue_loan(isbn, member_id)
    l.return_loan(isbn)
    assert l.books[0].available == True
    assert len(l.members[0].borrowed_books) == 0

def test_return_loan_no_active_loan():
    l = Library()
    l.add('Harry Potter', 'J K')
    isbn = l.books[0].isbn
    l.return_loan(isbn)  # never issued, should not crash

def test_calculate_fine_on_time():
    l = Library()
    l.add('Harry Potter', 'J K')
    l.add_member('Shokhruz')
    isbn = l.books[0].isbn
    member_id = l.members[0].member_id
    l.issue_loan(isbn, member_id)
    l.loans[-1].return_date = date.today()
    fine = l.loans[-1].calculate_fine()
    assert fine == 0

def test_calculate_fine_late():
    l = Library()
    l.add('Harry Potter', 'J K')
    l.add_member('Shokhruz')
    isbn = l.books[0].isbn
    member_id = l.members[0].member_id
    l.issue_loan(isbn, member_id)
    l.loans[-1].due_date = date.today() - timedelta(days=5)
    l.loans[-1].return_date = date.today()
    fine = l.loans[-1].calculate_fine()
    assert fine == 2.5

def test_add_member():
    l = Library()
    l.add_member('Shokhruz')
    assert len(l.members) == 1
    assert l.members[0].name == 'Shokhruz'

def test_remove_member():
    l = Library()
    l.add_member('Shokhruz')
    l.remove_member('Shokhruz')
    assert len(l.members) == 0

def test_remove_book():
    l = Library()
    l.add('Harry Potter', 'J K')
    isbn = l.books[0].isbn
    l.remove(isbn)
    assert len(l.books) == 0