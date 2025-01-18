# URL Shortener
A Django REST Framework-based URL shortener with expiry and analytics functionality.

## Features

- Create shortened URLs with optional expiry time
- Password protection for URLs
- Access analytics tracking
- SQLite database storage
- RESTful API endpoints

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `POST /shorten/`: Create a shortened URL
  - Parameters:
    - `original_url` (required): The URL to shorten
    - `expired_at` (optional): Number of hours until expiry (default: 24)
    - `password` (optional): Password protection for the URL

- `GET /<short_url>/`: Redirect to original URL
  - Query Parameters:
    - `password` (if required): Password to access protected URLs

- `GET /analytics/<short_url>/`: Get analytics for a shortened URL

## Example Usage

Create a shortened URL:
```bash
curl -X POST http://localhost:8000/api/v1/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com", "expiry_hours": 48}'
```

Access a shortened URL:
```bash
curl http://localhost:8000/api/v1/urls/abc123/
```

Get analytics:
```bash
curl http://localhost:8000/api/v1/urls/abc123/analytics/
```
