### Example of using a hexadecimal to wei/decimal converter
```python
client = HyperLiquidExchange(os.getenv('METAMASK_PKEY'))
balance = client.get_balance() # example, result = 0xf9c8cb532800

value = Converter.hex_to_eth(balance) # 0.0002746408

or 

value = Converter.hex_to_big(balance) # 274640800000000
```