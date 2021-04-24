import pygame
import pygame_menu
import random

WIDTH = 500
HEIGHT = 500
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MEMORY = [1, 2, 5, 10, 15, 20, 25, 50]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Informatics!")
clock = pygame.time.Clock()
bg = pygame.image.load('bg.jpg')

images_path = 'images/'
walkRight, walkLeft = [], []
for i in range(1, 7):
    walkRight.append(pygame.image.load(images_path + 'pygame_right_' + str(i) + '.png'))
    walkLeft.append(pygame.image.load(images_path + 'pygame_left_' + str(i) + '.png'))
playerStand = pygame.image.load((images_path + 'pygame_idle.png'))
heartImg = pygame.image.load((images_path + 'heart.png'))

img_memory = {}
for number in MEMORY:
    img_memory[number] = pygame.image.load(images_path + '/memory/' + str(number) + '_GB.png')

img_mob = pygame.image.load(images_path + 'garbage.png')


def game_show():
    def drawHearts(n):
        for i in range(n):
            screen.blit(heartImg, (HEIGHT - 20 * (i + 1), 4))


    font_name = pygame.font.match_font('arial')


    def draw_text(surf, score, size=20, x=5, y=5):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render('Счет: ' + str(score), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surf.blit(text_surface, text_rect)


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(playerStand, (60, 71))
            self.rect = self.image.get_rect()
            self.rect.topleft = 50, 420
            #self.image.blit(playerStand, self.rect.topleft)
            self.isJump = False
            self.jumpCount = 10
            self.animCount = 0
            self.left = False
            self.right = False
            self.speedx = 0
            self.life = 3
            self.memory = 0

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()

            if self.animCount + 1 >= 30:
                self.animCount = 0

            if keystate[pygame.K_LEFT]:
                self.speedx = -8
                self.left = True
                self.right = False
            elif keystate[pygame.K_RIGHT]:
                self.speedx = 8
                self.left = False
                self.right = True
            else:
                self.left = False
                self.right = False
            if not self.isJump:
                if keystate[pygame.K_UP]:
                    self.isJump = True
            else:
                if self.jumpCount >= -10:
                    if self.jumpCount < 0:
                        self.rect.y += (self.jumpCount ** 2) / 2
                    else:
                        self.rect.y -= (self.jumpCount ** 2) / 2
                    self.jumpCount -= 1
                else:
                    self.rect.y += 5
                    self.isJump = False
                    self.jumpCount = 10

            self.rect.x += self.speedx
            if self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
            if self.rect.left < 5:
                self.rect.left = 5

            if self.left:
                self.image = pygame.transform.scale(walkLeft[self.animCount // 5], (60, 71))
                self.animCount += 1
            elif self.right:
                self.image = pygame.transform.scale(walkRight[self.animCount // 5], (60, 71))
                self.animCount += 1
            else:
                self.image = pygame.transform.scale(playerStand, (60, 71))


    class Word(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.memory = random.choice(MEMORY)
            if self.memory > 10:
                size = (55, 20)
            else:
                size = (45, 20)
            self.image = pygame.transform.scale(img_memory[self.memory], size)
            #self.image = pygame.Surface((30, 40))
            #self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)
            self.speedx = random.randrange(-3, 3)
            #self.memory = random.choice(MEMORY)
            #self.image = pygame.transform.scale(img_memory[self.memory], (45, 15))

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(3, 6)


    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(img_mob, (35, 50))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 8)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(3, 6)



    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    words = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(3):
        w = Word()
        all_sprites.add(w)
        words.add(w)
    for i in range(2):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)


    running = True
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, mobs, True)
        for hit in hits:
            player.life -= 1
            print(player.life)
            if player.life < 0:
                running = False
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        hits = pygame.sprite.spritecollide(player, words, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.memory += hit.memory
            #print(player.memory)
            if player.life < 0:
                running = False
            w = Word()
            all_sprites.add(w)
            words.add(w)

        all_sprites.draw(screen)
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        drawHearts(player.life)
        draw_text(screen, player.memory)
        if player.memory > 200:
            running = False

    pygame.quit()
