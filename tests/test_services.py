import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.services import TransactionService
from app.models import Book, Member, Transaction, db

def generate_unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@test.com"

def test_issue_book_with_debt(app):
    with app.app_context():
        member = Member(name='Test', email=generate_unique_email(), debt=600)
        db.session.add(member)
        db.session.commit()

        with pytest.raises(ValueError, match='Member has too much debt'):
            TransactionService.issue_book(1, member.id)

def test_return_book_calculation(app):
    with app.app_context():
        book = Book(title='Test', author='Test', quantity=1)
        member = Member(name='Test', email=generate_unique_email())
        db.session.add_all([book, member])
        db.session.commit()

        transaction = TransactionService.issue_book(book.id, member.id)
        rent_fee = TransactionService.return_book(transaction.id)
        assert rent_fee >= 0
