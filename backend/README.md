
Futtatás:

```bash
cd backend
uvicorn app.main:app --reload
```


# FastAPI Project

This is a FastAPI-based project with JWT authentication middleware. The project includes protected routes under `/api` that require authentication and public routes accessible without authentication.

## Requirements

-   Python 3.10 or higher
-   Pip (Python package manager)
-   Virtual environment support (optional but recommended)

## Installation

Follow these steps to set up the project:

### 1. Clone the Repository

git clone <repository_url>

Navigate to the project directory:
cd <project_directory>

### 2. Create a Virtual Environment

Set up a virtual environment to isolate dependencies:
python -m venv venv

Activate the virtual environment:

-   On macOS/Linux:
    source venv/bin/activate
-   On Windows:
    venv\Scripts\activate

### 3. Install Dependencies

Install all required dependencies listed in `requirements.txt`:
pip install -r requirements.txt

### 4. Set Up Environment Variables

LATER

### 5. Run the Server

Start the FastAPI server using Uvicorn:
uvicorn app.main:app --reload

The server will start at `http://127.0.0.1:8000`.

## Usage

### Access API Documentation

Open your browser and navigate to:

-   Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Test Endpoints

#### Public Route (`GET /xyz`)

No authentication required:
curl http://127.0.0.1:8000/xyz

Expected Response:
{
"message": "This is a public route"
}

#### Protected Route (`GET /api/xyz`)

Requires a valid JWT token.

**Invalid Token**:

curl -X GET http://127.0.0.1:8000/api/xyz
-H "Authorization: Bearer invalid_token"

Expected Response (401 Unauthorized):
{
"detail": "Invalid token"
}

**Valid Token**:
Replace `<your_valid_jwt_token>` with a valid JWT token obtained from `/auth/token`.
curl -X GET http://127.0.0.1:8000/api/xyz
-H "Authorization: Bearer <your_valid_jwt_token>"
Expected Response (200 OK):
{
"message": "This is a protected route"
}

## Troubleshooting

### Common Issues

#### `ModuleNotFoundError`

If you encounter `ModuleNotFoundError` for modules like `app`, ensure you're running the server from the correct directory (the root of your project):
