# Claude Code Skill 安装和使用指南

## 方案一：使用全局安装脚本（推荐）

### 1. 下载全局安装脚本

```bash
# 创建脚本目录
mkdir -p ~/bin

# 下载安装脚本
curl -o ~/bin/install-skill https://raw.githubusercontent.com/mqq-persistence/stock-analyzer/main/scripts/install_skill.py
chmod +x ~/bin/install-skill
```

### 2. 使用全局命令安装 Skill

```bash
# 安装 Skill
install-skill mqq-persistence/stock-analyzer

# 或者使用完整 URL
install-skill https://github.com/mqq-persistence/stock-analyzer
```

### 3. 在 Claude Code 中使用

```bash
claude
# 然后说："分析今天的涨停股"
```

---

## 方案二：使用项目自带的安装器

```bash
# 克隆项目
git clone https://github.com/mqq-persistence/stock-analyzer.git
cd stock-analyzer

# 运行安装脚本
./install.sh

# 或者使用 Python 安装器
python scripts/install_skill.py .
```

---

## 方案三：手动安装

### 步骤 1：克隆或下载

```bash
# 方法 A: Git 克隆
git clone https://github.com/mqq-persistence/stock-analyzer.git ~/.claude/skills/stock-analyzer

# 方法 B: 下载 ZIP 解压后复制
# 下载 https://github.com/mqq-persistence/stock-analyzer/archive/main.zip
# 解压后将内容复制到 ~/.claude/skills/stock-analyzer
```

### 步骤 2：安装依赖

```bash
cd ~/.claude/skills/stock-analyzer
pip install -e .
```

### 步骤 3：复制 Skill 文件

```bash
# 复制 skill 文档到全局目录
cp skills/*.md ~/.claude/skills/
```

---

## 验证安装

在 Claude Code 中输入：

```
/skills
```

应该能看到 `limit-up-analysis.md` 在列表中。

然后尝试：

```
分析今天的涨停股
```

---

## 卸载 Skill

```bash
# 删除 Skill 文件
rm ~/.claude/skills/limit-up-analysis.md
rm -rf ~/.claude/skills/stock-analyzer
```

---

## Skill 配置文件说明

### skill.json

```json
{
  "name": "limit-up-analysis",          // Skill 名称
  "version": "1.0.0",                   // 版本号
  "trigger_phrases": [...]              // 触发短语列表
}
```

### skills/*.md

Skill 说明文档，包含：
- 触发条件
- 执行流程
- 使用示例
- 依赖配置

---

## 创建和发布自己的 Skill

1. 创建项目结构
2. 编写 `skill.json` 和 `skills/*.md`
3. 推送到 GitHub
4. 用户通过 `install-skill username/repo` 安装

详细模板参考：https://github.com/mqq-persistence/stock-analyzer
