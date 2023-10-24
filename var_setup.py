import pygame
pygame.init()

num = 8 #Size of the board
width = 600
height = 600
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
size = width // num #size of 1 tile
pygame.display.set_caption('2 Player Chess') #Title of the window
font = pygame.font.Font('freesansbold.ttf', 21)
timer = pygame.time.Clock()
fps = 50 #To just determine how smooth your game goes
#game variables and images here
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations =  [(0,0), (1,0), (2, 0), (3,0), (4, 0), (5, 0), (6, 0), (7,0),
                    (0,1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)] #(column, row)
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations =  [(0,7), (1,7), (2, 7), (3,7), (4, 7), (5, 7), (6, 7), (7,7),
                    (0,6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = [] #To keep track of what pieces are captured
captured_pieces_black = []

#0 - whites turn, no selection, 1 - whites turn, piece selection, 2 - blacks turn no selection, 3 - blacks turn piece selection
turn_step = 0
selection = 1000
valid_moves = [] #once a piece is selected, we have to display all valid moves

#load in game pieces' images (queen, king, rook, knight, pawn, bishop) (each piece 2 times)
black_queen = pygame.image.load('downloads/images/bQ.png')
black_queen_small = pygame.transform.scale(black_queen, (60, 60))
#black_queen = pygame.image.scale(black_queen, (70,70)) dont think its needed rn
black_king = pygame.image.load('downloads/images/bK.png')
black_king_small = pygame.transform.scale(black_king, (60, 60))
black_rook = pygame.image.load('downloads/images/bR.png')
black_rook_small = pygame.transform.scale(black_rook, (60, 60))
black_bishop = pygame.image.load('downloads/images/bB.png')
black_bishop_small = pygame.transform.scale(black_bishop, (60, 60))
black_knight = pygame.image.load('downloads/images/bN.png')
black_knight_small = pygame.transform.scale(black_knight, (60, 60))
black_pawn = pygame.image.load('downloads/images/bp.png')
black_pawn_small = pygame.transform.scale(black_pawn, (60, 60))
white_queen = pygame.image.load('downloads/images/wQ.png')
white_queen_small = pygame.transform.scale(white_queen, (60, 60))
white_king = pygame.image.load('downloads/images/wK.png')
white_king_small = pygame.transform.scale(white_king, (60, 60))
white_rook = pygame.image.load('downloads/images/wR.png')
white_rook_small = pygame.transform.scale(white_rook, (60, 60))
white_bishop = pygame.image.load('downloads/images/wB.png')
white_bishop_small = pygame.transform.scale(white_bishop, (60, 60))
white_knight = pygame.image.load('downloads/images/wN.png')
white_knight_small = pygame.transform.scale(white_knight, (60, 60))
white_pawn = pygame.image.load('downloads/images/wp.png')
white_pawn_small = pygame.transform.scale(white_pawn, (60, 60))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop'] #this order is important because index needs to be aligned with the previous 2 lists

#check variables or flash counter
counter = 0
winner = ''
game_over = False
