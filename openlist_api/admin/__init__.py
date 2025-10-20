"""管理员API模块。

包含所有管理员功能，包括元信息、用户、存储、驱动、设置和任务管理。
"""
from .meta import MetaAPI
from .user import UserAPI
from .storage import StorageAPI
from .driver import DriverAPI
from .setting import SettingAPI
from .task import TaskAPI

__all__ = [
    "MetaAPI",
    "UserAPI",
    "StorageAPI",
    "DriverAPI",
    "SettingAPI",
    "TaskAPI",
]
