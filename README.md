# Library Management System

A simple web application for librarians to manage books, members, and book transactions. Built with Flask and PostgreSQL.

## Features

- Manage books (add, edit, delete, track stock)
- Manage members (add, edit, track debt)
- Issue and return books
- Calculate rent fees (KES 10 per day)
- Search books by title or author
- View member transaction history
- Dashboard with key metrics

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the project root:
