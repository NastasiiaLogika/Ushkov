from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, 
                 player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Ігрова сцена:
window = display.set_mode((900, 500))
display.set_caption("Maze")
background = transform.scale(
    image.load("map.png"), 
    (900, 500)
)


# клас-спадкоємець для спрайту-гравця (керується стрілками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 900 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed


# клас-спадкоємець для спрайта-ворога (переміщається сам)
class Enemy(GameSprite):
     direction = "left"
     def update(self):
         if self.rect.x <= 470:
            self.direction = "right"
         if self.rect.x >= 900 - 85:
            self.direction = "left"
         if self.direction == "right":
            self.rect.x += self.speed
         else:
            self.rect.x -= self.speed



    # def update(self, player_rect):
       # if self.rect.x < player_rect.x:
       #     self.rect.x += self.speed
        #elif self.rect.x > player_rect.x:
        #    self.rect.x -= self.speed

      #  if self.rect.y < player_rect.y:
       #     self.rect.y += self.speed
    #    elif self.rect.y > player_rect.y:
     #       self.rect.y -= self.speed
            
            
# клас для спрайтів-перешкод
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        # картинка стіни - прямокутник потрібних розмірів та кольору
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        # кожен спрайт повинен зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y


    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        #draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))


# стіни
w1 = Wall(0, 0, 0, 124, 203, 106, 4)
#w2 = Wall(154, 205, 50, 100, 480, 350, 10)
#w3 = Wall(154, 205, 50, 100, 20, 10, 380)
w2 = Wall(0, 0, 0, 459, 170, 121, 4)
w3 = Wall(0, 0, 0, 702, 240, 106, 4)
w4 = Wall(23, 46, 30, 384, 278, 58, 67)


w11 = Wall(128, 128, 0, 120, 200, 8, 250)
w12 = Wall(128, 128, 0, 120, 200, 340, 8)
w13 = Wall(128, 128, 0, 455, 100, 8, 250)
w14 = Wall(128, 128, 0, 455, 100, 150, 8)
w15 = Wall(128, 128, 0, 660, 120, 8, 160)
w_final = Wall(255, 255, 255, 384, 278, 58, 67)

# написи
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))


# Персонажі гри:
player = Player('меджикарп.png', 5, 300, 4)
monster1 = Enemy('ворог.png', 700 - 80, 280, 2)
monster2 = Enemy('ворог.png', 200, 300, 0)


game = True
finish = False
clock = time.Clock()
FPS = 60


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False


    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster1.update()
        monster2.update()



        player.reset()
        monster1.reset()
        monster2.reset()
        


        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()

        w11.draw_wall()
        w12.draw_wall()
        w13.draw_wall()
        w14.draw_wall()
        w15.draw_wall()
        w_final.draw_wall()


    # Ситуація "Програш"
    if sprite.collide_rect(player, monster1) or sprite.collide_rect(player, w11) or sprite.collide_rect(player, w12) or sprite.collide_rect(player, w13) or sprite.collide_rect(player, w14) or sprite.collide_rect(player, w15) or sprite.collide_rect(player, monster2):
        finish = True
        window.blit(lose, (200, 200))


    # Ситуація "Перемога"
    if sprite.collide_rect(player, w_final):
        finish = True
        window.blit(win, (200, 200))
       

    display.update()
    clock.tick(FPS)

