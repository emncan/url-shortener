# FastAPI URL Shortener

This project provides a service for shortening long URLs and redirecting visitors when they use the shortened URLs. It includes PostgreSQL for data storage, Redis for caching, an API Key-based authentication mechanism, and a daily Rate Limit of 50 requests per user. A default user is created on the first run, as specified in your .env file.

## Features

- **URL Shortening**: Converts a long URL into a short code and stores the mapping in the database.
- **Redirection**: Automatically redirects to the original URL when a shortened URL is requested.
- **API Key Authentication**: All endpoints require an API key passed via the request header.
- **Daily Rate Limit**: Each user can make up to 50 requests per day.
- **Default User**: A default user is automatically created (based on .env values) when the service starts for the first time.
- **Docker & Docker Compose**: Containers for PostgreSQL, Redis, and FastAPI.

- **Pytest** for testing.

## Technologies Used

- **Python 3.11** + **FastAPI**
- **SQLAlchemy** (for database operations)
- **PostgreSQL** (main database)
- **Redis** (caching mechanism)
- **Docker & Docker Compose** (containerized deployments)
- **Logging** (using the standard Python logging library)
- **Pytest** (for testing)

## Project Structure

```bash
fastapi_url_shortener
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── url_endpoints.py
│   │   │   └── __init__.py
│   │   ├── dependencies
│   │   │   └── auth.py
│   │   └── __init__.py
│   ├── core
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── logging_config.py
│   │   ├── rate_limit_middleware.py
│   │   └── security.py
│   ├── db
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud
│   │       ├── crud_user.py
│   │       ├── crud_url.py
│   │       └── __init__.py
│   ├── services
│   │   ├── utils.py
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── tests
│   ├── test_urls.py
│   └── __init__.py
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup Instructions
### Build and Run with Docker

This project uses Docker to set up the necessary services.
#### Step 1: Build and start the containers
In the project root directory, run the following command to build and start the Docker containers:

```bash
docker-compose up --build
```
This will spin up:

- A **PostgreSQL** database container (
    ```postgres_db```)
- A **Redis** cache container (```redis_cache```)
- A **FastAPI** app container (```fastapi_app```)

#### Step 2: Access the API
Once the containers are up and running, the FastAPI application will be available at:
```bash
http://localhost:8000
```
You can access the automatic API documentation at:
- **Swagger UI**: http://localhost:8000/docs#/
- **ReDoc UI**: http://localhost:8000/redoc

<img src="https://github.com/user-attachments/assets/b5025e09-e540-48db-b869-4b693efc34d5" 
     alt="Görsel Açıklama" 
     style="width:700px; height:200px;" />

**Note: The default user (with the username and API key from .env) is automatically created on the first run.**

## Usage

#### 1. URL Shortening (POST ```/shorten```)
- Include the ```x-api-key``` header in your request, for example: ```x-api-key: abc123xyz```.
- send a POST request to `/shorten` with the following JSON payload:
    ```bash
    POST: http://localhost:8000/shorten
    {
        "original_url": "https://www.google.com"
    }
    ```

- Example Response:
    ```bash
            {
            "status": "success",
            "message": "URL shortened successfully.",
            "data": {
                "short_url": "http://localhost:8000/bkvUgdfZe2PoP6q"
            }
        }
    ```

    <img src="https://github.com/user-attachments/assets/298834f2-0b71-4788-8add-1cefe2b61a86" 
     alt="Görsel Açıklama" 
     style="width:500px; height:300px;" />


#### 2. Redirection (GET ```/{short_code}```)
- Navigate to http://localhost:8000/{short_code}, and the service will redirect you to the stored original URL if found.
- The system uses Redis cache for quicker lookups.

    <img src="https://github.com/user-attachments/assets/a30343b6-e527-4103-823a-ce411054b87d" 
     alt="Görsel Açıklama" 
     style="width:500px; height:300px;" />

#### 3. Rate Limit
- Each user can make 50 requests per day.
- If you exceed the limit, you get a ```429 Too Many Requests``` error, for example:

    ```
        {
            "status": "error",
            "message": "Daily request limit exceeded.",
            "data": {}
        }
    ```

## Running Tests with pytest Inside Docker
To run tests inside your Docker container using pytest, follow these steps:

#### 1. Access the Running Docker Container
Once the containers are running, you can access the web service container using the docker exec command.

First, find the name or ID of the running web container:
```bash
docker ps
```
This will show the list of running containers. Look for the container running the web service (your FastAPI app), and note the container name or ID

Then, use the following command to access the container’s shell:

```bash
docker exec -it <container_name> sh
```
Replace <container_name> with the actual name or ID of your container.

#### 2. Run the Tests
Once inside the container, you can run pytest to execute your tests:
```bash
pytest -k test_shorten_url
pytest -k test_exist_original_url
pytest -k test_redirect_url
pytest -k test_rate_limit_exceeded
```

### 4. Stop the Docker Containers
To stop the containers, use the following command:
```bash
docker-compose down
```

