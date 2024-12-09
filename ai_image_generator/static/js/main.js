const { createApp } = Vue

createApp({
    data() {
        return {
            prompt: '',
            images: [],
            isGenerating: false,
            notification: {
                show: false,
                message: '',
                type: 'success'
            }
        }
    },
    methods: {
        async generateImage() {
            if (!this.prompt.trim()) {
                this.showNotification('請輸入圖片描述', 'error');
                return;
            }

            this.isGenerating = true;
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: this.prompt })
                });

                const data = await response.json();
                if (data.status === 'success') {
                    this.images.unshift(data.data);
                    this.prompt = '';
                    this.showNotification('圖片生成成功！', 'success');
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                this.showNotification(`生成失敗: ${error.message}`, 'error');
            } finally {
                this.isGenerating = false;
            }
        },

        async deleteImage(imageId) {
            try {
                const response = await fetch(`/api/images/${imageId}`, {
                    method: 'DELETE'
                });

                const data = await response.json();
                if (data.status === 'success') {
                    this.images = this.images.filter(img => img.id !== imageId);
                    this.showNotification('圖片已刪除', 'success');
                }
            } catch (error) {
                this.showNotification('刪除失敗', 'error');
            }
        },

        async loadImages() {
            try {
                const response = await fetch('/api/images');
                const data = await response.json();
                if (data.status === 'success') {
                    this.images = data.data;
                }
            } catch (error) {
                this.showNotification('載入圖片失敗', 'error');
            }
        },

        formatDate(dateString) {
            return new Date(dateString).toLocaleString('zh-TW');
        },

        showNotification(message, type = 'success') {
            this.notification = {
                show: true,
                message,
                type
            };
            setTimeout(() => {
                this.notification.show = false;
            }, 3000);
        }
    },
    mounted() {
        this.loadImages();
    }
}).mount('#app')