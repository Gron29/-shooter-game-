from pygame import *
from random import randint
from time import time as timer


mixer.init()
mixer.music.load("viod.mp3")
mixer.music.play()
fire_sound = mixer.Sound("shoot.mp3")



font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render("You win!", True, (255, 255, 255))
lose = font1.render("You lose..", True, (255, 255, 255)) 
font2 = font.SysFont("Arial", 36)



img_back = "sound.jpg"
img_hero = "hero.png"
img_enemy = "plane.png"
img_bullet = "bullet.png"


score = 0
lost = 0
max_lost = 10
life = 7
goal = 30


class GameSprite(sprite.Sprite):
    
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()


        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        


        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)




class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


win_width = 1000
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



ship = Player(img_hero, 5, win_height - 100, 80, 100, 18)



monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster) 


bullets = sprite.Group()



finish = False

run = True
rel_time = False
num_fire = 0
while run:
    
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 8   and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 8 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:

        window.blit(background,(0,0))



        text = font2.render("Счёт:" + str(score), 1, (225, 225, 225))
        window.blit(text, (10, 20))


        text_lose = font2.render("Пропущено:" + str(lost), 1, (225, 225, 255))
        window.blit(text_lose, (10, 50)) 


        
        ship.update()
        monsters.update()
        bullets.update()



        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1.5:
                reload = font2.render("Reloading...", 1, (0, 0, 225))
                window.blit(reload, (450, 660))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life -= 1
        
        if life == 0 or lost >= max_lost: 
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text_life = font1.render(str(life), 1, (255, 0, 0))
        window.blit(text_life, (950, 10))


        display.update()

    time.delay(50)