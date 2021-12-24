import pygame
import random
import datetime

pygame.init()

display_wight = 800
display_height = 600

display = pygame.display.set_mode((display_wight, display_height))
pygame.display.set_caption('Multy world')

jump_sound = pygame.mixer.Sound(r'C:\\Users\\User\\Desktop\\MW\\Sounds\\Rrr.wav')
fall_sound = pygame.mixer.Sound(r'C:\\Users\\User\\Desktop\\MW\\Sounds\\Bdish.wav')
lose_sound = pygame.mixer.Sound(r'C:\\Users\\User\\Desktop\\MW\\Sounds\\lose.wav')
button_sound = pygame.mixer.Sound(r'C:\\Users\\User\\Desktop\\MW\\Sounds\\button.wav')
bullet_sound = pygame.mixer.Sound(r'C:\\Users\\User\\Desktop\\MW\\Sounds\\shot.wav')

icon = pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\icon.png')
pygame.display.set_icon(icon)

pygame.mixer.music.load(r'C:\\Users\\User\\Desktop\\MW\\Sounds\\backplay.wav')
pygame.mixer.music.set_volume(0.3)


cactus_img = [pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\cactus0.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\cactus1.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\cactus2.png')]
cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Stone0.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Stone1.png')
cloud_img = pygame.image.load(r'C:\Users\User\Desktop\MW\Grafics\\Cloud0.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Cloud1.png')

dino_img = [pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Dino00.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Dino01.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Dino02.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Dino03.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Dino04.png')]
bird_img = [pygame.image.load(r'C:\Users\User\Desktop\MW\Grafics\Bird0.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Bird1.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Bird2.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Bird3.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Bird4.png'), pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\Bird5.png')]


health_img = pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

bullet_img = pygame.image.load(r'C:\\Users\\User\\Desktop\\MW\\Grafics\\shot.png')
bullet_img = pygame.transform.scale(bullet_img, (22, 5))

img_counter = 0



class Object:
    def __init__(self, x, y, wight, image, speed):
       self.x = x
       self.y = y
       self.wight = wight
       self.image = image
       self.speed = speed

    def move(self):
        if self.x >= -self.wight:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, wight, image):
        self.x = radius
        self.y = y
        self.wight = wight
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, wight, height):
        self.wight = wight
        self.height = height
        self.inactive_clr = ()
        self.active_clr = ()

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.wight and y < mouse[1] < y + self.height:
                pygame.draw.rect(display, (176, 255, 51), (x, y, self.wight, self.height))

                if click[0] == 1:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(300)
                    if action is not None:
                        if action == quit:
                            pygame.quit()
                            quit()
                        else:
                            action()
        else:
            pygame.draw.rect(display, (13, 162, 58), (x, y, self.wight, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 8
        self.speed_y = 0
        self.dest_x = 0
        self.dest_y = 0

    def move(self):
        self.x += self.speed_x
        if self.x <= display_wight:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False

    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

        delta_x = dest_x - self.x
        count_up = delta_x // self.speed_x

        if self.y >= dest_y:
            delta_y = self.y - dest_y
            self.speed_y = delta_y / count_up
        else:
            delta_y = dest_y - self.y
            self.speed_y = -(delta_y / count_up)

    def move_to(self, reverse=False):
        if not reverse:
            self.x += self.speed_x
            self.y -= self.speed_y
        else:
            self.x -= self.speed_x
            self.y += self.speed_y

        if self.x <= display_wight and not reverse:
            display.blit(bullet_img, (self.x, self.y))
            return True
        elif self.x >= 0 and reverse:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False

class Bird:
    def __init__(self, away_y):
        self.x = random.randrange(550, 730)
        self.y = away_y
        self.wight = 105
        self.height = 55
        self.ay = away_y
        self.speed = 3
        self.dest_y = self.speed * random.randrange(20, 70)
        self.img_cnt = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False
        self.cd_shoot = 0
        self.all_bullets = []

    def draw(self):
        if self.img_cnt == 30:
            self.img_cnt = 0

        display.blit(bird_img[self.img_cnt // 5], (self.x, self.y))
        self.img_cnt += 1

        if self.come and self.cd_hide == 0:
            return 1
        elif self.go_away:
            return 2
        elif self.cd_hide > 0:
            self.cd_hide -= 1

        return 0

    def show(self):
       if self.y < self.dest_y:
           self.y += self.speed
       else:
           self.come = False
           self.go_away = True
           self.dest_y = self.ay

    def hide(self):
       if self.y > self.dest_y:
           self.y -= self.speed
       else:
           self.come = True
           self.go_away = False
           self.x = random.randrange(550, 730)
           self.dest_y = self.speed * random.randrange(20, 70)
           self.cd_hide = 80


#Переменные
usr_wight = 60
usr_height = 100
usr_x = display_wight // 3
usr_y = display_height - usr_height - 100

cactus_wight = 20
cactus_height = 70
cactus_x = display_wight - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0

cooldown = 0

eat = 0

def show_menu():
    menu_backgr = pygame.image.load(r'C:\Users\User\Desktop\MW\Grafics\fon.jpg')

    start_btn = Button(288, 70)
    quit_btn = Button(120, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_backgr, (0, 0))
        start_btn.draw(270, 200, 'Start game', start_game, 50)
        quit_btn.draw(358, 300, 'Quit', quit, 50)

        pygame.display.update()
        clock.tick(60)


def start_game():
    global scores, make_jump, jump_counter, usr_y, cooldown


    while game_cycle():
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100
        cooldown = 0


#Логика игры
def game_cycle():
    global make_jump, cooldown

    pygame.mixer.music.play(-1)

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(r'C:\Users\User\Desktop\MW\Grafics\Land.jpg')

    stone, cloud = open_random_objects()

    button = Button(110, 50)
    
    eat = 0

    all_btn_bullets = []
    all_ms_bullets = []

    bird1 = Bird(-80)
    bird2 = Bird(-40)

    all_birds = [bird1, bird2]

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)


        display.blit(land, (0, 0))
        print_text('Scores: ' + str(scores), 600, 10)
        print_text('Food:' + str(eat), 600, 70)


        draw_array(cactus_arr)
        move_objects(stone, cloud)


        draw_dino()

        if not cooldown:
            if keys[pygame.K_x]:
                pygame.mixer.Sound.play(bullet_sound)
                all_btn_bullets.append(Bullet(usr_x + usr_wight, usr_y + 28))
                cooldown = 50
                eat += 1
                
            elif click[0]:
                pygame.mixer.Sound.play(bullet_sound)
                add_bullet = Bullet(usr_x + usr_wight, usr_y + 28)
                add_bullet.find_path(mouse[0], mouse[1])

                all_ms_bullets.append(add_bullet)
                cooldown = 50
                eat += 1
        else:
            print_text('Cooldown time: ' + str(cooldown // 10), 500, 40)
            cooldown -= 1

        for bullet in all_btn_bullets:
            if not bullet.move():
                all_btn_bullets.remove(bullet)

        for bullet in all_ms_bullets:
            if not bullet.move_to():
                all_ms_bullets.remove(bullet)


        if check_collision(cactus_arr):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(lose_sound)
            # if not check_health():
            game = False

        # bird1.draw()
        # bird2.draw()

        draw_birds(all_birds)

        pygame.display.update()
        clock.tick(70)
    return game_over()


def jump():
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -25:
            pygame.mixer.Sound.play(fall_sound)

        usr_y -= jump_counter / 3
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    wight = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_wight + 20, height, wight, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    wight = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_wight + 300, height, wight, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    wight = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_wight + 600, height, wight, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < display_wight:
        radius = display_wight
        if radius - maximum < 50:
            radius += 280
        else:
            radius = maximum

        choice = random.randrange(0, 5)
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(250, 400)

        return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            wight = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, wight, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_wight, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_wight, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_wight, 500 + random.randrange(10, 80), stone.wight, img_of_stone)
    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_wight, random.randrange(10, 200), cloud.wight, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5],(usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color = (0, 0, 0,), font_type =r'C:\Users\User\Desktop\MW\Files\PINGPONG.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press enter to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
           paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449: # Маленький кактус
            if not make_jump:
                if barrier.x <= usr_x + usr_wight - 30 <= barrier.x + barrier.wight:
                    return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_wight - 35 <= barrier.x + barrier.wight:
                        return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.wight:
                        return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_wight - 5 <= barrier.x + barrier.wight:
                    return True
            elif jump_counter == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_wight - 5 <= barrier.x + barrier.wight:
                        return True
            elif jump_counter >= -1:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_wight - 35 <= barrier.x + barrier.wight:
                        return True
                else:
                    if usr_y + usr_height - 10 >= barrier.y:
                        if barrier.x <= usr_x + 5 <= barrier.x + barrier.wight:
                            return True
    return False


def count_scores(barriers):
    global scores, max_above
    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
             if barrier.x <= usr_x <= barrier.x + barrier.wight:
                above_cactus += 1
             elif barrier.x <= usr_x + usr_wight <= barrier.x + barrier.wight:
                 above_cactus += 1
             if scores == 20:
                 pygame.image.load('Night.jpg')
             elif scores == 50:
                 pygame.image.load('Land.jpg')

        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():
    global scores, max_scores
    if scores > max_scores:
        f = open(r'C:\\Users\\User\\Desktop\\MW\\Files\\game_scores.txt', 'w')
        max_scores = scores
        f.write(f'{max_scores}')
        f.close()

    stopped = True
    pygame.mixer.music.stop()

    return_btn = Button(288, 70)
    men_btn = Button(120, 70)

    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        return_btn.draw(270, 200, 'Play again', start_game, 50)
        men_btn.draw(350, 300, 'Menu', show_menu, 50)
        f = open(r'C:\\Users\\User\\Desktop\\MW\\Files\\game_scores.txt', 'r')
        maxik = f.readline()
        print_text('Max scores: ' + str(maxik), 300, 400)
        scores = 0


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
           return True
        if keys[pygame.K_ESCAPE]:
           return False

        pygame.display.update()
        clock.tick(15)


def draw_birds(birds):
    for bird in birds:
        action = bird.draw()
        if action == 1:
            bird.show()
        elif action == 2:
            bird.hide()


show_menu()
pygame.quit()
quit()