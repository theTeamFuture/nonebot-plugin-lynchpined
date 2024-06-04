<div align="center">
  
# nonebot-plugin-lynchpined

*Getting lynchpined everyday!*

</div>

## Description

`nonebot-plugin-lynchpined` is a [nonebot2](https://nonebot.dev/) plugin to help you track [lynchpin progress](https://ak.hypergryph.com/lynchpin) in QQ group.

## Installation

### By nb-cli (Recommended)

Pending.

```bash
nb plugin install nonebot-plugin-lynchpined
```

### By pip

```bash
pip install nonebot-plugin-lynchpined
```

and then adding following content in the `pyproject.toml`:

```toml
[tool.nonebot]
plugins = [
  ... # others
  "nonebot-plugin-lynchpined",
  ]
```

## Simple Usage

Just call `lynchpin` anywhere bot can chat.

```
> Lynchpined
Lynchpin: 24%
Pattern Matched:
 0  4 12 15 [24] 33 34 35 35
```

## Subscribe to Lynchpin Progress

Adding `lynchpined_user` or `lynchpined_group` in config, the plugin will send lynchpin progress to the lynchpined at 00:00 everyday.

For example: 

```Properties
LYNCHPINED_GROUP = [4121524, 33343535]
LYNCHPINED_USER = [11708102]
```

**Note:** Make sure the timezone on your machine is `UTC+8` or you have to manually modified the trigger in `__init__.py`.
