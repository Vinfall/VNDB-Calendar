# VNDB Release Calendar

## 介绍

这是一个创建 [VNDB](https://vndb.org) [upcoming releases](https://vndb.org/r?f=01731;o=a;s=released) 日历的小工具。
初始化后即可由 GitHub Actions 自动更新。
如果公开 `ICS` 文件，那么可以在任意支持 iCalendar 的日历应用中订阅。

## 目的

VNDB 目前只对 *Recent Changes* 提供 RSS，*Upcoming Releases* 和 *Just Released* 则没有提供。论坛之前讨论过好几次但 Yorhel 短期内应该不会做这个功能。

这是个人使用的替代方案（虽然协议从 RSS 修改为 ICS），同时当作博客文章 [iCalendar (ICS) 的养成方式](https://blog.vinfall.com/posts/2023/12/ics/) 的拓展。

## 搜索

运行结果应该和 [这则 VNDB 搜索](https://vndb.org/r?q=&o=a&s=released&f=0572171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-) 一样，但我为了不错过新发行视觉小说而把起始发售日往前挪了 14 天。

你可以 fork 这个项目后自行修改 [`vndb-calendar.py`](vndb-calendar.py) 中的 `filters` 和 `data`。

## Todo

- [x] 同一个视觉小说的多个 release 去重
- [x] 清理标题中的版本（比如 `ダウンロード版` 和 `DLカード版`）
- [ ] Better handling of partial date like `2026` and `2024-02`, or dates like `2024-01-01` would be a nightmare
- [ ] Filter out BLG/Otome game & other tags I wish to avoid
- [ ] Find out why many filters would make responses 400, and add more info in calendar events afterwards
- [ ] User wishlist, just like SteamWishlistCalendar (low priority as I don't use VNDB this way)
- [ ] Make filters work like arguments (low priority, you can simply use [compact filters](https://api.vndb.org/kana#filters) as an alternative)
- [ ] Add external links (Getchu/DMM/DLsite/Steam/Official website etc.) to event description (maybe not possible w/o refactoring)

## 贡献

如果你刚好知道 Elm 和 Perl，我建议直接向 VNDB 提交代码（相关文件：[vndb/lib/VNWeb/Misc/Feeds.pm - yorhel/vndb](https://code.blicky.net/yorhel/vndb/src/branch/master/lib/VNWeb/Misc/Feeds.pm)），摆脱第三方工具，一劳永逸。当然，我也欢迎任何对本仓库的贡献。

## 致谢

- 项目受 [SteamWishlistCalendar](https://github.com/icue/SteamWishlistCalendar) 启发，强烈建议用 SWC 替代邮件
- 从 [VNDB Steam Enhancer](https://greasyfork.org/en/scripts/456166-vndb-steam-enhancer/code) 了解到如何与 VNDB API 交互
