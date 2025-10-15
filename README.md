README.txt

 Trie Data Structure and Text System

 Overview
This project implements a robust Trie (prefix tree) data structure in Python, applying it to build a basic auto-completion and spell-checking system via a command-line interface (CLI). The Trie provides highly efficient O(L) complexity for insertion, search, and prefix checking, where L is the length of the word/prefix.

 How to Run
1.  **Save the Code:** Save the provided Python code as a single file (e.g., `spell.py`).
2.  **Dictionary File:** The program expects a dictionary file named **`dictionary.txt`** in the same directory. This file should contain one word per line.
3.  **Execution:** Run the script from your terminal:
    `python trie_system.py`
4.  The system will initialize, load the dictionary, and enter the interactive CLI.

 Design Choices and Assumptions
| Component | Design Choice | Assumption/Note |
| :--- | :--- | :--- |
| **Trie Node** | Uses a standard Python dictionary for children. | Provides dynamic and readable character-to-node mapping. |
| **Case Handling** | All input and storage are converted to **lowercase**. | Ensures all operations are case-insensitive. |
| **Data Loading** | `load_dictionary` handles file reading and validation. | If `dictionary.txt` is missing, a small internal default dictionary is loaded for testing. |
| **Spell Check** | Uses a simplified **one-edit distance** algorithm. | Generates suggestions by considering one insertion, deletion, transposition, or substitution. This is effective for common typos. |
| **Auto-Complete** | The core function returns **all** matches. | The CLI display is limited to **10** suggestions for cleaner output, but the underlying function is unlimited. |

 CLI Commands
* **insert <word>** : Adds a new word.
* **search <word>** : Checks for exact word existence.
* **prefix <p>** : Checks if any word starts with prefix 'p'.
* **auto <p>** : Shows auto-completion suggestions for prefix 'p'.
* **spell <word>** : Shows spelling corrections.
* **help** : Displays the list of commands.
* **exit** : Quits the program.
