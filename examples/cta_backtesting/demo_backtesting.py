from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
from vnpy.app.cta_strategy.strategies.tick_strategy import (
    TickStrategy,
)
from vnpy.app.cta_strategy.base import BacktestingMode
from datetime import datetime

engine = BacktestingEngine()
engine.set_parameters(
    mode=BacktestingMode.TICK,
    vt_symbol="c2005.DCE",
    interval="1m",
    start=datetime(2019, 1, 1),
    end=datetime(2020, 3, 20),
    rate=0.3/10000,
    slippage=0.2,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
    collection_name ="c2005"
    
)
engine.add_strategy(TickStrategy, {})

engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()