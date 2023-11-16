"""Utilities related to Boggle game."""

from random import choice
import string


class Boggle():

    def __init__(self):
        # This method is called when a new instance of the Boggle class is created.
        # It initializes the instance with a list of words read from a file.
        self.words = self.read_dict("words.txt")

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""
        # This method reads a file containing a list of words and returns a list of those words.
        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        dict_file.close()
        return words

    def make_board(self):
        """Make and return a random boggle board."""
        # This method creates a 5x5 boggle board by randomly selecting letters from the alphabet.
        board = []

        for y in range(5):
            row = [choice(string.ascii_uppercase) for i in range(5)]
            board.append(row)

        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""
        # This method checks if a given word is a valid word in the dictionary and/or the boggle board.
        # It returns "ok" if the word is valid in both, "not-on-board" if the word is not on the board but is in the dictionary,
        # and "not-word" if the word is not in the dictionary.
        word_exists = word in self.words
        valid_word = self.find(board, word.upper())

        if word_exists and valid_word:
            result = "ok"
        elif word_exists and not valid_word:
            result = "not-on-board"
        else:
            result = "not-word"

        return result

    def find_from(self, board, word, y, x, seen):
        """Can we find a word on board, starting at x, y?"""
        # This method is called recursively to find a word on the board starting at a given x, y position.
        # It returns True if the word is found and False otherwise.
        if x > 4 or y > 4:
            return

        # Base case: this isn't the letter we're looking for.
        if board[y][x] != word[0]:
            return False

        # Base case: we've used this letter before in this current path
        if (y, x) in seen:
            return False

        # Base case: we are down to the last letter --- so we win!
        if len(word) == 1:
            return True

        # Otherwise, this letter is good, so note that we've seen it,
        # and try of all of its neighbors for the first letter of the
        # rest of the word
        # This next line is a bit tricky: we want to note that we've seen the
        # letter at this location. However, we only want the child calls of this
        # to get that, and if we used `seen.add(...)` to add it to our set,
        # *all* calls would get that, since the set is passed around. That would
        # mean that once we try a letter in one call, it could never be tried again,
        # even in a totally different path. Therefore, we want to create a *new*
        # seen set that is equal to this set plus the new letter. Being a new
        # object, rather than a mutated shared object, calls that don't descend
        # from us won't have this `y,x` point in their seen.
        #
        # To do this, we use the | (set-union) operator, read this line as
        # "rebind seen to the union of the current seen and the set of point(y,x))."
        #
        # (this could be written with an augmented operator as "seen |= {(y, x)}",
        # in the same way "x = x + 2" can be written as "x += 2", but that would seem
        # harder to understand).
        seen = seen | {(y, x)}

        # adding diagonals
        if y > 0:
            if self.find_from(board, word[1:], y - 1, x, seen):
                return True

        if y < 4:
            if self.find_from(board, word[1:], y + 1, x, seen):
                return True

        if x > 0:
            if self.find_from(board, word[1:], y, x - 1, seen):
                return True

        if x < 4:
            if self.find_from(board, word[1:], y, x + 1, seen):
                return True

        # diagonals
        if y > 0 and x > 0:
            if self.find_from(board, word[1:], y - 1, x - 1, seen):
                return True

        if y < 4 and x < 4:
            if self.find_from(board, word[1:], y + 1, x + 1, seen):
                return True

        if x > 0 and y < 4:
            if self.find_from(board, word[1:], y + 1, x - 1, seen):
                return True

        if x < 4 and y > 0:
            if self.find_from(board, word[1:], y - 1, x + 1, seen):
                return True

        # Couldn't find the next letter, so this path is dead
        return False

    def find(self, board, word):
        """Can word be found in board?"""
        # This method checks if a given word can be found on the board.
        # It calls the find_from method for each position on the board and returns True if the word is found and False otherwise.
        for y in range(0, 5):
            for x in range(0, 5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        # We've tried every path from every starting square w/o luck.
        # Sad panda.
        return False
