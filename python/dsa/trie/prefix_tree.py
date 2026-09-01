"""
    Design:
        - declare TrieNode class:
            - char: str
            - children: {}
            - is_end: bool
        - in __init__: build trie based on the map
            - root = TrieNode()
        - in addWord: fill the trie
            init current starting from root
            iterate through word:
                if char in current.children:
                    current <- root[char]
                else:
                    root[char] = TrieNode(), create new child node
                    current <- root[char]
            current.is_end = true, set end of word

        - in search: 
            - first build standard search in trie
                init current from root
                iterate through word:
                    if char not in root.children: return false
                    current <- root[char]
                return if current.is_end
            - then handle dots '.' case
                init current from root
                iterate through word:
                    if char is not '.':
                        if char not in root.children: return false
                        current <- root[char]
                    else:
                        [backtracking approach] means iterate over all possible chars [a-z]
                        found = false
                        temp_char from a to z:
                            if temp_char in root.children: 
                                current <- root[temp_char]
                                found = true
                                break
                        if not found: return false




    Timeline:
        - understanding the problem 10:00
        - design 10:10 [standard trie, without dots case]
        - coding 10:20
        - testing 10:23
        - design dots case 10:29
        - coding dots case 10:40
        - testing dots case 10:48
        - submitting 10:50
        - testing edge cases 10:50
"""


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.is_end = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode('')
        self.chars = "abcdefghijklmnopqrstuvwxyz"

    # "bad"
    def addWord(self, word: str) -> None:
        current = self.root
        for c in word:  # b
            if c in current.children:
                current = current.children[c]
            else:
                current.children[c] = TrieNode(c)
                current = current.children[c]
        current.is_end = True
        return

    # ".ad", "b.."
    def search(self, word: str) -> bool:
        current = self.root
        for c in word:
            if c != '.':
                if c not in current.children:
                    return False
                current = current.children[c]
            else:
                found = False
                for temp_char in self.chars:
                    if temp_char in current.children:
                        current = current.children[temp_char]
                        found = True

                if not found:
                    return False

        return current.is_end

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)


"""
    Design:
        - __init__ 
            build TrieNode and init root
        - insert
            - similar to standart insert() in trie
            - at the end, mark last node's is_word = True and value = val
        - sum(prefix)
            - iterate over prefix
                - if prefix is not found, return 0
                - otherwise, call sum_helper(node) on the last node
        - sum_helper(node)
            - total += node.value
            - recursively calculates the sum of values for all keys that start from this prefix
                total += sum_helper(child)
            - return total

    Timeline:
        - understanding the problem 11:18
        - init design 11:20
        - break
        - redesign using gpt 21:30
        - coding 21:39
        - testing 21:43

"""


class TrieNode:
    def __init__(self, value=0):
        self.value = value
        self.children = {}
        self.is_word = False

# https://leetcode.com/problems/map-sum-pairs/
class MapSum:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, key: str, val: int) -> None:
        current = self.root
        for c in key:
            if c not in current.children:
                current.children[c] = TrieNode()
            current = current.children[c]
        current.is_word = True
        current.value = val

    def sum(self, prefix: str) -> int:
        current = self.root
        for c in prefix:
            if c not in current.children:
                return 0
            current = current.children[c]
        return self.sum_helper(current)

    def sum_helper(self, node: TrieNode):
        total = node.value
        for child in node.children.values():
            total += self.sum_helper(child)
        return total

# Your MapSum object will be instantiated and called as such:
# obj = MapSum()
# obj.insert(key,val)
# param_2 = obj.sum(prefix)