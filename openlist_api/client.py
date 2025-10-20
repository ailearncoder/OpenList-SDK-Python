"""核心API客户端实现。

提供了与OpenList API交互的基础HTTP请求处理功能。
"""
import requests
from typing import Optional, Dict, Any
from .exceptions import (
    OpenListAPIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    NetworkError,
    ServerError,
)


class BaseClient:
    """基础API客户端类。
    
    提供HTTP请求的封装和错误处理。
    
    Attributes:
        base_url: API基础URL
        timeout: 请求超时时间（秒）
        token: 认证token（可选）
    """
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        token: Optional[str] = None,
    ):
        """初始化客户端。
        
        Args:
            base_url: API基础URL，例如 "https://api.example.com"
            timeout: 请求超时时间（秒），默认30秒
            token: 认证token，可选
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.token = token
        self.session = requests.Session()
    
    def set_token(self, token: str) -> None:
        """设置认证token。
        
        Args:
            token: JWT token
        """
        self.token = token
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头。
        
        Returns:
            包含认证信息的请求头字典
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = self.token
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """处理HTTP响应。
        
        Args:
            response: requests响应对象
            
        Returns:
            解析后的JSON数据
            
        Raises:
            AuthenticationError: 认证失败 (401)
            AuthorizationError: 授权失败 (403)
            NotFoundError: 资源不存在 (404)
            ValidationError: 请求参数错误 (400)
            ServerError: 服务器错误 (5xx)
            OpenListAPIError: 其他API错误
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = response.status_code
            try:
                error_data = response.json()
                error_message = error_data.get('message', str(e))
            except:
                error_message = str(e)
            
            if status_code == 401:
                raise AuthenticationError(error_message, status_code, response)
            elif status_code == 403:
                raise AuthorizationError(error_message, status_code, response)
            elif status_code == 404:
                raise NotFoundError(error_message, status_code, response)
            elif status_code == 400:
                raise ValidationError(error_message, status_code, response)
            elif status_code >= 500:
                raise ServerError(error_message, status_code, response)
            else:
                raise OpenListAPIError(error_message, status_code, response)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Any:
        """发起HTTP请求。
        
        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            endpoint: API端点路径
            **kwargs: requests库支持的其他参数
            
        Returns:
            解析后的响应数据
            
        Raises:
            NetworkError: 网络连接错误
            OpenListAPIError: API请求错误
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        # 合并用户提供的headers
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"请求超时: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"连接失败: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"网络错误: {str(e)}")
    
    def get(self, endpoint: str, **kwargs) -> Any:
        """发起GET请求。"""
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Any:
        """发起POST请求。"""
        return self._request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Any:
        """发起PUT请求。"""
        return self._request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Any:
        """发起DELETE请求。"""
        return self._request("DELETE", endpoint, **kwargs)
