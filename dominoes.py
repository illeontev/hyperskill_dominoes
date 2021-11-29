import random

class DominoGame:

    def __init__(self):
        while True:
            self.stock_pieces = self.generate_fullset()
            self.player_pieces = self.get_pieces_for_player()
            self.computer_pieces = self.get_pieces_for_player()
            self.domino_snake = []
            self.game_finished = False

            common_list = self.player_pieces + self.computer_pieces
            max_double_index = self.get_max_double_index(common_list)
            if max_double_index != -1:
                break

        # if we found max double element in a computer list, that means
        # that player should make the next turn
        if max_double_index > 6:
            self.status = "player"
            self.domino_snake.append(self.computer_pieces.pop(max_double_index - 7))
        else:
            self.status = "computer"
            self.domino_snake.append(self.player_pieces.pop(max_double_index))


    def generate_fullset(self):
        fullset = []
        for i in range(7):
            for j in range(i, 7):
                puzzle = []
                puzzle.append(i)
                puzzle.append(j)
                fullset.append(puzzle)
        return fullset

    def get_pieces_for_player(self):
        pieces = []
        for i in range(7):
            piece = self.stock_pieces.pop(random.randint(0, len(self.stock_pieces) - 1))
            pieces.append(piece)
        return pieces

    def get_max_double_index(self, pieces):
        max_double = pieces[0]
        index = -1
        for i in range(1, len(pieces)):
            if pieces[i][0] == pieces[i][1] and pieces[i][0] > max_double[0]:
                max_double = pieces[i]
                index = i
        return index

    def print_domino_snake(self):
        if len(self.domino_snake) <= 6:
            for i in self.domino_snake:
                print(i, end='')
        else:
            print(f"{self.domino_snake[0]}{self.domino_snake[1]}{self.domino_snake[2]}"
                  f"...{self.domino_snake[-3]}{self.domino_snake[-2]}{self.domino_snake[-1]}")

    def print_player_pieces(self):
        for i in range(len(self.player_pieces)):
            print(f"{i + 1}:{self.player_pieces[i]}")


    def print(self):
        print("======================================================================")
        print("Stock size:", len(self.stock_pieces))
        print("Computer pieces: ", len(self.computer_pieces))
        print()
        self.print_domino_snake()
        print()
        self.print_player_pieces()
        print()
        self.check_game_status()

    def play(self):
        self.print()
        while not self.game_finished:
            self.make_turn()
            self.print()

    def get_optimal_turn(self, pieces):
        dict = {}
        for piece in pieces:
            if piece[0] in dict:
                dict[piece[0]] += 1
            else:
                dict[piece[0]] = 1
            if piece[1] in dict:
                dict[piece[1]] += 1
            else:
                dict[piece[1]] = 1

        points_list = []
        for piece in pieces:
            elem_list = []
            elem_list.append(piece)
            elem_list.append(dict.get(piece[0]) + dict.get(piece[1]))
            points_list.append(elem_list)

        points_list.sort(key=lambda elem: elem[1], reverse=True)

        koef = 0
        found_piece = None
        for piece_point in points_list:
            if self.domino_snake[0][0] in (piece_point[0][0], piece_point[0][1]):
                koef = -1
                found_piece = piece_point[0]
                break
            elif self.domino_snake[-1][1] in (piece_point[0][1], piece_point[0][1]):
                koef = 1
                found_piece = piece_point[0]
                break

        if koef != 0 and found_piece != None:
            for index in range(len(pieces)):
                piece = pieces[index]
                if piece[0] == found_piece[0] and piece[1] == found_piece[1]:
                    return (index + 1) * koef

        return 0

    def make_turn(self):
        if self.status == "player":
            while True:
                try:
                    turn = int(input())
                    if abs(turn) > len(self.player_pieces):
                        raise Exception
                    player_piece = self.player_pieces[abs(turn) - 1]
                    if turn > 0:
                        if self.domino_snake[-1][1] not in [player_piece[0],
                                                            player_piece[1]]:
                            print("Illegal move. Please try again.")
                            continue
                    elif turn < 0:
                        if self.domino_snake[0][0] not in [player_piece[0],
                                                           player_piece[1]]:
                            print("Illegal move. Please try again.")
                            continue
                    elif turn == 0 and not self.stock_pieces:
                        print("Illegal move. Please try again.")
                        continue

                    break
                except:
                    print("Invalid input. Please try again.")
            working_piece = self.player_pieces
            self.status = "computer"
        elif self.status == "computer":
            input()

            turn = self.get_optimal_turn(self.computer_pieces)
            working_piece = self.computer_pieces
            self.status = "player"

        if turn < 0:
            piece = working_piece.pop(abs(turn) - 1)
            if piece[1] != self.domino_snake[0][0]:
                piece[0], piece[1] = piece[1], piece[0]
            self.domino_snake.insert(0, piece)
        elif turn > 0:
            piece = working_piece.pop(abs(turn) - 1)
            if piece[0] != self.domino_snake[-1][1]:
                piece[0], piece[1] = piece[1], piece[0]
            self.domino_snake.append(piece)
        else:
            stock_piece = self.stock_pieces.pop(random.randint(0, len(self.stock_pieces) - 1))
            working_piece.append(stock_piece)

    def check_game_status(self):
        if not self.player_pieces:
            print("Status: The game is over. You won!")
            self.game_finished = True
        elif not self.computer_pieces:
            print("Status: The game is over. The computer won!")
            self.game_finished = True
        else:
            if self.domino_snake[0][0] == self.domino_snake[-1][1]:
                count = 0
                for piece in self.domino_snake:
                    if piece[0] == self.domino_snake[0][0]:
                        count += 1
                if count >= 8:
                    print("Status: The game is over. It's a draw!")
                    self.game_finished = True
                    return

            if self.status == "player":
                print("Status: It's your turn to make a move. Enter your command.")
            else:
                print("Status: Computer is about to make a move. Press Enter to continue...")

game = DominoGame()
game.play()






