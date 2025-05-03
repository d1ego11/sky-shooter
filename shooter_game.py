#Создай собственный Шутер!

from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption("shooter")
clock = time.Clock()
game = True
background = transform.scale(image.load("background.png"), (700, 500))
countscore = 0
countlose = 0

font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont("Arial", 60)
win = font2.render("PERFECT VICTORY", True, (50, 205, 50))
lose = font2.render("YOU LOSE", True, (178, 34, 34))

bullets = sprite.Group()

mixer.init()
firesound = mixer.Sound("firesound.ogg")
finish = False


#класс который самый крутой
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = "left"
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fire(self):
        pass


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-10, self.rect.top+20, -15, 20, 15)
        bullets.add(bullet)
        

class Enemy(GameSprite):  
    def update(self):
        self.rect.y += self.speed
        global countlose
        if self.rect.y > 520:
           self.rect.y = 0
           self.rect.x = randint(1, 650)
           countlose += 1
           


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
        


enemy1 = Enemy("enemy.png", randint(1, 630), randint(0, 100), randint(1, 1), 100, 100)
enemy2 = Enemy("enemy.png", randint(1, 630), randint(0, 100), randint(1, 1), 100, 100)
enemy3 = Enemy("enemy.png", randint(1, 630), randint(0, 100), randint(1, 1), 100, 100)
enemy4 = Enemy("enemy.png", randint(1, 630), randint(0, 100), randint(1, 1), 100, 100)
enemy5 = Enemy("enemy.png", randint(1, 630), randint(0, 100), randint(1, 1), 100, 100)
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)


'''
        if self.rect.y <= 370:
            self.direction = "right"
        if self.rect.y >= 640:
            self.direction = "left"
        if self.direction == "left":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
                                    '''


plane = Player("plane.png", 300, 400, 5, 80, 80)
enemy = Enemy("enemy.png", 300, 0, 2, 100, 100)

# игровой цикл
while game:
    window.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:            #или сделать выстрел на K_SPACE
                plane.fire()
                print("снаряд был выпущен")
                firesound.play()


    if not finish:
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        for c in sprites_list:
            countscore = countscore + 1
            enemy = Enemy("enemy.png", randint(1, 630), randint(0, 100), randint(1, 2), 100, 100)
            enemies.add(enemy)


        if sprite.spritecollide(plane, enemies, False) or countlose >= 15:
            finish = True
            window.blit(lose, (200,200))

        

        textlose = font1.render("misses: " + str(countlose), 1, (127, 255, 212))
        textscore = font1.render("score: " + str(countscore), 1, (127, 255, 212))
        window.blit(textlose, (0,0))
        window.blit(textscore, (0, 40))
        
        bullets.update()
        plane.update()
        plane.reset() 
        enemies.update()
        enemies.draw(window)
        bullets.draw(window)

        if countscore >= 30:
            finish = True
            window.blit(win, (150,200))
        
        if sprite.spritecollide(plane, enemies, False) or countlose >= 15:
            finish = True
            window.blit(lose, (200,200))

        
        display.update()
        clock.tick(100)

