import pygame
from math import cos, sin, radians
from random import randint



def asteroids_init():
    global screen, clock, coefficient, best_score
    pygame.init()

    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode([800, 600])
    clock = pygame.time.Clock()
    coefficient = 50
    best_score = 0

asteroids_init()
class Spaceship(pygame.sprite.Sprite):
    def __init__ (self):
        super(Spaceship, self).__init__()
        self.surf = pygame.image.load("spaceship.png").convert()
        width, height = self.surf.get_size()
        self.width = width
        self.surf = pygame.transform.scale(self.surf, (width//2, height//2))
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL )
        self.rect = self.surf.get_rect()
        self.rect.center = screen.get_rect().center
        self.Vx = 0
        self.Vy = 0
        self.angle = 0
        self.new_angle = 0
        
    def update(self, key):
        global lasers_num
        if key[pygame.K_UP]:
            #self.rect.move_ip(0, -5)
            self.Vy-=cos(radians(-self.angle))
            self.Vx+=sin(radians(-self.angle))
        if key[pygame.K_SPACE]:
            if lasers_num < 5:
                laser = Laser(self.rect.center, self.angle, self.width//2)
                lasers.add(laser)
                lasers_num += 1
        if key[pygame.K_LEFT]:
            self.new_angle = 15
            self.angle+=15
        if key[pygame.K_RIGHT]:
            self.angle-=15
            self.new_angle = -15
        if self.angle>360:
            self.angle%=360
        if self.angle <-360:
            self.angle = -1*(abs(self.angle)%360)
        #self.surf, self.rect = rot_center(self.surf, self.rect, self.new_angle)
        self.rect.move_ip(self.Vx, self.Vy)
        if self.rect.left<0:
            self.rect.right = 800
        if self.rect.top<0:
            self.rect.bottom = 600
        if self.rect.right > 800:
            self.rect.left = 0
        if self.rect.bottom > 600:
            self.rect.top = 0

class Laser(pygame.sprite.Sprite):
    def __init__(self, center_laser, angle, length=0):
        super(Laser, self).__init__()
        print(angle)
        self.surf = pygame.image.load("laser.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL )
        self.angle = angle
        print(center_laser)
        self.rect = self.surf.get_rect(center=(center_laser[0]+X, center_laser[1]+Y))
        #self.rect.centery+=sin(abs(self.angle))*length//2
        self.surf = pygame.transform.rotate(self.surf, self.angle)
        #print(angle)
    def update(self):
        global lasers_num
        self.rect.move_ip(-15*sin(radians(self.angle)), -15*cos(radians(self.angle)))
        if self.rect.left>800 or self.rect.right<0 or self.rect.top<0 or self.rect.bottom>600:
            self.kill()
            lasers_num -= 1
            
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, ratio=randint(3, 10), center = (0, 0)):
        super(Asteroid, self).__init__()
        self.surf = pygame.image.load("asteroid.png").convert()
        width, height = self.surf.get_size()
        self.width = width
        self.ratio = ratio
        self.surf = pygame.transform.scale(self.surf, (width//ratio, height//ratio))
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL )
        self.angle = randint(0, 360)
        var = randint(0, 3)
        self.Vx = 0
        self.Vy = 0
        if center != (0, 0):
            var = 4
            self.Vx = randint(-5, 5)
            self.Vy = randint(-5, 5)
        if var == 0:
            center = (0, randint(30, 570))
            self.Vx = randint(1, 10)
            self.VY = randint(-5, 5)
        if var == 1:
            center = (800, randint(30, 570))
            self.Vx = randint(-10, -1)
            self.VY = randint(-5, 5)
        if var == 2:
            center = (randint(30, 770), 0)
            self.Vx = randint(-5, 5)
            self.Vy = randint(1, 10)
        if var == 3:
            center = (randint(30, 770), 800)
            self.Vx = randint(-5, 5)
            self.Vy = randint(-10, -1)
        self.rect = self.surf.get_rect(center=center)
        self.surf = pygame.transform.rotate(self.surf, self.angle)
    def update(self):
        self.rect.move_ip(self.Vx, self.Vy)
        if self.rect.left>800 or self.rect.right<0 or self.rect.bottom<0 or self.rect.top>600:
            self.kill()

def game_asteroids():
    global lasers_num, X, Y, score, lasers, objects, spaceship, best_score
    lasers = pygame.sprite.Group()
    objects = pygame.sprite.Group()
    spaceship = Spaceship()

    X=0
    Y=0
    lasers_num = 0
    score = 0
    score_font = pygame.font.SysFont('Comic Sans MS', 30)
    score_surface = score_font.render(str(score), False, (0, 0, 0))
    while True:
        if score > best_score:
            best_score = score
        if pygame.sprite.spritecollideany(spaceship, objects):
            spaceship.kill()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        clock.tick(30)
        if randint(0, coefficient) == 0:
            objects.add(Asteroid())
        key = pygame.key.get_pressed()
        spaceship.update(key)
        lasers.update()
        objects.update()
        screen.fill((0,0,0))
        for sprite in lasers:
            screen.blit(sprite.surf, sprite.rect)
            exploded = pygame.sprite.spritecollide(sprite, objects, True)
            for asteroid in exploded:
                if asteroid.ratio<10:
                    score += 10
                    objects.add(Asteroid(asteroid.ratio+3, asteroid.rect.center), Asteroid(asteroid.ratio+1, asteroid.rect.center), Asteroid(asteroid.ratio+1, asteroid.rect.center))
                sprite.kill()
                lasers_num-=1
        if lasers_num <0:
            lasers_num = 0
        for sprite in objects:
            screen.blit(sprite.surf, sprite.rect)
        rot_image = pygame.transform.rotate(spaceship.surf, spaceship.angle)
        a = rot_image.get_rect()
        #print("left:",a.left, "right:", a.right, "top:", a.top, "down:", a.bottom)
        wing_center_x = a.left + a.width / 2
        wing_center_y = a.top + a.height / 2
        wing_left_x = a.left
        wing_left_y = wing_center_y
        wing_right_x = a.right
        wing_right_y = wing_center_y
        #printt((wing_left_x, wing_left_y), (wing_right_x, wing_right_y))
        X=(a.width-wing_left_x-wing_right_x)//2
        Y=(wing_left_y+wing_right_y)//2
        screen.blit(rot_image, spaceship.rect)     
        pygame.display.flip()
        spaceship.new_angle = 0
        font = pygame.font.Font(None, 48)

        # create a text surface with the desired color
        score_surface = score_font.render("SCORE: "+str(score)+"    laser battery: "+str(100-2*lasers_num*10)+"%", True, (0, 255, 0))

        # blit the text surface onto the screen
        screen.blit(score_surface, (250, 30))
        pygame.display.flip()
    menu_asteroids()


def menu_asteroids():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    # create the text object for the title
    title_text = font.render('Asteroids', True, (255, 255, 255))
    score_text = font.render('Best Score: '+str(best_score), True, (255, 255, 255))
    # set the position of the title
    title_pos = (400, 50)
    score_pos = (390, 150)

    button1_text = font.render('Play', True, (255, 255, 255))
    button2_text = font.render( 'Back to the infinite screen menu', True, (255, 255, 255))

    button1_pos = (250, 200)
    button2_pos = (250, 300)

    button_size = (400, 50)

    button1_rect = pygame.Rect(button1_pos, button_size)
    button2_rect = pygame.Rect(button2_pos, button_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    print('Button 1 clicked - pass')
                    game_asteroids()
                elif button2_rect.collidepoint(event.pos):
                    print('Button 2 clicked - pass')
                    exec("from menu import main\nmain()")
                    break
            screen.blit(title_text, title_pos)
            screen.blit(score_text, score_pos)
            pygame.draw.rect(screen, (0, 255, 0), button1_rect)
            screen.blit(button1_text, (button1_pos[0] + 10, button1_pos[1] + 10))
            pygame.draw.rect(screen, (0, 255, 0), button2_rect)
            screen.blit(button2_text, (button2_pos[0] + 10, button2_pos[1] + 10))
            pygame.display.update()

asteroids_init()
menu_asteroids()
