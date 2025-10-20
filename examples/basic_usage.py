"""
OpenList API 使用示例

演示如何使用openlist_api库进行常见操作。
"""

from openlist_api import OpenListClient, AuthenticationError, NotFoundError

def main():
    # 1. 创建客户端
    print("=== 创建客户端 ===")
    client = OpenListClient("http://localhost:5244")
    
    # 2. 登录
    print("\n=== 用户登录 ===")
    try:
        login_response = client.auth.login("admin", "password")
        print(f"登录成功！Token: {login_response.data.token[:50]}...")
        client.set_token(login_response.data.token)
    except AuthenticationError as e:
        print(f"登录失败: {e.message}")
        return
    
    # 3. 获取当前用户信息
    print("\n=== 获取用户信息 ===")
    user_info = client.auth.get_current_user()
    print(f"用户名: {user_info.data.username}")
    print(f"角色: {user_info.data.role}")
    print(f"根目录: {user_info.data.base_path}")
    print(f"2FA已启用: {user_info.data.otp}")
    
    # 4. 列出根目录文件
    print("\n=== 列出根目录 ===")
    files = client.fs.list("/")
    print(f"总共 {files.data.total} 个项目:")
    for item in files.data.content[:5]:  # 只显示前5个
        file_type = "📁 目录" if item.is_dir else "📄 文件"
        size = f"{item.size / 1024:.2f} KB" if not item.is_dir else "-"
        print(f"  {file_type} {item.name:30} {size:>15}")
    
    # 5. 搜索文件
    print("\n=== 搜索文件 ===")
    try:
        search_results = client.fs.search(
            parent="/",
            keywords="test",
            scope=0,  # 0=全部, 1=仅目录, 2=仅文件
            page=1,
            per_page=10
        )
        print(f"找到 {search_results.data.total} 个结果:")
        for item in search_results.data.content:
            print(f"  {item.parent}/{item.name}")
    except Exception as e:
        print(f"搜索失败: {e}")
    
    # 6. 创建文件夹
    print("\n=== 创建测试文件夹 ===")
    try:
        result = client.fs.mkdir("/test_folder")
        print(f"创建成功: {result.message}")
    except Exception as e:
        print(f"创建失败: {e}")
    
    # 7. 获取文件信息
    print("\n=== 获取文件信息 ===")
    try:
        file_info = client.fs.get("/test_folder")
        print(f"名称: {file_info.data.name}")
        print(f"类型: {'目录' if file_info.data.is_dir else '文件'}")
        print(f"创建时间: {file_info.data.created}")
        print(f"提供者: {file_info.data.provider}")
    except NotFoundError:
        print("文件/目录不存在")
    except Exception as e:
        print(f"获取失败: {e}")
    
    # 8. 列出所有子目录
    print("\n=== 获取所有子目录 ===")
    try:
        dirs = client.fs.dirs("/")
        print(f"找到 {len(dirs.data)} 个子目录:")
        for dir_item in dirs.data[:5]:
            print(f"  📁 {dir_item.name}")
    except Exception as e:
        print(f"获取失败: {e}")
    
    # 9. 文件操作示例（注释掉以避免意外修改）
    print("\n=== 文件操作示例（已注释） ===")
    print("# 重命名: client.fs.rename('/old_name.txt', 'new_name.txt')")
    print("# 移动: client.fs.move('/source', '/target', ['file.txt'])")
    print("# 复制: client.fs.copy('/source', '/target', ['file.txt'])")
    print("# 删除: client.fs.remove('/folder', ['file.txt'])")
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main()

