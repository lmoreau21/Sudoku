# import pygame library
import pygame
import random
import copy

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
 
pygame.display.set_caption("Sudoku")

tiles_removed = 50
x = 0
y = 0
dif = 500 / 9
val = 0
#grid = [[8, 1, 9, 3, 2, 5, 4, 7, 6], [3, 7, 2, 4, 1, 6, 5, 8, 9], [5, 4, 6, 8, 9, 7, 1, 3, 2], [2, 3, 8, 9, 6, 4, 7, 1, 5], [7, 6, 4, 1, 3, 2, 9, 5, 8], [1, 9, 5, 2, 7, 8, 6, 4, 3], [4, 5, 1, 6, 8, 9, 3, 2, 7], [9, 2, 3, 7, 5, 1, 8, 6, 4], [6, 8, 7, 5, 4, 3, 2, 9, 1]]
grid = []
grid_solved = []
grid_org = []
def remove_others(temp_board, pos):
    value = temp_board[pos]
    #remove rows
    for i in range(pos + 1,(pos + (9-pos%9))):
        if value in temp_board[i]: temp_board[i].remove(value)
    #remove cols
    for i in range(pos+9,81,9):
        if value in temp_board[i]: temp_board[i].remove(value)
    #remove box
    for i in range(1,10-(int((9+pos)/9))):
        #print(pos,i)
        num = pos +(9*i)
        if(pos%3 == 2):
            num = pos - 2 +(9*i)
        if(pos%3 == 1):
            num = pos - 1 +(9*i)
        while((int((num/9)/3),int((num%9)/3)) == (int((pos/9)/3),int((pos%9)/3))):
            if value in temp_board[num]: 
                temp_board[num].remove(value)
            num+=1
    return temp_board
def create_board():
    numbers = [1,2,3,4,5,6,7,8,9]
    temp_board = [numbers.copy() for i in numbers*9]
    for i in range(0,81):
        if temp_board[i] != []:
            temp_board[i] = random.choice(temp_board[i]) 
            temp_board = remove_others(temp_board,i)
        else:
            return False
    for i in range(9):
        grid.append(temp_board[i*9:9*i+9])
    return True
def set_up():    
    worked = False
    while not worked: 
        worked = create_board()  
    global grid_solved,grid,grid_org
    grid_solved = copy.deepcopy(grid)
    #print(grid_solved)
    for i in range(tiles_removed):
        grid[random.randint(0,8)][random.randint(0,8)] = 0
    print(grid_solved)
    global run, flag1, flag2,rs, error,error_count
    run = True
    flag1 = 0
    flag2 = 0
    rs = 0
    error = 0
    error_count = 0

set_up()

font1 = pygame.font.SysFont("comicsans", 30)
font2 = pygame.font.SysFont("comicsans", 15)

def get_cord(pos):
    global x, y
    x = pos[0]//dif
    y = pos[1]//dif
 
# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)  

# Function to draw required lines for making Sudoku grid        
def draw():
    # Draw the lines
    for i in range (9):
        for j in range (9):
            if grid[i][j] != 0:
 
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))
 
                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid          
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)     
 
# Fill value entered in cell     
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))   
 
# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (255, 0, 0))
    screen.blit(text1, (20, 550)) 

 
# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it]== val:
            return False
        if m[it][j]== val:
            return False
    it = i//3
    jt = j//3
    for i in range(it * 3, it * 3 + 3):
        for j in range (jt * 3, jt * 3 + 3):
            if m[i][j]== val:
                return False
    return True
 
# Solves the sudoku board using solved  grid
def solve():
    for j in range (9):
        for i in range (9):
            pygame.event.pump()   

            grid[i][j] = grid_solved[i][j]
            # white color background
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(10)
            screen.fill((255, 255, 255))
            
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(10)   
                
# Display instruction for the game
def instruction():
    text1 = font2.render("Errors: "+str(error_count), 1, (0, 0, 0))
    text2 = font2.render("PRESS R FOR NEW GAME / E TO EMPTY / ENTER TO SOLVE", 1, (0, 0, 0))
    screen.blit(text1, (25, 510))       
    screen.blit(text2, (25, 530))
 
# Display options when solved
def result():
    text1 = font1.render("FINISHED PRESS R", 1, (0, 0, 0))
    screen.blit(text1, (20, 550))   

# The loop thats keep the window running
while run:
    # White color background
    screen.fill((255, 255, 255))
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        error = 0
        if event.type == pygame.QUIT:
            run = False 
        # Get the mouse position to insert number   
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        # Get the number to be inserted if key pressed   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x-= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x+= 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y-= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y+= 1
                flag1 = 1   
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2   
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9 
            if event.key == pygame.K_RETURN:
                flag2 = 1
        
            # If R pressed clear the sudoku board
            if event.key == pygame.K_e:
                rs = 0
                error = 0
                flag2 = 0
                grid =[
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            # If D is pressed reset the board to default
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                grid = []
                grid_solved = []
                print("loading:")
                set_up()
            if event.key == pygame.K_q:
                pygame.quit() 

    if flag2 == 1:
        solve()
        flag2 = 0   
        rs = 1
    if val != 0:           
        draw_val(val)
        if valid(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)]= val
            flag1 = 0
            
        else:
            grid[int(x)][int(y)]= 0
            error = 1
            error_count+=1
        val = 0   
       
    if error == 1:
        raise_error1() 
    if rs == 1:
        result()       
    draw() 
    if flag1 == 1:
        draw_box()      
    instruction()   
 
    # Update window
    pygame.display.update() 
 
# Quit pygame window   
pygame.quit()    