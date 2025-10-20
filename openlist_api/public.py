"""公共API。

提供无需认证的公共接口，如站点设置、ping检测等。
"""
from .client import BaseClient
from .models import SiteSettingsResponse


class PublicAPI:
    """公共API类。
    
    封装了所有公共接口操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化公共API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def get_settings(self) -> SiteSettingsResponse:
        """获取站点设置。
        
        获取当前站点的公共设置信息，包括站点标题、logo、主题颜色等。
        
        Returns:
            SiteSettingsResponse: 包含站点设置的响应对象
            
        Raises:
            NetworkError: 网络连接错误
            
        Example:
            >>> public_api = PublicAPI(client)
            >>> response = public_api.get_settings()
            >>> print(response.data.site_title)
            'AList'
            >>> print(response.data.version)
            'v3.25.1'
            >>> print(response.data.logo)
            'https://cdn.jsdelivr.net/gh/alist-org/logo@main/logo.svg'
        
        Note:
            此API不需要认证，可以公开访问。
        """
        response_data = self.client.get("/api/public/settings")
        return SiteSettingsResponse(**response_data)
    
    def ping(self) -> str:
        """进行ping检测。
        
        检测服务器连通性。
        
        Returns:
            str: 响应字符串，正常为"pong"
            
        Raises:
            NetworkError: 网络连接错误或服务器不可达
            
        Example:
            >>> public_api = PublicAPI(client)
            >>> result = public_api.ping()
            >>> print(result)
            'pong'
        
        Note:
            - 此API不需要认证
            - 可用于健康检查和连通性测试
        """
        response_data = self.client.get("/ping")
        return response_data
