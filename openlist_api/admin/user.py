"""用户管理API。

提供用户的创建、查询、更新和删除功能。
"""
from typing import Optional
from ..client import BaseClient
from ..models import UserListResponse, UserInfoResponse, BaseResponse


class UserAPI:
    """用户管理API类。
    
    封装了所有用户管理相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化用户管理API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def list(self) -> UserListResponse:
        """列出所有用户。
        
        Returns:
            UserListResponse: 包含用户列表的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.list()
            >>> for user in response.data.content:
            ...     print(f"User: {user.username}, Role: {user.role}")
            'User: admin, Role: 2'
            'User: guest, Role: 1'
        
        Note:
            - 此API需要管理员权限
            - role: 0=普通用户, 1=管理员, 2=超级管理员
        """
        response_data = self.client.get("/api/admin/user/list")
        return UserListResponse(**response_data)
    
    def get(self, user_id: int) -> UserInfoResponse:
        """获取指定用户信息。
        
        Args:
            user_id: 用户ID
            
        Returns:
            UserInfoResponse: 包含用户详情的响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 用户不存在
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.get(1)
            >>> print(response.data.username)
            'admin'
            >>> print(response.data.base_path)
            '/'
        """
        params = {"id": str(user_id)}
        response_data = self.client.get("/api/admin/user/get", params=params)
        return UserInfoResponse(**response_data)
    
    def create(
        self,
        username: str,
        password: str = "",
        base_path: str = "/",
        role: int = 0,
        permission: int = 0,
        disabled: bool = False,
        sso_id: str = ""
    ) -> BaseResponse:
        """创建新用户。
        
        Args:
            username: 用户名
            password: 密码
            base_path: 用户根目录
            role: 用户角色 (0=普通用户, 1=管理员, 2=超级管理员)
            permission: 用户权限（位标志）
            disabled: 是否禁用
            sso_id: SSO ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            ValidationError: 参数错误（如用户名已存在）
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.create(
            ...     username="newuser",
            ...     password="pass123",
            ...     role=0,
            ...     permission=60  # 基本权限
            ... )
            >>> print(response.message)
            'success'
        
        Note:
            - permission是位标志，不同位代表不同权限
            - role: 0=普通用户, 1=管理员, 2=超级管理员
        """
        payload = {
            "id": 0,  # 创建id为0
            "username": username,
            "password": password,
            "base_path": base_path,
            "role": role,
            "permission": permission,
            "disabled": disabled,
            "sso_id": sso_id,
        }
        response_data = self.client.post("/api/admin/user/create", json=payload)
        return BaseResponse(**response_data)
    
    def update(
        self,
        user_id: int,
        username: str,
        password: Optional[str] = None,
        base_path: Optional[str] = None,
        role: Optional[int] = None,
        permission: Optional[int] = None,
        disabled: Optional[bool] = None,
        sso_id: Optional[str] = None
    ) -> BaseResponse:
        """更新用户信息。
        
        Args:
            user_id: 用户ID
            username: 用户名
            password: 密码（可选，为空则不修改）
            base_path: 用户根目录
            role: 用户角色
            permission: 用户权限
            disabled: 是否禁用
            sso_id: SSO ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 用户不存在
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.update(
            ...     user_id=3,
            ...     username="newuser",
            ...     password="newpass",
            ...     disabled=True
            ... )
            >>> print(response.message)
            'success'
        """
        payload = {
            "id": user_id,
            "username": username,
        }
        
        if password is not None:
            payload["password"] = password
        if base_path is not None:
            payload["base_path"] = base_path
        if role is not None:
            payload["role"] = role
        if permission is not None:
            payload["permission"] = permission
        if disabled is not None:
            payload["disabled"] = disabled
        if sso_id is not None:
            payload["sso_id"] = sso_id
        
        response_data = self.client.post("/api/admin/user/update", json=payload)
        return BaseResponse(**response_data)
    
    def cancel_2fa(self, user_id: int) -> BaseResponse:
        """取消用户的两步验证。
        
        Args:
            user_id: 用户ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 用户不存在
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.cancel_2fa(3)
            >>> print(response.message)
            'success'
        
        Note:
            用于管理员帮助用户重置两步验证。
        """
        params = {"id": str(user_id)}
        response_data = self.client.post("/api/admin/user/cancel_2fa", params=params)
        return BaseResponse(**response_data)
    
    def delete(self, user_id: int) -> BaseResponse:
        """删除用户。
        
        Args:
            user_id: 用户ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 用户不存在
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.delete(3)
            >>> print(response.message)
            'success'
        
        Warning:
            此操作不可逆，请谨慎使用。
        """
        params = {"id": str(user_id)}
        response_data = self.client.post("/api/admin/user/delete", params=params)
        return BaseResponse(**response_data)
    
    def delete_cache(self, username: str) -> BaseResponse:
        """删除用户缓存。
        
        Args:
            username: 用户名
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> user_api = UserAPI(client)
            >>> response = user_api.delete_cache("admin")
            >>> print(response.message)
            'success'
        
        Note:
            用于清除用户相关的缓存数据。
        """
        params = {"username": username}
        response_data = self.client.post("/api/admin/user/del_cache", params=params)
        return BaseResponse(**response_data)
