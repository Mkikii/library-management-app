from app.models import db, Book, Member, Transaction
from datetime import datetime

class TransactionService:
    @staticmethod
    def issue_book(book_id, member_id):
        member = Member.query.get_or_404(member_id)
        if member.debt > 500:
            raise ValueError('Member has too much debt')

        book = Book.query.get_or_404(book_id)
        if book.quantity < 1:
            raise ValueError('Book out of stock')

        transaction = Transaction(book_id=book_id, member_id=member_id)
        book.quantity -= 1

        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def return_book(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        if transaction.return_date:
            raise ValueError('Book already returned')

        days = (datetime.utcnow() - transaction.issue_date).days
        rent_fee = days * 10

        transaction.return_date = datetime.utcnow()
        transaction.rent_fee = rent_fee
        transaction.member.debt += rent_fee
        transaction.book.quantity += 1

        db.session.commit()
        return rent_fee
