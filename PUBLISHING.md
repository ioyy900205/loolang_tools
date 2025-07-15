# 发布到 PyPI 指南

本指南将帮助你将 WAV Finder 包发布到 PyPI。

## 准备工作

### 1. 注册 PyPI 账户

如果你还没有 PyPI 账户，请先注册：

1. 访问 https://pypi.org/account/register/
2. 创建账户并验证邮箱
3. 启用双因素认证（推荐）

### 2. 配置认证

创建 `~/.pypirc` 文件来存储你的认证信息：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

**注意：**
- 将 `pypi-your-token-here` 替换为你的实际 PyPI token
- 将 `pypi-your-test-token-here` 替换为你的实际 TestPyPI token
- 你可以在 https://pypi.org/manage/account/token/ 获取 token

## 发布步骤

### 方法 1: 使用发布脚本（推荐）

```bash
python3 publish.py
```

这个脚本会自动：
1. 清理之前的构建文件
2. 构建新的包
3. 检查包的有效性
4. 提供发布选项

### 方法 2: 手动发布

#### 1. 构建包

```bash
# 清理之前的构建
rm -rf build/ dist/ *.egg-info/

# 构建包
python3 -m build
```

#### 2. 检查包

```bash
python3 -m twine check dist/*
```

#### 3. 发布到 TestPyPI（推荐先测试）

```bash
python3 -m twine upload --repository testpypi dist/*
```

#### 4. 发布到 PyPI

```bash
python3 -m twine upload dist/*
```

## 验证发布

发布成功后，你可以：

1. 检查包是否可用：
   ```bash
   pip install wav-loo
   ```

2. 测试功能：
   ```bash
   wav-loo --help
   ```

3. 访问包页面：
   - PyPI: https://pypi.org/project/wav-loo/
   - TestPyPI: https://test.pypi.org/project/wav-loo/

## 更新包

要更新包版本：

1. 修改 `setup.py` 和 `pyproject.toml` 中的版本号
2. 更新 `wav_loo/__init__.py` 中的版本号
3. 重新构建和发布

## 常见问题

### 1. 包名冲突

如果包名 `wav-loo` 已被占用，请修改：
- `setup.py` 中的 `name` 字段
- `pyproject.toml` 中的 `name` 字段
- 重新构建和发布

### 2. 认证失败

确保：
- `~/.pypirc` 文件配置正确
- Token 有效且未过期
- 网络连接正常

### 3. 构建失败

检查：
- 所有依赖是否正确安装
- Python 版本是否符合要求（>=3.7）
- 文件结构是否正确

## 安全注意事项

1. **不要将 token 提交到版本控制**
2. **使用环境变量存储敏感信息**
3. **定期轮换 token**
4. **启用双因素认证**

## 支持

如果遇到问题，请：
1. 检查错误信息
2. 查看 PyPI 文档
3. 在 GitHub 上提交 issue 