import pyautogui
import cv2
import numpy as np
import os
from ..exceptions.exceptions import ImageNotFoundError

class ImageUtils:
    @staticmethod
    def locate_on_screen(image_path, confidence=0.9):
        """
        在屏幕上定位图像
        
        Args:
            image_path (str): 图像文件路径
            confidence (float): 匹配置信度
            
        Returns:
            tuple: 图像位置的坐标(x, y)
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                raise ImageNotFoundError(f"图像文件不存在: {image_path}")
                
            # 检查文件大小
            if os.path.getsize(image_path) == 0:
                raise ImageNotFoundError(f"图像文件为空: {image_path}")
                
            # 尝试读取图像
            try:
                cv2.imread(image_path)
            except Exception as e:
                raise ImageNotFoundError(f"图像文件无法读取: {image_path}, 错误: {str(e)}")
            
            # 在屏幕上查找图像
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=confidence
            )
            
            if location:
                center = pyautogui.center(location)
                return center
            return None
            
        except Exception as e:
            if isinstance(e, ImageNotFoundError):
                raise e
            raise ImageNotFoundError(f"定位图像失败: {str(e)}") 

    @staticmethod
    def take_screenshot(save_path):
        """
        截取屏幕截图用于调试
        
        Args:
            save_path (str): 保存路径
        """
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            return True
        except Exception as e:
            print(f"截图失败: {str(e)}")
            return False