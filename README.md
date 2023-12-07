# webman-boilerplate

快速创建 webman 工程，无需重复安装大量的库

## 预先安装的库
- `webman/console` 命令行功能支持
- `illuminate/database` Laravel ORM
- `illuminate/pagination` Laravel ORM 分页功能支持
- `symfony/var-dumper` 更好的 dump
- `illuminate/redis` Laravel Redis 支持
- `symfony/cache` Cache 支持 (依赖 `illuminate/redis`) 使用其封装的 Redis 相关的方法
- `vlucas/phpdotenv` .env 文件支持
- `webman/event` 事件系统
- `robmorgan/phinx` Migration 支持

## 快速上手
### 1. 快速配置环境
复制一份 `.env.example` 并更名为 `.env`，在其中配置你当前环境下的数据库、Redis 连接和相关配置，你便可以快速开始进行开发。如无特殊需求，无需在 `config/database.php` 中进行配置。

### 2. 迁移数据库 (migrations)
使用本项目，推荐使用 migration 构建数据库，而非手动编写 SQL 语句。当你配置 `.env` 文件之后，便可以使用 `php phinx` 命令开始编写迁移文件了！

**开始之前请确保数据库已经建立**

迁移文件的编写，请参考：
https://book.cakephp.org/phinx/0/en/migrations.html
