import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.models import db, Book, Member, Transaction
from datetime import datetime
from tests.conftest import TestConfig  # Import TestConfig

# Remove the app fixture as it's now in conftest.py
# Use the fixture from conftest.py instead

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_book(client):
    response = client.post('/books', data={
        'title': 'Test Book',
        'author': 'Test Author',
        'quantity': 5
    })
    assert response.status_code == 302
    with client.application.app_context():
        book = Book.query.filter_by(title='Test Book').first()
        assert book is not None
        assert book.quantity == 5

def test_issue_book(client):
    # First create test data
    with client.application.app_context():
        book = Book(title='Test Book', author='Test Author', quantity=1)
        member = Member(name='Test Member', email='test@test.com')
        db.session.add_all([book, member])
        db.session.commit()

        response = client.post('/issue-book', data={
            'book_id': book.id,
            'member_id': member.id
        })
        assert response.status_code == 302

        # Verify book quantity decreased
        book = Book.query.get(book.id)
        assert book.quantity == 0
