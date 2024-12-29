import json
import copy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Node:
    def __init__(self):
        self.children = {}
        self.value = None
        self.order = float('inf')
    def set_leaf(self, value:str, order:int):
        self.value = value
        self.order = order

class BestMatch:
    def __init__(self, value=None, order=float('inf')):
        self.key_len = 0
        self.value = value
        self.order = order
        self.unmatched_len = 0
    def __str__(self):
        return f"{self.value=}\n {self.order=}\n {self.key_len=}\n {self.unmatched_len=}"
        
class SpecialTrie:
    def __init__(self, patterns: list[str], values: list[str]):
        """
            This special trie matches text replace with the lowest
            order key as the key might have prefix relation.
            So pass the pattern in a order where earlier pattern will be 
            replaced first.
            args:
                patterns: list of unicode patterns in highest to lowest precedence
                values: list of unicode values for particular pattern
                note: their length must be same
                note2: strings should in plain unicode values 
                i.e.:A unicode string for sutonnoymj legacy font "Avjø¬vn, Avãyi iwng, Zvi gvÑevev I ¯Íªx †K Rv›bvZyj wdi`vDm `vb Kiyb, Avgxb|" 

        """
        assert len(patterns) == len(values), "Patterns and values must have the same length."
        self.ORDER = 0
        self.root = Node()
        self.__reset_progress()
        total_prefix = self.__build(patterns, values)
        logger.info(f"Total prefix found: {total_prefix}")

    def convert(self, text:str)-> str:
        EOF = "\U0010FFFF"
        text += EOF
        idx, ln = 0, len(text)
        unicode_text = []
        while idx < ln:
            has_next, match = self.__next(text[idx])
            if not has_next:
                idx-=match.unmatched_len
                if not match.value:
                    unicode_text.append(text[idx])
                    idx+=1
                else:
                    unicode_text.append(match.value)
                
            else: idx+=1
        return "".join(unicode_text[:-1])

    def search(self, key:str)-> str:
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value
    
    def __next(self, char:str)-> tuple[bool, BestMatch]:
        # this will run untill it matches, if stuck returns 
        # lowest key, value of the node
        if char not in self.current_node.children:
            match = copy.deepcopy(self.best_match)
            self.__reset_progress()
            return False, match

        self.current_node = self.current_node.children[char]
        self.key_len += 1
        if self.current_node.value and self.current_node.order < self.best_match.order:
            self.best_match.key_len =  self.key_len
            self.best_match.value = self.current_node.value
            self.best_match.order = self.current_node.order

        self.best_match.unmatched_len = self.key_len - self.best_match.key_len
        
        return True, self.best_match
    
    def __reset_progress(self):
        self.current_node = self.root
        self.key_len = 0
        self.best_match = BestMatch()
    
    def __insert(self, key:str, value:str)-> int:
        has_prefix = False
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]

            if node.value: has_prefix = True
        if self.ORDER < node.order:        
            node.set_leaf(value, self.ORDER)
        self.ORDER += 1
        return has_prefix

    def __build(self, patterns:list[str], values:list[str])-> int:
        # we expect patterns and values are in ncr format 
        total_prefix = 0
        for pattern, value in zip(patterns, values):
            total_prefix += self.__insert(pattern, value)
        return total_prefix
    
    
if __name__ == '__main__':
    file_name = "lab/modified_sutonnymj_mapper.json"
    
    data = json.load(open(file_name, 'r'))

    find, replace = data["find"], data["replace"]

    sutonnymj_to_unicode = SpecialTrie(find, replace)
    unicode_to_sutonnymj = SpecialTrie(replace, find)
    original_text = "আল্লাহ, আব্দুর রহিম, তার মা-বাবা ও স্ত্রী কে জান্নাতুল ফিরদাউস দান করুন, আমীন।"
    text = "Avjø¬vn, Avãyi iwng, Zvi gvÑevev I ¯Íªx †K Rv›bvZyj wdi`vDm `vb Kiyb, Avgxb|"
    
    logger.info(sutonnymj_to_unicode.convert(text))
    convert = sutonnymj_to_unicode.convert(text)
    

    assert convert == original_text, f"{convert} != {original_text}"
    
    convert = unicode_to_sutonnymj.convert(original_text)
    convert_back = sutonnymj_to_unicode.convert(convert)
    assert convert_back == original_text, f"{convert_back} != {original_text}"
    logger.info("Hurrah! Conversion successful.")
    logger.info(f"Converted: {convert}")
    logger.info(f"Converted back: {convert_back}")

