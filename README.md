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
