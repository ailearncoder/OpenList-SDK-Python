"""
OpenList API - Python客户端库

一个用于与OpenList (AList) API交互的Python客户端库。
提供了完整的类型提示和文档字符串支持。

基本用法:
    >>> from openlist_api import OpenListClient
    >>> client = OpenListClient("http://your-server.com")
    >>> # 登录
    >>> response = client.auth.login("username", "password")
    >>> client.set_token(response.data.token)
    >>> # 列出文件
    >>> files = client.fs.list("/")
    >>> for item in files.data.content:
    ...     print(item.name)
"""
from typing import Optional
from .client import BaseClient
from .auth import AuthAPI
from .fs import FileSystemAPI
from .public import PublicAPI
from .admin.meta import MetaAPI
from .admin.user import UserAPI
from .admin.storage import StorageAPI
from .admin.driver import DriverAPI
from .admin.setting import SettingAPI
from .admin.task import TaskAPI
from .exceptions import (
    OpenListAPIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    NetworkError,
    ServerError,
)

__version__ = "1.0.0"
__all__ = [
    "OpenListClient",
    "BaseClient",
    "OpenListAPIError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "NetworkError",
    "ServerError",
]


class OpenListClient:
    """
    OpenList API主客户端类。
    
    这是与OpenList API交互的主要入口点。提供对所有API模块的访问。
    
    Attributes:
        auth: 认证相关API
        fs: 文件系统相关API
        public: 公共API
        admin: 管理员API
            - meta: 元信息管理
            - user: 用户管理
            - storage: 存储管理
            - driver: 驱动管理
            - setting: 设置管理
            - task: 任务管理
        
    Example:
        >>> client = OpenListClient("http://localhost:5244")
        >>> # 登录
        >>> login_resp = client.auth.login("admin", "password")
        >>> client.set_token(login_resp.data.token)
        >>> # 使用文件系统API
        >>> files = client.fs.list("/")
        >>> # 使用管理员API
        >>> users = client.admin.user.list()
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        初始化OpenList客户端。
        
        Args:
            base_url: API基础URL，例如 "http://localhost:5244"
            timeout: 请求超时时间（秒），默认30秒
        """
        self._client = BaseClient(base_url=base_url, timeout=timeout)
        
        # 公共API
        self.auth = AuthAPI(self._client)
        self.fs = FileSystemAPI(self._client)
        self.public = PublicAPI(self._client)
        
        # 管理员API - 使用命名空间对象
        class AdminNamespace:
            """管理员API命名空间。"""
            def __init__(self, client: BaseClient):
                self.meta = MetaAPI(client)
                self.user = UserAPI(client)
                self.storage = StorageAPI(client)
                self.driver = DriverAPI(client)
                self.setting = SettingAPI(client)
                self.task = TaskAPI(client)
        
        self.admin = AdminNamespace(self._client)
    
    def set_token(self, token: str) -> None:
        """
        设置认证token。
        
        Args:
            token: JWT token字符串
        """
        self._client.set_token(token)
    
    @property
    def token(self) -> Optional[str]:
        """
        获取当前token。
        
        Returns:
            当前的JWT token，如果未设置则为None
        """
        return self._client.token
