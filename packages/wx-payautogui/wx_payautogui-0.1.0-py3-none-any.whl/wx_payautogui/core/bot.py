import os
from ..utils.image_utils import ImageUtils
from ..utils.logger import Logger
from ..exceptions.exceptions import WeChatBotError
import pyautogui
import pyperclip
import time
import subprocess
import platform

class WeChatBot:
    def __init__(self, config=None):
        self.config = config or {}
        self.image_utils = ImageUtils()
        self.logger = Logger(name='WeChatBot')
        
        # 设置资源目录
        self.resource_dir = self.config.get('resource_dir')
        if not self.resource_dir:
            # 如果未指定，使用默认路径（相对于bot.py的位置）
            self.resource_dir = os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'resources'
            ))
        else:
            # 如果指定了路径，转换为绝对路径
            self.resource_dir = os.path.abspath(self.resource_dir)
        
        self.logger.info(f"使用资源目录: {self.resource_dir}")
        self._init_wechat()
        
    def _init_wechat(self):
        """初始化微信：启动并全屏微信窗口"""
        try:
            self.logger.info("开始初始化微信...")
            
            # 保存调试截图
            debug_dir = os.path.join(self.resource_dir, 'debug')
            if not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
            
            debug_screenshot = os.path.join(debug_dir, 'debug_screenshot.png')
            self.image_utils.take_screenshot(debug_screenshot)
            self.logger.info(f"已保存调试截图: {debug_screenshot}")
            
            # 检查资源目录是否存在
            if not os.path.exists(self.resource_dir):
                raise WeChatBotError(f"资源目录不存在: {self.resource_dir}")
            
            # 检查必要的资源文件
            required_resources = [
                os.path.join(self.resource_dir, 'base/wechat_window.png'),
                os.path.join(self.resource_dir, 'base/wechat_icon.png')
            ]
            
            for resource in required_resources:
                if not os.path.exists(resource):
                    raise WeChatBotError(f"缺少必要的资源文件: {resource}")
            
            # 检查微信是否已运行
            if not self._is_wechat_running():
                self.logger.info("微信未运行，正在启动...")
                self._start_wechat()
                time.sleep(2)  # 等微信启动
            else:
                self.logger.info("微信已在运行")
            
            # 查找并激活微信窗口
            self.logger.debug("查找微信窗口...")
            window_location = self._find_wechat_window()
            if not window_location:
                raise WeChatBotError("未找到微信窗口")
            
            # 全屏显示
            self.logger.debug("最大化微信窗口...")
            self._maximize_window()
            time.sleep(1)  # 等待窗口调整完成
            
            self.logger.info("微信初始化完成")
            
        except Exception as e:
            self.logger.error(f"初始化微信失败: {str(e)}")
            raise WeChatBotError(f"初始化微信失败: {str(e)}")
    
    def _is_wechat_running(self):
        """检查微信是否在运行"""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                # 使用AppleScript检查微信是否运行
                apple_script = '''
                    tell application "System Events"
                        return (exists process "WeChat")
                    end tell
                '''
                result = subprocess.run(
                    ['osascript', '-e', apple_script],
                    capture_output=True,
                    text=True
                )
                return result.stdout.strip().lower() == 'true'
                
            elif system == "Windows":
                import win32gui
                return bool(win32gui.FindWindow("WeChatMainWndForPC", None))
                
            else:  # Linux
                # 使用pgrep检查进程
                result = subprocess.run(
                    ['pgrep', '-f', 'WeChat'],
                    capture_output=True
                )
                return result.returncode == 0
                
        except Exception as e:
            self.logger.error(f"检查微信运行状态失败: {str(e)}")
            return False
    
    def _start_wechat(self):
        """启动微信客户端"""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                # 使用AppleScript启动微信
                apple_script = '''
                    tell application "WeChat"
                        activate
                    end tell
                '''
                subprocess.run(['osascript', '-e', apple_script])
                self.logger.info("通过AppleScript启动微信")
                
            elif system == "Windows":
                # Windows下查找微信安装路径
                possible_paths = [
                    r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
                    r"C:\Program Files\Tencent\WeChat\WeChat.exe",
                    os.path.expanduser("~\\AppData\\Local\\Tencent\\WeChat\\WeChat.exe")
                ]
                
                wechat_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        wechat_path = path
                        break
                        
                if wechat_path:
                    subprocess.Popen(wechat_path)
                    self.logger.info(f"通过路径启动微信: {wechat_path}")
                else:
                    # 如果找不到安装路径，尝试使用命令启动
                    subprocess.Popen("start WeChat:", shell=True)
                    self.logger.info("通过命令启动微信")
                    
            else:  # Linux
                # 在Linux下尝试多种可能的命令
                commands = ["wechat", "WeChat", "wechat-uos"]
                launched = False
                
                for cmd in commands:
                    try:
                        subprocess.Popen(cmd)
                        launched = True
                        self.logger.info(f"通过命令启动微信: {cmd}")
                        break
                    except:
                        continue
                        
                if not launched:
                    raise WeChatBotError("未能找到可用的微信启动命令")
                    
            # 等待微信启动
            max_wait = 30  # 最长等待30秒
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                if self._is_wechat_running():
                    self.logger.info("微信已成功启动")
                    time.sleep(2)  # 额外等待一下界面加载
                    return
                time.sleep(1)
                
            raise WeChatBotError("微信启动超时")
            
        except Exception as e:
            raise WeChatBotError(f"启动微信失败: {str(e)}")
    
    def _find_wechat_window(self):
        """查找微信窗口"""
        try:
            # 首先尝试使用主窗口图标
            window_icon = os.path.join(self.resource_dir, 'base/wechat_icon.png')
            location = self.image_utils.locate_on_screen(window_icon, confidence=0.8)
            
            if not location:
                # 如果找不到图标，尝试使用窗口特征图
                window_feature = os.path.join(self.resource_dir, 'base/wechat_window.png')
                location = self.image_utils.locate_on_screen(window_feature, confidence=0.8)
            
            return location
            
        except Exception as e:
            self.logger.error(f"查找微信窗口失败: {str(e)}")
            return None
    
    def _maximize_window(self):
        """最大化窗口"""
        system = platform.system()
        try:
            if system == "Windows":
                import win32gui
                import win32con
                hwnd = win32gui.FindWindow("WeChatMainWndForPC", None)
                if hwnd:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            else:
                # 对于macOS和Linux，使用pyautogui模拟按键
                pyautogui.hotkey('command' if system == 'Darwin' else 'win', 'up')
                
        except Exception as e:
            raise WeChatBotError(f"最大化窗口失败: {str(e)}")
    
    def send_message(self, target, message, is_group=False):
        """
        发送消息到指定目标
        
        流程：
        1. 激活微信窗口并置顶
        2. 点击窗口确保焦点
        3. Ctrl+F 打开搜索
        4. 输入联系人名称并回车进入聊天
        5. 输入消息并回车发送
        """
        try:
            self.logger.info(f"准备发送消息到: {target}")
            
            # 1. 激活微信窗口并置顶
            system = platform.system()
            if system == "Darwin":  # macOS
                apple_script = '''
                    tell application "WeChat"
                        activate
                        set frontmost to true
                        delay 0.5
                    end tell
                '''
                subprocess.run(['osascript', '-e', apple_script])
            else:  # Windows/Linux
                # 使用Alt+Tab切换到微信
                pyautogui.keyDown('alt')
                time.sleep(0.1)
                pyautogui.press('tab')
                time.sleep(0.1)
                pyautogui.keyUp('alt')
            
            time.sleep(1)  # 等待窗口完全激活
            
            # 2. 点击窗口中心位置确保焦点
            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width // 2, screen_height // 2)
            time.sleep(0.5)
            
            # 按ESC键清除可能的搜索状态
            pyautogui.press('esc')
            time.sleep(0.2)
            
            # 3. Ctrl+F 打开搜索
            for _ in range(2):  # 尝试两次，以防第一次不成功
                pyautogui.hotkey('command' if system == 'Darwin' else 'ctrl', 'f')
                time.sleep(0.3)
            
            # 4. 输入联系人名称并回车进入聊天
            pyautogui.write(target, interval=0.1)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # 5. 输入消息并回车发送
            pyautogui.write(message, interval=0.1)
            pyautogui.press('enter')
            
            self.logger.info(f"消息已发送: {message[:20]}...")
            time.sleep(0.5)
            
        except Exception as e:
            self.logger.error(f"发送消息失败: {str(e)}")
            raise WeChatBotError(f"发送消息失败: {str(e)}")
    
    def _open_wechat(self):
        """使用快捷键打开微信"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                apple_script = '''
                    tell application "WeChat"
                        activate
                    end tell
                '''
                subprocess.run(['osascript', '-e', apple_script])
            else:  # Windows/Linux
                pyautogui.hotkey('ctrl', 'alt', 'w')
            
            time.sleep(1)
            self.logger.info("已打开微信窗口")
            
        except Exception as e:
            self.logger.error(f"打开微信失败: {str(e)}")
            raise WeChatBotError(f"打开微信失败: {str(e)}")
    
    def _find_contact(self, contact_name):
        """查找并选择联系人"""
        try:
            # 1. 打开搜索
            system = platform.system()
            pyautogui.hotkey('command' if system == 'Darwin' else 'ctrl', 'f')
            time.sleep(0.5)
            
            # 2. 输入联系人名称
            pyautogui.write(contact_name, interval=0.1)
            time.sleep(1)
            
            # 3. 选择联系人
            pyautogui.press('enter')
            time.sleep(0.5)
            
            self.logger.info(f"已选择联系人: {contact_name}")
            
        except Exception as e:
            self.logger.error(f"查找联系人失败: {str(e)}")
            raise WeChatBotError(f"查找联系人失败: {str(e)}")
    
    def _send_text(self, text):
        """发送文本消息"""
        try:
            # 1. 输入消息内容
            if any(ord(c) > 127 for c in text):  # 如果包含中文字符
                pyperclip.copy(text)
                system = platform.system()
                pyautogui.hotkey('command' if system == 'Darwin' else 'ctrl', 'v')
            else:
                pyautogui.write(text, interval=0.1)
            time.sleep(0.5)
            
            # 2. 发送消息
            pyautogui.press('enter')
            time.sleep(0.5)
            
            self.logger.info("消息已发送")
            
        except Exception as e:
            self.logger.error(f"发送文本失败: {str(e)}")
            raise WeChatBotError(f"发送文本失败: {str(e)}")
    
    def _activate_window(self):
        """激活微信窗口"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                apple_script = '''
                    tell application "WeChat"
                        activate
                        set frontmost to true
                    end tell
                '''
                subprocess.run(['osascript', '-e', apple_script])
            else:  # Windows/Linux
                # 使用快捷键打开微信
                pyautogui.hotkey('ctrl', 'alt', 'w')
                
            time.sleep(1)  # 等待窗口激活
            self.logger.info("已激活微信窗口")
            
        except Exception as e:
            self.logger.error(f"激活窗口失败: {str(e)}")
            raise WeChatBotError(f"激活窗口失败: {str(e)}")
    
    def _clear_search(self):
        """清除搜索框内容"""
        try:
            # 按ESC键退出搜索状态
            pyautogui.press('esc')
            time.sleep(0.2)
            pyautogui.press('esc')  # 再按一次以确保
            time.sleep(0.2)
        except Exception as e:
            self.logger.warning(f"清除搜索状态失败: {str(e)}")
    
    def add_friend(self, wxid, message=""):
        """
        添加好友
        
        Args:
            wxid (str): 要添加的微信ID
            message (str): 验证消息
        """
        try:
            # 1. 激活窗口
            self._activate_window()
            time.sleep(1)
            
            # 2. 打开添加好友界面
            system = platform.system()
            pyautogui.hotkey('command' if system == 'Darwin' else 'ctrl', 'shift', 'f')
            time.sleep(1)
            
            # 3. 输入微信ID
            pyautogui.write(wxid, interval=0.1)
            time.sleep(0.5)
            
            # 4. 点击搜索
            pyautogui.press('enter')
            time.sleep(1)
            
            # 5. 输入验证消息
            if message:
                if any(ord(c) > 127 for c in message):  # 检查是否包含非ASCII字符
                    pyperclip.copy(message)
                    pyautogui.hotkey('command' if system == 'Darwin' else 'ctrl', 'v')
                else:
                    pyautogui.write(message, interval=0.1)
                time.sleep(0.5)
            
            # 6. 发送请求
            pyautogui.press('enter')
            
            self.logger.info(f"已发送好友请求给: {wxid}")
            time.sleep(1)
            
        except Exception as e:
            self.logger.error(f"添加好友失败: {str(e)}")
            raise WeChatBotError(f"添加好友失败: {str(e)}")
    
    def invite_to_group(self, group_name, contact):
        """
        邀请联系人加入群聊
        
        Args:
            group_name (str): 群聊名称
            contact (str): 要邀请的联系人称
        """
        try:
            # TODO: 实现邀请联系人加入群聊的逻辑
            # 1. 定位并点击群聊
            # 2. 打开群聊设置
            # 3. 点击邀请按钮
            # 4. 搜索并选择联系人
            # 5. 确认邀请
            pass
        except Exception as e:
            raise WeChatBotError(f"邀请联系人加入群聊失败: {str(e)}")