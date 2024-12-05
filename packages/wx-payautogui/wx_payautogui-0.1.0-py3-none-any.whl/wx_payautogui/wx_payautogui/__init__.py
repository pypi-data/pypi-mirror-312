from .core.bot import WeChatBot
from .core.daemon import BotDaemon
from .exceptions.errors import (
    WeChatBotError,
    AccountError,
    RiskControlError,
    OperationError
)

__version__ = "0.1.0"
__title__ = "wx-pyautogui"

__all__ = [
    'WeChatBot',
    'BotDaemon',
    'WeChatBotError',
    'AccountError',
    'RiskControlError',
    'OperationError'
] 