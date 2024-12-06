# Litedis

Litedis 是一个轻量级的 模仿Redis 的本地实现，它实现了和 Redis 类似的功能，支持基本的数据结构和操作。适合调试代码时，没有 Redis 服务器或者不想连接 Redis 服务器的情况下使用。

## 功能特点

- 实现了基础数据结构：
  - STING
  - LIST
  - HASH
  - SET
  - ZSET
- 支持过期时间设置
- 支持持久化，包括 AOF 和 LDB、以及混合模式
- 简单轻量，数据存储在本地，无需服务器

## 使用示例

基本使用

```py
import time

from litedis import Litedis

with Litedis("litedis:///data/db") as db:
    db.set("key", "value", ex=1)
    assert db.get("key") == "value"

    time.sleep(1.1)
    assert not db.get("key")
```

