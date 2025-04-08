import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.models import Book, Member, Transaction, db
from datetime import datetime, timedelta

def test_book_creation(app):
    with app.app_context():
        book = Book(title='Test Book', author='Test Author', quantity=5)
        assert book.title == 'Test Book'
        assert book.quantity == 5

def test_member_debt_calculation(app):
    with app.app_context():
        member = Member(name='Test Member', email='test@test.com')
        book = Book(title='Test Book', author='Test Author', quantity=1)
        db.session.add_all([member, book])
        db.session.commit()

        transaction = Transaction(
            book_id=book.id,
            member_id=member.id,
            issue_date=datetime.utcnow() - timedelta(days=5)
        )
        db.session.add(transaction)
        transaction.return_date = datetime.utcnow()
        transaction.rent_fee = 50
        member.debt += transaction.rent_fee

        assert member.debt == 50
