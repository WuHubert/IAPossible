from flask import Flask
from routes.config import API_CONFIG
from routes._init_ import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)