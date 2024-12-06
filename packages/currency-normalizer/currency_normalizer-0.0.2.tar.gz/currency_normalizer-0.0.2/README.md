Whole purpose of this package is to normlize currency strings to the standard currency codes

You can input USD or $ or USD dollars and it will be normalized. This is it. 


```

cn = CurrencyNormalizer()
r=cn.normalize("$")
print(r)

# output is "USD"

```




