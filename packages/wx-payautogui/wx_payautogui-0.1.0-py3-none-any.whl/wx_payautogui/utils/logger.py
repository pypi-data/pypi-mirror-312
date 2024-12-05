import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name='wx_payautogui'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 创建logs目录
        self.logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'logs'
        )
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
            
        # 日志文件名格式：logs/wx_payautogui_2024-03-21.log
        log_file = os.path.join(
            self.logs_dir,
            f'wx_payautogui_{datetime.now().strftime("%Y-%m-%d")}.log'
        )
        
        # 文件处理器
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 清除已存在的处理器
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def debug(self, message):
        self.logger.debug(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def critical(self, message):
        self.logger.critical(message) 