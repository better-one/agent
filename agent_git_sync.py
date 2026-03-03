#!/usr/bin/env python3
"""
智能体 Git 自动同步系统
功能：
- 智能体生成代码后自动提交到 Git
- 自动生成 commit message
- 自动推送到远程仓库
- 版本变更追踪
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dashscope_llm_integration import DashScopeClient

class AgentGitSync:
    """智能体 Git 同步系统"""
    
    def __init__(self, project_dir: str, api_key: str = None):
        self.project_dir = Path(project_dir)
        self.git_dir = self.project_dir / ".git"
        self.client = DashScopeClient(api_key=api_key)
        
        # 检查是否是 Git 仓库
        if not self.git_dir.exists():
            self.init_git_repo()
    
    def init_git_repo(self):
        """初始化 Git 仓库"""
        print("📦 初始化 Git 仓库...")
        self._run_git_command("git init")
        print("✅ Git 仓库初始化完成")
    
    def _run_git_command(self, command: str, check: bool = True) -> tuple:
        """运行 Git 命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if check and result.returncode != 0:
                raise Exception(f"Git 命令失败：{result.stderr}")
            
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            raise Exception("Git 命令超时")
    
    def get_git_status(self) -> Dict:
        """获取 Git 状态"""
        # 获取变更文件
        _, stdout, _ = self._run_git_command("git status --porcelain")
        
        changed_files = []
        for line in stdout.strip().split('\n'):
            if line:
                status = line[:2].strip()
                filename = line[2:].strip()
                changed_files.append({
                    'status': status,
                    'filename': filename
                })
        
        # 获取当前分支
        _, branch, _ = self._run_git_command("git branch --show-current")
        
        # 获取最近提交
        _, log, _ = self._run_git_command("git log --oneline -5")
        
        return {
            'changed_files': changed_files,
            'branch': branch.strip(),
            'recent_commits': log.strip().split('\n'),
            'has_remote': self._check_remote()
        }
    
    def _check_remote(self) -> bool:
        """检查是否有远程仓库"""
        code, _, _ = self._run_git_command("git remote -v", check=False)
        return code == 0
    
    def add_files(self, files: List[str] = None):
        """添加文件到暂存区"""
        if files:
            for file in files:
                self._run_git_command(f"git add {file}")
                print(f"✅ 已添加：{file}")
        else:
            # 添加所有变更
            self._run_git_command("git add -A")
            print("✅ 已添加所有变更")
    
    def generate_commit_message(self, changes: List[Dict], agent_name: str = "智能体") -> str:
        """使用 LLM 生成智能 commit message"""
        
        # 构建变更摘要
        change_summary = ""
        for change in changes:
            change_summary += f"- {change['status']}: {change['filename']}\n"
        
        # 请求 LLM 生成 commit message
        prompt = f"""
作为{agent_name}，请为以下 Git 变更生成专业的 commit message：

变更文件：
{change_summary}

要求：
1. 使用 Conventional Commits 格式
2. 包括类型（feat/fix/docs/style/refactor/test/chore）
3. 简洁描述变更内容（50 字以内）
4. 可选：添加详细的 body 说明

示例：
feat: 新增用户登录功能
- 实现用户名密码验证
- 添加 JWT token 生成
- 集成 OAuth2.0

请生成 commit message："""

        response = self.client.chat([
            {"role": "user", "content": prompt}
        ], temperature=0.7)
        
        return response.strip()
    
    def commit(self, message: str, author: str = None):
        """提交代码"""
        if author:
            cmd = f'git commit -m "{message}" --author="{author}"'
        else:
            cmd = f'git commit -m "{message}"'
        
        self._run_git_command(cmd)
        print(f"✅ 已提交：{message[:50]}...")
    
    def push(self, remote: str = "origin", branch: str = None):
        """推送到远程仓库"""
        if not branch:
            _, branch, _ = self._run_git_command("git branch --show-current")
            branch = branch.strip()
        
        print(f"🚀 推送到 {remote}/{branch}...")
        self._run_git_command(f"git push {remote} {branch}", timeout=120)
        print(f"✅ 推送成功")
    
    def sync_to_git(self, files: List[str] = None, agent_name: str = "智能体", 
                   auto_push: bool = True, commit_message: str = None):
        """
        完整同步流程
        
        Args:
            files: 要同步的文件列表，None 表示所有变更
            agent_name: 智能体名称
            auto_push: 是否自动推送
            commit_message: 自定义 commit message，None 则自动生成
        """
        print("\n" + "="*70)
        print("🔄 开始 Git 同步流程")
        print("="*70)
        
        # 1. 获取变更
        print("\n📊 检查变更...")
        status = self.get_git_status()
        
        if not status['changed_files']:
            print("✅ 没有变更，无需同步")
            return
        
        print(f"📁 发现 {len(status['changed_files'])} 个变更文件:")
        for change in status['changed_files']:
            print(f"   {change['status']}: {change['filename']}")
        
        # 2. 添加文件
        print("\n📝 添加文件到暂存区...")
        self.add_files(files)
        
        # 3. 生成或使用自定义 commit message
        if commit_message:
            message = commit_message
        else:
            print("\n🤖 生成智能 commit message...")
            message = self.generate_commit_message(status['changed_files'], agent_name)
            print(f"💬 Commit Message: {message[:100]}...")
        
        # 4. 提交
        print("\n💾 提交代码...")
        author = f"{agent_name} <agent@snake-game.local>"
        self.commit(message, author)
        
        # 5. 推送
        if auto_push:
            if status['has_remote']:
                print("\n🚀 推送到远程仓库...")
                self.push()
            else:
                print("\n⚠️  未配置远程仓库，跳过推送")
                print("   配置远程仓库：git remote add origin <url>")
        
        print("\n" + "="*70)
        print("✅ Git 同步完成")
        print("="*70)
        
        return {
            'success': True,
            'files_changed': len(status['changed_files']),
            'commit_message': message,
            'pushed': auto_push and status['has_remote']
        }
    
    def create_branch(self, branch_name: str, from_branch: str = None):
        """创建新分支"""
        if from_branch:
            self._run_git_command(f"git checkout -b {branch_name} {from_branch}")
        else:
            self._run_git_command(f"git checkout -b {branch_name}")
        print(f"✅ 已创建分支：{branch_name}")
    
    def create_tag(self, tag_name: str, message: str = None):
        """创建标签"""
        if message:
            self._run_git_command(f'git tag -a {tag_name} -m "{message}"')
        else:
            self._run_git_command(f"git tag {tag_name}")
        print(f"✅ 已创建标签：{tag_name}")
    
    def get_commit_history(self, count: int = 10) -> List[Dict]:
        """获取提交历史"""
        _, log, _ = self._run_git_command(
            f"git log --oneline -{count} --pretty=format:'%h|%an|%ad|%s'"
        )
        
        commits = []
        for line in log.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'date': parts[2],
                        'message': parts[3]
                    })
        
        return commits


class AgentVersionControl:
    """智能体版本控制系统"""
    
    def __init__(self, project_dir: str, api_key: str = None):
        self.project_dir = Path(project_dir)
        self.git = AgentGitSync(project_dir, api_key)
        self.version_history_file = self.project_dir / "VERSION_HISTORY.json"
    
    def plan_and_commit(self, version: str, features: List[str], 
                       agent_name: str = "产品经理", auto_push: bool = True):
        """
        规划版本并提交
        
        Args:
            version: 版本号 (如 v1.31)
            features: 功能列表
            agent_name: 智能体名称
            auto_push: 是否自动推送
        """
        print("\n" + "="*70)
        print(f"📋 版本规划：{version}")
        print("="*70)
        
        # 1. 使用 LLM 生成版本规划文档
        prompt = f"""
请为贪吃蛇游戏 {version} 版本生成详细的功能规划文档。

功能列表:
{chr(10).join(['- ' + f for f in features])}

要求:
1. 详细描述每个功能
2. 技术方案
3. 预期效果
4. 开发周期评估

格式：Markdown"""

        client = DashScopeClient(api_key=self.git.client.api_key)
        plan_doc = client.chat([
            {"role": "user", "content": prompt}
        ])
        
        # 2. 保存规划文档
        plan_file = self.project_dir / "docs" / f"version_{version.replace('.', '_')}_plan.md"
        plan_file.parent.mkdir(exist_ok=True)
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(f"# {version} 版本规划\n\n")
            f.write(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(plan_doc)
        
        print(f"✅ 版本规划已保存到：{plan_file}")
        
        # 3. 同步到 Git
        result = self.git.sync_to_git(
            files=[str(plan_file)],
            agent_name=agent_name,
            auto_push=auto_push,
            commit_message=f"feat({version}): 版本规划 - {', '.join(features[:3])}"
        )
        
        # 4. 更新版本历史
        self._update_version_history(version, features, result)
        
        return result
    
    def _update_version_history(self, version: str, features: List[str], 
                               git_result: Dict):
        """更新版本历史"""
        history = []
        
        if self.version_history_file.exists():
            with open(self.version_history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append({
            'version': version,
            'features': features,
            'planned_at': datetime.now().isoformat(),
            'git_commit': git_result.get('commit_message', ''),
            'pushed': git_result.get('pushed', False)
        })
        
        with open(self.version_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 版本历史已更新")


# 使用示例
if __name__ == '__main__':
    # 示例 1: 同步单个文件
    print("示例 1: 同步智能体生成的代码")
    git_sync = AgentGitSync(
        project_dir='/home/firefly/snake_game',
        api_key='sk-sp-4c6bc141469d4ed7be788c9cb0e6af39'
    )
    
    # 同步指定文件
    result = git_sync.sync_to_git(
        files=['snake_v3_1_fixed.py'],
        agent_name='代码审查员',
        auto_push=True,
        commit_message='fix: 修复游戏崩溃问题'
    )
    
    # 示例 2: 版本规划
    print("\n\n示例 2: 版本规划并提交")
    version_control = AgentVersionControl(
        project_dir='/home/firefly/snake_game',
        api_key='sk-sp-4c6bc141469d4ed7be788c9cb0e6af39'
    )
    
    result = version_control.plan_and_commit(
        version='v1.31',
        features=['春节主题', '限定皮肤', '节日任务'],
        agent_name='产品经理',
        auto_push=True
    )
