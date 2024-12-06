# ReqCurl - Python Wrapper for cURL Commands

## Overview

**ReqCurl** is a Python library that allows you to easily parse cURL commands and convert them into a dictionary format suitable for making HTTP requests using Python’s `requests` library. This parser can handle HTTP methods, headers, data, and authentication parameters typically found in cURL commands, making it easier to work with APIs when transitioning from shell scripts to Python code.

## Features

- **HTTP Methods**: Supports standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, etc.).
- **URL Parsing**: Automatically extracts the URL from the cURL command.
- **Header Parsing**: Handles custom headers (e.g., `Authorization`, `Content-Type`, etc.).
- **Data Parsing**: Parses data passed via `-d` or `--data` flags (supports `key=value` pairs).
- **Authentication**: Supports parsing user credentials from the `--user` flag.
- **Error Handling**: Provides error messages for invalid cURL commands and formats.

## Table of Contents

- [Installation](#installation)
- [Clone the repository](#clone-the-repository)
- [Usage](#usage)
  - [Basic Example](#basic-example)
  - [Parsing Data](#parsing-data)
  - [Parsing Headers](#parsing-headers)
  - [Authentication Parsing](#authentication-parsing)
- [Tests](#tests)
- [Supported cURL Features](#supported-curl-features)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the `reqcurl` library, you can simply use pip to install it from the Python Package Index (PyPI).

### Installation via pip:

```bash
pip install reqcurl
```
Alternatively, you can clone this repository and install it locally.
## Clone the Repository:
```bash
git clone https://github.com/your-username/reqcurl.git
cd reqcurl
pip install 
```
## Usage

Once installed, you can start using the library by importing it into your Python script. The main function is `parse_curl()`, which takes a cURL command as input and returns a dictionary with parsed request details.

### Basic Example
```bash
from reqcurl import parse_curl

curl_command = 'curl -X GET https://api.example.com/data'
result = parse_curl(curl_command)

print(result)
```

### Output

```bash
{
    "method": "GET",
    "url": "https://api.example.com/data",
    "headers": {},
    "data": None,
    "auth": None
}
```

### Parsing Data

For POST requests with data, use the `-d` or `--data` flags. Here's an example of parsing a POST request with data:

```bash
curl_command = 'curl -X POST https://api.example.com/data -d "key=value"'
result = parse_curl(curl_command)

print(result)
```
### Output:
```bash
{
    "method": "POST",
    "url": "https://api.example.com/data",
    "headers": {},
    "data": {"key": "value"},
    "auth": None
}
```
### Parsing Headers
You can also add custom headers using the `-H` flag. Here's an example with an `Authorization` header:
```bash
curl_command = 'curl -X GET https://api.example.com/data -H "Authorization: Bearer token"'
result = parse_curl(curl_command)

print(result)
```
### Output
```bash
{
    "method": "GET",
    "url": "https://api.example.com/data",
    "headers": {
        "Authorization": "Bearer token"
    },
    "data": None,
    "auth": None
}
```
### Authentication Parsing
Authentication can be parsed using the `--user` flag, typically in the format `username:password`. Here's an example of parsing authentication credentials:
```bash
curl_command = 'curl -X GET https://api.example.com/data --user "username:password"'
result = parse_curl(curl_command)

print(result)
```
### Output
```bash
{
    "method": "GET",
    "url": "https://api.example.com/data",
    "headers": {},
    "data": None,
    "auth": ("username", "password")
}
```
## Tests
ReqCurl comes with unit tests to ensure that it works as expected. To run the tests, simply use `pytest`:
```bash
pytest tests/

OR

python -m pytest tests/
```
This will run all the tests defined in the `tests` folder and show the results in your terminal.
### Test Example
Here’s a simple test case for parsing a `GET` request:
```bash
def test_parse_curl_basic_get():
    curl_command = 'curl -X GET https://api.example.com/data'
    expected_result = {
        "method": "GET",
        "url": "https://api.example.com/data",
        "headers": {},
        "data": None,
        "auth": None
    }

    result = parse_curl(curl_command)
    assert result == expected_result
```
### Edge Case Handling
The parser also handles edge cases like missing URLs, invalid formats, and incorrect headers. Ensure that all such cases are covered in your tests.
```bash
def test_parse_invalid_curl():
    curl_command = 'curl -X INVALID https://api.example.com/data'
    try:
        result = parse_curl(curl_command)
    except ValueError as e:
        assert str(e) == "Invalid HTTP method: INVALID"
```
## Supported cURL Features
| Feature         | cURL Flag     | Supported | Notes                          |
|-----------------|---------------|-----------|--------------------------------|
| HTTP Methods    | -X            | ✅         | Defaults to GET if not specified |
| Headers         | -H            | ✅         | Parses multiple headers        |
| Data/Body       | -d, --data    | ✅         | Supports JSON or form data     |
| Authentication  | --user        | ✅         | Basic authentication           |
| Cookies         | -b, --cookie  | ❌         | Planned                        |
| File Upload     | -F, --form    | ❌         | Planned                        |
| Proxies         | -x, --proxy   | ❌         | Planned                        |

## Roadmap
- Add support for cookies, file uploads, and proxies.
- Handle multipart requests.
- Extend testing coverage for edge cases.

## Contributing
We welcome contributions to ReqCurl! If you have suggestions, fixes, or improvements, please fork the repository, make your changes, and submit a pull request.
### Steps to Contribute
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Write tests for the changes.
5. Submit a pull request for review.

## License
`ReqCurl` is released under the MIT License. See the [LICENSE](#license) file for details.
```bash 
This markdown file includes all sections, from installation to usage, tests, and contributing. Each section has been structured to be clear and easy to follow for users and contributors alike.
```
