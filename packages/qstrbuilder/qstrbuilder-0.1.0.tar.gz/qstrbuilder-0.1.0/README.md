qstrbuilder: Build Strings Quantitatively
=======================

qstrbuilder is a number formatter that use numerical parameters (rather than magic string) to control the number formatting.

### API

`build(number: float, width: Optional[int]=None, precision: Optional[int]=None) -> str`


### Usage Example

```
from qstrbuilder import build
s = build(2., width=4, precision=1)
print(s)   # Output " 2.0"
```
