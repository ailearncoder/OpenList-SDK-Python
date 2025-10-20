# 贡献指南

感谢您对OpenList API Python客户端库的关注！我们欢迎各种形式的贡献。

## 🚀 如何贡献

### 1. Fork项目

点击GitHub页面右上角的"Fork"按钮。

### 2. 克隆仓库

```bash
git clone https://github.com/your-username/openlist_api.git
cd openlist_api
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 设置开发环境

```bash
# 安装依赖
pip install -r requirements.txt

# 安装开发工具（可选）
pip install black flake8 mypy
```

### 5. 进行修改

按照项目的代码规范进行开发。

### 6. 运行测试

```bash
# 运行所有测试
pytest tests/

# 检查代码覆盖率
pytest --cov=openlist_api tests/
```

### 7. 提交代码

```bash
git add .
git commit -m "feat: 添加新功能"
git push origin feature/your-feature-name
```

### 8. 创建Pull Request

在GitHub上创建Pull Request，描述您的修改。

## 📝 开发规范

### 代码风格

- 遵循 PEP 8 代码规范
- 使用 4 空格缩进
- 行长度不超过 100 字符
- 使用类型提示

### 文档字符串

所有公共函数必须包含文档字符串：

```python
def example_function(param1: str, param2: int = 0) -> str:
    """函数简短描述。
    
    详细描述（可选）。
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述，默认为0
        
    Returns:
        返回值的描述
        
    Raises:
        ValueError: 何时抛出此异常
        
    Example:
        >>> result = example_function("test", 1)
        >>> print(result)
        'test1'
    """
    return param1 + str(param2)
```

### 提交消息

使用约定式提交 (Conventional Commits):

- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式化
- `refactor:` 重构代码
- `test:` 添加测试
- `chore:` 其他修改

示例：
```
feat: 添加批量重命名API
fix: 修复文件上传错误
docs: 更新README示例
```

## 🔧 添加新API

按照以下步骤添加新的API：

### 1. 获取API规范

```python
from openlist_api.utils import fetch_content

spec = fetch_content("https://openlist.apifox.cn/api-xxx.md")
```

### 2. 定义数据模型

在 `models.py` 中添加响应模型：

```python
class NewAPIData(BaseModel):
    """新API响应数据。"""
    field1: str = Field(..., description="字段1")
    field2: int = Field(..., description="字段2")

class NewAPIResponse(BaseResponse):
    """新API响应。"""
    data: NewAPIData = Field(..., description="数据")
```

### 3. 实现API函数

在相应模块（如 `fs.py`）中添加函数：

```python
def new_api(self, param1: str, param2: int = 0) -> NewAPIResponse:
    """新API功能描述。
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
        
    Returns:
        NewAPIResponse: 响应对象
        
    Raises:
        AuthenticationError: 认证失败
        ValidationError: 参数错误
        
    Example:
        >>> result = api.new_api("value", 123)
        >>> print(result.data.field1)
    """
    payload = {"param1": param1, "param2": param2}
    response_data = self.client.post("/api/new", json=payload)
    return NewAPIResponse(**response_data)
```

### 4. 添加测试

在 `tests/` 中添加测试：

```python
def test_new_api(self, mock_request):
    """测试新API"""
    # 准备mock响应
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {...}
    mock_request.return_value = mock_response
    
    # 执行测试
    client = OpenListClient("http://test.com")
    result = client.module.new_api("test", 1)
    
    # 验证结果
    assert result.data.field1 == "expected"
```

### 5. 更新文档

- 在 README.md 中添加API说明
- 在 CHANGELOG.md 中记录变更
- 更新 PROJECT_SUMMARY.md 的进度

## 🐛 报告Bug

发现bug？请[创建Issue](https://github.com/your-repo/issues/new)，包含：

1. **问题描述** - 简短描述问题
2. **复现步骤** - 如何重现问题
3. **预期行为** - 应该发生什么
4. **实际行为** - 实际发生了什么
5. **环境信息** - Python版本、操作系统等
6. **错误日志** - 完整的错误信息

## 💡 提出建议

有新想法？请[创建Issue](https://github.com/your-repo/issues/new)，包含：

1. **功能描述** - 详细描述建议的功能
2. **使用场景** - 为什么需要此功能
3. **预期行为** - 如何使用此功能
4. **其他信息** - 相关链接、示例等

## 📋 开发待办

查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解待实现的API。

优先级：
1. 🔥 **高优先级** - 完成文件系统模块剩余API
2. 📝 **中优先级** - 实现公共模块API
3. 🔧 **低优先级** - 实现管理员模块API

## 🤝 行为准则

- 尊重他人
- 接受建设性批评
- 专注于对社区最有利的事情
- 表现出对社区成员的同理心

## ❓ 获取帮助

- 查看 [README.md](README.md) 了解基本用法
- 查看 [QUICKSTART.md](QUICKSTART.md) 快速上手
- 查看现有的 [Issues](https://github.com/your-repo/issues)
- 在 [Discussions](https://github.com/your-repo/discussions) 提问

## 📜 许可证

贡献代码即表示您同意以 MIT 许可证授权您的贡献。

---

感谢您的贡献！🎉
