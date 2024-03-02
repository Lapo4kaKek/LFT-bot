### 1) Example use function "set_leverage"

```python
bybit = BybitExchange(api_key_bybit, api_secret_bybit)
print(bybit.set_leverage("ARBUSDT", 2))
```
#### when you select а pair of tokens, you need to glue then together 
#### Example: You want set_leverage in pair SOL/USDT, you need send SOLUSDT (SOL+USDT)
