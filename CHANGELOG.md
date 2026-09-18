# Changelog

本项目的重要变更记录于此文件。

## [Unreleased]

### Added

- 新增 `scrapydweb` 可视化管理界面服务：网页上部署/调度/取消任务、查看日志、配置定时任务；`docker-compose.yml` 新增对应服务，`.env.example` 增加登录鉴权相关变量，README 补充使用说明。

## 2026-09-18

### Added

- 初始模板：Scrapy + Redis（分布式调度/去重）+ PostgreSQL（数据存储）+ Scrapyd（任务调度）。
- MIT License。
- README 补充仓库地址。
