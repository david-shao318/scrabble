# Scrabble Word Finder

class Scrabble:
    def __init__(self, words: list[str]):
        """
        initialize trie
        :param words: list of words to use as dictionary
        """
        
        # declare instance variables
        self._length = self._letters = self.possible_words = None
        self._root = {}  # trie

        # create trie
        # for every letter in every word, create nested dicts if not already present
        # at the end of every word, insert '_end_': '_end_'
        for word in words:
            curr_dict = self._root
            for letter in word:
                curr_dict = curr_dict.setdefault(letter, {})
            curr_dict['_end_'] = '_end_'

        # trie structure is a set of nested dicts (value), with each letter as the key
        # the '_end_' denotes the end of a word
        # e.g., below is the indefinite article 'a' and the noun 'aa'
        # self._root = { 'a': { '_end_': '_end_',
        #                       'a': { '_end_': '_end_', ... },
        #                       ... },
        #                'b': { ... },
        #                ... }

        
    def scrabble(self, letters: str, length: int) -> list[str]:
        """
        find possible words, given a group of letters
        :param letters: scrabble letters available
        :param length: length of words to find
        :return: possible words
        """
        
        # reset variables
        self._length, self._letters, self.possible_words = length, {}, []
        
        # transfer string into dict (key: letter, value: number of instances of letter)
        for letter in letters:
            self._letters[letter] = self._letters.get(letter, 0) + 1
        
        # find possible words from root trie
        self._recursive_find(self._root)
        
        return self.possible_words

    def _recursive_find(self, root: dict, prefix: str = ''):
        """
        :param root: dictionary trie
        :param prefix: letters above current root
        """
        
        # for every letter in root, test if possible to make the word, given user letters
        for letter in root:
            if letter in self._letters:
                if prefix.count(letter) < self._letters[letter]:
                    # add letter on to prefix
                    new_prefix = prefix + letter
                    
                    # if not desired length, call self with new root and new prefix
                    if len(new_prefix) < self._length:
                        self._recursive_find(root[letter], new_prefix)
                    
                    # elif reached end of word, add new prefix (full word) to output list
                    elif '_end_' in root[letter]:
                        self.possible_words.append(new_prefix)

                        
    def autocomplete(self, prefix: str) -> list[str]:
        """
        autocomplete words, given a prefix
        :param prefix: starting letters of word
        :return: list of possible words
        """
        self.possible_words = []  # reset list
        
        # locate base root at prefix
        root = self._root
        for letter in prefix:
            if letter in root:
                root = root[letter]
            else:
                return []  # if non-existent prefix
        
        # autocomplete prefix, given current root
        self._recursive_auto(root, prefix)
        
        return self.possible_words
    
    def _recursive_auto(self, root: dict, prefix: str = ''):
        """
        :param root: dictionary trie
        :param prefix: letters above current root
        """
        
        # for every letter in root trie:
        for letter in root:
            
            # if at end, add prefix (full word) to output list
            if letter == '_end_':
                self.possible_words.append(prefix)
            
            # else, call self with new root and new prefix
            else:
                self._recursive_auto(root[letter], prefix + letter)


# driver code
if __name__ == '__main__':
    try:
        # create Scrabble object with list of words from dictionary text file
        try:
            with open(input('Enter dictionary file: ')) as word_list:
                scrabbler = Scrabble(word_list.read().split())
        except OSError:
            print('Unable to find file.')
            raise EOFError

        while True:
            usr_input = input('\nEnter letters: ')

            # if last char in input is '_', autocomplete
            if usr_input[-1] == '_':
                print(scrabbler.autocomplete(usr_input[:-1]))

            # otherwise, ask for word length; scrabble
            else:
                try:
                    usr_length = int(input('Enter length: '))
                    if usr_length < 1:
                        raise ValueError
                except ValueError:  # data sanitize
                    print('Input error. Length must be a positive integer.')
                    continue
                print(scrabbler.scrabble(usr_input, usr_length))

    # to exit
    except (KeyboardInterrupt, EOFError):
        print('\nExiting...')
