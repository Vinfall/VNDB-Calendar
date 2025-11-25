# 使用

## 新游戏发行日历

你可以通过（可选）参数运行 [`vndb_calendar.py`](vndb_calendar.py) 来自定义结果：
- `python vndb_calendar.py -f {自定义的 compact filter} -p {最大页数} -d {1 或 0} -b {0 或 1}`
- 以中日未发售视觉小说（带介绍）为例：`python vndb-calendar.py -f "0572171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-" -t 0 -d 1 -b 0`
- `-f` 或 `--filter`：自定义 [compact filters](https://api.vndb.org/kana#filters)，默认为我高度自定义的个人方案
- `-p` 或 `--max-page`：搜索结果的最大页数，默认为 `2`
- `-t` 或 `--shift-time`：显示 X 天前发售到尚未发售的视觉小说，设置为 `0` 才是真正的「即将发售作品」，默认为 `14`
- `-d`，`--description` 或 `--intro`：添加视觉小说介绍，布尔类型（只接受 `0` 或 `1`），默认为 `0`/`False`
- `-b`, `--beta` 或 `--partial`：在搜索结果中显示不完整的发行版本，常见于分割商法

## 愿望单发行日历

新游戏发行日历的下级替代，关注于用户愿望单。

运行 [`wishlist.py`](wishlist.py):
- `python wishlist.py -u "{uid}" -p {最大页数}`
- Example of Yorhel's wishlist: `python wishlist.py -u "u2"`
- `-u` 或 `--user`：**包含 'u'** 的用户 id，比如 `u2`
- `-p` 或 `--max-page`：搜索结果的最大页数，默认为 `1`。由于愿望单采用倒序获取，新游戏在前，每页 100 项结果，如果你只希望在日历看到未发售游戏，通常 1 页就足够

> [!NOTE]
> `wishlist.py` 默认你使用 `wishlist` 标签并且没有将其隐藏。
> 如果你希望使用其他默认标签或自定义标签来生成日历，请根据脚本注释的 one-liner 确定 label id 并修改 `default_filters`。
