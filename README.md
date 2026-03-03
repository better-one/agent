# AI 智能体协作系统

> 🤖 基于 LLM 的多智能体协作开发平台，模拟真实软件团队

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![LLM](https://img.shields.io/badge/LLM-阿里云百炼-orange.svg)](https://help.aliyun.com/zh/dashscope/)

---

## 🎯 项目简介

这是一个**智能体协作开发系统**，通过 11 个专业角色的 AI 智能体，模拟真实的软件开发团队：

- 💬 **智能讨论** - 多轮对话、观点碰撞、达成共识
- 📊 **版本规划** - 自动生成版本功能规划和技术方案
- 📝 **文档输出** - PRD、技术方案、测试计划一键生成
- 🚀 **自动同步** - 智能体生成的代码自动提交到 Git

### 核心价值

| 传统开发 | 智能体协作 |
| :--- | :--- |
| 人工讨论，耗时耗力 | 自动讨论，分钟级产出 |
| 视角单一，考虑不周 | 多角色视角，全面分析 |
| 文档质量参差不齐 | 标准化输出，质量稳定 |
| 沟通成本高 | 低成本，可重复 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│           用户界面层                     │
│  CLI 工具  │  Web 界面  │  API 调用     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           应用服务层                     │
│  协作平台  │  智能体管理  │  版本控制   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           核心引擎层                     │
│  LLM 客户端 │  智能体基类  │  消息总线  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           基础设施层                     │
│  阿里云百炼 │  本地存储  │  Git 仓库    │
└─────────────────────────────────────────┘
```

详细架构文档：[AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md)

---

## 🤖 智能体角色

系统包含 **11 个专业角色**：

| 角色 | 职责 | 专业领域 |
| :--- | :--- | :--- |
| **产品经理** | 需求分析、产品规划 | 用户需求、市场分析 |
| **架构师** | 技术选型、架构设计 | 系统设计、技术栈 |
| **测试工程师** | 测试计划、质量保证 | 测试用例、自动化 |
| **UI/UX设计师** | 界面设计、用户体验 | 视觉设计、可用性 |
| **安全工程师** | 安全审计、漏洞防护 | 渗透测试、加密 |
| **运维工程师** | 部署运维、监控告警 | 容器化、CI/CD |
| **性能优化专家** | 性能分析、系统优化 | Profiling、调优 |
| **代码审查员** | 代码 Review、规范检查 | 代码质量、最佳实践 |
| **技术文档工程师** | 文档编写、API 文档 | 技术写作、知识管理 |
| **数据分析师** | 数据分析、指标监控 | 埋点、报表、洞察 |
| **发布经理** | 版本发布、变更管理 | 发布流程、风险管理 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 复制配置模板
cp dashscope_config.example.py dashscope_config.py

# 编辑配置，填入你的阿里云百炼 API Key
vim dashscope_config.py
```

**获取 API Key：**
1. 访问：https://help.aliyun.com/zh/dashscope/
2. 注册/登录阿里云账号
3. 创建 API Key（推荐使用 Coding Plan，首月 7.9 元）

### 3. 运行智能体协作

```bash
# 简化版协作（推荐）
python3 run_collaboration_lite.py

# 完整协作流程
python3 agent_collaboration_platform.py

# 版本规划
python3 run_10versions_collaboration.py
```

### 4. 自动同步到 Git

```python
from agent_git_sync import AgentGitSync

# 初始化
git = AgentGitSync(
    project_dir='/path/to/project',
    api_key='sk-sp-xxx'
)

# 智能体生成代码后，自动提交
git.sync_to_git(
    agent_name='架构师',
    auto_push=True
)
```

---

## 📁 项目结构

```
agent/
├── # 核心模块
├── llm_agent_communication.py      # LLM 智能沟通核心
├── dashscope_llm_integration.py    # 阿里云百炼集成
├── agent_collaboration_platform.py # 协作平台
├── agent_version_control.py        # 版本控制
├── agent_test_suite.py             # 测试套件
├── agent_optimizer.py              # 优化器
├── agent_git_sync.py               # Git 自动同步
├── multi_agent_system.py           # 多智能体系统
│
├── # 运行脚本
├── run_collaboration_lite.py       # 简化版协作
├── run_10versions_collaboration.py # 10 版本规划
├── run_collaboration_5versions.py  # 5 版本规划
│
├── # 智能体配置
├── agents/
│   ├── product_manager.md         # 产品经理
│   ├── architect.md               # 架构师
│   ├── qa_engineer.md             # 测试工程师
│   ├── ui_ux_designer.md          # UI/UX设计师
│   ├── security_engineer.md       # 安全工程师
│   ├── devops_engineer.md         # 运维工程师
│   ├── performance_expert.md      # 性能优化专家
│   ├── code_reviewer.md           # 代码审查员
│   ├── documentation_engineer.md  # 技术文档工程师
│   ├── data_analyst.md            # 数据分析师
│   └── release_manager.md         # 发布经理
│
├── # 文档
├── AGENT_SYSTEM_ARCHITECTURE.md   # 完整架构文档
├── GIT_SYNC_GUIDE.md              # Git 同步指南
├── TEN_VERSION_PLAN.md            # 10 版本规划
├── FIVE_VERSION_PLAN.md           # 5 版本规划
├── docs/
│   ├── agent_collaboration_report_v1_23.md
│   └── agent_collaboration_report_v1_24_25.md
│
├── # 配置
├── dashscope_config.py            # API 配置
├── dashscope_config.example.py    # 配置模板
├── requirements.txt               # Python 依赖
└── README.md                      # 本文件
```

---

## 💡 使用场景

### 场景 1: 版本功能规划

```bash
python3 run_collaboration_lite.py
```

**输出：**
- 产品需求文档（PRD）
- 技术方案设计
- 测试计划
- 版本路线图

### 场景 2: 多版本迭代规划

```bash
python3 run_10versions_collaboration.py
```

**输出：**
- 10 个版本的详细规划
- 技术架构演进路线
- 预期成果和指标

### 场景 3: 智能体讨论特定话题

```python
from agent_collaboration_platform import AgentCollaborationPlatform

platform = AgentCollaborationPlatform(
    project_dir='/path/to/project',
    api_key='sk-sp-xxx'
)

# 发起讨论
platform.start_discussion(
    topic="如何实现多人对战功能",
    participants=["产品经理", "架构师", "运维工程师"]
)
```

### 场景 4: 自动生成代码并提交

```python
from agent_git_sync import AgentGitSync

git = AgentGitSync(
    project_dir='/path/to/project',
    api_key='sk-sp-xxx'
)

# 智能体生成代码后自动提交
git.sync_to_git(
    files=['new_feature.py'],
    agent_name='架构师',
    auto_push=True
)
```

---

## 📊 性能指标

| 指标 | 数值 | 说明 |
| :--- | :--- | :--- |
| **讨论时间** | 5-10 分钟 | 完成一次版本规划 |
| **API 调用** | 4-10 次 | 根据参与智能体数量 |
| **Token 消耗** | 5000-20000 | 根据讨论复杂度 |
| **文档产出** | 5000-20000 字 | 完整版本规划文档 |
| **成本** | ￥0.1-0.5/次 | 按阿里云百炼定价 |

---

## 🔧 配置说明

### API Key 配置

```python
# dashscope_config.py
DASHSCOPE_API_KEY = "sk-sp-xxxxxxxxxxxx"  # 你的 API Key
CODING_PLAN_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
DEFAULT_MODEL = "qwen3.5-plus"
```

### Git 配置

```bash
# 配置 Git 用户信息
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 添加远程仓库
git remote add origin git@github.com:your-username/your-repo.git
```

---

## 📚 文档导航

| 文档 | 说明 |
| :--- | :--- |
| [AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md) | 完整系统架构设计 |
| [GIT_SYNC_GUIDE.md](GIT_SYNC_GUIDE.md) | Git 自动同步使用指南 |
| [TEN_VERSION_PLAN.md](TEN_VERSION_PLAN.md) | 10 个版本详细规划 |
| [FIVE_VERSION_PLAN.md](FIVE_VERSION_PLAN.md) | 5 个版本详细规划 |
| [docs/agent_collaboration_report_v1_23.md](docs/agent_collaboration_report_v1_23.md) | v1.23 版本讨论报告 |
| [docs/agent_collaboration_report_v1_24_25.md](docs/agent_collaboration_report_v1_24_25.md) | v1.24-v1.25 版本讨论报告 |

---

## 🤝 贡献指南

### 添加新的智能体角色

1. 在 `agents/` 目录创建配置文件
2. 在 `agent_collaboration_platform.py` 中注册
3. 测试新角色的表现

### 优化 Prompt

1. 编辑对应智能体的配置文件
2. 运行测试验证效果
3. 提交改进的 Prompt

### 报告 Bug

请在 GitHub Issues 中报告问题，包括：
- Bug 描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息

---

## 📄 License

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

---

## 🔗 相关链接

- **GitHub:** https://github.com/better-one/agent
- **阿里云百炼文档:** https://help.aliyun.com/zh/dashscope/
- **系统架构文档:** [AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md)
- **Git 同步指南:** [GIT_SYNC_GUIDE.md](GIT_SYNC_GUIDE.md)

---

## 📧 联系方式

- **Issues:** https://github.com/better-one/agent/issues
- **Email:** better-one@github

---

**🎉 开始你的智能体协作之旅吧！**

```bash
python3 run_collaboration_lite.py
```
