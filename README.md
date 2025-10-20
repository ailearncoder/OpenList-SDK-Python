# OpenList API - Python客户端库

一个功能完整的Python客户端库，用于与OpenList (AList) API进行交互。提供了完整的类型提示、文档字符串和异常处理。

## 特性

✅ **完整的类型支持** - 使用Pydantic模型提供强类型返回值  
✅ **清晰的文档** - 每个函数都有详细的Docstrings  
✅ **健壮的错误处理** - 自定义异常类型，优雅处理各种错误  
✅ **模块化设计** - 按功能模块组织API  
✅ **易于使用** - 简洁直观的API设计  

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
- `move(src_dir, dst_dir, names)` - 移动文件
- `copy(src_dir, dst_dir, names)` - 复制文件
- `remove(dir, names)` - 删除文件

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

### ✅ 已实现的模块

- **认证模块** (5/5 APIs)
  - ✅ token获取
  - ✅ token获取hash
  - ✅ 生成2FA密钥
  - ✅ 验证2FA code
  - ✅ 获取当前用户信息

- **文件系统模块** (9/21 APIs)
  - ✅ 列出文件目录
  - ✅ 获取文件/目录信息
  - ✅ 获取目录
  - ✅ 搜索文件或文件夹
  - ✅ 新建文件夹
  - ✅ 重命名文件
  - ✅ 移动文件
  - ✅ 复制文件
  - ✅ 删除文件或文件夹

### 🚧 待实现的模块

- **文件系统模块** (剩余12个APIs)
  - 批量重命名
  - 正则重命名
  - 聚合移动
  - 删除空文件夹
  - 添加离线下载
  - 表单上传文件
  - 流式上传文件
  - 等...

- **公共模块** (2个APIs)
  - 获取站点设置
  - ping检测

- **管理员模块** (44个APIs)
  - 元信息管理
  - 用户管理
  - 存储管理
  - 驱动管理
  - 设置管理
  - 任务管理

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

**项目基于 [openlist.md](openlist.md) 中的API规范动态生成**
