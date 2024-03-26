# Importing necessary libraries
import json
import pygame
import socket
import sys
import time
import traceback

# Initial offset of game steps
initial_offset = 0

# Initialize the chess board as a 2D list
board = [['  ' for i in range(8)] for i in range(8)]

# Creates a chess piece class that shows what team a piece is on, what type of piece it is and whether or not it can be killed by another selected piece.
class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image

# JSON encoder for the Piece class
class PieceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Piece):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


# Creates instances of chess pieces, so far we got: pawn, king, rook and bishop
# The first parameter defines what team its on and the second, what type of piece it is
bp = Piece('b', 'p', 'images/b_pawn.png')
wp = Piece('w', 'p', 'images/w_pawn.png')
bk = Piece('b', 'k', 'images/b_king.png')
wk = Piece('w', 'k', 'images/w_king.png')
br = Piece('b', 'r', 'images/b_rook.png')
wr = Piece('w', 'r', 'images/w_rook.png')
bb = Piece('b', 'b', 'images/b_bishop.png')
wb = Piece('w', 'b', 'images/w_bishop.png')
bq = Piece('b', 'q', 'images/b_queen.png')
wq = Piece('w', 'q', 'images/w_queen.png')
bn = Piece('b', 'n', 'images/b_knight.png')
wn = Piece('w', 'n', 'images/w_knight.png')


#
def get_starting_order(offset):

    return {

        str((0, 0)): br if (offset == 0) else wr,
        str((1, 0)): bn if (offset == 0) else wn,
        str((2, 0)): bb if (offset == 0) else wb,
        str((3, 0)): bk if (offset == 0) else wk,
        str((4, 0)): bq if (offset == 0) else wq,
        str((5, 0)): bb if (offset == 0) else wb,
        str((6, 0)): bn if (offset == 0) else wn,
        str((7, 0)): br if (offset == 0) else wr,
        str((0, 1)): bp if (offset == 0) else wp,
        str((1, 1)): bp if (offset == 0) else wp,
        str((2, 1)): bp if (offset == 0) else wp,
        str((3, 1)): bp if (offset == 0) else wp,
        str((4, 1)): bp if (offset == 0) else wp,
        str((5, 1)): bp if (offset == 0) else wp,
        str((6, 1)): bp if (offset == 0) else wp,
        str((7, 1)): bp if (offset == 0) else wp,

        str((0, 2)): None,
        str((1, 2)): None,
        str((2, 2)): None,
        str((3, 2)): None,
        str((4, 2)): None,
        str((5, 2)): None,
        str((6, 2)): None,
        str((7, 2)): None,
        str((0, 3)): None,
        str((1, 3)): None,
        str((2, 3)): None,
        str((3, 3)): None,
        str((4, 3)): None,
        str((5, 3)): None,
        str((6, 3)): None,
        str((7, 3)): None,
        str((0, 4)): None,
        str((1, 4)): None,
        str((2, 4)): None,
        str((3, 4)): None,
        str((4, 4)): None,
        str((5, 4)): None,
        str((6, 4)): None,
        str((7, 4)): None,
        str((0, 5)): None,
        str((1, 5)): None,
        str((2, 5)): None,
        str((3, 5)): None,
        str((4, 5)): None,
        str((5, 5)): None,
        str((6, 5)): None,
        str((7, 5)): None,

        str((0, 6)): wp if (offset == 0) else bp,
        str((1, 6)): wp if (offset == 0) else bp,
        str((2, 6)): wp if (offset == 0) else bp,
        str((3, 6)): wp if (offset == 0) else bp,
        str((4, 6)): wp if (offset == 0) else bp,
        str((5, 6)): wp if (offset == 0) else bp,
        str((6, 6)): wp if (offset == 0) else bp,
        str((7, 6)): wp if (offset == 0) else bp,
        str((0, 7)): wr if (offset == 0) else br,
        str((1, 7)): wn if (offset == 0) else bn,
        str((2, 7)): wb if (offset == 0) else bb,
        str((3, 7)): wk if (offset == 0) else bk,
        str((4, 7)): wq if (offset == 0) else bq,
        str((5, 7)): wb if (offset == 0) else bb,
        str((6, 7)): wn if (offset == 0) else bn,
        str((7, 7)): wr if (offset == 0) else br

    }


# Initial arrangement of pieces on the chessboard
starting_order = get_starting_order(initial_offset)


# Function to create the initial chessboard
def create_board(board, offset):
    board[0 if (offset == 0) else 7] = [
        Piece('b', 'r', 'images/b_rook.png'),
        Piece('b', 'n', 'images/b_knight.png'),
        Piece('b', 'b', 'images/b_bishop.png'),
        Piece('b', 'q', 'images/b_queen.png'),
        Piece('b', 'k', 'images/b_king.png'),
        Piece('b', 'b', 'images/b_bishop.png'),
        Piece('b', 'n', 'images/b_knight.png'),
        Piece('b', 'r', 'images/b_rook.png')
    ]

    board[7 if (offset == 0) else 0] = [
        Piece('w', 'r', 'images/w_rook.png'),
        Piece('w', 'n', 'images/w_knight.png'),
        Piece('w', 'b', 'images/w_bishop.png'),
        Piece('w', 'q', 'images/w_queen.png'),
        Piece('w', 'k', 'images/w_king.png'),
        Piece('w', 'b', 'images/w_bishop.png'),
        Piece('w', 'n', 'images/w_knight.png'),
        Piece('w', 'r', 'images/w_rook.png')
    ]

    if (offset != 0):
        get = board[0][3], board[0][4]
        board[0][4], board[0][3] = get
        get = board[7][3], board[7][4]
        board[7][4], board[7][3] = get

    for i in range(8):
        board[1 if (offset == 0) else 6][i] = Piece('b', 'p', 'images/b_pawn.png')
        board[6 if (offset == 0) else 1][i] = Piece('w', 'p', 'images/w_pawn.png')
    return board


# Function to check if a position is within the boundaries of the board
def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True


# Function to convert the board to a readable string format
def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output


# Function to reset 'x's and killable pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convert_to_readable(board)


# Function to highlight valid moves on the board
def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try:
                    if board[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass
    return highlighted

# Function to check the team of a piece based on the move count
def check_team(index, moves):
    row, col = index
    return board[row][col].team == ('w' if (moves%2 == 0) else 'b')

# Function to select valid moves for a given piece and index
def select_moves(piece, index, moves):
    if check_team(index, moves):
        if piece.type == 'p':
            return highlight(pawn_moves(index))
        if piece.type == 'k':
            return highlight(king_moves(index))
        if piece.type == 'r':
            return highlight(rook_moves(index))
        if piece.type == 'b':
            return highlight(bishop_moves(index))
        if piece.type == 'q':
            return highlight(queen_moves(index))
        if piece.type == 'n':
            return highlight(knight_moves(index))


# Basically, check black and white pawns and checks the square above them.
# If its free that space gets an 'x' and if it is occupied by a piece of the opposite team then that piece becomes killable.
def pawn_moves(index):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if isinstance(board[positions[0]][positions[1]], Piece) and board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board


# This just checks a 3x3 tile surrounding the king. Empty spots get an 'x' and pieces of the opposite team become killable.
def king_moves(index):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if isinstance(board[index[0] - 1 + y][index[1] - 1 + x], Piece) and board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return board


# This creates 4 lists for up, down, left and right and checks all those spaces for pieces of the opposite team. The list comprehension is pretty long so if you don't get it just msg me.
def rook_moves(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if isinstance(board[positions[0]][positions[1]], Piece) and board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board


# Same as the rook but this time it creates 4 lists for the diagonal directions and so the list comprehension is a little bit trickier.
def bishop_moves(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if isinstance(board[positions[0]][positions[1]], Piece) and board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board


# applies the rook moves to the board then the bishop moves because a queen is basically a rook and bishop in the same position.
def queen_moves(index):
    board = rook_moves(index)
    board = bishop_moves(index)
    return board


# Checks a 5x5 grid around the piece and uses pythagoras to see if if a move is valid. Valid moves will be a distance of sqrt(5) from centre
def knight_moves(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if isinstance(board[index[0] + i][index[1] + j], Piece) and board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    return board


# Get king position
def king_position(team, board):
    # Find the king's position
    for i in range(len(board)):
        for j in range(len(board[0])):
            if isinstance(board[i][j], Piece) and board[i][j].type == 'k' and board[i][j].team == team:
                return i, j

# Function to check if a king is in check
def is_check(team, board, moves):
    # Check if the king is under attack
    for i in range(len(board)):
        for j in range(len(board[0])):
            if isinstance(board[i][j], Piece) and board[i][j].team != team:
                possible_moves = select_moves(board[i][j], (i, j), moves)  # Assuming it's white's move
                if possible_moves and king_position(team, board) in possible_moves:
                    return True  # King is in check
    return False  # King is not in check

# Function to check if a player is in checkmate
def is_checkmate(team, board):
    # Checkmate if the king is in check and there are no valid moves for any piece
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], Piece) and board[i][j].team == team and board[i][j].type == 'k':
                return False
    return True


# Window size
WIDTH = 800
# Colors
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(96, 96, 96)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)

# PyGame window initialization
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame_icon = pygame.image.load('images/w_queen.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Chess Client')

# Window font
font = pygame.font.SysFont(None, 40)


# Class definition for a node in the chessboard grid
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))
        draw_text(chr(ord('A') + self.row) + str(self.col + 1), pygame.font.SysFont(None, 20), BLACK, self.x + 15, self.y + 15)

    def setup(self, WIN):
        if starting_order[str((self.row, self.col))]:
            if starting_order[str((self.row, self.col))] == None:
                pass
            else:
                WIN.blit(pygame.image.load(starting_order[str((self.row, self.col))].image), (self.x + 16, self.y + 16))

# Function to create the chessboard grid
def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 == 1:
                grid[i][j].colour = GREY
    return grid

# Function to draw the grid on the display
def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

# Function to update the display with the current state of the chessboard
def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Function to find the node based on the mouse position
def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

# Function to display potential moves on the board
def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = grid[x][y].colour.lerp(BLUE, 0.25)

# Function to display a potential piece
def display_potential_piece(x, y, grid):
    grid[x][y].colour = GREEN

# Function to display a non-potential piece
def display_not_potential_piece(x, y, grid):
    grid[x][y].colour = RED

# Function to display a potential mate
def display_potential_mate(x, y, grid):
    grid[x][y].colour = YELLOW

# Function to perform a move on the chessboard
def Do_Move(OriginalPos, FinalPosition, WIN):
    starting_order[str(FinalPosition)] = starting_order[str(OriginalPos)]
    starting_order[str(OriginalPos)] = None

# Function to remove highlight from the grid
def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid

# Function to draw text on the display
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    WIN.blit(text_surface, text_rect)


# UI states
CONN_STATE = 0
MENU_STATE = 1
CODE_STATE = 2
AUTH_STATE = 3
GAME_STATE = 4
FAIL_STATE = 5
DONE_STATE = 6
IWIN_STATE = 7
LOST_STATE = 8


# Main function
def main(WIN, WIDTH):

    # Used globals
    global board, starting_order

    try:

        # Connection details
        server_ip = '127.0.0.1'
        server_port = 8080
        client_socket = None

        # Input box setup for connection details
        input_box_ip = pygame.Rect(300, 200, 200, 50)
        input_box_port = pygame.Rect(300, 300, 200, 50)
        input_box_connect = pygame.Rect(200, 500, 400, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active_ip = False
        active_port = False
        ip_text = server_ip
        port_text = str(server_port)

        # Buttons for connection state
        create_button = pygame.Rect(200, 200, 400, 50)
        connect_button = pygame.Rect(200, 400, 400, 50)

        # Input box setup for game code
        active_code = False
        code_text = ''
        input_box_code = pygame.Rect(300, 200, 200, 50)
        auth_button = pygame.Rect(200, 400, 400, 50)

        # Game state
        current_state = CONN_STATE

        # Moves and selection variables
        moves = 0
        selected = False
        piece_to_move=[]

        # Grid setup
        grid = make_grid(8, WIDTH)

        # Loop running
        running = True

        # Main loop
        while running:

            # Clear display
            WIN.fill(WHITE)

            # Process game events
            for event in pygame.event.get():

                # Handling quit event
                if event.type == pygame.QUIT:
                    # Stop loop
                    running = False
                    break

                # Handling left button click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_state == GAME_STATE:
                        if moves%2 != initial_offset:
                            # Skip if not our move
                            continue
                        remove_highlight(grid)
                        pos = pygame.mouse.get_pos()
                        y, x = Find_Node(pos, WIDTH)
                        if selected == False:
                            try:
                                possible = select_moves((board[x][y]), (x, y), moves)
                                display_potential_piece(x, y, grid)
                                display_potential_moves(possible, grid)
                                if is_check(('w' if (initial_offset != 0) else 'b'), board, moves):
                                    king_x, king_y = king_position(('w' if (initial_offset != 0) else 'b'), board)
                                    display_potential_mate(king_x, king_y, grid)
                                piece_to_move = x,y
                                selected = True
                            except:
                                piece_to_move = []
                                remove_highlight(grid)
                                display_not_potential_piece(x, y, grid)
                        else:
                            try:
                                if board[x][y].killable == True:
                                    row, col = piece_to_move
                                    board[x][y] = board[row][col]
                                    board[row][col] = '  '
                                    deselect()
                                    remove_highlight(grid)
                                    Do_Move((col, row), (y, x), WIN)
                                    moves += 1
                                    # Send the updated board state to the opponent
                                    try:
                                        client_socket.send(('BOARD\x00' + json.dumps(board, cls=PieceEncoder) + '\x00' + json.dumps(starting_order, cls=PieceEncoder)).encode())
                                    except Exception as e:
                                        print(e)
                                    if is_checkmate(('w' if (initial_offset != 0) else 'b'), board):
                                        current_state = IWIN_STATE
                                else:
                                    deselect()
                                    remove_highlight(grid)
                                    selected = False
                            except:
                                if board[x][y] == 'x ':
                                    row, col = piece_to_move
                                    board[x][y] = board[row][col]
                                    board[row][col] = '  '
                                    deselect()
                                    remove_highlight(grid)
                                    Do_Move((col, row), (y, x), WIN)
                                    moves += 1
                                    # Send the updated board state to the opponent
                                    try:
                                        client_socket.send(('BOARD\x00' + json.dumps(board, cls=PieceEncoder) + '\x00' + json.dumps(starting_order, cls=PieceEncoder)).encode())
                                    except Exception as e:
                                        print(e)
                                    if is_checkmate(('w' if (initial_offset != 0) else 'b'), board):
                                        current_state = IWIN_STATE
                                else:
                                    deselect()
                                    remove_highlight(grid)
                                    selected = False
                            selected = False

                    # Check if the input boxes are clicked
                    elif current_state == CONN_STATE:
                        if input_box_ip.collidepoint(event.pos):
                            active_ip = not active_ip
                            active_port = False
                            color = color_active if active_ip else color_inactive
                        if input_box_port.collidepoint(event.pos):
                            active_port = not active_port
                            active_ip = False
                            color = color_active if active_port else color_inactive
                        if input_box_connect.collidepoint(event.pos):
                            active_ip = False
                            active_port = False
                            color = color_inactive
                            server_ip = ip_text
                            # Attempt to connect to the server
                            try:
                                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                client_socket.connect((server_ip, server_port))
                                client_socket.setblocking(False)
                                current_state = MENU_STATE
                            except:
                                current_state = CONN_STATE
                    elif current_state == MENU_STATE:
                        # Set up as the WHITE
                        if create_button.collidepoint(event.pos):
                            # Create a new game
                            try:
                                client_socket.send('0'.encode())
                            except Exception as e:
                                print(e)
                            pygame_icon = pygame.image.load('images/w_queen.png')
                            pygame.display.set_icon(pygame_icon)
                            pygame.display.set_caption('Chess Client [WHITE]')
                            initial_offset = 0
                            code_text = '- - -'
                            current_state = CODE_STATE
                        # Set up as the BLACK
                        if connect_button.collidepoint(event.pos):
                            # Connect to existing game
                            pygame_icon = pygame.image.load('images/b_queen.png')
                            pygame.display.set_icon(pygame_icon)
                            pygame.display.set_caption('Chess Client [BLACK]')
                            initial_offset = 1
                            current_state = AUTH_STATE
                    # Check if the input box for game code is clicked
                    elif current_state == CODE_STATE:
                        if auth_button.collidepoint(event.pos):
                            # Initial arrangement of pieces on the chessboard
                            starting_order = get_starting_order(initial_offset)
                            create_board(board, initial_offset)
                            current_state = GAME_STATE
                    # Check if the input box for game code is clicked
                    elif current_state == AUTH_STATE:
                        if input_box_code.collidepoint(event.pos):
                            active_code = not active_code
                            color = color_active if active_code else color_inactive
                        if auth_button.collidepoint(event.pos):
                            if code_text != '- - -':
                                try:
                                    client_socket.send(code_text.encode())
                                except Exception as e:
                                    print(e)
                            # Initial arrangement of pieces on the chessboard
                            starting_order = get_starting_order(initial_offset)
                            create_board(board, initial_offset)
                            current_state = GAME_STATE
                    # Wrong game code
                    elif current_state == FAIL_STATE:
                        # Retry
                        if connect_button.collidepoint(event.pos):
                            current_state = CONN_STATE

                # Handling key event
                if event.type == pygame.KEYDOWN:
                    if active_ip or active_port or active_code:
                        if event.key == pygame.K_RETURN:
                            active_ip = False
                            active_port = False
                            active_code = False
                            color = color_inactive
                        elif event.key == pygame.K_BACKSPACE:
                            if active_ip:
                                ip_text = ip_text[:-1]
                            elif active_port:
                                port_text = port_text[:-1]
                            elif active_code:
                                code_text = code_text[:-1]
                        else:
                            if active_ip:
                                ip_text += event.unicode
                            elif active_port:
                                port_text += event.unicode
                            elif active_code:
                                code_text += event.unicode

            # Draw based on the current state
            if current_state == CONN_STATE:
                # Draw input boxes for connection details
                pygame.draw.rect(WIN, color, input_box_ip, 2)
                pygame.draw.rect(WIN, color, input_box_port, 2)
                pygame.draw.rect(WIN, BLACK, input_box_connect)
                draw_text('Enter Server IP:', font, BLACK, WIDTH // 2, 180)
                draw_text('Enter Server Port:', font, BLACK, WIDTH // 2, 280)
                draw_text('Connect to server', font, WHITE, input_box_connect.centerx, input_box_connect.centery)
                draw_text(ip_text, font, BLUE, input_box_ip.centerx, input_box_ip.centery)
                draw_text(port_text, font, BLUE, input_box_port.centerx, input_box_port.centery)

            elif current_state == MENU_STATE:
                # Draw buttons for menu state
                pygame.draw.rect(WIN, BLACK, create_button)
                pygame.draw.rect(WIN, BLACK, connect_button)
                draw_text('Create new game', font, WHITE, create_button.centerx, create_button.centery)
                draw_text('Connect to existing game', font, WHITE, connect_button.centerx, connect_button.centery)

            elif current_state == CODE_STATE:
                # Draw input box for game code and button for starting the game
                if code_text == '- - -':
                    try:
                        data = client_socket.recv(8192)
                        if data:
                            code_text = data.decode().split('\x00')[0]
                    except Exception as e:
                        print(e)
                draw_text(code_text, font, color_active, WIDTH // 2, 280)
                draw_text('Game code for opponent:', font, BLACK, WIDTH // 2, 180)
                pygame.draw.rect(WIN, BLACK, auth_button)
                draw_text('Authenticate to game', font, WHITE, auth_button.centerx, auth_button.centery)

            elif current_state == AUTH_STATE:
                # Draw input box for game code and button for starting the game
                draw_text('Game code from opponent:', font, BLACK, WIDTH // 2, 180)
                pygame.draw.rect(WIN, color, input_box_code, 2)
                pygame.draw.rect(WIN, BLACK, auth_button)
                draw_text(code_text, font, BLUE, input_box_code.centerx, input_box_code.centery)
                draw_text('Authenticate to game', font, WHITE, auth_button.centerx, auth_button.centery)

            elif current_state == GAME_STATE:
                # Draw the chess grid and update the display
                WIN.fill(WHITE)
                # Wait input from server
                try:
                    data = client_socket.recv(8192)
                    if data:
                        data_array = data.decode().split('\x00')
                        # Try again
                        if 'UNKNOWN' == data_array[0]:
                            # Close connection
                            try:
                                client_socket.close()
                            except Exception as e:
                                print(e)
                            current_state = FAIL_STATE
                        # Start game
                        if 'START' == data_array[0]:
                            pass
                        # Board update
                        if 'BOARD' == data_array[0]:
                            moves += 1
                            table = json.loads(data_array[1])
                            order = json.loads(data_array[2])
                            for x in range(len(grid)):
                                for y in range(len(grid[0])):
                                    board[len(board) - 1 - x][len(board) - 1 - y] = Piece(**table[x][y]) if ('  ' != table[x][y]) else '  '
                                    starting_order[str((len(board) - 1 - x, len(board) - 1 - y))] = Piece(**order[str((x, y))]) if (None != order[str((x, y))]) else None
                            if is_checkmate(('w' if (initial_offset == 0) else 'b'), board):
                                current_state = LOST_STATE
                except Exception as e:
                    WIN.fill(WHITE)
                update_display(WIN, grid, 8, WIDTH)

            elif current_state == FAIL_STATE:
                # Draw win text
                draw_text('WRONG GAME CODE', font, RED, WIDTH // 2, 180)
                # Draw buttons for menu state
                pygame.draw.rect(WIN, BLACK, connect_button)
                draw_text('Retry', font, WHITE, connect_button.centerx, connect_button.centery)

            elif current_state == IWIN_STATE:
                # Draw win text
                draw_text('YOU WIN', font, GREEN, WIDTH // 2, 280)

            elif current_state == LOST_STATE:
                # Draw win text
                draw_text('YOU LOST', font, RED, WIDTH // 2, 280)

            # Redraw screen
            pygame.time.Clock().tick(60)
            pygame.display.flip()

        # Close connection
        client_socket.close()

    # Quit on exception
    except Exception as e:
        print(e)
        print(traceback.format_exc())

    # Close all
    pygame.display.quit()
    pygame.quit()
    sys.exit()


# Run main function
main(WIN, WIDTH)

