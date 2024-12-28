import re
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class Node:
    def __init__(self):
        self.children = {}
        self.value = None
        self.order = None
    def set_leaf(self, value:str, order:int):
        self.value = value
        self.order = order

class BestMatch:
    def __init__(self, key_len=None, value=None, order=float('inf')):
        self.key_len = key_len
        self.value = value
        self.order = order
        self.unmatched_len = 0

class SpecialTrie:
    def __init__(self):
        self.ORDER = 0
        self.root = Node()
        self.__reset_progress()

    def next(self, char:str)-> tuple[bool, BestMatch]:
        # this will run untill it matches, if stuck returns 
        # lowest key, value of the node
        if char not in self.current_node.children:
            self.__reset_progress()
            return False, self.best_match
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
    
    def insert(self, key:str, value:str)-> int:
        has_prefix = False
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = self.Node()
            node = node.children[char]

            if node.value: 
                has_prefix = True
                logger.debug(f"Prefix found: {key} -> {node.value}")
        node.set_leaf(value, self.ORDER)
        self.ORDER += 1
        return has_prefix

    def build(self, patterns:list, values:list)-> int:
        total_prefix = 0
        for pattern, value in zip(patterns, values):
            total_prefix += self.insert(pattern, value)
        return total_prefix
    
    def search(self, key:str)-> str:
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value
    

def ncr_to_unicode(text:str)-> str:
    return re.sub(r'&#(\d+);', lambda match: chr(int(match.group(1))), text)

if __name__ == '__main__':
    file_name = "lab/sutonnymj_mapper.json"
    modified_file_name = "lab/modified_sutonnymj_mapper.json"
    data = json.load(open(file_name, 'r'))

    find, replace = data["find"], data["replace"]
    find = [ncr_to_unicode(pattern) for pattern in find]
    replace = [ncr_to_unicode(pattern) for pattern in replace]
    with open(modified_file_name, "w") as file:
        json.dump(
            {"find": find, "replace": replace}, 
            file, 
            indent=4
        )
    assert len(find) == len(replace), f"For {file_name} find and replace must have the same length."
    trie = SpecialTrie()
    total_prefix = trie.build(find, replace)
    logger.debug(f"Total prefix found: {total_prefix}")

    text = "Avjø¬vn, Avãyi iwng, Zvi gvÑevev I ¯Íªx †K Rv›bvZyj wdi`vDm `vb Kiyb, Avgxb|"
    idx, ln = 0, len(text)
    unicode_text = []
    last_idx = 0
    while idx < ln:
        has_next, match = trie.next(text[idx])
        if not has_next:
            unicode_text.append(match.value)
            last_idx+=max(match.key_len,1)
            idx = last_idx
        else:
            idx+=1