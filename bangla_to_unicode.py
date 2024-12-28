import re
import json
class BanglaToUnicode:
    def __init__(self):
        self.sutonnymj_mapper = None
        self.geetanjali_mapper = None
        self.path = {
            "sutonnymj": 'resources/sutonnymj_mapper.json',
            "geetanjali": 'resources/geetanjali_mapper.json'
        }
        
    def unicode_to_ncr(self, text):
        # NCR = Numeric Character Reference Example: 'A' -> '&#65;'
        return ''.join(f'&#{ord(char)};' for char in text)
    
    def ncr_to_unicode(self, text):
        # Example: '&#65;' -> 'A'
        return re.sub(r'&#(\d+);', lambda match: chr(int(match.group(1))), text)
    
    def __load_mapper(self, name):
        try:
            with open(self.path[name], 'r') as file:
                data = json.load(file)
                setattr(self, f"{name}_mapper", data)
            assert len(data["find"]) == len(data["replace"]), f"For {name} find and replace must have the same length."
            print(f"{name} mapper loaded successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def from_sutonnymj(self, text):
        if not self.sutonnymj_mapper:
            self.__load_mapper("sutonnymj")
        
        return self.convert(text, self.sutonnymj_mapper["find"], self.sutonnymj_mapper["replace"])
    
    def to_sutonnymj(self, text):
        if not self.sutonnymj_mapper:
            self.__load_mapper("sutonnymj")
        
        return self.convert(text, self.sutonnymj_mapper["replace"], self.sutonnymj_mapper["find"])
    
    def from_geetanjali(self, text):
        if not self.geetanjali_mapper:
            self.__load_mapper("geetanjali")
        return self.convert(text, self.geetanjali_mapper["find"], self.geetanjali_mapper["replace"])
    
    def to_geetanjali(self, text):
        if not self.geetanjali_mapper:
            self.__load_mapper("geetanjali")
        return self.convert(text, self.geetanjali_mapper["replace"], self.geetanjali_mapper["find"])
    
    def convert(self, text, find_patterns, replace_patterns):
        text = self.unicode_to_ncr(text)
        for find, replace in zip(find_patterns, replace_patterns):
            text = re.sub(find, replace, text)
        
        return self.ncr_to_unicode(text)
    

if __name__ == '__main__':
    bangla_to_unicode = BanglaToUnicode()
    text = "আল্লাহ, আব্দুর রহিম, তার মা-বাবা ও স্ত্রী কে জান্নাতুল ফিরদাউস দান করুন, আমীন।"
    geetanjali = "aal্lাh, aab্dুR Rhিm, tাR mা-bাbা o s্t্Rী kে jাn্nাtুl PিRdাus dাn kRুn, aamীn|"
    sutonnymj = "Avjø¬vn, Avãyi iwng, Zvi gvÑevev I ¯Íªx †K Rv›bvZyj wdi`vDm `vb Kiyb, Avgxb|"
    converted = bangla_to_unicode.from_sutonnymj(sutonnymj)
    assert text == converted, f"Sutonnymj: Expected: {text}\n Got: {converted}"
    print("Hurrah!! sutonnymj passed!")

    converted = bangla_to_unicode.from_geetanjali(geetanjali)
    assert text == converted, f"geetanjali: Expected: {text}\n Got: {converted}"
    print("Hurrah!! geetanjali passed!")