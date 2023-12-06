## Welcome to Object-Oriented Chess: Wish Edtition! 
## I hope you enjoy. Quick note though...
## I wasn't able to code in: castling, checks, en passant, promotions, and checkmate... So please keep that in mind. 
## To be fair though, it wouldn't be wish edition with those things added, it'd just be chess!

import pygame 
import sys

## constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

## Colors (Using RGB)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

## Chess Piece Classes
## and also initializing their color and symbol. Capital if white, lowercase if black. 
class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'p' if color == 'black' else 'P')

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'r' if color == 'black' else 'R')

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'n' if color == 'black' else 'N')

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'b' if color == 'black' else 'B')

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'q' if color == 'black' else 'Q')

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'k' if color == 'black' else 'K')

## Code that creates and designs the chess board, and populates it with the chess pieces in a standard game of chess. If you're reading this... you're pretty cool. 
class ChessBoard:
    def __init__(self):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.initialize_pieces()
        self.selected_square = None
        self.turn = 'white'  # Initial turn

    def initialize_pieces(self):
        # Initialize pawns
        for i in range(BOARD_SIZE):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')

        # Initialize rooks
        self.board[0][0] = Rook('black')
        self.board[0][7] = Rook('black')
        self.board[7][0] = Rook('white')
        self.board[7][7] = Rook('white')

        # Initialize knights
        self.board[0][1] = Knight('black')
        self.board[0][6] = Knight('black')
        self.board[7][1] = Knight('white')
        self.board[7][6] = Knight('white')

        # Initialize bishops
        self.board[0][2] = Bishop('black')
        self.board[0][5] = Bishop('black')
        self.board[7][2] = Bishop('white')
        self.board[7][5] = Bishop('white')

        # Initialize queens
        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')

        # Initialize kings
        self.board[0][4] = King('black')
        self.board[7][4] = King('white')

     ## This draws the board! I think the colors weren't that bad of a choice, also makes it easier to show the letters that represent the pieces. 
    def draw_board(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board[row][col]
                if piece:
                    font_color = BLACK if piece.color == 'black' else WHITE
                    font = pygame.font.Font(None, 36)
                    text = font.render(piece.symbol, True, font_color)
                    screen.blit(text, (col * SQUARE_SIZE + SQUARE_SIZE // 3, row * SQUARE_SIZE + SQUARE_SIZE // 3))

                ## This code highlights the selected square to let you know you selected it. 
                if self.selected_square == (row, col):
                    pygame.draw.rect(screen, (0, 255, 0, 100), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

## Function that checks valid moves for pawns.
    def is_valid_move_pawn(self, start_row, start_col, target_row, target_col):
        selected_piece = self.board[start_row][start_col]
        target_piece = self.board[target_row][target_col]


        if selected_piece.color == 'black':
            if target_col == start_col and (target_row == start_row + 1 or (start_row == 1 and target_row == start_row + 2)) and target_piece is None:
                return True
            elif abs(target_col - start_col) == 1 and target_row == start_row + 1 and target_piece is not None and target_piece.color == 'white':
                return True
        elif selected_piece.color == 'white':
            if target_col == start_col and (target_row == start_row - 1 or (start_row == 6 and target_row == start_row - 2)) and target_piece is None:
                return True
            ## Code for pawn capturing diagnolly. (This was a pain in the butt to figure out)
            elif abs(target_col - start_col) == 1 and target_row == start_row - 1 and target_piece is not None and target_piece.color == 'black':
                return True
        return False
## Function that checks valid moves for rooks. (This was super easy)
    def is_valid_move_rook(self, start_row, start_col, target_row, target_col):
        selected_piece = self.board[start_row][start_col]
        target_piece = self.board[target_row][target_col]

        return (target_row == start_row or target_col == start_col) and target_piece is None or (
                target_piece is not None and target_piece.color != selected_piece.color)

## Function that checks valid moves for knights. (This was horrid to figure out.)
    def is_valid_move_knight(self, start_row, start_col, target_row, target_col):
        selected_piece = self.board[start_row][start_col]
        target_piece = self.board[target_row][target_col]

        return (
                abs(target_row - start_row) == 2 and abs(target_col - start_col) == 1 or
                abs(target_col - start_col) == 2 and abs(target_row - start_row) == 1
        ) and (target_piece is None or target_piece.color != selected_piece.color)

## Function that checks valid moves for bishops. (This wasn't so bad)
    def is_valid_move_bishop(self, start_row, start_col, target_row, target_col):
        selected_piece = self.board[start_row][start_col]
        target_piece = self.board[target_row][target_col]

        return abs(target_row - start_row) == abs(target_col - start_col) and (
                target_piece is None or target_piece.color != selected_piece.color)

## Function that checks valid moves for queens. (This was super easy since it was just rook and bishop mixed together. 
    def is_valid_move_queen(self, start_row, start_col, target_row, target_col):
        selected_piece = self.board[start_row][start_col]
        target_piece = self.board[target_row][target_col]

        return (
            target_row == start_row or
            target_col == start_col or
            abs(target_row - start_row) == abs(target_col - start_col)
        ) and (
            self.is_valid_move_rook(start_row, start_col, target_row, target_col) or
            self.is_valid_move_bishop(start_row, start_col, target_row, target_col)
        )

## King movement, super easy since it's just 1 space.
    def is_valid_move_king(self, start_row, start_col, target_row, target_col):
        selected_piece = self.board[start_row][start_col]
        target_piece = self.board[target_row][target_col]

        # King can move one square in any direction
        return abs(target_row - start_row) <= 1 and abs(target_col - start_col) <= 1 and (
                target_piece is None or target_piece.color != selected_piece.color)

    ## This code handles clicking and uses functions to check if a move is valid depending on the piece. 
    ## Ex. If the piece is a pawn, all ifs don't pass besides the is_valid_move_pawn if, it checks if the move is valid, if it isn't it fails to go through and returns nothing. 
    
    def handle_click(self, row, col):
        if self.selected_square is not None:
            start_row, start_col = self.selected_square

            # Validate the move based on the piece type
            if isinstance(self.board[start_row][start_col], Pawn):
                valid_move = self.is_valid_move_pawn(start_row, start_col, row, col)
            elif isinstance(self.board[start_row][start_col], Rook):
                valid_move = self.is_valid_move_rook(start_row, start_col, row, col)
            elif isinstance(self.board[start_row][start_col], Knight):
                valid_move = self.is_valid_move_knight(start_row, start_col, row, col)
            elif isinstance(self.board[start_row][start_col], Bishop):
                valid_move = self.is_valid_move_bishop(start_row, start_col, row, col)
            elif isinstance(self.board[start_row][start_col], Queen):
                valid_move = self.is_valid_move_queen(start_row, start_col, row, col)
            elif isinstance(self.board[start_row][start_col], King):
                valid_move = self.is_valid_move_king(start_row, start_col, row, col)
            else:
                valid_move = self.board[row][col] is None

            if valid_move:
                self.board[row][col] = self.board[start_row][start_col]
                self.board[start_row][start_col] = None
                self.turn = 'black' if self.turn == 'white' else 'white'  # Switch turns

            self.selected_square = None
        else:
            piece = self.board[row][col]
            if piece is not None and piece.color == self.turn:
                self.selected_square = (row, col)

## This sets the window width and height using the variable at the top of the code, the window name, and runs the functions that I need to get the game going, as well as handle everything else I need. 
def main():


    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Object-Oriented Chess: Wish Edition")

    chess_board = ChessBoard()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                row = event.pos[1] // SQUARE_SIZE
                col = event.pos[0] // SQUARE_SIZE
                chess_board.handle_click(row, col)

        screen.fill((255, 255, 255))
        chess_board.draw_board(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()


## Hello if you made it this far. I'm sorry it doesn't have images, or a proper check system, or an ending if you take the other King, but I hope you enjoyed it because it was a lot harder than it looked to code. Thank you!
