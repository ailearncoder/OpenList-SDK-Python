"""数据模型定义。

包含所有API响应的数据结构定义。
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, List


class BaseResponse(BaseModel):
    """通用API响应基类。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 响应数据
    """
    code: int = Field(..., description="状态码")
    message: str = Field(..., description="响应消息")
    data: Any = Field(..., description="响应数据")


# ==================== Auth Models ====================

class LoginData(BaseModel):
    """登录响应数据。
    
    Attributes:
        token: JWT token字符串
    """
    token: str = Field(..., description="JWT token")


class LoginResponse(BaseResponse):
    """登录API响应。
    
    Attributes:
        code: 状态码，200表示成功
        message: 响应消息
        data: 包含token的数据对象
    """
    data: LoginData = Field(..., description="登录数据")


class Generate2FAData(BaseModel):
    """生成2FA密钥响应数据。
    
    Attributes:
        qr: 二维码图片的data URL
        secret: 2FA密钥
    """
    qr: str = Field(..., description="二维码图片的data URL")
    secret: str = Field(..., description="2FA密钥")


class Generate2FAResponse(BaseResponse):
    """生成2FA密钥API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 2FA密钥和二维码数据
    """
    data: Generate2FAData = Field(..., description="2FA数据")


class UserInfo(BaseModel):
    """用户信息数据。
    
    Attributes:
        id: 用户ID
        username: 用户名
        password: 密码（通常为空）
        base_path: 用户根目录
        role: 用户角色 (0:普通用户, 1:管理员, 2:超级管理员)
        disabled: 是否被禁用
        permission: 用户权限
        sso_id: SSO ID
        otp: 是否开启两步验证
    """
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    base_path: str = Field(..., description="用户根目录")
    role: int = Field(..., description="用户角色")
    disabled: bool = Field(..., description="是否被禁用")
    permission: int = Field(..., description="用户权限")
    sso_id: str = Field(..., description="SSO ID")
    otp: bool = Field(..., description="是否开启两步验证")


class UserInfoResponse(BaseResponse):
    """获取用户信息API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 用户信息数据
    """
    data: UserInfo = Field(..., description="用户信息")


# ==================== File System Models ====================

class FileItem(BaseModel):
    """文件/目录项数据。
    
    Attributes:
        name: 文件名
        size: 文件大小（字节）
        is_dir: 是否是文件夹
        modified: 修改时间
        created: 创建时间
        sign: 签名
        thumb: 缩略图链接
        type: 文件类型
        hashinfo: hash信息字符串
        hash_info: hash信息对象
    """
    name: str = Field(..., description="文件名")
    size: int = Field(..., description="文件大小")
    is_dir: bool = Field(..., description="是否是文件夹")
    modified: str = Field(..., description="修改时间")
    sign: str = Field(..., description="签名")
    thumb: str = Field(..., description="缩略图")
    type: int = Field(..., description="文件类型")
    created: Optional[str] = Field(None, description="创建时间")
    hashinfo: Optional[str] = Field(None, description="hash信息")
    hash_info: Optional[Any] = Field(None, description="hash信息对象")


class ListData(BaseModel):
    """列出文件目录响应数据。
    
    Attributes:
        content: 文件列表
        total: 总数
        readme: README内容
        header: 头部信息
        write: 是否可写
        provider: 存储提供者
    """
    content: List[FileItem] = Field(..., description="文件列表")
    total: int = Field(..., description="总数")
    readme: str = Field(..., description="README内容")
    header: str = Field(..., description="头部信息")
    write: bool = Field(..., description="是否可写")
    provider: str = Field(..., description="存储提供者")


class ListResponse(BaseResponse):
    """列出文件目录API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 文件列表数据
    """
    data: ListData = Field(..., description="文件列表数据")


class FileInfoData(BaseModel):
    """文件/目录详细信息数据。
    
    Attributes:
        name: 文件名
        size: 文件大小
        is_dir: 是否是文件夹
        modified: 修改时间
        created: 创建时间
        sign: 签名
        thumb: 缩略图
        type: 文件类型
        hashinfo: hash信息
        hash_info: hash信息对象
        raw_url: 原始URL
        readme: README内容
        header: 头部信息
        provider: 存储提供者
        related: 相关信息
    """
    name: str = Field(..., description="文件名")
    size: int = Field(..., description="文件大小")
    is_dir: bool = Field(..., description="是否是文件夹")
    modified: str = Field(..., description="修改时间")
    created: str = Field(..., description="创建时间")
    sign: str = Field(..., description="签名")
    thumb: str = Field(..., description="缩略图")
    type: int = Field(..., description="文件类型")
    hashinfo: str = Field(..., description="hash信息")
    hash_info: Optional[Any] = Field(..., description="hash信息对象")
    raw_url: str = Field(..., description="原始URL")
    readme: str = Field(..., description="README内容")
    header: str = Field(..., description="头部信息")
    provider: str = Field(..., description="存储提供者")
    related: Optional[Any] = Field(..., description="相关信息")


class FileInfoResponse(BaseResponse):
    """获取文件/目录信息API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 文件信息
    """
    data: FileInfoData = Field(..., description="文件信息")


class DirItem(BaseModel):
    """目录项数据。
    
    Attributes:
        name: 目录名
        modified: 修改时间
    """
    name: str = Field(..., description="目录名")
    modified: str = Field(..., description="修改时间")


class DirsResponse(BaseResponse):
    """获取目录API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 目录列表
    """
    data: List[DirItem] = Field(..., description="目录列表")


class SearchResultItem(BaseModel):
    """搜索结果项数据。
    
    Attributes:
        parent: 父目录路径
        name: 文件/目录名
        is_dir: 是否是文件夹
        size: 大小
        type: 类型
    """
    parent: str = Field(..., description="父目录路径")
    name: str = Field(..., description="文件/目录名")
    is_dir: bool = Field(..., description="是否是文件夹")
    size: int = Field(..., description="大小")
    type: int = Field(..., description="类型")


class SearchData(BaseModel):
    """搜索响应数据。
    
    Attributes:
        content: 搜索结果列表
        total: 总数
    """
    content: List[SearchResultItem] = Field(..., description="搜索结果列表")
    total: int = Field(..., description="总数")


class SearchResponse(BaseResponse):
    """搜索API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 搜索结果
    """
    data: SearchData = Field(..., description="搜索结果")


class RenameObject(BaseModel):
    """批量重命名对象。
    
    Attributes:
        src_name: 原文件名
        new_name: 新文件名
    """
    src_name: str = Field(..., description="原文件名")
    new_name: str = Field(..., description="新文件名")


class TaskInfo(BaseModel):
    """任务信息。
    
    Attributes:
        id: 任务ID
        name: 任务名称
        state: 任务状态 (0:等待中, 1:运行中, 2:已完成, 3:已失败, 4:已取消)
        status: 状态描述
        progress: 进度 (0-100)
        error: 错误信息
    """
    id: str = Field(..., description="任务ID")
    name: str = Field(..., description="任务名称")
    state: int = Field(..., description="任务状态")
    status: str = Field(..., description="状态描述")
    progress: int = Field(..., description="进度")
    error: str = Field(..., description="错误信息")


class OfflineDownloadData(BaseModel):
    """离线下载响应数据。
    
    Attributes:
        tasks: 创建的任务列表
    """
    tasks: List[TaskInfo] = Field(..., description="任务列表")


class OfflineDownloadResponse(BaseResponse):
    """离线下载API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 任务列表
    """
    data: OfflineDownloadData = Field(..., description="任务列表")


class UploadTaskData(BaseModel):
    """上传任务响应数据。
    
    Attributes:
        task: 任务信息
    """
    task: TaskInfo = Field(..., description="任务信息")


class UploadResponse(BaseResponse):
    """上传文件API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 任务信息
    """
    data: UploadTaskData = Field(..., description="任务信息")


# ==================== Public Models ====================

class SiteSettings(BaseModel):
    """站点设置数据。
    
    Attributes:
        allow_indexed: 允许索引
        allow_mounted: 允许挂载
        announcement: 公告
        audio_autoplay: 自动播放音频
        audio_cover: 音频封面
        auto_update_index: 自动更新索引
        default_page_size: 默认分页数
        external_previews: 外部预览
        favicon: 网站图标
        filename_char_mapping: 文件名字符映射
        forward_direct_link_params: 转发直接链接参数
        hide_files: 隐藏文件
        home_container: 主页容器
        home_icon: 主页图标
        iframe_previews: iframe预览设置
        logo: logo
        main_color: 主题颜色
        ocr_api: OCR接口
        package_download: 打包下载
        pagination_type: 分页类型
        robots_txt: robots文件
        search_index: 搜索索引
        settings_layout: 设置布局
        site_title: 站点标题
        sso_login_enabled: 启用SSO登录
        sso_login_platform: SSO登录平台
        version: 版本
        video_autoplay: 视频自动播放
    """
    allow_indexed: str = Field(..., description="允许索引")
    allow_mounted: str = Field(..., description="允许挂载")
    announcement: str = Field(..., description="公告")
    audio_autoplay: str = Field(..., description="自动播放音频")
    audio_cover: str = Field(..., description="音频封面")
    auto_update_index: str = Field(..., description="自动更新索引")
    default_page_size: str = Field(..., description="默认分页数")
    external_previews: str = Field(..., description="外部预览")
    favicon: str = Field(..., description="网站图标")
    filename_char_mapping: str = Field(..., description="文件名字符映射")
    forward_direct_link_params: str = Field(..., description="转发直接链接参数")
    hide_files: str = Field(..., description="隐藏文件")
    home_container: str = Field(..., description="主页容器")
    home_icon: str = Field(..., description="主页图标")
    iframe_previews: str = Field(..., description="iframe预览设置")
    logo: str = Field(..., description="logo")
    main_color: str = Field(..., description="主题颜色")
    ocr_api: str = Field(..., description="OCR接口")
    package_download: str = Field(..., description="打包下载")
    pagination_type: str = Field(..., description="分页类型")
    robots_txt: str = Field(..., description="robots文件")
    search_index: str = Field(..., description="搜索索引")
    settings_layout: str = Field(..., description="设置布局")
    site_title: str = Field(..., description="站点标题")
    sso_login_enabled: str = Field(..., description="启用SSO登录")
    sso_login_platform: str = Field(..., description="SSO登录平台")
    version: str = Field(..., description="版本")
    video_autoplay: str = Field(..., description="视频自动播放")


class SiteSettingsResponse(BaseResponse):
    """获取站点设置API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 站点设置数据
    """
    data: SiteSettings = Field(..., description="站点设置数据")


# ==================== Admin Meta Models ====================

class MetaInfo(BaseModel):
    """元信息数据。
    
    Attributes:
        id: 元信息ID
        path: 路径
        password: 密码
        p_sub: 密码是否应用到子文件夹
        write: 是否允许写入
        w_sub: 写入是否应用到子文件夹
        hide: 隐藏规则
        h_sub: 隐藏是否应用到子文件夹
        readme: 说明文档
        r_sub: 说明是否应用到子文件夹
    """
    id: int = Field(..., description="元信息ID")
    path: str = Field(..., description="路径")
    password: str = Field(..., description="密码")
    p_sub: bool = Field(..., description="密码是否应用到子文件夹")
    write: bool = Field(..., description="是否允许写入")
    w_sub: bool = Field(..., description="写入是否应用到子文件夹")
    hide: str = Field(..., description="隐藏规则")
    h_sub: bool = Field(..., description="隐藏是否应用到子文件夹")
    readme: str = Field(..., description="说明文档")
    r_sub: bool = Field(..., description="说明是否应用到子文件夹")


class MetaListData(BaseModel):
    """元信息列表数据。
    
    Attributes:
        content: 元信息列表
        total: 总数
    """
    content: List[MetaInfo] = Field(..., description="元信息列表")
    total: int = Field(..., description="总数")


class MetaListResponse(BaseResponse):
    """列出元信息API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 元信息列表数据
    """
    data: MetaListData = Field(..., description="元信息列表数据")


class MetaResponse(BaseResponse):
    """单个元信息API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 元信息数据
    """
    data: MetaInfo = Field(..., description="元信息数据")


# ==================== Admin User Models ====================

class UserListData(BaseModel):
    """用户列表数据。
    
    Attributes:
        content: 用户列表
        total: 总数
    """
    content: List[UserInfo] = Field(..., description="用户列表")
    total: int = Field(..., description="总数")


class UserListResponse(BaseResponse):
    """列出用户API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 用户列表数据
    """
    data: UserListData = Field(..., description="用户列表数据")


# ==================== Admin Storage Models ====================

class StorageInfo(BaseModel):
    """存储信息数据。
    
    Attributes:
        id: 存储ID
        mount_path: 挂载路径
        order: 排序
        driver: 驱动
        cache_expiration: 缓存过期时间
        status: 状态
        addition: 额外信息
        remark: 备注
        modified: 修改时间
        disabled: 是否禁用
        enable_sign: 启用签名
        order_by: 排序方式
        order_direction: 排序方向
        extract_folder: 提取目录
        web_proxy: web代理
        webdav_policy: webdav策略
        down_proxy_url: 下载代理URL
    """
    id: int = Field(..., description="存储ID")
    mount_path: str = Field(..., description="挂载路径")
    order: int = Field(..., description="排序")
    driver: str = Field(..., description="驱动")
    cache_expiration: int = Field(..., description="缓存过期时间")
    status: str = Field(..., description="状态")
    addition: str = Field(..., description="额外信息")
    remark: str = Field(..., description="备注")
    modified: str = Field(..., description="修改时间")
    disabled: bool = Field(..., description="是否禁用")
    enable_sign: Optional[bool] = Field(None, description="启用签名")
    order_by: str = Field(..., description="排序方式")
    order_direction: str = Field(..., description="排序方向")
    extract_folder: str = Field(..., description="提取目录")
    web_proxy: bool = Field(..., description="web代理")
    webdav_policy: str = Field(..., description="webdav策略")
    down_proxy_url: str = Field(..., description="下载代理URL")


class StorageListData(BaseModel):
    """存储列表数据。
    
    Attributes:
        content: 存储列表
        total: 总数
    """
    content: List[StorageInfo] = Field(..., description="存储列表")
    total: int = Field(..., description="总数")


class StorageListResponse(BaseResponse):
    """列出存储API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 存储列表数据
    """
    data: StorageListData = Field(..., description="存储列表数据")


class StorageResponse(BaseResponse):
    """单个存储API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 存储信息
    """
    data: StorageInfo = Field(..., description="存储信息")


class StorageIDData(BaseModel):
    """存储ID数据。
    
    Attributes:
        id: 存储ID
    """
    id: int = Field(..., description="存储ID")


class StorageIDResponse(BaseResponse):
    """创建/更新存储API响应。
    
    Attributes:
        code: 状态码
        message: 响应消息
        data: 包含ID的数据
    """
    data: StorageIDData = Field(..., description="存储ID数据")
