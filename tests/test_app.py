import pytest
from app import app, db
from models import Contact
@pytest.fixture
def client():
    """Create a test client for the Flask app"""
        # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    # Create test client
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
        db.drop_all()
@pytest.fixture
def sample_contact():
    """Create a sample contact in the database"""
    contact = Contact(
        name='John Doe',
        phone='1234567890',
        email='john@example.com',
        type='Personal'
    )
    db.session.add(contact)
    db.session.commit()
    return contact
def test_index_page(client):
    """Test that the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
def test_add_contact(client):
    """Test adding a new contact through the web form"""
    data = {
        'name': 'Jane Doe',
        'phone': '9876543210',
        'email': 'jane@example.com',
        'type': 'Personal'
    }
    response = client.post('/add', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Jane Doe' in response.data
def test_update_contact(client, sample_contact):
    """Test updating an existing contact"""
    data = {
        'name': 'John Smith',
        'phone': sample_contact.phone,
        'email': sample_contact.email,
        'type': sample_contact.type,
        'submit': 'Update'
    }
    response = client.post(
        f'/update/{sample_contact.id}',
        data=data,  
        follow_redirects=True
    )
    assert response.status_code == 200
    updated_contact = db.session.get(Contact, sample_contact.id)
    assert updated_contact.name == 'John Smith'