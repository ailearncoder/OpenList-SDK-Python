# OpenList API - Python客户端库

[English](README_EN.md) | 简体中文

一个功能完整的Python客户端库，用于与OpenList (AList) API进行交互。提供了完整的类型提示、文档字符串和异常处理。

## 特性

✅ **完整的类型支持** - 使用Pydantic模型提供强类型返回值  
✅ **清晰的文档** - 每个函数都有详细的Docstrings  
✅ **健壮的错误处理** - 自定义异常类型，优雅处理各种错误  
✅ **模块化设计** - 按功能模块组织API  
✅ **易于使用** - 简洁直观的API设计  
✅ **100%完成** - 所有61个API已完全实现  

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 基础用法

```python
from openlist_api import OpenListClient

# 创建客户端实例
client = OpenListClient("http://localhost:5244")

# 登录获取token
login_response = client.auth.login("admin", "password")
client.set_token(login_response.data.token)

# 列出根目录文件
files = client.fs.list("/")
for file in files.data.content:
    print(f"{file.name} ({'目录' if file.is_dir else '文件'})")
```

### 认证功能

```python
# 方式1: 明文密码登录
response = client.auth.login("username", "password")
print(response.data.token)

# 方式2: Hash密码登录（更安全）
response = client.auth.login_hash("username", "password")

# 获取当前用户信息
user_info = client.auth.get_current_user()
print(f"用户名: {user_info.data.username}")
print(f"角色: {user_info.data.role}")

# 生成2FA密钥
twofa = client.auth.generate_2fa()
print(f"密钥: {twofa.data.secret}")
print(f"二维码: {twofa.data.qr[:50]}...")

# 验证2FA验证码
client.auth.verify_2fa("123456", "your_secret")
```

### 文件系统操作

```python
# 列出目录内容
files = client.fs.list("/documents", page=1, per_page=50)
print(f"总计: {files.data.total} 个项目")

# 获取文件/目录信息
file_info = client.fs.get("/document.pdf")
print(f"文件大小: {file_info.data.size} 字节")
print(f"下载链接: {file_info.data.raw_url}")

# 搜索文件
results = client.fs.search("/", "test", scope=2)  # scope=2: 仅搜索文件
for item in results.data.content:
    print(f"找到: {item.parent}/{item.name}")

# 创建文件夹
client.fs.mkdir("/new_folder")

# 重命名文件
client.fs.rename("/old_name.txt", "new_name.txt")

# 移动文件
client.fs.move("/source_dir", "/target_dir", ["file1.txt", "file2.txt"])

# 复制文件
client.fs.copy("/source_dir", "/target_dir", ["file.txt"])

# 删除文件
client.fs.remove("/documents", ["unwanted.txt"])
```

## API模块

### 认证模块 (`client.auth`)

- `login(username, password, otp_code)` - 登录获取token
- `login_hash(username, password, otp_code)` - 使用hash密码登录
- `generate_2fa()` - 生成两步验证密钥
- `verify_2fa(code, secret)` - 验证2FA验证码
- `get_current_user()` - 获取当前用户信息

### 文件系统模块 (`client.fs`)

- `list(path, password, page, per_page, refresh)` - 列出目录内容
- `get(path, password, page, per_page, refresh)` - 获取文件/目录信息
- `dirs(path, password, force_root)` - 获取所有子目录
- `search(parent, keywords, scope, page, per_page, password)` - 搜索文件
- `mkdir(path)` - 创建文件夹
- `rename(path, name)` - 重命名文件
- `batch_rename(src_dir, rename_objects)` - 批量重命名
- `regex_rename(src_dir, src_name_regex, new_name_regex)` - 正则重命名
- `move(src_dir, dst_dir, names)` - 移动文件
- `recursive_move(src_dir, dst_dir)` - 递归移动
- `copy(src_dir, dst_dir, names)` - 复制文件
- `remove(dir, names)` - 删除文件
- `remove_empty_directory(src_dir)` - 删除空文件夹
- `add_offline_download(urls, path, tool)` - 添加离线下载
- `form_upload(file_path, as_task, dst_dir)` - 表单上传文件
- `stream_upload(file_data, file_name, dst_dir, as_task)` - 流式上传文件

### 公共模块 (`client.public`)

- `get_settings()` - 获取站点设置
- `ping()` - Ping检测

### 管理员模块

#### 元信息管理 (`client.admin.meta`)

- `list(page, per_page)` - 列出元信息
- `get(id)` - 获取元信息
- `create(...)` - 新增元信息
- `update(...)` - 更新元信息
- `delete(id)` - 删除元信息

#### 用户管理 (`client.admin.user`)

- `list(page, per_page)` - 列出所有用户
- `get(id)` - 获取用户信息
- `create(username, password, role, ...)` - 新建用户
- `update(id, username, password, role, ...)` - 更新用户
- `cancel_2fa(id)` - 取消两步验证
- `delete(id)` - 删除用户
- `delete_cache(username)` - 删除用户缓存

#### 存储管理 (`client.admin.storage`)

- `list(page, per_page)` - 列出存储列表
- `create(...)` - 创建存储
- `update(...)` - 更新存储
- `get(id)` - 查询指定存储
- `enable(id)` - 启用存储
- `disable(id)` - 禁用存储
- `delete(id)` - 删除存储
- `load_all()` - 重新加载所有存储

#### 驱动管理 (`client.admin.driver`)

- `list()` - 查询所有驱动配置模板
- `names()` - 列出驱动名列表
- `info(driver)` - 列出特定驱动信息

#### 设置管理 (`client.admin.setting`)

- `list(group)` - 列出设置
- `get(key)` - 获取某项设置
- `save(settings)` - 保存设置
- `delete(key)` - 删除设置
- `reset_token()` - 重置令牌
- `set_aria2(uri, secret)` - 设置aria2
- `set_qbittorrent(url, seedtime)` - 设置qBittorrent

#### 任务管理 (`client.admin.task`)

- `get_info(tid)` - 获取任务信息
- `get_done()` - 获取已完成任务
- `get_undone()` - 获取未完成任务
- `delete(tid)` - 删除任务
- `cancel(tid)` - 取消任务
- `retry(tid)` - 重试任务
- `clear_done()` - 清除已完成任务
- `clear_succeeded()` - 清除已成功任务

## 异常处理

库提供了多种自定义异常类型：

```python
from openlist_api import (
    OpenListAPIError,        # 基础异常
    AuthenticationError,     # 认证失败 (401)
    AuthorizationError,      # 授权失败 (403)
    NotFoundError,          # 资源不存在 (404)
    ValidationError,        # 参数验证失败 (400)
    NetworkError,           # 网络连接错误
    ServerError,            # 服务器错误 (5xx)
)

try:
    client.fs.get("/nonexistent.txt")
except NotFoundError as e:
    print(f"文件不存在: {e.message}")
except NetworkError as e:
    print(f"网络错误: {e.message}")
except OpenListAPIError as e:
    print(f"API错误 [{e.status_code}]: {e.message}")
```

## 类型提示

所有API方法都提供完整的类型提示支持：

```python
from openlist_api.models import ListResponse, FileItem

response: ListResponse = client.fs.list("/")
file: FileItem = response.data.content[0]

# IDE将提供自动补全
print(file.name)      # str
print(file.size)      # int
print(file.is_dir)    # bool
print(file.modified)  # str
```

## 项目结构

```
openlist_api/
├── __init__.py          # 主入口，OpenListClient类
├── client.py            # 基础HTTP客户端
├── models.py            # Pydantic数据模型
├── exceptions.py        # 自定义异常
├── auth.py              # 认证API
├── fs.py                # 文件系统API
├── public.py            # 公共API (待实现)
└── admin/               # 管理员API (待实现)
    ├── __init__.py
    ├── meta.py
    ├── user.py
    ├── storage.py
    ├── driver.py
    ├── setting.py
    └── task.py
```

## 开发状态

### 🎉 项目完成度：100%

所有61个API已全部实现！

| 模块 | 总数 | 已实现 | 完成率 |
|------|------|--------|--------|
| Auth | 5 | 5 | ✅ 100% |
| FileSystem | 16 | 16 | ✅ 100% |
| Public | 2 | 2 | ✅ 100% |
| Admin.Meta | 5 | 5 | ✅ 100% |
| Admin.User | 7 | 7 | ✅ 100% |
| Admin.Storage | 8 | 8 | ✅ 100% |
| Admin.Driver | 3 | 3 | ✅ 100% |
| Admin.Setting | 7 | 7 | ✅ 100% |
| Admin.Task | 8 | 8 | ✅ 100% |
| **总计** | **61** | **61** | **✅ 100%** |

## 依赖

- Python >= 3.7
- requests >= 2.28.0
- pydantic >= 2.0.0

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 注意事项

1. 所有需要认证的API都需要先调用 `client.set_token()` 设置token
2. 文件路径参数应使用Unix风格的路径（如 `/folder/file.txt`）
3. 删除操作不可逆，请谨慎使用

## 示例代码

更多示例请查看 `examples/` 目录。

---

**项目基于 [OPENLIST_API.md](OPENLIST_API.md) 中的API规范动态生成**
