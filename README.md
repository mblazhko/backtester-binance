# backtester-binance

## Task

1. Отримати 4 роки 1-хвилинних свічок з Binance API (pip install python-binance)
2. Зберегти дані котируваня в .csv файл
3. Завантажити бібліотеку TALib (працює з python 3.10.8)
4. Переписати з PineScript індикатори RSIBANDS_LB:

```
    study("RSI Bands [LazyBear]", shorttitle="RSIBANDS_LB", overlay=true)
    obLevel = input(70, title="RSI Overbought")
    osLevel = input(30, title="RSI Oversold")
    length = input(14, title="RSI Length")
    src=close
    ep = 2 * length - 1
    auc = ema( max( src - src[1], 0 ), ep )
    adc = ema( max( src[1] - src, 0 ), ep )
    x1 = (length - 1) * ( adc * obLevel / (100-obLevel) - auc)
    ub = iff( x1 >= 0, src + x1, src + x1 * (100-obLevel)/obLevel )
    x2 = (length - 1) * ( adc * osLevel / (100-osLevel) - auc)
    lb = iff( x2 >= 0, src + x2, src + x2 * (100-osLevel)/osLevel )
    
    plot( ub, title="Resistance", color=red, linewidth=2)
    plot( lb, title="Support", color=green, linewidth=2)
    plot( avg(ub, lb), title="RSI Midline", color=gray, linewidth=1)
```



5. Імпортувати індикатор CCI з TALib (період CCI - “30”)
6. Реалізувати окремим скриптом торгову стратегію, що приймає на вхід історію котирування і розраховує індикатори CCI та RSIBANDS_LB, якщо поточна ціна активу перетинає нижню лінію RSIBANDS_LB згори вниз, а CCI менше “-100”, відкрити LONG з TP 1% та SL 0.4%; якщо поточна ціна активу перетинає верхню лінію RSIBANDS_LB знизу вгору, а CCI більше “120”, відкрити SHORT з TP 1.1% та SL 0.5%. Об’єм торгівлі - завжди 100$, комісія - 0.5%. (Ці трейди ніде не треба відкривати, лише повернути з метода get_signals класу Strategy або {“action”:false}, або {“action”:, true, “entry price”: ціна входу в трейд, “TP”: ціна фіксації прибутку, “SL”: ціна фіксації збитків}).
7. Реалізувати окремим скриптом бектестер, яким пройдеться по 4 рокам історичних даних з Binance і визначить відповідно до стратегії абсолютний прибуток/збиток, winrate (відсоток прибуткових угод), profit factor.


## How to use

1. Run ```python binance_data.py``` to get data from Binance. Data will be stored as binance_data.csv.
2. Run ```python main.py``` to test strategy and get metrics