import time
import pygame
from threading import Thread
import os
from site1 import parse
H = 1024
W = 1280
pygame.mixer.pre_init(44100, -16, 1, H)

pygame.init()
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 30)
v = parse()
color = {'B':H//4,'G':H*2//4,'Y':H*3//4,'R':H*4//4}
colors = {'B':(0,0,255),'G':(0,255,0),'Y':(255,255,0),'R':(255,0,0)}
fps = 60
clock = pygame.time.Clock()
ball = pygame.image.load('1.png')
sound1 = pygame.mixer.Sound("./hitsound.wav")
# pygame.mouse.set_visible(False)


def music_play():
    sound1 = pygame.mixer.Sound("./blends.wav")
    pygame.mixer.find_channel(True).play(sound1)

class slider():
    def __init__(self, x, screen, velocity, color, length):
        self.r = 15
        self.b = 1
        self.length = length * velocity 
        self.x = x
        self.y = 0 - self.r - self.length
        self.screen = screen
        self.velocity = velocity
        self.color = colors[color]

    def move():
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y + self.length), self.r)
        pygame.draw.rect(self.screen, self.color, (self.x - self.r, self.y , self.r * 2, self.length))

    def move(self):
        self.y += self.velocity

    def __del__(self):
        self.y = H
        self.color = (0,0,0)
        self.b = 0


class note():
    def __init__(self, x, screen, velocity, color):
        self.r = 15
        self.x = x
        self.y = 0 - self.r
        self.screen = screen
        self.velocity = velocity
        self.color = colors[color]

    def draw(self):
        # pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        self.screen.blit(ball, (self.x - self.r, self.y - self.r))

    def move(self):
        self.y += self.velocity

    def __del__(self):
        self.y = H
        self.color = (0,0,0)
        self.r = 0


def main():
    
    combo = 0
    combo_counter = 0
    temp = 0
    notes = []
    sliders = []
    points = 0
    timer = 0
    timer_for_penalty = 0

    while True:
        screen = pygame.display.set_mode((W,H))

        draw_field(screen)

        points_temp = points

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYUP:
                # flag = False
                if i.key == pygame.K_q:
                    xtemp = H//4
                elif i.key == pygame.K_w:
                    xtemp = H*2//4
                elif i.key == pygame.K_e:
                    xtemp = H*3//4
                elif i.key == pygame.K_r:
                    xtemp = H*4//4
                elif i.key == pygame.K_u:
                    exit()
                else:
                    xtemp = -100


                for i in notes:
                    if i.y <  W*8//10 + 10 and i.y >  W*8//10 - 10 and i.x == xtemp:

                        pygame.mixer.find_channel(True).play(sound1)
                        points += 10 * combo_counter
                        timer_for_penalty = 0
                        i.__del__()


                for i in sliders:
                    i[1] += 1
                    if i[0].y < 465 and i[0].y + i[0].length > 445 and i[0].x == xtemp:
                        if i[1] >= 7:
                            i[1] = 0
                            points += 5 * combo_counter
                            timer_for_penalty = 0

            combo += points - points_temp

            if points == points_temp:
                if timer_for_penalty >= 30:
                        points -= 5
                        timer_for_penalty = 0
                        combo = 0
                        combo_counter = 0

            if combo >= 100 * combo_counter:
                if combo_counter < 10:
                    combo_counter += 1
                        # flag = True
                # if not flag:
                #     points -=1

        if v[0][2] == temp:
            if v[0][0] == 'N':
                notes.append(note(color[v[0][1]], screen, 3, v[0][1]))

            elif v[0][0] == 'S':
                sliders.append([slider(color[v[0][1]],screen, 3, v[0][1], v[0][3]),10])

            v.pop(0)
            if len(v) == 0:
                v.append((0, 0, -1))

        for i in notes:
            if i.y > H:
                del i
            else:
                i.draw()
                i.move()

        for i in sliders:
            if i[0].y > H:
                del i
            else:
                i[0].draw()
                i[0].move()

        textsurface = myfont.render(str(points), False, (255, 255, 255))
        screen.blit(textsurface,(50,10))

        textsurface = myfont.render(str(combo_counter), False, (255, 255, 255))
        screen.blit(textsurface,(50,80))

        pygame.display.flip()

        clock.tick(fps)

        temp += 1
        timer_for_penalty += 1

def draw_field(screen):
        pygame.display.set_caption("KekRythm")
        pygame.draw.rect(screen,(100, 100, 100), (0, 0, W, H))
        # pygame.draw.line(screen, (0, 0, 0), (0, 455), (W, 455), 1)
        pygame.draw.line(screen, (0, 0, 255), (H // 4, 0), (H // 4, H), 3)
        pygame.draw.line(screen, (0, 255, 0), (H // 2, 0), (H // 2, H), 3)
        pygame.draw.line(screen, (255, 255, 0), (H * 3 // 4, 0), (H * 3 // 4, H), 3)
        pygame.draw.line(screen, (255, 0, 0), (H, 0), (H, H), 3)

        pygame.draw.circle(screen, (255, 255, 255), (H // 4, W*8//10), 15, 1)
        # pygame.draw.circle(screen, (0, 0, 0), (128, 455), 15)
        pygame.draw.circle(screen, (255, 255, 255), (H * 2// 4, W*8//10), 15, 1)
        # pygame.draw.circle(screen, (0, 0, 0), (256, 455), 15)
        pygame.draw.circle(screen, (255, 255, 255), (H * 3 // 4, W*8//10), 15, 1)
        # pygame.draw.circle(screen, (0, 0, 0), (384, 455), 15)
        pygame.draw.circle(screen, (255, 255, 255), (H ,  W*8//10), 15, 1)
        # pygame.draw.circle(screen, (0, 0, 0), (H, 455), 15)


if __name__ == "__main__":
    # os.system('python3 music_play.py')
    polling_thread = Thread(target=main)
    spam_thread = Thread(target=music_play)
    polling_thread.start()
    spam_thread.start()
    # music = pygame.mixer.music.load('./music.mp3')
    # pygame.mixer.music.play()