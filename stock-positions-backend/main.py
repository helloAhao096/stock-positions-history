import easytrader
from data_manager import StockDataManager
from datetime import datetime


def connect_to_ths(trader_path: str):
    """连接同花顺客户端"""
    import easytrader_patch 

    user = easytrader.use('ths')
    user.connect(trader_path)
    return user

def print_position_and_trades(user):
    positions = user.position
    if not positions:
        print("当前无持仓")
        return

    print("\n=== 当前持仓列表 ===\n")
    print(positions)
    return positions

def save_positions_to_file(positions, account_summary=None):
    """保存持仓数据到文件"""
    data_manager = StockDataManager()
    filepath = data_manager.save_positions(positions, account_summary=account_summary)
    return filepath

def get_latest_positions():
    """获取最新的持仓数据"""
    data_manager = StockDataManager()
    return data_manager.get_latest_positions()

def main():
    trader_path = r"C:\同花顺软件\同花顺\xiadan.exe"

    try:
        user = connect_to_ths(trader_path)
        positions = print_position_and_trades(user)
        account_summary = None
        try:
            # 优先尝试 user.balance
            account_summary = user.balance
        except Exception:
            try:
                # 兼容不同券商，尝试 user.assets
                account_summary = user.assets
            except Exception:
                account_summary = None
        
        if positions:
            # 保存持仓数据和账户资金信息
            filepath = save_positions_to_file(positions, account_summary=account_summary)
            print(f"\n持仓数据已保存到: {filepath}")
        
    except Exception as e:
        print(f"出现错误：{e}")

def update_positions():
    """更新持仓数据（用于定时任务）"""
    trader_path = r"C:\同花顺软件\同花顺\xiadan.exe"
    
    try:
        user = connect_to_ths(trader_path)
        positions = user.position
        account_summary = None
        try:
            account_summary = user.balance
        except Exception:
            try:
                account_summary = user.assets
            except Exception:
                account_summary = None
        
        if positions:
            data_manager = StockDataManager()
            filepath = data_manager.save_positions(positions, account_summary=account_summary)
            print(f"持仓数据已更新: {filepath}")
            return True
        else:
            print("当前无持仓")
            return False
            
    except Exception as e:
        print(f"更新持仓数据失败: {e}")
        return False

if __name__ == "__main__":
    main()
