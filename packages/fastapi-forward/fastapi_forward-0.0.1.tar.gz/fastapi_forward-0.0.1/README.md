# FastAPI Forward

FastAPI Forward is a middleware that enables request forwarding/proxying in FastAPI applications. It allows you to easily forward specific routes to different target URLs while maintaining the original request context.

## Features

- Simple decorator-based route forwarding
- Preserves request headers and body
- Supports conditional forwarding
- Easy integration with FastAPI applications

## Installation

```bash
pip install fastapi-forward
```

## Quick Start

Here's a simple example that forwards requests from your FastAPI application to another service:

```python
from fastapi import FastAPI
from fastapi_forward import forward, init_app

app = FastAPI()
init_app(app)

@app.get("/")
@forward("https://api.example.com")
async def root():
    return {"message": "This response will be replaced by the forwarded response"}
```

In this example, any GET request to "/" will be forwarded to "https://api.example.com/".

## Usage

### Basic Forwarding

The most basic usage is to forward a route to another URL:

```python
@app.get("/users")
@forward("https://api.example.com")
async def get_users():
    pass
```

All requests to "/users" will be forwarded to "https://api.example.com/users".

### Initialization

Make sure to initialize the middleware before using the forward decorator:

```python
from fastapi import FastAPI
from fastapi_forward import init_app

app = FastAPI()
init_app(app)
```

### Request Handling

The middleware:
- Preserves request headers
- Forwards request body
- Maintains HTTP methods
- Returns the response from the target URL

## Requirements

- Python 3.10
- FastAPI
- httpx >= 0.28.0

## Development

To set up the development environment:

```bash
# Install PDM if you haven't already
pip install pdm

# Install dependencies
pdm install

# Run tests
pdm run pytest
```

## License

This project is licensed under the MIT License.