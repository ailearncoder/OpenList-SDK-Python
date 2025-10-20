"""驱动管理API。

提供驱动（Driver）配置模板的查询功能。
驱动用于定义不同存储服务的连接和配置方式。
"""
from typing import List, Any, Dict
from ..client import BaseClient


class DriverAPI:
    """驱动管理API类。
    
    封装了所有驱动管理相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化驱动管理API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def list(self) -> Dict[str, Any]:
        """查询所有驱动配置模板列表。
        
        Returns:
            Dict[str, Any]: 包含所有驱动配置模板的字典
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> driver_api = DriverAPI(client)
            >>> response = driver_api.list()
            >>> print(response['code'])
            200
            >>> for driver_name in response['data'].keys():
            ...     print(driver_name)
            '115 Cloud'
            'Local'
        
        Note:
            - 此API需要管理员权限
            - 返回所有可用驱动的配置模板
        """
        response_data = self.client.get("/api/admin/driver/list")
        return response_data
    
    def names(self) -> List[str]:
        """列出所有驱动名称列表。
        
        Returns:
            List[str]: 驱动名称列表
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> driver_api = DriverAPI(client)
            >>> names = driver_api.names()
            >>> print(names)
            ['Local', '115 Cloud', 'Aliyundrive', ...]
        """
        response_data = self.client.get("/api/admin/driver/names")
        return response_data.get("data", [])
    
    def info(self, driver: str) -> Dict[str, Any]:
        """获取特定驱动的详细信息。
        
        Args:
            driver: 驱动名称
            
        Returns:
            Dict[str, Any]: 包含驱动配置信息的字典
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 驱动不存在
            NetworkError: 网络错误
            
        Example:
            >>> driver_api = DriverAPI(client)
            >>> info = driver_api.info("Local")
            >>> print(info['data']['config']['name'])
            'Local'
            >>> for field in info['data']['additional']:
            ...     print(f"{field['name']}: {field['type']}")
        
        Note:
            返回的数据包含common（通用配置）、additional（额外配置）和config（驱动配置）三部分。
        """
        params = {"driver": driver}
        response_data = self.client.get("/api/admin/driver/info", params=params)
        return response_data
