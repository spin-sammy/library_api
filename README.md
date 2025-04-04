#  Library API

A modern, REST API for managing books in a digital library. Built with **Django 5**, **Django REST Framework**, **PostgreSQL**, and powered by **Docker**.

---

## Features

- Full CRUD support for books (Create, Read, Update, Delete)
- Filtering by `author`, `published_date`, and `language`
- Pagination (default: 10 books per page)
- ViewSet-based structure for clean routing
- `pytest`-driven testing with 100% coverage
- `docker-compose` for isolated development and testing

---

## Technologies

- **Framework:** Django 5.x, Django REST Framework
- **Database:** PostgreSQL 15
- **Testing:** Pytest, Coverage
- **Packaging:** Docker, docker-compose
- **Filtering:** django-filter

---

## Project Structure

```
library_api/
├── books/                 # App with models, views, serializers, tests
│   ├── models.py
│   ├── views.py           # ViewSet implementation
│   ├── urls.py            # DefaultRouter-based routing
│   ├── serializers.py
│   ├── test_books.py      # All tests using Pytest
├── library/               # Project core
│   ├── settings.py
│   ├── wsgi.py
│   └── manage.py
├── Dockerfile             # Docker build instructions
├── docker-compose.yml     # Main docker config
├── docker-compose.override.yml # Dev-mode (runserver)
├── requirements.txt       # All dependencies including test ones
```

---

## Installation

### 1. Clone the repo
```bash
git clone https://github.com/spin-sammy/library_api.git
cd library_api
```

### 2. Set up environment
Create `.env` file based on this template:
```env
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Start the project
```bash
docker-compose up --build
```

API will be available at: `http://localhost:8000/api/books/`

---

## Running Tests

### 1. Inside Docker
```bash
docker-compose exec web pytest
```

### 2. With coverage
```bash
docker-compose exec web coverage run -m pytest
```
View report:
```
docker-compose exec web coverage report -m
```

Generate a detailed web report:
```bash
docker-compose exec web coverage html
```
It will be available in the folder: `library/htmlcov/index.html`

---

## API Overview

### Endpoints:
- `GET /api/books/` — List books
- `POST /api/books/` — Create new book
- `GET /api/books/{id}/` — Retrieve book by ID
- `PUT /api/books/{id}/` — Update book
- `DELETE /api/books/{id}/` — Delete book

### Filters:
```bash
/api/books/?author=King
/api/books/?language=English
/api/books/?published_date=2023-01-01
```

### Pagination:
```bash
/api/books/?page=2&page_size=5
```

---

## Contribution

Feel free to fork and submit pull requests. We use `pytest` and `coverage`, so please write tests for any new features.

