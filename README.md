# 历史记录

元扫雷第三方插件。使用带 GitHub 插件发现功能的新版元扫雷。

## 安装

1. 在插件管理器中打开「插件」→「插件市场」。
2. 搜索 `metasweeper-history`，选择版本并安装，然后重启插件管理器。

也可以选择「从仓库 URL 安装」，输入 <https://github.com/ljzloser/metasweeper-history>。此仓库使用 GitHub 主题 `metasweeper-plugin` 和版本标签 `metasweeper-v1.0.0`。插件运行依赖由宿主提供。

数据和配置继续使用元扫雷现有数据目录。训练统计插件通过宿主提供的 `HistoryService` 读取记录。

数据库字段约定见[历史记录存储说明](docs/history-board-storage.md)。

[插件使用说明](history/README.md)

## 开发与测试

在已按主仓说明安装开发依赖的环境中，设置元扫雷源码路径，再从本仓库根目录运行测试：

```powershell
$env:PYTHONPATH = 'D:\work\Python\Solvable-Minesweeper\src'
$env:QT_QPA_PLATFORM = 'offscreen'
& 'D:\work\Python\Solvable-Minesweeper\.venv\Scripts\python.exe' -m pytest
```

Qt 翻译的 `.ts` 和 `.qm` 都随包分发。修改翻译源文件后，用 `pyside6-lrelease` 重新生成对应的 `.qm`。

[GPLv3 许可证](LICENSE)
