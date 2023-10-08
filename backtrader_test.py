import backtrader as bt


class MyStrategy(bt.Strategy):
    params = (
        ('ob_level', 70),
        ('os_level', 30),
        ('length', 14),
        ('cci_long', -100),
        ('cci_short', 120),
        ('tp_long', 1.01),
        ('sl_long', 0.996),
        ('tp_short', 1.011),
        ('sl_short', 0.995),
        ('trade_size', 100),
        ('commission', 0.005),
    )

    def __init__(self):
        self.cci = bt.indicators.CCI(period=30)
        ep = 2 * self.p.length - 1
        auc = bt.indicators.EMA(
            bt.indicators.Max(self.data.close - self.data.close(-1), 0),
            period=ep
        )
        adc = bt.indicators.EMA(
            bt.indicators.Max(self.data.close(-1) - self.data.close, 0),
            period=ep
        )

        x1 = (self.p.length - 1) * (adc * self.p.ob_level / (100 - self.p.ob_level) - auc)
        self.ub = bt.If(x1 >= 0, self.data.close + x1, self.data.close + (x1 * (100 - self.p.ob_level) / self.p.ob_level))
        x2 = (self.p.length - 1) * (adc * self.p.os_level / (100 - self.p.os_level) - auc)
        self.lb = bt.If(x2 >= 0, self.data.close + x2, self.data.close + (x2 * (100 - self.p.os_level) / self.p.os_level))
        
    def next(self):
        if self.data.close > self.ub and self.cci < self.p.cci_long:
            self.buy(
                exectype=bt.Order.Stop,
                price=self.data.close * self.p.tp_long,
                qty=self.p.trade_size,
                transmit=False
            )
            self.sell(
                price=self.data.close * self.p.sl_long,
                qty=self.p.trade_size,
                transmit=False
            )
        elif self.data.close < self.lb and self.cci > self.p.cci_short:
            self.sell(
                exectype=bt.Order.Stop,
                price=self.data.close * self.p.tp_short,
                qty=self.p.trade_size,
                transmit=False
            )
            self.buy(
                price=self.data.close * self.p.sl_short,
                qty=self.p.trade_size,
                transmit=False
            )


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    data = bt.feeds.GenericCSVData(
        dataname='binance_data.csv',
        nullvalue=0.0,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.005)
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
