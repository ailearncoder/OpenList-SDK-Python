"""文件系统相关API。

提供文件和目录的列表、搜索、操作等功能。
"""
from typing import Optional, List, BinaryIO
from urllib.parse import quote
from .client import BaseClient
from .models import (
    ListResponse, 
    FileInfoResponse, 
    DirsResponse, 
    SearchResponse, 
    BaseResponse,
    RenameObject,
    OfflineDownloadResponse,
    UploadResponse,
)


class FileSystemAPI:
    """文件系统API类。
    
    封装了所有与文件系统相关的API操作。
    
    Attributes:
        client: 基础HTTP客户端实例
    """
    
    def __init__(self, client: BaseClient):
        """初始化文件系统API。
        
        Args:
            client: BaseClient实例
        """
        self.client = client
    
    def list(
        self,
        path: str,
        password: str = "",
        page: int = 1,
        per_page: int = 0,
        refresh: bool = False
    ) -> ListResponse:
        """列出指定目录下的文件和子目录。
        
        Args:
            path: 目录路径，例如 "/" 或 "/folder"
            password: 目录密码（如果目录被加密）
            page: 页码，从1开始
            per_page: 每页数量，0表示不分页
            refresh: 是否强制刷新缓存
            
        Returns:
            ListResponse: 包含文件列表的响应对象
            
        Raises:
            AuthenticationError: 未认证或token无效
            NotFoundError: 目录不存在
            ValidationError: 密码错误或参数错误
            NetworkError: 网络连接错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.list("/")
            >>> for item in response.data.content:
            ...     print(f"{item.name} ({'dir' if item.is_dir else 'file'})")
            'Documents (dir)'
            'photo.jpg (file)'
        
        Note:
            - 此API需要认证
            - per_page=0表示返回所有结果
        """
        payload = {
            "path": path,
            "password": password,
            "page": page,
            "per_page": per_page,
            "refresh": refresh,
        }
        response_data = self.client.post("/api/fs/list", json=payload)
        return ListResponse(**response_data)
    
    def get(
        self,
        path: str,
        password: str = "",
        page: int = 1,
        per_page: int = 0,
        refresh: bool = False
    ) -> FileInfoResponse:
        """获取某个文件或目录的详细信息。
        
        Args:
            path: 文件或目录路径
            password: 密码（如果被加密）
            page: 页码
            per_page: 每页数量
            refresh: 是否强制刷新
            
        Returns:
            FileInfoResponse: 包含文件/目录详细信息的响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 文件/目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.get("/document.pdf")
            >>> print(response.data.name)
            'document.pdf'
            >>> print(response.data.raw_url)
            'http://127.0.0.1:5244/p/local/document.pdf'
        """
        payload = {
            "path": path,
            "password": password,
            "page": page,
            "per_page": per_page,
            "refresh": refresh,
        }
        response_data = self.client.post("/api/fs/get", json=payload)
        return FileInfoResponse(**response_data)
    
    def dirs(
        self,
        path: str,
        password: str = "",
        force_root: bool = False
    ) -> DirsResponse:
        """获取指定目录下的所有子目录。
        
        Args:
            path: 目录路径
            password: 目录密码
            force_root: 是否强制从根目录开始
            
        Returns:
            DirsResponse: 包含子目录列表的响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.dirs("/")
            >>> for dir_item in response.data:
            ...     print(dir_item.name)
            'Documents'
            'Downloads'
        """
        payload = {
            "path": path,
            "password": password,
            "force_root": force_root,
        }
        response_data = self.client.post("/api/fs/dirs", json=payload)
        return DirsResponse(**response_data)
    
    def search(
        self,
        parent: str,
        keywords: str,
        scope: int = 0,
        page: int = 1,
        per_page: int = 100,
        password: str = ""
    ) -> SearchResponse:
        """搜索文件或文件夹。
        
        Args:
            parent: 搜索的父目录路径
            keywords: 搜索关键词
            scope: 搜索类型 (0=全部, 1=仅文件夹, 2=仅文件)
            page: 页码
            per_page: 每页数量
            password: 目录密码
            
        Returns:
            SearchResponse: 包含搜索结果的响应对象
            
        Raises:
            AuthenticationError: 未认证
            ValidationError: 参数错误
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.search("/", "test", scope=2)  # 仅搜索文件
            >>> for item in response.data.content:
            ...     print(f"{item.parent}/{item.name}")
            '/documents/test.txt'
        
        Note:
            scope参数: 0=全部, 1=仅文件夹, 2=仅文件
        """
        payload = {
            "parent": parent,
            "keywords": keywords,
            "scope": scope,
            "page": page,
            "per_page": per_page,
            "password": password,
        }
        response_data = self.client.post("/api/fs/search", json=payload)
        return SearchResponse(**response_data)
    
    def mkdir(self, path: str) -> BaseResponse:
        """新建文件夹。
        
        Args:
            path: 新目录的完整路径
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            ValidationError: 路径无效或已存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.mkdir("/new_folder")
            >>> print(response.message)
            'success'
        """
        payload = {"path": path}
        response_data = self.client.post("/api/fs/mkdir", json=payload)
        return BaseResponse(**response_data)
    
    def rename(self, path: str, name: str) -> BaseResponse:
        """重命名文件或文件夹。
        
        Args:
            path: 源文件/文件夹的完整路径
            name: 新名称（不包含路径，不支持'/'）
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 源文件不存在
            ValidationError: 名称无效
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.rename("/old_name.txt", "new_name.txt")
            >>> print(response.message)
            'success'
        
        Note:
            name参数不能包含'/'字符
        """
        payload = {"path": path, "name": name}
        response_data = self.client.post("/api/fs/rename", json=payload)
        return BaseResponse(**response_data)
    
    def move(self, src_dir: str, dst_dir: str, names: List[str]) -> BaseResponse:
        """移动文件或文件夹。
        
        Args:
            src_dir: 源目录路径
            dst_dir: 目标目录路径
            names: 要移动的文件/文件夹名称列表
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 源文件或目标目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.move("/source", "/target", ["file1.txt", "file2.txt"])
            >>> print(response.message)
            'success'
        """
        payload = {
            "src_dir": src_dir,
            "dst_dir": dst_dir,
            "names": names,
        }
        response_data = self.client.post("/api/fs/move", json=payload)
        return BaseResponse(**response_data)
    
    def copy(self, src_dir: str, dst_dir: str, names: List[str]) -> BaseResponse:
        """复制文件或文件夹。
        
        Args:
            src_dir: 源目录路径
            dst_dir: 目标目录路径
            names: 要复制的文件/文件夹名称列表
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 源文件或目标目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.copy("/source", "/target", ["file1.txt"])
            >>> print(response.message)
            'success'
        """
        payload = {
            "src_dir": src_dir,
            "dst_dir": dst_dir,
            "names": names,
        }
        response_data = self.client.post("/api/fs/copy", json=payload)
        return BaseResponse(**response_data)
    
    def remove(self, dir: str, names: List[str]) -> BaseResponse:
        """删除文件或文件夹。
        
        Args:
            dir: 所在目录路径
            names: 要删除的文件/文件夹名称列表
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 文件或目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.remove("/documents", ["old_file.txt"])
            >>> print(response.message)
            'success'
        
        Warning:
            此操作不可逆，请谨慎使用。
        """
        payload = {"dir": dir, "names": names}
        response_data = self.client.post("/api/fs/remove", json=payload)
        return BaseResponse(**response_data)
    
    def batch_rename(self, src_dir: str, rename_objects: List[RenameObject]) -> BaseResponse:
        """批量重命名文件或文件夹。
        
        Args:
            src_dir: 源目录路径
            rename_objects: 重命名对象列表，每个对象包含src_name和new_name
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 源文件不存在
            ValidationError: 参数错误或新名称冲突
            NetworkError: 网络错误
            
        Example:
            >>> from openlist_api.models import RenameObject
            >>> fs_api = FileSystemAPI(client)
            >>> renames = [
            ...     RenameObject(src_name="test.txt", new_name="test1.txt"),
            ...     RenameObject(src_name="file.doc", new_name="document.doc")
            ... ]
            >>> response = fs_api.batch_rename("/documents", renames)
            >>> print(response.message)
            'success'
        
        Note:
            此方法可以一次性重命名多个文件，比多次调用rename()更高效。
        """
        payload = {
            "src_dir": src_dir,
            "rename_objects": [obj.dict() for obj in rename_objects],
        }
        response_data = self.client.post("/api/fs/batch_rename", json=payload)
        return BaseResponse(**response_data)
    
    def regex_rename(self, src_dir: str, src_name_regex: str, new_name_regex: str) -> BaseResponse:
        """使用正则表达式批量重命名。
        
        Args:
            src_dir: 源目录路径
            src_name_regex: 源文件名匹配正则表达式
            new_name_regex: 新文件名正则表达式（支持捕获组替换）
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            ValidationError: 正则表达式无效
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> # 将所有.txt文件重命名为.bak
            >>> response = fs_api.regex_rename(
            ...     "/documents",
            ...     r"^(.+)\.txt$",
            ...     r"\1.bak"
            ... )
            >>> print(response.message)
            'success'
        
        Note:
            - src_name_regex: 用于匹配文件名的正则表达式
            - new_name_regex: 用于生成新文件名，可以使用\1, \2等引用捕获组
        """
        payload = {
            "src_dir": src_dir,
            "src_name_regex": src_name_regex,
            "new_name_regex": new_name_regex,
        }
        response_data = self.client.post("/api/fs/regex_rename", json=payload)
        return BaseResponse(**response_data)
    
    def recursive_move(self, src_dir: str, dst_dir: str) -> BaseResponse:
        """聚合移动（递归移动目录下所有文件）。
        
        将源文件夹下的所有文件递归移动到目标文件夹。
        
        Args:
            src_dir: 源文件夹路径
            dst_dir: 目标文件夹路径
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 源目录或目标目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.recursive_move("/temp", "/archive")
            >>> print(response.message)
            'success'
        
        Note:
            此操作会递归移动源目录下的所有内容到目标目录。
        """
        payload = {
            "src_dir": src_dir,
            "dst_dir": dst_dir,
        }
        response_data = self.client.post("/api/fs/recursive_move", json=payload)
        return BaseResponse(**response_data)
    
    def remove_empty_directory(self, src_dir: str) -> BaseResponse:
        """删除空文件夹。
        
        递归删除指定目录下的所有空文件夹。
        
        Args:
            src_dir: 目录路径
            
        Returns:
            BaseResponse: 基础响应对象
            
        Raises:
            AuthenticationError: 未认证
            NotFoundError: 目录不存在
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> response = fs_api.remove_empty_directory("/downloads")
            >>> print(response.message)
            'success'
        
        Note:
            只会删除完全为空的文件夹，包含文件的文件夹不会被删除。
        """
        payload = {"src_dir": src_dir}
        response_data = self.client.post("/api/fs/remove_empty_directory", json=payload)
        return BaseResponse(**response_data)
    
    def add_offline_download(
        self,
        path: str,
        urls: List[str],
        tool: str = "SimpleHttp",
        delete_policy: str = "delete_on_upload_succeed"
    ) -> OfflineDownloadResponse:
        """添加离线下载任务。
        
        Args:
            path: 目标保存路径
            urls: 下载链接列表
            tool: 下载工具，可选: "aria2", "SimpleHttp", "qBittorrent"
            delete_policy: 删除策略，可选:
                - "delete_on_upload_succeed": 上传成功后删除
                - "delete_on_upload_failed": 上传失败后删除
                - "delete_never": 从不删除
                - "delete_always": 总是删除
            
        Returns:
            OfflineDownloadResponse: 包含创建的任务列表的响应对象
            
        Raises:
            AuthenticationError: 未认证
            ValidationError: 参数错误（无效的tool或delete_policy）
            NetworkError: 网络错误
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> urls = [
            ...     "https://example.com/file1.zip",
            ...     "https://example.com/file2.pdf"
            ... ]
            >>> response = fs_api.add_offline_download(
            ...     path="/downloads",
            ...     urls=urls,
            ...     tool="aria2"
            ... )
            >>> for task in response.data.tasks:
            ...     print(f"Task {task.id}: {task.name}")
        
        Note:
            - tool="SimpleHttp": 简单HTTP下载
            - tool="aria2": 使用aria2下载器（需要配置）
            - tool="qBittorrent": 使用qBittorrent（需要配置）
        """
        payload = {
            "path": path,
            "urls": urls,
            "tool": tool,
            "delete_policy": delete_policy,
        }
        response_data = self.client.post("/api/fs/add_offline_download", json=payload)
        return OfflineDownloadResponse(**response_data)
    
    def form_upload(
        self,
        file_path: str,
        file: BinaryIO,
        as_task: bool = True
    ) -> UploadResponse:
        """表单方式上传文件。
        
        Args:
            file_path: 目标文件的完整路径（会自动进行URL编码）
            file: 文件对象（二进制读模式）
            as_task: 是否作为任务添加
            
        Returns:
            UploadResponse: 包含上传任务信息的响应对象
            
        Raises:
            AuthenticationError: 未认证
            ValidationError: 文件路径无效
            NetworkError: 网络错误或上传失败
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> with open("local_file.pdf", "rb") as f:
            ...     response = fs_api.form_upload("/documents/file.pdf", f)
            ...     print(f"Upload task: {response.data.task.id}")
            ...     print(f"Status: {response.data.task.status}")
        
        Note:
            - 适用于较小的文件上传
            - 使用multipart/form-data方式
            - file_path会自动进行URL编码
        """
        headers = {
            "File-Path": quote(file_path, safe=''),
            "As-Task": str(as_task).lower(),
        }
        
        files = {'file': file}
        
        # 使用PUT方法，需要特殊处理headers
        response_data = self.client.put(
            "/api/fs/form",
            files=files,
            headers=headers
        )
        return UploadResponse(**response_data)
    
    def stream_upload(
        self,
        file_path: str,
        file_data: BinaryIO,
        as_task: bool = True
    ) -> UploadResponse:
        """流式上传文件。
        
        Args:
            file_path: 目标文件的完整路径（会自动进行URL编码）
            file_data: 文件数据流（二进制读模式）
            as_task: 是否作为任务添加
            
        Returns:
            UploadResponse: 包含上传任务信息的响应对象
            
        Raises:
            AuthenticationError: 未认证
            ValidationError: 文件路径无效
            NetworkError: 网络错误或上传失败
            
        Example:
            >>> fs_api = FileSystemAPI(client)
            >>> with open("large_file.zip", "rb") as f:
            ...     response = fs_api.stream_upload("/backups/backup.zip", f)
            ...     print(f"Upload task: {response.data.task.id}")
        
        Note:
            - 适用于大文件上传
            - 使用application/octet-stream方式
            - 更节省内存，适合大文件
        """
        headers = {
            "File-Path": quote(file_path, safe=''),
            "As-Task": str(as_task).lower(),
            "Content-Type": "application/octet-stream",
        }
        
        response_data = self.client.put(
            "/api/fs/put",
            data=file_data,
            headers=headers
        )
        return UploadResponse(**response_data)
