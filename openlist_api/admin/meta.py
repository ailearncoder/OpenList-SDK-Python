"""元信息管理API。

提供元信息（Meta）的创建、查询、更新和删除功能。
元信息用于配置目录的密码、写入权限、隐藏规则和README等属性。
"""
from typing import Optional
from ..client import BaseClient
from ..models import MetaListResponse, MetaResponse, BaseResponse, MetaInfo


class MetaAPI:
    """元信息管理API类。
    
    封装了所有元信息管理相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化元信息管理API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def list(
        self,
        page: int = 1,
        per_page: int = 0
    ) -> MetaListResponse:
        """列出所有元信息。
        
        Args:
            page: 页码，从1开始
            per_page: 每页数量，0表示不分页
            
        Returns:
            MetaListResponse: 包含元信息列表的响应对象
            
        Raises:
            AuthenticationError: 未认证或token无效
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> meta_api = MetaAPI(client)
            >>> response = meta_api.list()
            >>> for meta in response.data.content:
            ...     print(f"Path: {meta.path}, Password: {meta.password}")
            'Path: /a, Password: ***'
        
        Note:
            此API需要管理员权限。
        """
        params = {}
        if page:
            params["page"] = str(page)
        if per_page:
            params["per_page"] = str(per_page)
        
        response_data = self.client.get("/api/admin/meta/list", params=params)
        return MetaListResponse(**response_data)
    
    def get(self, meta_id: int) -> MetaResponse:
        """获取指定元信息。
        
        Args:
            meta_id: 元信息ID
            
        Returns:
            MetaResponse: 包含元信息详情的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 元信息不存在
            NetworkError: 网络错误
            
        Example:
            >>> meta_api = MetaAPI(client)
            >>> response = meta_api.get(1)
            >>> print(response.data.path)
            '/a'
            >>> print(response.data.write)
            False
        """
        params = {"id": str(meta_id)}
        response_data = self.client.get("/api/admin/meta/get", params=params)
        return MetaResponse(**response_data)
    
    def create(
        self,
        path: str,
        password: str = "",
        p_sub: bool = False,
        write: bool = False,
        w_sub: bool = False,
        hide: str = "",
        h_sub: bool = False,
        readme: str = "",
        r_sub: bool = False
    ) -> BaseResponse:
        """创建新的元信息。
        
        Args:
            path: 路径
            password: 密码
            p_sub: 密码是否应用到子文件夹
            write: 是否允许写入
            w_sub: 写入是否应用到子文件夹
            hide: 隐藏规则（正则表达式）
            h_sub: 隐藏是否应用到子文件夹
            readme: 说明文档
            r_sub: 说明是否应用到子文件夹
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> meta_api = MetaAPI(client)
            >>> response = meta_api.create(
            ...     path="/private",
            ...     password="secret123",
            ...     p_sub=True,
            ...     write=False
            ... )
            >>> print(response.message)
            'success'
        
        Note:
            - path: 必须是有效的目录路径
            - hide: 支持正则表达式，例如 "/README.md/i"
        """
        payload = {
            "id": 0,  # 创建id为0
            "path": path,
            "password": password,
            "p_sub": p_sub,
            "write": write,
            "w_sub": w_sub,
            "hide": hide,
            "h_sub": h_sub,
            "readme": readme,
            "r_sub": r_sub,
        }
        response_data = self.client.post("/api/admin/meta/create", json=payload)
        return BaseResponse(**response_data)
    
    def update(
        self,
        meta_id: int,
        path: str,
        password: str = "",
        p_sub: bool = False,
        write: bool = False,
        w_sub: bool = False,
        hide: str = "",
        h_sub: bool = False,
        readme: str = "",
        r_sub: bool = False
    ) -> BaseResponse:
        """更新元信息。
        
        Args:
            meta_id: 元信息ID
            path: 路径
            password: 密码
            p_sub: 密码是否应用到子文件夹
            write: 是否允许写入
            w_sub: 写入是否应用到子文件夹
            hide: 隐藏规则
            h_sub: 隐藏是否应用到子文件夹
            readme: 说明文档
            r_sub: 说明是否应用到子文件夹
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 元信息不存在
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> meta_api = MetaAPI(client)
            >>> response = meta_api.update(
            ...     meta_id=1,
            ...     path="/private",
            ...     password="newsecret",
            ...     write=True
            ... )
            >>> print(response.message)
            'success'
        """
        payload = {
            "id": meta_id,
            "path": path,
            "password": password,
            "p_sub": p_sub,
            "write": write,
            "w_sub": w_sub,
            "hide": hide,
            "h_sub": h_sub,
            "readme": readme,
            "r_sub": r_sub,
        }
        response_data = self.client.post("/api/admin/meta/update", json=payload)
        return BaseResponse(**response_data)
    
    def delete(self, meta_id: int) -> BaseResponse:
        """删除元信息。
        
        Args:
            meta_id: 元信息ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 元信息不存在
            NetworkError: 网络错误
            
        Example:
            >>> meta_api = MetaAPI(client)
            >>> response = meta_api.delete(1)
            >>> print(response.message)
            'success'
        
        Warning:
            此操作不可逆，请谨慎使用。
        """
        params = {"id": str(meta_id)}
        response_data = self.client.post("/api/admin/meta/delete", params=params)
        return BaseResponse(**response_data)
