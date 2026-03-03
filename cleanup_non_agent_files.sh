#!/bin/bash
# 清理非 Agent 相关代码
# 只保留智能体协作系统核心文件

echo "🧹 开始清理非 Agent 代码..."
echo ""

# 定义要保留的核心 Agent 文件
AGENT_CORE_FILES=(
    # 核心模块
    "llm_agent_communication.py"
    "dashscope_llm_integration.py"
    "dashscope_config.py"
    "dashscope_config.example.py"
    "agent_collaboration_platform.py"
    "agent_version_control.py"
    "agent_test_suite.py"
    "agent_optimizer.py"
    "agent_git_sync.py"
    "multi_agent_system.py"
    "multi_agent_system_v2.py"
    "agent_driven_development.py"
    
    # 运行脚本
    "run_collaboration_lite.py"
    "run_10versions_collaboration.py"
    "run_collaboration_5versions.py"
    "run_ui_ux_upgrade.py"
    
    # 智能体配置
    "agents/"
    
    # 文档
    "AGENT_SYSTEM_ARCHITECTURE.md"
    "GIT_SYNC_GUIDE.md"
    "AGENT_TEST_OPTIMIZATION_REPORT.md"
    "AGENT_5VERSION_DEVELOPMENT_REPORT.md"
    "AGENTS_TEAM_REPORT.md"
    "AGENT_COLLABORATION_STATUS.md"
    "AGENT_COLLABORATION_VERSION_REPORT.md"
    "LLM_REAL_COMMUNICATION_REPORT.md"
    "FINAL_SUMMARY.md"
    "TEN_VERSION_PLAN.md"
    "FIVE_VERSION_PLAN.md"
    "VERSION_ROADMAP_SUMMARY.md"
    "AUTO_ITERATION_REPORT.md"
    "DEVELOPMENT_REPORT.md"
    
    # 讨论报告
    "docs/agent_collaboration_report_v1_23.md"
    "docs/agent_collaboration_report_v1_24_25.md"
    "docs/ui_ux_upgrade_report.md"
    
    # 测试
    "test_dashscope_connection.py"
    "test_api_speed.py"
    "TEST_REPORT_V3_1.md"
    "ISSUE_1_FIX_REPORT.md"
    
    # 配置
    "requirements.txt"
    "README.md"
)

# 定义要删除的游戏相关文件
GAME_FILES=(
    "snake.py"
    "snake_v1.3.py"
    "snake_v1.4.py"
    "snake_v1.5.py"
    "snake_v2_neon.py"
    "snake_v3_1_fixed.py"
    "snake_v3_ultimate.py"
    "achievements.py"
    "daily_challenge.py"
    "quest_system.py"
    "shop_system.py"
    "skin_editor.py"
    "leaderboard.py"
    "social_share.py"
    "stats_tracker.py"
    "weather_system.py"
    "ai_opponent.py"
    "replay_system.py"
    "cloud_save.py"
    "test_game.py"
    "v1.11_1.17_batch.py"
    
    # 游戏文档
    "docs/level_design.md"
    "docs/iteration_report.md"
    "docs/test_results.json"
    "docs/implementation_plan.json"
    "docs/test_plan.json"
    "docs/PRD_v1.3.json"
)

cd /home/firefly/snake_game

echo "📁 要删除的游戏文件："
for file in "${GAME_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "   - $file"
        rm -rf "$file"
    fi
done

echo ""
echo "🗑️  清理 __pycache__ 目录..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "🗑️  清理 .pyc 文件..."
find . -name "*.pyc" -delete 2>/dev/null

echo "🗑️  清理临时文件..."
rm -f *.log 2>/dev/null
rm -f *.json 2>/dev/null
rm -f leaderboard.json custom_skins.json game_stats.json 2>/dev/null

echo ""
echo "📦 保留的 Agent 核心文件："
for file in "${AGENT_CORE_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "   ✓ $file"
    fi
done

echo ""
echo "✅ 清理完成！"
echo ""
echo "📊 统计："
echo "   文件数：$(find . -type f -not -path './.git/*' | wc -l)"
echo "   Python 文件：$(find . -name '*.py' -not -path './.git/*' | wc -l)"
echo "   Markdown 文件：$(find . -name '*.md' -not -path './.git/*' | wc -l)"
