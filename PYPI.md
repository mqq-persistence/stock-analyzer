# PyPI 发布指南

## 发布到 PyPI

### 步骤 1: 获取 PyPI API Token

1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API token
3. 复制 token（只显示一次）

### 步骤 2: 在 GitHub 配置 Secret

1. 访问仓库：https://github.com/mqq-persistence/stock-analyzer/settings/secrets/actions
2. 添加新的 secret：
   - Name: `PYPI_API_TOKEN`
   - Value: 粘贴你的 PyPI token

### 步骤 3: 创建 GitHub Release

1. 访问 https://github.com/mqq-persistence/stock-analyzer/releases
2. 创建新的 Release
3. 设置版本号（如 `v0.1.0`）
4. 发布后会自动触发 CI 发布到 PyPI

---

## 本地手动发布

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 测试上传到 TestPyPI
python -m twine upload --repository testpypi dist/*

# 正式上传到 PyPI
python -m twine upload dist/*
```

---

## 验证发布

```bash
# 测试安装包
pip install stock-analyzer-cn

# 使用命令行工具
stock-analyzer
```

---

## 版本号说明

遵循 [Semantic Versioning](https://semver.org/):

- `0.1.0` - 初始版本
- `0.1.1` - Bug 修复
- `0.2.0` - 新功能
- `1.0.0` - 稳定版本

更新版本号在 `pyproject.toml` 中。

---

## PyPI 项目页面

发布后可在以下地址访问：
- **PyPI**: https://pypi.org/project/stock-analyzer-cn/
- **TestPyPI**: https://test.pypi.org/project/stock-analyzer-cn/
