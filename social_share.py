#!/usr/bin/env python3
"""社交分享系统 v1.16.0"""
import random

class SocialShare:
    def __init__(self):
        self.templates = [
            "我刚在贪吃蛇得到 {score} 分！来挑战我吧！🐍",
            "新纪录！{score} 分！贪吃蛇大师就是我！🏆",
            "玩了 {time} 秒，得到 {score} 分，求超越！⏱️",
            "解锁成就：{achievement}！{score} 分达成！🎉",
            "今日挑战完成！{score} 分到手！💪",
        ]
    
    def generate_share_text(self, score, time_played=0, achievement=None):
        template = random.choice(self.templates)
        return template.format(
            score=score,
            time=time_played,
            achievement=achievement or "传奇蛇王"
        )
    
    def share_to_platform(self, platform, text):
        print(f"\n📤 分享到 {platform}:")
        print(f"   {text}")
        return True
    
    def share_score(self, score, platform="wechat"):
        text = self.generate_share_text(score)
        return self.share_to_platform(platform, text)

print("📱 v1.16.0 - 社交分享系统")
ss = SocialShare()
ss.share_score(450)
ss.share_score(500, platform="weibo")
