import pygame
import time
import random
import math
from pygame import mixer
mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Pyle Up!")

BG = pygame.image.load("road.jpg")
Player_Image = pygame.image.load("player_car.jpg")
Enemy_Car = pygame.image.load("enemy_car.jpg")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

CAR_WIDTH = 40
CAR_HEIGHT = 60
CAR_VEL = 5

CAR_VEL_INCREMENT_INTERVAL = 30  
CAR_VEL_INCREMENT_AMOUNT = 0.1   

HI_SCORE = 0

FONT = pygame.font.SysFont("Bahnschrift", 30)

mixer.music.load("music.mp3")
mixer.music.set_volume(0.2)
mixer.music.play(loops = -1)

enemy_car_positions = [250,300,350,400,450,500,550,600,650,700]

def draw(player, elapsed_time, cars):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time: {round(elapsed_time, 2)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    hi_score_words = FONT.render("Hi-Score:", 1, "white")
    WIN.blit(hi_score_words, (780,10))

    hi_score_numbers = FONT.render(f"{round(HI_SCORE, 2)} seconds", 1, "white")
    WIN.blit(hi_score_numbers, (780,60))

    pause_text_1 = FONT.render("Press ' p '", 1 , "white")
    pause_text_2 = FONT.render("to pause", 1, "white")
    WIN.blit(pause_text_1, (10,350))
    WIN.blit(pause_text_2, (10,400))
    
    WIN.blit(Player_Image, (player.x, player.y))

    for car in cars:
        WIN.blit(Enemy_Car, (car.x, car.y))
    
    pygame.display.update()

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return float(file.read())
    except (FileNotFoundError, ValueError):
        return 0.0


def main():
    global player
    global HI_SCORE
    global CAR_VEL
    HI_SCORE = load_high_score()
    run = True
    
    player = pygame.Rect(500, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    car_add_increment = 1000
    car_count = 0

    cars = []
    hit = False
    pause = False
    game_over = False

    car_vel_increment_timer = time.time()
    elapsed_time_since_increment = 0


    while run:
        car_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        elapsed_time_since_increment += car_count

        if elapsed_time_since_increment >= CAR_VEL_INCREMENT_INTERVAL * 1000:
            CAR_VEL += CAR_VEL_INCREMENT_AMOUNT
            elapsed_time_since_increment = 0
            car_vel_increment_timer  = time.time()
        


        if car_count > car_add_increment:
            for _ in range(random.randint(1,2)):
                car_x = random.choice(enemy_car_positions)
                car = pygame.Rect(car_x, -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT)
                cars.append(car)
            
            car_add_increment = max(200, car_add_increment - 10)
            car_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_c:
                    pause = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 230:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= 770:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL > 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= 800:
            player.y += PLAYER_VEL
        if keys[pygame.K_p]:
            pause = True
            while pause:
                
                mixer.music.pause()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_c:
                            pause = False
                            mixer.music.unpause()

                        
                pause_text = FONT.render("Game Paused - Press ' c ' to Continue", 1, "red")
                background_box = pygame.Rect(100, 100, 800, 600)
                pygame.draw.rect(WIN, "white", background_box)
                WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2, 250))
                pygame.display.update()
                if keys[pygame.K_c]:
                    pause = False


        for car in cars[:]:
            car.y += CAR_VEL
            if car.y > HEIGHT:
                cars.remove(car)
            elif car.y >= player.y and car.colliderect(player):
                cars.remove(car)
                hit = True
                

        if hit:
            game_over = True
            if elapsed_time > HI_SCORE:
                HI_SCORE = elapsed_time 
                save_high_score(HI_SCORE)
            lost_text = FONT.render("Game Over!", 1, "red")
            score_text = FONT.render(f"You were Accident Free for : {round(elapsed_time, 2)}s", 1, "red")
            background_box = pygame.Rect(100, 100, 800, 600)
            pygame.draw.rect(WIN, "white", background_box)
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, 200))
            WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 400))
            pygame.display.update()
            pygame.time.delay(4000)
            WIN.blit(BG, (0, 0))
            pygame.display.update()
            
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        game_over = False
                        break

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_y:
                            cars.clear()
                            player.x = 500
                            player.y = HEIGHT - PLAYER_HEIGHT
                            start_time = time.time()
                            elapsed_time = 0
                            car_add_increment = 1000
                            car_count = 0
                            hit = False
                            game_over = False
                            checker_time = 0


                play_again_text = FONT.render("Play Again?", 1, "red")
                play_again_confirm = FONT.render("(Press 'y' to Play Again)", 1, "red")
                background_box = pygame.Rect(100, 100, 800, 600)
                pygame.draw.rect(WIN, "white", background_box)
                WIN.blit(play_again_text, (WIDTH/2 - play_again_text.get_width()/2, 250))
                WIN.blit(play_again_confirm, (WIDTH/2 - play_again_confirm.get_width()/2, 400))
                pygame.display.update()
                

        draw(player, elapsed_time, cars)

    pygame.quit()


if __name__ == "__main__":
    main()
