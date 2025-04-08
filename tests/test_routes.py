import pytest
from app import create_app
from app.models import db, Book, Member, Transaction
from datetime import datetime

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

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
