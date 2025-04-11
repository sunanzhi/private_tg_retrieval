# private_tg_retrieval

私人Telegram内容检索工具

## 项目简介

这是一个用于检索和管理私人Telegram消息内容的工具。它能够帮助用户方便地搜索、归档和管理自己的Telegram聊天记录。

## 主要功能

- 指定分组检索相关影视资源（阿里云盘/夸克云盘）

## 环境要求

- Python 3.12+
- Telegram API密钥
- SQLite/PostgreSQL（用于数据存储）

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/private_tg_retrieval.git
cd private_tg_retrieval
```
2. 安装依赖
```bash
pip install -r requirements.txt
```
3. 配置环境变量
```bash
cp .env.example .env
```
然后编辑.env文件，填入您的Telegram API密钥和其他必要配置。

## 使用说明
1. 启动服务
```bash
python http_server.py
```
访问 http://localhost:8000 开始使用检索功能

## 注意事项
- 请妥善保管您的API密钥
- 定期备份数据库
- 遵守Telegram的使用条款和API限制
## 贡献指南
欢迎提交Issue和Pull Request来帮助改进这个项目。