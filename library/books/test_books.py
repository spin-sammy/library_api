import pytest
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book


@pytest.fixture
def api_client():
    """Fixture to provide an instance of APIClient for HTTP requests."""
    return APIClient()


@pytest.fixture
def sample_book(db):
    """Fixture to create a sample book for use in tests."""
    return Book.objects.create(
        title='Test Book',
        author='Test Author',
        isbn='1234567890123',
        language='English'
    )


@pytest.fixture
def book_factory(db):
    """Factory fixture to create multiple book instances."""
    def create(**kwargs):
        return Book.objects.create(
            title=kwargs.get("title", "Sample Book"),
            author=kwargs.get("author", "Sample Author"),
            published_date=kwargs.get("published_date", "2023-01-01"),
            isbn=kwargs.get("isbn", f"978316148{Book.objects.count():04d}"),
            pages=kwargs.get("pages", 150),
            cover=kwargs.get("cover", "https://example.com/image.jpg"),
            language=kwargs.get("language", "English")
        )
    return create


@pytest.mark.django_db
def test_create_book(api_client):
    """Test creating a book with valid data."""
    response = api_client.post('/api/books/', {
        'title': 'New Book',
        'author': 'New Author',
        'isbn': '9876543210123',
        'language': 'English'
    })
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_book_missing_fields(api_client):
    """Test creating a book with missing required fields."""
    response = api_client.post('/api/books/', {
        'title': '',
        'author': '',
        'isbn': '',
        'language': ''
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_book_duplicate_isbn(api_client, sample_book):
    """Test creating a book with an existing ISBN."""
    response = api_client.post('/api/books/', {
        'title': 'Duplicate Book',
        'author': 'Another Author',
        'isbn': sample_book.isbn,
        'language': 'English'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_books(api_client, book_factory):
    """Test retrieving the list of books."""
    book_factory(title="Book One", isbn="9783161481001")
    book_factory(title="Book Two", isbn="9783161481002")
    response = api_client.get('/api/books/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) >= 2


@pytest.mark.django_db
def test_get_book_detail(api_client, sample_book):
    """Test retrieving a book by ID."""
    response = api_client.get(f'/api/books/{sample_book.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == sample_book.title


@pytest.mark.django_db
def test_update_book(api_client, sample_book):
    """Test updating a book's information."""
    response = api_client.put(f'/api/books/{sample_book.id}/', {
        'title': 'Updated Title',
        'author': 'Updated Author',
        'isbn': sample_book.isbn,
        'language': 'English'
    })
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_book(api_client, sample_book):
    """Test deleting an existing book."""
    response = api_client.delete(f'/api/books/{sample_book.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_filter_books_by_author(api_client, sample_book):
    """Test filtering books by author name."""
    response = api_client.get('/api/books/?author=Test Author')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) >= 1


@pytest.mark.django_db
def test_filter_books_by_language(api_client, sample_book):
    """Test filtering books by language."""
    response = api_client.get('/api/books/?language=English')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) >= 1


@pytest.mark.django_db
def test_pagination(api_client):
    """Test pagination returns correct number of results per page."""
    for i in range(15):
        Book.objects.create(
            title=f'Book {i}',
            author='Author',
            isbn=f'978316148{i:04d}',
            language='English'
        )
    response = api_client.get('/api/books/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 10


@pytest.mark.django_db
def test_invalid_book_update(api_client, sample_book):
    """Test updating a book with invalid data."""
    response = api_client.put(f'/api/books/{sample_book.id}/', {
        'title': '',
        'author': '',
        'isbn': 'invalidisbn',
        'language': ''
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_nonexistent_book(api_client):
    """Test retrieving a book that does not exist."""
    response = api_client.get('/api/books/99999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_nonexistent_book(api_client):
    """Test deleting a book that does not exist."""
    response = api_client.delete('/api/books/99999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
