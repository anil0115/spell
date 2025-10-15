import os
import sys


class TrieNode:
    """A node in the Trie structure."""
    def __init__(self):
        
        self.children = {}
        
        self.is_end_of_word = False

class Trie:
    """A robust Prefix Tree (Trie) implementation."""
    def __init__(self):
        self.root = TrieNode()

    
    def insert(self, word: str) -> None:
        """Inserts a word into the Trie."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Checks if a word is completely present in the Trie."""
        node = self._traverse(word)
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """Checks if any word starts with the given prefix."""
        return self._traverse(prefix) is not None

    def _traverse(self, word_or_prefix: str) -> TrieNode | None:
        """Helper function to traverse the Trie."""
        node = self.root
        for char in word_or_prefix.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    
    def _find_all_words_from_node(self, node: TrieNode, current_prefix: str, word_list: list) -> None:
        """Recursive helper to find all words below a given node."""
        if node.is_end_of_word:
            word_list.append(current_prefix)

        for char, child_node in node.children.items():
            self._find_all_words_from_node(child_node, current_prefix + char, word_list)

    def autoComplete(self, prefix: str) -> list[str]:
        """
        Returns a list of ALL words that begin with the given prefix.
        The display limit is handled by the calling CLI.
        """
        results = []
        start_node = self._traverse(prefix)

        if start_node:
            self._find_all_words_from_node(start_node, prefix.lower(), results)
        
        return results

    
    def spellCheck(self, word: str) -> list[str]:
        """Suggests corrections for a word using one-edit distance."""
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

        return sorted(list(suggestions))



def load_dictionary(trie: Trie, filename: str) -> int:
    """Loads words from a text file into the Trie."""
    word_count = 0
    
    default_words = ["apple", "apply", "appetizer", "banana", "band", "cat", "car", "cart", "dog", "doughnut", "computer", "commuter", "code", "coding", "programming", "project", "python", "programmer", "program"]

    try:
        if not os.path.exists(filename):
            print(f" Warning: Dictionary file '{filename}' not found. Loading a small internal default set.")
            words = default_words
        else:
            with open(filename, 'r', encoding='utf-8') as f:
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



def run_cli():
    """The main function to run the interactive CLI."""
    trie = Trie()
    DICTIONARY_FILE = "dictionary.txt"

    print("\n--- Trie Project: Auto-Completion & Spell Check ---")
    count = load_dictionary(trie, DICTIONARY_FILE)
    print(f" Initialization complete. Loaded **{count}** words (case-insensitive).")
    print("-" * 55)
    print("Commands: **insert**, **search**, **prefix**, **auto**, **spell**, **help**, **exit**")

    
    while True:
        try:
            command_line = input("Trie-CLI> ").strip().split()
            if not command_line:
                continue

            command = command_line[0].lower()
            args = command_line[1:]

            if command == "exit":
                print("Exiting application. Goodbye! ")
                break
            
            elif command == "insert":
                if not args or not args[0].isalpha():
                    print("Usage: insert <word> (must be alphabetic)")
                    continue
                word = args[0]
                trie.insert(word)
                print(f"'{word.lower()}' inserted successfully.")

            elif command == "search":
                if not args:
                    print("Usage: search <word>")
                    continue
                word = args[0]
                if trie.search(word):
                    print(f" **'{word.lower()}'** found in the dictionary.")
                else:
                    print(f" **'{word.lower()}'** not found. Try 'spell {word}' for corrections.")

            elif command == "prefix":
                if not args:
                    print("Usage: prefix <prefix>")
                    continue
                prefix = args[0]
                if trie.startsWith(prefix):
                    print(f" A word starting with **'{prefix.lower()}'** exists.")
                else:
                    print(f" No word starts with **'{prefix.lower()}'**.")

            elif command == "auto":
                if not args:
                    print("Usage: auto <prefix>")
                    continue
                prefix = args[0]
                suggestions = trie.autoComplete(prefix) 
                
                print(f"\n--- Autocomplete Suggestions for '{prefix.lower()}' ({len(suggestions)} found) ---")
                
                
                display_limit = 10
                if suggestions:
                    print(", ".join(suggestions[:display_limit]))
                    if len(suggestions) > display_limit:
                        print(f"... and {len(suggestions) - display_limit} more. Use a longer prefix to narrow results.")
                else:
                    print("No completions found.")
                print("-" * 55)
            
            elif command == "spell":
                if not args:
                    print("Usage: spell <word>")
                    continue
                word = args[0]
                suggestions = trie.spellCheck(word)
                
                print(f"\n--- Spell Check for '{word.lower()}' ---")
                if isinstance(suggestions, list) and suggestions and suggestions[0].startswith("'"):
                    print(suggestions[0])
                elif suggestions:
                    print("Suggestions (1-edit distance):", ", ".join(suggestions))
                else:
                    print(f"No close matches found for '{word.lower()}'.")
                print("-" * 55)

            elif command == "help":
                print("\n--- Available Commands ---")
                print("  **insert <word>** : Add a new word to the dictionary.")
                print("  **search <word>** : Check if a word exists.")
                print("  **prefix <p>** : Check if any word starts with prefix 'p'.")
                print("  **auto <p>** : Get auto-completion suggestions for prefix 'p'.")
                print("  **spell <word>** : Get spelling corrections (1-edit distance).")
                print("  **help** : Show this command list.")
                print("  **exit** : Quit the program.")
                print("-" * 55)

            else:
                print(f"Unknown command: '{command}'. Type 'help' for commands.")

        except EOFError:
            print("\nExiting application. Goodbye! ")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    
    if not os.path.exists("dictionary.txt"):
        try:
            with open("dictionary.txt", "w") as f:
                f.write("programming\nproject\npython\nchallenge\ncomputer\ncommuter\ncoding\ncode\napple\napply\nappetizer\nbanana\nband\ncat\ncar\ncart\ndog\ndoughnut\nprogrammer\nprogram")
        except IOError:
            pass 

    run_cli()
