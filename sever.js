const express = require('express');
const path = require('path');
const cors = require('cors');
const errorHandler = require('./middleware/errorhandler');
const apiRoutes = require('./routes/api');

const app = express();
const PORT = process.env.PORT || 3000;

// 中間件
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// 路由
app.use('/api', apiRoutes);

// 錯誤處理
app.use(errorHandler);

// 處理 SPA 路由
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`服務器運行在 http://localhost:${PORT}`);
});