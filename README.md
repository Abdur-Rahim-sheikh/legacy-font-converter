# Abdur-Rahim Sheikh Legacy Font Converter

A Python package for converting legacy fonts.

## Introduction
In today's context we use or will use LLM (Large Language Models) in our daily life. But the problem is that the LLMs are trained on the Unicode text. But in many cases, we have to deal with the legacy fonts. So, this package will help you to convert the legacy fonts to Unicode text.

Specially for Bangla language, there are many legacy fonts like SutonnyMJ, SolaimanLipi, etc. Which are used in docx files, pdf files, etc.But we have no help to work with them programatically. So, this package will help you to convert those legacy fonts to Unicode text. To easily encorporate with issues like feeding the LLMs and revert back the llm response to the legacy fonts.

## Available fonts
- [x] SutonnyMJ
- [ ] Salma
- [ ] SolaimanLipi
- [ ] Nikosh


## Features
```python
convert(text:str, font_name:str, to_legacy:bool)->str
available_fonts()->list[str]
```
## Installation

You can install the package using pip:

```bash
pip install legacy-font-converter
```

Or you can install the package from source:

```bash
pip install git+https://github.com/Abdur-Rahim-sheikh/legacy-font-converter.git
```

## usages

```python
from legacy_font_converter import LegacyFontConverter
legacy_font_converter = LegacyFontConverter()
sutonnymj_text = "Avjø¬vn, Avãyi iwng, Zvi gvÑevev I ¯Íªx †K Rv›bvZyj wdi`vDm `vb Kiyb, Avgxb|"
text = legacy_font_converter.convert(sutonnymj_text,font_name='sutonnymj', to_legacy=False)
print(text)
```


## Reference
- A big applaus to [True finder studio](https://github.com/truefinderstudio)

