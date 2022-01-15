import random
import string
import time
import multiprocessing

# This code is written by Goutamkumar Tulajappa Kalburgi. NAU Email ID: gk325@nau.edu
# n = the size of board desired
# outFile = name of desired output file

n = 4
count = 0
dict_set = None  # dict_set = dictionary file converted into a set data structure.
words_found = {}


def generateBoard():
    """This method generates a random boggle board of given size.
    Returns the board file name."""
    file_name = input('Please enter the name of the desired output file\n')
    board = open(file_name, 'w')
    characters = string.ascii_uppercase
    for i in range(0, n):
        line = ' '.join(random.choices(characters, k=n))
        board.write((line + "\n"))
    board.close()
    return file_name


def loadBoard():
    """This method takes the file name of the board file and loads that into a board data structure.
    Returns a dictionary with the position as the key and the corresponding alphabet as the value. (x,y):'A'."""
    global n
    generate_board = int(input("Enter 0 if you would you like to generate a random boggle board of a specific size.\n"
                               "Enter 1 if you have an existing boggle board.\n"))
    n = int(input('Please enter the board size\n'))
    if generate_board == 0:
        file = generateBoard()
    else:
        file = input('Please enter the file name of the board.\n')
    board_file = open(file, 'r')
    board = {}
    for i in range(0, n):
        line = board_file.readline().strip().replace(' ', '')
        for j in range(0, n):
            position = (i, j)
            board[position] = line[j]
    return board


def printBoard(board):
    """This method takes in reference to a loaded board data structure and prints it out."""
    for i in range(0, n):
        for j in range(0, n):
            print(board[(i, j)], ' ', end='')
        print()


def possibleMoves(position):
    """This method takes in a current position (x, y) and generates all possible next positions (x, y) pairs in a
    set. """
    x, y = position[0], position[1]
    top = 0
    bottom = 0
    left = 0
    right = 0
    possible_next_positions = set()

    if x - 1 < 0:
        top = None

    if x + 1 > n - 1:
        bottom = None

    if y - 1 < 0:
        left = None

    if y + 1 > n - 1:
        right = None

    if top != None:
        top = (x - 1, y)
        possible_next_positions.add(top)

    if bottom != None:
        bottom = (x + 1, y)
        possible_next_positions.add(bottom)

    if left != None:
        left = (x, y - 1)
        possible_next_positions.add(left)

    if right != None:
        right = (x, y + 1)
        possible_next_positions.add(right)

    if top != None and left != None:
        top_left = (x - 1, y - 1)
        possible_next_positions.add(top_left)

    if top != None and right != None:
        top_right = (x - 1, y + 1)
        possible_next_positions.add(top_right)

    if bottom != None and left != None:
        bottom_left = (x + 1, y - 1)
        possible_next_positions.add(bottom_left)

    if bottom != None and right != None:
        bottom_right = (x + 1, y + 1)
        possible_next_positions.add(bottom_right)

    return possible_next_positions


def legalMoves(possible_moves, path):
    """This method takes in a list of possible moves as well as a path (list of x-y pairs) of places you've already been,
    and essentially subtracts the latter from the former"""
    legal_moves = possible_moves - set(path)
    return legal_moves


def examineState(board, current_position, path):
    global words_found
    """This method takes in a boggle board, a current position, a path up to that position and the dictionary file name.
    It adds the current position's tile to the path,
    computes the word now formed by that path,
    and returns a tuple of (<current word generated>, <yes/no depending on whether that word is in dictionary>)."""
    path += (current_position,)
    legal_moves = legalMoves(possibleMoves(current_position), path)
    word = ''
    for z in path:
        word += board[z]
        global count
        count += 1
    out = (word, isWordInDict(word))
    if out[1] == 'Yes':
        if len(word) in words_found:
            words_found[len(word)].add(word)
        else:
            words_found[len(word)] = set()
            words_found[len(word)].add(word)
    for move in legal_moves:
        examineState(board, move, path)


def isWordInDict(word):
    global dict_set
    if word in dict_set:
        return 'Yes'
    else:
        return 'No'


def loadDict(file_name):
    file = open(file_name, 'r')
    global dict_set
    dict_set = set(file.read().upper().split('\n'))


def main():
    board = loadBoard()
    start_time = time.time();
    print('Output from', n, 'x', n, 'Testing Boggle Board\n')
    printBoard(board)
    print('\nSolving Boggle Board...')
    loadDict('twl06.txt')
    processes = []
    for i in range(0, n):
        for j in range(0, n):
            path = ()
            print(i, j)
            # proc = multiprocessing.Process(target=examineState, args=(board, (i, j), path))
            # processes.append(proc)
            # proc.start()
            examineState(board, (i, j), path)
    # for p in processes:
    #     p.join()
    print('Boggle Solved!\n')
    print('Searched total of', count, 'moves in', time.time() - start_time, 'seconds\n')
    print('Words found:')
    all_words = set()
    for word_length in sorted(words_found.keys()):
        print(word_length, '- letter words:', ', '.join(str(item) for item in words_found[word_length]))
        all_words = all_words.union(words_found[word_length])
    print('\nFound', len(all_words), 'words in total.\nAlpha-sorted list words:')
    print(sorted(all_words))


if __name__ == '__main__':
    main()
