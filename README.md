# 股票持仓管理系统

一个基于FastAPI的股票持仓实时监控和管理系统，通过easytrader连接同花顺客户端获取持仓数据。

## 功能特性

- 📊 **实时持仓监控**: 实时显示股票持仓信息，包括盈亏情况
- 💾 **智能数据存储**: 按日期自动存储持仓数据，每天只保留最新一次
- 📈 **历史数据查看**: 查看历史持仓数据，支持按日期筛选
- 🔄 **自动刷新**: 页面自动刷新数据，保持信息最新
- 🎨 **现代化UI**: 使用Bootstrap构建的响应式界面
- 📱 **移动端适配**: 支持手机和平板设备访问

## 系统架构

```
stockData/
├── main.py              # 主要功能模块，连接同花顺客户端
├── data_manager.py      # 数据管理模块，处理数据存储和读取
├── web_app.py          # FastAPI Web应用
├── start_web.py        # Web应用启动脚本
├── easytrader_patch.py # easytrader补丁文件
├── stock_history/      # 持仓数据存储目录
├── templates/          # HTML模板文件
│   ├── index.html     # 主页模板
│   └── history.html   # 历史数据页面模板
└── pyproject.toml     # 项目依赖配置
```

## 安装和配置

### 1. 安装依赖

```bash
# 使用uv安装依赖
uv sync

# 或者使用pip
pip install -r requirements.txt
```

### 2. 配置同花顺路径

在 `main.py` 中修改同花顺客户端路径：

```python
trader_path = r"C:\同花顺软件\同花顺\xiadan.exe"  # 修改为你的实际路径
```

### 3. 启动Web应用

```bash
# 方式1: 使用启动脚本
python start_web.py

# 方式2: 直接运行
python web_app.py

# 方式3: 使用uvicorn
uvicorn web_app:app --host 0.0.0.0 --port 5000 --reload
```

### 4. 访问系统

- 主页: http://localhost:5000
- API文档: http://localhost:5000/docs
- 历史数据: http://localhost:5000/history

## 使用说明

### 数据获取

1. **手动获取**: 点击页面上的"更新持仓"按钮
2. **自动获取**: 运行 `python main.py` 获取并保存数据
3. **定时任务**: 可以设置定时任务定期运行 `update_positions()` 函数

### 数据存储

- 数据按日期存储在 `stock_history/` 目录下
- 文件命名格式: `YYYY-MM-DD.json`
- 每天多次运行只会保留最新一次的数据

### API接口

- `GET /api/positions` - 获取最新持仓数据
- `GET /api/update` - 手动更新持仓数据
- `GET /api/history/{date}` - 获取指定日期的历史数据
- `GET /api/dates` - 获取所有可用日期

## 数据格式

持仓数据包含以下字段：

```json
{
  "股票代码": "000001",
  "股票名称": "平安银行",
  "持仓数量": 1000,
  "可用数量": 1000,
  "成本价": 12.50,
  "当前价": 13.20,
  "盈亏金额": 700.00,
  "盈亏比例": 5.60,
  "市值": 13200.00
}
```

## 注意事项

1. **同花顺客户端**: 确保同花顺客户端已安装并可以正常登录
2. **网络连接**: 需要稳定的网络连接获取实时数据
3. **权限问题**: 确保程序有足够的权限访问同花顺客户端
4. **数据安全**: 持仓数据包含敏感信息，请妥善保管

## 开发说明

### 添加新功能

1. 在 `data_manager.py` 中添加数据处理逻辑
2. 在 `web_app.py` 中添加API接口
3. 在 `templates/` 中添加或修改HTML模板

### 自定义样式

修改HTML模板中的CSS样式来自定义界面外观。

### 扩展数据源

可以修改 `main.py` 中的连接逻辑来支持其他交易软件。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
