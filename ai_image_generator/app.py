from flask import Flask
from routes.config import API_CONFIG
from routes.image_routes import image_bp
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
app.register_blueprint(image_bp, url_prefix='/image')

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)