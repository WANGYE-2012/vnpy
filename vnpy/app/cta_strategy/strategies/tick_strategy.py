from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)
import datetime
from datetime import time

class TickStrategy(CtaTemplate):
    author = "WangYe"

    fast_window = 10
    slow_window = 20

    a = 0
    b = 0

    day_open = 0.0
    exit_time = time(hour=14, minute=55)

    parameters = ["fast_window", "slow_window"]
    variables = ["day_open"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        # 范围时间
        # d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '8:55', '%Y-%m-%d%H:%M')
        # d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '20:59', '%Y-%m-%d%H:%M')
        #
        # # 当前时间
        # n_time = datetime.datetime.now()
        #
        # # 判断当前时间是否在范围时间内
        # if n_time > d_time and n_time < d_time1:
        #     if self.day_open:
        #         self.buy(self.day_open * 1.04, 1)
        #         print(self.day_open)
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")
        self.put_event()

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        if self.pos == 0 and self.a == 0:
            self.buy(tick.limit_up,1)
        if self.pos > 0 and self.a == 0:
            self.sell(tick.open_price + 2, abs(self.pos))
            self.a = 1
        elif self.pos < 0 and self.b == 0:
            self.cover(tick.open_price - 2, abs(self.pos))
            self.b = 1
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        #self.day_open = bar.close_price
        if bar.datetime.time() > self.exit_time:
            self.cancel_all()
            if self.pos > 0:
                self.sell(bar.close_price * 0.99, abs(self.pos))
            elif self.pos < 0:
                self.cover(bar.close_price * 1.01, abs(self.pos))

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
