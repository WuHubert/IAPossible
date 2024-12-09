from flask import Blueprint, request, jsonify, render_template
import requests
from PIL import Image
import os
from datetime import datetime
import base64
from io import BytesIO
from .utils.image_handler import ImageHandler
from .config import API_CONFIG

# 創建 Blueprint
image_bp = Blueprint('image', __name__)

class ImageGenerator:
    def __init__(self):
        self.api_url = API_CONFIG['URL']
        self.headers = {"Authorization": f"Bearer {API_CONFIG['TOKEN']}"}
        self.image_handler = ImageHandler()

    def generate(self, prompt):
        """調用 API 生成圖片"""
        response = requests.post(
            self.api_url, 
            headers=self.headers, 
            json={"inputs": prompt}
        )
        return response.content

@image_bp.route('/')
def index():
    """渲染主頁"""
    return render_template('index.html')

@image_bp.route('/api/generate', methods=['POST'])
def generate_image():
    """生成圖片的 API 端點"""
    try:
        generator = ImageGenerator()
        data = request.json
        prompt = data.get('prompt', "Astronaut riding a horse")
        
        # 生成圖片
        image_bytes = generator.generate(prompt)
        
        # 轉換為 base64
        image = Image.open(BytesIO(image_bytes))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'image': f"data:image/png;base64,{base64_image}",
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@image_bp.route('/api/save', methods=['POST'])
def save_image():
    """保存生成的圖片"""
    try:
        handler = ImageHandler()
        data = request.json
        image_data = data.get('image').split(',')[1]
        
        # 保存圖片
        filename = handler.save_base64_image(
            image_data,
            save_dir='static/generated'
        )
            
        return jsonify({
            'success': True,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 