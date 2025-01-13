# VNDB Calendar

[![Build](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/gen-calendar.yml/badge.svg)](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/gen-calendar.yml) [![Release](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release-calendar.yml/badge.svg)](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release-calendar.yml) [![Test](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml/badge.svg)](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml)

## 介绍

这是一个创建 [VNDB](https://vndb.org) [upcoming releases](https://vndb.org/r?f=01731;o=a;s=released) 日历的小工具。
初始化后即可由 GitHub Actions 自动更新。
如果公开 `ICS` 文件，那么可以在任意支持 iCalendar 的日历应用中订阅。
[点击这里](https://github.com/Vinfall/VNDB-Calendar/releases/download/zh/vndb-calendar.ics)获取包含中日双语视觉小说的示例文件。

## 目的

VNDB 目前只对 *Recent Changes* 提供 RSS，*Upcoming Releases* 和 *Just Released* 则没有提供。论坛之前讨论过好几次但 Yorhel 短期内应该不会做这个功能。

这是个人使用的替代方案（虽然协议从 RSS 修改为 ICS），同时当作博客文章 [iCalendar (ICS) 的养成方式](https://blog.vinfall.com/posts/2023/12/ics/) 的拓展。

## 使用

你可以通过（可选）参数运行脚本来自定义结果：
- `python vndb-calendar.py -f {自定义的 compact filter} -p {最大页数} -d {1 或 0}`
- 以中日未发售视觉小说（带介绍）为例：`python vndb-calendar.py -f "0572171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-" -t 0 -d 1`
- `-f` 或 `--filter`：自定义 [compact filters](https://api.vndb.org/kana#filters)，默认为我高度自定义的个人方案
- `-p` 或 `--max-page`：搜索结果的最大页数，默认为 `2`
- `-t` 或 `--shift-time`：显示 X 天前发售到尚未发售的视觉小说，设置为 `0` 才是真正的「即将发售作品」，默认为 `14`
- `-d`，`--description` 或 `--intro`：添加视觉小说介绍，布尔类型（只接受 `0` 或 `1`），默认为 `0`/`False`

## TODO

- [x] 同一个视觉小说的多个 release 去重
- [x] 清理标题中的版本（比如 `ダウンロード版` 和 `DLカード版`）
- [x] 优化不完整日期（比如 `2026` 和 `2024-02`）的处理
- [x] 排查自定义筛选返回 400 的原因（筛选填写有误）
- [x] 排除带有 BLG、乙女游戏和其他预期外标签的视觉小说
- [x] 允许通过运行参数自定义搜索（具体参见 VNDB API 文档的 [compact filters](https://api.vndb.org/kana#filters) 部分）
- [x] （自动化发布）通用的中日视觉小说发售日历
- [x] 在日历事件中添加视觉小说介绍，并设置为可选参数
- [ ] User wishlist, just like SteamWishlistCalendar
- [ ] Do not use alternative title in en tagged release (low priority, I assume people would prefer literal title instead of confusing Romaji)
- [ ] Add external links (Getchu/DMM/DLsite/Steam/Official website etc.) to event description (low priority, quite long already with VN description)

## 贡献

如果你恰好知道 Perl，我建议直接向 VNDB 提交代码（相关文件：[vndb/lib/VNWeb/Misc/Feeds.pm - yorhel/vndb](https://code.blicky.net/yorhel/vndb/src/branch/master/lib/VNWeb/Misc/Feeds.pm)），摆脱第三方工具，一劳永逸。当然，我也欢迎任何对本仓库的贡献。

## 致谢

- 项目受 [SteamWishlistCalendar](https://github.com/icue/SteamWishlistCalendar) 启发，强烈建议用 SWC 替代 Steam 邮件通知
- 从 [VNDB Steam Enhancer](https://greasyfork.org/en/scripts/456166-vndb-steam-enhancer/code) 了解到如何与 VNDB API 交互
- 感谢 VNDB 全体贡献者和编辑者
