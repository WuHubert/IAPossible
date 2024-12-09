import time
import threading
from queue import Queue, Empty
from datetime import datetime, timedelta

class TokenBucket:
    def __init__(self, tokens_per_second, burst_size):
        self.tokens_per_second = tokens_per_second
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = time.time()
        self.lock = threading.Lock()

    def get_token(self, timeout=None):
        """嘗試獲取令牌"""
        start_time = time.time()
        
        while True:
            with self.lock:
                now = time.time()
                # 計算應該添加的令牌
                time_passed = now - self.last_update
                new_tokens = time_passed * self.tokens_per_second
                self.tokens = min(self.burst_size, self.tokens + new_tokens)
                self.last_update = now

                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                
                if timeout is not None:
                    if time.time() - start_time >= timeout:
                        return False
                    
            # 等待一小段時間後重試
            time.sleep(0.1)

class RateLimiter:
    def __init__(self):
        # 每分鐘最多10個請求
        self.token_bucket = TokenBucket(tokens_per_second=10/60, burst_size=10)
        # 記錄每個IP的請求歷史
        self.ip_history = {}
        self.history_lock = threading.Lock()

    def can_process_request(self, ip_address, timeout=5):
        """檢查是否可以處理請求"""
        # 檢查IP的請求歷史
        with self.history_lock:
            now = datetime.now()
            if ip_address in self.ip_history:
                # 清理舊的請求記錄
                self.ip_history[ip_address] = [
                    time for time in self.ip_history[ip_address]
                    if now - time < timedelta(hours=1)
                ]
                # 檢查最近一小時的請求數
                if len(self.ip_history[ip_address]) >= 50:  # 每小時最多50個請求
                    return False, "已超過每小時請求限制"
            else:
                self.ip_history[ip_address] = []

            # 嘗試獲取令牌
            if not self.token_bucket.get_token(timeout):
                return False, "服務器繁忙，請稍後再試"

            # 記錄這次請求
            self.ip_history[ip_address].append(now)
            return True, None 