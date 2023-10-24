#Welcome to our 2 player chess game!!!
#This game follows all rules of chess!


#Part one: Set up variables, images and game loop

import pygame
pygame.init()
from var_setup import *
#for music
'''
pygame.mixer.music.load('master_da_blaster.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)
n = int(input('Enter number of songs you want to play: '))
for i in range(n):
    pygame.mixer.music.queue(input('Enter song name in .wav format: '))
'''
#draw main gameboard
def draw_board():
    for i in range(0, num - 1, 2):
        for j in range(0, num - 1, 2):
            rect = pygame.Rect(i*size, j*size, size, size)
            pygame.draw.rect(screen, '#f1e0ab', rect)
    for i in range(1, num, 2):
        for j in range(1, num, 2):
            rect = pygame.Rect(i*size, j*size, size, size)
            pygame.draw.rect(screen, '#f1e0ab', rect)
    pygame.draw.rect(screen, 'light gray', [0, 600, 800, size])
    pygame.draw.rect(screen, 'gold', [0, 600, 800, size], 5)
    pygame.draw.rect(screen, 'light gray', [600, 0, 200, 800])
    pygame.draw.rect(screen, 'gold', [600, 0, 200, 800], 5)

    status_text = ['White: select a piece!', "White: Select pieces' destination",
                   'Black: select a piece to move, my ni-', "Black: Select pieces' destination"]
    screen.blit(font.render(status_text[turn_step], True, 'white'), (120, 620))
    for i in range(9):
        pygame.draw.line(screen, 'black', (0,600//8 * i), (600, (600//8) * i), 2)
        pygame.draw.line(screen, 'black', ((600//8) * i,0), ((600//8) * i, 600), 2)
    screen.blit(font.render('You QUIT!?', True, 'orange'), (630, 610))
#draw pieces onto the board
def draw_pieces(): #btw draw_pieces needs to be after draw_board function since pieces are going to be on top of the board
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 600//8 + 10, white_locations[i][1] * 600//8 + 10))

        else:
            screen.blit(white_images[index], (white_locations[i][0] * 600//8 + 10, white_locations[i][1] * 600//8 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 600//8 + 1, white_locations[i][1] * 600//8 + 1,
                                                 600//8, 600//8], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 600//8 + 10, black_locations[i][1] * 600//8 + 10))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 600//8 + 10, black_locations[i][1] * 600//8 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 600//8 + 1, black_locations[i][1] * 600//8 + 1,
                                                  600//8, 600//8], 2)

'''def draw_position():
    for i in range(1,9):
        new_font = font.render(f'{i}', True, 'black')
        screen.blit(new_font, (size - i, size - i))'''
#function to check all valid options for the piece to move
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = [] #use moves_list to calculate and append to this list
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    #going to return list of all possible moves (valid)
    return all_moves_list

#Check all valid moves for all pieces
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and (position[0], position[1] + 1) not in black_locations \
            and position[1] < 7: #last condition to check if the piece on last square
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and (position[0], position[1] + 2) not in black_locations \
                and position[1] == 1: #last condition to check if the pawn in initial position
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and (position[0], position[1] - 1) not in black_locations \
                    and position[1] > 0 :  # last condition to check if the piece on last square
                moves_list.append((position[0], position[1] - 1))
                if (position[0], position[1] - 2) not in white_locations and (position[0], position[1] - 2) not in black_locations \
                        and position[1] == 6:  # last condition to check if the pawn in initial position
                    moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def check_passant(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        passant_coords = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        passant_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        pass
    else:
        passant_coords = (100000,100000)
    return passant_coords
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    for i in range(4): #down up right left
        path = True #to check if path is valid (taken by the rook)
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        elif i == 3:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) \
                not in friends_list and 0 <= position[0] + (chain*x) <= 7 and \
                0 <= position[1] + (chain*y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain*y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) \
                in enemies_list: #if enemy piece is there we can't go further
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    # 8 squares to check for knight
    # they can go 2 squares in one direction, then one to left or right
    #up - -1, down - 1, right - 2, left - 1
    targets = [(1,2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8): #for all 8 possible moves
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <=target[0] <= 7 and \
            0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list

def check_bishop(position, color): #similar to rook
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    # similar to rook but diagonal
    for i in range(4): #up-right, up-left, down-right, down-left
        path = True #to check if path is valid (taken by the bishop)
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        elif i == 3:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) \
                    not in friends_list and 0 <= position[0] + (chain * x) <= 7 and \
                    0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) \
                        in enemies_list:  # if enemy piece is there we can't go further
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    moves_list += second_list
    return moves_list

def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * (600//8) + 40, moves[i][1] * (600//8) + 40),5)

#to show captured pieces on the side
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (625, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (725, 5 + 50 * i))

#to flash the square of king if king in check
#under this function only you have to do the proper check moves
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'red', (white_locations[king_index][0] * size + 1,
                                                            white_locations[king_index][1] * size + 1 , 600//8, 600//8), 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * size + 1,
                                                            black_locations[king_index][1] * size + 1 , 600//8, 600//8], 5)

def draw_game_over():
    pygame.draw.rect(screen, 'brown', [130,250,400,50])
    screen.blit(font.render(f' W {winner} who wins the game!', True, 'orange'), (130,250))
    screen.blit(font.render(f'Press ENTER for a new game', True, 'orange'), (140,280))


#main game loop
black_options = check_options(black_pieces,black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else: counter = 0
    screen.fill('#b38a0d') #whatever color you want the screen's background to be and the dark squared
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 1000:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves) #to draw valid moves on the screen for user

    #event handling
    for event in pygame.event.get(): #getting everything that is happening in the computer like click, etc
        if event.type == pygame.QUIT: #the little X in the top of the window
            run = False
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        x_coord = event.pos[0] // (600//8) #event.pos tells the (x, y) coordinates
        y_coord = event.pos[1] // (600//8)
        click_coords = (x_coord, y_coord)
        if turn_step < 2:
            if click_coords == (8, 8) or click_coords == (9,8):
                winner = 'Black'
            if click_coords in white_locations:
                selection = white_locations.index(click_coords)
                if turn_step == 0:
                    turn_step = 1 #We're making turn_step = 1 to make the move
            if click_coords in valid_moves and selection != 1000:
                white_passant = check_passant(white_locations[selection], click_coords)
                white_locations[selection] = click_coords
                if click_coords in black_locations:
                    black_piece = black_locations.index(click_coords)
                    captured_pieces_white.append(black_pieces[black_piece])
                    if black_pieces[black_piece] == 'king':
                        winner = 'White'
                    #Now we are removing the piece from the board as well as the list
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)
                    #Now we are going to check for black and white pieces' options for next move
                black_options = check_options(black_pieces,black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                #Now we are going to let black play
                turn_step = 2
                selection = 1000
                valid_moves = [] #Because now valid moves are going to be different
        if turn_step >= 2:
            if click_coords == (8,8) or click_coords == (9,8):
                winner = 'White'
            if click_coords in black_locations:
                selection = black_locations.index(click_coords)
                if turn_step == 2:
                    turn_step = 3 #We're making turn_step = 1 to make the move
            if click_coords in valid_moves and selection != 1000:
                black_passant = check_passant(black_locations[selection], click_coords)
                black_locations[selection] = click_coords
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    captured_pieces_black.append(white_pieces[white_piece])
                    if white_pieces[white_piece] == 'king':
                        winner = 'Black'
                    #Now we are removing the piece from the board as well as the list
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                    #Now we are going to check for black and white pieces' options for next move
                black_options = check_options(black_pieces,black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                #Now we are going to let white play
                turn_step = 0
                selection = 1000
                valid_moves = [] #Because now valid moves are going to be different

    if event.type == pygame.KEYDOWN and game_over:
        if event.key == pygame.K_RETURN:
            game_over = False
            winner = ''
            white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                            'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
            white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                               (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]  # (column, row)
            black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                            'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
            black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                               (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

            captured_pieces_white = []  # To keep track of what pieces are captured
            captured_pieces_black = []
            turn_step = 0
            selection = 1000
            valid_moves = []
            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')
    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip() #throws everything onto the screen

pygame.quit()
#So until this code we should be able to get the window + background color + ability to quit
