# 文本转语音工具 (TTS Tool)

基于火山引擎豆包 TTS API 的文本转语音工具，使用 FastAPI + 纯前端实现。

## ⚠️ 重要提示

**本项目仅供学习交流，请勿将自己的 AK/SK 提交到公开仓库！**

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

**Windows:**
```bash
python main.py
```

**Mac/Linux:**
```bash
python3 main.py
```

### 3. 访问应用

打开浏览器访问 http://localhost:8888

### 3. 访问应用

启动后会自动打开浏览器，或手动访问：http://localhost:8000

## 📁 项目结构

```
tts-tool/
├── main.py              # FastAPI 后端
├── requirements.txt     # Python 依赖
├── .env                 # 环境变量（不提交到 Git）
├── .env.example         # 环境变量模板
├── .gitignore           # Git 忽略文件
├── start.bat            # Windows 启动脚本
├── start.sh             # Mac/Linux 启动脚本
├── README.md            # 项目说明
├── static/              # 前端静态文件
│   └── index.html       # 主页面
└── mini_program/        # 微信小程序示例（可选）
    ├── app.js
    ├── app.json
    ├── pages/
    │   └── index/
    │       ├── index.wxml
    │       ├── index.wxss
    │       └── index.js
    └── README.md
```

## 🎨 功能特性

- ✅ 大文本输入框，支持长文本
- ✅ 多种音色选择
- ✅ 语速、音量调节
- ✅ 长文本自动分段处理
- ✅ 音频在线播放和下载
- ✅ 紫色主题，苹果简约风设计
- ✅ 配置隔离，AK/SK 不暴露在前端

## 📤 上传到 GitHub

```bash
git init
git add .
git commit -m "Initial commit: TTS Tool with Volcengine Doubao API"
git branch -M main
git remote add origin https://github.com/你的用户名/tts-tool.git
git push -u origin main
```

## 🔧 技术栈

- **后端**: Python + FastAPI
- **前端**: 原生 HTML/CSS/JavaScript
- **TTS API**: Edge TTS (微软 Edge 浏览器语音合成，免费)

## 📄 许可证

MIT License - 仅供学习交流使用
