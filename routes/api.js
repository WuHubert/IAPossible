const express = require('express');
const router = express.Router();
const imageController = require('../controllers/imagecontroller.js/index.js');
const rateLimiter = require('../middleware/rateLimiter.js');

// 圖片生成路由
router.post('/generate-image', rateLimiter, imageController.generateImage);

// 獲取歷史記錄
router.get('/history', imageController.getHistory);

// 保存圖片
router.post('/save-image', imageController.saveImage);

// 刪除歷史記錄
router.delete('/history/:id', imageController.deleteHistory);

module.exports = router;