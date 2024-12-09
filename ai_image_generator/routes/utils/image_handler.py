import os
import base64
from datetime import datetime

class ImageHandler:
    def save_base64_image(self, base64_data, save_dir):
        """保存 base64 格式的圖片"""
        os.makedirs(save_dir, exist_ok=True)
        filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(save_dir, filename)
        
        image_bytes = base64.b64decode(base64_data)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
            
        return filename 