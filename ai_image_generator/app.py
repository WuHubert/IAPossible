from flask import Flask
from routes.config import API_CONFIG
from routes.image_routes import image_bp

app = Flask(__name__)
app.register_blueprint(image_bp)

if __name__ == '__main__':
    app.run(debug=True)
else:
    # 确保 Gunicorn 可以访问到 app 变量
    application = app