# Coding exercise: URL shortener

## Installation and preparation

- Create a virtualenv `python -m .venv`
- Install dependenciies `pip install -r requirements.txt`
- Initiate db migration `python manage.py migrate`

> **Note:** This program doesn't need to run the server, we will rely on unit tests to check working api endpoints.

## Instruction

1. Create url endpoint: `/`
    - A short url should have a random unique key of a 10 char-length.
        - e.g. http://localhost:8000/random-key this url points to http://example.com/ultra-long-url-with-more-data-xxx
    - Input: `{url: http://example.com/ultra-long-url-with-more-data-xxx}`
    - Output: `{shortUrl: http://localhost:8000/random-key}`

1. Redirect url endpoint: `/<key>`
    - e.g. the `http://localhost:8000/random-key` should be redirected to the original url e.g. `http://example.com/ultra-long-url-with-more-data-xxx`.
    - Note: every time we visit a short url, the url `views` should increase.

1. Detail url endpoint: `/<key>/detail`
    - It should return the details of the short url.
    - e.g. `{url: http://example.com/ultra-long-url-with-more-data-xxx, views: 100}`. 

> **Note:** Work on the `views.py` there will be more instruction and you can also check `tests.py` for hints.

## Tests

- Run `pytest .`, the goal is to make all tests passed.
