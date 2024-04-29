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
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed


# клас-спадкоємець для спрайта-ворога (переміщається сам)
class Enemy(GameSprite):
    # direction = "left"
    # def update(self):
    #     if self.rect.x <= 470:
    #         self.direction = "right"
    #     if self.rect.x >= 700 - 85:
    #         self.direction = "left"
    #     if self.direction == "left":
    #         self.rect.x -= self.speed
    #     else:
    #         self.rect.x += self.speed
    def update(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed
            
            
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
w1 = Wall(154, 205, 50, 100, 20, 10, 100)
#w2 = Wall(154, 205, 50, 100, 480, 350, 10)
#w3 = Wall(154, 205, 50, 100, 20, 10, 380)

# написи
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))


# Персонажі гри:
player = Player('sprite11.png', 5, 400, 4)
monster = Enemy('sprite22.png', 700 - 80, 280, 2)
final = GameSprite('sprite11.png', 700 - 120, 500 - 80, 0)


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
        # monster.update()
        monster.update(player.rect)


        player.reset()
        monster.reset()
        final.reset()


        w1.draw_wall()
        #w2.draw_wall()
        #w3.draw_wall()


    # Ситуація "Програш"
    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) :
        finish = True
        window.blit(lose, (200, 200))


    # Ситуація "Перемога"
    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (200, 200))
       

    display.update()
    clock.tick(FPS)


