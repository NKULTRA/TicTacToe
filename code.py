import random


class TicTacToe:

    cell_dict = {
        (1, 3): [0, 0], (2, 3): [0, 1], (3, 3): [0, 2],
        (1, 2): [1, 0], (2, 2): [1, 1], (3, 2): [1, 2],
        (1, 1): [2, 0], (2, 1): [2, 1], (3, 1): [2, 2],
    }
    commands = ("start", "exit", "easy", "medium", "hard", "user")
    move = ""

    def __init__(self):
        self.cells = list(" "*9)
        self.players = None
        self.x = 0
        self.o = 0

    def command(self):
        self.reshape()
        self.output()
        while True:
            com = [x for x in input("Input command: ").strip().split(" ")]
            if com[0] == "exit":
                exit()
            elif len(com) != 3 or com[0] != "start" \
                    or not all(elements in TicTacToe.commands[2:] for elements in com[1:]):
                print("Bad parameters!")
            else:
                self.players = com[1:]
                break
         self.game()

    def game(self):
        if all(x == "user" for x in self.players):
            while True:
                self.input()
        elif all(x in TicTacToe.commands[2:5] for x in self.players):
            while True:
                eval("self.move_"+self.players[0]+"()")
                eval("self.move_"+self.players[1]+"()")
        elif self.players[0] == "user":
            while True:
                self.input()
                eval("self.move_"+self.players[1]+"()")
        elif self.players[1] == "user":
            while True:
                eval("self.move_"+self.players[0]+"()")
                self.input()

    def reshape(self):
        cells = list()
        for i in range(0, 9, 3):
            cells.append([x for j in range(3) for x in self.cells[i + j]])
        self.cells = cells

    def output(self):
        print("-" * 9)
        for element in self.cells:
            print("| " + " ".join(letter for letter in element) + " |")
        print("-" * 9)

    def input(self):
        while True:
            try:
                coord_a, coord_b = (int(x) for x in input("Enter the coordinates: ").split(" "))
                coord_a, coord_b = TicTacToe.cell_dict[coord_a, coord_b]
            except ValueError:
                print("You should enter numbers!")
            except KeyError:
                print("Coordinates should be from 1 to 3!")
            except EOFError:
                print("You should enter numbers!")
            else:
                if self.cells[coord_a][coord_b] != " ":
                    print("This cell is occupied! Choose another one!")
                    continue
                else:
                    self.move_user(coord_a, coord_b)
                    break

    def move_user(self, coord_a, coord_b):
        if self.x <= self.o:
            self.cells[coord_a][coord_b] = "X"
            self.x += 1
        else:
            self.cells[coord_a][coord_b] = "O"
            self.o += 1
        self.output()
        if self.status(self.cells) != 0:
            self.end()

    def move_easy(self):
        print("Making move level 'easy'")
        while True:
            move_a, move_b = TicTacToe.cell_dict[random.randint(1, 3), random.randint(1, 3)]
            if self.cells[move_a][move_b] == " ":
                if self.x <= self.o:
                    self.cells[move_a][move_b] = "X"
                    self.x += 1
                else:
                    self.cells[move_a][move_b] = "O"
                    self.o += 1
                break
        self.output()
        if self.status(self.cells) != 0:
            self.end()

    def move_medium(self):
        print('Making move level "medium"')
        if self.x <= self.o:
            turn = "X"
            test = "O"
            self.x += 1
        else:
            turn = "O"
            test = "X"
            self.o += 1
        # can I win?
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == " ":
                    self.cells[i][j] = turn
                    if self.status(self.cells) == 0:
                        self.cells[i][j] = " "
                    else:
                        self.output()
                        self.end()
                        return None
        # can the other one win?
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == " ":
                    self.cells[i][j] = test
                    if self.status(self.cells) == 0:
                        self.cells[i][j] = " "
                    else:
                        self.cells[i][j] = turn
                        self.output()
                        return None
        # randommove
        while True:
            move_a, move_b = TicTacToe.cell_dict[random.randint(1, 3), random.randint(1, 3)]
            if self.cells[move_a][move_b] == " ":
                self.cells[move_a][move_b] = turn
                break
        self.output()
        if self.status(self.cells) != 0:
            self.end()

    def move_hard(self):
        print("Making move level 'hard'")
        if self.x <= self.o:
            turn = "X"
            self.x += 1
        else:
            turn = "O"
            self.o += 1
        board = [[self.cells[i][j] for j in range(3)] for i in range(3)]
        self.minimax(board, turn)
        coord_a, coord_b = TicTacToe.move
        self.cells[coord_a][coord_b] = turn
        self.output()
        if self.status(self.cells) != 0:
            self.end()

    def minimax(self, board, player):
        available = self.free(board)
        move = list(range(len(available)))
        if len(available) == 0 and self.status(board) == 3:
            return 0
        elif player == "X" and self.status(board) == 1:
            return 10
        elif player == "X" and self.status(board) == 2:
            return -10
        elif player == "O" and self.status(board) == 1:
            return -10
        elif player == "O" and self.status(board) == 2:
            return 10
        else:
            for i in range(len(available)):
                coord_a, coord_b = available[i]
                board[coord_a][coord_b] = player
                if player == "X":
                    move[i] += - self.minimax(board, "O")
                else:
                    move[i] += - self.minimax(board, "X")
                board[coord_a][coord_b] = " "
        TicTacToe.move = available[move.index(max(move))]
        return max(move)

    def free(self, board):
        if all([board[i].count(" ") == 0 for i in range(3)]):
            return []
        else:
            return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

    def status(self, board):
        if any([all([x == "X" for x in board[i]]) for i in range(3)]) \
                or any([all([x == "X" for i in range(3) for x in board[i][j]])for j in range(3)]) \
                or all(x == "X" for i in range(3) for x in board[i][i]) \
                or all(x == "X" for i in range(3) for x in board[i][2-i]):
            return 1
        elif any([all([x == "O" for x in board[i]]) for i in range(3)]) \
                or any([all([x == "O" for i in range(3) for x in board[i][j]])for j in range(3)]) \
                or all(x == "O" for i in range(3) for x in board[i][i]) \
                or all(x == "O" for i in range(3) for x in board[i][2-i]):
            return 2
        elif all([board[i].count(" ") == 0 for i in range(3)]):
            return 3
        return 0

    def end(self):
        if self.status(self.cells) == 1:
            print("X wins")
        elif self.status(self.cells) == 2:
            print("O wins")
        elif self.status(self.cells) == 3:
            print("Draw")
        again = TicTacToe()
        again.command()


# start of the game
def main():
    game = TicTacToe()
    game.command()
    

if __name__ == '__main__':
    main()
