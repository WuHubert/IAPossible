import os

class Config:
    # 數據庫配置
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上傳配置
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    
 