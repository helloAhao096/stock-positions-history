import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional


class StockDataManager:
    """股票数据管理器"""
    
    def __init__(self, data_dir: str = "stock-positions-history"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_positions(self, positions: List[Dict], timestamp: Optional[datetime] = None, account_summary: Optional[Dict] = None) -> str:
        """
        保存持仓数据到文件
        
        Args:
            positions: 持仓数据列表
            timestamp: 时间戳，如果为None则使用当前时间
            account_summary: 账户资金和盈亏信息
            
        Returns:
            保存的文件路径
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # 清洗positions，去除所有Unnamed字段和空key字段
        def clean_position_dict(d):
            return {k: v for k, v in d.items() if not str(k).startswith('Unnamed') and str(k).strip() != ''}
        cleaned_positions = [clean_position_dict(pos) for pos in positions]
        
        # 生成文件名：YYYY-MM-DD.json
        date_str = timestamp.strftime("%Y-%m-%d")
        filename = f"{date_str}.json"
        filepath = self.data_dir / filename
        
        # 准备保存的数据
        data = {
            "date": date_str,
            "timestamp": timestamp.isoformat(),
            "positions": cleaned_positions,
            "position_count": len(cleaned_positions) if cleaned_positions else 0,
            "account_summary": account_summary or {}
        }
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"持仓数据已保存到: {filepath}")
        return str(filepath)
    
    def load_positions(self, date: str) -> Optional[Dict]:
        """
        加载指定日期的持仓数据
        
        Args:
            date: 日期字符串，格式为 YYYY-MM-DD
            
        Returns:
            持仓数据字典，如果文件不存在则返回None
        """
        filepath = self.data_dir / f"{date}.json"
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"加载数据文件失败: {e}")
            return None
    
    def get_latest_positions(self) -> Optional[Dict]:
        """
        获取最新的持仓数据（今天的或最近一天的）
        
        Returns:
            最新的持仓数据字典
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 先尝试获取今天的数据
        data = self.load_positions(today)
        if data:
            return data
        
        # 如果没有今天的数据，获取最近一天的数据
        json_files = list(self.data_dir.glob("*.json"))
        if not json_files:
            return None
        
        # 按文件名排序，获取最新的
        latest_file = sorted(json_files)[-1]
        date_str = latest_file.stem
        
        return self.load_positions(date_str)
    
    def get_available_dates(self) -> List[str]:
        """
        获取所有可用的数据日期
        
        Returns:
            日期字符串列表
        """
        json_files = list(self.data_dir.glob("*.json"))
        dates = [f.stem for f in json_files]
        return sorted(dates)
    
    def format_positions_for_display(self, positions: List[Dict]) -> List[Dict]:
        """
        格式化持仓数据用于网页显示
        
        Args:
            positions: 原始持仓数据
            
        Returns:
            格式化后的持仓数据
        """
        if not positions:
            return []
        
        formatted = []
        for pos in positions:
            # 根据easytrader返回的数据结构进行格式化
            formatted_pos = {
                "股票代码": pos.get("证券代码", ""),
                "股票名称": pos.get("证券名称", ""),
                "持仓数量": pos.get("股票余额", 0),
                "可用数量": pos.get("可用余额", 0),
                "成本价": pos.get("成本价", 0),
                "当前价": pos.get("市价", 0),
                "盈亏金额": pos.get("盈亏", 0),
                "盈亏比例": pos.get("盈亏比(%)", 0),
                "市值": pos.get("市值", 0),
                "仓位占比": pos.get("仓位占比(%)", 0),
                "当日盈亏比": pos.get("当日盈亏比(%)", 0),
                "持股天数": pos.get("持股天数", 0)
            }
            formatted.append(formatted_pos)
        
        return formatted 