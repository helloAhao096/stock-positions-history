#!/usr/bin/env python3
"""
股票持仓管理系统 - Web应用启动脚本
"""

import uvicorn
from web_app import app

if __name__ == "__main__":
    print("=" * 50)
    print("股票持仓管理系统")
    print("=" * 50)
    print("正在启动Web服务器...")
    print("访问地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)