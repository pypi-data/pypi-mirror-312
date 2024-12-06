# flask-notion-database

notion-database flask extension

The flask-notion-database is a Flask extension that allows you to manage routes within your Flask application. 

## Installation

To install the Flask notion-database extension, you can use pip:

```bash
pip install flask-notion-database
```

## Usage

First, import the `NotiondatabaseExtension` from the `flask-notion-database` package:

Then, create an instance of the `NotiondatabaseExtension` and initialize it with your Flask application:

```python
from flask import Flask
from flask_notion_database import NotionDatabaseExtension

NDE = NotionDatabaseExtension()
app = Flask(__name__)
NDE.init_app(app)
```

Now, you can use the notion-database features in your Flask routes.

## Example

run the example.py file to see how the extension works.

http://127.0.0.1:8888/apidocs/#/ will show the swagger documentation of the api.

## License

This project is licensed under the terms of the LGPL license.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.