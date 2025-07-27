from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from data_manager import StockDataManager
from main import update_positions
import json
from datetime import datetime
from pathlib import Path

app = FastAPI(title="股票持仓管理系统", description="实时查看和管理股票持仓数据")

# 创建templates目录
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory="templates")

data_manager = StockDataManager()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """主页 - 显示最新持仓数据"""
    latest_data = data_manager.get_latest_positions()
    
    if latest_data:
        positions = data_manager.format_positions_for_display(latest_data['positions'])
        update_time = datetime.fromisoformat(latest_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    else:
        positions = []
        update_time = "暂无数据"
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "positions": positions, 
        "update_time": update_time
    })

@app.get("/api/positions")
async def api_positions():
    """API接口 - 获取最新持仓数据"""
    latest_data = data_manager.get_latest_positions()
    
    if latest_data:
        positions = data_manager.format_positions_for_display(latest_data['positions'])
        return {
            'success': True,
            'data': {
                'positions': positions,
                'update_time': latest_data['timestamp'],
                'position_count': latest_data['position_count']
            }
        }
    else:
        return {
            'success': False,
            'message': '暂无持仓数据'
        }

@app.get("/api/update")
async def api_update():
    """API接口 - 手动更新持仓数据"""
    try:
        success = update_positions()
        if success:
            return {
                'success': True,
                'message': '持仓数据更新成功'
            }
        else:
            return {
                'success': False,
                'message': '当前无持仓或更新失败'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'更新失败: {str(e)}'
        }

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    """历史数据页面"""
    available_dates = data_manager.get_available_dates()
    return templates.TemplateResponse("history.html", {
        "request": request, 
        "dates": available_dates
    })

@app.get("/api/history/{date}")
async def api_history(date: str):
    """API接口 - 获取指定日期的持仓数据"""
    data = data_manager.load_positions(date)
    
    if data:
        positions = data_manager.format_positions_for_display(data['positions'])
        return {
            'success': True,
            'data': {
                'positions': positions,
                'update_time': data['timestamp'],
                'position_count': data['position_count']
            }
        }
    else:
        return {
            'success': False,
            'message': f'未找到 {date} 的数据'
        }

@app.get("/api/dates")
async def api_dates():
    """API接口 - 获取所有可用日期"""
    dates = data_manager.get_available_dates()
    return {
        'success': True,
        'dates': dates
    }

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=5000) 