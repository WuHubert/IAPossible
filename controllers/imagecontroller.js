const config = require('../config/config');
const axios = require('axios');

class ImageController {
    async generateImage(req, res, next) {
        try {
            const { prompt } = req.body;

            if (!prompt) {
                return res.status(400).json({ error: '請提供圖片描述' });
            }

            const response = await axios.post('https://api.openai.com/v1/images/generations', {
                prompt,
                n: 1,
                size: "1024x1024"
            }, {
                headers: {
                    'Authorization': `Bearer ${config.OPENAI_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            });

            res.json(response.data);
        } catch (error) {
            next(error);
        }
    }

    async getHistory(req, res, next) {
        try {
            // 這裡應該實現從數據庫獲取歷史記錄的邏輯
            // 目前返回模擬數據
            const history = [
                // ... 歷史記錄數據
            ];
            res.json(history);
        } catch (error) {
            next(error);
        }
    }

    async saveImage(req, res, next) {
        try {
            const { prompt, imageUrl } = req.body;
            // 實現保存圖片到數據庫的邏輯
            res.json({ success: true, message: '圖片已保存' });
        } catch (error) {
            next(error);
        }
    }

    async deleteHistory(req, res, next) {
        try {
            const { id } = req.params;
            // 實現刪除歷史記錄的邏輯
            res.json({ success: true, message: '記錄已刪除' });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new ImageController();