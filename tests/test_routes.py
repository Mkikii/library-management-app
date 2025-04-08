import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.models import db, Book, Member, Transaction
from datetime import datetime
from tests.conftest import TestConfig  # Import TestConfig

def generate_unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@test.com"

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_book(client, db_session):
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

def test_issue_book(client, db_session):
    # First create test data
    with client.application.app_context():
        book = Book(title='Test Book', author='Test Author', quantity=1)
        member = Member(name='Test Member', email=generate_unique_email())
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
