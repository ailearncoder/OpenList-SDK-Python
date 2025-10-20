"""自定义异常类模块。

定义了openlist_api库中使用的所有自定义异常。
"""
from typing import Optional


class OpenListAPIError(Exception):
    """OpenList API基础异常类。
    
    所有openlist_api相关异常的基类。
    
    Attributes:
        message: 错误消息
        status_code: HTTP状态码（可选）
        response: 原始响应对象（可选）
    """
    
    def __init__(self, message: str, status_code: Optional[int] = None, response=None):
        """初始化异常。
        
        Args:
            message: 错误消息
            status_code: HTTP状态码
            response: 原始响应对象
        """
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(OpenListAPIError):
    """认证失败异常。
    
    当API认证失败时抛出（如token无效、用户名密码错误等）。
    """
    pass


class AuthorizationError(OpenListAPIError):
    """授权失败异常。
    
    当用户没有权限访问特定资源时抛出。
    """
    pass


class NotFoundError(OpenListAPIError):
    """资源不存在异常。
    
    当请求的资源不存在时抛出（HTTP 404）。
    """
    pass


class ValidationError(OpenListAPIError):
    """请求参数验证失败异常。
    
    当请求参数不符合API要求时抛出。
    """
    pass


class NetworkError(OpenListAPIError):
    """网络连接异常。
    
    当网络请求失败时抛出（如超时、连接失败等）。
    """
    pass


class ServerError(OpenListAPIError):
    """服务器错误异常。
    
    当服务器返回5xx错误时抛出。
    """
    pass
