# OpenList API - Python Client Library

English | [简体中文](README.md)

A full-featured Python client library for interacting with the OpenList (AList) API. Provides complete type hints, docstrings, and exception handling.

## Features

✅ **Full Type Support** - Strong typing with Pydantic models  
✅ **Clear Documentation** - Detailed docstrings for every function  
✅ **Robust Error Handling** - Custom exception types for graceful error handling  
✅ **Modular Design** - APIs organized by functional modules  
✅ **Easy to Use** - Simple and intuitive API design  
✅ **100% Complete** - All 61 APIs fully implemented  

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from openlist_api import OpenListClient

# Create client instance
client = OpenListClient("http://localhost:5244")

# Login to get token
login_response = client.auth.login("admin", "password")
client.set_token(login_response.data.token)

# List files in root directory
files = client.fs.list("/")
for file in files.data.content:
    print(f"{file.name} ({'directory' if file.is_dir else 'file'})")
```

### Authentication

```python
# Method 1: Plain password login
response = client.auth.login("username", "password")
print(response.data.token)

# Method 2: Hash password login (more secure)
response = client.auth.login_hash("username", "password")

# Get current user info
user_info = client.auth.get_current_user()
print(f"Username: {user_info.data.username}")
print(f"Role: {user_info.data.role}")

# Generate 2FA secret
twofa = client.auth.generate_2fa()
print(f"Secret: {twofa.data.secret}")
print(f"QR Code: {twofa.data.qr[:50]}...")

# Verify 2FA code
client.auth.verify_2fa("123456", "your_secret")
```

### File System Operations

```python
# List directory contents
files = client.fs.list("/documents", page=1, per_page=50)
print(f"Total: {files.data.total} items")

# Get file/directory info
file_info = client.fs.get("/document.pdf")
print(f"File size: {file_info.data.size} bytes")
print(f"Download URL: {file_info.data.raw_url}")

# Search files
results = client.fs.search("/", "test", scope=2)  # scope=2: files only
for item in results.data.content:
    print(f"Found: {item.parent}/{item.name}")

# Create folder
client.fs.mkdir("/new_folder")

# Rename file
client.fs.rename("/old_name.txt", "new_name.txt")

# Batch rename
from openlist_api.models import RenameObject
renames = [
    RenameObject(src_name="a.txt", new_name="1.txt"),
    RenameObject(src_name="b.txt", new_name="2.txt")
]
client.fs.batch_rename("/folder", renames)

# Regex rename
client.fs.regex_rename("/folder", r"^(.+)\.txt$", r"\1.bak")

# Move files
client.fs.move("/source_dir", "/target_dir", ["file1.txt", "file2.txt"])

# Copy files
client.fs.copy("/source_dir", "/target_dir", ["file.txt"])

# Delete files
client.fs.remove("/documents", ["unwanted.txt"])
```

### Admin Operations

```python
# User management
users = client.admin.user.list()
for user in users.data.content:
    print(f"{user.username}: {user.role}")

# Create user
client.admin.user.create(
    username="newuser",
    password="pass123",
    role=0
)

# Storage management
storages = client.admin.storage.list()
for storage in storages.data.content:
    print(f"{storage.mount_path}: {storage.driver}")

# Task management
tasks = client.admin.task.get_undone()
for task in tasks:
    print(f"Task {task['id']}: {task['name']}")
```

## API Modules

### Authentication Module (`client.auth`)

- `login(username, password, otp_code)` - Login to get token
- `login_hash(username, password, otp_code)` - Login with hashed password
- `generate_2fa()` - Generate 2FA secret
- `verify_2fa(code, secret)` - Verify 2FA code
- `get_current_user()` - Get current user info

### File System Module (`client.fs`)

- `list(path, password, page, per_page, refresh)` - List directory contents
- `get(path, password, page, per_page, refresh)` - Get file/directory info
- `dirs(path, password, force_root)` - Get all subdirectories
- `search(parent, keywords, scope, page, per_page, password)` - Search files
- `mkdir(path)` - Create folder
- `rename(path, name)` - Rename file
- `batch_rename(src_dir, rename_objects)` - Batch rename
- `regex_rename(src_dir, src_name_regex, new_name_regex)` - Regex rename
- `move(src_dir, dst_dir, names)` - Move files
- `recursive_move(src_dir, dst_dir)` - Recursive move
- `copy(src_dir, dst_dir, names)` - Copy files
- `remove(dir, names)` - Delete files
- `remove_empty_directory(src_dir)` - Remove empty directory
- `add_offline_download(urls, path, tool)` - Add offline download
- `form_upload(file_path, as_task, dst_dir)` - Form upload
- `stream_upload(file_data, file_name, dst_dir, as_task)` - Stream upload

### Public Module (`client.public`)

- `get_settings()` - Get site settings
- `ping()` - Ping test

### Admin Modules

#### Meta Management (`client.admin.meta`)

- `list(page, per_page)` - List meta info
- `get(id)` - Get meta info
- `create(...)` - Create meta info
- `update(...)` - Update meta info
- `delete(id)` - Delete meta info

#### User Management (`client.admin.user`)

- `list(page, per_page)` - List all users
- `get(id)` - Get user info
- `create(username, password, role, ...)` - Create user
- `update(id, username, password, role, ...)` - Update user
- `cancel_2fa(id)` - Cancel 2FA
- `delete(id)` - Delete user
- `delete_cache(username)` - Delete user cache

#### Storage Management (`client.admin.storage`)

- `list(page, per_page)` - List storages
- `create(...)` - Create storage
- `update(...)` - Update storage
- `get(id)` - Get storage info
- `enable(id)` - Enable storage
- `disable(id)` - Disable storage
- `delete(id)` - Delete storage
- `load_all()` - Reload all storages

#### Driver Management (`client.admin.driver`)

- `list()` - List all driver templates
- `names()` - List driver names
- `info(driver)` - Get driver info

#### Settings Management (`client.admin.setting`)

- `list(group)` - List settings
- `get(key)` - Get a setting
- `save(settings)` - Save settings
- `delete(key)` - Delete setting
- `reset_token()` - Reset token
- `set_aria2(uri, secret)` - Configure aria2
- `set_qbittorrent(url, seedtime)` - Configure qBittorrent

#### Task Management (`client.admin.task`)

- `get_info(tid)` - Get task info
- `get_done()` - Get completed tasks
- `get_undone()` - Get uncompleted tasks
- `delete(tid)` - Delete task
- `cancel(tid)` - Cancel task
- `retry(tid)` - Retry task
- `clear_done()` - Clear completed tasks
- `clear_succeeded()` - Clear succeeded tasks

## Exception Handling

The library provides multiple custom exception types:

```python
from openlist_api import (
    OpenListAPIError,        # Base exception
    AuthenticationError,     # Authentication failed (401)
    AuthorizationError,      # Authorization failed (403)
    NotFoundError,          # Resource not found (404)
    ValidationError,        # Validation failed (400)
    NetworkError,           # Network error
    ServerError,            # Server error (5xx)
)

try:
    client.fs.get("/nonexistent.txt")
except NotFoundError as e:
    print(f"File not found: {e.message}")
except NetworkError as e:
    print(f"Network error: {e.message}")
except OpenListAPIError as e:
    print(f"API error [{e.status_code}]: {e.message}")
```

## Type Hints

All API methods provide full type hint support:

```python
from openlist_api.models import ListResponse, FileItem

response: ListResponse = client.fs.list("/")
file: FileItem = response.data.content[0]

# IDE will provide auto-completion
print(file.name)      # str
print(file.size)      # int
print(file.is_dir)    # bool
print(file.modified)  # str
```

## Project Structure

```
openlist_api/
├── __init__.py          # Main entry, OpenListClient class
├── client.py            # Base HTTP client
├── models.py            # Pydantic data models
├── exceptions.py        # Custom exceptions
├── auth.py              # Authentication API
├── fs.py                # File system API
├── public.py            # Public API
└── admin/               # Admin APIs
    ├── __init__.py
    ├── meta.py          # Meta management
    ├── user.py          # User management
    ├── storage.py       # Storage management
    ├── driver.py        # Driver management
    ├── setting.py       # Settings management
    └── task.py          # Task management
```

## Development Status

### 🎉 Project Completion: 100%

All 61 APIs have been fully implemented!

| Module | Total | Implemented | Completion |
|--------|-------|-------------|------------|
| Auth | 5 | 5 | ✅ 100% |
| FileSystem | 16 | 16 | ✅ 100% |
| Public | 2 | 2 | ✅ 100% |
| Admin.Meta | 5 | 5 | ✅ 100% |
| Admin.User | 7 | 7 | ✅ 100% |
| Admin.Storage | 8 | 8 | ✅ 100% |
| Admin.Driver | 3 | 3 | ✅ 100% |
| Admin.Setting | 7 | 7 | ✅ 100% |
| Admin.Task | 8 | 8 | ✅ 100% |
| **Total** | **61** | **61** | **✅ 100%** |

## Dependencies

- Python >= 3.7
- requests >= 2.28.0
- pydantic >= 2.0.0

## License

MIT License

## Contributing

Issues and Pull Requests are welcome!

## Notes

1. All APIs requiring authentication need `client.set_token()` to be called first
2. File path parameters should use Unix-style paths (e.g., `/folder/file.txt`)
3. Delete operations are irreversible, use with caution
4. Admin module APIs require administrator privileges

## Examples

More examples can be found in the `examples/` directory.

## Technical Highlights

### 1. Modular Design
- Clear namespace organization
- Organized by functionality
- Easy to extend and maintain

### 2. Type Safety
- Full type annotations
- IDE auto-completion support
- Static type checking friendly

### 3. Complete Documentation
- PEP 257 compliant docstrings
- Usage examples for every API
- Detailed parameter and exception descriptions

### 4. Error Handling
- Layered exception hierarchy
- Clear error messages
- Graceful error recovery

### 5. Development Standards
- Strict adherence to iterative development process
- Based on real OpenAPI specifications
- High code quality standards

---

**Project based on the API specifications in [OPENLIST_API.md](OPENLIST_API.md)**
