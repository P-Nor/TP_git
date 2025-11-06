from pyray import *
from raylib import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_SPACE, KEY_KP_1, KEY_KP_2, KEY_KP_3, KEY_KP_4
import random

SIDE = 40
WIDTH = 20
HEIGHT = 20

snake = [[1,1],[2,1],[3,1]]

vitesse = [1,0]
fruit = [ WIDTH//2,HEIGHT//2]
perdu = False
score = 0
max_score = 0
vit = 5
frame = 0
frame_fruit = random.randint(50,200)
fruit_spec=[]
magic_fruit = False
start_game = False #permet d'avoir une fenêtre de début de jeu
Max = False #enregistre le score maximum si on ne quitte pas le jeu

level_1 = False
level_2 = False
level_3 = False
level_4 = False

init_window(SIDE * WIDTH,SIDE * HEIGHT,"Mon jeu") #créé une fenêtre sur l'écran 
set_target_fps(5) #nb d'images par secondes

while not window_should_close():  #boucle infinie (petite croix rouge de la fenêtre)

#DEBUT DU JEU ET CHOIX DES NIVEAUX
    while not start_game :
        if window_should_close():
            close_window()
        begin_drawing()
        clear_background(BLACK)
        draw_text("Welcome !", 10,10,60, WHITE)
        draw_text("Please select a level :",10,90,40,WHITE)
        #niveau 1
        draw_text("EASY :",10,135,40,RED)
        draw_text('Your speed is slow and you can go accross walls.',150,150,20,WHITE)
        draw_text("To play EASY, please press 1",10,180,20,WHITE)
        #niveau 2
        draw_text("MEDIUM 1:",10,235,40,RED)
        draw_text('Your speed increases and you can go accross walls.',220,250,20,WHITE)
        draw_text("To play MEDIUM 1, please press 2",10,280,20,WHITE)
        #niveau 3
        draw_text("MEDIUM 2:",10,325,40,RED)
        draw_text('Your speed is slow and you cannot go accross walls.',225,340,20,WHITE)
        draw_text("To play MEDIUM 2, please press 3",10,370,20,WHITE)
        #niveau 4
        draw_text("HARD:",10,425,40,RED)
        draw_text('Your speed increases and you cannot go accross walls.',140,440,20,WHITE)
        draw_text("To play HARD, please press 4",10,470,20,WHITE)

        #Rappel des règles : 
        draw_text('RULES :',10,520,40,RED)
        draw_text('The rules are quite straightforward. You need to eat the red fruit to gain ',10,580,20,WHITE)
        draw_text('points and make your snake grow. Sometimes, a yellow fruit will appear. This',10,610,20,WHITE)
        draw_text('is a magic fruit, it will make you win 5 points and make your snake grow',10,640,20,WHITE)
        draw_text('faster. It will however disappear if you do not eat it fast enough.',10,670,20,WHITE)
        draw_text('Depending on the level you choose, you can go accross walls (level 1 and 3),',10,700,20,WHITE)
        draw_text('or you will die if you try (level 2 and 4).',10,730,20,WHITE)
        draw_text('Difficulty will increase over time.',10,760,20,WHITE)
        end_drawing()

        if is_key_pressed(KEY_KP_1)== True : 
            level_1 = True
            start_game = True
        elif is_key_pressed(KEY_KP_2)== True : 
            level_2 = True
            start_game = True
        elif is_key_pressed(KEY_KP_3)== True : 
            level_3 = True
            start_game = True
        elif is_key_pressed(KEY_KP_4)== True : 
            level_4 = True
            start_game = True

    set_target_fps(vit)
    while not perdu :
        if window_should_close():
            close_window()
        #DETECTION DES TOUCHES
        if is_key_pressed(KEY_RIGHT)==True and vitesse != [-1,0]:  #Attention : le serpent ne peux pas faire demi-tour 
            vitesse = [1,0]
        elif is_key_pressed(KEY_LEFT)==True and vitesse != [1,0] : 
            vitesse = [-1,0]
        elif is_key_pressed(KEY_UP)==True and vitesse != [0,1]: 
            vitesse = [0,-1]
        elif is_key_pressed(KEY_DOWN)==True and vitesse != [0,-1]: 
            vitesse = [0,1]
        
        #APPARITION DU FRUIT SPECIAL    
        if frame == frame_fruit : 
            fruit_spec = [
                random.randint(0,WIDTH-1),
                random.randint(0,HEIGHT-1)
                ]
            while fruit_spec in snake : 
                fruit_spec = [
                random.randint(0,WIDTH-1),
                random.randint(0,HEIGHT-1)
                ]
            magic_fruit = True
        if frame == frame_fruit + 30 :
            frame = 0
            frame_fruit = random.randint(50,200)
            magic_fruit = False

        #ANIMATION
        vx, vy = vitesse
        hx, hy = snake[-1]
        new_head = [hx + vx, hy + vy]
        new_tail = [snake[0][0] - 1, snake[0][1] - 1] 
        frame += 1

        if new_head == fruit: #quand on mange un fruit
            snake = snake + [new_head]
            fruit = [
                random.randint(0,WIDTH-1),
                random.randint(0,HEIGHT-1)
                ]
            while fruit in snake : #pour éviter qu'il spawn dans le serpent
                fruit = [
                random.randint(0,WIDTH-1),
                random.randint(0,HEIGHT-1)
                ]
            score += 1
            if level_2 or level_4 :
                if score//2 == 0: #On augmente la difficulté progressivement (cas niveaux 2 et 4)
                    vit = vit + 1
                    set_target_fps(vit)
       
        #ANIMATION DU FRUIT SPECIAL
        elif magic_fruit and new_head == fruit_spec :
            snake = [new_tail] + snake + [new_head] 
            frame_fruit = random.randint(50,200)
            frame = 0
            score = score + 5
            magic_fruit = False
            if level_2 or level_4 : #on augmente la vitesse pour les niveaux 2 et 4
                vit = vit + 1 
                set_target_fps(vit)
        else :
            snake = snake[1:] + [new_head] #c'est plus facile de supprimer le dernier carré et d'en recréer un nouveau au niveau de la tête

        
        
        #CONDITIONS DE FIN DE PARTIE   
        if new_head in snake[:-1]: #le serpent se mord la queue (les coordonnées de la tête se trouvent dans le reste du corps du serpent)
            perdu = True
        if level_3 or level_4 : #conditions de fin de jeu pour les niveaux 3 et 4
            if new_head[0]<0 or new_head[0] >= WIDTH : 
                perdu = True
            elif new_head[1]<0 or new_head[1]>= HEIGHT :
                perdu = True

        
        #POUR FAIRE UN JEU CIRCULAIRE (cas niveaux 1 et 2)
        if level_1 or level_2 :
            if new_head[0]<0:
                new_head[0]= new_head[0]+WIDTH
            elif new_head[0]>=WIDTH:
                new_head[0]= new_head[0]-WIDTH
            elif new_head[1]<0:
                new_head[1]= new_head[1]+HEIGHT
            elif new_head[1]>=HEIGHT:
                new_head[1]= new_head[1]-HEIGHT
        

    
        #DESSIN
        begin_drawing()  #il faut tjrs commencer par begin drawing et finir par end drawing
        clear_background(BLACK)

        draw_rectangle(fruit[0]*SIDE,fruit[1]*SIDE,SIDE,SIDE,RED)
        draw_text(f"score = {score}", 10,10,20,WHITE) #f"nom : {variable}" permet d'insérer une variable dans un texte (il faut pas oublier f)

        for i, (x, y) in enumerate(snake) : #permet de retourner l'indice et la valeur de l'indice dans le tableau 
            color = PURPLE if i == len(snake) - 1 else DARKPURPLE
            draw_rectangle(x*SIDE+1,y*SIDE+1,SIDE-2,SIDE-2,color)
        
        if magic_fruit :
            draw_circle(fruit_spec[0]*SIDE + SIDE//2,fruit_spec[1]*SIDE + SIDE//2 ,SIDE//2, YELLOW)
    

        end_drawing()

    #GAME OVER  
    if score > max_score :
        max_score = score 
        Max = True
    begin_drawing()
    clear_background(BLACK)
    draw_text("You lost the game :(", 10,100,77,RED)
    draw_text("Press space to restart",200,320,20,WHITE)
    draw_text(f"Your score is {score}",200,200,20,WHITE)
    draw_text(f"Maximum score = {max_score}",200,240,20,WHITE)
    if Max :
        draw_text(f"Congratulations ! You have a new maximum score ! ", 50,280,20,WHITE)
    end_drawing()

    if is_key_pressed(KEY_SPACE)== True : 
        snake = [[1,1],[2,1],[3,1]]
        vitesse = [1,0]
        fruit = [ WIDTH//2,HEIGHT//2]
        score = 0
        vit = 5
        perdu = False
        Max = False
        start_game = False

close_window()

#Pour la prochaine fois : score, page de game over, fruit circulaire, super fruit, 
#jeu circulaire (le serpent peut passer aux bords)