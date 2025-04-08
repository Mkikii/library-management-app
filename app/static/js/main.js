$(document).ready(function() {
    // Book search functionality
    $("#bookSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("table tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

function showLoading(element) {
    element.prop('disabled', true).html('<span class="spinner-border spinner-border-sm"></span> Loading...');
}

function hideLoading(element, originalText) {
    element.prop('disabled', false).html(originalText);
}

function showError(message) {
    const alert = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    $('.container').prepend(alert);
}

function editBook(bookId) {
    const btn = $(event.target);
    showLoading(btn);
    const row = $(event.target).closest('tr');
    const title = row.find('td:eq(0)').text();
    const author = row.find('td:eq(1)').text();
    const quantity = row.find('td:eq(2)').text();

    const newTitle = prompt('Enter new title:', title);
    const newAuthor = prompt('Enter new author:', author);
    const newQuantity = prompt('Enter new quantity:', quantity);

    if (newTitle && newAuthor && newQuantity) {
        fetch(`/books/${bookId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: newTitle,
                author: newAuthor,
                quantity: parseInt(newQuantity)
            })
        })
        .then(response => window.location.reload())
        .catch(error => {
            showError(error.message);
        })
        .finally(() => {
            hideLoading(btn, 'Edit');
        });
    }
}

function deleteBook(bookId) {
    if (confirm("Are you sure you want to delete this book?")) {
        fetch(`/books/${bookId}`, { method: 'DELETE' })
            .then(response => window.location.reload())
            .catch(error => console.error('Error:', error));
    }
}

function editMember(memberId) {
    const row = $(event.target).closest('tr');
    const name = row.find('td:eq(0)').text();
    const email = row.find('td:eq(1)').text();

    const newName = prompt('Enter new name:', name);
    const newEmail = prompt('Enter new email:', email);

    if (newName && newEmail) {
        fetch(`/members/${memberId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: newName,
                email: newEmail
            })
        })
        .then(response => window.location.reload())
        .catch(error => console.error('Error:', error));
    }
}

function viewHistory(memberId) {
    fetch(`/transactions/history/${memberId}`)
        .then(response => response.json())
        .then(transactions => {
            const content = transactions.map(t => `
                <tr>
                    <td>${t.book_title}</td>
                    <td>${t.issue_date}</td>
                    <td>${t.return_date || 'Not returned'}</td>
                    <td>${t.rent_fee ? 'KES ' + t.rent_fee : '-'}</td>
                </tr>
            `).join('');

            $('#historyModal .modal-body table tbody').html(content);
            $('#historyModal').modal('show');
        });
}

function calculateRentFee(issueDateString) {
    const issueDate = new Date(issueDateString);
    const today = new Date();
    const diffTime = Math.abs(today - issueDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays * 10; // KES 10 per day
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-GB');
}

// Update search functionality to use AJAX
$("#bookSearch").on("keyup", function() {
    const query = $(this).val();
    if (query.length > 2) {
        fetch(`/search/books?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(books => updateBookTable(books))
            .catch(error => console.error('Error:', error));
    }
});

function updateBookTable(books) {
    const tbody = $('.table tbody');
    tbody.empty();

    books.forEach(book => {
        tbody.append(`
            <tr>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.quantity}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editBook(${book.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteBook(${book.id})">Delete</button>
                </td>
            </tr>
        `);
    });
}
