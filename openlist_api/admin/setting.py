"""设置管理API。

提供系统设置的查询和保存功能。
包括站点设置、样式设置、预览设置、全局设置等。
"""
from typing import List, Dict, Any, Optional
from ..client import BaseClient
from ..models import BaseResponse


class Setting(Dict[str, Any]):
    """设置项数据类型（继承自dict以保持灵活性）"""
    pass


class SettingAPI:
    """设置管理API类。
    
    封装了所有设置管理相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化设置管理API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def list(
        self,
        group: Optional[int] = None,
        groups: Optional[str] = None
    ) -> List[Setting]:
        """列出设置项。
        
        Args:
            group: 设置分组 (1=站点, 2=样式, 3=预览, 4=全局, 5=其它, 7=单点登录)
            groups: 多个分组，逗号分隔，例如 "5,0"
            
        Returns:
            List[Setting]: 设置项列表
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> settings = setting_api.list(group=1)  # 获取站点设置
            >>> for setting in settings:
            ...     print(f"{setting['key']}: {setting['value']}")
            'site_title: AList'
            'version: v3.25.1'
        
        Note:
            - group: 1=站点, 2=样式, 3=预览, 4=全局, 5=其它(aria2/令牌), 7=单点登录
            - flag: 0=公开, 1=私有, 2=只读, 3=弃用
        """
        params = {}
        if group is not None:
            params["group"] = str(group)
        if groups is not None:
            params["groups"] = groups
        
        response_data = self.client.get("/api/admin/setting/list", params=params)
        return response_data.get("data", [])
    
    def get(self, key: str) -> Optional[Setting]:
        """获取某项设置。
        
        Args:
            key: 设置键名
            
        Returns:
            Optional[Setting]: 设置项，如果不存在返回None
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> setting = setting_api.get("site_title")
            >>> print(setting)
            {'key': 'site_title', 'value': 'AList', ...}
        """
        params = {"key": key}
        response_data = self.client.get("/api/admin/setting/get", params=params)
        return response_data.get("data")
    
    def save(self, settings: List[Dict[str, Any]]) -> BaseResponse:
        """保存设置。
        
        Args:
            settings: 设置列表，每个设置包含key、value等字段
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> settings = [
            ...     {"key": "site_title", "value": "My AList"},
            ...     {"key": "announcement", "value": "Welcome!"}
            ... ]
            >>> response = setting_api.save(settings)
            >>> print(response.message)
            'success'
        
        Note:
            - 只需要提供key和value字段即可
            - 其他字段（help、type等）可选
        """
        response_data = self.client.post("/api/admin/setting/save", json=settings)
        return BaseResponse(**response_data)
    
    def delete(self, key: str) -> BaseResponse:
        """删除设置。
        
        仅用于删除已弃用的设置项。
        
        Args:
            key: 设置键名
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> response = setting_api.delete("deprecated_key")
            >>> print(response.message)
            'success'
        
        Warning:
            仅用于弃用的设置项，不要删除正在使用的设置。
        """
        params = {"key": key}
        response_data = self.client.post("/api/admin/setting/delete", params=params)
        return BaseResponse(**response_data)
    
    def reset_token(self) -> BaseResponse:
        """重置永久令牌。
        
        生成新的永久令牌。
        
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> response = setting_api.reset_token()
            >>> print(response.message)
            'success'
        
        Warning:
            重置后旧的永久令牌将失效。
        """
        response_data = self.client.post("/api/admin/setting/reset_token")
        return BaseResponse(**response_data)
    
    def set_aria2(
        self,
        uri: str,
        secret: str = ""
    ) -> BaseResponse:
        """设置aria2配置。
        
        Args:
            uri: aria2 RPC地址
            secret: aria2密钥
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> response = setting_api.set_aria2(
            ...     uri="http://localhost:6800/jsonrpc",
            ...     secret="my_secret"
            ... )
            >>> print(response.message)
            'success'
        """
        payload = {
            "uri": uri,
            "secret": secret,
        }
        response_data = self.client.post("/api/admin/setting/set_aria2", json=payload)
        return BaseResponse(**response_data)
    
    def set_qbittorrent(
        self,
        url: str,
        seedtime: int = 0
    ) -> BaseResponse:
        """设置qBittorrent配置。
        
        Args:
            url: qBittorrent WebUI地址（包含用户名密码）
            seedtime: 做种时间（分钟）
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> setting_api = SettingAPI(client)
            >>> response = setting_api.set_qbittorrent(
            ...     url="http://admin:pass@localhost:8080/",
            ...     seedtime=60
            ... )
            >>> print(response.message)
            'success'
        
        Note:
            URL格式: http://username:password@host:port/
        """
        payload = {
            "url": url,
            "seedtime": seedtime,
        }
        response_data = self.client.post("/api/admin/setting/set_qbit", json=payload)
        return BaseResponse(**response_data)
