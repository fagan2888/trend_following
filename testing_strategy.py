from strategy import *
import matplotlib.pyplot as plt


# british pound
bp = get_market_data('british_pound')
bp = make_continuous(bp)
bp['Close'] = fix_quotes(bp, 50, 'Close')
bp = strategy(bp, fast_ema=42, slow_ema=252)
bp.plot(y=['Close', 'fast_ma', 'slow_ma'], title='British Pound, Continuous', figsize=(14, 8), linewidth=1)
plt.show()

# canadian dollar
cd = get_market_data('canadian_dollar')
cd = make_continuous(cd)
cd['Close'] = fix_quotes(cd, 30, 'Close')
cd = strategy(cd, fast_ema=42, slow_ema=252)
cd.plot(y=['Close', 'fast_ma', 'slow_ma'], title='Canadian Dollar, Continuous', figsize=(14, 8), linewidth=1)
plt.show()
