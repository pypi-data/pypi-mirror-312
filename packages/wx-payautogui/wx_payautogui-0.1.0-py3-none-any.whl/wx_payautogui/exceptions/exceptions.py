class WeChatBotError(Exception):
    """微信机器人操作异常"""
    pass

class ImageNotFoundError(WeChatBotError):
    """图像未找到异常"""
    pass

class OperationTimeoutError(WeChatBotError):
    """操作超时异常"""
    pass 