"""
历史记录插件

功能：
- 监听 GameFinishedEvent，将游戏录像数据持久化到 SQLite 数据库
- 提供 GUI 界面：表格浏览、筛选、分页、播放/导出录像
- 使用 self.data_dir 存储数据库文件（每个插件独立目录）
"""

import sys

from . import service
from .plugin import HistoryPlugin

# 已发布的服务消费者通过这个路径延迟导入协议。
sys.modules["plugins.services.history"] = service

__all__ = ["HistoryPlugin"]
