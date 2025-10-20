# OpenList API - 快速开始指南

## 5分钟上手

### 1. 安装依赖

```bash
cd openlist_api
pip install -r requirements.txt
```

### 2. 创建第一个脚本

创建文件 `my_script.py`:

```python
from openlist_api import OpenListClient

# 创建客户端（替换为你的服务器地址）
client = OpenListClient("http://localhost:5244")

# 登录
response = client.auth.login("admin", "your_password")
print(f"✅ 登录成功！")

# 保存token
client.set_token(response.data.token)

# 列出根目录
files = client.fs.list("/")
print(f"\n📁 根目录有 {files.data.total} 个项目:\n")

for item in files.data.content:
    icon = "📁" if item.is_dir else "📄"
    print(f"{icon} {item.name}")
```

### 3. 运行脚本

```bash
python my_script.py
```

## 常用操作

### 🔐 认证

```python
# 1. 登录
response = client.auth.login("username", "password")
client.set_token(response.data.token)

# 2. 获取当前用户信息
user = client.auth.get_current_user()
print(f"欢迎, {user.data.username}!")
```

### 📂 浏览文件

```python
# 列出目录
files = client.fs.list("/documents")
for f in files.data.content:
    print(f"{f.name} - {f.size} bytes")

# 获取文件信息
info = client.fs.get("/photo.jpg")
print(f"下载链接: {info.data.raw_url}")
```

### 🔍 搜索文件

```python
# 搜索所有包含"报告"的文件
results = client.fs.search("/", "报告", scope=2)  # scope=2表示只搜文件
for item in results.data.content:
    print(f"找到: {item.parent}/{item.name}")
```

### 📝 文件操作

```python
# 创建文件夹
client.fs.mkdir("/新文件夹")

# 重命名
client.fs.rename("/旧名字.txt", "新名字.txt")

# 移动文件
client.fs.move("/source", "/target", ["file.txt"])

# 复制文件
client.fs.copy("/source", "/target", ["file.txt"])

# 删除文件（谨慎！）
# client.fs.remove("/folder", ["file.txt"])
```

## 错误处理

```python
from openlist_api import NotFoundError, AuthenticationError

try:
    client.fs.get("/不存在的文件.txt")
except NotFoundError:
    print("❌ 文件不存在")
except AuthenticationError:
    print("❌ 请先登录")
```

## 完整示例

查看 `examples/basic_usage.py` 获取更多示例。

## 获取帮助

- 查看 [README.md](README.md) 了解详细文档
- 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解实现细节
- 使用 IDE 的自动补全功能查看可用方法

## 下一步

- 探索更多文件系统API
- 学习异常处理最佳实践
- 查看完整API文档

---

开始使用吧！🚀
