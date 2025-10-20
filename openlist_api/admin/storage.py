"""存储管理API。

提供存储（Storage）的创建、查询、更新和删除功能。
存储用于配置不同的驱动来挂载外部存储服务。
"""
from typing import Optional
from ..client import BaseClient
from ..models import (
    StorageListResponse,
    StorageResponse,
    StorageIDResponse,
    BaseResponse
)


class StorageAPI:
    """存储管理API类。
    
    封装了所有存储管理相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化存储管理API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def list(
        self,
        page: int = 1,
        per_page: int = 0
    ) -> StorageListResponse:
        """列出所有存储。
        
        Args:
            page: 页码，从1开始
            per_page: 每页数量，0表示不分页
            
        Returns:
            StorageListResponse: 包含存储列表的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> response = storage_api.list()
            >>> for storage in response.data.content:
            ...     print(f"Mount: {storage.mount_path}, Driver: {storage.driver}")
            'Mount: /local, Driver: Local'
        
        Note:
            此API需要管理员权限。
        """
        params = {}
        if page:
            params["page"] = str(page)
        if per_page:
            params["per_page"] = str(per_page)
        
        response_data = self.client.get("/api/admin/storage/list", params=params)
        return StorageListResponse(**response_data)
    
    def get(self, storage_id: int) -> StorageResponse:
        """获取指定存储信息。
        
        Args:
            storage_id: 存储ID
            
        Returns:
            StorageResponse: 包含存储详情的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 存储不存在
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> response = storage_api.get(1)
            >>> print(response.data.mount_path)
            '/local'
            >>> print(response.data.status)
            'work'
        """
        params = {"id": str(storage_id)}
        response_data = self.client.get("/api/admin/storage/get", params=params)
        return StorageResponse(**response_data)
    
    def create(
        self,
        mount_path: str,
        driver: str,
        addition: str,
        order_by: str = "name",
        order_direction: str = "asc",
        extract_folder: str = "front",
        web_proxy: bool = False,
        enable_sign: bool = False,
        status: str = "work",
        order: int = 0,
        cache_expiration: int = 30,
        remark: str = "",
        webdav_policy: str = "native_proxy",
        down_proxy_url: str = ""
    ) -> StorageIDResponse:
        """创建新存储。
        
        Args:
            mount_path: 挂载路径
            driver: 驱动名称 (如 "Local", "Aliyundrive" 等)
            addition: 额外配置信息 (JSON字符串)
            order_by: 排序字段
            order_direction: 排序方向 ("asc" 或 "desc")
            extract_folder: 提取目录 ("front" 或其他)
            web_proxy: 是否启用web代理
            enable_sign: 是否启用签名
            status: 状态
            order: 排序序号
            cache_expiration: 缓存过期时间（分钟）
            remark: 备注
            webdav_policy: webdav策略
            down_proxy_url: 下载代理URL
            
        Returns:
            StorageIDResponse: 包含新创建存储ID的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> addition = '{"root_folder_path":"/data","show_hidden":true}'
            >>> response = storage_api.create(
            ...     mount_path="/local",
            ...     driver="Local",
            ...     addition=addition
            ... )
            >>> print(f"Created storage ID: {response.data.id}")
            'Created storage ID: 7'
        
        Note:
            - addition参数需要根据不同driver提供相应的配置
            - 不同驱动的addition字段要求不同
        """
        payload = {
            "id": 0,  # 创建时id为0
            "mount_path": mount_path,
            "order": order,
            "driver": driver,
            "cache_expiration": cache_expiration,
            "status": status,
            "addition": addition,
            "remark": remark,
            "web_proxy": web_proxy,
            "webdav_policy": webdav_policy,
            "down_proxy_url": down_proxy_url,
            "order_by": order_by,
            "order_direction": order_direction,
            "extract_folder": extract_folder,
            "enable_sign": enable_sign,
        }
        response_data = self.client.post("/api/admin/storage/create", json=payload)
        return StorageIDResponse(**response_data)
    
    def update(
        self,
        storage_id: int,
        mount_path: str,
        driver: str,
        addition: str,
        order_by: str,
        order_direction: str,
        extract_folder: str,
        web_proxy: bool,
        enable_sign: bool,
        status: str,
        order: Optional[int] = None,
        cache_expiration: Optional[int] = None,
        remark: Optional[str] = None,
        webdav_policy: Optional[str] = None,
        down_proxy_url: Optional[str] = None
    ) -> StorageIDResponse:
        """更新存储信息。
        
        Args:
            storage_id: 存储ID
            mount_path: 挂载路径
            driver: 驱动名称
            addition: 额外配置信息 (JSON字符串)
            order_by: 排序字段
            order_direction: 排序方向
            extract_folder: 提取目录
            web_proxy: 是否启用web代理
            enable_sign: 是否启用签名
            status: 状态
            order: 排序序号（可选）
            cache_expiration: 缓存过期时间（可选）
            remark: 备注（可选）
            webdav_policy: webdav策略（可选）
            down_proxy_url: 下载代理URL（可选）
            
        Returns:
            StorageIDResponse: 包含存储ID的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 存储不存在
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> addition = '{"root_folder_path":"/new_data"}'
            >>> response = storage_api.update(
            ...     storage_id=1,
            ...     mount_path="/local",
            ...     driver="Local",
            ...     addition=addition,
            ...     order_by="name",
            ...     order_direction="asc",
            ...     extract_folder="front",
            ...     web_proxy=False,
            ...     enable_sign=False,
            ...     status="work"
            ... )
            >>> print(response.message)
            'success'
        """
        payload = {
            "id": storage_id,
            "mount_path": mount_path,
            "driver": driver,
            "addition": addition,
            "order_by": order_by,
            "order_direction": order_direction,
            "extract_folder": extract_folder,
            "web_proxy": web_proxy,
            "enable_sign": enable_sign,
            "status": status,
        }
        
        if order is not None:
            payload["order"] = order
        if cache_expiration is not None:
            payload["cache_expiration"] = cache_expiration
        if remark is not None:
            payload["remark"] = remark
        if webdav_policy is not None:
            payload["webdav_policy"] = webdav_policy
        if down_proxy_url is not None:
            payload["down_proxy_url"] = down_proxy_url
        
        response_data = self.client.post("/api/admin/storage/update", json=payload)
        return StorageIDResponse(**response_data)
    
    def enable(self, storage_id: int) -> BaseResponse:
        """启用存储。
        
        Args:
            storage_id: 存储ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 存储不存在
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> response = storage_api.enable(1)
            >>> print(response.message)
            'success'
        """
        params = {"id": storage_id}
        response_data = self.client.post("/api/admin/storage/enable", params=params)
        return BaseResponse(**response_data)
    
    def disable(self, storage_id: int) -> BaseResponse:
        """禁用存储。
        
        Args:
            storage_id: 存储ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 存储不存在
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> response = storage_api.disable(1)
            >>> print(response.message)
            'success'
        """
        params = {"id": str(storage_id)}
        response_data = self.client.post("/api/admin/storage/disable", params=params)
        return BaseResponse(**response_data)
    
    def delete(self, storage_id: int) -> BaseResponse:
        """删除存储。
        
        Args:
            storage_id: 存储ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 存储不存在
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> response = storage_api.delete(1)
            >>> print(response.message)
            'success'
        
        Warning:
            此操作不可逆，请谨慎使用。
        """
        params = {"id": str(storage_id)}
        response_data = self.client.post("/api/admin/storage/delete", params=params)
        return BaseResponse(**response_data)
    
    def load_all(self) -> BaseResponse:
        """重新加载所有存储。
        
        重新初始化所有存储配置。
        
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> storage_api = StorageAPI(client)
            >>> response = storage_api.load_all()
            >>> print(response.message)
            'success'
        
        Note:
            用于在修改存储配置后重新加载所有存储。
        """
        response_data = self.client.post("/api/admin/storage/load_all")
        return BaseResponse(**response_data)
