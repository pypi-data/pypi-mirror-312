# Niho

Niho is a simple HTTP server framework for Python.

## Features
- Lightweight and easy to use.
- Add, update, and delete routes with ease.

## Installation
Install Niho using pip:
```bash
pip install niho
```

```python
from niho import NihoServer // import package

PORT = 3000
server = NihoServer() // create server

server.add("/", "Welcome to the homepage!") // "/" for homepage
server.add("/about", "This is the about page.") // You can replace the second variable with the file location.
server.set("/", status_code=200, content="Homepage with custom status code")
server.run(port=PORT)  # IP defaults to localhost change with ip=INPUT_IP if you want
```