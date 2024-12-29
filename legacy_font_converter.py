import os
import re
import json
import logging

from special_trie import SpecialTrie

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegacyFontConverter:
    def __init__(self, json_path="resources"):
        self.mapper = {}
        self.path = {}
        for file in os.listdir(json_path):
            if not file.endswith(".json"): continue
            name = ".".join(file.split(".")[:-1])
            self.mapper[name] = None
                
            self.path[name] = os.path.join(json_path, file)
        
    
    def __load_mapper(self, name):
        try:
            with open(self.path[name], 'r') as file:
                data = json.load(file)
            assert "find" in data and "replace" in data, "Invalid json format"
            trie = SpecialTrie(patterns=data["find"], values=data["replace"])
            trie_inverse = SpecialTrie(patterns=data["replace"], values=data["find"])
            print(f"{name} mapper loaded successfully.")
        except Exception as e:
            print(f"Error: {e}")
        
        self.mapper[name] = trie
        self.mapper[name+"_inverse"] = trie_inverse

    
    def convert(self, text, font_name="sutonnymj", to_legacy=False):
        """
            text: string to convert
            font_name: name of the font to convert should be in the available list
            to_legacy: if True, convert from font to unicode, else unicode to font
        """
        font_name = font_name.lower()
        assert font_name in self.mapper, f"Font {font_name} not found. call available_fonts() to see available fonts."
        if self.mapper[font_name] is None:
            self.__load_mapper(font_name)
        
        if to_legacy: font_name += "_inverse"
        return self.mapper[font_name].convert(text)
    

if __name__ == '__main__':
    legacy_font_converter = LegacyFontConverter()
    text = "আল্লাহ, আব্দুর রহিম, তার মা-বাবা ও স্ত্রী কে জান্নাতুল ফিরদাউস দান করুন, আমীন।"
   
    sutonnymj = "Avjø¬vn, Avãyi iwng, Zvi gvÑevev I ¯Íªx †K Rv›bvZyj wdi`vDm `vb Kiyb, Avgxb|"

    converted = legacy_font_converter.convert(sutonnymj,'sutonnymj')
    assert text == converted, f"Sutonnymj: Expected: {text}\n Got: {converted}"
    logger.info("Hurrah!! sutonnymj passed!")