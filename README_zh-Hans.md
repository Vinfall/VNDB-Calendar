# VNDB Calendar

[![Build][build]][build-ci] [![Release][release]][release-ci] [![Test][test]][test-ci]

## 介绍

VNDB 目前只对 *Recent Changes* 提供 RSS，*Upcoming Releases* 和 *Just Released* 则没有提供。
本工具可以创建 [VNDB](https://vndb.org) [upcoming releases][released] 发售日历。
    ，同时当作博客文章 [iCalendar (ICS) 的养成方式][ics] 的拓展。

初始化后即可由 GitHub Actions 自动更新。
如果选择公开 `ICS` 文件，那么可以在支持 iCalendar 的日历应用中订阅。

为方便测试，项目默认提供了下列发售日历。如果这些已经满足你的需求，没有必要阅读配置部分。
- [zhpatch][zhpatch]: 2025 下半年至今发布的民间汉化补丁
- ~~[zh][zh]: 尚未发售的中/日视觉小说~~ 待修复

## 配置

对日历的进一步定制需要 fork repo 并修改查询条件。
[USAGE](USAGE_zh-Hans.md) 文件包含运行参数的更多细节。

精简的配置流程：
1. 打开 VNDB [Browser releases][vndb] 页面，修改查询条件，并复制 *filters*
   - 举例说明，[zhpatch][zhpatch] 对应的 URL 可能是这样的：
     - `https://vndb.org/r?q=&o=a&s=title&f=04122wzh_dHans-2wzh_dHant-Ng1174172_0ceSs`
     - `https://vndb.org/r?f=04122wzh_dHans-2wzh_dHant-Ng1174172_0ceSs&o=a&s=released`
   - 这里的 *filters* 就是 `04122wzh_dHans-2wzh_dHant-Ng1174172_0ceSs`，之后会用到它
2. Fork 本仓库
3. 用前面复制的 filters 替换 [vndb_calendar.py](vndb_calendar.py) 中的 `default_filters`

    ```python
    # fmt: on

    # ↓↓↓ 复制到这里 ↓↓↓
    default_filters = "04122wzh_dHans-2wzh_dHant-Ng1174172_0ceSs"
    # ↑↑↑ 复制到这里 ↑↑↑

    default_data = {
        ...
    }
    ```

4. 在 [output/vndb-calendar.ics][custom] 获取个性化日历（记得修改 URL 中的用户名）

## 贡献

如果你恰好知道 Perl，我建议直接向 VNDB 提交代码（相关文件：[vndb/lib/VNWeb/Misc/Feeds.pm - yorhel/vndb][Feeds.pm]），摆脱第三方工具，一劳永逸。
当然，我也欢迎任何对本仓库的贡献。

## 致谢

- 项目受 [SteamWishlistCalendar][swc] 启发，强烈建议用 SWC 替代 Steam 邮件通知
- 与 VNDB API 交互参考了 [VNDB Steam Enhancer][vndb-steam-enhancer]
- 感谢 VNDB 全体贡献者和编辑者

[build]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/custom.yml/badge.svg
[build-ci]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/custom.yml
[release]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release.yml/badge.svg
[release-ci]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release.yml
[test]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml/badge.svg
[test-ci]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml
[released]: https://vndb.org/r?f=01731&o=a&s=released
[zh]: https://github.com/Vinfall/VNDB-Calendar/releases/download/zh/vndb-calendar.ics
[zhpatch]: https://github.com/Vinfall/VNDB-Calendar/releases/download/zhpatch/vndb-calendar.ics
[ics]: https://blog.vinfall.com/posts/2023/12/ics/
[Feeds.pm]: https://code.blicky.net/yorhel/vndb/src/branch/master/lib/VNWeb/Misc/Feeds.pm
[swc]: https://github.com/icue/SteamWishlistCalendar
[vndb-steam-enhancer]: https://greasyfork.org/en/scripts/456166-vndb-steam-enhancer/code
[custom]: https://github.com/yourusername/VNDB-Calendar/raw/refs/heads/main/output/vndb-calendar.ics
[vndb]: https://vndb.org/r
