```markdown
# Flask Weather Data Collector

This project is a Python-based service that collects weather data from the OpenWeather API and stores it as JSON data. It provides two main endpoints for collecting and retrieving weather data.

## Table of Contents
- [Specifications](#specifications)
- [Tools and Frameworks](#tools-and-frameworks)
- [Installation](#installation)
  - [Docker Installation](#docker-installation)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)
- [API Endpoints](#api-endpoints)
- [Repository](#repository)
- [License](#license)

## Specifications

- **Python 3** is mandatory.
- **Service API Endpoints:**
  - `POST /collect`: Receives a user-defined ID, collects weather data from OpenWeather API and stores:
    - The user-defined ID (unique for each request)
    - Datetime of request
    - JSON data with:
      - City ID
      - Temperature in Celsius
      - Humidity
  - `GET /progress/<user_id>`: Receives the user-defined ID, returns the percentage of the POST progress (collected cities completed) until the current moment.
- **Async calls** to collect weather information from multiple city IDs.
- Respect API rate limits of 60 cities per minute.
- **Test coverage** over 90%.
- Dockerized application for easy setup and deployment.

## Tools and Frameworks

### Flask
Used to create the web service and handle API endpoints.

### Flask-RESTful
An extension for Flask that adds support for quickly building REST APIs.

### aiohttp
A Python library used to make asynchronous HTTP requests to the OpenWeather API.

### python-dotenv
Used to load environment variables from a `.env` file, including the OpenWeather API key.

### pytest
A testing framework for Python, used to ensure the application works correctly with over 90% test coverage.

## Installation

### Docker Installation
Ensure you have Docker installed on your system. You can download it from the [Docker website](https://www.docker.com/products/docker-desktop).

1. Clone the repository:
   ```sh
   git clone https://github.com/PabloCGSilva/dev-grid.git
   cd dev-grid
   ```

2. Build the Docker image:
   ```sh
   docker build -t weather_data_collector .
   ```

3. Run the Docker container:
   ```sh
   docker run -d -p 5000:5000 --name weather_data_collector weather_data_collector
   ```

## Running the Application

1. Ensure Docker is running.
2. Follow the [Docker Installation](#docker-installation) steps.
3. The application will be accessible at `http://localhost:5000`.

## Testing the Application

### Running Tests

1. Stop any running container if necessary:
   ```sh
   docker stop weather_data_collector
   docker rm weather_data_collector
   ```

2. Run the tests:
   ```sh
   sh run_tests.sh
   ```

### Testing with Postman, Browser, or curl

- **Using curl**:
  ```sh
  curl -X POST http://localhost:5000/collect -H "Content-Type: application/json" -d "{\"user_id\": \"test_user\", \"city_ids\": [3439525, 3439781]}"
  curl -X GET http://localhost:5000/progress/test_user
  ```

- **Using PowerShell**:
  ```powershell
  $headers = @{
      "Content-Type" = "application/json"
  }
  
  $body = @{
      "user_id" = "test_user"
      "city_ids" = @(3439525, 3439781)
  } | ConvertTo-Json
  
  Invoke-RestMethod -Uri http://localhost:5000/collect -Method Post -Headers $headers -Body $body
  
  Invoke-RestMethod -Uri http://localhost:5000/progress/test_user -Method Get
  ```

## API Endpoints

### POST /collect

**Description:** Collect weather data for specified city IDs.

**Request Body:**
```json
{
  "user_id": "test_user",
  "city_ids": [3439525, 3439781]
}
```

**Response:**
```json
{
  "message": "Data collection in progress"
}
```

### GET /progress/<user_id>

**Description:** Retrieve the progress of the data collection.

**Response:**
```json
{
  "data": [
    {
      "city_id": 3439781,
      "temperature": 11.83,
      "humidity": 73
    },
    {
      "city_id": 3439525,
      "temperature": 13.98,
      "humidity": 66
    }
  ],
  "datetime": "2024-07-15T17:51:31"
}
```

## Repository

GitHub Repository: [https://github.com/PabloCGSilva/dev-grid](https://github.com/PabloCGSilva/dev-grid)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This `README.md` file should provide a comprehensive guide to setting up, running, and testing your application, as well as explaining the tools and frameworks used.
