import sys, pygame, os
#Set game parameters
WIDTH = 340
HEIGHT = 340
FPS = 20
running = True
turn = 1
turns_all = 1
game_state = 'Play'

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#Set up assets
player0 = '<path to white block image>/player0.png'
player1 = '<Path to exes image>/exes.png'
player2 = '<Path to ohs image>/ohs.png'
end_win = '<Path to winner graphic>/winner.png'
end_draw = '<Path to draw graphic>/draw.png'
all_players = [player0, player1, player2]

#Screen positions for exex and ohs
position1 = (60, 70)
position2 = (170, 70)
position3 = (285, 70)
position4 = (60, 160)
position5 = (170, 160)
position6 = (285, 160)
position7 = (60, 255)
position8 = (170, 255)
position9 = (285, 255)
all_pos = [position1, position2, position3, position4, position5, position6, position7, position8, position9]

#Create player class
class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self, coords, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        
#Initialize game
pygame.init()
pygame.display.set_caption('Tic-Tac-Toe')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Set up background and sprites
background = pygame.image.load('/home/jeff/Pictures/board.png').convert()
screen.blit(background, (0, 0))        #draw the background
coords = all_pos[0]
all_sprites = pygame.sprite.Group()
player = []
position = []

#Create player objects
for i in range(9):
    coords = all_pos[i]
    img = all_players[0]
    player.append(Player(coords, img)) 
    position.append(0)

#Add players and draw the initial screen
all_sprites.add(player)
all_sprites.draw(screen)
pygame.display.flip()

#Win/Draw logic function
def winner():
    w = []
    #Keep track of player positions
    w.append(position[0] + position[1] + position[2])
    w.append(position[3] + position[4] + position[5])
    w.append(position[6] + position[7] + position[8])
    w.append(position[0] + position[3] + position[6])
    w.append(position[1] + position[4] + position[7])
    w.append(position[2] + position[5] + position[8])
    w.append(position[0] + position[4] + position[8])
    w.append(position[2] + position[4] + position[6])
    
    #get all unique values in the list
    s = set(w)
    
    #Any row, column or diagonal indicates a win condition
    #No win conditions after move 9 are a draw
    if -3 in s or 3 in s:
        return "Win"
    elif turns_all == 9: 
        return "Draw"
    else:
        return "Play"

#Main game loop
while running:
    clock.tick(FPS) #This is set to 20 FPS just for fun
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False #Quit if window closed
            
        # If a right mouse click occurs on a sprite on the game board
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos #Capture the mouse position
            for j in range(9): #Loop through Sprites to find the selected collision
                player_rect = player[j].rect
                if player_rect.collidepoint(x, y):
                    if position[j] == 0:
                        turn = 2 if turn == 1 else 1 #Next Player's turn
                        #Assign a value for the last move to the list position
                        position[j] = 1 if turn = 1 else -1 
                        
                        coords = all_pos[j] #Grab the coordinates
                        img = all_players[turn] #Grab the correct ex or oh
                        #Continue playing by update the board with the correct
                        #ex or oh of the last move
                        if game_state == 'Play': 
                            player[j].image = pygame.image.load(img).convert()
                            player[j].image.set_colorkey(WHITE)
                            player[j].rect = player[j].image.get_rect()
                            player[j].rect.center = coords
                            
                        move_num = str(position[j])
                        turn_num = str(turns_all)
                        
                        #Update
                        all_sprites.update

                        #Draw screen
                        all_sprites.draw(screen)

                        #Flip display last
                        pygame.display.flip()
                        
                        #Determine win/draw/play condition
                        game_state = winner()
                        
                        #Display win and exit
                        if game_state == "Win":
                            #I thought this would remove sprites from the board
                            #but it doesn't. It does, however, place the 'win'
                            #sprite in the foreground
                            all_sprites.remove(player)
                            last_turn = Player((175, 155), end_win)
                            all_sprites.add(last_turn)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            pygame.time.wait(2500)
                            running = False
                            break
                        #Display draw and exit
                        elif game_state == "Draw":
                            last_turn = Player((175, 155), end_draw)
                            all_sprites.remove(player)
                            all_sprites.add(last_turn)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            pygame.time.wait(2500)
                            running = False
                            break
                        else:
                            pass
                        
                        
                        all_sprites.update
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        turns_all += 1 

                        
    #Update
    all_sprites.update
    
    #Draw screen
    all_sprites.draw(screen)
    
    #Flip display last
    pygame.display.flip()

pygame.quit()
