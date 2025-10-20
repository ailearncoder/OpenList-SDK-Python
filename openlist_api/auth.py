"""认证相关API。

提供用户认证、token获取、两步验证等功能。
"""
import hashlib
from typing import Optional
from .client import BaseClient
from .models import LoginResponse, Generate2FAResponse, BaseResponse, UserInfoResponse


class AuthAPI:
    """认证API类。
    
    封装了所有与用户认证相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化认证API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def login(
        self,
        username: str,
        password: str,
        otp_code: Optional[str] = None
    ) -> LoginResponse:
        """获取用户登录token。
        
        获取某个用户的临时JWT token，默认48小时过期。
        
        Args:
            username: 用户名
            password: 密码（明文）
            otp_code: 二步验证码（可选）
            
        Returns:
            LoginResponse: 包含token的响应对象
            
        Raises:
            AuthenticationError: 认证失败（用户名或密码错误）
            ValidationError: 参数验证失败
            NetworkError: 网络连接错误
            
        Example:
            >>> auth_api = AuthAPI(client)
            >>> response = auth_api.login("admin", "password123")
            >>> print(response.data.token)
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        """
        payload = {
            "username": username,
            "password": password,
        }
        
        if otp_code:
            payload["otp_code"] = otp_code
        
        response_data = self.client.post("/api/auth/login", json=payload)
        return LoginResponse(**response_data)
    
    def login_hash(
        self,
        username: str,
        password: str,
        otp_code: Optional[str] = None
    ) -> LoginResponse:
        """使用hash密码获取用户登录token。
        
        获取某个用户的临时JWT token。传入的密码需要在添加
        "-https://github.com/alist-org/alist"后缀后再进行sha256加密。
        
        Args:
            username: 用户名
            password: 密码（明文，将自动hash）
            otp_code: 二步验证码（可选）
            
        Returns:
            LoginResponse: 包含token的响应对象
            
        Raises:
            AuthenticationError: 认证失败（用户名或密码错误）
            ValidationError: 参数验证失败
            NetworkError: 网络连接错误
            
        Example:
            >>> auth_api = AuthAPI(client)
            >>> response = auth_api.login_hash("admin", "password123")
            >>> print(response.data.token)
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        
        Note:
            密码处理方式: sha256(password + "-https://github.com/alist-org/alist")
        """
        # 添加后缀并计算SHA256
        password_with_suffix = password + "-https://github.com/alist-org/alist"
        hashed_password = hashlib.sha256(password_with_suffix.encode()).hexdigest()
        
        payload = {
            "username": username,
            "password": hashed_password,
        }
        
        if otp_code:
            payload["otp_code"] = otp_code
        
        response_data = self.client.post("/api/auth/login/hash", json=payload)
        return LoginResponse(**response_data)
    
    def generate_2fa(self) -> Generate2FAResponse:
        """生成2FA（两步验证）密钥。
        
        为当前用户生成两步验证密钥和二维码。
        
        Returns:
            Generate2FAResponse: 包含2FA密钥和二维码的响应对象
            
        Raises:
            AuthenticationError: 未认证或token无效
            NetworkError: 网络连接错误
            
        Example:
            >>> auth_api = AuthAPI(client)
            >>> client.set_token("your_token_here")
            >>> response = auth_api.generate_2fa()
            >>> print(response.data.secret)
            'RPQZG4MDS3'
            >>> print(response.data.qr[:30])
            'data:image/png;base64,iVBORw...'
        
        Note:
            此API需要认证，必须先设置token。
        """
        response_data = self.client.post("/api/auth/2fa/generate")
        return Generate2FAResponse(**response_data)
    
    def verify_2fa(self, code: str, secret: str) -> BaseResponse:
        """验证2FA（两步验证）验证码。
        
        验证2FA验证码是否正确。
        
        Args:
            code: 2FA验证码（从认证器应用生成）
            secret: 2FA密钥
            
        Returns:
            BaseResponse: 基础响应对象，data为null
            
        Raises:
            AuthenticationError: 未认证或token无效
            ValidationError: 验证码错误
            NetworkError: 网络连接错误
            
        Example:
            >>> auth_api = AuthAPI(client)
            >>> client.set_token("your_token_here")
            >>> response = auth_api.verify_2fa("123456", "RPQZG4MDS3")
            >>> print(response.code)
            200
        
        Note:
            此API需要认证，必须先设置token。
        """
        payload = {
            "code": code,
            "secret": secret,
        }
        response_data = self.client.post("/api/auth/2fa/verify", json=payload)
        return BaseResponse(**response_data)
    
    def get_current_user(self) -> UserInfoResponse:
        """获取当前登录用户的信息。
        
        Returns:
            UserInfoResponse: 包含用户详细信息的响应对象
            
        Raises:
            AuthenticationError: 未认证或token无效
            NetworkError: 网络连接错误
            
        Example:
            >>> auth_api = AuthAPI(client)
            >>> client.set_token("your_token_here")
            >>> response = auth_api.get_current_user()
            >>> print(response.data.username)
            'admin'
            >>> print(response.data.role)
            2
        
        Note:
            此API需要认证，必须先设置token。
            role值: 0=普通用户, 1=管理员, 2=超级管理员
        """
        response_data = self.client.get("/api/me")
        return UserInfoResponse(**response_data)
