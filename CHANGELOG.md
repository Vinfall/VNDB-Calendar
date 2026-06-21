# Changelog

All notable changes to this project will be documented in this file.

## [5.10.1] - 2026-06-21

### 📦 Dependencies

- Bump uv.lock
- Bump actions/checkout from 6 to 7
- Bump ics from 0.8.0.dev0 to 0.8.0.dev1
- Bump requests from 2.30.0 to 2.30.1
- Bump dependencies
- Bump jdx/mise-action from 3 to 4

### 🎨 Styling

- Tweak tombi schema.strict
- Set indent_size to 2 for json/jsonc

### 🛠️ Chores

- Bump {en,zh}patch start date to 2026-01
- Bump {en,zh}patch start date to 2025-10
- Set cache_key_prefix to avoid cache pollution
- Pip -> uv in dependabot
- Update .gitignore
- Sync mise config

## [5.9.6] - 2026-02-16

### 📚 Docs

- Add missing wishlist workflow
- Zh is broken

### 📦 Dependencies

- Bump uv.lock, properly
- Use aqua zizmor
- Use aqua ty

### 🎨 Styling

- Lint via tombi
- Mypy -> ty

### 🧪 Testing

- Wishlist

### 🛠️ Chores

- Update prod filters
- Set python.uv_venv_auto to source
- Ubuntu-latest -> ubuntu-slim
- Update regex filters
- Bump {en,zh}patch start date to 2025-07

## [5.7.2] - 2025-12-12

### 🐛 Fixes

- Exclude dvdpg
- Include re-release

### 📦 Dependencies

- Bump uv.lock
- Bump python to 3.14 per PEP 745
- Bump actions/checkout from 5 to 6
- Bump Python Matrix to 3.13~3.14 per PEP 745
- Revert zizmor to ubi backend

### 🛠️ Chores

- Update regex filters
- Add dependency cooldown
- Pin ad-m/github-push-action to v1
- Use native `gh release upload`
- Update tag filters

## [5.5.0] - 2025-09-01

### 🚀 Features

- Add enpatch release calendar
- Add zhpatch release calendar

### 📚 Docs

- Update usage command

### 📦 Dependencies

- Bump dependencies
- Bump jdx/mise-action from 2 to 3
- Bump actions/checkout from 4 to 5

## [5.3.1] - 2025-07-13

### 🚀 Features

- Add `--partial` param for partial releases

### 🐛 Fixes

- Args.filter treated as string
- Fix mise freeze by dropping pypy
- Ruff exe001

### 📚 Docs

- Update readme

### 📦 Dependencies

- Use aqua zizmor
- Bump uv.lock
- Bump dependencies

### 🎨 Styling

- Lint
- Add zizmor, actionlint, yamllint as ci linter
- Ignore ruff d203
- Lint via ruff + mypy
- Extend ruff rules, rm pylint, add mypy

### 🛠️ Chores

- Update regex filters
- Update prod filters
- Update regex & prod filter

## [5.0.0] - 2025-03-09

### 🚀 Features

- Uv run

### 🎨 Styling

- Lint via zizmor

### 🛠️ Chores

- Rm makefile
- Migrate make/uv to mise
- Uv.lock
- Make install
- Use cached uv in release
- Rename workflow
- Use cached uv

## [4.2.0] - 2025-02-01

### 📦 Dependencies

- Mv to pyproject.toml altoghther

### 🛠️ Chores

- Update metadata in pyproject.toml
- Mute version bump in changelog
- Simplify code

## [4.1.0] - 2025-01-13

### 🛠️ Chores

- Make changelog

## [4.0.0] - 2025-01-13

### 🚀 Features

- Add wishlist caldendar
- Add pyproject.toml

### 📚 Docs

- Add wishlist usage
- Update todo

### 📦 Dependencies

- Bump default python version to 3.13

### 🎨 Styling

- Lint

### 🛠️ Chores

- Rename

## [3.14.1] - 2024-12-07

### 📚 Docs

- Silent changelog update

## [3.14.0] - 2024-12-07

### 🚀 Features

- Update regex filters

## [3.13.4] - 2024-11-13

### 🐛 Fixes

- Fix make command

## [3.13.3] - 2024-11-13

### 🚀 Features

- Update regex filter
- Add Makefile

### 🎨 Styling

- Lint
- Set insert_final_newline to false for yaml
- Add editorconfig

### 🛠️ Chores

- Rename command
- Use make command in test

## [3.11.2] - 2024-10-09

### 🚀 Features

- Update regex & prod filter
- Update regex

### 🐛 Fixes

- Fix pypy -mpip install

### 📦 Dependencies

- Bump python matrix to 3.13 as per PEP 719, add pypy3.10

### 🛠️ Chores

- Use unique cache key

## [3.9.0] - 2024-10-02

### 🚀 Features

- Update prod filter

## [3.8.0] - 2024-09-01

### 🚀 Features

- Update regex & prod filter

### 🛠️ Chores

- Update ref
- Ignore test on docs change

## [3.6.1] - 2024-08-15

### 🚀 Features

- Update prod filter
- Update regex & prod filters

### 🐛 Fixes

- Badge location

### 🛠️ Chores

- Add ci badge
- Cache installed packages
- Rename workflow

## [3.5.0] - 2024-08-03

### 🚀 Features

- Add git-cliff

### 🛠️ Chores

- Add changelog

## [3.4.0] - 2024-07-28

### 🎨 Styling

- Lint

## [3.2.1] - 2024-07-07

### 🚀 Features

- Update regex & prod filters

## [3.2.0] - 2024-07-06

### 📦 Dependencies

- Bump Python Matrix to 3.11~3.13-dev ahead of 3.13-rc1

### 🛠️ Chores

- Add commit msg prefix

## [3.1.2] - 2024-06-16

### 🚀 Features

- Update prod filter
- Update title regex

### 📦 Dependencies

- Bump requests from 2.31.0 to 2.32.3

## [3.0.4] - 2024-05-18

### 🛠️ Chores

- Discard hacky & faulty sed replacement

## [3.0.3] - 2024-05-18

### 🚀 Features

- Feat: fix longstanding last_modified and dtstamp issue once for all
BREAKING CHANGE: ics 0.7.2 complies w/ only RFC 2445 while 0.8.0.dev0
complies w/ RFC 5545, ics format is a bit different because of this

### 🛠️ Chores

- Rename workflow artifact
- Rename continued
- Rename

## [2.6.12] - 2024-05-10

### 🚀 Features

- Update prod filter & title regex

### 📚 Docs

- Link to zh-Hans README

### 🛠️ Chores

- Add symlink
- Update producer filters
- Update regex filters
- Hunt bug
- Update tag & fix producer filters

## [2.6.7] - 2024-03-31

### 🛠️ Chores

- Update regex, tag & producer filters

## [2.6.3] - 2024-03-16

### 🛠️ Chores

- Update regex, tag & producer filters

## [2.6.0] - 2024-02-18

### 🛠️ Chores

- Normalize full width characters

## [2.5.0] - 2024-02-18

### 🛠️ Chores

- Improve filters with list comprehension
- Update tag & producer filters

## [2.4.4] - 2024-02-18

### 🐛 Fixes

- Fix filename & condition for sure
- Fix set-output deprecation warning & git diff

### 🛠️ Chores

- Probably fix condition

## [2.4.2] - 2024-02-17

### 🐛 Fixes

- Fix ics eol

### 🛠️ Chores

- Update ics only if new release is available

## [2.4.0] - 2024-02-17

### 🚀 Features

- Make output pass iCalendar Validator

## [2.3.7] - 2024-02-09

### 🛠️ Chores

- Normalize v47056
- Update commit message
- Ignore test on output push

## [2.3.4] - 2024-01-29

## [2.3.2] - 2024-01-29

## [2.3.1] - 2024-01-25

### 🐛 Fixes

- Fix title regex & update filters

## [2.3.0] - 2024-01-20

## [2.2.0] - 2024-01-19

## [2.1.0] - 2024-01-18

## [2.0.0] - 2024-01-18

## [1.7.6] - 2024-01-18

## [1.7.3] - 2024-01-16

## [1.7.0] - 2024-01-12

### 🐛 Fixes

- Fix _TO_REPLACE regex

## [1.6.0] - 2024-01-11

## [1.5.1] - 2024-01-11

## [1.5.0] - 2024-01-11

### 🐛 Fixes

- Fix _YEAR_ONLY_REGEX

## [1.4.0] - 2024-01-11

## [1.3.2] - 2024-01-11

### 🐛 Fixes

- Fix YYYY-MM date handling

## [1.3.0] - 2024-01-10

## [1.2.2] - 2024-01-09

### 🐛 Fixes

- Fix edge case formatting

<!-- generated by git-cliff -->
