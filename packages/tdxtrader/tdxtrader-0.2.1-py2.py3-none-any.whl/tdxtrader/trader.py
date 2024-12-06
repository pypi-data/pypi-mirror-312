from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
import random
from tdxtrader.utils import timestamp_to_datetime_string, parse_order_type, convert_to_current_date

class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        """
        连接状态回调
        :return:
        """
        print("connection lost")
    def on_stock_order(self, order):
        """
        委托信息推送
        :param order: XtOrder对象
        :return:
        """
        if order.order_status == 50:
            print(f"【已委托】类型: {parse_order_type(order.order_type)} 订单编号:{order.order_id} 代码:{order.stock_code} 委托价格:{order.price:.2f} 委托数量:{order.order_volume} 委托时间:{timestamp_to_datetime_string(convert_to_current_date(order.order_time))} {timestamp_to_datetime_string(order.order_time)}")
    def on_stock_trade(self, trade):
        """
        成交信息推送
        :param trade: XtTrade对象
        :return:
        """
        print(f"【已成交】类型: {parse_order_type(trade.order_type)} 成交编号:{trade.order_id} 代码:{trade.stock_code} 成交价格:{trade.traded_price:.2f} 成交数量:{trade.traded_volume} 成交时间:{timestamp_to_datetime_string(convert_to_current_date(trade.traded_time))}")

def create_trader(account_id, mini_qmt_path):
    # 创建session_id
    session_id = int(random.randint(100000, 999999))
    # 创建交易对象
    xt_trader = XtQuantTrader(mini_qmt_path, session_id)
    # 启动交易对象
    xt_trader.start()
    # 连接客户端
    connect_result = xt_trader.connect()

    if connect_result == 0:
        print('连接成功')

    # 创建账号对象
    account = StockAccount(account_id)
    # 订阅账号
    xt_trader.subscribe(account)
    # 注册回调类
    xt_trader.register_callback(MyXtQuantTraderCallback())

    return xt_trader, account