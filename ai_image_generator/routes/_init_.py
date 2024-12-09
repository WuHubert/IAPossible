from flask import Flask
from dotenv import load_dotenv
from routes.image_routes import image_bp
import os

def create_app():
    load_dotenv()  # 加载 .env 文件
    
    app = Flask(__name__, 
                template_folder='../templates',  # 添加這行
                static_folder='../static')       # 添加這行
    
    # 加载配置
    app.config.from_object('config.Config')
    
    # 注册蓝图
    app.register_blueprint(image_bp)
    
    return app

