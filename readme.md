# Coding exercise: URL shortener

## Installation and preparation

- Create a virtualenv `python -m venv`.
- Activate the virtualenv `source venv/bin/activate`.
- Install dependenciies `pip install -r requirements.txt`.
- Initiate db migration `python manage.py migrate`.

> **Note:** This program doesn't need to run the server, we will rely on unit tests to check working api endpoints.

## Instruction

This template already provides the endpoints necessary for the url shortener app. There are 3 endpoints:

- The `/create` for creating shorturl.
- The `/<key>` for redirecting shorturl.
- The `/<key>/detail` for getting shorturl information.

The views for the following endpoints resides on `views.py`. The `url_create_view`, `url_redirect_view`, and `url_detail_view`. These views are empty and have no logic.

What we need to do is to add logic into this view to achieve the following endpoint results:

- For `/create` endpoint:
    - It should accept a `url` payload and return shortUrl in `JSON` format. e.g.:
        - Input:
            ```
            { url: "http://example.com/ultra-very-long-descriptive-url" }
            ```
        - Output: 
            ```
            { shortUrl: "http://localhost:8000/<key>" }
            ```
            or 

            ```
            { shortUrl: "http://localhost:8000/TkAIbLPWrQ" }
            ```

    - The `<key>` should be a random 10-char length safe-url string. It can be any characters as long as it is url safe.
    - The data should be stored on `Url` model on `models.py`.
        - Where the `url` field is the original url.
        - The `key` is the unique shorturl identifer for the long `url`.

- For `/<key>` endpoint:
    - Accesing this url will redirect you to the original url.
    - Everytime we visit the short url, increase the number of views of the url.

- For `/<key>/details`:
    - It should return the details of the short url e.g.:
        ```
        {url: http://example.com/ultra-long-url-with-more-data-xxx, views: 100}
        ```

> **Note:** Work on the `views.py` there will be more instructions and you can also check `tests.py` for hints.

## Tests

- Run `pytest .`, the goal is to make all tests passed.
