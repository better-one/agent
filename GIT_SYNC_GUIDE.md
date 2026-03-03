# 智能体 Git 自动同步系统

**功能：** 智能体生成代码后自动提交到 Git，无需手动操作

---

## 🚀 快速开始

### 1. 基本用法

```python
from agent_git_sync import AgentGitSync

# 初始化
git = AgentGitSync(
    project_dir='/path/to/project',
    api_key='sk-sp-xxx'  # 阿里云百炼 API Key
)

# 同步所有变更
git.sync_to_git(
    agent_name='代码审查员',
    auto_push=True
)
```

### 2. 同步指定文件

```python
git.sync_to_git(
    files=['snake_v3_1_fixed.py', 'new_feature.py'],
    agent_name='架构师',
    commit_message='feat: 新增多人对战功能'
)
```

### 3. 版本规划自动提交

```python
from agent_git_sync import AgentVersionControl

vc = AgentVersionControl(
    project_dir='/path/to/project',
    api_key='sk-sp-xxx'
)

vc.plan_and_commit(
    version='v1.31',
    features=['春节主题', '限定皮肤', '节日任务'],
    agent_name='产品经理'
)
```

---

## 📋 API 文档

### AgentGitSync

#### 初始化
```python
AgentGitSync(
    project_dir: str,      # 项目目录
    api_key: str = None    # 阿里云百炼 API Key
)
```

#### 方法

**sync_to_git()** - 完整同步流程
```python
git.sync_to_git(
    files: List[str] = None,        # 文件列表，None=所有变更
    agent_name: str = "智能体",      # 智能体名称
    auto_push: bool = True,         # 是否自动推送
    commit_message: str = None      # 自定义 commit message，None=自动生成
) -> Dict
```

**返回值:**
```json
{
  "success": true,
  "files_changed": 5,
  "commit_message": "feat: 新增功能",
  "pushed": true
}
```

**generate_commit_message()** - 智能生成 commit message
```python
message = git.generate_commit_message(
    changes=[
        {"status": "A", "filename": "new_file.py"},
        {"status": "M", "filename": "modified.py"}
    ],
    agent_name="代码审查员"
)
```

**其他方法:**
- `get_git_status()` - 获取 Git 状态
- `add_files(files)` - 添加文件到暂存区
- `commit(message, author)` - 提交
- `push(remote, branch)` - 推送
- `create_branch(name)` - 创建分支
- `create_tag(name)` - 创建标签

### AgentVersionControl

#### 初始化
```python
AgentVersionControl(
    project_dir: str,
    api_key: str = None
)
```

#### 方法

**plan_and_commit()** - 版本规划并提交
```python
vc.plan_and_commit(
    version: str,              # 版本号 (如 v1.31)
    features: List[str],       # 功能列表
    agent_name: str,           # 智能体名称
    auto_push: bool = True     # 是否自动推送
)
```

---

## 🔧 配置

### Git 用户信息

首次使用需要配置 Git 用户信息：

```bash
git config --global user.name "你的名字"
git config --global user.email "your@email.com"
```

### 远程仓库

```bash
# 添加远程仓库
git remote add origin https://github.com/your-username/your-repo.git

# 推送
git push -u origin master
```

### API Key 配置

推荐在环境变量中配置：

```bash
export DASHSCOPE_API_KEY="sk-sp-xxx"
```

或在代码中：

```python
git = AgentGitSync(
    project_dir='/path/to/project',
    api_key=os.getenv('DASHSCOPE_API_KEY')
)
```

---

## 📊 工作流程

### 自动同步流程

```
1. 检查 Git 变更
   ↓
2. 添加文件到暂存区
   ↓
3. 使用 LLM 生成智能 commit message
   ↓
4. 提交代码（带智能体署名）
   ↓
5. 推送到远程仓库（可选）
   ↓
6. 更新版本历史
```

### Commit Message 生成

智能体自动生成的 commit message 遵循 **Conventional Commits** 规范：

```
feat: 新增多人对战功能
- 实现 WebSocket 实时通信
- 添加房间匹配系统
- 集成好友邀请

fix: 修复游戏崩溃问题
- 修复颜色值范围错误
- 移除不存在的 API 调用

docs: 更新架构文档
- 添加系统架构图
- 补充 API 说明
```

---

## 💡 使用场景

### 场景 1: 智能体生成代码后自动提交

```python
# 智能体生成新文件
code = llm.generate_code("实现宠物系统")
with open('pet_system.py', 'w') as f:
    f.write(code)

# 自动提交
git.sync_to_git(
    files=['pet_system.py'],
    agent_name='架构师'
)
```

### 场景 2: 版本规划自动创建文档并提交

```python
vc = AgentVersionControl(...)

vc.plan_and_commit(
    version='v1.32',
    features=['宠物收集', '宠物技能', '宠物养成'],
    agent_name='产品经理'
)
```

### 场景 3: 批量变更智能提交

```python
# 智能体讨论了 10 个版本规划
# 生成了多个文档

# 一次性提交所有变更
git.sync_to_git(
    agent_name='技术文档工程师',
    commit_message='docs: 完成 10 个版本规划文档'
)
```

---

## 🎯 最佳实践

### 1. 使用有意义的 agent_name

```python
# ✅ 好的命名
git.sync_to_git(agent_name='产品经理')
git.sync_to_git(agent_name='架构师')
git.sync_to_git(agent_name='测试工程师')

# ❌ 避免
git.sync_to_git(agent_name='AI')
git.sync_to_git(agent_name='Bot')
```

### 2. 自定义重要的 commit message

对于重大变更，建议手动指定 commit message：

```python
git.sync_to_git(
    files=['snake_v4.0.py'],
    commit_message='feat(v4.0): 重大版本更新 - 支持多人对战'
)
```

### 3. 小步提交

```python
# ✅ 推荐：分多次提交
git.sync_to_git(files=['feature_a.py'], agent_name='架构师')
git.sync_to_git(files=['feature_b.py'], agent_name='架构师')

# ❌ 不推荐：一次性提交所有
git.sync_to_git(agent_name='架构师')  # 变更太多
```

### 4. 定期推送

```python
# 本地开发时 auto_push=False
git.sync_to_git(auto_push=False)

# 完成一个阶段后手动推送
git.push()
```

---

## ⚠️ 注意事项

### 1. API 调用成本

自动生成 commit message 会调用 LLM API：

```python
# 每次 sync_to_git() 调用 1 次 API
# 成本：约 0.01 元/次

# 节省成本：手动指定 commit message
git.sync_to_git(
    commit_message='fix: 修复 Bug',
    agent_name='测试工程师'
)
```

### 2. 大文件处理

对于大文件（>10MB），建议：

```python
# 添加到 .gitignore
echo "*.large" >> .gitignore

# 或使用 Git LFS
git lfs install
git lfs track "*.large"
```

### 3. 冲突处理

如果有冲突，需要手动解决：

```bash
git pull origin master
# 解决冲突
git add .
git commit -m "merge: 解决冲突"
git push
```

---

## 📈 示例输出

### 成功同步

```
======================================================================
🔄 开始 Git 同步流程
======================================================================

📊 检查变更...
📁 发现 3 个变更文件:
   M: snake_v3_1_fixed.py
   A: new_feature.py
   A: docs/plan.md

📝 添加文件到暂存区...
✅ 已添加所有变更

🤖 生成智能 commit message...
💬 Commit Message: feat: 新增功能和文档更新
- 实现新特性
- 更新规划文档

💾 提交代码...
✅ 已提交：feat: 新增功能和文档更新...

🚀 推送到远程仓库...
✅ 推送成功

======================================================================
✅ Git 同步完成
======================================================================
```

### 无变更

```
📊 检查变更...
✅ 没有变更，无需同步
```

### 无远程仓库

```
🚀 推送到远程仓库...
⚠️  未配置远程仓库，跳过推送
   配置远程仓库：git remote add origin <url>
```

---

## 🔗 相关文档

- [智能体系统架构](AGENT_SYSTEM_ARCHITECTURE.md)
- [版本控制](agent_version_control.py)
- [协作平台](agent_collaboration_platform.py)

---

**最后更新：** 2024-03-03  
**GitHub:** https://github.com/better-one/snake-game
