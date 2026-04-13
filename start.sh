#!/bin/bash

echo "=========================================="
echo "    文本转语音工具 - TTS Tool"
echo "=========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi

echo "[1/4] 检查 Python 环境... OK"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "[警告] 未找到 .env 文件"
    echo "请先复制 .env.example 为 .env，并填入你的 AK/SK"
    echo ""
    cp .env.example .env
    echo "已自动创建 .env 文件，请编辑后重新运行"
    if command -v code &> /dev/null; then
        code .env
    elif command -v vim &> /dev/null; then
        vim .env
    else
        echo "请手动编辑 .env 文件"
    fi
    exit 1
fi

echo "[2/4] 检查环境变量配置... OK"

# 安装依赖
echo "[3/4] 安装/更新依赖..."
pip3 install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败"
    exit 1
fi
echo "[3/4] 依赖安装... OK"

# 启动服务
echo "[4/4] 启动服务..."
echo ""
echo "=========================================="
echo "服务启动中，请稍候..."
echo "浏览器将自动打开 http://localhost:8000"
echo "按 Ctrl+C 停止服务"
echo "=========================================="
echo ""

# 等待几秒后打开浏览器
sleep 2

# 根据系统打开浏览器
if command -v open &> /dev/null; then
    open http://localhost:8000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000
fi

# 启动服务
python3 main.py
