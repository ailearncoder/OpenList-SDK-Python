"""
OpenList API 客户端单元测试

测试基础HTTP客户端和核心功能。
"""
import pytest
from unittest.mock import Mock, patch
from openlist_api import OpenListClient
from openlist_api.exceptions import (
    AuthenticationError,
    NotFoundError,
    NetworkError,
)


class TestOpenListClient:
    """测试OpenListClient主类"""
    
    def test_client_initialization(self):
        """测试客户端初始化"""
        client = OpenListClient("http://localhost:5244")
        assert client._client.base_url == "http://localhost:5244"
        assert client._client.timeout == 30
        assert client.auth is not None
        assert client.fs is not None
    
    def test_set_token(self):
        """测试设置token"""
        client = OpenListClient("http://localhost:5244")
        client.set_token("test_token")
        assert client.token == "test_token"
        assert client._client.token == "test_token"


class TestAuthAPI:
    """测试认证API"""
    
    @patch('openlist_api.client.requests.Session.request')
    def test_login_success(self, mock_request):
        """测试成功登录"""
        # 模拟API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "message": "success",
            "data": {"token": "mock_jwt_token"}
        }
        mock_request.return_value = mock_response
        
        # 执行登录
        client = OpenListClient("http://localhost:5244")
        response = client.auth.login("admin", "password")
        
        # 验证结果
        assert response.code == 200
        assert response.data.token == "mock_jwt_token"
        
        # 验证请求参数
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs['json'] == {"username": "admin", "password": "password"}
    
    @patch('openlist_api.client.requests.Session.request')
    def test_login_failure(self, mock_request):
        """测试登录失败"""
        # 模拟401错误
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid credentials"}
        mock_response.raise_for_status.side_effect = Exception("401")
        mock_request.return_value = mock_response
        
        # 执行登录应该抛出异常
        client = OpenListClient("http://localhost:5244")
        with pytest.raises(AuthenticationError):
            client.auth.login("admin", "wrong_password")


class TestFileSystemAPI:
    """测试文件系统API"""
    
    @patch('openlist_api.client.requests.Session.request')
    def test_list_files(self, mock_request):
        """测试列出文件"""
        # 模拟API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "message": "success",
            "data": {
                "content": [
                    {
                        "name": "test.txt",
                        "size": 1024,
                        "is_dir": False,
                        "modified": "2024-01-01T00:00:00Z",
                        "sign": "",
                        "thumb": "",
                        "type": 1
                    }
                ],
                "total": 1,
                "readme": "",
                "header": "",
                "write": True,
                "provider": "Local"
            }
        }
        mock_request.return_value = mock_response
        
        # 执行列表操作
        client = OpenListClient("http://localhost:5244")
        client.set_token("test_token")
        response = client.fs.list("/")
        
        # 验证结果
        assert response.code == 200
        assert len(response.data.content) == 1
        assert response.data.content[0].name == "test.txt"
        assert response.data.content[0].size == 1024
        assert response.data.total == 1
    
    @patch('openlist_api.client.requests.Session.request')
    def test_mkdir(self, mock_request):
        """测试创建文件夹"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "message": "success",
            "data": None
        }
        mock_request.return_value = mock_response
        
        client = OpenListClient("http://localhost:5244")
        client.set_token("test_token")
        response = client.fs.mkdir("/new_folder")
        
        assert response.code == 200
        assert response.message == "success"


class TestExceptionHandling:
    """测试异常处理"""
    
    @patch('openlist_api.client.requests.Session.request')
    def test_not_found_error(self, mock_request):
        """测试404错误"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not found"}
        mock_response.raise_for_status.side_effect = Exception("404")
        mock_request.return_value = mock_response
        
        client = OpenListClient("http://localhost:5244")
        client.set_token("test_token")
        
        with pytest.raises(NotFoundError):
            client.fs.get("/nonexistent.txt")
    
    @patch('openlist_api.client.requests.Session.request')
    def test_network_error(self, mock_request):
        """测试网络错误"""
        import requests
        mock_request.side_effect = requests.exceptions.ConnectionError("Network error")
        
        client = OpenListClient("http://localhost:5244")
        
        with pytest.raises(NetworkError):
            client.auth.login("admin", "password")


# 运行测试的说明
"""
运行所有测试:
    pytest tests/

运行特定测试:
    pytest tests/test_client.py::TestAuthAPI::test_login_success

生成覆盖率报告:
    pytest --cov=openlist_api tests/

安装测试依赖:
    pip install pytest pytest-cov
"""
