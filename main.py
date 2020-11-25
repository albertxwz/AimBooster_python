import pygame
import random

screen_length = 800
screen_width = 600

def button(screen, font, txt, loc):
    textsuf = font.render(txt, True, (255, 255, 255))
    textrect = textsuf.get_rect()
    screen.blit(textsuf, loc)
    posx, posy = loc[0]-10, loc[1]-10
    lenx, leny = textrect[2] + 20, textrect[3] + 20
    pygame.draw.rect(screen, (255, 255, 255), (posx, posy, lenx, leny), 1)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0] and posx < mouse[0] < posx+lenx and posy < mouse[1] < posy+leny:
        return True
    return False

def dist(x1, y1, x2, y2):
    return ((x1-x2) ** 2 + (y1-y2) ** 2) ** 0.5


if __name__ == '__main__':

    # 初始化工作
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Aim Booster')



    # 相关设置
    screen = pygame.display.set_mode((screen_length, screen_width))
    clock = pygame.time.Clock()
    wordGroup = pygame.sprite.Group()
    font1 = pygame.font.SysFont('simsunnsimsun', 32)
    font2 = pygame.font.SysFont('simsunnsimsun', 24)
    img1 = pygame.image.load('1.png').convert_alpha()

    flag = False # 开始与否
    while True:
        # 开始界面和初始化
        clock.tick(30)
        screen.fill((0, 0, 0))
        screen.blit(img1, (280, 100))
        if (button(screen, font1, '开 始', (365, 400))):
            flag = True

        lives = 3 # 生命
        pertime = 1.00 # 出现时间
        bg = pygame.time.get_ticks() # 开始时间
        liscir = [] # 圆形个数
        miss = 0
        last = 0
        hold = 0
        holdtime = 5000 # 500 ms
        upradius = 40
        lowradius = 10
        click = 0 # 是否单击
        while flag:
            clock.tick(30)
            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if lives > 0:
                hold = pygame.time.get_ticks()-bg
                screen.blit(font2.render('时间：'+str(hold / 1000)+'s', True, (255, 255, 255)),
                            (10, 15))
                screen.blit(font2.render('生命：' + str(lives), True, (255, 255, 255)),
                            (350, 15))
                if button(screen, font2, '退出', (730, 15)):
                    flag = False
                    break

                # 产生圆
                if hold - last >= 1000 / pertime:
                    x, y = random.randint(10, screen_length-20), random.randint(40, screen_width)
                    liscir.append((x, y, hold))
                    last = hold

                mouse = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    click = click + 1
                else:
                    click = 0

                # 删除圆
                k = -1
                if click == 1:
                    for i in range(0, len(liscir)):
                        if k == -1 or dist(mouse[0], mouse[1], liscir[i][0], liscir[i][1]) < dist(mouse[0], mouse[1], liscir[k][0], liscir[k][1]):
                            k = i
                    if k > -1:
                        col = (0, 0, 255)
                        if dist(mouse[0], mouse[1], liscir[k][0], liscir[k][1]) > upradius*(1-abs((hold-liscir[k][2])/holdtime-0.5)):
                            col = (255, 0, 0)
                            lives = lives - 1
                        pygame.draw.circle(screen, col, liscir[k][:2], upradius*(1-abs((hold-liscir[k][2])/holdtime-0.5)))
                        liscir.pop(k)
                k = -1
                for i in range(0, len(liscir)):
                    pygame.draw.circle(screen, (255, 255, 255), liscir[i][:2], upradius*(1-abs((hold-liscir[i][2])/holdtime-0.5)))
                    if k == -1 and upradius*(1-abs((hold-liscir[i][2])/holdtime-0.5)) < lowradius:
                        k = i
                if k > -1:
                    pygame.draw.circle(screen, (255, 0, 0), liscir[k][:2],
                                       upradius*(1-abs((hold-liscir[k][2])/holdtime-0.5)))
                    miss = miss + 1
                    liscir.pop(k)
                    lives = lives - 1
            else:
                screen.blit(font1.render('持续时间：' + str(hold / 1000) + 's', True, (255, 255, 255)),
                            (200, 100))
                screen.blit(font1.render('错过：' + str(miss) + '次', True, (255, 255, 255)),
                            (200, 200))
                if button(screen, font1, '退出', (370, 300)):
                    flag = False
                    break

            pygame.display.update()
        # 设置退出的条件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        pygame.display.update()