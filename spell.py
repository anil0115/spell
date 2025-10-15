import os

class TrieNode:
    """A node in the Trie structure."""
    def __init__(self):
        # A dictionary to hold children. Key: character, Value: TrieNode
        self.children = {}
        # Boolean to mark if this node represents the end of a word
        self.is_end_of_word = False

class Trie:
    """A robust Prefix Tree (Trie) implementation."""
    def __init__(self):
        self.root = TrieNode()

   
    def insert(self, word: str) -> None:
        """Inserts a word into the Trie."""
        node = self.root
        for char in word.lower(): # Use lower() for case-insensitive operations
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Checks if a word is completely present in the Trie."""
        node = self._traverse(word)
        # Check if traversal was successful AND if the final node marks the end of a word
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """Checks if there is any word in the Trie that starts with the given prefix."""
        # A successful traversal to the end of the prefix means the prefix exists
        return self._traverse(prefix) is not None

    def _traverse(self, word_or_prefix: str) -> TrieNode | None:
        """Helper function to traverse the Trie based on a string."""
        node = self.root
        for char in word_or_prefix.lower():
            if char not in node.children:
                return None  # Path doesn't exist
            node = node.children[char]
        return node

    
    def _find_all_words_from_node(self, node: TrieNode, prefix: str, word_list: list) -> None:
        """Recursive helper to find all words below a given node."""
        if node.is_end_of_word:
            word_list.append(prefix)

        for char, child_node in node.children.items():
            self._find_all_words_from_node(child_node, prefix + char, word_list)

    def autoComplete(self, prefix: str) -> list[str]:
        """Returns a list of all words in the Trie that begin with the given prefix."""
        results = []
        start_node = self._traverse(prefix)

        if start_node:
            self._find_all_words_from_node(start_node, prefix.lower(), results)
        
        # Return a maximum of 10 suggestions for a cleaner CLI experience
        return results[:10]

       
    def spellCheck(self, word: str, max_distance: int = 1) -> list[str]:
        """
        Suggests corrections for a word not found in the Trie using a simple
        edit distance (one character difference).
        
        This uses a basic approach (insertion, deletion, substitution) for simplicity.
        """
        word = word.lower()
        suggestions = set()
        
        
        if self.search(word):
            return [f"'{word}' is spelled correctly!"]

        
        def edits1(w):
            letters    = 'abcdefghijklmnopqrstuvwxyz'
            splits     = [(w[:i], w[i:]) for i in range(len(w) + 1)]
            deletes    = [L + R[1:] for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
            replaces   = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts    = [L + c + R for L, R in splits for c in letters]
            return set(deletes + transposes + replaces + inserts)

        
        for edit_word in edits1(word):
            if self.search(edit_word):
                suggestions.add(edit_word)

        return sorted(list(suggestions)) or [f"No close matches found for '{word}'."]



def load_dictionary(trie: Trie, filename: str) -> int:
    """Loads words from a text file into the Trie."""
    word_count = 0
    # A simple example dictionary list for local testing if the file isn't available
    default_words = ["apple", "apply", "appetizer", "banana", "band", "cat", "car", "cart", "dog", "doughnut"]

    try:
        if not os.path.exists(filename):
            print("f⚠️ Warning: Dictionary file '{filename}' not found. Loading a small internal default set.")
            words = default_words
        else:
            with open(filename, 'r') as f:
                # Read words, strip whitespace, and filter out empty lines/invalid characters
                words = [line.strip().lower() for line in f if line.strip().isalpha()]
        
        for word in words:
            if word:
                trie.insert(word)
                word_count += 1
                
    except Exception as e:
        print(f"An error occurred during file loading: {e}. Loading internal default set.")
        for word in default_words:
            trie.insert(word)
            word_count += 1

    return word_count