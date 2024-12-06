# langcode_turner

A tool to turn language code to other language code.
Such as ISO 639-1 to ISO 639-3.
en -> eng
or
ISO 639-3 to ISO 639-1
est -> et

# Usage

## install
```
pip install langcode_turner
```

## use
```python
from langcode_turner import LangcodeTurner

langcode = LangcodeTurner("cho")
print(langcode.iso_639_3)

```

# update log

- v0.0.1 build code
- v0.0.2 - v0.0.6 fix error
- v0.0.6 a normal version
- v0.0.7 add baidu langcode

# License
MIT License

# Author
Feliks Peegel

