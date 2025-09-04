# YouTube RAG API

A FastAPI application for YouTube content processing with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- FastAPI backend with automatic API documentation
- CORS middleware for cross-origin requests
- Docker containerization
- Google Cloud Run deployment via GitHub Actions
- Mock weather endpoint for testing

## Local Development

### Prerequisites

- Python 3.9+
- Docker (optional)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ShenSeanChen/yt-rag.git
cd yt-rag
```

2. Create a virtual environment:
```bash
python -m venv venv_yt_rag
source venv_yt_rag/bin/activate  # On Windows: venv_yt_rag\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Docker

### Build and run locally:
```bash
docker build -t yt-rag .
docker run -p 8080:8080 yt-rag
```

## Deployment

This project is configured for automatic deployment to Google Cloud Run via GitHub Actions.

### Prerequisites for deployment:

1. Create a Google Cloud Project
2. Enable Cloud Run API
3. Create a service account with necessary permissions
4. Add the service account key as `GCP_SA_KEY` secret in GitHub repository settings

### Deployment triggers:

- Automatic deployment on push to `main` branch
- Manual deployment via GitHub Actions

## API Endpoints

- `GET /` - Welcome message
- `GET /greet/{name}` - Personalized greeting
- `GET /weather` - Mock weather data

## Environment Variables

- `PORT` - Server port (default: 8080)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to your fork
5. Create a Pull Request

## License

This project is licensed under the MIT License.
