# ShopApp Backend

Django REST Framework backend for ShopApp.

## Requirements
- Python 3.10+
- PostgreSQL

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure database
Create a PostgreSQL database then update `settings.py` with your DB credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Create superuser
```bash
python manage.py createsuperuser
```

### 5. Run server
```bash
python manage.py runserver
```

Server runs at `http://127.0.0.1:8000`

## Notes
- Make sure PostgreSQL is running before starting the server
- Frontend must be running at `http://localhost:4200`
- Admin panel available at `http://127.0.0.1:8000/admin`