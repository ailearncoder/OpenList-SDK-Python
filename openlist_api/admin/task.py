"""任务管理API。

提供上传任务的查询、删除、取消、重试等管理功能。
"""
from typing import List, Optional
from ..client import BaseClient
from ..models import BaseResponse, TaskInfo


class UploadTaskData(dict):
    """上传任务数据（使用dict保持灵活性）"""
    pass


class TaskAPI:
    """任务管理API类。
    
    封装了所有任务管理相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化任务管理API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def get_info(self, tid: str) -> UploadTaskData:
        """获取任务信息。
        
        Args:
            tid: 任务ID
            
        Returns:
            UploadTaskData: 任务详细信息
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 任务不存在
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> task = task_api.get_info("task_id_here")
            >>> print(task)
            {'id': '...', 'name': '...', 'state': 2, ...}
        """
        params = {"tid": tid}
        response_data = self.client.get("/api/admin/task/upload/info", params=params)
        return response_data.get("data", {})
    
    def get_done(self) -> List[UploadTaskData]:
        """获取已完成的上传任务列表。
        
        Returns:
            List[UploadTaskData]: 已完成任务列表
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> tasks = task_api.get_done()
            >>> for task in tasks:
            ...     print(f"Task: {task['name']}, State: {task['state']}")
        
        Note:
            state: 0=等待中, 1=运行中, 2=已完成, 3=已失败, 4=已取消
        """
        response_data = self.client.get("/api/admin/task/upload/done")
        return response_data.get("data", [])
    
    def get_undone(self) -> List[UploadTaskData]:
        """获取未完成的上传任务列表。
        
        Returns:
            List[UploadTaskData]: 未完成任务列表（等待中、运行中）
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> tasks = task_api.get_undone()
            >>> for task in tasks:
            ...     print(f"Task: {task['name']}, Progress: {task['progress']}%")
        """
        response_data = self.client.get("/api/admin/task/upload/undone")
        return response_data.get("data", [])
    
    def delete(self, tid: str) -> BaseResponse:
        """删除任务。
        
        Args:
            tid: 任务ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 任务不存在
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> response = task_api.delete("task_id_here")
            >>> print(response.message)
            'success'
        """
        params = {"tid": tid}
        response_data = self.client.post("/api/admin/task/upload/delete", params=params)
        return BaseResponse(**response_data)
    
    def cancel(self, tid: str) -> BaseResponse:
        """取消任务。
        
        Args:
            tid: 任务ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 任务不存在
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> response = task_api.cancel("task_id_here")
            >>> print(response.message)
            'success'
        
        Note:
            只能取消等待中或运行中的任务。
        """
        params = {"tid": tid}
        response_data = self.client.post("/api/admin/task/upload/cancel", params=params)
        return BaseResponse(**response_data)
    
    def retry(self, tid: str) -> BaseResponse:
        """重试失败的任务。
        
        Args:
            tid: 任务ID
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NotFoundError: 任务不存在
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> response = task_api.retry("task_id_here")
            >>> print(response.message)
            'success'
        
        Note:
            只能重试失败或取消的任务。
        """
        params = {"tid": tid}
        response_data = self.client.post("/api/admin/task/upload/retry", params=params)
        return BaseResponse(**response_data)
    
    def clear_done(self) -> BaseResponse:
        """清除所有已完成的任务。
        
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> response = task_api.clear_done()
            >>> print(response.message)
            'success'
        """
        response_data = self.client.post("/api/admin/task/upload/clear_done")
        return BaseResponse(**response_data)
    
    def clear_succeeded(self) -> BaseResponse:
        """清除所有成功完成的任务。
        
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            AuthorizationError: 没有管理员权限
            NetworkError: 网络错误
            
        Example:
            >>> task_api = TaskAPI(client)
            >>> response = task_api.clear_succeeded()
            >>> print(response.message)
            'success'
        
        Note:
            只清除成功的任务，保留失败的任务。
        """
        response_data = self.client.post("/api/admin/task/upload/clear_succeeded")
        return BaseResponse(**response_data)
