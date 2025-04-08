from app.models import db, Book, Member, Transaction
from datetime import datetime
from app import cache

class TransactionService:
    @staticmethod
    @cache.memoize(timeout=300)
    def get_member_transactions(member_id):
        return Transaction.query.filter_by(member_id=member_id).all()

    @staticmethod
    def issue_book(book_id, member_id):
        try:
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
            cache.delete_memoized(TransactionService.get_member_transactions, member_id)
            return transaction
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def return_book(transaction_id):
        try:
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
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def batch_update_books(book_updates):
        """Batch update multiple books at once"""
        try:
            for book_id, quantity in book_updates.items():
                book = Book.query.get(book_id)
                if book:
                    book.quantity = quantity
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    @cache.memoize(timeout=300)
    def get_member_stats(member_id):
        """Get cached member statistics"""
        return {
            'total_books': Transaction.query.filter_by(member_id=member_id).count(),
            'active_loans': Transaction.query.filter_by(
                member_id=member_id,
                return_date=None
            ).count(),
            'total_fees': db.session.query(
                db.func.sum(Transaction.rent_fee)
            ).filter_by(member_id=member_id).scalar() or 0
        }
