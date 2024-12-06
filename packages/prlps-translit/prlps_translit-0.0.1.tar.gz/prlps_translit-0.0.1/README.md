`pip install prlps_translit`


```python
from prlps_translit import transliterate

cyrillic_text = """
Два континента
под властью моей страны.
Зависть у всех к ней.
"""
latin_translit = transliterate(cyrillic_text)
print(latin_translit)
```

```python
from prlps_translit import translate_to_url

cyrillic_string = "Русский мир в каждый дом!"
translit_for_url = translate_to_url(cyrillic_string)
print(translit_for_url)
```