import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import pyautogui as auto
import pygame
import sys
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)

# Eye Blink Detection Variables
cap = cv2.VideoCapture(1)
detector = FaceMeshDetector(maxFaces=1)
idList = [23, 24, 25, 26, 22, 110, 157, 158, 159, 160, 161, 130, 243]
RatioList = []
blinkCounter = 0
counter = 0

# Dino Game Variables
game_speed = 15
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

ground = pygame.image.load("ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))
cloud = pygame.image.load("cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()  # Initialize ptero_group

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Dino1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Dino2.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"DinoDucking1.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"DinoDucking2.png"), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 280
        self.gravity = 8.5
        self.ducking = False

    def jump(self):
        if self.rect.centery >= 360:
            self.rect.centery -= self.velocity

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360:
            self.rect.centery += self.gravity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"cacti/cactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos =  350
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("Ptero1.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("Ptero2.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 15
    cloud_group.empty()
    obstacle_group.empty()

dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Initialize Pygame mixer
pygame.mixer.init()
death_sfx = pygame.mixer.Sound("sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("sfx/jump.mp3")

CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

while True:
    # Eye Blink Detection Logic
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    if not success:
        continue
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 2, (0, 255, 0), 1, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]

        cv2.line(img, leftUp, leftDown, (0, 0, 255), 1)
        cv2.line(img, leftLeft, leftRight, (0, 0, 255), 1)
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        ratio = 100 * lengthVer / lengthHor
        RatioList.append(ratio)
        if len(RatioList) > 3:
            RatioList.pop(0)
        ratioAvg = sum(RatioList) / len(RatioList)
        print(ratioAvg)

        if ratioAvg < 31.5 :
            dinosaur.jump()
            jump_sfx.play()

    cv2.imshow("Eye Blink Detection", img)
    cv2.waitKey(1)

    # Dino Game Logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
                if game_over:
                    game_over = False
                    game_speed = 15
                    player_score = 0

    screen.fill("white")

    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.015
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 100)  # Increase the range for less frequent obstacles
            if obstacle_random in range(1, 4):  # Adjust the range to reduce the number of cacti
                new_obstacle = Cactus(1280, 340)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(5, 7):  # Adjust the range to reduce the number of pteros
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)  # Draw pteros

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed

        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))

        if ground_x <= -1280:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()
